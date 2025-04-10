"""
Small utility module that checks if a mode for a given filter is applicable.
"""


def perform_mode_check(mode: str, possible_modes: "list[str]"):
    """
    Performs a check of the given `mode` string against the list of all
    possible modes. Raises a `ValueError` if the mode is not found.
    """

    if not mode in possible_modes:
        raise ValueError(
            f"Mode not accepted. This filter's mode must be one of those: \
{', '.join(possible_modes)}."
        )
