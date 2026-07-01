# 📈 Finance Dashboard — Work Experience Project

Welcome! Over the next few days you are going to build a **finance dashboard**: a
small web app that downloads real stock-market data and lets you search, filter
and chart it. By the end you'll have something you can show people — and you'll
have written real Python to make it work.

You do **not** need any previous coding experience. Every step is explained.

---

## What you'll build

A [Streamlit](https://streamlit.io) web app where you can:

- Type in a company's ticker (like `AAPL` for Apple, `MSFT` for Microsoft)
- Download its recent share-price history from the internet
- See the data in a table
- Filter it (e.g. "only show days the price went up")
- Draw a chart of the price over time

Here's the shape of it:

```
   ┌─────────────────────────────────────────────┐
   │  📈 My Finance Dashboard                     │
   │                                              │
   │  Ticker: [ AAPL ]   Period: [ 6 months ▾ ]   │
   │                                              │
   │   ╱╲      ╱╲                                  │
   │  ╱  ╲╱╲  ╱  ╲   ← price chart                 │
   │ ╱      ╲╱    ╲                                │
   │                                              │
   │  Date        Open    Close   Volume          │
   │  2024-01-02  185.6   187.2   52,000,000  ←table│
   │  2024-01-03  187.1   184.9   48,000,000      │
   └─────────────────────────────────────────────┘
```

---

## The tools you'll learn

| Tool | What it is | Why we use it |
| ---- | ---------- | ------------- |
| **Python** | A popular, readable programming language | The language everything here is written in |
| **uv** | A tool that installs Python and manages the project | Makes setup painless — one tool, same steps on Windows and Mac |
| **pandas** | A library for working with tables of data ("DataFrames") | Loads, filters and reshapes the market data |
| **yfinance** | A library that downloads stock data from Yahoo Finance | Where the real numbers come from |
| **Streamlit** | A library that turns Python into a web app | Gives you the dashboard, no web-design needed |
| **Jupyter notebooks** | An interactive way to run Python bit by bit | How you'll learn and experiment before writing the app |

---

## 🚀 How to start (read these in order)

1. **[SETUP.md](SETUP.md)** — install everything and get the project running. **Do this first.**
2. **[guides/00-welcome.md](guides/00-welcome.md)** — the friendly, step-by-step track. Start here to learn.
3. **[SPEC.md](SPEC.md)** — the "job": what your finished dashboard should do, broken into stages.
4. **[notebooks/](notebooks/)** — interactive lessons you run and edit yourself.
5. **[reference/](reference/)** — short cheat-sheets to look things up once you're going.

There are **two learning tracks** — use whichever suits you:

- 📖 **`guides/`** — walks you through everything slowly, assumes zero experience.
- ⚡ **`reference/`** — quick cheat-sheets for when you just need to remember the syntax.

---

## Project layout

```
finance-dashboard-workexp/
├── README.md          ← you are here
├── SETUP.md           ← install & run instructions (start here)
├── SPEC.md            ← what to build, stage by stage
├── app.py             ← the dashboard you'll grow (starts as a skeleton)
├── pyproject.toml     ← the list of packages the project needs
├── guides/            ← step-by-step lessons (hand-holding)
├── reference/         ← short cheat-sheets
├── notebooks/         ← interactive Jupyter lessons
└── data/              ← a place to save data you download
```

> 💡 **Mentors:** a complete, working version of the dashboard lives on the
> **`solution`** branch (`git switch solution`). The `main` branch deliberately
> ships only a skeleton so students build it up themselves.

---

## Stuck?

That's normal — being stuck and then un-stuck is what coding *is*. Try, in order:

1. Re-read the error message slowly. It usually says what's wrong.
2. Check the matching cheat-sheet in `reference/`.
3. Ask your mentor. Show them the code and the full error text.

Good luck — have fun with it. 🎉
