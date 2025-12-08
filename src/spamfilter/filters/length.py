"""
Module for the message length filter.

More information about this filter can be found in its class docstring.
"""

from ._check_modes import perform_mode_check
from .filter import Filter

POSSIBLE_MODES = ["normal", "crop", "shorten-only", "fill-only"]


class Length(Filter):
    """
    Checks if a string matches given length requirements.

    - `Length.min_`: The inclusive minimum length.
    - `Length.max_`: The inclusive maximum length.
    - `Length.padding`: A character used to fill up strings that are too short
    in the `crop` and `fill-only` modes.
    - `Length.mode`: How to handle failing strings.
        - `normal`: Fail too short or too long strings.
        - `crop`: Shorten too long strings and fill too short strings up using
        `Length.padding`.
        - `shorten-only`: Only shorten too long strings, do not fill up too
        short strings.
        - `fill-only`: Only fill up too short strings, do not shorten too long
        strings.
    """

    def __init__(
        self,
        min_: int = 10,
        max_: int = 200,
        padding: str = " ",
        mode: str = "normal",
    ):
        perform_mode_check(mode, POSSIBLE_MODES)

        if len(padding) != 1:
            raise ValueError(
                "Invalid padding. The filter padding must be exactly one \
character long."
            )

        self.min_ = min_
        self.max_ = max_
        self.mode = mode
        self.padding = padding

    def check(self, string: str):
        ln = len(string)
        passes = (self.min_ <= ln <= self.max_) or (
            self.mode in ["crop", "fill-only", "crop-only"]
        )

        if self.mode in ["crop", "fill-only"] and ln < self.min_:
            return (passes, string + self.padding * (self.min_ - ln))

        if self.mode in ["crop", "shorten-only"] and ln > self.max_:
            return (passes, string[: self.max_])

        return (passes, string)
