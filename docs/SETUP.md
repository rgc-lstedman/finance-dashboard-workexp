# 🛠️ Setup — get everything installed and running

This guide takes you from a **brand-new computer with no Python** to a running
finance dashboard.

We use a single tool called **`uv`** to do the hard work. `uv` installs the
right version of Python *for this project*, downloads the packages we need, and
runs our code — so you don't have to install Python separately or worry about
versions clashing with anything else on your machine.

Follow the section for **your** operating system, then everyone does the same
"Run the project" steps at the end.

---

## 0. What you need before you start

- A computer you can install software on (if it's a locked-down school or work
  laptop, whoever manages it may need to allow installs).
- An internet connection.

You do **not** need to install Python yourself — `uv` does that for you.

---

## 1. Get the project files

**The easy way — the zip:** you were given a link to download the project as a
**`.zip`**. Download it, then **unzip** it somewhere you'll find again — for
example your **Desktop** or **Documents** folder.

(You've probably already done this — it's how you're reading this file.)

You should end up with a folder called `finance-dashboard-workexp` containing
`README.md`, `app.py`, and the rest. That's all you need — carry on to step 2.

> 🌿 **Prefer to use Git?** You don't have to — the zip works perfectly. But if
> you know Git (or want to learn it), see **[GIT.md](GIT.md)**. Using Git also
> lets you peek at the finished `solution` version. If you're not sure what any
> of that means, ignore it and use the zip.

---

## 2. Install `uv`

### 🪟 Windows

1. Click the **Start** menu, type `PowerShell`, and open **Windows PowerShell**.
2. Copy-paste this line and press **Enter**:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. When it finishes, **close PowerShell and open it again** (this makes the new
   `uv` command available).
4. Check it worked:

   ```powershell
   uv --version
   ```

   You should see something like `uv 0.10.7`. If you get "not recognised", close
   and reopen PowerShell once more, or restart your computer.

### 🍎 macOS

1. Open the **Terminal** app (press `Cmd + Space`, type `Terminal`, press Enter).
2. Copy-paste this line and press **Enter**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. When it finishes, **close Terminal and open it again**.
4. Check it worked:

   ```bash
   uv --version
   ```

   You should see something like `uv 0.10.7`.

> 📖 More detail / troubleshooting: <https://docs.astral.sh/uv/getting-started/installation/>

---

## 3. Open the project in a terminal

You need your terminal to be "inside" the project folder. The command is `cd`
("change directory"), followed by the path to the folder.

- **Windows (PowerShell):**

  ```powershell
  cd $HOME\Desktop\finance-dashboard-workexp
  ```

  (change `Desktop` if you put it somewhere else)

- **macOS (Terminal):**

  ```bash
  cd ~/Desktop/finance-dashboard-workexp
  ```

> 💡 **Tip:** on both systems you can type `cd ` (with a space) and then **drag
> the folder from your file explorer onto the terminal window** — it fills in
> the path for you. Then press Enter.

To check you're in the right place, list the files:

- Windows: `dir`
- macOS: `ls`

You should see `app.py` and `README.md` in the list.

---

## 4. Let `uv` set up Python and the packages

Run this **one** command from inside the project folder:

```bash
uv sync
```

The first time, this will:

- download the correct version of Python (defined in `.python-version`),
- create a private environment for this project (a `.venv` folder), and
- install `streamlit`, `yfinance`, `pandas` and the rest.

It might take a couple of minutes the first time. When it's done you'll get your
prompt back with no errors.

---

## 5. Run the screener 🎉

```bash
uv run streamlit run app.py
```

Your web browser should pop open at `http://localhost:8501` showing the
screener. If it doesn't open automatically, copy that address into your browser.

You now have a running app! It's only a skeleton for now — a table of stocks. The
rest of the project is about growing it into a real screener. Follow
**[guides/00-welcome.md](../guides/00-welcome.md)** (or the plan in
**[SCHEDULE.md](SCHEDULE.md)**) next.

To **stop** the app, go back to the terminal and press **`Ctrl + C`**.

---

## 6. Run the interactive lessons (notebooks)

The `notebooks/` folder has lessons you run bit-by-bit. To open them:

```bash
uv run jupyter lab
```

This opens Jupyter in your browser. Double-click a notebook in the `notebooks`
folder on the left to open it. (The guides tell you when to use each one.)

Stop Jupyter the same way — `Ctrl + C` in the terminal.

---

## Quick reference — the only commands you need

| I want to… | Command |
| ---------- | ------- |
| Set up the project (first time, and after new packages are added) | `uv sync` |
| Run the screener | `uv run streamlit run app.py` |
| Open the notebook lessons | `uv run jupyter lab` |
| Add a new package | `uv add <package-name>` |
| Stop a running app / notebook | `Ctrl + C` in the terminal |

---

## Something went wrong?

| Problem | Try this |
| ------- | -------- |
| `uv: command not found` / "not recognised" | Close the terminal and open a new one. Still failing? Restart the computer. |
| `uv sync` fails with a network error | Check your internet is working. On a locked-down school/work network a firewall or proxy may block it — try a different network (e.g. a home connection). |
| Browser didn't open | Manually visit `http://localhost:8501`. |
| "Port 8501 is already in use" | You already have the app running in another terminal. Close that one, or run `uv run streamlit run app.py --server.port 8502`. |
| Something else | Copy the **full** error text and search for it online — someone has almost certainly hit it before. Errors are clues, not failures. |
