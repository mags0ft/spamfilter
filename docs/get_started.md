# Getting started

You can easily get started with `spamfilter` as it's quick to pick up and easy to understand.

🔥 **First of all, you should install the module by following [these steps](./installation.md).**

You can then validate if the install was successful by running the Python console and typing:

```python
>>> import spamfilter
>>> spamfilter.__version__
'v2.0.1'
>>> 
```

You may also try to play around with the built-in, premade pipelines to test how good `spamfilter` keeps user-generated content clean. Create a new file and paste the following code:

```python
from spamfilter.premade import chat

c = chat.create_pipeline()

INPUT_STRING = "This is a test string."
print(c.check(INPUT_STRING).passed)
```

By running the file, you see how the pre-made model assessed the input string. `True` corresponds for the string to have **passed** and therefore not being spam according to the model. `False` corresponds for the string to have **failed** the filter and being spam.

**Awesome!** You're all set. See the [documentation](./documentation.md) to continue.
