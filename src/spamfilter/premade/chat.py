"""
The module containing a pre-made Pipeline class for chat message filtering.
"""

from .construct_pipeline import construct_filter_list
from ..pipelines import Pipeline


def create_pipeline(
    bypass_protection: bool = True,
    length_filter: bool = True,
    min_length: int = 1,
    max_length: int = 200,
    wordlength_filter: bool = True,
    max_word_length: int = 20,
    max_num_too_long_words: int = 1,
    capitals_filter: bool = True,
    capitals_percentage: float = 0.3,
    capitals_mode: str = "crop",
    specialchars_filter: bool = True,
    profanity_filter: bool = False,
    profanity_blocklist_filepath: str = "",
):
    """
    Create a Pipeline that is pre-made to be used in fast-paced, internet
    chatting environments.
    """

    # pylint: disable=unused-argument

    return Pipeline(
        construct_filter_list(**locals()),
        mode="normal-quick",
    )


chatPipeline = create_pipeline()
