# 🚀 Next steps — where to take this next

You've built a working screener. Here are ideas for making it better and for
learning more, roughly easiest first. **Pick whatever sounds fun** — there's no
order you have to follow, and you don't need anyone's permission to experiment.

> 💾 A good habit: before a big change, save a copy of your working `app.py`
> (or learn `git` — see the bottom). That way you can always get back to something
> that worked.

---

## 🟢 Quick wins

- **Add your own companies.** Edit the `UNIVERSE` dictionary at the top of
  `app.py` — add stocks you've heard of (`"UBER": "Uber"`, `"SPOT": "Spotify"`).
  Non-US stocks use a suffix, e.g. `"VOD.L"` (London), `"BMW.DE"` (Germany).
- **More filters.** Add a "max Volatility %" slider, or a checkbox for "only
  stocks that fell today" (`view = view[view["Day %"] < 0]`).
- **Colour the gains and losses.** Style the `Change %` column red/green with
  `st.dataframe(view.style.background_gradient(subset=["Change %"], cmap="RdYlGn"))`.
- **A download button.** Let the user save the filtered table:
  `st.download_button("Download CSV", view.to_csv().encode(), "screener.csv")`.
- **Best & worst of the day.** Use `.idxmax()` / `.idxmin()` on the `Day %`
  column and show the two names with `st.metric`.

## 🟡 Bigger features (an hour or two each)

- **A moving average on the stock chart.** Plot `one["Close"]` together with
  `one["Close"].rolling(20).mean()` so you can see the trend.
- **A candlestick chart.** Swap the line chart for a proper finance candlestick
  using `plotly` (already installed). Search "plotly candlestick" for the pattern.
- **Company fundamentals.** `yf.Ticker("AAPL").info` returns a big dictionary with
  things like `marketCap`, `trailingPE`, `sector`, `dividendYield`. Show a few for
  the stock you picked. (Heads-up: `.info` makes an extra network call per stock
  and can be slow or occasionally fail — fine for one stock at a time.)
- **Group by sector.** Add a sector to each stock in `UNIVERSE` and let the user
  filter by it, or show average `Change %` per sector.
- **A favourites / watchlist.** Let the user tick stocks to "watch" and keep the
  list between reruns using `st.session_state`.
- **Compare two stocks.** Let the user pick two tickers and draw both closing
  prices on one chart (remember: downloading a list gives multi-level columns).

## 🔴 Go further (a weekend project)

- **Put it on the internet.** Deploy your app for free with **Streamlit Community
  Cloud** (<https://streamlit.io/cloud>) so you can send friends a link. You'll
  push your code to GitHub and connect it — a great thing to have done.
- **A tiny portfolio simulator.** Let the user "buy" some shares of a few stocks
  and show what that would be worth now.
- **Backtest a simple rule.** e.g. "if the 20-day average crosses above the
  50-day average, that's a buy signal" — mark those days on the chart. (This is a
  real technique; keep it simple and don't trade real money on it!)
- **A first taste of machine learning.** These need one extra package —
  `uv add scikit-learn` (one time) — then `from sklearn... import ...`:
  - *Group similar stocks (clustering).* Let the computer sort your table into
    "types" of stock by how they behave — no labels needed:
    ```python
    from sklearn.cluster import KMeans

    # Pick the numbers that describe each stock's "behaviour" (its features).
    feats = data[["Change %", "Volatility %", "Avg Volume"]].dropna()

    # KMeans finds 3 clusters of stocks that look alike across those features.
    # n_clusters=3 = how many groups to make; n_init=10 = try 10 times, keep the best.
    # fit_predict returns which group (0, 1 or 2) each stock landed in.
    data.loc[feats.index, "Group"] = KMeans(n_clusters=3, n_init=10).fit_predict(feats)

    st.dataframe(data)  # each stock now has a Group 0/1/2 of similar ones
    ```
  - *Guess tomorrow's direction (classification).* Train a tiny model on one
    stock's daily returns to "predict" up vs down:
    ```python
    from sklearn.linear_model import LogisticRegression

    # Daily % change of the stock you picked (each day's return).
    r = load_one(choice, period)["Close"].pct_change().dropna()

    # Build the training data:
    #   X = today's return (the "feature" we learn from), for every day but the last.
    #   y = the answer we want: did the NEXT day go up? 1 = up, 0 = down.
    #       r.shift(-1) pulls tomorrow's return onto today's row so they line up.
    X, y = r[:-1].to_frame("today"), (r.shift(-1) > 0)[:-1].astype(int)

    # "Train" the model: it learns any link between today's move and tomorrow's.
    model = LogisticRegression().fit(X, y)

    # Ask it about the most recent day; predict_proba gives [P(down), P(up)] — take P(up).
    st.write(f"Guessed chance it rises next day: {model.predict_proba(r[-1:].to_frame('today'))[0][1]:.0%}")
    ```
    ⚠️ **This one is a toy.** One feature, tiny data, and markets are close to
    random day-to-day — expect roughly coin-flip accuracy. It's here to show *how*
    ML plugs in, **not** a way to make money. Never trade on it.

---

## 📚 Learn the ideas more deeply

- **Python** — the official beginner tutorial: <https://docs.python.org/3/tutorial/>
  and the friendly *Automate the Boring Stuff*: <https://automatetheboringstuff.com/>
- **pandas** — "10 minutes to pandas": <https://pandas.pydata.org/docs/user_guide/10min.html>
- **Streamlit** — the docs are excellent and full of examples: <https://docs.streamlit.io/>
- **yfinance** — what else you can download: <https://ranaroussi.github.io/yfinance/>
- **git & GitHub** — how programmers save and share code, and how you'd deploy the
  app above: <https://docs.github.com/en/get-started>

---

## 📈 More data & bigger toolkits

`yfinance` is a great, free starting point — but it's only one source. When you
want more (fundamentals, crypto, forex, economic data) or want to see how the
pros structure things, these curated lists point at almost everything worth
knowing:

- **awesome-quant** — a huge, well-kept list of libraries, data sources and tools
  for quantitative finance in Python (and other languages):
  <https://github.com/wilsonfreitas/awesome-quant>
- **Public APIs — Finance section** — free/freemium APIs for prices, company data
  and more: <https://github.com/public-apis/public-apis#finance>

And a few individual data sources you can actually pull from today:

- **Alpha Vantage** — free stock/forex/crypto API (grab a free key):
  <https://www.alphavantage.co/>
- **FRED** — the US Federal Reserve's economic data (rates, inflation, GDP), free:
  <https://fred.stlouisfed.org/>
- **Nasdaq Data Link** (formerly Quandl) — many free and paid datasets:
  <https://data.nasdaq.com/>
- **OpenBB** — a free, open-source "Bloomberg-lite" research platform you can
  drive from Python: <https://openbb.co/>

> 🔑 **Heads-up:** most of these want a free **API key** (a password that
> identifies your app), and free tiers have limits (e.g. X requests per minute).
> Read each one's "getting started" page. `yfinance` needs no key, which is why we
> start there.

---

## 🧠 A few things worth knowing

- **This data is delayed and free**, so it's great for learning but not for real
  trading decisions. Real firms pay for faster, cleaner data.
- **"Past performance doesn't predict the future."** A stock going up a lot
  recently doesn't mean it will keep going up. Screeners help you *look*, not
  *predict*.
- **The best way to learn is to build something you're curious about.** Change the
  code, break it, fix it. That loop is the whole job.

Have fun with it. 🎉
