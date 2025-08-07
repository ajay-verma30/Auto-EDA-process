import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}. Please check your secrets.toml file.")
    st.stop()

def get_gemini_text_model():
    """Finds and returns the name of an available text-based model."""
    try:
        for model_info in genai.list_models():
            if 'generateContent' in model_info.supported_generation_methods:
                if 'vision' not in model_info.supported_generation_methods:
                    st.success(f"Using available text model: {model_info.name}")
                    return model_info.name
        return None
    except Exception as e:
        st.error(f"An error occurred while listing models: {e}")
        return None

gemini_text_model_name = get_gemini_text_model()
gemini_text_model = None
if gemini_text_model_name:
    gemini_text_model = genai.GenerativeModel(gemini_text_model_name)
else:
    st.error("No compatible text model found. AI analysis will be disabled.")

@st.cache_data
def analyze_data_with_gemini(plot_type, data_description):
    """
    Analyzes data and summary statistics using the Gemini text model.
    """
    if not gemini_text_model:
        return "Gemini AI analysis is disabled because a compatible model was not found."

    try:
        prompt = f"""
        You are an expert data analyst. Based on the following plot type and data,
        provide a concise summary of the key insights in 5 lines or less.
        
        Plot Type: {plot_type}
        Data Description:
        {data_description}
        """
        response = gemini_text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while analyzing the data: {e}"

@st.cache_data
def generate_overall_eda_summary(df):
    """Generates an overall EDA summary for the entire dataset using Gemini."""
    if not gemini_text_model:
        return "Gemini AI analysis is disabled, cannot generate overall summary."

    try:
        data_info = f"Dataset Shape: {df.shape}\n"
        data_info += f"Data Types:\n{df.dtypes.to_string()}\n\n"
        data_info += f"Numeric Column Statistics:\n{df.select_dtypes(include=['number']).describe().to_string()}\n\n"
        data_info += f"Categorical Column Value Counts (Top 5 for each):\n"
        for col in df.select_dtypes(include=['object', 'category']).columns:
            data_info += f"- {col}:\n{df[col].value_counts().head(5).to_string()}\n"

        prompt = f"""
        You are an expert data analyst. Based on the following dataset information,
        provide a comprehensive Exploratory Data Analysis (EDA) summary.
        The summary should be around 250 words. Highlight key characteristics,
        distributions, potential issues (like missing values or outliers),
        and interesting relationships you observe.

        Dataset Information:
        {data_info}
        """
        response = gemini_text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating overall EDA summary: {e}"

@st.cache_data
def generate_plot(df_to_plot, col, plot_type):
    """
    Generates and returns a plot figure. This function is cached.
    """
    fig, ax = plt.subplots()
    
    if pd.api.types.is_numeric_dtype(df_to_plot[col]):
        if plot_type == 'Histogram':
            sns.histplot(df_to_plot[col].dropna(), kde=True, ax=ax)
            ax.set_title(f"Histogram of {col}")
        elif plot_type == 'Box Plot':
            sns.boxplot(x=df_to_plot[col].dropna(), ax=ax)
            ax.set_title(f"Boxplot of {col}")
        elif plot_type == 'Line Plot':
            df_to_plot[col].plot(ax=ax)
            ax.set_title(f"Line Plot of {col}")
    else: # Categorical
        if plot_type == 'Bar Chart':
            df_to_plot[col].value_counts().plot(kind='bar', ax=ax)
            ax.set_title(f"Bar Plot of {col}")
            plt.xticks(rotation=45, ha='right')
        elif plot_type == 'Pie Chart':
            value_counts = df_to_plot[col].value_counts()
            if len(value_counts) > 10:
                 value_counts = value_counts.head(10)
            ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Pie Chart of {col}")
            ax.axis('equal')

    plt.tight_layout()
    return fig

