# 🎉 Guide 5 — Build the screener

This is the capstone. You've learned Python, DataFrames, downloading data, and
filtering. Now you'll wire it all into a real web app using **Streamlit** — a
**stock screener**.

A screener shows **many stocks at once** — one row per company, with a few key
numbers for each — and lets you **filter, sort and search** to find the ones you
care about. Then you can click into a single stock to see its price chart. It's
the tool a real analyst opens first thing in the morning.

By the end of this guide you'll have something you can genuinely show people. 🚀

You'll grow the starter `app.py`, one Spec stage at a time. The good news: you're
**given** the tricky data-downloading part below — your job is to build the
filtering, sorting and searching on top of it, which is exactly what you already
practised in Guide 4.

---

## What is Streamlit? 🖥️

**Streamlit** turns a plain Python script into a web app — no HTML, no
JavaScript, no web-design knowledge needed. You write normal Python, sprinkle in
a few `st.something(...)` lines, and Streamlit draws the page for you.

You import it (already at the top of `app.py`) as `st`:

```python
import streamlit as st
```

A handful of building blocks do most of the work:

```python
st.title("📈 Stock Screener")     # a big heading
st.write("Hello!")                # text, tables, almost anything
st.dataframe(data)                # show a DataFrame as an interactive table
st.line_chart(data["Close"])      # draw a line chart from a column
```

You've already seen `st.title`, `st.write` and `st.dataframe` in the skeleton.

---

## The one weird thing about Streamlit: it reruns everything 🔄

This trips everyone up at first, so let's get it clear now.

**Every time the user touches a control, Streamlit runs your *whole script again*
from top to bottom.** Type in the search box? The script reruns. Move a slider?
Reruns.

That sounds wasteful, but it's what makes Streamlit so simple: you never write
"when the user clicks, update that box" code. You just describe what the page
should look like *given the current values*, and Streamlit re-draws it every time
something changes.

So a Streamlit widget does two jobs at once:

1. It **draws** the control on the page.
2. It **returns** the current value, which you use further down the script.

```python
query = st.text_input("Search")
# `query` now holds whatever is in the box right now — "" until the user
# types something, at which point the whole script reruns with the new value.
```

Keep that picture in your head — "the script reruns and hands me the latest
values" — and Streamlit stops feeling mysterious.

---

## The widgets you'll use 🎛️

These are your controls. Each one draws something *and* returns the user's
current choice:

| Widget | Draws | Returns |
| ------ | ----- | ------- |
| `st.text_input("Search")` | A text box | The typed text |
| `st.selectbox("Period", ["1mo","6mo","1y"])` | A dropdown | The chosen option |
| `st.slider("Min change %", -50, 50)` | A slider | The chosen number |
| `st.checkbox("Only up today")` | A tick box | `True` or `False` |
| `st.metric("Price", 187.25, 1.4)` | A big number with an arrow | *(nothing — display only)* |

And two layout helpers:

- `st.sidebar.something(...)` puts a widget in the **sidebar** — the panel down
  the left — to keep the main area clean. It's the natural home for filters.
- `col1, col2 = st.columns(2)` splits a row into side-by-side columns.

> 💡 `st.sidebar.text_input(...)` and `st.text_input(...)` are the same widget —
> the `.sidebar` part just chooses *where* it appears.

---

## The stocks, and the table that describes them 🌍

A screener needs **many** companies. So instead of downloading one ticker, we
download a whole list of them and boil each one down to a single row of summary
numbers.

**You are given this part — copy it as-is into `app.py`.** It's the fiddly bit;
your job is the filtering on top. Read the comments so you understand *what* it
hands back:

