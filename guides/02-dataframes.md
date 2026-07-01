# 🐼 Guide 2 — pandas and DataFrames

All your stock data lives in a **table**: rows of days, columns of prices. In
Python, the go-to tool for tables is a library called **pandas**, and its table
is called a **DataFrame**. This guide is all about getting comfortable with it.

Keep the notebook open and run each snippet as you read — that's how this clicks.

---

## What is pandas? What is a DataFrame? 📊

**pandas** is a library for working with tables of data. You import it like this
(the nickname `pd` is standard — everyone uses it):

```python
import pandas as pd
```

A **DataFrame** is pandas' word for a table. It has three parts:

- **Rows** — each row is one record. For us, one trading day.
- **Columns** — each column is one kind of value: `Open`, `Close`, `Volume`, …
- **The index** — the label down the left-hand side that names each row. For our
  data, the index is the **date**.

Here's a tiny slice of what a downloaded table looks like:

```
              Open    High     Low   Close     Volume
Date
2024-01-02  185.64  186.95  183.92  185.14   52020000
2024-01-03  184.22  185.88  183.43  184.25   58410000
2024-01-04  182.15  183.09  180.88  181.91   71980000
```

The dates on the left are the **index**. `Open`, `High`, … are the **columns**.
Each line is a **row**.

Let's get a real one to play with:

```python
import yfinance as yf
data = yf.download("AAPL", period="6mo", auto_adjust=True, multi_level_index=False, progress=False)
```

`data` is now a DataFrame with roughly six months of Apple's daily prices. (Guide
3 explains that download line in detail — for now we just want a table to poke
at.)

---

## First look — peeking at a DataFrame 👀

A real table has hundreds of rows, so you rarely print the whole thing. These
five tools show you just enough:

```python
data.head()       # the first 5 rows
data.tail()       # the last 5 rows
data.shape        # (rows, columns), e.g. (126, 5)
data.columns      # the list of column names
data.describe()   # quick stats: count, mean, min, max, ...
```

A couple of notes:

- `data.head()` and `data.tail()` have brackets — they're **functions** that
  return rows. You can ask for a different number: `data.head(10)`.
- `data.shape` and `data.columns` have **no** brackets — they're facts *about*
  the table, not actions. `data.shape` might give `(126, 5)`, meaning 126 days
  and 5 columns.
- `data.describe()` is great for a sanity check: it shows the average `Close`,
  the biggest `Volume`, and so on, all at once.

**Try this 👉** run `data.shape` and read off how many trading days you got.

---

## Selecting one column 🧵

To pull out a single column, put its name in square brackets, in quotes:

```python
data["Close"]
```

That gives you just the closing prices — every day's `Close`, with the dates
still attached. A single column like this is called a **Series** (a DataFrame is
basically several Series side by side).

You'll use `data["Close"]` a *lot* — it's the headline price we care about most.

```python
data["Close"].head()   # first 5 closing prices
data["Volume"].max()   # the busiest day's share volume
data["Close"].mean()   # the average closing price
```

---

## Selecting rows — `.iloc` and `.loc` 🎯

Columns go by name. **Rows** go by either their *position* or their *label*.
There are two tools, and the difference is worth learning once, properly:

### `.iloc` — by position (a number)

`iloc` = "**i**nteger **loc**ation". You give it a row number, counting from 0:

```python
data.iloc[0]    # the very first row (earliest day)
data.iloc[-1]   # the very last row (most recent day)
```

This is exactly like list positions from Guide 1: `0` is first, `-1` is last.

You can combine it with a column to get one single value:

```python
data["Close"].iloc[-1]   # the most recent closing price
data["Close"].iloc[0]    # the closing price on the first day
```

> **In the app:** Stage 3 uses `data["Close"].iloc[-1]` to show today's price and
> `data["Close"].iloc[0]` to work out how much it's changed since the start.

### `.loc` — by label (the index)

`loc` uses the row's **label** — for us, the date:

```python
data.loc["2024-01-02"]   # the row for that exact date
```

Rule of thumb: **`iloc` for "the Nth row", `loc` for "the row named X".**

---

## Doing maths on columns ➗

This is where pandas feels like magic. You can do arithmetic on a whole column at
once, and it applies to every row:

```python
data["High"] - data["Low"]
```

That gives you the day's price **range** (highest minus lowest) for *every* day,
in one line — no loop needed. You can save it as a brand-new column:

```python
data["Range"] = data["High"] - data["Low"]
data["Range"].head()
```

Now the table has an extra `Range` column. A few more you might try:

```python
data["Close"] - data["Open"]          # how much it moved during the day
data["Close"] / data["Open"]          # ratio of close to open
(data["Close"] - data["Open"]) * 100  # scale it up
```

**Try this 👉** make a new column called `Gain` equal to `Close` minus `Open`,
then run `data["Gain"].describe()` to see the typical daily move.

---

## ✅ Check yourself

You're ready for the next guide if you can:

- Say what the **rows**, **columns** and **index** of our DataFrame are.
- Get the first 5 rows, and find out how many rows there are in total.
- Pull out the `Close` column, and get just the *last* closing price.
- Explain when you'd use `.iloc` versus `.loc`.
- Make a new column that's one column minus another.

---

## 📓 Practise now

Work through the second notebook — it walks you through every tool above on real
data, with room to experiment:

**➡️ [`../notebooks/02_pandas_dataframes.ipynb`](../notebooks/02_pandas_dataframes.ipynb)**

Keep the [`../reference/pandas-cheatsheet.md`](../reference/pandas-cheatsheet.md)
handy for quick lookups.

---

**What's next →** [`03-getting-data-yfinance.md`](03-getting-data-yfinance.md) —
where the real numbers come from, and how to download any company you like.
