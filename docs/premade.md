# 🍰 Pre-made machines

There are pre-made collections of usecase-optimized filters built into `spamfilter`. Those are made to fit right into the environment they are made for and don't need additional setup in most cases.

## How to use a pre-made machine

To use a pre-made machine, do the following (this example is using the `chat` machine):

```
from spamfilter.premade import chat

c1 = chat.create_machine(...args)
c2 = chat.chatMachine
```

`c1` is a machine created using `create_machine`, a function that accepts arguments depending on the pre-made machines you chose.

`c2` is a ready-to-use, default-setup machine object that runs immediately.

You can now use the functions of machines you know, such as `check`.

---

⚠ **Warning!** Always extensively test pre-made machines for their accuracy as this might depend on your usecase. You want the least amount of spammy content to pass through them, so you might do some adjustments to the `create_machine` function instead of using the ready-to-go-options right away.

---
## premade.chat
**For chatroom environments.**

Filters built in:
- `Length`,
- `WorldLength`,
- `Symbols`,
- `Capitals`,
- `BypassDetector`,
- `BlocklistFromJSON` (inactive by default)

This machine does already pretty good to block awful spam from your environment. It is also set to be running in `normal-quick` machine mode, meaning it cancels out any additional checks and sanitation as soon as a filter marks the string as failed.

### Using premade.chat
Create a Machine that is pre-made to be used in fast-paced, internet chatting environments.

**If you want to fine-tune your machine with `create_machine`, you are free to adjust these arguments:**

```
from spamfilter.premade import chat

c = chat.create_machine(
    bypass_protection: bool = True,
    length_filter: bool = True,
    min_length: int = 1,
    max_length: int = 200,
    wordlength_filter: bool = True,
    max_word_length: int = 20,
    max_num_too_long_words: int = 1,
    capitals_filter: bool = True,
    capitals_percentage: float = 0.3,
    capitals_mode: str = "crop",
    symbols_filter: bool = True,
    profanity_filter: bool = False,
    profanity_blocklist_filepath: str = ""
)
```

**If you want to use a default, no-setup and maybe less optimized machine, go for:**

```
from spamfilter.premade import chat

c = chat.chatMachine
```

### Using premade.article
Create a Machine that is pre-made to be used in high-quality, demanding writing platforms.

**If you want to fine-tune your machine with `create_machine`, you are free to adjust these arguments:**

```
from spamfilter.premade import article

c = article.create_machine(
    bypass_protection: bool = True,
    length_filter: bool = True,
    min_length: int = 400,
    max_length: int = 300_000,
    wordlength_filter: bool = True,
    max_word_length: int = 50,
    max_num_too_long_words: int = 3,
    capitals_filter: bool = True,
    capitals_percentage: float = 0.4,
    capitals_mode: str = "normal",
    symbols_filter: bool = True,
    profanity_filter: bool = False,
    profanity_blocklist_filepath: str = ""
)
```

**If you want to use a default, no-setup and maybe less optimized machine, go for:**

```
from spamfilter.premade import article

c = chat.articleMachine
```