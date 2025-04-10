"""
The machines module handles the core mechanism of spamfilter's spam detection
pipeline: Machine objects. For info on how to use them, consult the docstring
of the `machines.Machine` class.
"""

from typing import Type, Union

from ..result import Result
from ..filters import Filter
from ..filters.check_modes import perform_mode_check


POSSIBLE_MODES = ["normal", "tolerant", "zero-tolerance", "normal-quick"]


class Machine:
    """
    A machine is an object that accepts several filters and passes strings
    through these. It's the core mechanism to filter potential spam strings.

    - `Machine.filters`: this property is a list of all filters in a machine.
    The order is kept.
    - `Machine.mode`: can either be `"normal"`, `"tolerant`" or
    `"zero-tolerance"`.
        - `"normal"` lets filters change the string itself and will make
        strings fail if a filter says so.
        - `"normal-quick"` is like normal, but stops execution as soon as a
        fail happens.
        - `"tolerant`" passes strings, no matter what filters say, and does not
        stop execution of them on fail.
        - `"zero-tolerance"` does not accept any changes to a string and fails
        it as soon as a filter registers something.
    """

    def __init__(
        self,
        filters: "Union[None, list[Type[Filter]]]" = None,
        mode: str = "normal",
    ):
        """
        Initializes the Machine object for later use. Filters do not need to be
        passed at this stage, they can be added later on.

        Modes `normal`, `normal-quick`, `tolerant` and `zero-tolerance` are
        supported.
        """

        if filters is None:
            filters = []

        perform_mode_check(mode, POSSIBLE_MODES)

        self.filters: "list[Type[Filter]]" = filters
        self.mode: str = mode

    def check(self, string: str) -> Result:
        """
        Checks a given string against the filters inside the Machine. Returns a
        `Result` object.
        """

        changed_string: str = string
        passed: bool = True
        changes: int = 0
        failed: "list[Type[Filter]]" = []

        for filter_ in self.filters:
            temp_changed_string: str = ""
            temp_passed: bool = False
            (temp_passed, temp_changed_string) = filter_.check(  # type: ignore
                changed_string
            )

            if not temp_passed:
                failed.append(filter_)

            if temp_changed_string != changed_string:
                if self.mode == "zero-tolerance":
                    passed = False
                    break

                changes += 1
                changed_string = temp_changed_string  # type: ignore

            if passed and not temp_passed:
                passed = False
                if self.mode in ["normal-quick", "zero-tolerance"]:
                    break

        if self.mode == "tolerant":
            passed = True

        return Result(
            passed=passed,
            res_string=changed_string,  # type: ignore
            original_string=string,
            changes=changes,
            failed_filters=failed,
        )
