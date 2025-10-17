# 👩‍💻 Contributing

No matter whether you're an active contibutor at `spamfilter` or just browsing around, we're happy to see everyone engage and could really use some help!

- **Do you have ideas for new features?** [Go here!](https://github.com/mags0ft/spamfilter/issues/new?template=feature_request.md)
- **Found any bugs?** [Go here!](https://github.com/mags0ft/spamfilter/issues/new?template=bug_report.md)
- **Do you want to disclose a security vulnerability?** [Click here.](https://github.com/mags0ft/spamfilter/security/advisories/new)
- **Write your own code for the library?** Feel free to do so and please continue to read to the next section!

## Contribute own code

You're always welcome to build new features, filters and options into the `spamfilter` library! We love to see what you got to contribute to the library.

To get started, please first make sure you have a working git, Python 3.9+ and pip installation. You can set up a dev environment like so:

```bash
git clone https://github.com/mags0ft/spamfilter.git
cd spamfilter
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate
pip install -e .[dev]
```

That's it! You can now start coding. One last tip: Please consider adding test cases to your code if it's reasonable to do so. It really does make a difference!

## Submitting code

After you've made your desired changes - and if wish to get them merged - please follow these few rules of thumb:

- **run `pytest`** and **`pylint $(git ls-files *.py)`** once you like to publish your changes.
- **create a custom fork** to push your changes to, then [create a pull request](https://github.com/mags0ft/spamfilter/pulls) on GitHub!
- **get your code reviewed** to ensure your code is alright, fast and great to use for the users of `spamfilter`!
