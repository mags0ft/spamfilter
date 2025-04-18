"""
The module containing the Result class, a data structure to manage the output
of Pipelines.
"""

from dataclasses import dataclass, field
from typing import Type

from ..filters.filter import Filter


@dataclass
class Result:
    """
    Dataclass to determine a result of a string running through a filtering
    pipeline.

    - `Result.passed`: bool whether the text passed the filters.
    - `Result.result`: resulting, sanitized string.
    - `Result.original`: the string before getting passed through the filtering
    pipelines.
    - `Result.changes_made`: how many changes have been commited to the string
    by the filters.
    - `Result.failed_filters`: the filters that made the string fail if it did.
    """

    passed: bool = True
    result: str = ""
    original: str = ""
    changes_made: int = 0
    failed_filters: "list[Type[Filter]]" = field(default_factory=list)
