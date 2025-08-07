import streamlit as st
import os
from pathlib import Path
from utils.edit import (
    load_file,
    preview_data,
    show_basic_stats,
    show_info,
    show_missing_values
)

st.title("🧼 Data Upload & Cleaning")

if "df" not in st.session_state:
    st.session_state.df = None

uploaded_file = st.file_uploader("📁 Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    file_name = uploaded_file.name
    file_ext = os.path.splitext(file_name)[1].lower()
    save_path = Path("uploads") / file_name
    save_path.parent.mkdir(exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state.df = load_file(str(save_path))
    st.success("✅ File uploaded successfully")

if st.session_state.df is not None:
    df = st.session_state.df

    preview_data(df)
    show_basic_stats(df)
    show_info(df)
    show_missing_values(df)
