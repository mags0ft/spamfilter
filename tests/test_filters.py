"""
Test cases for the filter classes.

Accepts different environment variables to control the behavior of the tests:
- `SPAMFILTER_TEST_OPENAI`: If set to "true", tests the OpenAI filter, which
is expensive and requires a ready endpoint.
- `SPAMFILTER_OPENAI_MODEL`: Specifies the model to use.
- `SPAMFILTER_TEST_ML_CLASSIFIER`: If set to "true", tests the MLClassifier
filter, which is slightly less expensive and requires a transformers
installation.
- `SPAMFILTER_ML_CLASSIFIER_MODEL`: The model to use for the ML Text
Classifier.
"""

from os import getenv

from dotenv import load_dotenv

from spamfilter import filters


load_dotenv()


class TestSetup:
    """
    Test setup class with meta information for running the test suite.
    """

    _prefix = "SPAMFILTER_"

    test_openai = getenv(f"{_prefix}TEST_OPENAI", "false").lower() == "true"
    test_ml = getenv(f"{_prefix}TEST_ML_CLASSIFIER", "false").lower() == "true"

    test_openai_model = getenv(f"{_prefix}OPENAI_MODEL")
    test_ml_model = getenv(f"{_prefix}ML_CLASSIFIER_MODEL")

    test_openai_base_url = getenv(f"{_prefix}OPENAI_API_BASE")
    test_openai_api_key = getenv(f"{_prefix}OPENAI_API_KEY")


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
            filters.OpenAI,
            filters.MLTextClassifier,
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

    f.max_ = 2

    assert f.check("A!a.a:b;c d")[0]
    assert not f.check("Normal sentence")[0]


def test_length_exception() -> None:
    """
    Tests the exceptions of the length filter.
    """

    try:
        filters.Length(padding="##")

        # we should never reach this
        assert False
    except ValueError:
        # all fine!
        pass


def test_length() -> None:
    """
    Tests the standard length filter.
    """

    f = filters.Length()

    assert f.check("Perfectly green apples.")[0]
    assert not f.check("Perfectly green apples." * 10)[0]

    f.mode = "crop"
    f.max_ = 15

    t = "This is a test string - technically too long."
    r = f.check(t)

    assert r[0]


def test_length_fillonly() -> None:
    """
    Tests the length filter in fill-only mode.
    """

    f = filters.Length(min_=20, mode="fill-only", padding="_")

    t = "Short string"
    r = f.check(t)

    assert r[0]
    assert r[1] == t + "_" * (20 - len(t))

    t2 = "This string is definitely long enough."
    r2 = f.check(t2)

    assert r2[0]
    assert r2[1] == t2


def test_length_shortenonly() -> None:
    """
    Tests the length filter in shorten-only mode.
    """

    f = filters.Length(max_=25, mode="shorten-only")

    t = "This string is definitely way too long to be accepted."
    r = f.check(t)

    assert not r[0]
    assert r[1] == t[:25]

    t2 = "Short enough."
    r2 = f.check(t2)

    assert r2[0]
    assert r2[1] == t2


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


def test_openai() -> None:
    """
    Tests the OpenAI API compatible filter.
    """

    if not TestSetup.test_openai:
        return

    if not TestSetup.test_openai_model:
        raise ValueError(
            "Please set the SPAMFILTER_OPENAI_MODEL environment variable to a "
            "valid OpenAI model."
        )

    assert TestSetup.test_openai_base_url is not None

    f = filters.OpenAI(
        TestSetup.test_openai_model,
        base_url=TestSetup.test_openai_base_url,
        api_key=TestSetup.test_openai_api_key,
        timeout=30,
    )

    assert f.check("Thanks for the great video, really liked it")[0]
    assert not f.check("BUY THE BEST MAGAZINES TODAY AT NOON IN MY STORE!")[0]


def test_ml_classification() -> None:
    """
    Tests the ML text classification filter.
    """

    if not TestSetup.test_ml:
        return

    if not TestSetup.test_ml_model:
        raise ValueError(
            "Please set the SPAMFILTER_ML_CLASSIFIER_MODEL environment "
            "variable to a valid ML model."
        )

    f = filters.MLTextClassifier(TestSetup.test_ml_model)

    assert f.check("Have you ever heard about dragonfruit?")[0]
    assert not f.check("Go fuck yourself, you're so ugly, buah.")[0]
