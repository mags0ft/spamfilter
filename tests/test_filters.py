"""
Test cases for the filter classes.
"""

from spamfilter import filters


def test_empty_inputs():
    """
    Tests the filters' reactions to empty input strings.
    """

    for filter_ in filters.FILTERS:
        if filter_ in [
            filters.Length,
            filters.Blocklist,
            filters.BlocklistFromJSON,
            filters.PersonalInformation,
        ]:
            continue
        print(filter_)
        assert filter_().check("")[0]


def test_blocklist():
    """
    Tests the functionality of the blocklist filter.
    """

    l = {"badword", "pancake"}

    f = filters.Blocklist(l)

    assert not f.check("This is a badword.")[0]
    assert f.check("This is a ppancakee.")[0]


def test_strict_blocklist():
    """
    Tests the blocklist filter in strict mode.
    """

    l = {"pancake"}

    f = filters.Blocklist(l, mode="strict")

    assert not f.check("This is a ppancakee.")[0]
    assert f.check("This is a ppanccakee.")[0]
