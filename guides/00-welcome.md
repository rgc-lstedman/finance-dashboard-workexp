# 👋 Welcome — start here

Hello, and welcome to your stock screener project! In a single **half-day**,
working on your own, you're going to build a real, working web app — one that
downloads live prices for a whole **list** of companies and shows them as a
table with **one row per company**. Then you can filter, sort and search to find
the ones you care about, and click into any single stock to see its chart.
You'll write actual Python to make it happen.

This is a **self-guided** project — there's no mentor looking over your shoulder.
That's on purpose: everything you need is right here in these files, and getting
un-stuck by yourself is a huge part of the fun.

Here's the most important thing to know before you start:

> **You are not expected to already know any of this.** Everything is explained
> from scratch. If a word is new, we tell you what it means the first time it
> appears.

---

## The one mindset that matters 🧠

Coding is not about knowing all the answers. It's about getting **stuck**, then
getting **un-stuck** — over and over. That loop *is* the job. Professional
developers do it all day.

So when something breaks (and it will), that's not you failing. That's just
Tuesday. An error message is a **clue**, not a telling-off. We'll show you how to
read them.

Four things to try when you're stuck — in this order:

1. **Read the error slowly.** It usually points at the problem — often the very
   last line tells you what went wrong.
2. **Search the exact error text online.** Copy the key part of the message into
   a search engine. Whatever you hit, someone has hit it before.
3. **Check the matching cheat-sheet** in [`../reference/`](../reference/).
4. **Peek at the worked answer.** A complete version lives on the `solution` git
   branch — run `git switch solution` to read it, then `git switch main` to go
   back to your own. Try your own way first; peek only when you're truly stuck.

---

## What the half-day looks like ⏳

Roughly, you'll move through this shape:

1. **Get set up** — install the tools, run the starter app once. (One-off.)
2. **Learn the building blocks** — Python, then tables of data, then how to
   download stock prices.
3. **Learn the core skill** — filtering a table down to the rows you care about.
4. **Build the screener** — glue it all together into the finished app.

It's meant to fit in a half-day, so keep moving and don't polish too early. You
don't need to memorise anything. Look things up. That's normal.

---

## The four kinds of material (and how they fit together) 🧩

There's more than one file here, and that's on purpose — each does a different
job. Use them together:

| Material | What it's for | Where |
| -------- | ------------- | ----- |
| **SETUP** | Install everything and run the app once. **Do this first.** | [`../SETUP.md`](../SETUP.md) |
| **Guides** (you're reading one) | Slow, friendly lessons that teach each idea from zero. | `guides/` |
| **Notebooks** | Interactive lessons you *run and edit yourself* to practise. | [`../notebooks/`](../notebooks/) |
| **The Spec** | The "job description": what the finished app must do, in stages. | [`../SPEC.md`](../SPEC.md) |
| **Reference** | Short cheat-sheets to look up syntax once you're going. | [`../reference/`](../reference/) |

A good rhythm is: **read a guide → practise in the matching notebook → look
things up in the reference when you build.** The Spec is your checklist for the
final app.

---

## 👉 Do this first

If you haven't already, go and do the setup:

**➡️ [`../SETUP.md`](../SETUP.md)** — installs Python and the packages, and gets
the starter app running in your browser. It takes about 15–20 minutes. Come back
here when you can see the skeleton screener on screen.

---

## ✅ Check yourself

Before moving on, you should be able to tick these off:

- I've run `uv sync` and `uv run streamlit run app.py` and seen the app open.
- I understand that getting stuck is normal and errors are clues.
- I know the difference between the guides, notebooks, Spec and reference.

If all three feel true, you're ready. 🎉

---

**What's next →** [`01-python-basics.md`](01-python-basics.md) — the absolute
basics of Python, tied to the finance app you're building.
