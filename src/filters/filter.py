class Filter:
    """
    The filter base class the other filters inherit from.
    
    `Filter.check(string: str)`: check a string against this filter.
    """
    def __init__(self, mode : str = "default"):
        self.mode = mode

    def check(self, string : str):
        return (True, string)