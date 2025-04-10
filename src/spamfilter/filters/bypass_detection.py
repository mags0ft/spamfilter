"""
Module for the bypass detection filter.

More information about this filter can be found in its Class docstring.
"""

from string import ascii_letters

from .filter import Filter

# For the unprobable case you opened this python file just to understand what
# the BypassDetector filter is for, here is a small exmaple. A string like ...
# "This is a  v e r y   b a d   w o r d !"
# ... couldn't be detected by the Profanity filter due to the spaces in the bad
# word. Therefore, the BypassDetector checks for a bypass try just like this in
# order to prevent bad messages to pass into the filters.


class BypassDetector(Filter):
    """
    Detect if a string is written to bypass filtering.

    This is achieved by checking if characters are commonly adjacent to
    characters that could be used to confuse the filters. The safe characters
    are called "isles" and defined as a list of characters in
    `BypassDetector.isles`.

    - `BypassDetector.percentage`: percentage of suspicious adjacencies needed
    to fail.
    - `BypassDetector.max_findings`: absolute number of suspicious adjacencies
    needed to fail.
    """

    def __init__(self, percentage: float = 0.4, max_findings: int = 5):
        self.isles = list(ascii_letters)
        self.percentage = percentage
        self.max_findings = max_findings

    def check(self, string: str):
        ln = len(string)
        adjacencies = 0
        iterations = 0

        for idx, char in enumerate(string):
            if not char in self.isles:
                continue

            adj_left = idx > 0 and not string[idx - 1] in self.isles
            adj_right = idx < ln - 1 and not string[idx + 1] in self.isles

            if adj_left and adj_right:
                adjacencies += 1
            iterations += 1

        passed = (
            (adjacencies / iterations) if iterations > 0 else 0
        ) <= self.percentage
        if (
            passed
            and self.max_findings > 0
            and adjacencies >= self.max_findings
        ):
            passed = False

        return (passed, string)
