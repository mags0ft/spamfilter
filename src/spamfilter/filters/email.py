"""
Module for the email information filter.

More information about this filter can be found in its class docstring.
"""

from .regex import Regex

POSSIBLE_MODES = ["normal", "censor"]
STD_EMAIL_REGEX = r"([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"


class Email(Regex):
    """
    Check if a string contains an email address.

    - `Email.regex`: the regex used to check for email addresses.
    - `Email.mode`: how to handle a failing string.
        - `normal`: fail the string.
        - `censor`: censor the information.
    - `Email.replacement`: what regex to replace email addresses with.
    """

    def __init__(
        self,
        regex: str = STD_EMAIL_REGEX,
        mode: str = "normal",
        replacement: str = r"***",
    ):
        super().__init__(regex, mode, replacement)
