import pandas as pd
import streamlit as st
import os
import numpy as np

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Data Overview"

def set_active_tab(tab_name):
    st.session_state.active_tab = tab_name

def load_file(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding="ISO-8859-1")
                except UnicodeDecodeError:
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
        st.info("Once done, move to the EDA page")
        return

    st.dataframe(missing_df.sort_values(by="% Missing", ascending=False))

    st.markdown("### 🔧 Handle Missing Values")
    method = st.selectbox(
        "Select a method",
        [
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
        ],
        key="missing_method_select"  # ✅ unique key
    )

    selected_cols = st.multiselect(
        "Select columns to apply",
        options=df.columns[df.isnull().any()],
        default=df.columns[df.isnull().any()],
        key="missing_cols_multiselect"  # ✅ unique key
    )

    constant = None
    if method == "Fill with Constant value":
        constant = st.text_input("Enter constant value:", key="missing_constant_input")  # ✅ unique key

    if st.button("Apply", key="apply_missing_btn"):
        if method != "Drop rows with any missing value (entire row)" and not selected_cols:
            st.warning("⚠️ Please select at least one column.")
            return

        updated_df = df.copy()

        if method == "Drop rows with missing values (selected columns only)":
            updated_df.dropna(subset=selected_cols, inplace=True)
        elif method == "Drop rows with any missing value (entire row)":
            updated_df.dropna(inplace=True)
        elif method == "Drop columns with missing values":
            updated_df.drop(columns=selected_cols, inplace=True)
        elif method == "Fill with Mean":
            for col in selected_cols:
                updated_df[col] = updated_df[col].fillna(updated_df[col].mean())
        elif method == "Fill with Median":
            for col in selected_cols:
                updated_df[col] = updated_df[col].fillna(updated_df[col].median())
        elif method == "Fill with Mode":
            for col in selected_cols:
                updated_df[col] = updated_df[col].fillna(updated_df[col].mode()[0])
        elif method == "Fill with Constant value":
            if constant is None or constant == "":
                st.warning("⚠️ Please enter a constant value.")
                return
            for col in selected_cols:
                updated_df[col] = updated_df[col].fillna(constant)
        elif method == "Forward Fill (ffill)":
            updated_df[selected_cols] = updated_df[selected_cols].fillna(method='ffill')
        elif method == "Backward Fill (bfill)":
            updated_df[selected_cols] = updated_df[selected_cols].fillna(method='bfill')
        elif method == "Interpolate":
            for col in selected_cols:
                updated_df[col] = updated_df[col].interpolate()

        st.session_state.df = updated_df
        st.success("✅ Missing value handling applied successfully.")


def show_duplicates(df):
    st.subheader("👥 Duplicated Rows")
    duplicates_count = df.duplicated().sum()

    if duplicates_count > 0:
        st.warning(f"⚠️ {duplicates_count} duplicate rows detected!")
        if st.button("Drop Duplicate Rows", key="drop_duplicates_btn"):
            st.session_state.df = df.drop_duplicates()
            st.success(f"✅ {duplicates_count} duplicate rows have been dropped.")
    else:
        st.success("✅ No duplicate rows detected in the dataset!")

def show_data_standardization(df):
    st.subheader("🔄 Data Standardization")
    text_cols = df.select_dtypes(include='object').columns.tolist()
    if text_cols:
        cols_to_clean = st.multiselect("Select text columns to clean:", options=text_cols, key="standardize_text_cols")
        if st.button("Convert to Lowercase", key="lower_case_btn") and cols_to_clean:
            for col in cols_to_clean:
                st.session_state.df[col] = st.session_state.df[col].str.lower()
            st.success("✅ Converted to lowercase.")

def show_outliers(df):
    st.subheader("📈 Outlier Detection & Handling")

    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df.copy()
    else:
        st.warning("⚠️ Please upload and clean the data first.")
        return

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.info("No numerical columns found.")
        return

    col_to_check = st.selectbox("Select a numerical column:", options=numeric_cols, key="outlier_col_select")

    if st.button("Detect Outliers", key="detect_outliers_btn"):
        Q1 = df[col_to_check].quantile(0.25)
        Q3 = df[col_to_check].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = float(Q1 - 1.5 * IQR)
        upper_bound = float(Q3 + 1.5 * IQR)
        outliers = df[(df[col_to_check] < lower_bound) | (df[col_to_check] > upper_bound)]
        st.session_state["outlier_info"] = {
            "col": col_to_check,
            "lb": lower_bound,
            "ub": upper_bound,
            "count": int(len(outliers))
        }
        st.session_state.active_tab = "Outliers"  

    if "outlier_info" in st.session_state and st.session_state["outlier_info"].get("col") == col_to_check:
        info = st.session_state["outlier_info"]
        st.warning(f"⚠️ {info['count']} outliers detected in `{col_to_check}`.")
        outliers = df[(df[col_to_check] < info['lb']) | (df[col_to_check] > info['ub'])]
        st.dataframe(outliers)

    option = st.selectbox("Select an action:", ["Remove Outliers", "Cap Outliers"], key="outlier_action")

    if st.button("Apply Outlier Handling", key="apply_outlier_btn"):
        Q1 = df[col_to_check].quantile(0.25)
        Q3 = df[col_to_check].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        updated_df = df.copy()
        if option == "Remove Outliers":
            updated_df = updated_df[(updated_df[col_to_check] >= lower_bound) & (updated_df[col_to_check] <= upper_bound)]
        elif option == "Cap Outliers":
            updated_df[col_to_check] = np.where(updated_df[col_to_check] > upper_bound, upper_bound, updated_df[col_to_check])
            updated_df[col_to_check] = np.where(updated_df[col_to_check] < lower_bound, lower_bound, updated_df[col_to_check])

        st.session_state.df = updated_df
        st.success("✅ Outlier handling applied.")
        st.session_state.active_tab = "Outliers"


tabs = ["Data Overview", "Missing Values", "Duplicates", "Standardize", "Outliers"]
tab_objects = st.tabs(tabs)

for i, tab in enumerate(tab_objects):
    with tab:
        if tabs[i] == "Data Overview":
            if "df" in st.session_state:
                preview_data(st.session_state.df)
        elif tabs[i] == "Missing Values":
            if "df" in st.session_state:
                show_missing_values(st.session_state.df)
        elif tabs[i] == "Duplicates":
            if "df" in st.session_state:
                show_duplicates(st.session_state.df)
        elif tabs[i] == "Standardize":
            if "df" in st.session_state:
                show_data_standardization(st.session_state.df)
        elif tabs[i] == "Outliers":
            if "df" in st.session_state:
                show_outliers(st.session_state.df)