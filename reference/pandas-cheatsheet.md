# 🐼 pandas Cheat-Sheet

`pandas` is the library for working with tables of data. Scan for what you need.
Examples assume `data` is the price table from `yfinance` (columns `Open`,
`High`, `Low`, `Close`, `Volume`; the date is the row label).

```python
import pandas as pd
```

---

## The two building blocks

| Thing | What it is |
| ----- | ---------- |
| **DataFrame** | the whole table (rows and columns) — `data` |
| **Series** | one single column on its own — `data["Close"]` |

---

## Inspect the table

| Do this | What you get |
| ------- | ------------ |
| `data.head()` | first 5 rows |
| `data.head(10)` | first 10 rows |
| `data.tail()` | last 5 rows |
| `data.shape` | `(rows, columns)`, e.g. `(126, 5)` |
| `data.columns` | the column names |
| `data.dtypes` | the type of each column |
| `data.info()` | columns, types, how many values |
| `data.describe()` | count / mean / min / max per column |

---

## Select columns

```python
data["Close"]                 # one column  → a Series
data[["Open", "Close"]]       # several columns → a smaller DataFrame
```

> ⚠️ Several columns need **double brackets** — you pass a *list* of names.

---

## Select rows — `.iloc` vs `.loc`

| Tool | Selects by | Example |
| ---- | ---------- | ------- |
| `.iloc` | **position** (0, 1, 2, …) | `data.iloc[0]` → first row |
| `.iloc` | | `data.iloc[-1]` → last row |
| `.iloc` | | `data.iloc[0:5]` → first 5 rows |
| `.loc` | **label** (the row's name) | `data.loc["2024-01-02"]` |

Grab a single value from a column:

```python
data["Close"].iloc[-1]        # the most recent close
data["Close"].iloc[0]         # the first close in the period
```

---

## Filtering with boolean masks ⭐ (the main skill)

A **mask** is a column of `True`/`False`. Put it in `data[...]` to keep only the
`True` rows.

```python
data["Close"] > data["Open"]          # the mask (True/False per row)
data[data["Close"] > data["Open"]]    # keep only the "up" days
```

**Combine conditions** — `&` (and), `|` (or). Wrap **each** condition in brackets:

```python
data[(data["Close"] > 150) & (data["Volume"] > 50_000_000)]   # both
data[(data["Close"] > 200) | (data["Close"] < 100)]           # either
```

**Other handy filters:**

```python
data[data.index >= "2024-03-01"]              # rows on/after a date
data["Volume"].between(40_000_000, 60_000_000)  # mask: within a range
tickers = pd.Series(["AAPL", "MSFT"])
tickers.isin(["MSFT"])                         # mask: value is in a list
```

---

## Sort

```python
data.sort_values("Close")                       # low → high
data.sort_values("Close", ascending=False)      # high → low
data.sort_values("Volume", ascending=False).head(5)   # 5 busiest days
```

---

## Simple aggregations (one number from a column)

```python
data["Close"].mean()      # average
data["Close"].max()       # highest
data["Close"].min()       # lowest
data["Volume"].sum()      # total
data["Close"].idxmax()    # the DATE of the highest close
data["Close"].idxmin()    # the DATE of the lowest close
```

> `max` gives you the *value*; `idxmax` gives you the *row label* (here, the
> date) where that value happened.

---

## Make a new column from old ones

```python
data["Range"] = data["High"] - data["Low"]        # daily high-low spread
data["Change"] = data["Close"] - data["Open"]     # up or down on the day
```

---

## Rolling / moving average (a smoothed line)

```python
data["Close"].rolling(20).mean()          # 20-day moving average
data["MA20"] = data["Close"].rolling(20).mean()   # save it as a column
```

The first 19 values are blank (`NaN`) — there aren't 20 days to average yet.

---

## Read / write CSV files

```python
data.to_csv("data/prices.csv")            # save the table to a file
old = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
```

`index_col=0` uses the first column (the date) as the row label;
`parse_dates=True` reads it as real dates rather than text.

---

## Common gotchas

| Trap | Fix |
| ---- | --- |
| `data["A", "B"]` errors | use double brackets: `data[["A", "B"]]` |
| `data[cond1 and cond2]` errors | use `&` and bracket each: `data[(cond1) & (cond2)]` |
| Forgot the brackets: `data[a & b]` gives wrong rows | `data[(a) & (b)]` |
| `.iloc` vs `.loc` mixed up | `.iloc` = position number, `.loc` = the label/date |
| `SettingWithCopyWarning` | you filtered then edited a copy — make the new column on `data` first, filter after |