@st.cache_data
def generate_bivariate_plot(df_to_plot, x_axis, y_axis, plot_type):
    """
    Generates and returns a bivariate plot figure. This function is cached.
    """
    fig, ax = plt.subplots()
    if plot_type == 'Scatter Plot':
        sns.scatterplot(data=df_to_plot, x=x_axis, y=y_axis, ax=ax)
        ax.set_title(f"Scatter Plot of {x_axis} vs {y_axis}")
    elif plot_type == 'Correlation Heatmap':
        corr = df_to_plot.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
    
    plt.tight_layout()
    return fig

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Automated EDA Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln(5)

    def add_image_and_summary(self, image_path, summary):
        if os.path.exists(image_path):
            try:
                img_width = self.w - 2*self.l_margin
                img_height = Image.open(image_path).height * img_width / Image.open(image_path).width
                
                if self.get_y() + img_height + 20 > self.h - self.b_margin:
                    self.add_page()

                self.image(image_path, x=self.l_margin, w=img_width)
                self.ln(5)
                self.set_font('Arial', 'I', 9)
                self.multi_cell(0, 5, "AI Summary: " + summary)
                self.ln(10)
            except Exception as e:
                self.set_font('Arial', '', 10)
                self.multi_cell(0, 5, f"Error adding image {os.path.basename(image_path)}: {e}")
                self.ln(5)
        else:
            self.set_font('Arial', '', 10)
            self.multi_cell(0, 5, f"Image not found: {os.path.basename(image_path)}")
            self.ln(5)

def create_pdf_report(df, overall_summary, plot_data_for_report):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.chapter_title("Overall Data Summary")
    pdf.chapter_body(overall_summary)
    pdf.add_page()

    pdf.chapter_title("Individual Graph Analysis")
    for plot_info in plot_data_for_report:
        pdf.add_image_and_summary(plot_info['path'], plot_info['summary'])

    return pdf.output(dest='S').encode('latin1')

