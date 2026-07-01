# 💹 yfinance Cheat-Sheet

`yfinance` downloads real stock data from Yahoo Finance. Scan for what you need.

```python
import yfinance as yf
```

---

## Download price history

**Use this exact form to fetch one ticker** — it gives you plain, easy columns:

```python
data = yf.download(ticker, period=period, auto_adjust=True,
                   multi_level_index=False, progress=False)
```

| Option | What it does |
| ------ | ------------ |
| `auto_adjust=True` | prices already adjusted for splits/dividends (the numbers you want) |
| `multi_level_index=False` | flattens the columns to plain `Open/High/Low/Close/Volume`, so `data["Close"]` is a single column (a Series) |
| `progress=False` | hides the download progress bar (tidier in a web app) |

You get back a pandas **DataFrame**: one row per trading day, the date as the
row label, and the columns below. Change the period or add an interval the same
way:

```python
data = yf.download("AAPL", period="1y", interval="1wk",
                   auto_adjust=True, multi_level_index=False, progress=False)
```

> ⚠️ Without `multi_level_index=False`, yfinance gives you **MultiIndex**
> columns like `('Close', 'AAPL')`, which makes `data["Close"]` return a whole
> DataFrame instead of a single column — that breaks filtering and charts. See
> "Column shape" at the bottom.

---

## What each column means

| Column | Meaning |
| ------ | ------- |
| `Open` | price when the market opened that day |
| `High` | highest price during the day |
| `Low` | lowest price during the day |
| `Close` | price when the market closed (the "headline" price) |
| `Volume` | how many shares changed hands that day |

The **date** is the row label (the index), not a column. Get closes with
`data["Close"]`.

---

## `period` — how far back to go

| Value | Meaning |
| ----- | ------- |
| `1d` | 1 day |
| `5d` | 5 days |
| `1mo` | 1 month |
| `3mo` | 3 months |
| `6mo` | 6 months |
| `1y` | 1 year |
| `2y` | 2 years |
| `5y` | 5 years |
| `10y` | 10 years |
| `ytd` | since Jan 1st this year |
| `max` | everything available |

---

## `interval` — the size of each row

| Value | Meaning | Note |
| ----- | ------- | ---- |
| `1d` | one row per day | the usual choice |
| `1wk` | one row per week | |
| `1mo` | one row per month | |
| `1m` | one row per minute | intraday |
| `5m` | one row per 5 minutes | intraday |
| `60m` | one row per hour | intraday |

> ⚠️ **Intraday intervals** (`1m`, `5m`, `60m`) only work for a short, recent
> window — roughly the last few days for `1m`, the last couple of months for
> `60m`. Ask for `1m` over `5y` and you get nothing back. Use `1d` unless you
> specifically need intraday.

---

## The `Ticker` object — more than just prices

```python
apple = yf.Ticker("AAPL")

apple.info                    # dict of company facts (name, sector, market cap…)
apple.info["longName"]        # "Apple Inc."
apple.history(period="6mo")   # same shape of price table as yf.download
```

`yf.download(...)` is the quick way to get a price table; `yf.Ticker(...)` is
handy when you also want company details.

---

## Example tickers

| Ticker | Company |
| ------ | ------- |
| `AAPL` | Apple |
| `MSFT` | Microsoft |
| `GOOGL` | Alphabet (Google) |
| `TSLA` | Tesla |
| `AMZN` | Amazon |
| `NVDA` | Nvidia |

**Non-US markets** use a suffix after a dot:

| Ticker | Market |
| ------ | ------ |
| `VOD.L` | Vodafone, London |
| `BMW.DE` | BMW, Germany (Xetra) |
| `AIR.PA` | Airbus, Paris |
| `7203.T` | Toyota, Tokyo |

---

## Good to know

- The data comes **from the internet**, so you need a connection. It can
  occasionally be slow, or come back **empty** if Yahoo is busy or the ticker is
  wrong.
- Always check before using it:

  ```python
  data = yf.download("AAPL", period="6mo", auto_adjust=True,
                     multi_level_index=False, progress=False)
  if data.empty:
      print("No data — check the ticker and your connection.")
  ```

- A wrong/unknown ticker usually returns an **empty** table rather than an
  error, so a spelling mistake looks like "no data".

---

## Column shape: one ticker vs many

Start simple with **one company**; you meet multi-level columns later, when you
compare **several**.

**One ticker** (with `multi_level_index=False`) → flat columns:

```python
data = yf.download("AAPL", period="6mo", auto_adjust=True,
                   multi_level_index=False, progress=False)
data["Close"]                 # a Series — the close prices
```

**Many tickers** → **MultiIndex** columns like `('Close', 'AAPL')`:

```python
data = yf.download(["AAPL", "MSFT"], period="6mo", auto_adjust=True)
data["Close"]                 # a DataFrame — closes for BOTH companies
data["Close"]["AAPL"]         # a Series — just Apple's closes
```

| You downloaded | `data["Close"]` gives | One company's closes |
| -------------- | --------------------- | -------------------- |
| one ticker, `multi_level_index=False` | a Series | `data["Close"]` |
| many tickers | a DataFrame | `data["Close"]["AAPL"]` |
