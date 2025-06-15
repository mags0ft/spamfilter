"""
Test cases for the pre-made chat filtering mechanisms.
"""

from spamfilter.premade import chat
from spamfilter.filters import WorldLength, SpecialChars, BypassDetector

m = chat.create_pipeline()


def test_capitals():
    """
    Tests against a message with too many capital letters.
    """

    for message in [
        "CAPITAL LETTER MESSAGE.",
        "I LOVE YOU ALL",
        "Crazy? I WAS CRAZY once.",
    ]:
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
        res = m.check(string)

        assert not res.passed
        assert any(isinstance(f, WorldLength) for f in res.failed_filters)


def test_symbol_spam():
    """
    Tests if spamming random specialchars is correctly identified as spam.
    """

    spam = [
        "§(/%=)§%&=(/$&())",
        '?=&%()/)"(&%§?%)',
        ")/)(&/=)((%((>:>)",
        "[]}{}][]}{[ß]}",
        "!!!!!!!!!!!!!!!!",
        "huh?!?!??§)",
        ";-; <3<3<3<3<3<3",
    ]

    for string in spam:
        res = m.check(string)

        assert not m.check(string).passed
        assert any(isinstance(f, SpecialChars) for f in res.failed_filters)


def test_bypass_detect():
    """
    Tests the bypass detection filter.
    """

    res = m.check("I want to b y p a s s the f i l t e r.")
    assert not res.passed
    assert any(isinstance(f, BypassDetector) for f in res.failed_filters)

    assert not (
        m.check(
            "This is a fairly long text, but it does still contain some, \
let's say, s u s p i c i o u s string of text in it!"
        ).passed
    )
    assert any(isinstance(f, BypassDetector) for f in res.failed_filters)
