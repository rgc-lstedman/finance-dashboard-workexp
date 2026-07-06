# 📥 Guide 3 — Getting real data with yfinance

So far the tables have appeared by magic. Now you'll learn to summon them
yourself. **yfinance** is a library that downloads real stock-market data from
Yahoo Finance — for free, over the internet. One line of code and you have months
of real prices to work with. 🌍

---

## What's a ticker symbol? 🏷️

Every company on the stock market has a short code called a **ticker symbol**.
It's how you ask for one specific company. A few you'll recognise:

| Ticker | Company |
| ------ | ------- |
| `AAPL` | Apple |
| `MSFT` | Microsoft |
| `TSLA` | Tesla |
| `GOOGL` | Alphabet (Google) |
| `AMZN` | Amazon |
| `NVDA` | Nvidia |

Tickers are usually uppercase letters. When you type one, spelling counts —
`APPL` (a common typo) is not Apple, and you'll get an empty table.

---

## Downloading data 📡

First, import the library (this is already at the top of your `app.py`):

```python
import yfinance as yf
```

Then download a company's price history. This is the exact line we'll use every
time — copy it as-is:

```python
data = yf.download("AAPL", period="6mo", auto_adjust=True, multi_level_index=False, progress=False)
```

Reading it out loud: "use yfinance's `download` function to fetch six months of
AAPL, and put the resulting table into a variable called `data`." The important
parts:

- `"AAPL"` — **which** company (the ticker).
- `period="6mo"` — **how much history** you want (here, 6 months).

The last three are settings that keep things tidy — set them once and forget
them:

- `auto_adjust=True` — gives you clean, adjusted prices and a single `Close`
  column (the number everyone quotes).
- `multi_level_index=False` — keeps the column names plain (`Open`, `Close`, …),
  so `data["Close"]` is one simple column of numbers.
- `progress=False` — hides the little download bar so your output stays clean.

What comes back is a pandas **DataFrame** — exactly the kind of table you met in
Guide 2. One row per trading day.

> 💡 Downloading needs an internet connection, and can take a second or two. If
> you get a network error, check you're online.

---

## Choosing how much history — `period` 🗓️

The `period` setting controls how far back you go. Use one of these text values:

| `period` | You get |
| -------- | ------- |
| `"1mo"` | The last month |
| `"3mo"` | The last 3 months |
| `"6mo"` | The last 6 months |
| `"1y"` | The last year |
| `"2y"` | The last 2 years |
| `"5y"` | The last 5 years |
| `"ytd"` | This year so far ("year to date") |
| `"max"` | Everything Yahoo has |

```python
year = yf.download("MSFT", period="1y", auto_adjust=True, multi_level_index=False, progress=False)
long_history = yf.download("MSFT", period="5y", auto_adjust=True, multi_level_index=False, progress=False)
```

> **In the app:** Stage 2 lets the user pick the period from a dropdown offering
> `1mo`, `6mo`, `1y`, `5y` — these are just the values from the table above.

---

## Choosing the spacing — `interval` ⏱️

By default you get **one row per day**. The `interval` setting changes the
spacing — for example, one row per week:

```python
weekly = yf.download("AAPL", period="1y", interval="1wk", auto_adjust=True, multi_level_index=False, progress=False)
```

Common intervals:

| `interval` | One row per |
| ---------- | ----------- |
| `"1d"` | Day (the default) |
| `"1wk"` | Week |
| `"1mo"` | Month |

> 💡 There are finer intervals like `"1h"` (hourly), but Yahoo only keeps those
> for short recent periods — pairing `"1h"` with `"5y"` won't work. For this
> project, daily data (`"1d"`) is perfect. You can leave `interval` out entirely.

---

## What the columns mean 📖

Every row (one trading day) has these columns. In plain English:

| Column | What it means |
| ------ | ------------- |
| `Open` | The price at the moment the market **opened** that morning |
| `High` | The **highest** price reached at any point during the day |
| `Low` | The **lowest** price during the day |
| `Close` | The price when the market **closed** — the "headline" price everyone quotes |
| `Volume` | How many **shares changed hands** that day (a measure of how busy it was) |

We care most about `Close`. When the news says "Apple finished up today", they
mean its `Close` was higher than yesterday's.

---

## Peeking at what you got 👀

Always take a quick look after downloading, so you know it worked:

```python
data = yf.download("AAPL", period="6mo", auto_adjust=True, multi_level_index=False, progress=False)
data.head()      # first few rows — sanity check
data.shape       # how many days did we get?
data.columns     # what are the columns called?
```

If `data.head()` shows dates and price columns, you're golden. If it's empty, the
ticker was probably misspelled.

> 💡 Because we asked for `multi_level_index=False`, `data.columns` shows nice
> plain names — `Open`, `High`, `Low`, `Close`, `Volume`. That's exactly what you
> want, so `data["Close"]` gives you one clean column to work with. (When you
> download *several* companies at once, the columns get an extra layer — but
> that's a later trick, saved for a stretch goal in Guide 5.)

**Try this 👉** download `TSLA` for `1y`, then run `data["Close"].max()` to find
its highest closing price over the year.

---

## Saving data to a file 💾

Downloading every time is a bit wasteful, and you can't use the internet forever.
You can save a table to a **CSV file** (a simple spreadsheet-style file) and
reopen it later:

```python
data.to_csv("data/aapl.csv")
```

That writes the table into the project's `data/` folder (which already exists for
exactly this). To read it back another time:

```python
import pandas as pd
saved = pd.read_csv("data/aapl.csv", index_col=0, parse_dates=True)
```

The extra bits — `index_col=0` and `parse_dates=True` — tell pandas "the first
column is the date index, and please treat it as real dates." Without them the
dates come back as plain text.

> 💡 CSV stands for "comma-separated values". If you open `data/aapl.csv` in a
> text editor you'll see the numbers separated by commas — that's all it is.

---

## ✅ Check yourself

You've got this if you can:

- Explain what a ticker symbol is and give three examples.
- Download 1 year of Microsoft data into a variable.
- Say what `Open`, `Close` and `Volume` mean without looking.
- Check whether a download worked using `.head()` or `.shape`.
- Save a table to `data/something.csv`.

---

## 📓 Practise now

The third notebook lets you download several companies and explore the real data
hands-on:

**➡️ [`../notebooks/03_yfinance_data.ipynb`](../notebooks/03_yfinance_data.ipynb)**

Quick lookups are in the
[`../reference/yfinance-cheatsheet.md`](../reference/yfinance-cheatsheet.md).

This is also enough to tackle **Stage 1** of the [`../docs/SPEC.md`](../docs/SPEC.md) — go
and make the starter app show a table for a company you choose. 📈

---

**What's next →** [`04-filtering-searching.md`](04-filtering-searching.md) — the
core skill of the whole project: asking your data questions and keeping only the
rows that answer them.
