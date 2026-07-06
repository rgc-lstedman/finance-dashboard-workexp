# 🐍 Guide 1 — Python basics

This guide teaches you just enough Python to build the screener. We'll keep
every example tied to something you'll actually use — tickers, prices, days.

You don't need to write any of this into `app.py` yet. The best way to learn is
to **type these snippets into the matching notebook and run them** (more on that
at the end). Watching a line run and seeing what comes out is worth ten pages of
reading.

Let's go. 🚀

---

## What *is* Python?

Python is a programming language — a way of writing instructions a computer can
follow. It's popular because it reads almost like English. Here's a whole
program:

```python
print("Hello!")
```

Run that and the computer prints the word `Hello!`. That's it. `print(...)` just
means "show this on screen". We'll use it constantly to peek at what our code is
doing.

> 💡 The `#` symbol starts a **comment** — a note for humans that Python ignores.
> Use comments to remind yourself what a line does.
>
> ```python
> price = 187.25   # today's closing price for AAPL
> ```

---

## Variables — giving a value a name 🏷️

A **variable** is a name that holds a value, so you can use it again later. You
make one with `=` ("put the thing on the right into the name on the left").

```python
ticker = "AAPL"
price = 187.25
shares = 10
```

Now `ticker` means `"AAPL"`, `price` means `187.25`, and so on. You can use them:

```python
print(ticker)   # AAPL
print(price)    # 187.25
```

And you can do maths with them:

```python
total_value = price * shares
print(total_value)   # 1872.5
```

> **In the app:** your screener will store the whole table of companies in a
> variable called `data`, and the one ticker the user clicks into in a variable
> called `choice`.

**Try this 👉** make a variable `company = "MSFT"` and print it.

---

## The basic types of value 🔢🔤

Every value has a **type**. You'll meet four right away:

| Type | Means | Example | Notes |
| ---- | ----- | ------- | ----- |
| `int` | Whole number | `shares = 10` | No decimal point |
| `float` | Number with decimals | `price = 187.25` | Prices are floats |
| `str` | Text ("string") | `ticker = "AAPL"` | Always in quotes |
| `bool` | True or False | `is_up = True` | Note the capital letters |

You can ask Python for the type of anything:

```python
print(type(price))    # <class 'float'>
print(type(ticker))   # <class 'str'>
print(type(True))     # <class 'bool'>
```

The quotes matter: `"10"` is text, but `10` is a number. `"10" + "5"` gives the
text `"105"`, while `10 + 5` gives the number `15`. Mixing them up is a common
early mistake — and a very normal one.

---

## Lists — many values in a row 📋

A **list** holds several values in order, inside square brackets `[ ]`:

```python
tickers = ["AAPL", "MSFT", "TSLA", "GOOGL"]
```

You reach into a list by **position**, counting **from 0**:

```python
print(tickers[0])   # AAPL   (the first one)
print(tickers[1])   # MSFT
print(tickers[-1])  # GOOGL  (-1 means the last one)
```

Useful things you can do with a list:

```python
len(tickers)            # 4  — how many items
tickers.append("NVDA")  # add "NVDA" to the end
```

> **In the app:** the period dropdown is really just a list of choices —
> `["1mo", "6mo", "1y", "5y"]`. The user picks one.

**Try this 👉** make a list of three companies you've heard of and print the
first and last.

---

## Dictionaries — labelled values 🗂️

A **dictionary** stores values under **labels** (called "keys") instead of
positions. You use curly braces `{ }`, with `key: value` pairs:

```python
company = {
    "ticker": "AAPL",
    "name": "Apple",
    "sector": "Technology",
}
```

Look things up by their key:

```python
print(company["name"])     # Apple
print(company["ticker"])   # AAPL
```

Think of a list as a numbered row, and a dictionary as a labelled form. Both are
everywhere in Python.

---

## Functions — a reusable recipe 🍳

A **function** is a named block of instructions you can run whenever you like.
You **define** it with `def`, and you **call** it by writing its name with
brackets.

```python
def profit(buy_price, sell_price):
    return sell_price - buy_price
```

- `profit` is the name.
- `buy_price` and `sell_price` are **parameters** — the inputs it expects.
- `return` hands a result back to you.

Now call it with real numbers:

```python
print(profit(180, 187.25))   # 7.25
```

You've already been using functions: `print(...)` and `len(...)` are functions
that come with Python. Soon you'll call ones from libraries, like
`yf.download(...)`.

> ⚠️ **Indentation matters in Python.** The lines *inside* a function (or an
> `if`, or a `for`) must be indented — usually four spaces. It's not decoration;
> it's how Python knows what belongs together.

---

## Making decisions — `if` / `else` 🔀

`if` runs some code **only when** a condition is true. `else` covers the other
case.

```python
price = 187.25

if price > 150:
    print("That's a pricey share.")
else:
    print("Fairly cheap.")
```

The condition (`price > 150`) is a question with a yes/no answer — it produces a
`bool`, `True` or `False`. Comparisons you'll use a lot:

| You write | Means |
| --------- | ----- |
| `a > b` | a greater than b |
| `a < b` | a less than b |
| `a >= b` | a greater than or equal to b |
| `a == b` | a **equal to** b (note: two equals signs!) |
| `a != b` | a **not** equal to b |

> ⚠️ `=` sets a variable; `==` **compares** two things. `price = 150` changes
> `price`; `price == 150` asks "is price 150?". Getting these two mixed up is a
> rite of passage.

**In the app** this exact idea appears already — the skeleton checks
`if data.empty:` to show a friendly message when a ticker has no data.

---

## Repeating things — `for` loops 🔁

A `for` loop runs the same code once for each item in a list:

```python
for ticker in ["AAPL", "MSFT", "TSLA"]:
    print("Checking", ticker)
```

That prints three lines, one per company. The variable `ticker` takes each value
in turn. Loops save you from copy-pasting the same line over and over.

**Try this 👉** loop over your list of companies and print each one with the word
`"Buy"` in front of it.

---

## Using someone else's code — `import` 📦

You almost never build everything yourself. A **library** is a bundle of ready-made
code someone else wrote. You bring one in with `import`:

```python
import pandas as pd
import yfinance as yf
```

The `as pd` part gives the library a short nickname so you type less. After
importing, you use the library's tools through that nickname:

```python
data = yf.download("AAPL", period="6mo", auto_adjust=True, multi_level_index=False, progress=False)
```

Here `yf` is yfinance, and `download` is one of its functions. Those two import
lines are already at the top of your `app.py`. You'll meet `pandas` properly in
the next guide.

---

## ✅ Check yourself

You've got the basics if you can explain, in your own words:

- The difference between an `int`, a `float`, a `str` and a `bool`.
- What `tickers[0]` gives you, and why it's not the second item.
- The difference between `=` and `==`.
- What `import yfinance as yf` lets you do afterwards.

Don't worry if it's not all solid yet — you'll use every one of these again and
again, and it sticks through use.

---

## 📓 Practise now

Open the first notebook and run through it, changing values as you go:

**➡️ [`../notebooks/01_python_basics.ipynb`](../notebooks/01_python_basics.ipynb)**

Start it with `uv run jupyter lab` (see [`../docs/SETUP.md`](../docs/SETUP.md) if you need
a reminder), then double-click the notebook in the file list on the left.

Quick lookups live in the
[`../reference/python-cheatsheet.md`](../reference/python-cheatsheet.md).

---

**What's next →** [`02-dataframes.md`](02-dataframes.md) — meet pandas and the
DataFrame, the table that holds all your stock data.
