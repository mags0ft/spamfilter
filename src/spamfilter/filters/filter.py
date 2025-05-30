"""
Base module for the base filter class.
"""


class Filter:
    """
    The filter base class the other filters inherit from.

    - `Filter.check(string: str)`: check a string against this filter.
    """

    def __init__(self, mode: str = "default") -> None:
        self.mode = mode

    def check(self, string: str) -> "tuple[bool, str]":
        """
        Checks if a given string passes the filter's criteria.

        Returns a tuple containing a boolean (whether it passed) and optionally
        a string (modified version of the input string made by the filter to
        mitigate errors - might not be given, depending on the mode selected).

        The base Filter class does not modify the string, so it always returns
        `True` and the original string. Any other filter that inherits from
        this class should override this method to implement its specific
        filtering logic.
        """

        return (True, string)
