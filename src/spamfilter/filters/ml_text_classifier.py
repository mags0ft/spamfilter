"""
Uses text classification models from platforms like Hugging Face to detect spam
and harmful content.
"""

try:
    import transformers

    transformers_available: bool = True
except ImportError:
    transformers_available: bool = False

from ._check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES: "list[str]" = ["normal"]


def check_transformers_availability():
    """
    Checks if the `transformers_available` global has been set to `True`,
    otherwise raises an exception.
    """

    if not transformers_available:
        raise ImportError(
            "Please install the 🤗 Transformers dependencies for spamfilter" \
"using `pip install spamfilter[transformers]`."
        )


class MLTextClassifier(Filter):
    """
    A filter that instantiates a 🤗 Transformers text classification pipeline
    and uses it to classify text as spam or not. Note that machine learning is
    never 100% accurate, so this filter may not always return the correct
    result and let harmful content through.

    This filter requires the `transformers` Python package to be installed,
    which can be done with `pip install spamfilter[transformers]`.

    - `MLTextClassifier.model`: the model to use for checking spam.
    - `MLTextClassifier.mode`: how to handle a failing string.
        - `normal`: fail the string.
    - `MLTextClassifier.response_parsing_function`: a function that
      parses the response from the model and returns a boolean indicating
      whether the string is spam or not.
    """

    def __init__(
        self,
        model: str = "facebook/roberta-hate-speech-dynabench-r4-target",
        mode: str = "normal",
    ) -> None:
        perform_mode_check(mode, POSSIBLE_MODES)
        check_transformers_availability()

        self._pipeline = None

        self.model = model
        self.mode = mode

    def check(self, string: str) -> "tuple[bool, str]":
        """
        Checks if the given string is spam or not using the text classification
        model specified in `self.model`.
        """

        raise NotImplementedError(
            "The machine learning text classification filter is not "
            "implemented yet. Please use a different filter."
        )
