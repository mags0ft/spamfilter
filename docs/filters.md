# 📢 filters

The spamfilter module comes with many built-in filtering algorithms that can determine whether a string is spam
or rather not. In this document, all of these filters will be listed.

## How to import filters

There are a lot of ways to import the filters you need. If you just want to use a pre-made model for filtering,
you don't need to import them at all, they are going to be imported into the model by itself.

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
:::spamfilter.filters.Ollama

---

## Incorporating these filters

If you want to use these filters, please don't use them roughly as `Filter` instance but rather wrapped into a `Pipeline` object.
