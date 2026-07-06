# 📋 The Spec — what your screener should do

Think of this as the **job description** for the app you're building. It's broken
into **stages**. Each stage adds one feature. Do them in order — each builds on
the last.

You are building a **stock screener**: an app that shows lots of companies at
once (one row each), lets you **filter, sort and search** to find the interesting
ones, and lets you **click into a single stock** to see its price chart.

For every stage you'll see:

- **Goal** — what you're adding, in plain English.
- **Done when** — how you know it works (your checklist).
- **Hints** — the code you'll likely need. The guide and cheat-sheets go deeper.

You edit **one file** the whole way through: **`app.py`**. Run it with
`uv run streamlit run app.py` and refresh your browser as you go.

> 🎯 **Stages 1–5 are the goal.** The stretch goals and
> **[NEXT-STEPS.md](NEXT-STEPS.md)** are for afterwards — you can keep working on
> this whenever you like.

> 🧭 Get each stage actually working before starting the next. A small thing that
> works beats a big thing that doesn't. Stuck? Peek at the finished version on the
> `solution` branch: `git switch solution`.

---

## Background: the screener table

The starter `app.py` already downloads the stocks for you and builds a table with
**one row per company**. Each row has these columns:

| Column | Meaning |
| ------ | ------- |
| `Ticker` (the row label) | The stock's short code, e.g. `AAPL` |
| `Name` | The company name |
| `Price` | The most recent closing price |
| `Change %` | How much the price moved over the whole period |
| `Day %` | How much it moved on the most recent day |
| `Avg Volume` | Average number of shares traded per day (how "busy" it is) |
| `Volatility %` | How bumpy the price is (bigger = wilder swings) |

**A screener is really just filtering and sorting this table** — which is the main
skill this project teaches.

---

## Stage 1 — Run it and read the table ✅

**Goal:** get the starter app running and understand what you're looking at.

**Done when:**
- `uv run streamlit run app.py` shows a table of ~25 stocks in your browser.
- You can point at a row and say what each number means.

**Hints:**
- This stage is already done for you — it's your starting point.
- Change the `page_icon` or title text to make it feel like yours.

---

## Stage 2 — Let the user choose the time period 🎛️

**Goal:** replace the fixed `period = "6mo"` with a control the user picks.

**Done when:**
- There's a dropdown in the sidebar to choose `1mo`, `6mo` or `1y`.
- Changing it refreshes the numbers (the `Change %` column especially).

**Hints:**
- `period = st.sidebar.selectbox("History period", ["1mo", "6mo", "1y"], index=1)`
- Put it **above** the `data = load_universe(period)` line so the choice is used.
- Guide: [`guides/05-building-the-dashboard.md`](../guides/05-building-the-dashboard.md)

---

## Stage 3 — Filter the screener 🔍 (the main event)

**Goal:** let the user narrow the table down to the stocks they care about.

**Done when (do at least the first two):**
- A **search box** that keeps only rows whose ticker or name matches what's typed.
- A **slider** for minimum `Change %` (hide stocks that didn't move enough).
- A **slider** for minimum `Avg Volume` (hide the quiet stocks).

**Hints:**
- Work on a copy so you never lose the full list: `view = data.copy()`.
- Filtering is a *boolean mask*: `view = view[view["Change %"] >= min_change]`.
- Search: `text = st.sidebar.text_input("Search").upper()` then keep rows where
  `view.index.str.contains(text) | view["Name"].str.upper().str.contains(text)`.
- This is the heart of the project. Guide: [`guides/04-filtering-searching.md`](../guides/04-filtering-searching.md)

---

## Stage 4 — Sort / rank the results 🏆

**Goal:** let the user rank the table by any column.

**Done when:**
- A dropdown chooses which column to sort by.
- The biggest values come first (the "winners" at the top).

**Hints:**
- `sort_col = st.sidebar.selectbox("Sort by", ["Change %", "Day %", "Price", "Avg Volume", "Volatility %"])`
- `view = view.sort_values(sort_col, ascending=False)`
- Cheat-sheet: [`reference/pandas-cheatsheet.md`](../reference/pandas-cheatsheet.md)

---

## Stage 5 — Look at one stock 📈

**Goal:** pick a single company from your results and chart its price.

**Done when:**
- A dropdown lets the user pick one ticker from the filtered table.
- You show its recent price as a line chart (and maybe its latest price).

**Hints:**
- `choice = st.selectbox("Pick a stock", view.index)`
- Download just that one, using the flat form so `["Close"]` is a single column:
  ```python
  one = yf.download(choice, period=period, auto_adjust=True,
                    multi_level_index=False, progress=False)
  ```
- `st.line_chart(one["Close"])`, and `st.metric("Latest", f"${one['Close'].iloc[-1]:,.2f}")`.
- Guide: [`guides/05-building-the-dashboard.md`](../guides/05-building-the-dashboard.md)

---

## 🌟 Stretch goals (for afterwards)

Finished stages 1–5? Nice work. Pick anything from here or from
**[NEXT-STEPS.md](NEXT-STEPS.md)**:

1. **More filters** — max `Volatility %`, or "only stocks that fell" (`Change % < 0`).
2. **Colour the winners and losers** — style the `Change %` column green/red.
3. **A moving average** on the single-stock chart: `one["Close"].rolling(20).mean()`.
4. **Add your own companies** to the `UNIVERSE` dictionary at the top of `app.py`.
5. **Download button** — let the user save the filtered table as a CSV.
6. **Best & worst** — show which stock rose most and which fell most today.

---

## What "finished" looks like

A screener where you choose a period, filter and sort a table of stocks to find
the ones you want, and click into any one of them to see its chart — all updating
as you change the controls. That's a real, useful data app. 👏

> 🔎 Want to compare with one finished version? `git switch solution`. Try to
> build yours first — there's no single "right" answer.
