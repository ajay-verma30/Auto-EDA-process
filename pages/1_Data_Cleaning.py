import streamlit as st
import os
from pathlib import Path
import pandas as pd
from utils.edit import (
    load_file,
    preview_data,
    show_basic_stats,
    show_info,
    show_missing_values,
    show_duplicates,
    show_outliers,
    show_data_standardization
)
from utils.eda_process import eda_section

st.title("🧼 Data Upload & Cleaning")

if "df" not in st.session_state:
    st.session_state.df = None

if st.session_state.df is None:
    uploaded_file = st.file_uploader("📁 Upload your CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        file_name = uploaded_file.name
        save_path = Path("uploads") / file_name
        save_path.parent.mkdir(exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.df = load_file(str(save_path))
        if st.session_state.df is not None:
            st.success("✅ File uploaded successfully")
            st.rerun()

    st.info("Please upload a file to begin.")

else:
    df = st.session_state.df

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Data Overview",
        "Missing Values",
        "Duplicates",
        "Standardize Data",
        "Outliers",
        "Export"
    ])

    with tab1:
        preview_data(df)
        show_basic_stats(df)
        show_info(df)

    with tab2:
        show_missing_values(df)

    with tab3:
        show_duplicates(df)

    with tab4:
        show_data_standardization(df)

    with tab5:
        show_outliers(df)
    
    with tab6:

        st.subheader("### Export Cleaned Data")
        
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
        
        csv = convert_df(st.session_state.df)
        st.download_button(
            label="📥 Download Cleaned Data as CSV",
            data=csv,
            file_name='cleaned_data.csv',
            mime='text/csv',
            use_container_width=True
        )
