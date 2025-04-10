"""
Small utility module that checks if a mode for a given filter is applicable.
"""


def perform_mode_check(mode: str, possible_modes: "list[str]"):
    if not mode in possible_modes:
        raise ValueError(
            "Mode not accepted. This filter's mode must be one of those: %s."
            % ", ".join(possible_modes)
        )
