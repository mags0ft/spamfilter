"""
Module for the JSON blocklist filter.

More information about this filter can be found in its Class docstring.
"""

from json import load
import os

from .blocklist import Blocklist


class BlocklistFromJSON(Blocklist):
    """
    Behaves just like the `Blocklist` class. Reads a JSON list and inserts it's
    content into the `Blocklist.blocklist` property.

    - `BlocklistFromJSON.file`: filename or path of the JSON file.
    """

    def __init__(
        self, file: str, mode: str = "normal", encoding: str = "utf-8"
    ) -> None:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"The file '{file}' does not exist.")

        with open(file, "r", encoding=encoding) as f:
            super().__init__(set(load(f)), mode)
