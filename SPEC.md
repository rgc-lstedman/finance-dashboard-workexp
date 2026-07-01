# 📋 The Spec — what your dashboard should do

Think of this as the **job description** for the app you're building. It's broken
into **stages**. Each stage adds one feature. Do them in order — each builds on
the last.

For every stage you'll see:

- **Goal** — what you're adding, in plain English.
- **Done when** — how you know it works (your checklist).
- **Hints** — where to look. The matching guide and cheat-sheet go deeper.

You edit **one file** the whole way through: **`app.py`**. Run it with
`uv run streamlit run app.py` and refresh your browser as you go. Streamlit
even has a **"Rerun"** button that appears when it notices you saved changes.

> 🧭 Don't rush ahead. Get each stage actually working before starting the next.
> A small thing that works beats a big thing that doesn't.

---

## Background: what the data looks like

When you download a stock with `yfinance`, you get a **DataFrame** (a table). One
row per trading day. The important columns are:

| Column | Meaning |
| ------ | ------- |
| `Open` | Price when the market opened that day |
| `High` | Highest price during the day |
| `Low` | Lowest price during the day |
| `Close` | Price when the market closed (the "headline" price) |
| `Volume` | How many shares changed hands that day |

The **date** is the row label (the "index"). We mostly care about `Close`.

We download it with this one line (the options just keep the column names simple —
you'll learn what they mean in the guides):

```python
data = yf.download(ticker, period=period, auto_adjust=True,
                   multi_level_index=False, progress=False)
```

---

## Stage 1 — Show data for one company 📥

**Goal:** download the price history for a single ticker and show it as a table.

**Done when:**
- The app downloads data for a hard-coded ticker (e.g. `"AAPL"`).
- The full table appears on the page.
- You can see dates going down the side and `Open`/`Close`/`Volume` columns.

**Hints:**
- Use the download line from the "Background" section above — it gives you the table.
- `st.dataframe(data)` shows a table in Streamlit.
- Guide: [`guides/03-getting-data-yfinance.md`](guides/03-getting-data-yfinance.md)

---

## Stage 2 — Let the user choose the company and time range 🎛️

**Goal:** replace the hard-coded ticker with inputs the user controls.

**Done when:**
- There's a text box where the user types a ticker (default it to `AAPL`).
- There's a dropdown (or radio buttons) to pick the period: `1mo`, `6mo`, `1y`, `5y`.
- Changing either one updates the table.

**Hints:**
- `st.text_input("Ticker", value="AAPL")` returns whatever the user typed.
- `st.selectbox("Period", ["1mo", "6mo", "1y", "5y"])` returns the chosen option.
- Put these in the **sidebar** with `st.sidebar.text_input(...)` to keep it tidy.
- Guide: [`guides/05-building-the-dashboard.md`](guides/05-building-the-dashboard.md)

---

## Stage 3 — Show the headline numbers 🔢

**Goal:** show a few key figures at the top so you don't have to read the whole table.

**Done when:**
- You show the **latest closing price**.
- You show the **change** vs the start of the period (as a number or %).
- You show the **highest** and **lowest** close over the period.

**Hints:**
- `data["Close"]` is the column of closing prices.
- `.iloc[-1]` is the last value, `.iloc[0]` is the first, `.max()` / `.min()` do what they say.
- `st.metric("Latest close", value, delta)` shows a nice number with an up/down arrow.
- Cheat-sheet: [`reference/pandas-cheatsheet.md`](reference/pandas-cheatsheet.md)

---

## Stage 4 — Search and filter the data 🔍

**Goal:** let the user narrow the table down to the rows they care about.

**Done when (pick at least two):**
- A checkbox "Only show up days" that keeps rows where `Close > Open`.
- A slider for **minimum volume** that hides low-activity days.
- A date filter that keeps only rows on/after a chosen date.

**Hints:**
- Filtering a DataFrame: `data[data["Close"] > data["Open"]]`.
- A slider: `st.slider("Min volume", 0, int(data["Volume"].max()))`.
- This is the heart of the project — understanding *filtering* is the main skill.
- Guide: [`guides/04-filtering-searching.md`](guides/04-filtering-searching.md)

---

## Stage 5 — Draw a chart 📈

**Goal:** turn the numbers into a picture.

**Done when:**
- There's a line chart of the closing price over time.
- The chart updates when the user changes the ticker or period.

**Hints:**
- The quick way: `st.line_chart(data["Close"])`.
- The prettier way: build a `plotly` figure and use `st.plotly_chart(fig)`.
- Cheat-sheet: [`reference/streamlit-cheatsheet.md`](reference/streamlit-cheatsheet.md)

---

## Stretch goals — only if you've finished the above 🌟

These are optional. Pick whatever sounds fun.

1. **Moving average.** Add a smoothed line: `data["Close"].rolling(20).mean()`.
   Plot it on the same chart as the price.
2. **Compare two companies.** Let the user enter a second ticker and plot both
   closing prices together. Tip: downloading a *list* of tickers
   (`yf.download(["AAPL", "MSFT"], ...)`) gives you "multi-level" columns like
   `data["Close"]["AAPL"]` — the guides explain how to read them.
3. **Download button.** Let the user save the (filtered) table as a CSV with
   `st.download_button(...)`.
4. **Best/worst day.** Work out and display the single biggest up-day and
   down-day in the period.
5. **Make it yours.** Add an emoji, a title, colours, a "fun fact" — anything.

---

## What "finished" looks like

A dashboard where you can type any ticker, pick a period, see the headline
numbers, filter the table, and view a chart — and it all updates as you change
the controls. If you get there, you've built a real, useful data app. 👏

> 🔎 Want to see one way of doing it? A complete version lives on the
> **`solution`** branch: `git switch solution`. Try to build yours first — then
> compare. There's no single "right" answer.
