"""
The module containing a pre-made Pipeline class for spam filtering article-like
texts.
"""

from .construct_pipeline import construct_filter_list

from ..pipelines import Pipeline


def create_pipeline(
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
    specialchars_filter: bool = True,
    profanity_filter: bool = False,
    profanity_blocklist_filepath: str = "",
):
    """
    Create a Pipeline that is pre-made to be used in high-quality, demanding
    writing platforms.
    """

    # pylint: disable=unused-argument

    return Pipeline(
        construct_filter_list(**locals()),
        mode="zero-tolerance",
    )


articlePipeline = create_pipeline()
