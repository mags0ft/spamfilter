"""
The module containing a pre-made Machine class for spam filtering article-like
texts.
"""

from .construct_machine import construct_filter_list

from ..machines import Machine


def create_machine(
    bypass_protection: bool = True,
    length_filter: bool = True,
    min_length: int = 400,
    max_length: int = 300_000,
    wordlength_filter: bool = True,
    max_word_length: int = 50,
    max_num_too_long_words: int = 3,
    capitals_filter: bool = True,
    capitals_percentage: float = 0.4,
    capitals_mode: str = "normal",
    symbols_filter: bool = True,
    profanity_filter: bool = False,
    profanity_blocklist_filepath: str = "",
):
    """
    Create a Machine that is pre-made to be used in high-quality, demanding
    writing platforms.
    """

    # pylint: disable=unused-argument

    return Machine(
        construct_filter_list(**locals()),
        mode="zero-tolerance",
    )


articleMachine = create_machine()
