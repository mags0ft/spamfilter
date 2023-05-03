# 🔎 Results

The `spamfilter` module is highly object-oriented and therefore encapsulates results of filtering runs in a `Result` object which will be constructed once a machine is done filtering a string.

The Result object is made to unify returned data by machines and is very easy to use.

## The `Result` object

Class to determine a result of a string running through a filtering machine.

`results.Result(passed = True, res_string = "", original_string = "", changes = 0, failed_filters = [])`

`Result.passed`: bool whether the text passed the filters.

`Result.result`: resulting, sanitized string.

`Result.original`: the string before getting passed through the filtering machines.

`Result.changes_made`: how many changes have been commited to the string by the filters.

`Result.failed_filters`: the filter objects that made the string fail (if it did).

## Create your own result

Whenever you need to create your own `Result` object, just do as follows:

```
from spamfilter.results import Result

r = Result(...args)
```