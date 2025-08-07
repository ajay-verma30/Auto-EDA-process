import pandas as pd
import streamlit as st
import os
from utils.eda_process import eda_section


def load_file(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding="ISO-8859-1")
                except:
                    df = pd.read_csv(file_path, encoding="cp1252")
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported File Format.")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def preview_data(df):
    st.subheader("🧾 Data Preview")
    st.dataframe(df.head())
    st.markdown(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")


def show_basic_stats(df):
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())


def show_info(df):
    st.subheader("📋 Data Info")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.notnull().sum(),
        "Dtype": df.dtypes.astype(str)
    }).reset_index(drop=True)

    st.write(info_df)


def show_missing_values(df):
    st.subheader("🔍 Missing Values")

    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Column", "Missing Values"]
    missing_df["% Missing"] = (missing_df["Missing Values"] / len(df)) * 100
    missing_df = missing_df[missing_df["Missing Values"] > 0]

    if missing_df.empty:
        st.success("✅ No missing values detected in the dataset!")
        st.info("Once Done move to the EDA page")
        return

    st.dataframe(missing_df.sort_values(by="% Missing", ascending=False))

    st.markdown("### 🔧 Handle Missing Values")
    method = st.selectbox("Select a method", [
        "Drop rows with missing values (selected columns only)",
        "Drop rows with any missing value (entire row)",
        "Drop columns with missing values",
        "Fill with Mean",
        "Fill with Median",
        "Fill with Mode",
        "Fill with Constant value",
        "Forward Fill (ffill)",
        "Backward Fill (bfill)",
        "Interpolate"
    ])

    selected_cols = st.multiselect(
        "Select columns to apply",
        options=df.columns[df.isnull().any()],
        default=df.columns[df.isnull().any()]
    )

    constant = None
    if method == "Fill with Constant value":
        constant = st.text_input("Enter constant value:")

    if st.button("Apply", key="apply_missing_btn"):
        if method != "Drop rows with any missing value (entire row)" and not selected_cols:
            st.warning("⚠️ Please select at least one column.")
            return

        if method == "Drop rows with missing values (selected columns only)":
            df.dropna(subset=selected_cols, inplace=True)
            st.success("✅ Dropped rows with missing values in selected columns.")

        elif method == "Drop rows with any missing value (entire row)":
            df.dropna(inplace=True)
            st.success("✅ Dropped all rows that had any missing value.")

        elif method == "Drop columns with missing values":
            df.drop(columns=selected_cols, inplace=True)
            st.success("✅ Dropped selected columns with missing values.")

        elif method == "Fill with Mean":
            for col in selected_cols:
                df[col].fillna(df[col].mean(), inplace=True)
            st.success("✅ Filled selected columns with mean.")

        elif method == "Fill with Median":
            for col in selected_cols:
                df[col].fillna(df[col].median(), inplace=True)
            st.success("✅ Filled selected columns with median.")

        elif method == "Fill with Mode":
            for col in selected_cols:
                df[col].fillna(df[col].mode()[0], inplace=True)
            st.success("✅ Filled selected columns with mode.")

        elif method == "Fill with Constant value":
            if constant is None or constant == "":
                st.warning("⚠️ Please enter a constant value.")
                return
            for col in selected_cols:
                df[col].fillna(constant, inplace=True)
            st.success(f"✅ Filled selected columns with constant value: `{constant}`")

        elif method == "Forward Fill (ffill)":
            df[selected_cols] = df[selected_cols].fillna(method='ffill')
            st.success("✅ Forward filled selected columns.")

        elif method == "Backward Fill (bfill)":
            df[selected_cols] = df[selected_cols].fillna(method='bfill')
            st.success("✅ Backward filled selected columns.")

        elif method == "Interpolate":
            for col in selected_cols:
                df[col].interpolate(inplace=True)
            st.success("✅ Interpolated missing values in selected columns.")

        # Update session_state
        st.session_state.df = df

        # Preview
        st.markdown("---")
        st.subheader("📌 Updated Data Preview")
        st.dataframe(df.head())

        st.markdown("---")
        st.subheader("✅ Rechecking Missing Values After Handling")
        updated_missing_df = df.isnull().sum().reset_index()
        updated_missing_df.columns = ["Column", "Missing Values"]
        updated_missing_df["% Missing"] = (updated_missing_df["Missing Values"] / len(df)) * 100
        updated_missing_df = updated_missing_df[updated_missing_df["Missing Values"] > 0]

        if updated_missing_df.empty:
            st.success("✅ No missing values remain!")
            st.info("Go to the EDA analysis TAB once you are done")
        else:
            st.warning("⚠️ Still missing values exist.")
