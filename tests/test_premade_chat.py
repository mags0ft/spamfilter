from src.spamfilter.premade import chat

m = chat.create_machine()

def test_capitals():
    MSG = "CAPITAL LETTER MESSAGE."
    EXPECTED = "capital letter message."

    res = m.check(MSG)

    assert res.changes_made == 1
    assert res.passed
    assert res.result == EXPECTED

def test_char_spam():
    SPAM = [
        "oeidbnfpiowsubvpesirfsbugvp",
        "pqiwfdjhiweufgbwoirngvb",
        "<osedifhrepiugvbnepiugbnpeo",
        "e0wfpjnrüweogivbnep98g43z098721",
        "eifhbnipwseubvrierug0983745gt38704h2poirnf2pgivubo8q7waegfc",
        "03rhfeiubfwiolgvop984i",
        "pefjouwbnfviurghnnreb"
    ]

    for string in SPAM:
        assert m.check(string).passed == False

def test_symbol_spam():
    SPAM = [
        "§(/%=)§%&=(/$&())",
        '?=&%()/)"(&%§?%)',
        ")/)(&/=)((%((>:>)",
        "[]}{}][]}{[ß]}"
    ]

    for string in SPAM:
        assert m.check(string).passed == False

def test_bypass_detect():
    assert m.check("I want to b y p a s s the f i l t e r.").passed == False
    assert m.check("This is a fairly long text, but it does still contain some, let's say, s u s p i c i o u s string of text in it!")