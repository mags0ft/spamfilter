"""
Base module for the Regex base filter class.
"""

import re

from .check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES = ["normal", "censor"]


class Regex(Filter):
    """
    Check if a string matches a given regular expression.

    - `Regex.mode`: how to handle a failing string.
        - `normal`: fail the string.
        - `censor`: censor the match.
    - `Regex.regex`: the regex used to check for matches.
    - `Regex.replacement`: what regex to replace matches with.

    _Was called "PersonalInformation" prior to v2.0.0, which was a breaking
    change._
    """

    def __init__(
        self, regex: str, mode: str = "normal", replacement: str = r"***"
    ):
        perform_mode_check(mode, POSSIBLE_MODES)

        self.regex = regex
        self.mode = mode
        self.replacement = replacement

        self._regex_compiled = re.compile(self.regex)

    def check(self, string: str):
        passed = not self._regex_compiled.search(string)

        return (
            (True if self.mode == "censor" else passed),
            (
                re.sub(self.regex, self.replacement, string)
                if self.mode == "censor"
                else string
            ),
        )
