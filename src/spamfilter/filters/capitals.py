"""
Module for the excessive capital letters filter.

More information about this filter can be found in its Class docstring.
"""

from string import ascii_lowercase, ascii_uppercase

from .filter import Filter

POSSIBLE_MODES = ["normal", "crop"]


class Capitals(Filter):
    """
    Check if a string contains too much capitals.
    - `Capitals.percentage`: how many percent of the text need to be in capital
    for it to fail.
    - `Capitals.mode`: how to handle a failing string.
        - `normal`: fail the string
        - `crop`: crop all letters to lowercase if the string is too capital,
        makes it always pass
    """

    def __init__(self, percentage: float = 0.3, mode: str = "normal"):
        if mode not in POSSIBLE_MODES:
            raise ValueError(
                f"Mode not accepted. This filter's mode must be one of those: \
{', '.join(POSSIBLE_MODES)}."
            )

        self.percentage = percentage
        self.mode = mode

    def check(self, string: str):
        def get_capital_percentage(string: str):
            letters = 0
            capitals = 0

            for letter in string:
                if letter in ascii_uppercase:
                    letters += 1
                    capitals += 1
                    continue

                if letter in ascii_lowercase:
                    letters += 1
                    continue

            return (
                (capitals / letters)
                if (len(string) > 0 and letters > 0)
                else 0
            )

        is_too_capital = self.percentage <= get_capital_percentage(string)

        return (
            (True if self.mode == "crop" else (not is_too_capital)),
            (
                string.lower()
                if is_too_capital and self.mode == "crop"
                else string
            ),
        )
