import streamlit as st
from utils.eda_process import eda_section

query_params = st.query_params

if query_params.get("page") == "eda":
    st.query_params.clear()

st.title("📈 Exploratory Data Analysis (EDA)")

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload and clean your dataset in the 🧼 Data Cleaning tab first.")
else:
    df = st.session_state.df
    eda_section(df)
