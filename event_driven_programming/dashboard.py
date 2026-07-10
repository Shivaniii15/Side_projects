import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# path to the SQLite database (same as in file_monitor.py)
DB_PATH = Path.home() / "file_monitor_log.db"

st.set_page_config(page_title="File Monitor Dashboard", layout="wide")

st.title("📊 File Monitor Dashboard")

# Connect to database
conn = sqlite3.connect(DB_PATH)

# load data
df = pd.read_sql_query("SELECT * FROM file_log ORDER BY processed_at DESC", conn)

conn.close()

# if no data
if df.empty:
    st.warning("No files processed yet.")
else:
    # --- metrics ---
    total_files = len(df)
    pdf_count = len(df[df["file_type"] == ".pdf"])
    csv_count = len(df[df["file_type"] == ".csv"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Files", total_files)
    col2.metric("PDF Files", pdf_count)
    col3.metric("CSV Files", csv_count)

    st.divider()

    # --- recent files table ---
    st.subheader("📁 Recent Files Processed")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # --- file type breakdown ---
    st.subheader("📊 File Type Breakdown")
    type_counts = df["file_type"].value_counts()
    st.bar_chart(type_counts)