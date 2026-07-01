# 🎈 Streamlit Cheat-Sheet

Streamlit turns a Python script into a web app. Scan for what you need.

```python
import streamlit as st
```

---

## Run it

```bash
uv run streamlit run app.py
```

It opens in your browser. **Every time you save `app.py`**, Streamlit notices
and shows a **"Rerun"** button (top-right) — click it (or turn on "Always rerun")
to see your change.

> 🔁 The whole script runs **top to bottom on every interaction**. There's no
> separate "setup" step — Streamlit re-runs the file each time.

---

## Page setup (once, at the top)

```python
st.set_page_config(page_title="My Dashboard", page_icon="📈")
```

---

## Text & output

| Call | Shows |
| ---- | ----- |
| `st.title("Hi")` | big page title |
| `st.header("Section")` | section heading |
| `st.subheader("Smaller")` | smaller heading |
| `st.write(anything)` | text, a number, a table, a chart — it figures it out |
| `st.markdown("**bold** and *italic*")` | formatted text |
| `st.dataframe(data)` | an interactive, scrollable table |
| `st.table(data)` | a plain static table |
| `st.metric("Close", 187.2, 1.5)` | a big number with an up/down delta |

```python
st.metric(label="Latest close", value=187.20, delta=1.5)   # green ▲ 1.5
st.metric(label="Latest close", value=120.00, delta=-3.0)  # red ▼ 3.0
```

---

## Inputs (widgets) — they return the current value

Each widget **returns whatever the user has chosen right now**. Store it in a
variable and use it.

```python
ticker = st.text_input("Ticker", value="AAPL")            # → the typed text
period = st.selectbox("Period", ["1mo", "6mo", "1y"])     # → the chosen option
choice = st.radio("Pick one", ["A", "B", "C"])            # → the chosen option
min_vol = st.slider("Min volume", 0, 100, 20)             # min, max, default
only_up = st.checkbox("Only up days")                     # → True / False
day = st.date_input("From date")                          # → a date
go = st.button("Run")                                     # → True only on click
```

| Widget | Returns |
| ------ | ------- |
| `st.text_input` | the text typed |
| `st.selectbox` | the one option chosen |
| `st.radio` | the one option chosen |
| `st.slider` | the number/position chosen |
| `st.checkbox` | `True` / `False` |
| `st.date_input` | a `date` |
| `st.button` | `True` on the run right after a click, else `False` |

---

## Layout

**Sidebar** — put controls on the left. Add `.sidebar` to any call:

```python
ticker = st.sidebar.text_input("Ticker", value="AAPL")
st.sidebar.header("Controls")
```

**Columns** — side by side. `st.columns(n)` gives you a list:

```python
c1, c2, c3 = st.columns(3)
c1.metric("Open", 185.6)
c2.metric("Close", 187.2)
c3.metric("Volume", "52M")
```

**Tabs:**

```python
tab1, tab2 = st.tabs(["Table", "Chart"])
tab1.dataframe(data)
tab2.line_chart(data["Close"])
```

**Expander** — a collapsible box:

```python
with st.expander("Show raw data"):
    st.dataframe(data)
```

---

## Charts

```python
st.line_chart(data["Close"])          # line
st.bar_chart(data["Volume"])          # bars
st.area_chart(data["Close"])          # filled line
```

Plot several columns at once by passing a small DataFrame:

```python
st.line_chart(data[["Open", "Close"]])
```

**Prettier charts with Plotly:**

```python
import plotly.express as px
fig = px.line(data, y="Close", title="Closing price")
st.plotly_chart(fig)
```

---

## Download a file

```python
st.download_button(
    label="Download CSV",
    data=data.to_csv(),
    file_name="prices.csv",
    mime="text/csv",
)
```

---

## Gotchas

| Trap | What's going on |
| ---- | --------------- |
| "My change didn't show" | save the file, then click **Rerun** in the browser |
| The script seems to run again on every click | it does — top to bottom, every interaction |
| `st.button` "forgets" it was clicked | it's `True` only on the run right after the click, not after |
| A widget's value looks stale | read it into a variable *after* you create the widget, then use that variable |
| Two widgets clash / "duplicate key" error | give them different labels, or add `key="something_unique"` |
