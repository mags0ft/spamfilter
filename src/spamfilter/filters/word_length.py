"""
Module for the word length filter.

More information about this filter can be found in its Class docstring.
"""

import re

from .check_modes import perform_mode_check
from .filter import Filter

POSSIBLE_MODES = ["absolute", "percentage", "hybrid"]


class WorldLength(Filter):
    """
    Checks if the words in a string match given length requirements.

    - `WordLength.max`: The inclusive maximum length of a single word.
    - `WordLength.max_abs_population`: The maximum amount of too long words to
    make the string fail.
    - `WordLength.max_perc_population`: The maximum percentage of too long
    words to make the string fail.
    - `WordLength.mode`: How to detect failing strings.
        - `absolute`: Fail the string if there are too many words that are too
        long, specified in `max_abs_population` as a max int.
        - `percentage`: Fail the string if there more too long words than the
        specified percentage in `max_perc_population` as a percentage float.
        - `hybrid`: Fail the string if not both of the above conditions are
        met.
    - `WordLength.split_regex`: The regex used to split into standalone words.
    """

    def __init__(
        self,
        max_length: int = 20,
        mode: str = "absolute",
        max_abs_population: int = 1,
        max_perc_population: float = 0.1,
    ):
        perform_mode_check(mode, POSSIBLE_MODES)

        self.max_length = max_length
        self.mode = mode
        self.split_regex = r",|;|\.| |:|-|_|\!|\?|\(|\)"
        self.max_abs_population = max_abs_population
        self.max_perc_population = max_perc_population

    def check(self, string: str):
        split_string = re.split(self.split_regex, string)

        fails = 0
        for word in split_string:
            if len(word) > self.max_length:
                fails += 1

        passes_abs = fails < self.max_abs_population
        passes_rel = (
            (fails / len(split_string)) > self.max_perc_population
            if len(split_string) > 0
            else True
        )

        if self.mode == "absolute":
            passes = passes_abs
        elif self.mode == "hybrid":
            passes = passes_abs and passes_rel
        else:
            passes = passes_rel

        return (passes, string)
