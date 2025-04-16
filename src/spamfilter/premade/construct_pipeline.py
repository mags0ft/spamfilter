"""
Small helper module that constructs a list of filters from arguments.
"""

from typing import Type, Union

from ..filters.filter import Filter
from ..filters import (
    Length,
    WorldLength,
    Symbols,
    Capitals,
    BypassDetector,
    BlocklistFromJSON,
)


def construct_filter_list(
    bypass_protection: bool,
    length_filter: bool,
    min_length: int,
    max_length: int,
    wordlength_filter: bool,
    max_word_length: int,
    max_num_too_long_words: int,
    capitals_filter: bool,
    capitals_percentage: float,
    capitals_mode: str,
    symbols_filter: bool,
    profanity_filter: bool,
    profanity_blocklist_filepath: str,
) -> "list[Type[Filter]]":
    """
    Constructs a list of filters out of the arguments.
    """

    f: "list[Type[Filter]]" = []
    p: (
        "list[tuple[bool, Type[Filter], tuple[Union[int, str, float], ...]]]"
    ) = [
        (bypass_protection, BypassDetector, ()),
        (length_filter, Length, (min_length, max_length)),
        (
            wordlength_filter,
            WorldLength,
            (max_word_length, "absolute", max_num_too_long_words),
        ),
        (capitals_filter, Capitals, (capitals_percentage, capitals_mode)),
        (symbols_filter, Symbols, ()),
        (profanity_filter, BlocklistFromJSON, (profanity_blocklist_filepath,)),
    ]

    for val, obj, args in p:
        if val:
            f.append(obj(*args))  # type: ignore

    return f
