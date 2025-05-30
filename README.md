<p align="center">
    <img src="docs/assets/icon-white-box.png" alt="Spamfilter logo" width=350>
</p>

# spamfilter

<p align="center">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/spamfilter?style=for-the-badge&logo=pypi&labelColor=%231e1e1e" />
    <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/mags0ft/spamfilter/python-package.yml?style=for-the-badge&logo=python&labelColor=%231e1e1e" />
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/spamfilter?style=for-the-badge&labelColor=%231e1e1e" />
</p>

The spamfilter module is a lightweight, fast and straightforward Python package that helps you to build your own spam filtering pipelines in order to keep  your applications featuring user-generated content clean.

It's object-oriented and makes a quick, concise approach to remove spam easy.

---

**Important links**
- [🌎 GitHub page](https://mags0ft.github.io/spamfilter/)
- [🔓 Report a security vulnerability](https://github.com/mags0ft/spamfilter/security/advisories/new)
- [🚩 Create a new issue](https://github.com/mags0ft/spamfilter/issues/new/choose)
- [👩‍💻 How to contribute](./docs/contributing.md)

## Installation
You can install spamfilter by cloning the GitHub repository, downloading it from the GitHub page or using pip:

```bash
pip install spamfilter
```

## Usage
Define a pipeline using several spam filters stacked onto each other.

```python
from spamfilter.filters import Length, Symbols
from spamfilter.pipelines import Pipeline

m = Pipeline([
    Length(min_length=10, max_length=200, mode="crop"),
    Symbols(mode="normal")
])

TEST_STRING = "This is a test string."
print(m.check(TEST_STRING).passed)
```

Output:

```
True
```

## License
This project is licensed under the MIT License as found in the `LICENSE` file.

## Contributing
Feel free to contribute to the project using the GitHub repository. Additions to the spam filters, pipelines and documentation are always welcome!
