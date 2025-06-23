"""
The base filter module that includes a collection of all the available filter
types.
"""

from typing import Type

from .filter import Filter
from .length import Length
from .blocklist import Blocklist
from .specialchars import SpecialChars
from .capitals import Capitals
from .bypass_detection import BypassDetector
from .blocklist_from_json import BlocklistFromJSON
from .word_length import WorldLength
from .regex import Regex
from .email import Email
from .api import API
from .ollama import Ollama

FILTERS: "list[Type[Filter]]" = [
    Length,
    Blocklist,
    SpecialChars,
    Capitals,
    BypassDetector,
    BlocklistFromJSON,
    WorldLength,
    Regex,
    Email,
    API,
    Ollama,
]
