class Result:
    """
    Class to determine a result of a string running through a filtering machine.
    
    `Result.passed`: bool whether the text passed the filters.
    `Result.result`: resulting, sanitized string.
    `Result.original`: the string before getting passed through the filtering machines.
    `Result.changes_made`: how many changes have been commited to the string by the filters.
    `Result.failed_filters`: the filters that made the string fail if it did.
    """
    
    def __init__(self, passed = True, res_string = "", original_string = "", changes = 0, failed_filters = []):
        self.passed : bool = passed
        self.result : str = res_string
        self.original : str = original_string
        self.changes_made : int = changes
        self.failed_filters : list = failed_filters