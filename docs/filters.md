# 📢 filters

The spamfilter module comes with many built-in filtering algorithms that can determine whether a string is spam
or rather not. In this document, all of these filters will be listed.

## How to import filters

There are a lot of ways to import the filters you need. If you just want to use a pre-made model for filtering,
you don't need to import them at all, they are going to be imported into the model by itself.

If you want to import the built-in filters into your script, do it using one of the following ways:

*For one single filter:*
```
from spamfilter.filters import Filter
```

*For several filters:*

```python
from spamfilter.filters import (
    Capitals,
    Length,
    Symbols
)
```

*For **all** filters*

```python
from spamfilter.filters import *
```

## All filters explained
Generally, all filters are stacked onto each other using a machine object which will then check them one after each other.

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
- **output_string** is the string returned by the filter as it might do corrections on it like lower-casing all letters in case it's too much capital.

---

## filters.Filter
**Base class. No functionality.**

`filters.Filter(mode: str = "default")`

The `Filter` class is the class all other filters inherit from. It does not contain any further functionality and will always return the string it was given as input, marked as **passed**.

**args**:

`Filter.mode`: the mode of the filter.
- `default`: default mode, no functionality.

---
## filters.Capitals
**Filters out texts with too many capital letters.**

`filters.Capitals(percentage: float = 0.3, mode: str = "normal", abs_safe_min: int = 3)`

Check if a string contains too much capitals.

**args**:

`Capitals.percentage`: how many percent of the text need to be in capital for it to fail.

`Capitals.mode`: how to handle a failing string.
- `normal`: fail the string 
- `crop`: crop all letters to lowercase if the string is - too capital, makes it **always pass** (!)

- `Capitals.abs_safe_min`: the absolute amound of capital characters that are always okay. Set to -1 to deactivate.

---
## filters.Length
**Filters out too short/long texts.**

`filters.Length(min_length: int = 10, max_length: int = 200, padding: str = " ", mode: str = "normal")`

Checks if a string matches given length requirements.

**args**:


`Length.min`: The inclusive minimum length.

`Length.max`: The inclusive maximum length.

`Length.padding`: A character used to fill up strings that are too short in the `crop` mode.

`Length.mode`: How to handle failing strings.

- `normal`: Fail too short or too long strings.
- `crop`: Shorten too long strings and fill too short strings up using `Length.padding`.

---
## filters.Symbols
**Filters for too many symbols.**

`filters.Symbols(percentage: float = 0.15, mode: str = "normal", symboldef: str = "explicit", abs_safe_min: int = 3)`

Check if a string contains too many symbols.

**args**:

`Symbols.percentage`: how many percent of the text need to be symbols for it to fail.

`Symbols.mode`: how to handle a failing string.

- `normal`: fail the string if it contains too many symbols
- `crop`: remove all symbols from the string if it would fail, but then make the string pass.

`Symbols.symboldef`: what to identify as a symbol

- `explicit`: everything that matches `Symbols.symbolset`.
- `implicit`: everything that does not match `Symbols.charset`.
 - ⚠ **WARNING!** Use `implicit` with caution. Explicit is better than implicit. Non-latin characters may unfortunately be detected as a symbol in implicit mode. `explicit` is way more safe to use.

`Symbols.abs_safe_min`: absolute amount of symbols that are always okay to use. Set to -1 to deactivate.

---
## filters.WordLength
**Filters for too long, standalone words.**

`filters.WordLength(max_length: int = 20, mode: str = "absolute", max_abs_population: int = 1, max_perc_population: float = 0.1)`

Checks if the words in a string match given length requirements.

**args**:

`Length.max`: The inclusive maximum length of a single word.

`Length.max_abs_population`: The maximum amount of too long words to make the string fail.

`Length.max_perc_population`: The maximum percentage of too long words to make the string fail.

`Length.mode`: How to detect failing strings.

- `absolute`: Fail the string if there are too many words that are too long, specified in `max_abs_population` as a max int.
- `percentage`: Fail the string if there more too long words than the specified percentage in `max_perc_population` as a percentage float.
- `hybrid`: Fail the string if not both of the above conditions are met.

`Length.split_regex`: The regex used to split into standalone words.

---
## filters.PersonalInformation
**Personal information detection base class.**

`filters.PersonalInformation(regex: str, mode: str = "normal", replacement: str = r"***")`

Base class other filters for personal information inherit from.

**args**:

`PersonalInformation.mode`: how to handle a failing string.

- `normal`: fail the string.
- `censor`: censor the information.

`PersonalInformation.regex`: the regex used to check for info.

`PersonalInformation.replacement`: what regex to replace info with.

---
## filters.Email
**Filters for accidentally exposed email addresses in texts to filter them out before they reach the public.**

`filters.Email(regex: str = r"([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", mode: str = "normal", replacement: str = r"***")`

Check if a string contains an email address.

**args**:

`Email.mode`: how to handle a failing string.

- `normal`: fail the string.
- `censor`: censor the information.

`Email.regex`: the regex used to check for email addresses.

`Email.replacement`: what regex to replace email addresses with.

---
## filters.BypassDetector
**Detects fraudulently constructed strings which try to bypass the filters using spaces between the characters.**

`filters.BypassDetector(percentage = 0.4, max_findings = 5)`

Detect if a string is written to bypass filtering.

This is achieved by checking if characters are commonly adjacent to characters that could be used to confuse the filters.
The safe characters are called "isles" and defined as a list of characters in `BypassDetector.isles`.

**args**:

`BypassDetector.percentage`: percentage of suspicious adjacencies needed to fail.

`BypassDetector.max_findings`: absolute number of suspicious adjacencies needed to fail.

---
## filters.Blocklist
**Filters for words in a string using a black-/blocklist.**

`filters.Blocklist(blocklist: set, mode: str = "normal")`

Filter text for blocked words. Works better in combination with `BypassDetector`.

**args**:

`Blocklist.mode`: How to handle incoming text.

- `normal`: search for profane words adjacent to punctuation or spaces.
- `strict`: search for any occurence of a profane word.\
**WARNING**: this might detect words like "classic" as they contain parts of a profane words.
- `tolerant`: simply replace the problematic words.

`Blocklist.blocklist`: a python `set()` with words as `str` objects that shall be blocked.

`Blocklist.ignore_regex`: a regular expression that matches punctuation characters for splitting the string in non-strict mode.

`Blocklist.profanity_replacement`: what to replace profanity with.

---
## filters.BlocklistFromJSON
**Filters for words in a string using a black-/blocklist loaded from a JSON file list.**

`filters.BlocklistFromJSON(file: str, mode: str = "normal")`

Behaves just like the `Blocklist` class. Reads a JSON list and inserts it's content into the `Blocklist.blocklist` property.

**args**:

`BlocklistFromJSON.file`: filename of JSON file.

## Incorporating these filters

If you want to use these filters, please don't use them roughly as `Filter` instance but rather wrapped into a `Machine` object.