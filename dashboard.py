import streamlit as st
import pandas as pd

st.title("Portfolio Tracker")

# Load both CSVs
df = pd.read_csv("stock_data.csv")
summary_df = pd.read_csv("stock_summary.csv")

# Convert timestamps
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
summary_df["Timestamp"] = pd.to_datetime(summary_df["Timestamp"])

# -----------------------------
# CURRENT PORTFOLIO (latest run only)
# -----------------------------
latest_timestamp = df["Timestamp"].max()
latest_df = df[df["Timestamp"] == latest_timestamp].copy()

st.subheader("Current Portfolio")
st.caption(f"Last updated: {latest_timestamp.strftime('%d %b %Y, %H:%M')}")

# Colour the P/L column green/red
def colour_pnl(val):
    color = "green" if val > 0 else "red"
    return f"color: {color}"

st.dataframe(
    latest_df[["Stock", "Buy Price", "Current Price", "P/L"]]
    .style.map(colour_pnl, subset=["P/L"]),
    use_container_width=True
)

# Total P/L for latest run
total = latest_df["P/L"].sum()
st.metric(label="Total P/L (latest run)", value=f"${total:,.2f}")

# -----------------------------
# HISTORICAL TREND
# -----------------------------
st.subheader("Total P/L Over Time")
st.line_chart(summary_df.set_index("Timestamp")["Total P/L"])

# -----------------------------
# FULL HISTORY (collapsed, optional)
# -----------------------------
with st.expander("See full data history"):
    st.dataframe(df, use_container_width=True)