def eda_section(df):
    if not os.path.exists("Figures"):
        os.makedirs("Figures")
    
    if 'overall_eda_summary' not in st.session_state:
        st.session_state.overall_eda_summary = None
    if 'plot_summaries_and_paths' not in st.session_state:
        st.session_state.plot_summaries_and_paths = {}

    st.subheader("📊 Dataset Overview")
    st.write("**Shape:**", df.shape)
    st.write("**Data Types:**")
    st.write(df.dtypes)
    st.markdown("---")

    st.subheader("⚙️ Performance Options")
    sample_size = st.slider(
        "Select sample size for plotting (to improve performance)",
        min_value=1000,
        max_value=min(len(df), 20000),
        value=min(len(df), 5000),
        step=500
    )
    df_sampled = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
    st.markdown("---")

    st.subheader("📈 Univariate Analysis")
    selected_col = st.selectbox("🔍 Select a column to analyze", df.columns, key="univariate_col")

    plot_key = f"{selected_col}_univariate_plot"
    fig_path = f"Figures/{plot_key}.png"

    if pd.api.types.is_numeric_dtype(df[selected_col]) or pd.api.types.is_categorical_dtype(df[selected_col]):
        if pd.api.types.is_numeric_dtype(df[selected_col]):
            st.write(f"**Summary statistics for `{selected_col}`**")
            st.write(df[selected_col].describe())
            plot_type = st.radio("Select a plot type:", ('Histogram', 'Box Plot', 'Line Plot'), key="numeric_plot_type")
        else:
            st.write(f"**Value counts for `{selected_col}`**")
            st.write(df[selected_col].value_counts())
            plot_type = st.radio("Select a plot type:", ('Bar Chart', 'Pie Chart'), key="categorical_plot_type")
        
        fig = generate_plot(df_sampled, selected_col, plot_type)
        fig.savefig(fig_path)
        st.pyplot(fig)
        plt.close(fig)

        if st.button(f"Generate AI Summary for {plot_type}", key=f"ai_univariate_button_{plot_key}"):
            with st.spinner("Generating summary..."):
                if pd.api.types.is_numeric_dtype(df[selected_col]):
                    data_description = f"Column Name: {selected_col}\nPlot Type: {plot_type}\nSummary Statistics:\n{df[selected_col].describe().to_string()}"
                else:
                    data_description = f"Column Name: {selected_col}\nPlot Type: {plot_type}\nValue Counts:\n{df[selected_col].value_counts().to_string()}"
                
                ai_text = analyze_data_with_gemini(plot_type, data_description)
                st.session_state.plot_summaries_and_paths[plot_key] = {'path': fig_path, 'summary': ai_text}
                st.rerun()

        if plot_key in st.session_state.plot_summaries_and_paths:
            st.markdown("### AI-Powered Insights for Current Plot")
            st.info(st.session_state.plot_summaries_and_paths[plot_key]['summary'])
            
    st.markdown("---")

    numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()

    if len(numeric_cols) >= 2:
        st.subheader("📊 Bivariate & Correlation Analysis")
        bivariate_plot_type = st.selectbox("Select a bivariate plot type:", ('Scatter Plot', 'Correlation Heatmap'), key="bivariate_plot_type")
        bivariate_plot_key = f"bivariate_{bivariate_plot_type.replace(' ', '_').lower()}"
        fig_path = f"Figures/{bivariate_plot_key}.png"

        if bivariate_plot_type == 'Scatter Plot':
            st.write("### Scatter Plot")
            x_axis = st.selectbox("Select X-axis", numeric_cols, key="x_axis")
            y_axis_options = [col for col in numeric_cols if col != x_axis]
            y_axis = st.selectbox("Select Y-axis", y_axis_options, key="y_axis")

            if x_axis and y_axis:
                fig = generate_bivariate_plot(df_sampled, x_axis, y_axis, bivariate_plot_type)
                fig.savefig(fig_path)
                st.pyplot(fig)
                plt.close(fig)

                if st.button("Generate AI Summary for this Scatter Plot", key=f"ai_scatter_button"):
                    with st.spinner("Generating summary..."):
                        data_description = f"Scatter Plot of {x_axis} vs {y_axis}. Correlation: {df[[x_axis, y_axis]].corr().iloc[0, 1]:.2f}"
                        ai_text = analyze_data_with_gemini("Scatter Plot", data_description)
                        st.session_state.plot_summaries_and_paths[bivariate_plot_key] = {'path': fig_path, 'summary': ai_text}
                        st.rerun()
                
                if bivariate_plot_key in st.session_state.plot_summaries_and_paths:
                    st.markdown("### AI-Powered Insights for Current Plot")
                    st.info(st.session_state.plot_summaries_and_paths[bivariate_plot_key]['summary'])
        
        elif bivariate_plot_type == 'Correlation Heatmap':
            st.write("### Correlation Heatmap")
            fig = generate_bivariate_plot(df, None, None, bivariate_plot_type)
            fig.savefig(fig_path)
            st.pyplot(fig)
            plt.close(fig)
            
            if st.button("Generate AI Summary for this Correlation Heatmap", key=f"ai_correlation_button"):
                with st.spinner("Generating summary..."):
                    corr_description = f"Correlation Matrix:\n{df[numeric_cols].corr(numeric_only=True).to_string()}"
                    ai_text = analyze_data_with_gemini("Correlation Heatmap", corr_description)
                    st.session_state.plot_summaries_and_paths[bivariate_plot_key] = {'path': fig_path, 'summary': ai_text}
                    st.rerun()
            
            if bivariate_plot_key in st.session_state.plot_summaries_and_paths:
                st.markdown("### AI-Powered Insights for Current Plot")
                st.info(st.session_state.plot_summaries_and_paths[bivariate_plot_key]['summary'])
            
    else:
        st.subheader("🔗 Correlation Matrix")
        st.info("❗ Not enough numeric columns to compute correlation.")

    st.markdown("---")
    st.subheader("📄 Generate Full EDA Report")

    if st.button("Generate Overall EDA Summary", key="generate_overall_summary"):
        with st.spinner("Generating overall summary..."):
            st.session_state.overall_eda_summary = generate_overall_eda_summary(df)
            st.rerun()
    
    if st.session_state.overall_eda_summary:
        st.markdown("### Overall EDA Summary (AI-Generated)")
        st.info(st.session_state.overall_eda_summary)
        
        plot_data_for_report = []
        for key, value in st.session_state.plot_summaries_and_paths.items():
            if value['summary']:
                plot_data_for_report.append(value)

        if plot_data_for_report:
            if st.button("Download Full PDF Report", key="download_pdf_report"):
                with st.spinner("Generating PDF report..."):
                    pdf_output = create_pdf_report(df, st.session_state.overall_eda_summary, plot_data_for_report)
                    st.download_button(
                        label="Click to Download PDF",
                        data=pdf_output,
                        file_name="eda_report.pdf",
                        mime="application/pdf"
                    )
        else:
            st.warning("Generate individual plot summaries first to include them in the PDF report.")