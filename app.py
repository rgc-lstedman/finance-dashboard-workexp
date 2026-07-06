"""
🔎 Stock Screener — starter skeleton
====================================

A "screener" looks at lots of stocks at once — one row per company — and lets you
filter, sort and search to find the interesting ones. Then you can pick one and
look at its price chart.

Right now this file just downloads the stocks and shows the table. Your job,
following docs/SPEC.md, is to add the filtering, sorting and the single-stock view.

Run it with:

    uv run streamlit run app.py

Every time you save this file, go to the browser and click "Rerun" (top-right).
Look for the  # TODO (Stage N)  comments — they mark where each stage goes.
"""

import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Screener", page_icon="🔎", layout="wide")
st.title("🔎 Stock Screener")
st.write("A work-experience project. Follow docs/SPEC.md to build me up!")


# ---------------------------------------------------------------------------
# The list of stocks our screener looks at. Ticker -> company name.
# Want different companies? Add or remove lines here (it's just a dictionary).
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


# ---------------------------------------------------------------------------
# This function downloads every stock in one go and builds a summary table:
# one row per company, with the numbers a screener cares about.
# You don't need to change it — you build your screener on top of it.
#
# @st.cache_data means the download only happens once (not every time you move a
# slider), so the app stays fast.
# ---------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_universe(period):
    # Downloading a LIST of tickers gives "multi-level" columns, so raw["Close"]
    # is a table with one column per stock. (See guides 03 and 05.)
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
        "Change %": (close.iloc[-1] / close.iloc[0] - 1) * 100,      # over the whole period
        "Day %": (close.iloc[-1] / prev_close - 1) * 100,            # most recent day
        "Avg Volume": volume.mean(),
        "Volatility %": daily_returns.std() * 100,                   # how bumpy the price is
    })
    summary.index.name = "Ticker"
    return summary.dropna(subset=["Price"]).round(2)


# Stage 2 (TODO): let the user choose the period with st.sidebar.selectbox(...)
period = "6mo"

data = load_universe(period)
if data.empty:
    st.error("Couldn't load market data. Check your internet connection and refresh.")
    st.stop()

# Stage 3 (TODO): add filters (search box / min Change % / min Avg Volume) that
#                 narrow `data` down before it is shown below.

# Stage 4 (TODO): sort the table by a column the user picks (data.sort_values(...)).

# Stage 5 (TODO): let the user pick one stock and show its price chart, e.g.
#   choice = st.selectbox("Pick a stock", data.index)
#   one = yf.download(choice, period=period, auto_adjust=True,
#                     multi_level_index=False, progress=False)
#   st.line_chart(one["Close"])

st.subheader(f"{len(data)} stocks")
st.dataframe(data, width="stretch")