```python
import pandas as pd
import streamlit as st
import yfinance as yf

UNIVERSE = {
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon",
    "META": "Meta", "NVDA": "Nvidia", "TSLA": "Tesla", "AMD": "AMD",
    "INTC": "Intel", "NFLX": "Netflix", "JPM": "JPMorgan", "V": "Visa",
    "MA": "Mastercard", "DIS": "Disney", "KO": "Coca-Cola", "PEP": "PepsiCo",
    "MCD": "McDonald's", "NKE": "Nike", "XOM": "Exxon Mobil", "CVX": "Chevron",
    "PFE": "Pfizer", "JNJ": "Johnson & Johnson", "WMT": "Walmart",
    "BA": "Boeing", "SBUX": "Starbucks",
}

@st.cache_data(ttl=3600)
def load_universe(period):
    """Download every stock once, build a one-row-per-stock summary table."""
    raw = yf.download(list(UNIVERSE), period=period, auto_adjust=True, progress=False)
    close = raw["Close"]            # a table: one column per stock
    volume = raw["Volume"]
    daily_returns = close.pct_change()
    summary = pd.DataFrame({
        "Name": pd.Series(UNIVERSE),
        "Price": close.iloc[-1],
        "Change %": (close.iloc[-1] / close.iloc[0] - 1) * 100,
        "Day %": (close.iloc[-1] / close.iloc[-2] - 1) * 100,
        "Avg Volume": volume.mean(),
        "Volatility %": daily_returns.std() * 100,
    })
    summary.index.name = "Ticker"
    return summary.dropna(subset=["Price"]).round(2)
```

### Why this works — read this bit slowly 🧠

Two ideas make the whole thing tick.

**1. Downloading a *list* of tickers gives you two-level columns.** Back in
Guides 3 and 4 you downloaded **one** company and asked for
`multi_level_index=False`, so the columns were plain — `Open`, `Close`, `Volume`.
Here we hand `yf.download` a whole *list* (`list(UNIVERSE)`), so pandas needs a
way to say *whose* `Close` is whose. It uses **two-level** column names: the
measurement on top (`Close`, `Volume`, …) and the ticker underneath.

That's why `raw["Close"]` isn't a single column — it's a whole **table with one
column per stock** (and dates down the side). The same for `raw["Volume"]`. Once
you've got that table, the summary numbers fall out easily:

- `close.iloc[-1]` — the **last** row → today's price for *every* stock at once.
- `close.iloc[0]` — the **first** row → the price at the start of the period.
- `close.iloc[-2]` — the **second-to-last** row → yesterday's price.
- `volume.mean()` — the average of each column → typical daily volume per stock.
- `close.pct_change().std()` — how bumpy each stock's daily returns are
  (our rough "volatility").

**2. The result is one clean row per company.** `load_universe` packs those
numbers into a new DataFrame called `summary`, with the **ticker as the index**
and exactly these columns:

```
        Name        Price  Change %  Day %   Avg Volume  Volatility %
Ticker
AAPL    Apple      187.25      8.40   1.10   58000000.0          1.80
MSFT    Microsoft  402.10     12.30  -0.40   22000000.0          1.50
TSLA    Tesla      248.50     -6.20   2.90   95000000.0          3.40
...
```

That's the screener's raw material: **one row per stock, key numbers as columns.**
Everything from here is just filtering and sorting that table — which you already
know how to do.

> 💡 `@st.cache_data(ttl=3600)` above the function means "download once, then
> reuse the result for an hour". Without it, Streamlit's rerun-on-every-click
> would re-download all 25 stocks every time you nudged a slider — slow and
> annoying. With it, the first run is a little slow and the rest are instant.

---

## Building it up, stage by stage 🧱

Open `app.py`. Paste in the `UNIVERSE` dict and `load_universe` function above,
then add each stage on top. Run `uv run streamlit run app.py`, keep the browser
open, and click **Rerun** (top-right) each time you save.

### Stage 2 — load the table and show it 📥

Pick how much history to summarise, load the universe, and show it:

```python
period = st.sidebar.selectbox("History period", ["1mo", "6mo", "1y"], index=1)
data = load_universe(period)

st.dataframe(data)
```

- `index=1` makes `6mo` the starting choice (item number 1, counting from 0).
- `data` is now the summary table — one row per stock.

Save, Rerun, and you should see all 25 companies in a sortable table. That's a
screener already, just without controls yet. 🎉

### Stage 3 — the filters (this is the core) 🔍

This is where Guide 4 pays off. Add three controls to the sidebar, then use them
to narrow a **copy** of the table. Working on a copy called `view` keeps the full
`data` around so you can always show "X of Y stocks".

