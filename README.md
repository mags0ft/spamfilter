![Spamfilter Logo](https://raw.githubusercontent.com/mags0ft/spamfilter/master/docs/assets/icon.png)

# spamfilter
The spamfilter module is a lightweight, fast and straightforward way to build your own spam filtering machines in order to keep applications using user-generated content clean.

It's object-oriented and makes a quick, yet concise approach to remove spam easy.

## Installation
You can install spamfilter by cloning the GitHub repository or using pip:

`pip install spamfilter`

## Usage
Define a machine using several spam filters stacked onto each other.

```from spamfilter.filters import Length, Symbols
from spamfilter import Machine

m = Machine([
   Length(min_length=10, max_length=200, mode="crop"),
   Symbols(mode="normal")`\
])

TEST_STRING = "This is a test string."
print(m.check(TEST_STRING).passed)
```

## License
This project is licensed under the MIT License as found in the `LICENSE` file.

## Contributing
Feel free to contribute to the project using the GitHub repository. Additions to the spam filters, machines and documentation are always welcome!