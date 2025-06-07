# 🔎 Results

The `spamfilter` module is highly object-oriented and therefore encapsulates results of filtering runs in a `Result` object which will be constructed once a pipeline is done filtering a string.

The Result object is made to unify returned data by pipelines and is very easy to use.

:::spamfilter.result.Result

## Create your own result

Whenever you need to create your own `Result` object, just do as follows:

```python
from spamfilter.results import Result

r = Result(...args)
```