```python
query = st.sidebar.text_input("Search ticker or name")
min_change = st.sidebar.slider("Minimum Change %", -50, 50, -50)
min_volume_m = st.sidebar.slider("Minimum avg volume (millions)", 0, 100, 0)

view = data.copy()

if query:
    q = query.strip().lower()
    view = view[view.index.str.lower().str.contains(q)
                | view["Name"].str.lower().str.contains(q)]

view = view[view["Change %"] >= min_change]
view = view[view["Avg Volume"] >= min_volume_m * 1_000_000]
```

What's happening — every line is a boolean mask from Guide 4:

- **The search box** matches either the ticker (the index) or the company name.
  `.str.lower()` on both sides makes it case-insensitive, and `|` (or) means
  "matches *either*". If the box is empty we skip it.
- **The Change % slider** keeps only stocks up at least that much. Drag it to `5`
  and you get today's winners; drag it negative to hunt for fallers.
- **The volume slider** is in *millions* for readability, so we multiply by
  `1_000_000` before comparing to the raw `Avg Volume` column.

Each filter just reassigns `view` to a smaller table. Exactly the `data[mask]`
move you already know — pointed at a table of companies.

### Stage 4 — sort the winners to the top 🔢

Filtering keeps rows; **sorting** reorders them. Let the user choose the column,
then sort with the biggest first:

```python
sort_col = st.sidebar.selectbox(
    "Sort by", ["Change %", "Day %", "Price", "Avg Volume", "Volatility %"]
)
view = view.sort_values(sort_col, ascending=False)

st.caption(f"Showing {len(view)} of {len(data)} stocks")
st.dataframe(view)
```

`ascending=False` puts the largest at the top — so "Sort by Change %" ranks the
day's best performers first. The caption tells the user how much the filters
trimmed. Move the sliders and watch the table shrink and reorder live. That's a
working screener. 🎯

### Stage 5 — look at one stock 📈

The screener finds interesting stocks; now let the user click into one. Pick a
ticker from whatever survived the filters, download **that single company** (back
to the plain, one-company form with `multi_level_index=False`), and chart it:

```python
if len(view) > 0:
    choice = st.selectbox("Pick a stock", view.index)

    one = yf.download(choice, period=period, auto_adjust=True,
                      multi_level_index=False, progress=False)

    row = data.loc[choice]
    c1, c2 = st.columns(2)
    c1.metric(f"{choice} price", f"{row['Price']:,.2f}", f"{row['Change %']:.2f}%")
    c2.metric("Volatility %", f"{row['Volatility %']:.2f}")

    st.line_chart(one["Close"])
```

- `st.selectbox("Pick a stock", view.index)` offers only the tickers currently in
  the filtered table.
- We pull that stock's summary row back out with `data.loc[choice]` (the `.loc`
  by-label lookup from Guide 2) to fill the metrics. The third argument to the
  first `st.metric` is the **delta** — Streamlit shows it green with an up arrow
  when positive, red when negative. Free and nice. 📈
- `st.line_chart(one["Close"])` draws the price history, and redraws whenever the
  choice or period changes.

The `if len(view) > 0` guard matters: if the filters are so strict that *no*
stock matches, there's nothing to pick, so we skip this block instead of erroring.

---

## The finished screener, all together 🧩

Here's `app.py` with every stage in place — your target for the core project:

