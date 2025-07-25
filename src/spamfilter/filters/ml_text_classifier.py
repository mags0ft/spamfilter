"""
Uses text classification models from platforms like Hugging Face to detect spam
and harmful content.
"""

try:
    import transformers

    transformers_available: bool = True
except ImportError:
    transformers_available: bool = False


from typing import Callable, Union
from ._check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES: "list[str]" = ["normal"]
DEFAULT_MODEL = "facebook/roberta-hate-speech-dynabench-r4-target"


def check_transformers_availability():
    """
    Checks if the `transformers_available` global has been set to `True`,
    otherwise raises an exception.
    """

    if not transformers_available:
        raise ImportError(
            "Please install the 🤗 Transformers dependencies for spamfilter"
            "using `pip install spamfilter[transformers]`."
        )


def _default_response_parsing_function(
    result: list[dict[str, Union[str, float]]],
) -> bool:
    """
    Default response parsing function that checks if the label
    is 'spam' or 'toxic'.
    """

    sorted_result = sorted(result, key=lambda x: x["score"], reverse=True)
    top_label: str = str(sorted_result[0]["label"]).lower()

    return top_label not in ["spam", "toxic", "hate", "abusive"]


class MLTextClassifier(Filter):
    """
    A filter that instantiates a 🤗 Transformers text classification pipeline
    and uses it to classify text as spam or not. Note that machine learning is
    never 100% accurate, so this filter may not always return the correct
    result and let harmful content through.
    
    Please make sure to have read the warnings in the
    [documentation](https://mags0ft.github.io/spamfilter/ai_and_ml/).

    This filter requires the `transformers` Python package to be installed,
    which can be done with `pip install spamfilter[transformers]`.

    - `MLTextClassifier.__init__.model`: the model to use for checking spam.
    - `MLTextClassifier.mode`: how to handle a failing string.
        - `normal`: fail the string.
    - `MLTextClassifier.response_parsing_function`: a function that
      parses the response from the model and returns a boolean indicating
      whether the string is spam or not.
    
    **WARNING**: The standard model is a hate detection model which will be
    automatically pulled from Hugging Face (~ 500 MB). You may want to use a
    more suitable model for your use case, such as a custom spam detection
    model for email spam detection.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        response_parsing_function: "Union[Callable[[str], bool], None]" = None,
        mode: str = "normal",
    ) -> None:
        perform_mode_check(mode, POSSIBLE_MODES)
        check_transformers_availability()

        self._pipeline = transformers.pipeline(  # type: ignore
            "text-classification", model=model
        )

        self.mode = mode

        if response_parsing_function is None:
            self.response_parsing_function = _default_response_parsing_function

    def check(self, string: str) -> "tuple[bool, str]":
        """
        Checks if the given string is spam or not using the text classification
        model specified in `self.model`.
        """

        return (self.response_parsing_function(self._pipeline(string)), string)
