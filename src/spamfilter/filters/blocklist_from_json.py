"""
Module for the JSON blocklist filter.

More information about this filter can be found in its class docstring.
"""

from json import load, JSONDecodeError
import os
from typing import Union

from .blocklist import Blocklist


class BlocklistFromJSON(Blocklist):
    """
    Behaves just like the `Blocklist` class. Reads a JSON list and inserts it's
    content into the `Blocklist.blocklist` property.

    - `BlocklistFromJSON.file`: filename or path of the JSON file.
    - `BlocklistFromJSON.mode`: how to handle a failing string.
        - `normal`: fail the string.
        - `censor`: censor the blocked words.
    - `BlocklistFromJSON.encoding`: the encoding used to read the JSON file.

    Raises `FileNotFoundError` if the file does not exist and `JSONDecodeError`
    if the file does not contain valid JSON data. Also raises `ValueError` if
    the JSON data is not a list.
    """

    def __init__(
        self, file: str, mode: str = "normal", encoding: str = "utf-8"
    ) -> None:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"The file '{file}' does not exist.")

        json_data: "Union[list[str], None]" = None

        try:
            with open(file, "r", encoding=encoding) as f:
                json_data = load(f)
        except JSONDecodeError as e:
            raise JSONDecodeError(
                f'The file "{file}" does not contain valid JSON data.',
                e.doc,
                e.pos,
            ) from e

        if not isinstance(json_data, list):
            raise ValueError(
                f'The file "{file}" does not contain a JSON list.'
            )

        with open(file, "r", encoding=encoding) as f:
            super().__init__(set(json_data), mode)
