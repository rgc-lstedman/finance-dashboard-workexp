"""
📈 Finance Dashboard — starter skeleton
=======================================

This is the file you'll grow into a full dashboard. Right now it does the
minimum: it downloads data for one company and shows it in a table. Your job,
following SPEC.md, is to build it up stage by stage.

Run it with:

    uv run streamlit run app.py

Every time you save this file, go to the browser and click "Rerun" (top-right).

Look for the  # TODO (Stage N)  comments — they mark where each stage goes.
"""

import streamlit as st
import yfinance as yf

# ---------------------------------------------------------------------------
# Page setup — the title and browser-tab name. Change these to make it yours!
# ---------------------------------------------------------------------------
st.set_page_config(page_title="My Finance Dashboard", page_icon="📈")
st.title("📈 My Finance Dashboard")
st.write("A work-experience project. Follow SPEC.md to build me up!")


# ---------------------------------------------------------------------------
# Stage 2 (TODO): let the user choose the ticker and period.
# For now these are fixed. Replace them with st.text_input / st.selectbox.
# ---------------------------------------------------------------------------
ticker = "AAPL"
period = "6mo"


# ---------------------------------------------------------------------------
# Stage 1: download the data.
# `yf.download` returns a pandas DataFrame — a table of prices, one row per day.
#
# The extra options keep things simple for now:
#   auto_adjust=True        -> tidy prices, one "Close" column
#   multi_level_index=False -> plain column names (Open, High, Close ...) so that
#                              `data["Close"]` gives you a single column.
#   progress=False          -> no download bar cluttering the app
# (You'll meet the fancier "multi-level" columns later, when comparing two companies.)
# ---------------------------------------------------------------------------
st.subheader(f"Showing: {ticker}  (last {period})")

data = yf.download(
    ticker,
    period=period,
    auto_adjust=True,
    multi_level_index=False,
    progress=False,
)

if data.empty:
    st.error(f"No data found for '{ticker}'. Is the ticker spelled correctly?")
else:
    # Stage 3 (TODO): show headline numbers here with st.metric(...)

    # Stage 4 (TODO): add filters (checkbox / slider / date) that change `data`
    # before it's displayed below.

    # Stage 5 (TODO): draw a chart, e.g. st.line_chart(data["Close"])

    # Show the raw table (Stage 1). This already works.
    st.dataframe(data)
