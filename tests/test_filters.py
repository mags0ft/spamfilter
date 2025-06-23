"""
Test cases for the filter classes.

Accepts different environment variables to control the behavior of the tests:
- `SPAMFILTER_TEST_OLLAMA`: If set to "true", tests the Ollama filter, which
is expensive and requires an Ollama installation.

"""

from os import getenv

from dotenv import load_dotenv

from spamfilter import filters


load_dotenv()

TEST_OLLAMA = getenv("SPAMFILTER_TEST_OLLAMA", "false").lower() == "true"
TEST_OLLAMA_MODEL = getenv(
    "SPAMFILTER_OLLAMA_MODEL",
)


def test_empty_inputs() -> None:
    """
    Tests the filters' reactions to empty input strings.
    """

    for filter_ in filters.FILTERS:
        if filter_ in [
            filters.Length,
            filters.Blocklist,
            filters.BlocklistFromJSON,
            filters.Regex,
            filters.API,
            filters.Ollama,
        ]:
            continue
        print(filter_)
        assert filter_().check("")[0]


def test_blocklist() -> None:
    """
    Tests the functionality of the blocklist filter.
    """

    l = {"badword", "pancake"}

    f = filters.Blocklist(l)

    assert not f.check("This is a badword.")[0]
    assert f.check("This is a ppancakee.")[0]


def test_strict_blocklist() -> None:
    """
    Tests the blocklist filter in strict mode.
    """

    l = {"pancake"}

    f = filters.Blocklist(l, mode="strict")

    assert not f.check("This is a ppancakee.")[0]
    assert f.check("This is a ppanccakee.")[0]


def test_bypass_detection() -> None:
    """
    Tests the bypass detection filter.
    """

    f = filters.BypassDetector()

    assert not f.check("I am trying to b y p a s s  y o u!")[0]
    assert not f.check("Again want to b_y_p_a_s_s  y!o!u")[0]
    assert f.check("This is a normal string to test against")[0]


def test_capitals() -> None:
    """
    Tests the capital-sensitive filter.
    """

    f = filters.Capitals()

    for message in [
        "AGGRESSIVELY SPAMMING CAPITALS",
        "AGGRESSIVELY SPAMMING capitals, but not fully",
        "Teetering riiight on the BRINK OF IT.",
    ]:
        assert not f.check(message)[0]

    assert f.check("This is a perfectly reasonable PHRASE.")[0]
    assert f.check("I")[0]


def test_capitals_crop() -> None:
    """
    Tests the cropping mode of the capitals filter.
    """

    f = filters.Capitals(mode="crop")
    t = "APPLES ARE SOMETHING REALLY GREAT."

    r = f.check(t)
    assert r[0]
    assert r[1] == t.lower()

    t = "Totally normal sentence."

    r = f.check(t)
    assert r[0]
    assert r[1] == t


def test_email() -> None:
    """
    Tests the email filter.
    """

    f = filters.Email()
    t = "Hey there! My email is john.doe@subdomain.example.com."

    assert not f.check(t)[0]

    f.mode = "censor"
    r = f.check(t)

    assert r[0]
    assert r[1] == "Hey there! My email is ***."


def test_word_length() -> None:
    """
    Tests the word length filter.
    """

    f = filters.WorldLength()

    assert f.check("This is a perfectly normal sentence about tomatoes.")[0]
    assert not f.check(
        "Haha wiebcfierdjnwoidhiruerilh certainly wudciuewbifwubwieb weiudcber"
    )[0]

    f.max_length = 2

    assert f.check("A!a.a:b;c d")[0]
    assert not f.check("Normal sentence")[0]


def test_length() -> None:
    """
    Tests the standard length filter.
    """

    f = filters.Length()

    assert f.check("Perfectly green apples.")[0]
    assert not f.check("Perfectly green apples." * 10)[0]

    f.mode = "crop"
    f.max = 15

    t = "This is a test string - technically too long."
    r = f.check(t)

    assert r[0]
    assert r[1] == t[:15]


def test_specialchars() -> None:
    """
    Tests the specialchars filter.
    """

    f = filters.SpecialChars()

    assert f.check("Great video!!! Thanks (so much) for explaining this.")[0]
    assert not f.check("HAHA!!!!!!!!")[0]

    f.mode = "crop"
    t = "This is so great*)§($="
    r = f.check(t)

    assert r[0]
    assert r[1] == t[:16]


def test_ollama() -> None:
    """
    Tests the Ollama filter.
    """

    if not TEST_OLLAMA:
        return

    if not TEST_OLLAMA_MODEL:
        raise ValueError(
            "Please set the SPAMFILTER_OLLAMA_MODEL environment variable to a "
            "valid Ollama model."
        )

    f = filters.Ollama(TEST_OLLAMA_MODEL, timeout=30)

    assert f.check("Thanks for the great video, really liked it")[0]
    assert not f.check("BUY THE BEST MAGAZINES TODAY AT NOON IN MY STORE!")[0]
