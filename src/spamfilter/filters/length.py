"""
Module for the message length filter.

More information about this filter can be found in its Class docstring.
"""

from .check_modes import perform_mode_check
from .filter import Filter

POSSIBLE_MODES = ["normal", "crop"]


class Length(Filter):
    """
    Checks if a string matches given length requirements.
    - `Length.min`: The inclusive minimum length.
    - `Length.max`: The inclusive maximum length.
    - `Length.padding`: A character used to fill up strings that are too short
    in the `crop` mode.
    - `Length.mode`: How to handle failing strings.
        - `normal`: Fail too short or too long strings.
        - `crop`: Shorten too long strings and fill too short strings up using
        `Length.padding`.
    """

    def __init__(
        self,
        min_length: int = 10,
        max_length: int = 200,
        padding: str = " ",
        mode: str = "normal",
    ):
        perform_mode_check(mode, POSSIBLE_MODES)

        if len(padding) != 1:
            raise ValueError(
                "Invalid padding. The filter padding must be exactly one \
character long."
            )

        self.min = min_length
        self.max = max_length
        self.mode = mode
        self.padding = padding

    def check(self, string: str):
        ln = len(string)
        passes = (self.min <= ln <= self.max) or (self.mode == "crop")
        res = string

        if self.mode == "crop":
            if ln < self.min:
                res = string + self.padding * (self.min - ln)
            elif ln > self.max:
                res = string[: self.max]

        return (passes, res)
