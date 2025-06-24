<p align="center">
    <img src="https://raw.githubusercontent.com/mags0ft/spamfilter/master/docs/assets/icon-white-box.png" alt="Spamfilter logo" width=350>
</p>

<h1 align="center">spamfilter</h1>

<p align="center">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/spamfilter?style=for-the-badge&logo=pypi&labelColor=%231e1e1e" />
    <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/mags0ft/spamfilter/python-package.yml?style=for-the-badge&logo=python&labelColor=%231e1e1e" />
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/spamfilter?style=for-the-badge&labelColor=%231e1e1e" />
</p>

The `spamfilter` module is a lightweight, fast and straightforward Python package that helps you to build your own [spam filtering pipelines](https://mags0ft.github.io/spamfilter/pipelines/) in order to keep your applications featuring user-generated content clean.

It's object-oriented and makes a quick, concise approach to remove spam easy. `spamfilter` is highly configurable and ships with deep integrations for [third-party APIs](https://mags0ft.github.io/spamfilter/filters/#spamfilter.filters.API) and language models via [Ollama](https://mags0ft.github.io/spamfilter/filters/#spamfilter.filters.Ollama).

---

**Important links**
- [🌎 Website and documentation](https://mags0ft.github.io/spamfilter/)
- [🔓 Report a security vulnerability](https://github.com/mags0ft/spamfilter/security/advisories/new)
- [🚩 Create a new issue](https://github.com/mags0ft/spamfilter/issues/new/choose)
- [👩‍💻 How to contribute](https://mags0ft.github.io/spamfilter/contributing/)

## Installation

You can [install spamfilter](https://mags0ft.github.io/spamfilter/installation/) by cloning the GitHub repository, downloading it from the GitHub page or using pip - which is the recommended approach:

```bash
pip install spamfilter
```

Please see the [installation guide](https://mags0ft.github.io/spamfilter/installation/) for more information on how to install `spamfilter` and its dependencies, especially if you plan to use API or Ollama functionality.

## Usage

Define a [pipeline](https://mags0ft.github.io/spamfilter/pipelines/) using several spam [filters](https://mags0ft.github.io/spamfilter/filters/) stacked onto each other.

```python
from spamfilter.filters import Length, SpecialChars
from spamfilter.pipelines import Pipeline

# create a new pipeline
m = Pipeline([
    # length of 10 to 200 chars, crop if needed
    Length(min_length=10, max_length=200, mode="crop"),
    # limit use of special characters
    SpecialChars(mode="normal")
])

# test a string against it
TEST_STRING = "This is a test string."
print(m.check(TEST_STRING).passed)
```

Output:

```
True
```

## License

This project is licensed under the MIT License, as declared in the [`LICENSE` file](./LICENSE).

## Contributing

Feel free to contribute to the project using the GitHub repository. Additions to the spam filters, pipelines and documentation are always welcome!

Learn more [here](https://mags0ft.github.io/spamfilter/contributing/) if you're interested in helping out!
