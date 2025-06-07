# 🔎 Results

The `spamfilter` module is highly object-oriented and therefore encapsulates results of filtering runs in a `Result` object which will be constructed once a pipeline is done filtering a string.

The Result object is made to unify returned data by pipelines and is very easy to use.

## The `Result` object

Dataclass to determine a result of a string running through a filtering pipeline.

`results.Result(passed = True, result = "", original = "", changes_made = 0, failed_filters = [])`

`Result.passed`: bool whether the text passed the filters.

`Result.result`: resulting, sanitized string.

`Result.original`: the string before getting passed through the filtering pipelines.

`Result.changes_made`: how many changes have been commited to the string by the filters.

`Result.failed_filters`: the filter objects that made the string fail (if it did).

## Create your own result

Whenever you need to create your own `Result` object, just do as follows:

```python
from spamfilter.results import Result

r = Result(...args)
```