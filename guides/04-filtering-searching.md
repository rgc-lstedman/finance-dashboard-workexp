# 🔍 Guide 4 — Filtering and searching (the core skill)

This is the big one. If you take one thing from the whole project, take this.

**Filtering** means: out of a big table, keep only the rows you care about.
"Show me only the days the price went up." "Only the really busy days." "Only
this year." Almost every question you'll ever ask of data is a filter.

It looks a bit strange the first time. We'll build it up slowly, from the ground.
Follow along in the notebook. 🧩

We'll use a downloaded table throughout:

```python
import yfinance as yf
data = yf.download("AAPL", period="6mo", auto_adjust=True, multi_level_index=False, progress=False)
```

---

## Step 1 — a comparison makes True/False ✅❌

Start with something small. Ask a question of a whole column at once:

```python
data["Close"] > 100
```

You don't get back prices. You get back a column of **True** and **False** — one
answer per day:

```
Date
2024-01-02     True
2024-01-03     True
2024-01-04    False
2024-01-05    False
...
```

Read it as: for each day, "is the close above 100?" `True` where yes, `False`
where no. This column of yes/no answers has a name: a **boolean mask** (boolean
just means True/False). It's the heart of everything that follows.

The comparisons you can ask:

| You write | Question it asks |
| --------- | ---------------- |
| `data["Close"] > 100` | Is the close **above** 100? |
| `data["Close"] < 100` | Is the close **below** 100? |
| `data["Close"] >= 100` | Above **or equal to** 100? |
| `data["Close"] == 100` | **Exactly** 100? (two equals signs) |
| `data["Volume"] > 50_000_000` | More than 50 million shares? |

> 💡 You can put underscores in big numbers to read them more easily:
> `50_000_000` is the same as `50000000`. Python ignores the underscores.

---

## Step 2 — use the mask to keep rows 🎣

Here's the magic move. Put that True/False column **inside `data[ ... ]`**, and
pandas keeps only the rows where the answer was `True`:

```python
data[data["Close"] > 100]
```

That returns a smaller table — only the days where the close was above 100. The
`False` days are dropped.

It can help to do it in two steps the first few times:

```python
mask = data["Close"] > 100   # the True/False column
data[mask]                   # keep the True rows
```

Both do exactly the same thing. Once it feels natural, you'll write it as the
one-liner above.

> **The whole idea in one sentence:** a comparison gives you a column of
> True/False; wrapping it in `data[...]` keeps the True rows. That's filtering.

**Try this 👉** show only the days where `Volume` was above 60 million:
`data[data["Volume"] > 60_000_000]`.

---

## A finance favourite — "up days" 📈

You don't have to compare against a fixed number. You can compare **one column
against another**. A day is an "up day" if it closed higher than it opened:

```python
data[data["Close"] > data["Open"]]
```

Same pattern exactly — `data["Close"] > data["Open"]` is still just a column of
True/False, one per day. This one line answers "which days did the price rise?"

The opposite, "down days":

```python
data[data["Close"] < data["Open"]]
```

> **In the app:** your screener leans on this exact move — a boolean mask — to
> filter its table of companies down to the interesting ones. You'll see it on a
> real screener table at the end of this guide.

---

## Combining conditions — `&` and `|` 🔗

Real questions often have two parts: "up days **that were also** busy". You
combine masks with:

- `&` means **and** — both must be true.
- `|` means **or** — either can be true.

Up days that were also high-volume:

```python
data[(data["Close"] > data["Open"]) & (data["Volume"] > 50_000_000)]
```

Look closely — **each condition is wrapped in its own brackets** `( )`. This is
not optional:

```python
# ✅ correct — brackets around each part
data[(data["Close"] > data["Open"]) & (data["Volume"] > 50_000_000)]

# ❌ wrong — no brackets, gives a confusing error
data[data["Close"] > data["Open"] & data["Volume"] > 50_000_000]
```

> ⚠️ **Two easy traps here:**
> 1. Use `&` and `|`, **not** the words `and` / `or`, when filtering a DataFrame.
> 2. Wrap **each** condition in brackets. If you get a weird error mentioning
>    "ambiguous" or "truth value", a missing bracket is almost always why.

The `|` (or) version — days that were *either* very cheap *or* very busy:

```python
data[(data["Close"] < 90) | (data["Volume"] > 80_000_000)]
```

**Try this 👉** keep only down days that were also high-volume (a busy sell-off).

---

## Sorting — putting rows in order 🔢

Filtering keeps rows; **sorting** reorders them. Use `sort_values` with the
column to sort by:

```python
data.sort_values("Volume")                    # quietest days first
data.sort_values("Volume", ascending=False)   # busiest days first
```

