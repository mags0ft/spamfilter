"""
Module for the symbols filter.

More information about this filter can be found in its Class docstring.
"""

from string import punctuation, ascii_letters

from .check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES = ["normal", "crop"]


class Symbols(Filter):
    """
    Check if a string contains too many symbols.

    - `Symbols.percentage`: how many percent of the text need to be symbols for
    it to fail.
    - `Symbols.mode`: how to handle a failing string.
        - `normal`: fail the string if it contains too many symbols
        - `crop`: remove all symbols from the string if it would fail, but then
        make the string pass.
    - `Symbols.symboldef`: what to identify as a symbol
        - `explicit`: everything that matches `Symbols.symbolset`.
        - `implicit`: everything that does not match `Symbols.charset`.
    - `Symbols.abs_safe_min`: absolute amount of symbols that are always okay
    to use.
    """

    def __init__(
        self,
        percentage: float = 0.15,
        mode: str = "normal",
        symboldef: str = "explicit",
        abs_safe_min: int = 3,
    ):
        perform_mode_check(mode, POSSIBLE_MODES)

        self.percentage = percentage
        self.mode = mode
        self.symboldef = symboldef
        self.symbolset = list(punctuation + "§")
        self.charset = list(ascii_letters)
        self.abs_safe_min = abs_safe_min

    def check(self, string: str):
        def get_symbol_percentage(string: str):
            letters = 0
            symbols = 0

            for letter in string:
                if (
                    self.symboldef == "explicit" and letter in self.symbolset
                ) or (
                    self.symboldef == "implicit"
                    and (not letter in self.charset)
                ):
                    symbols += 1
                letters += 1

            return (symbols / letters if letters > 0 else 0, symbols)

        def clean_string(string: str):
            if self.symboldef == "explicit":
                res = string
                for symbol in self.symbolset:
                    res = res.replace(symbol, "")
            else:
                res = ""
                for letter in string:
                    if not letter in self.charset:
                        continue
                    res += letter
            return res

        (perc, absl) = get_symbol_percentage(string)
        is_symbol_amount_okay = (self.percentage >= perc) or (
            absl <= self.abs_safe_min
        )

        return (
            (True if self.mode == "crop" else is_symbol_amount_okay),
            (
                clean_string(string)
                if (not is_symbol_amount_okay) and self.mode == "crop"
                else string
            ),
        )
