from .blocklist import Blocklist
from json import load

class BlocklistFromJSON(Blocklist):
    """
    Behaves just like the `Blocklist` class. Reads a JSON list and inserts it's content into the `Blocklist.blocklist` property.
    `BlocklistFromJSON.file`: filename of JSON file.
    """

    def __init__(self, file : str, mode : str = "normal"):
        with open(file, "r") as f:
            super().__init__(set(load(f)), mode)