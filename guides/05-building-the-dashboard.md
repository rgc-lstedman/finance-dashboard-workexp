# 🎉 Guide 5 — Building the dashboard

This is the capstone. You've learned Python, DataFrames, downloading data, and
filtering. Now you'll wire it all into a real web app using **Streamlit**, then
grow the starter `app.py` from a bare table into the full dashboard, one Spec
stage at a time.

By the end of this guide you'll have something you can genuinely show people. 🚀

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
st.title("📈 My Finance Dashboard")   # a big heading
st.write("Hello!")                    # text, tables, almost anything
st.dataframe(data)                    # show a DataFrame as an interactive table
st.line_chart(data["Close"])          # draw a line chart from a column
```

You've already seen `st.title`, `st.write` and `st.dataframe` in the skeleton.

---

## The one weird thing about Streamlit: it reruns everything 🔄

This trips everyone up at first, so let's get it clear now.

**Every time the user touches a control, Streamlit runs your *whole script again*
from top to bottom.** Type a new ticker? The script reruns. Move a slider? Reruns.

That sounds wasteful, but it's what makes Streamlit so simple: you never write
"when the user clicks, update that box" code. You just describe what the page
should look like *given the current values*, and Streamlit re-draws it every time
something changes.

So a Streamlit widget does two jobs at once:

1. It **draws** the control on the page.
2. It **returns** the current value, which you use further down the script.

```python
ticker = st.text_input("Ticker", value="AAPL")
# `ticker` now holds whatever is in the box right now — "AAPL" until the
# user types something else, at which point the whole script reruns with
# the new value.
```

Keep that picture in your head — "the script reruns and hands me the latest
values" — and Streamlit stops feeling mysterious.

---

## The widgets you'll use 🎛️

These are your controls. Each one draws something *and* returns the user's
current choice:

| Widget | Draws | Returns |
| ------ | ----- | ------- |
| `st.text_input("Ticker", value="AAPL")` | A text box | The typed text |
| `st.selectbox("Period", ["1mo","6mo","1y","5y"])` | A dropdown | The chosen option |
| `st.slider("Min volume", 0, 100)` | A slider | The chosen number |
| `st.checkbox("Only up days")` | A tick box | `True` or `False` |
| `st.metric("Latest", 187.25, 1.4)` | A big number with an arrow | *(nothing — display only)* |

And two layout helpers:

- `st.sidebar.something(...)` puts a widget in the **sidebar** — the panel down
  the left — to keep the main area clean.
- `col1, col2 = st.columns(2)` splits a row into side-by-side columns.

> 💡 `st.sidebar.text_input(...)` and `st.text_input(...)` are the same widget —
> the `.sidebar` part just chooses *where* it appears.

---

## Building it up, stage by stage 🧱

Open `app.py`. You'll recognise the skeleton — it already does Stage 1. We'll add
each stage on top. Run `uv run streamlit run app.py`, then keep the browser open
and click **Rerun** (top-right) each time you save.

### Stage 1 — one company, shown as a table ✅ (already done)

The skeleton already downloads a fixed ticker and shows it as a table. We'll use
the same tidy download line from Guide 3 — with `auto_adjust`,
`multi_level_index=False` and `progress=False` — so `data["Close"]` stays one
clean column for the stages ahead:

```python
ticker = "AAPL"
period = "6mo"

data = yf.download(ticker, period=period, auto_adjust=True, multi_level_index=False, progress=False)

if data.empty:
    st.error(f"No data found for '{ticker}'. Is the ticker spelled correctly?")
else:
    st.dataframe(data)
```

That's Stage 1 complete. Now we make it interactive.

### Stage 2 — let the user choose 🎛️

Replace the two hard-coded lines with widgets, and put them in the sidebar:

```python
ticker = st.sidebar.text_input("Ticker", value="AAPL")
period = st.sidebar.selectbox("Period", ["1mo", "6mo", "1y", "5y"], index=1)
```

- `value="AAPL"` makes Apple the starting ticker.
- `index=1` makes `6mo` the starting choice (item number 1 in the list, counting
  from 0).

Save, Rerun, and try typing `MSFT` or picking `1y` — the table updates. That's
the rerun model doing its thing. 🪄

### Stage 3 — the headline numbers 🔢

Inside the `else:` block, *above* the table, add some `st.metric` calls so you
don't have to read every row. Recall from Guide 2: `.iloc[-1]` is the last value,
`.iloc[0]` the first.

```python
    close = data["Close"]
    latest = close.iloc[-1]
    first = close.iloc[0]

    st.metric("Latest close", f"{latest:,.2f}", f"{latest - first:,.2f}")

    col1, col2 = st.columns(2)
    col1.metric("Highest close", f"{close.max():,.2f}")
    col2.metric("Lowest close", f"{close.min():,.2f}")
```

A couple of notes:

- `f"{latest:,.2f}"` formats the number nicely — two decimal places and a comma
  for thousands, e.g. `1,872.50`.
- The third argument to the first `st.metric` is the **delta** (the change since
  the start). Streamlit shows it green with an up arrow if positive, red if
  negative. Nice and free. 📈

### Stage 4 — filters that narrow the table 🔍

This is where Guide 4 pays off. Add controls in the sidebar, then use them to
build a `filtered` copy of the table:

```python
    show_up_only = st.sidebar.checkbox("Only show up days")
    min_volume = st.sidebar.slider("Minimum volume", 0, int(data["Volume"].max()), 0)

    filtered = data
    if show_up_only:
        filtered = filtered[filtered["Close"] > filtered["Open"]]
    filtered = filtered[filtered["Volume"] >= min_volume]
