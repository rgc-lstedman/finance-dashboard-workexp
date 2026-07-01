"""
🔎 Stock Screener — worked solution
===================================

One complete version of the screener described in docs/SPEC.md. It's here so you
can compare after having a go — there's no single "right" answer, and yours might
look different and still be great.

Run it with:

    uv run streamlit run app.py

It covers every stage in docs/SPEC.md (universe table → period → filters → sort →
single-stock view) plus a couple of stretch goals (moving average).
"""

import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Screener", page_icon="🔎", layout="wide")
st.title("🔎 Stock Screener")


# ---------------------------------------------------------------------------
# The stocks our screener looks at. Ticker -> company name. Add your own!
# ---------------------------------------------------------------------------
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
    """Download every stock once and build a one-row-per-stock summary table."""
    # A LIST of tickers -> multi-level columns, so raw["Close"] is a table with
    # one column per stock.
    raw = yf.download(list(UNIVERSE), period=period, auto_adjust=True, progress=False)
    close = raw["Close"]
    volume = raw["Volume"]
    if close.empty:
        return pd.DataFrame()  # nothing came back (e.g. no internet)

    daily_returns = close.pct_change()
    prev_close = close.iloc[-2] if len(close) >= 2 else close.iloc[-1]

    summary = pd.DataFrame({
        "Name": pd.Series(UNIVERSE),
        "Price": close.iloc[-1],
        "Change %": (close.iloc[-1] / close.iloc[0] - 1) * 100,
        "Day %": (close.iloc[-1] / prev_close - 1) * 100,
        "Avg Volume": volume.mean(),
        "Volatility %": daily_returns.std() * 100,
    })
    summary.index.name = "Ticker"
    return summary.dropna(subset=["Price"]).round(2)


@st.cache_data(ttl=3600)
def load_one(ticker, period):
    """Download a single stock's price history (flat columns, so ['Close'] is one column)."""
    return yf.download(
        ticker, period=period, auto_adjust=True, multi_level_index=False, progress=False
    )


# ---------------------------------------------------------------------------
# Stage 2 — controls
# ---------------------------------------------------------------------------
st.sidebar.header("Screener")
period = st.sidebar.selectbox("History period", ["1mo", "6mo", "1y"], index=1)
data = load_universe(period)

if data.empty:
    st.error("Couldn't load market data. Check your internet connection and refresh.")
    st.stop()

# ---------------------------------------------------------------------------
# Stage 3 — filters (build up a filtered copy called `view`)
# ---------------------------------------------------------------------------
search = st.sidebar.text_input("Search ticker or name").strip().upper()
min_change = st.sidebar.slider("Min change % over period", -50, 50, -50)
min_volume_m = st.sidebar.slider("Min avg volume (millions)", 0, 100, 0)

view = data.copy()
if search:
    view = view[view.index.str.contains(search) | view["Name"].str.upper().str.contains(search)]
view = view[view["Change %"] >= min_change]
view = view[view["Avg Volume"] >= min_volume_m * 1_000_000]

# ---------------------------------------------------------------------------
# Stage 4 — sort / rank
# ---------------------------------------------------------------------------
sort_col = st.sidebar.selectbox(
    "Sort by", ["Change %", "Day %", "Price", "Avg Volume", "Volatility %"]
)
view = view.sort_values(sort_col, ascending=False)

# ---------------------------------------------------------------------------
# The screener table
# ---------------------------------------------------------------------------
st.subheader(f"{len(view)} of {len(data)} stocks match")
st.dataframe(view, width="stretch")

# ---------------------------------------------------------------------------
# Stage 5 — look at one stock
# ---------------------------------------------------------------------------
st.subheader("📈 Look at one stock")
if len(view) == 0:
    st.info("No stocks match your filters — loosen them in the sidebar.")
else:
    choice = st.selectbox(
        "Pick a stock", view.index, format_func=lambda t: f"{t} — {data.loc[t, 'Name']}"
    )
    one = load_one(choice, period)
    if one.empty:
        st.error(f"Couldn't load price history for {choice}.")
    else:
        close = one["Close"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Latest", f"${close.iloc[-1]:,.2f}", f"{data.loc[choice, 'Change %']:+.2f}% over period")
        c2.metric("Period high", f"${close.max():,.2f}")
        c3.metric("Period low", f"${close.min():,.2f}")

        chart = pd.DataFrame({"Close": close})
        if st.checkbox("Add a 20-day moving average"):
            chart["MA20"] = close.rolling(20).mean()
        st.line_chart(chart)
