"""
The pipelines module handles the core mechanism of spamfilter's spam detection
pipeline: Pipeline objects. For info on how to use them, consult the docstring
of the `pipelines.Pipeline` class.

Prior to `spamfilter` v2.0.0, the pipelines were called "machines". This is no
longer the case, as we figured the term "machine" is not fully accurate for the
way they work. The term "pipeline" is the new standard, as it describes the
process of passing data through a series of filters. Thus, `spamfilter` v2.0.0
is a breaking change and you will need to update your code if you used machines
before.
"""

from typing import Type, Union

from ..result import Result
from ..filters import Filter
from ..filters.check_modes import perform_mode_check


POSSIBLE_MODES = ["normal", "tolerant", "zero-tolerance", "normal-quick"]


class Pipeline:
    """
    A pipeline is an object that accepts several filters and passes strings
    through these. It's the core mechanism to filter potential spam strings.

    - `Pipeline.filters`: this property is a list of all filters in a pipeline.
    The order is kept.
    - `Pipeline.mode`: can either be `"normal"`, `"tolerant`" or
    `"zero-tolerance"`.
        - `"normal"` lets filters change the string itself and will make
        strings fail if a filter says so.
        - `"normal-quick"` is like normal, but stops execution as soon as a
        fail happens.
        - `"tolerant`" passes strings, no matter what filters say, and does not
        stop execution of them on fail.
        - `"zero-tolerance"` does not accept any changes to a string and fails
        it as soon as a filter registers something.

    _Was called "Machine" prior to v2.0.0, which was a breaking change._
    """

    def __init__(
        self,
        filters: "Union[None, list[Type[Filter]]]" = None,
        mode: str = "normal",
    ):
        """
        Initializes the Pipeline object for later use. Filters do not need to
        be passed at this stage, they can be added later on.

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
        Checks a given string against the filters inside the Pipeline. Returns
        a `Result` object.
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
            result=changed_string,  # type: ignore
            original=string,
            changes_made=changes,
            failed_filters=failed,
        )
