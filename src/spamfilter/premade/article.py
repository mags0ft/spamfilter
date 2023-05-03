from ..machines import Machine
from ..filters import (
    Length,
    WorldLength,
    Symbols,
    Capitals,
    BypassDetector,
    BlocklistFromJSON
)

def create_machine(
    bypass_protection : bool = True,
    length_filter : bool = True,
    min_length : int = 400,
    max_length : int = 300_000,
    wordlength_filter : bool = True,
    max_word_length: int = 50,
    max_num_too_long_words: int = 3,
    capitals_filter : bool = True,
    capitals_percentage : float = 0.4,
    capitals_mode : str = "normal",
    symbols_filter : bool = True,
    profanity_filter : bool = False,
    profanity_blocklist_filepath : str = ""
):
    """
    Create a Machine that is pre-made to be used in high-quality, demanding writing platforms.
    """
    f = []
    p = [
        (bypass_protection, BypassDetector, ()),
        (length_filter, Length, (min_length, max_length)),
        (wordlength_filter, WorldLength, (max_word_length, "absolute", max_num_too_long_words)),
        (capitals_filter, Capitals, (capitals_percentage, capitals_mode)),
        (symbols_filter, Symbols, ()),
        (profanity_filter, BlocklistFromJSON, (profanity_blocklist_filepath))
    ]

    for val, obj, args in p:
        if val:
            f.append(
                obj(*args)
            )

    return Machine(f, mode = "zero-tolerance")

ArticleMachine = create_machine()