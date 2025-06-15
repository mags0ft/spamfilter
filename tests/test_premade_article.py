"""
Test cases for the pre-made article filtering mechanisms.
"""

from spamfilter.premade import article
from spamfilter.filters import BypassDetector, SpecialChars, Length

m = article.create_pipeline()


LEGITIMATE_ARTICLE = """
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At
vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum
dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero
eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no
sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit
amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut
labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam
et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata
sanctus est Lorem ipsum dolor sit amet.  

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie
consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan
et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis
dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer.
"""

BYPASS_SEQUENCE = """
This sequence of the a-r-t-i-c-l-e consists o_f__p#r-o/f!a(n)i%t.y!
"""


def test_length():
    """
    Tests against an too short or too long articles.
    """

    # Test for too long articles
    res = m.check(LEGITIMATE_ARTICLE * 250)

    assert res.changes_made == 0
    assert not res.passed
    assert any(isinstance(f, Length) for f in res.failed_filters)

    # Test for too short articles
    res = m.check(LEGITIMATE_ARTICLE[:64])

    assert res.changes_made == 0
    assert not res.passed
    assert any(isinstance(f, Length) for f in res.failed_filters)

    # Test for legitimate articles
    res = m.check(LEGITIMATE_ARTICLE)

    assert res.changes_made == 0
    assert res.passed


def test_symbol_spam():
    """
    Tests against symbol spam.
    """

    res = m.check("abc!/)=(!?-" * 40)

    assert res.changes_made == 0
    assert not res.passed

    assert any(isinstance(f, SpecialChars) for f in res.failed_filters)


def test_bypass_protection():
    """
    Tests against articles that try to bypass the filters.
    """

    res = m.check(LEGITIMATE_ARTICLE + BYPASS_SEQUENCE)

    assert res.changes_made == 0
    assert not res.passed

    assert any(isinstance(f, BypassDetector) for f in res.failed_filters)
