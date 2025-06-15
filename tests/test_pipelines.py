"""
These tests cover the Pipeline class of the spamfilter package.
"""

from spamfilter.pipelines import Pipeline
from spamfilter.filters import Capitals, Filter, Length, SpecialChars


# TODO: fix typing linter warnings by changing type definitions
# (in the long run)


def test_empty_pipeline():
    """
    Tests the library's behavior when there is an empty pipeline.
    """

    pipe = Pipeline([])

    for text in ["", "A text", "Long text, " * 100]:
        res = pipe.check(text)

        assert res.passed
        assert res.changes_made == 0
        assert res.failed_filters == []


def test_doubled_filters_in_pipeline():
    """
    Tests what happens when filters are doubled in a pipeline.
    """

    pipe = Pipeline(
        [
            Capitals(),
            Capitals(),
        ]  # type: ignore -- the types match as-is, but not formally.
    )

    assert pipe.check("valid").passed
    assert not pipe.check("INVALID").passed


def test_full_pipeline():
    """
    Tests what happens when a Pipeline is very full.
    """

    pipe = Pipeline()

    for _ in range(10_000):
        pipe.filters.append(Filter())  # type: ignore

    assert pipe.check("").passed


def test_normal_pipeline():
    """
    A normal test case for a pipeline.
    """

    pipe = Pipeline(
        [Length(), SpecialChars(), Capitals()]  # type: ignore -- types match
    )

    res = pipe.check("This is a perfectly normal piece of text.")

    assert res.changes_made == 0
    assert res.passed

    res = pipe.check("RANDOM PIECE OF TEXT")

    assert res.changes_made == 0
    assert not res.passed
    assert any(isinstance(f, Capitals) for f in res.failed_filters)

    res = pipe.check("A long piece of text" * 100)

    assert res.changes_made == 0
    assert not res.passed
    assert any(isinstance(f, Length) for f in res.failed_filters)

    res = pipe.check("SpecialChars /&(§)!(=!/=!/())")

    assert res.changes_made == 0
    assert not res.passed
    assert any(isinstance(f, SpecialChars) for f in res.failed_filters)
