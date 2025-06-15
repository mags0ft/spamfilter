# 🎨 The `Pipeline` class

Pipelines in `spamfilter` allow you to customize own models that periodically work through the filters wrapped into them.

**Please note**: Prior to `spamfilter` v2.0.0, the pipelines were called "machines". This is no longer the case, as we figured the term "machine" is not fully accurate for the way they work. The term "pipeline" is the new standard, as it describes the process of passing data through a series of filters. Thus, `spamfilter` v2.0.0 is a **breaking change** and you will need to update your code if you used machines before.

## How to import the pipeline class

To import the class of a Pipeline, simply run:

```python
from spamfilter.pipelines import Pipeline
```

## Pipelines explained
Generally, all filters are stacked onto each other using a pipeline object which will then check them one after each other.

A pipeline also has a `check(string: str)` method which accepts a string as an input and will return a [`results.Result`](./results.md) object. This object contains info about the filtering run.

Check the [documentation for `results.Result`](./results.md) for more information.

---

:::spamfilter.pipelines.Pipeline

**Filters may modify the strings they get as input. The pipeline will pass the modified strings from one filter to the next ones:**

[**THIS IS A CAPITAL STRING**]

 ⬇

[`Capitals` filter]

 ⬇

[**this is a capital string**]

 ⬇

[other filters...]

---
### An example

This is an example of how you could implement three filters into one pipeline, which will check the string of them through each of the given filters.

```python
from spamfilter.pipelines import Pipeline
from spamfilter.filters import (
    Capitals,
    SpecialChars,
    Length
)

m = Pipeline([
    Capitals(),
    SpecialChars(mode = "crop"),
    Length(min_length = 20, max_length = 60)
])

print(
    m.check("Test string!").passed
)
```