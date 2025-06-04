"""
Module for using the Ollama API as a spam filter by leveraging LLMs to
determine if a string is spam or not.
"""

try:
    import ollama

    ollama_available: bool = True
except ImportError:
    ollama_available: bool = False

from .check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES: "list[str]" = ["normal"]


class MalformedResponseException(Exception):
    """
    Exception thrown when the LLM response is malformed.
    """


def check_ollama_availability():
    """
    Checks if the `ollama_available` global has been set to `True`, otherwise
    raises an exception.
    """

    if not ollama_available:
        raise ImportError(
            "Please install the Ollama dependencies for spamfilter using \
`pip install spamfilter[ollama]`."
        )


class Ollama(Filter):
    """
    A filter that connects to an Ollama API endpoint to check if a given string
    is spam or not. This might introduce **significant latency** in your
    pipeline, so use this with caution and only if necessary.

    This filter requires the `ollama` Python package to be installed, which can
    be done with `pip install spamfilter[ollama]`.

    It is **NOT YET** implemented, so it will always return `True` and the
    original string. The implementation will be added in a future version of
    spamfilter.
    """

    def __init__(
        self,
        mode: str = "normal",
        host: str = "127.0.0.1",
        timeout: float = 3.0,
    ) -> None:
        perform_mode_check(mode, POSSIBLE_MODES)
        check_ollama_availability()

        self._client = ollama.Client(  # type: ignore
            host=host, timeout=timeout
        )
        self.mode = mode

    def check(self, string: str) -> "tuple[bool, str]":
        """
        Sends the given string to the Ollama API and checks if it is spam or
        not. Returns a tuple of a boolean (whether it is spam) and the
        potentially corrected string.
        """

        # TODO: Implement the actual API call to Ollama.

        return (True, string)
