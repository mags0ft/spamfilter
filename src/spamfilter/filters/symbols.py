from .filter import Filter
from string import punctuation, ascii_letters

POSSIBLE_MODES = [
    "normal",
    "crop"
]

class Symbols(Filter):
    """
    Check if a string contains too many symbols.
    `Symbols.percentage`: how many percent of the text need to be symbols for it to fail.
    `Symbols.mode`: how to handle a failing string.
        `normal`: fail the string if it contains too many symbols
        `crop`: remove all symbols from the string if it would fail, but then make the string pass.
    `Symbols.symboldef`: what to identify as a symbol
        `explicit`: everything that matches `Symbols.SYMBOLSET`.
        `implicit`: everything that does not match `Symbols.CHARSET`.
    `Symbols.abs_safe_min`: absolute amount of symbols that are always okay to use.
    """
    def __init__(self, percentage : float = 0.15, mode : str = "normal", symboldef : str = "explicit", abs_safe_min : int = 3):
        if not mode in POSSIBLE_MODES:
            raise ValueError(
                "Mode not accepted. This filter's mode must be one of those: %s." % ", ".join(POSSIBLE_MODES)
            )
        
        self.percentage = percentage
        self.mode = mode
        self.symboldef = symboldef
        self.SYMBOLSET = list(punctuation)
        self.CHARSET = list(ascii_letters)
        self.abs_safe_min = abs_safe_min

    def check(self, string : str):
        def getSymbolPercentage(string : str):
            letters = 0
            symbols = 0

            for letter in string:
                if (self.symboldef == "explicit" and letter in self.SYMBOLSET) or (self.symboldef == "implicit" and (not letter in self.CHARSET)):
                    symbols += 1
                letters += 1
            
            return (symbols / letters if letters > 0 else 0, symbols)
        
        def cleanString(string : str):
            if self.symboldef == "explicit":
                res = string
                for symbol in self.symboldef:
                    res = res.replace(symbol, "")
            else:
                res = ""
                for letter in string:
                    if not letter in self.CHARSET:
                        continue
                    res += letter
            return res
        
        (perc, absl) = getSymbolPercentage(string)
        isSymbolAmountOkay = (self.percentage >= perc) or (absl <= self.abs_safe_min)

        return (
            (True if self.mode == "crop" else isSymbolAmountOkay),
            (cleanString(string) if (not isSymbolAmountOkay) and self.mode == "crop" else string)
        )