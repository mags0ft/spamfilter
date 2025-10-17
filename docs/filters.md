# 📢 filters

The spamfilter library comes with many built-in filtering algorithms that can determine whether a string is spam
or rather not. In this document, all of these filters will be listed.

## How to import filters

There are a lot of ways to import the filters you need. If you just want to use a pre-made model for filtering,
you don't need to import them at all, they are going to be imported into the library by itself - just use `spamfilter.premade`.

If you want to import the built-in filters into your script, do it using one of the following ways:

*For one single filter:*

```python
from spamfilter.filters import Filter
```

*For several filters:*

```python
from spamfilter.filters import (
    Capitals,
    Length,
    SpecialChars
)
```

*For **all** filters*

```python
from spamfilter.filters import *
```

Please note that wildcard imports are generally not recommended and may raise linter warnings.

## All filters explained

Generally, all filters are stacked onto each other using a pipeline object which will then check them one after each other.

You construct a filter like this:

```python
Filter(**options, mode = "normal")
```

Each filter also has a `check(string: str)` method which accepts a string as an input and will return the filter's assesment of it using the options given at construction as a tuple.

The tuple is built as following:

```python
(passed: int, output_string: str)
```

- **passed** indicated whether the string did complete the check successfully and therefore wasn't indicated as spam.
- **output_string** is the string returned by the filter as it might do corrections on it like lower-casing all letters in case it contains too many capital letters.

---

:::spamfilter.filters.Filter
:::spamfilter.filters.SpecialChars
:::spamfilter.filters.Capitals
:::spamfilter.filters.Length
:::spamfilter.filters.Blocklist
:::spamfilter.filters.BlocklistFromJSON
:::spamfilter.filters.API
:::spamfilter.filters.Regex
:::spamfilter.filters.Email

**Note**: The default regex used by the `Email` filter is `([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)`.

:::spamfilter.filters.OpenAI

**Note**: The default response parsing function is the following:

```python
RespFuncType = Callable[[dict[str, Union[bool, str]]], Tuple[bool, str]]

STD_RESP_FUNC: RespFuncType = lambda resp: (  # type: ignore
    not resp["is_spam"],
    (resp["corrected_text"] if "corrected_text" in resp else ""),
)
```

**Note**: The `Ollama` filter has been deprecated in favor of the `OpenAI` filter.
[Ollama exposes an OpenAI-compatible API](https://ollama.com/blog/openai-compatibility), so you can use the `OpenAI` filter with it.

:::spamfilter.filters.MLTextClassifier

**Note**: The default response parsing function is the following:

```python
def _default_response_parsing_function(
    result: list[dict[str, Union[str, float]]],
) -> bool:
    """
    Default response parsing function that checks if the label
    is 'spam' or 'toxic'.
    """

    sorted_result = sorted(result, key=lambda x: x["score"], reverse=True)
    top_label: str = str(sorted_result[0]["label"]).lower()

    return top_label not in ["spam", "toxic", "hate", "abusive"]
```

---

## Incorporating these filters

If you want to use these filters, please don't use them roughly as `Filter` instance but rather wrapped into a `Pipeline` object.
