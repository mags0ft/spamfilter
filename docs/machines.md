# 🎨 The `Machine` class

Machines in `spamfilter` allow you to customize own models that periodically work through the filters wrapped into them.

## How to import the machine class

To import the class of a Machine, simply run:

```
from spamfilter.machines import Machine
```

## Machines explained
Generally, all filters are stacked onto each other using a machine object which will then check them one after each other.

A machine also has a `check(string: str)` method which accepts a string as an input and will return a [`results.Result`](./results.md) object. This object contains info about the filtering run.

Check the [documentation for `results.Result`](./results.md) for more information.

---

### `machines.Machine`
**The main class used to stack/wrap filters.**

`machines.Machine(filters: list = [], mode: str = "normal")`

A machine is an object that accepts several filters and passes strings through these.

It's the core mechanism to filter potential spam strings.

**Filters may modify the strings they get as input. The machine will pass the modified strings from one filter to the next ones:**

[**THIS IS A CAPITAL STRING**]\
 ⬇\
[`Capitals` filter]\
 ⬇\
[**this is a capital string**]\
 ⬇\
[other filters...]

**args**:

`Machine.filters`: this property is a list of all filters in a machine. The order is kept.

`Machine.mode`: can either be `"normal"`, `"tolerant`" or `"zero-tolerance"`.

- `"normal"` lets filters change the string itself and will make strings fail if a filter says so.
- `"normal-quick"` is like normal, but stops execution as soon as a fail happens.
- `"tolerant`" passes strings, no matter what filters say, and does not stop execution of them on fail.
- `"zero-tolerance"` does not accept any changes to a string and fails it as soon as a filter registers something.

---
### An example

This is an example of how you could implement three filters into one machine, which will check the string of them through each of the given filters.

```
from spamfilter.machines import Machine
from spamfilter.filters import (
    Capitals,
    Symbols,
    Length
)

m = Machine([
    Capitals(),
    Symbols(mode = "crop"),
    Length(min_length = 20, max_length = 60)
])

print(
    m.check("Test string!").passed
)
```