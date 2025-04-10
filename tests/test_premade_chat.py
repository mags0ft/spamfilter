"""
Test cases for the pre-made chat filtering mechanisms.
"""

from spamfilter.premade import chat

m = chat.create_machine()


def test_capitals():
    """
    Tests against a message with too many capital letters.
    """

    message = "CAPITAL LETTER MESSAGE."
    expected = message.lower()

    res = m.check(message)

    assert res.changes_made == 1
    assert res.passed
    assert res.result == expected


def test_char_spam():
    """
    Tests if spamming random characters is detected correctly.
    """

    spam = [
        "oeidbnfpiowsubvpesirfsbugvp",
        "pqiwfdjhiweufgbwoirngvb",
        "<osedifhrepiugvbnepiugbnpeo",
        "e0wfpjnrüweogivbnep98g43z098721",
        "eifhbnipwseubvrierug0983745gt38704h2poirnf2pgivubo8q7waegfc",
        "03rhfeiubfwiolgvop984i",
        "pefjouwbnfviurghnnreb",
    ]

    for string in spam:
        assert not m.check(string).passed


def test_symbol_spam():
    """
    Tests if spamming random symbols is correctly identified as spam.
    """

    spam = [
        "§(/%=)§%&=(/$&())",
        '?=&%()/)"(&%§?%)',
        ")/)(&/=)((%((>:>)",
        "[]}{}][]}{[ß]}",
    ]

    for string in spam:
        assert not m.check(string).passed


def test_bypass_detect():
    """
    Tests the bypass detection filter.
    """

    assert not m.check("I want to b y p a s s the f i l t e r.").passed
    assert not (
        m.check(
            "This is a fairly long text, but it does still contain some, \
let's say, s u s p i c i o u s string of text in it!"
        ).passed
    )
