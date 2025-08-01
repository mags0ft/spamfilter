# Installation

In this document, you will learn how to install the `spamfilter` module. There are generally three options to
get started.

---

## 👉 How to install

You may install the module using `pip`, which is the easiest way to do it as `spamfilter` is in the PyPI index.

To achieve this, run

```bash
pip install spamfilter
```

in your terminal. If that doesn't work, for example due to `pip` not being added to your PATH, just try

```bash
python3 -m pip install spamfilter
```

instead.

## Extra dependencies

If you plan to use spamfilter with third-party API calling support, run

```bash
pip install spamfilter[api]
```

If you want to use the Ollama integration, run

```bash
pip install spamfilter[ollama]
```

If you want to take advantage of machine learning text classification using 🤗 Transformers, run

```bash
pip install spamfilter[transformers]
```

If you want to install development dependencies, run

```bash
pip install spamfilter[dev]
```

## Other installation methods

You can also install `spamfilter` without using the Python package index and instead install the source files locally. This can be achieved using this website's [download links](https://github.com/mags0ft/spamfilter/zipball/master) at the very top or the files available at the [GitHub repository](https://github.com/mags0ft/spamfilter).

Place the `.zip` or `.tar.gz`-files into your project folder, unpack them and move the `src` folder into your project root.

**🚩 Note that the manual install using download is not recommended because it's way less optimized, bloated with unnecessary files and hard to do.**
