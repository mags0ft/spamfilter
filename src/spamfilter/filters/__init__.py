"""
The base filter module that includes a collection of all the available filter
types.
"""

from typing import Type
from .filter import Filter
from .length import Length
from .blocklist import Blocklist
from .symbols import Symbols
from .capitals import Capitals
from .bypass_detection import BypassDetector
from .blocklist_from_json import BlocklistFromJSON
from .word_length import WorldLength
from .personal_information import PersonalInformation
from .email import Email

FILTERS: "list[Type[Filter]]" = [
    Length,
    Blocklist,
    Symbols,
    Capitals,
    BypassDetector,
    BlocklistFromJSON,
    WorldLength,
    PersonalInformation,
    Email,
]
