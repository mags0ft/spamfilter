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
    - `Capitals.abs_safe_min`: the absolute amound of capital characters that
    are always okay. Set to -1 to deactivate.
    - `Capitals.mode`: how to handle a failing string.
        - `normal`: fail the string
        - `crop`: crop all letters to lowercase if the string is too capital,
        makes it always pass
    """

    def __init__(
        self,
        percentage: float = 0.3,
        mode: str = "normal",
        abs_safe_min: int = 3,
    ):
        if mode not in POSSIBLE_MODES:
            raise ValueError(
                f"Mode not accepted. This filter's mode must be one of those: \
{', '.join(POSSIBLE_MODES)}."
            )

        self.percentage = percentage
        self.mode = mode
        self.abs_safe_min = abs_safe_min

    def check(self, string: str):
        def analyse_capitals(string: str):
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
            ), capitals

        capital_percentage, total_capitals = analyse_capitals(string)
        is_too_capital = (
            self.percentage <= capital_percentage
            and total_capitals > self.abs_safe_min
        )

        return (
            (True if self.mode == "crop" else (not is_too_capital)),
            (
                string.lower()
                if is_too_capital and self.mode == "crop"
                else string
            ),
        )