```

What's happening:

- The **checkbox** returns `True`/`False`. When it's ticked, we keep only up days
  (`Close > Open`) — the exact boolean-mask filter from Guide 4.
- The **slider** goes from 0 up to the busiest day's volume
  (`int(data["Volume"].max())`), starting at 0. We keep only days at or above the
  chosen volume.
- We start `filtered` as the full table, then narrow it down step by step.

Then show `filtered` instead of `data` at the bottom:

```python
    st.caption(f"Showing {len(filtered)} of {len(data)} days")
    st.dataframe(filtered)
```

Tick the box, drag the slider, and watch the table shrink. That's the core of the
whole project, live. 🎯

### Stage 5 — draw a chart 📈

One line turns the closing prices into a picture. Add it inside the `else:`
block:

```python
    st.line_chart(data["Close"])
```

That's it — Streamlit draws a line chart of the closing price, and it redraws
whenever the ticker or period changes.

Want it prettier? **plotly** (already installed) gives you titles, hover labels
and zoom:

```python
    import plotly.express as px

    fig = px.line(data, y="Close", title=f"{ticker} closing price")
    st.plotly_chart(fig)
```

Use `st.line_chart` to get going; reach for plotly once the rest works.

---

## The finished dashboard, all together 🧩

Here's `app.py` with every stage in place — your target for the core project:

```python
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="My Finance Dashboard", page_icon="📈")
st.title("📈 My Finance Dashboard")
st.write("Pick a company and explore its share price.")

# Stage 2 — user inputs, tucked into the sidebar
ticker = st.sidebar.text_input("Ticker", value="AAPL")
period = st.sidebar.selectbox("Period", ["1mo", "6mo", "1y", "5y"], index=1)

st.subheader(f"Showing: {ticker}  (last {period})")

# Stage 1 — download the data (tidy columns, no progress bar)
data = yf.download(ticker, period=period, auto_adjust=True, multi_level_index=False, progress=False)

if data.empty:
    st.error(f"No data found for '{ticker}'. Is the ticker spelled correctly?")
else:
    # Stage 3 — headline numbers
    close = data["Close"]
    latest = close.iloc[-1]
    first = close.iloc[0]
    st.metric("Latest close", f"{latest:,.2f}", f"{latest - first:,.2f}")

    col1, col2 = st.columns(2)
    col1.metric("Highest close", f"{close.max():,.2f}")
    col2.metric("Lowest close", f"{close.min():,.2f}")

    # Stage 5 — chart of the closing price
    st.line_chart(data["Close"])

    # Stage 4 — filters that narrow the table
    show_up_only = st.sidebar.checkbox("Only show up days")
    min_volume = st.sidebar.slider("Minimum volume", 0, int(data["Volume"].max()), 0)

    filtered = data
    if show_up_only:
        filtered = filtered[filtered["Close"] > filtered["Open"]]
    filtered = filtered[filtered["Volume"] >= min_volume]

    st.caption(f"Showing {len(filtered)} of {len(data)} days")
    st.dataframe(filtered)
```

If yours does all this — types any ticker, picks a period, shows the headline
numbers, filters the table and draws a chart — **you've built a real, working data
app.** 👏

---

## Go further — the stretch goals 🌟

Finished the core? Pick whatever sounds fun from the [`../SPEC.md`](../SPEC.md)
stretch list. Some starting points:

**Moving average** — a smoothed line over the price (`rolling(20)` averages each
day with the 19 before it):

```python
    import pandas as pd

    chart_data = pd.DataFrame({
        "Close": data["Close"],
        "MA20": data["Close"].rolling(20).mean(),
    })
    st.line_chart(chart_data)
```

**Download button** — let the user save the filtered table as a CSV:

```python
    st.download_button("Download CSV", filtered.to_csv(), "prices.csv")
```

**Best / worst day** — reuse `.idxmax()` / `.idxmin()` from Guide 4 to find and
display the single biggest up-day and down-day.

**Compare two companies** — add a second `st.text_input`, download both, and plot
both closing prices together. This one has a neat twist worth understanding.

So far you've always downloaded **one** company, and asked for
`multi_level_index=False` to get plain column names. When you download **several**
companies at once, pandas needs a way to say *whose* `Close` is whose — so it uses
**two-level** column names. Give `yf.download` a *list* of tickers:

```python
    two = yf.download(["AAPL", "MSFT"], period="6mo", auto_adjust=True, progress=False)
    two.columns   # pairs like ('Close', 'AAPL'), ('Close', 'MSFT'), ...
```

Now the columns come in two levels — the measurement (`Close`, `Volume`, …) *and*
the company. You read them from the outside in:

```python
    two["Close"]           # every company's closing price (one column each)
    two["Close"]["AAPL"]   # just Apple's closing price
    two["Close"]["MSFT"]   # just Microsoft's closing price
```

The nice part: `two["Close"]` is already a table with one column per company, so
you can chart both at once with a single line:

```python
    st.line_chart(two["Close"])   # both closing prices on the same chart
```

So the rule of thumb is simple: **one company = plain columns; several companies =
two-level columns.** Same idea, just an extra label to say which company.

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

- The user can type a ticker and pick a period, and the page updates.
- The headline numbers show the latest close and the change.
- At least two filters work (checkbox, slider or date).
- A chart of the closing price is on the page.

---

## 📓 Practise now

The final notebook covers charts and getting your code Streamlit-ready:

**➡️ [`../notebooks/05_charts_and_streamlit_prep.ipynb`](../notebooks/05_charts_and_streamlit_prep.ipynb)**

Keep the [`../reference/streamlit-cheatsheet.md`](../reference/streamlit-cheatsheet.md)
open while you build.

---

**What's next →** you've reached the end of the guide track. 🎉 Go make the
dashboard yours — a title, an emoji, a fun fact, your favourite companies. Then
show someone what you built. Well done!
