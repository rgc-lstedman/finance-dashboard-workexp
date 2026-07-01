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

> **In the app:** Stage 4 puts this behind a checkbox — tick "Only show up days"
> and the table filters itself to `data[data["Close"] > data["Open"]]`.

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

> **In the app:** Stage 4 offers a date filter — the user picks a start date and
> the table keeps only rows from that date onward.

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

## ✅ Check yourself

This is the core skill, so it's worth being sure. Can you:

- Explain what a **boolean mask** is (a column of True/False)?
- Write the filter for "days the close was above 150"?
- Write the filter for "up days" (close above open)?
- Combine two conditions with `&`, remembering the brackets?
- Find the date of the highest close with `.idxmax()`?
- Keep only rows on or after a given date?

If those feel doable, you're ready to build the dashboard. If not, that's fine —
go back to the notebook and try each one on real data until it clicks.

---

## 📓 Practise now

The fourth notebook is packed with filtering exercises on real prices — this is
the one to really take your time over:

**➡️ [`../notebooks/04_filtering_and_searching.ipynb`](../notebooks/04_filtering_and_searching.ipynb)**

Quick lookups: [`../reference/pandas-cheatsheet.md`](../reference/pandas-cheatsheet.md).

You now have everything for **Stage 4** of the [`../SPEC.md`](../SPEC.md) — the
heart of the project.

---

**What's next →** [`05-building-the-dashboard.md`](05-building-the-dashboard.md)
— put it all together into the finished web app. 🎉
