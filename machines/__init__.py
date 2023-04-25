from result import Result

POSSIBLE_MODES = [
    "normal",
    "tolerant",
    "zero-tolerance",
    "normal-quick"
]

class Machine:
    """
    A machine is an object that accepts several filters and passes strings through these.
    It's the core mechanism to filter potential spam strings.

    `Machine.filters`: this property is a list of all filters in a machine. The order is kept.
    `Machine.mode`: can either be `"normal"`, `"tolerant`" or `"zero-tolerance"`.
        - `"normal"` lets filters change the string itself and will make strings fail if a filter says so.
        - `"normal-quick"` is like normal, but stops execution as soon as a fail happens.
        - `"tolerant`" passes strings, no matter what filters say, and does not stop execution of them on fail.
        - `"zero-tolerance"` does not accept any changes to a string and fails it as soon as a filter registers something.
    """

    def __init__(self, filters : list = [], mode : str = "normal"):
        if not mode in POSSIBLE_MODES:
            raise ValueError(
                "Mode not accepted. A machine mode must be one of those: %s." % ", ".join(POSSIBLE_MODES)
            )
        
        self.filters : list = filters
        self.mode : str = mode

    def check(self, string : str):
        changed_string = string
        passed = True
        changes = 0
        failed = []

        for filter in self.filters:
            (temp_passed, temp_changed_string) = filter.check(changed_string)
            
            if not temp_passed:
                failed.append(filter)

            if temp_changed_string != changed_string:
                if self.mode == "zero-tolerance":
                    passed = False
                    break

                changes += 1
                changed_string = temp_changed_string
                
            if passed and not temp_passed:
                passed = False
                if self.mode in ["normal-quick", "zero-tolerance"]:
                    break


        if self.mode == "tolerant":
            passed = True

        return Result(
            passed = passed,
            res_string = changed_string,
            original_string = string,
            changes = changes,
            failed_filters = failed
        )