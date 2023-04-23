from .filter import Filter
from string import ascii_lowercase, ascii_uppercase

POSSIBLE_MODES = [
    "normal",
    "crop"
]

class Capitals(Filter):
    """
    Check if a string contains too much capitals.
    `Capitals.percentage`: how many percent of the text need to be in capital for it to fail.
    `Capitals.mode`: how to handle a failing string.
        `normal`: fail the string 
        `crop`: crop all letters to lowercase if the string is too capital, makes it always pass
    """
    def __init__(self, percentage : float = 0.3, mode : str = "normal"):
        if not mode in POSSIBLE_MODES:
            raise ValueError(
                "Mode not accepted. This filter's mode must be one of those: %s." % ", ".join(POSSIBLE_MODES)
            )
        
        self.percentage = percentage
        self.mode = mode

    def check(self, string : str):
        def getCapitalPercentage(string: str):
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
            
            return (capitals / letters) if (len(string) > 0 and letters > 0) else 0
        
        isTooCapital = self.percentage <= getCapitalPercentage(string)

        return (
            (True if self.mode == "crop" else (not isTooCapital)),
            (string.lower() if isTooCapital and self.mode == "crop" else string)
        )