"""
Module for the API-based spam filter class.
"""

from typing import Any, Callable, Literal, Union

try:
    import requests

    requests_available: bool = True
except ImportError:
    requests_available: bool = False

from .check_modes import perform_mode_check
from .filter import Filter


POSSIBLE_MODES: "list[str]" = ["normal"]


class InvalidAPIInputParametersException(Exception):
    """
    Exception thrown when invalid input parameters for the filter are found.
    """


class InvalidAPIResponseException(Exception):
    """
    Exception raised upon encountering an invalid API response.
    """


def check_requests_availability():
    """
    Checks if the `requests_available` global has been set to `True`, otherwise
    raises an exception.
    """

    if not requests_available:
        raise ImportError(
            "Please install the API dependencies for spamfilter using \
`pip install spamfilter[api]`."
        )


class API(Filter):
    """
    JSON API-based, synchronous spam filter. Requires installation with the
    optional API dependencies: `pip install spamfilter[api]`.

    - `API.url`: API URL to call.
    - `API.headers`: dictionary of headers to pass to the API
    - `API.method`: whether to use GET (`get`) or POST (`post`)
    - `API.payload_func`: function called before the request to the API is
    sent; needs to convert the passed argument, the text string, to a
    dictionary with the correct payload format used by your API of choice.
    - `API.interpretation_func`: function called after the response arrives;
    gets the JSON response passed to it and needs to figure out if the filter
    shall pass. Needs to return a tuple of a boolean and the modified string.
    - `API.timeout`: After how many seconds the request to the API shall time
    out.
    - `API.mode`: currently, only "normal" is supported.

    - `API.check(string: str)`: send this string to the API and check the
    response JSON against the provided
    """

    def __init__(
        self,
        url: str,
        headers: "dict[str, Any]",
        method: 'Literal["get", "post"]',
        payload_func: "Callable[[str], dict[str, Any]]",
        interpretation_func: "Callable[[dict[str, Any]], tuple[bool, str]]",
        timeout: float = 3.0,
        mode: str = "normal",
    ) -> None:
        perform_mode_check(mode, POSSIBLE_MODES)
        check_requests_availability()

        self.url = url
        self.headers = headers
        self.method = method
        self.payload_func = payload_func
        self.interpretation_func = interpretation_func
        self.timeout = timeout
        self.mode = mode

    def check(self, string: str) -> "tuple[bool, str]":
        payload: "dict[str, Any]" = self.payload_func(string)
        method_lower: str = self.method.lower()
        resp: "Union[None, requests.Response]" = None

        if method_lower == "get":
            resp = requests.get(  # type: ignore
                self.url,
                params=payload,
                headers=self.headers,
                timeout=self.timeout,
            )
        elif method_lower == "post":
            resp = requests.post(  # type: ignore
                self.url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout,
            )
        else:
            raise InvalidAPIInputParametersException(
                'The mode for the API filter needs to be "get" or "post".'
            )

        try:
            resp_json = resp.json()
            return self.interpretation_func(resp_json)
        except requests.exceptions.JSONDecodeError:  # type: ignore
            # pylint: disable=raise-missing-from
            raise InvalidAPIResponseException(
                "The API did not return a valid response (response object is \
not valid JSON)."
            )
