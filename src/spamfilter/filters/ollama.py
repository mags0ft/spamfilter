"""
Module for using the Ollama API as a spam filter by leveraging LLMs to
determine if a string is spam or not.
"""

try:
    import ollama

    ollama_available: bool = True
except ImportError:
    ollama_available: bool = False

import json
from typing import Any, Union
from .check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES: "list[str]" = ["normal", "correcting"]

STD_PROMPT = """You are a spam filter.
Your task is to determine if the given text is spam or not. Give a definite \
answer formatted as JSON."""

JSON_SCHEMA_NORMAL: "dict[str, Any]" = {  # type: ignore
    "type": "object",
    "properties": {
        "is_spam": {
            "type": "boolean",
            "description": "Whether the given text is spam or not.",
        },
    },
    "required": ["is_spam"],
}

JSON_SCHEMA_CORRECTING: "dict[str, Any]" = {
    "type": "object",
    "properties": {
        "is_spam": {
            "type": "boolean",
            "description": "Whether the given text is spam or not.",
        },
        "corrected_text": {
            "type": "string",
            "description": "The corrected text if the input was spam.",
        },
    },
    "required": ["is_spam", "corrected_text"],
}

STD_OPTIONS: "dict[str, Any]" = {
    "temperature": 0.1,
    "num_predict": 1024,
}


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

    - `Ollama.model`: the model to use for checking spam.
    - `Ollama.mode`: how to handle a failing string.
        - `normal`: fail the string.
        - `correcting`: correct the string if it is spam, always allow it
    - `Ollama.host`: the host of the Ollama API endpoint.
    - `Ollama.prompt`: the prompt to use for the LLM.
    - `Ollama.json_schema`: the json schema to use for formatted outputs.
    - `Ollama.options`: the options to use for the Ollama API request.
    - `Ollama.thinking`: whether to enable thinking mode for the LLM.

    It is highly recommended to adjust most of these paramters to your needs,
    especially the `Ollama.model` and `Ollama.prompt` parameters.
    """

    def __init__(
        self,
        model: str,
        mode: str = "normal",
        host: str = "127.0.0.1",
        timeout: float = 3.0,
        prompt: str = STD_PROMPT,
        schema: "Union[dict[str, Any], None]" = None,
        options: "Union[dict[str, Any], None]" = None,
        thinking: bool = False,
    ) -> None:
        perform_mode_check(mode, POSSIBLE_MODES)
        check_ollama_availability()

        self._client = ollama.Client(  # type: ignore
            host=host, timeout=timeout
        )

        self.model = model
        self.mode = mode
        self.prompt = prompt
        self.options = options
        self.thinking = thinking

        self.json_schema: "Union[dict[str, Any], None]" = None

        if schema is None:
            if mode == "normal":
                self.json_schema = JSON_SCHEMA_NORMAL
            elif mode == "correcting":
                self.json_schema = JSON_SCHEMA_CORRECTING
        else:
            self.json_schema = schema

        if options is None:
            self.options = STD_OPTIONS

    def check(self, string: str) -> "tuple[bool, str]":
        """
        Sends the given string to the Ollama API and checks if it is spam or
        not. Returns a tuple of a boolean (whether it is spam) and the
        potentially corrected string.
        """

        # pylint: disable=no-member

        response_raw = self._client.chat(  # type: ignore
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": string},
            ],
            format=self.json_schema,
            stream=False,
            think=self.thinking,
            options=self.options,
        )

        if response_raw.message.content is None:
            raise MalformedResponseException(
                "The response from the Ollama API was malformed."
            )

        response = json.loads(response_raw.message.content)
        passed: bool = not response["is_spam"]

        return (
            passed,
            string if self.mode == "normal" else response["corrected_text"],
        )
