from .filter import Filter
from re import split

POSSIBLE_MODES = [
    "normal",
    "strict",
    "tolerant"
]

class Blocklist(Filter):
    """
    Filter text for blocked words. Works better in combination with `BypassDetector`.
    `Blocklist.mode`: How to handle incoming text.
        `normal`: search for profane words adjacent to punctuation or spaces.
        `strict`: search for any occurence of a profane word. WARNING: this might detect words like "classic" as they contain parts of a profane words.
        `tolerant`: simply replace the problematic words.
    `Blocklist.blocklist`: a set with words that shall be blocked.
    `Blocklist.ignore_regex`: a regular expression that matches punctuation characters for splitting the string in non-strict mode.
    `Blocklist.profanity_replacement`: what to replace profanity with.
    """

    def __init__(self, blocklist : set, mode : str = "normal"):
        if not mode in POSSIBLE_MODES:
            raise ValueError(
                "Mode not accepted. This filter's mode must be one of those: %s." % ", ".join(POSSIBLE_MODES)
            )
        
        self.mode = mode
        self.blocklist : set = blocklist
        self.ignore_regex : str = r''';|:|!|\?|\*|\[|\(|\)|\.| |\||"|'|\$|\+'''
        self.profanity_replacement : str = "#@!"

    def check(self, string : str):
        found = set()
        passed : bool = True

        if self.mode != "strict":
            to_check = set(
                split(self.ignore_regex, string)
            )

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