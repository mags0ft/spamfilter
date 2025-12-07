"""
Module for using the OpenAI API as a spam filter by leveraging LLMs to
determine if a string is spam or not.
"""

openai_available: bool = False

try:
    import openai

    openai_available: bool = True
except ImportError:
    pass

import json
from typing import Any, Callable, Union, Tuple
from ._check_modes import perform_mode_check
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
            "description": "The cleaned version of the text - in case the \
input contained spam.",
        },
    },
    "required": ["is_spam", "corrected_text"],
}

STD_OPTIONS: "dict[str, Any]" = {
    "temperature": 0.1,
    "max_tokens": 1024,
}

RespFuncType = Callable[[dict[str, Union[bool, str]]], Tuple[bool, str]]
JSONParameterType = Union[dict[str, Any], None]

std_resp_func: RespFuncType = lambda resp: (  # type: ignore
    not resp["is_spam"],
    (resp["corrected_text"] if "corrected_text" in resp else ""),
)


class MalformedResponseException(Exception):
    """
    Exception thrown when the LLM response is malformed.
    """


def check_openai_availability():
    """
    Checks if the `openai_available` global has been set to `True`, otherwise
    raises an exception.
    """

    if not openai_available:
        raise ImportError(
            "Please install the OpenAI dependencies for spamfilter using \
`pip install spamfilter[openai]`."
        )


class OpenAI(Filter):
    """
    A filter that connects to an OpenAI API endpoint to check if a given string
    is spam or not. This might introduce **significant latency** in your
    pipeline, so use this with caution and only if necessary.

    The endpoint is not required to literally be by OpenAI; it should merely be
    an OpenAI API-compatible one (one that meets the specification of the API).

    For connecting to remote instances, this may require an API key.

    Please make sure to have read the warnings in the
    [documentation](https://mags0ft.github.io/spamfilter/ai_and_ml/).

    This filter requires the `openai` Python package to be installed, which can
    be done with `pip install spamfilter[openai]`.

    - `OpenAI.model`: the model to use for checking spam.
    - `OpenAI.mode`: how to handle a failing string.
        - `normal`: fail the string.
        - `correcting`: correct the string if it is spam, always allow it
    - `OpenAI.base_url`: the base URL of the OpenAI API endpoint.
    - `OpenAI.api_key`: API key to use for authentication.
    - `OpenAI.prompt`: the prompt to use for the LLM.
    - `OpenAI.json_schema`: the json schema to use for formatted outputs.
    - `OpenAI.options`: the options to use for the OpenAI API request.
    - `OpenAI.response_parsing_function`: a function that takes the response
      from the OpenAI API and returns a tuple of a boolean (whether it is spam)
      and the potentially corrected string.

    It is highly recommended to adjust most of these paramters to your needs,
    especially the `OpenAI.model` and `OpenAI.prompt` parameters. Please also
    be aware that the maximum amount of tokens is 1024 by default, which may
    need to be adjusted based on your use case (like correcting long texts).
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        model: str,
        mode: str = "normal",
        base_url: str = "https://api.openai.com/v1",
        api_key: "Union[str, None]" = None,
        timeout: float = 3.0,
        prompt: str = STD_PROMPT,
        json_schema: JSONParameterType = None,
        options: JSONParameterType = None,
        response_parsing_function: RespFuncType = std_resp_func,
    ) -> None:
        perform_mode_check(mode, POSSIBLE_MODES)
        check_openai_availability()

        self._client = openai.OpenAI(  # type: ignore
            base_url=base_url, timeout=timeout, api_key=api_key
        )

        self.model = model
        self.mode = mode
        self.prompt = prompt
        self.options = options
        self.response_parsing_function = response_parsing_function

        self.json_schema: "Union[dict[str, Any], None]" = None

        if json_schema is None:
            if mode == "normal":
                self.json_schema = JSON_SCHEMA_NORMAL
            elif mode == "correcting":
                self.json_schema = JSON_SCHEMA_CORRECTING
        else:
            self.json_schema = json_schema

        if options is None:
            self.options = STD_OPTIONS

    def check(self, string: str) -> "tuple[bool, str]":
        """
        Sends the given string to the OpenAI API and checks if it is spam or
        not. Returns a tuple of a boolean (whether it is spam) and the
        potentially corrected string.
        """

        # pylint: disable=no-member

        response_raw = self._client.chat.completions.create(  # type: ignore
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": string},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "SpamSchema",
                    "schema": self.json_schema,
                },
            },  # type: ignore
            stream=False,
            **(self.options if self.options is not None else {}),
        )

        resp_dict: "Union[dict[str, Any], None]" = json.loads(
            response_raw.choices[0].message.content  # type: ignore
        )

        if resp_dict is None:
            raise MalformedResponseException(
                "OpenAI response is None or malformed."
            )

        result: "Tuple[bool, str]" = self.response_parsing_function(resp_dict)

        return (
            result[0],
            string if self.mode == "normal" else result[1],
        )
