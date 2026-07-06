# 🌿 A gentle intro to Git (optional, but handy)

**You do not need Git to do this project.** If you were given a link to a
**`.zip`** file, download it, unzip it, and skip straight back to
**[SETUP.md](SETUP.md)**. Everything works.

This page is for when you're curious *what that "git" word keeps meaning* — and
for one genuinely useful trick it unlocks (peeking at the finished answer). It's
written assuming you've never used it. No prior coding needed.

---

## What is Git, really? 🕹️

Think of a video game with **save points**.

You play for a while, then you save. If you then do something disastrous — fall
off a cliff, delete the wrong thing — you reload the last save and you're fine.
You can even keep **several** saves and jump between them.

**Git is save points for a folder of files.** You work on your project, and
every so often you tell Git "save the state of everything right now." Git
remembers it forever. Later you can:

- see **exactly what changed** and when,
- **go back** to any earlier save if you break something,
- keep **parallel versions** ("what if I tried it this other way?") without
  copying the whole folder into `project-v2-final-FINAL-real`.

A single save point is called a **commit**. That's the one bit of jargon worth
knowing.

## And GitHub? ☁️

**Git** is the tool that runs on your computer. **GitHub** is a *website* that
stores a copy of a Git project online — like Google Drive, but built for code.

It's how you'd get a project **onto** your machine from someone else, back your
work **up**, or share it. This project lives on GitHub; the `.zip` you may have
been given is just a snapshot of it with the Git bits stripped out.

---

## Why you might want it *for this project* 🎯

One reason, mainly: **there's a finished, working version you can peek at.**

The project comes in two versions living side by side, called **branches**:

- **`main`** — the skeleton. This is *your* copy, the one you build up.
- **`solution`** — the complete, working answer.

If you got the project **with Git** (see below), you can flip to the answer,
read how it's done, then flip back to your own work — without losing anything:

```bash
git switch solution   # look at the finished version
git switch main       # back to your own work
```

If you got the **`.zip`** instead, you just have `main` — that's totally fine.
(You can always grab the Git version later if you want the solution branch.)

---

## Getting the project *with* Git (instead of the zip)

Only do this if you'd rather use Git than the zip. Otherwise, skip it.

### 1. Install Git

- **🪟 Windows** — download and run the installer from
  <https://git-scm.com/download/win>. Click **Next** through all the defaults.
- **🍎 macOS** — open **Terminal** and type `git --version`. If Git isn't there,
  macOS offers to install it for you — say yes. (Or get it from
  <https://git-scm.com/download/mac>.)

Check it worked — open a fresh terminal and run:

```bash
git --version
```

You should see something like `git version 2.43.0`.

### 2. Copy the project onto your computer

The word for "download a Git project" is **clone**. You'll have been given a
link ending in `.git`:

```bash
git clone <the-repo-link-you-were-given>
cd finance-dashboard-workexp
```

That's it — you now have the folder, same as unzipping, but Git-aware. Carry on
with **[SETUP.md](SETUP.md)** from step 2.

---

## The five commands that cover 90% of it 🧰

You honestly don't need these for this project. But if you want to make your own
save points, here they are. Run them **inside the project folder**.

| I want to… | Command | Plain English |
| ---------- | ------- | ------------- |
| See what I've changed | `git status` | "What's different since my last save?" |
| Save a checkpoint | `git add -A` then `git commit -m "message"` | "Save everything, with a note about what I did" |
| See my past saves | `git log --oneline` | "List my save points" |
| Switch version | `git switch <name>` | "Jump to `main` or `solution`" |
| Undo un-saved changes to a file | `git restore <file>` | "Reload this file from my last save" |

> 💡 The `-m "message"` is a short note to your future self — like naming a save
> slot. Write what you did: `git commit -m "added the search box"`.

A typical loop looks like: change some code → `git status` to see what moved →
`git add -A` → `git commit -m "what I did"`. Repeat whenever you reach a bit that
works.

---

## Wait, I broke everything 😱

Two escape hatches:

- **Undo changes to one file** (since your last commit):
  `git restore path/to/file.py`
- **You made commits and want to see an older one:** `git log --oneline` to find
  it, then `git switch --detach <the-code-beside-it>` to look. `git switch main`
  brings you home.

And the oldest trick in the book: if it's really tangled and you have the `.zip`,
you can always unzip a fresh copy and start that file again. No shame in it.

---

## The whole thing in one breath

> Git = save points for your project. A save is a **commit**. **GitHub** is those
> saves stored online. You **don't need any of it here** — the `.zip` works —
> but with Git you can `git switch solution` to peek at the finished answer.

Now go build something → **[SETUP.md](SETUP.md)**.
