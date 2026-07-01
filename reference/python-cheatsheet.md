# 🐍 Python Cheat-Sheet

Quick syntax reminders. Scan for the heading you need. For the slow, friendly
version see `guides/`.

---

## Variables & types

```python
name = "Apple"      # str  — text
price = 187.2       # float — number with a decimal
shares = 100        # int  — whole number
is_up = True        # bool — True or False
nothing = None      # "no value yet"
```

| Check the type | Convert |
| ------ | ------- |
| `type(price)` → `float` | `int("100")` → `100` |
| | `float("187.2")` → `187.2` |
| | `str(100)` → `"100"` |

Rules: no spaces in names (`close_price`, not `close price`); names are
case-sensitive (`Price` ≠ `price`).

---

## Strings

```python
ticker = "aapl"
```

| Do this | Result |
| ------- | ------ |
| `ticker.upper()` | `"AAPL"` |
| `ticker.lower()` | `"aapl"` |
| `"  hi  ".strip()` | `"hi"` (trims spaces) |
| `"AAPL,MSFT".split(",")` | `["AAPL", "MSFT"]` |
| `"-".join(["a", "b"])` | `"a-b"` |
| `ticker.replace("a", "x")` | `"xxpl"` |
| `len(ticker)` | `4` |
| `"AA" in "AAPL"` | `True` |
| `ticker[0]` | `"a"` (first letter) |

**f-strings** — drop a value straight into text with `f"...{value}..."`:

```python
price = 187.2
print(f"Close was {price}")          # Close was 187.2
print(f"Close was {price:.2f}")      # Close was 187.20  (2 decimals)
print(f"Up {0.0512:.1%}")            # Up 5.1%           (percent)
```

---

## Numbers & math

| Operator | Meaning | Example |
| -------- | ------- | ------- |
| `+ - * /` | add, subtract, multiply, divide | `10 / 4` → `2.5` |
| `//` | divide, drop the remainder | `10 // 4` → `2` |
| `%` | remainder | `10 % 4` → `2` |
| `**` | power | `2 ** 3` → `8` |

```python
round(187.256, 2)   # 187.26
abs(-5)             # 5
max(3, 9, 1)        # 9
min(3, 9, 1)        # 1
```

---

## Lists — an ordered collection

```python
tickers = ["AAPL", "MSFT", "GOOGL"]
```

| Do this | Result |
| ------- | ------ |
| `tickers[0]` | `"AAPL"` (first) |
| `tickers[-1]` | `"GOOGL"` (last) |
| `tickers[0:2]` | `["AAPL", "MSFT"]` (slice, stop is excluded) |
| `tickers.append("TSLA")` | adds to the end |
| `len(tickers)` | `3` |
| `"MSFT" in tickers` | `True` |

Loop over a list:

```python
for t in tickers:
    print(t)
```

---

## Dictionaries — labelled values (key → value)

```python
stock = {"ticker": "AAPL", "price": 187.2}
```

| Do this | Result |
| ------- | ------ |
| `stock["ticker"]` | `"AAPL"` |
| `stock["price"] = 190` | change / add a value |
| `stock.keys()` | all keys |
| `stock.values()` | all values |
| `"price" in stock` | `True` |

Loop over a dict:

```python
for key, value in stock.items():
    print(key, value)
```

---

## Booleans & comparisons

| Operator | Means | Example |
| -------- | ----- | ------- |
| `==` | equal to | `price == 100` |
| `!=` | not equal | `price != 100` |
| `>` `<` | greater / less | `price > 100` |
| `>=` `<=` | greater-or-equal / less-or-equal | `price >= 100` |

Combine conditions with `and`, `or`, `not`:

```python
price > 100 and price < 200     # both must be true
price < 50 or price > 500       # either one
not is_up                       # flips True/False
```

> ⚠️ Plain Python uses `and` / `or`. **pandas** filtering uses `&` / `|` instead
> — see the pandas cheat-sheet.

---

## `if` / `elif` / `else`

```python
if price > 200:
    print("expensive")
elif price > 100:
    print("mid")
else:
    print("cheap")
```

The `:` and the indent (4 spaces) matter — Python uses them to group code.

---

## `for` loops

```python
for t in ["AAPL", "MSFT"]:      # each item in a list
    print(t)

for i in range(3):              # 0, 1, 2
    print(i)

for i in range(1, 4):           # 1, 2, 3  (stop is excluded)
    print(i)
```

---

## Functions — name a block of code

```python
def greet(name):            # define it
    return f"Hi {name}"

message = greet("Sam")      # call it → "Hi Sam"
```

```python
def add(a, b=10):           # b has a default of 10
    return a + b

add(5)          # 15
add(5, 1)       # 6
```

---

## `import` — use code from a library

```python
import pandas as pd         # "as pd" gives it a short nickname
import yfinance as yf
import streamlit as st

from datetime import date   # grab one thing from a library
```

---

## Printing (for checking things while you code)

```python
print("hello")
print("price is", price)         # print several things
print(f"price is {price}")       # f-string is usually tidier
```

> 💡 In Jupyter notebooks, just putting a variable on the last line of a cell
> shows it — you don't always need `print`.
