# 🗺️ A suggested order to work through it

Here's a suggested order. It's a guide, not a rule — if you're enjoying one part,
stay with it. The **goal** is a working screener (Stages 1–5 in
[SPEC.md](SPEC.md)). Everything after that is a bonus. Take a break whenever you
need one.

| Step | What you're doing | Where to look |
| ---- | ----------------- | ------------- |
| **1** | **Get set up.** Install `uv`, get the project, run the starter app and see the screener table appear. | [SETUP.md](SETUP.md) |
| **2** | **Python basics.** Variables, lists, dictionaries, loops, functions — just enough to read the code. | [guides/01-python-basics.md](../guides/01-python-basics.md) + [notebooks/01_python_basics.ipynb](../notebooks/01_python_basics.ipynb) |
| **3** | **Tables (pandas).** What a DataFrame is; selecting columns; `.head()`. | [guides/02-dataframes.md](../guides/02-dataframes.md) + [notebooks/02_pandas_dataframes.ipynb](../notebooks/02_pandas_dataframes.ipynb) |
| **4** | **Getting the data.** How `yfinance` downloads stocks; one company vs many. | [guides/03-getting-data-yfinance.md](../guides/03-getting-data-yfinance.md) + [notebooks/03_yfinance_data.ipynb](../notebooks/03_yfinance_data.ipynb) |
| **5** | **Filtering & searching — the core skill.** Boolean masks; filtering a table of stocks. | [guides/04-filtering-searching.md](../guides/04-filtering-searching.md) + [notebooks/04_filtering_and_searching.ipynb](../notebooks/04_filtering_and_searching.ipynb) |
| **6** | **Build your screener.** Work through [SPEC.md](SPEC.md) Stages 2–5 in `app.py`: period picker → filters → sort → single-stock chart. | [guides/05-building-the-dashboard.md](../guides/05-building-the-dashboard.md) + [SPEC.md](SPEC.md) |
| **7** | **Keep going.** Pick a stretch goal or an idea from [NEXT-STEPS.md](NEXT-STEPS.md). | [NEXT-STEPS.md](NEXT-STEPS.md) |

---

## How to actually work through it

- **Type the code yourself** rather than copy-pasting — it sticks far better, and
  the typos you fix along the way teach you a lot.
- **Run things often.** After almost every change, save and look at the result.
  Small steps are easier to fix than big ones.
- **It's fine not to finish.** Getting a filter working is a real achievement.
  The project is yours to continue another day.

## If you're moving fast

Skim the guides, glance at the cheat-sheets in [reference/](../reference/) instead,
and spend your time in `app.py` and the stretch goals. Try wiring up an extra
filter the spec doesn't mention, or add your favourite companies to the
`UNIVERSE` list at the top of `app.py`.

## If you're finding it hard

That's completely normal — this is real programming. Slow right down, do one line
at a time, and lean on [notebooks/01_python_basics.ipynb](../notebooks/01_python_basics.ipynb).
Getting the starter app to run and understanding the table is already a great
first session. Everything else can wait for next time.
