"""
Module for the JSON blocklist filter.

More information about this filter can be found in its Class docstring.
"""

from json import load

from .blocklist import Blocklist


class BlocklistFromJSON(Blocklist):
    """
    Behaves just like the `Blocklist` class. Reads a JSON list and inserts it's
    content into the `Blocklist.blocklist` property.

    - `BlocklistFromJSON.file`: filename of JSON file.
    """

    def __init__(
        self, file: str, mode: str = "normal", encoding: str = "utf-8"
    ) -> None:
        with open(file, "r", encoding=encoding) as f:
            super().__init__(set(load(f)), mode)
