"""
Base module for the Regex base filter class.
"""

import re

from ._check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES = ["normal", "censor"]


class Regex(Filter):
    """
    Check if a string matches a given regular expression.

    - `Regex.expression`: the regular expression used to check for matches.
    - `Regex.mode`: how to handle a failing string.
        - `normal`: fail the string.
        - `censor`: censor the match.
    - `Regex.replacement`: what regex to replace matches with.
    - `Regex.flags`: any optional regex flags to use when compiling the
      expression.

    **Warning**: Changing flags after initialization will not automatically
    recompile the regex. Call `Regex.compile_regex()` to do so.

    _Was called "PersonalInformation" prior to v2.0.0, which was a breaking
    change._
    """

    def __init__(
        self,
        expression: str,
        mode: str = "normal",
        replacement: str = r"***",
        flags: int = 0,
    ):
        perform_mode_check(mode, POSSIBLE_MODES)

        self.expression = expression
        self.mode = mode
        self.replacement = replacement
        self.flags = flags

        self.compile_regex()

    def compile_regex(self):
        """
        Recompiles the internal regex. Useful if the expression or flags have
        been modified.
        """

        self._regex_compiled = re.compile(self.expression, self.flags)

    def check(self, string: str):
        passed = not self._regex_compiled.search(string)

        return (
            (True if self.mode == "censor" else passed),
            (
                re.sub(self.expression, self.replacement, string)
                if self.mode == "censor"
                else string
            ),
        )