```python
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Screener", page_icon="📈")
st.title("📈 Stock Screener")
st.write("Filter a table of well-known stocks, then click into one for its chart.")

UNIVERSE = {
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon",
    "META": "Meta", "NVDA": "Nvidia", "TSLA": "Tesla", "AMD": "AMD",
    "INTC": "Intel", "NFLX": "Netflix", "JPM": "JPMorgan", "V": "Visa",
    "MA": "Mastercard", "DIS": "Disney", "KO": "Coca-Cola", "PEP": "PepsiCo",
    "MCD": "McDonald's", "NKE": "Nike", "XOM": "Exxon Mobil", "CVX": "Chevron",
    "PFE": "Pfizer", "JNJ": "Johnson & Johnson", "WMT": "Walmart",
    "BA": "Boeing", "SBUX": "Starbucks",
}

@st.cache_data(ttl=3600)
def load_universe(period):
    """Download every stock once, build a one-row-per-stock summary table."""
    raw = yf.download(list(UNIVERSE), period=period, auto_adjust=True, progress=False)
    close = raw["Close"]            # a table: one column per stock
    volume = raw["Volume"]
    daily_returns = close.pct_change()
    summary = pd.DataFrame({
        "Name": pd.Series(UNIVERSE),
        "Price": close.iloc[-1],
        "Change %": (close.iloc[-1] / close.iloc[0] - 1) * 100,
        "Day %": (close.iloc[-1] / close.iloc[-2] - 1) * 100,
        "Avg Volume": volume.mean(),
        "Volatility %": daily_returns.std() * 100,
    })
    summary.index.name = "Ticker"
    return summary.dropna(subset=["Price"]).round(2)

# Stage 2 — pick the history period and load the table
period = st.sidebar.selectbox("History period", ["1mo", "6mo", "1y"], index=1)
data = load_universe(period)

# Stage 3 — the filters (the core of a screener)
query = st.sidebar.text_input("Search ticker or name")
min_change = st.sidebar.slider("Minimum Change %", -50, 50, -50)
min_volume_m = st.sidebar.slider("Minimum avg volume (millions)", 0, 100, 0)

view = data.copy()
if query:
    q = query.strip().lower()
    view = view[view.index.str.lower().str.contains(q)
                | view["Name"].str.lower().str.contains(q)]
view = view[view["Change %"] >= min_change]
view = view[view["Avg Volume"] >= min_volume_m * 1_000_000]

# Stage 4 — sort
sort_col = st.sidebar.selectbox(
    "Sort by", ["Change %", "Day %", "Price", "Avg Volume", "Volatility %"]
)
view = view.sort_values(sort_col, ascending=False)

st.caption(f"Showing {len(view)} of {len(data)} stocks")
st.dataframe(view)

# Stage 5 — click into one stock
if len(view) > 0:
    choice = st.selectbox("Pick a stock", view.index)
    one = yf.download(choice, period=period, auto_adjust=True,
                      multi_level_index=False, progress=False)
    row = data.loc[choice]

    c1, c2 = st.columns(2)
    c1.metric(f"{choice} price", f"{row['Price']:,.2f}", f"{row['Change %']:.2f}%")
    c2.metric("Volatility %", f"{row['Volatility %']:.2f}")

    st.line_chart(one["Close"])
```

If yours does all this — loads the table, filters it with the search box and
sliders, sorts it, and charts whichever stock you pick — **you've built a real,
working screener.** 👏

---

## Go further 🌟

Finished the core? There's a list of things to try next — a moving-average line,
a "Day %" gainers-vs-losers split, more companies in `UNIVERSE`, a download
button, and more — in **[`../docs/NEXT-STEPS.md`](../docs/NEXT-STEPS.md)**. Pick whatever
sounds fun.

---

## 👀 Peek at one solution

A complete, working version lives on the **`solution`** git branch. Try to build
yours first — *then* compare, to see one way of doing it:

```bash
git switch solution
```

There's no single "right" answer, so don't worry if yours looks different. When
you're done looking, `git switch main` goes back to your own version.

---

## ✅ Check yourself

You've finished the project if:

- The table shows many stocks, one row each, and you can pick the history period.
- The search box and sliders narrow the table down.
- Choosing a "Sort by" column reorders the rows.
- Picking a stock shows its metrics and a line chart of its price.

---

## 📓 Practise now

The final notebook covers charts and getting your code Streamlit-ready:

**➡️ [`../notebooks/05_charts_and_streamlit_prep.ipynb`](../notebooks/05_charts_and_streamlit_prep.ipynb)**

Keep the [`../reference/streamlit-cheatsheet.md`](../reference/streamlit-cheatsheet.md)
open while you build.

---

**What's next →** you've reached the end of the guide track. 🎉 Go make the
screener yours — a title, an emoji, your favourite companies in `UNIVERSE`, a
"fun fact". Then show someone what you built. Well done!
