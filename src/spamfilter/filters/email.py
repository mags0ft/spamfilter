"""
Module for the email information filter.

More information about this filter can be found in its Class docstring.
"""

from .personal_information import PersonalInformation

POSSIBLE_MODES = ["normal", "censor"]


class Email(PersonalInformation):
    """
    Check if a string contains an email address.
    - `Email.mode`: how to handle a failing string.
        - `normal`: fail the string.
        - `censor`: censor the information.
    - `Email.regex`: the regex used to check for email addresses.
    - `Email.replacement`: what regex to replace email addresses with.
    """

    def __init__(
        self,
        regex: str = r"([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",
        mode: str = "normal",
        replacement: str = r"***",
    ):
        super().__init__(regex, mode, replacement)