`ascending=False` means "largest at the top". Combine it with `.head()` to get a
top-10:

```python
data.sort_values("Volume", ascending=False).head(10)   # 10 busiest days
```

That reads left-to-right like a sentence: sort by volume, biggest first, then
show the top 10.

---

## Finding the single best/worst day 🏆

Sometimes you don't want a whole sorted table — just *the* one record. Two neat
tools:

- `.idxmax()` — the **index label** (the date) where a column is **highest**.
- `.idxmin()` — the date where it's **lowest**.

```python
data["Close"].idxmax()   # the date of the highest close
data["Close"].idxmin()   # the date of the lowest close
```

That gives you the date. To see the **whole row** for that day, feed the date
back in with `.loc` (from Guide 2):

```python
best_day = data["Close"].idxmax()
data.loc[best_day]        # the full row for the highest-close day
```

**Try this 👉** find the date of the biggest-volume day using
`data["Volume"].idxmax()`, then look at its full row.

---

## Searching by date 📅

The date is the index, so you filter on it with `data.index`. Keep only rows on
or after a date:

```python
data[data.index >= "2024-03-01"]
```

Same boolean-mask idea — `data.index >= "2024-03-01"` is True/False per row.
Between two dates uses `&`:

```python
data[(data.index >= "2024-03-01") & (data.index <= "2024-04-30")]
```

> 💡 The same mask idea works whatever the index holds — dates here, or stock
> tickers in a screener table (more on that just below).

---

## Counting the matches 🔢

Want to know *how many* days matched, not see them all? Wrap the filtered table
in `len(...)`:

```python
len(data[data["Close"] > data["Open"]])   # how many up days?
```

Or as a fraction of all days, to get "what % of days were up":

```python
up_days = len(data[data["Close"] > data["Open"]])
total = len(data)
print(up_days / total)
```

---

## Filtering a screener table 🧮

Everything above filtered **one company's daily prices** — one row per *day*. But
the exact same moves work on a table where each row is a whole **company**. That
table is the heart of a stock screener.

Imagine a DataFrame called `universe` with **one row per stock**, the ticker as
the index, and a handful of summary columns:

```
        Name        Price  Change %  Day %   Avg Volume  Volatility %
Ticker
AAPL    Apple      187.25      8.40   1.10   58_000_000          1.80
MSFT    Microsoft  402.10     12.30  -0.40   22_000_000          1.50
TSLA    Tesla      248.50     -6.20   2.90   95_000_000          3.40
NVDA    Nvidia     880.00     22.10   0.75  41_000_000          2.60
```

Now the *same* boolean-mask filtering answers questions about **stocks** instead
of days:

```python
universe[universe["Change %"] > 5]              # only stocks up more than 5%
universe[universe["Avg Volume"] > 20_000_000]   # only heavily-traded stocks
```

Ranking works too — sort the winners to the top:

```python
universe.sort_values("Change %", ascending=False)   # biggest gainers first
```

And you combine conditions exactly like before, with `&` and brackets around each
part:

```python
universe[(universe["Change %"] > 0) & (universe["Volatility %"] < 3)]
# stocks that are up, but not too jumpy
```

That's it — **this is literally what a screener does.** It takes a table of every
stock and filters it down to the interesting ones: the big movers, the busy ones,
the steady ones. You already know how; it's the same `data[mask]` move, pointed at
a table of companies instead of a table of days. In Guide 5 you'll wire these
filters up to sliders and a search box so anyone can drive them. 🎛️

---

## ✅ Check yourself

This is the core skill, so it's worth being sure. Can you:

- Explain what a **boolean mask** is (a column of True/False)?
- Write the filter for "days the close was above 150"?
- Write the filter for "up days" (close above open)?
- Combine two conditions with `&`, remembering the brackets?
- Find the date of the highest close with `.idxmax()`?
- Keep only rows on or after a given date?

If those feel doable, you're ready to build the screener. If not, that's fine —
go back to the notebook and try each one on real data until it clicks.

---

## 📓 Practise now

The fourth notebook is packed with filtering exercises on real prices — this is
the one to really take your time over:

**➡️ [`../notebooks/04_filtering_and_searching.ipynb`](../notebooks/04_filtering_and_searching.ipynb)**

Quick lookups: [`../reference/pandas-cheatsheet.md`](../reference/pandas-cheatsheet.md).

You now have everything for the filtering stage of the [`../SPEC.md`](../SPEC.md)
— the heart of the project.

---

**What's next →** [`05-building-the-dashboard.md`](05-building-the-dashboard.md)
— put it all together into the finished screener. 🎉
