"""
Module for the blocklist filter.

More information about this filter can be found in its Class docstring.
"""

from re import split

from .check_modes import perform_mode_check
from .filter import Filter

POSSIBLE_MODES: "list[str]" = ["normal", "strict", "tolerant"]


class Blocklist(Filter):
    """
    Filter text for blocked words. Works better in combination with
    `BypassDetector`.

    - `Blocklist.mode`: How to handle incoming text.
        - `normal`: search for profane words adjacent to punctuation or spaces.
        - `strict`: search for any occurence of a profane word. WARNING: this
        might detect words like "classic" as they contain parts of a profane
        words.
        - `tolerant`: simply replace the problematic words.
    - `Blocklist.blocklist`: a set with words that shall be blocked.
    - `Blocklist.ignore_regex`: a regular expression that matches punctuation
    characters for splitting the string in non-strict mode.
    - `Blocklist.profanity_replacement`: what to replace profanity with.
    """

    def __init__(self, blocklist: "set[str]", mode: str = "normal"):
        perform_mode_check(mode, POSSIBLE_MODES)

        self.mode: str = mode
        self.blocklist: "set[str]" = blocklist
        self.ignore_regex: str = r""";|:|!|\?|\*|\[|\(|\)|\.| |\||"|'|\$|\+"""
        self.profanity_replacement: str = "#@!"

    def check(self, string: str):
        found: "set[str]" = set()
        passed: bool = True

        if self.mode != "strict":
            to_check = set(split(self.ignore_regex, string))

            for word in to_check:
                if word in self.blocklist:
                    found.add(word)
        else:
            for profane_word in self.blocklist:
                if profane_word in string:
                    found.add(profane_word)

        if found:
            passed = False

        if self.mode == "tolerant":
            passed = True
            for word in found:
                string = string.replace(word, self.profanity_replacement)

        return (passed, string)
