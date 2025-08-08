import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Custom header styling */
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .custom-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .custom-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
        margin: 0;
    }
    
    /* Section headers */
    .section-header {
        background: #f8f9fa;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 2rem 0 1rem 0;
    }
    
    .section-header h3 {
        margin: 0;
        color: #333;
        font-size: 1.3rem;
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3e0;
        border: 1px solid #ffcc02;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"⚠️ Failed to configure Gemini API: {e}. Please check your secrets.toml file.")
    st.stop()

def get_gemini_text_model():
    """Finds and returns the name of an available text-based model."""
    try:
        for model_info in genai.list_models():
            if 'generateContent' in model_info.supported_generation_methods:
                if 'vision' not in model_info.supported_generation_methods:
                    st.success(f"✅ Using available text model: {model_info.name}")
                    return model_info.name
        return None
    except Exception as e:
        st.error(f"❌ An error occurred while listing models: {e}")
        return None

gemini_text_model_name = get_gemini_text_model()
gemini_text_model = None
if gemini_text_model_name:
    gemini_text_model = genai.GenerativeModel(gemini_text_model_name)
else:
    st.error("❌ No compatible text model found. AI analysis will be disabled.")

@st.cache_data
def analyze_data_with_gemini(plot_type, data_description):
    """Analyzes data and summary statistics using the Gemini text model."""
    if not gemini_text_model:
        return "🚫 Gemini AI analysis is disabled because a compatible model was not found."

    try:
        prompt = f"""
        You are an expert data analyst. Based on the following plot type and data,
        provide a concise summary of the key insights in 5 lines or less.
        Focus on actionable insights and patterns.
        
        Plot Type: {plot_type}
        Data Description:
        {data_description}
        """
        response = gemini_text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ An error occurred while analyzing the data: {e}"

@st.cache_data
def generate_overall_eda_summary(df):
    """Generates an overall EDA summary for the entire dataset using Gemini."""
    if not gemini_text_model:
        return "🚫 Gemini AI analysis is disabled, cannot generate overall summary."

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
        and interesting relationships you observe. Focus on actionable insights.

        Dataset Information:
        {data_info}
        """
        response = gemini_text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ An error occurred while generating overall EDA summary: {e}"

@st.cache_data
def generate_plot(df_to_plot, col, plot_type):
    """Generates and returns a plot figure with professional styling."""
    # Set professional matplotlib style
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Color palette
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    
    if pd.api.types.is_numeric_dtype(df_to_plot[col]):
        if plot_type == 'Histogram':
            sns.histplot(df_to_plot[col].dropna(), kde=True, ax=ax, color=colors[0], alpha=0.7)
            ax.set_title(f"Distribution of {col}", fontsize=16, fontweight='bold', pad=20)
        elif plot_type == 'Box Plot':
            sns.boxplot(x=df_to_plot[col].dropna(), ax=ax, color=colors[1])
            ax.set_title(f"Box Plot of {col}", fontsize=16, fontweight='bold', pad=20)
        elif plot_type == 'Line Plot':
            df_to_plot[col].plot(ax=ax, color=colors[2], linewidth=2)
            ax.set_title(f"Line Plot of {col}", fontsize=16, fontweight='bold', pad=20)
    else: # Categorical
        if plot_type == 'Bar Chart':
            value_counts = df_to_plot[col].value_counts()
            bars = ax.bar(range(len(value_counts)), value_counts.values, color=colors[:len(value_counts)])
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_title(f"Distribution of {col}", fontsize=16, fontweight='bold', pad=20)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom')
                       
        elif plot_type == 'Pie Chart':
            value_counts = df_to_plot[col].value_counts()
            if len(value_counts) > 10:
                 value_counts = value_counts.head(10)
            ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', 
                  startangle=90, colors=colors[:len(value_counts)])
            ax.set_title(f"Distribution of {col}", fontsize=16, fontweight='bold', pad=20)
            ax.axis('equal')

    # Professional styling
    ax.grid(True, alpha=0.3)
    ax.set_xlabel(ax.get_xlabel(), fontsize=12, fontweight='medium')
    ax.set_ylabel(ax.get_ylabel(), fontsize=12, fontweight='medium')
    
    plt.tight_layout()
    return fig

@st.cache_data
def generate_bivariate_plot(df_to_plot, x_axis, y_axis, plot_type):
    """Generates professional bivariate plots."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if plot_type == 'Scatter Plot':
        sns.scatterplot(data=df_to_plot, x=x_axis, y=y_axis, ax=ax, 
                       color='#667eea', alpha=0.6, s=50)
        ax.set_title(f"Relationship between {x_axis} and {y_axis}", 
                    fontsize=16, fontweight='bold', pad=20)
    elif plot_type == 'Correlation Heatmap':
        corr = df_to_plot.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", 
                   center=0, ax=ax, cbar_kws={"shrink": .8})
        ax.set_title("Correlation Matrix", fontsize=16, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.cell(0, 15, 'Professional EDA Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Generated by AI-Powered Data Analysis Tool', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 12, title, 0, 1, 'L')
        self.ln(3)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(8)

    def add_image_and_summary(self, image_path, summary):
        if os.path.exists(image_path):
            try:
                img_width = self.w - 2*self.l_margin
                img_height = Image.open(image_path).height * img_width / Image.open(image_path).width
                
                if self.get_y() + img_height + 25 > self.h - self.b_margin:
                    self.add_page()

                self.image(image_path, x=self.l_margin, w=img_width)
                self.ln(8)
                self.set_font('Arial', 'B', 10)
                self.cell(0, 6, "AI-Generated Insights:", 0, 1, 'L')
                self.set_font('Arial', '', 10)
                self.multi_cell(0, 5, summary)
                self.ln(12)
            except Exception as e:
                self.set_font('Arial', '', 10)
                self.multi_cell(0, 5, f"Error adding image {os.path.basename(image_path)}: {e}")
                self.ln(5)

def create_pdf_report(df, overall_summary, plot_data_for_report):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.chapter_title("Executive Summary")
    pdf.chapter_body(overall_summary)
    pdf.add_page()

    pdf.chapter_title("Detailed Analysis")
    for plot_info in plot_data_for_report:
        pdf.add_image_and_summary(plot_info['path'], plot_info['summary'])

    return pdf.output(dest='S').encode('latin1')

def display_dataset_overview(df):
    """Display professional dataset overview with metrics cards (fixed responsive layout)."""
    
    # Inject CSS once
    st.markdown("""
    <style>
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 0.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        height: 100%;
        width: 100%;
    }
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><h3>📊 Dataset Overview</h3></div>', unsafe_allow_html=True)
    
    # Calculate metrics
    total_rows = f"{df.shape[0]:,}"
    total_cols = df.shape[1]
    numeric_cols = len(df.select_dtypes(include=['number']).columns)
    categorical_cols = len(df.select_dtypes(include=['object', 'category']).columns)

    # Layout with 4 columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Rows</div>
            <div class="metric-value">{total_rows}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Columns</div>
            <div class="metric-value">{total_cols}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Numeric Columns</div>
            <div class="metric-value">{numeric_cols}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Categorical Columns</div>
            <div class="metric-value">{categorical_cols}</div>
        </div>
        """, unsafe_allow_html=True)

    # Extra details in expander
    with st.expander("📋 View Data Types", expanded=False):
        dtype_df = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.astype(str),
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum()
        })
        st.dataframe(dtype_df, use_container_width=True)


def eda_section(df):
    st.markdown("""
    <div class="custom-header">
        <p>AI-Powered Exploratory Data Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not os.path.exists("Figures"):
        os.makedirs("Figures")
    
    if 'overall_eda_summary' not in st.session_state:
        st.session_state.overall_eda_summary = None
    if 'plot_summaries_and_paths' not in st.session_state:
        st.session_state.plot_summaries_and_paths = {}

    display_dataset_overview(df)
    
    with st.sidebar:
        st.markdown("### ⚙️ Analysis Controls")
        sample_size = st.slider(
            "Sample Size (for performance)",
            min_value=min(100, len(df)),  # agar dataset chhota ho to safe
            max_value=len(df),
            value=min(len(df), 5000),
            step=500,
            help="Reduce sample size for faster plotting with large datasets"
        )   
        
        st.markdown("### 🎨 Visualization Theme")
        plot_style = st.selectbox(
            "Select plot style",
            ["Professional", "Minimal", "Dark"],
            help="Choose visualization theme"
        )
    
    df_sampled = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
    
    if sample_size < len(df):
        st.markdown(f"""
        <div class="info-box">
            ℹ️ <strong>Note:</strong> Using sample of {sample_size:,} rows out of {len(df):,} for better performance.
        </div>
        """, unsafe_allow_html=True)

    # Univariate Analysis Section
    st.markdown('<div class="section-header"><h3>📈 Univariate Analysis</h3></div>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_col = st.selectbox(
            "🔍 Select column for analysis",
            df.columns,
            key="univariate_col",
            help="Choose a column to analyze its distribution"
        )
    
    with col2:
        if pd.api.types.is_numeric_dtype(df[selected_col]):
            plot_type = st.selectbox(
                "📊 Plot Type",
                ('Histogram', 'Box Plot', 'Line Plot'),
                key="numeric_plot_type"
            )
        else:
            plot_type = st.selectbox(
                "📊 Plot Type",
                ('Bar Chart', 'Pie Chart'),
                key="categorical_plot_type"
            )

    plot_key = f"{selected_col}_{plot_type.replace(' ', '_').lower()}"
    fig_path = f"Figures/{plot_key}.png"

    # Display statistics
    col1, col2 = st.columns(2)
    
    if pd.api.types.is_numeric_dtype(df[selected_col]):
        with col1:
            st.markdown("**📊 Summary Statistics**")
            stats_df = df[selected_col].describe().round(3)
            st.dataframe(stats_df, use_container_width=True)
        
        with col2:
            st.markdown("**🎯 Key Metrics**")
            missing_pct = (df[selected_col].isnull().sum() / len(df)) * 100
            st.metric("Missing Values", f"{missing_pct:.1f}%")
            st.metric("Unique Values", df[selected_col].nunique())
            if df[selected_col].nunique() < len(df):
                st.metric("Most Common", df[selected_col].mode().iloc[0] if len(df[selected_col].mode()) > 0 else "N/A")
    else:
        with col1:
            st.markdown("**📊 Value Counts**")
            value_counts = df[selected_col].value_counts().head(10)
            st.dataframe(value_counts, use_container_width=True)
        
        with col2:
            st.markdown("**🎯 Key Metrics**")
            missing_pct = (df[selected_col].isnull().sum() / len(df)) * 100
            st.metric("Missing Values", f"{missing_pct:.1f}%")
            st.metric("Unique Values", df[selected_col].nunique())
            st.metric("Most Common", df[selected_col].mode().iloc[0] if len(df[selected_col].mode()) > 0 else "N/A")

    # Generate and display plot
    fig = generate_plot(df_sampled, selected_col, plot_type)
    fig.savefig(fig_path, dpi=300, bbox_inches='tight')
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # AI Analysis button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button(f"🤖 Generate AI Insights", key=f"ai_univariate_button_{plot_key}"):
            with st.spinner("🔄 Analyzing data..."):
                if pd.api.types.is_numeric_dtype(df[selected_col]):
                    data_description = f"Column: {selected_col}\nPlot: {plot_type}\nStats:\n{df[selected_col].describe().to_string()}"
                else:
                    data_description = f"Column: {selected_col}\nPlot: {plot_type}\nCounts:\n{df[selected_col].value_counts().to_string()}"
                
                ai_text = analyze_data_with_gemini(plot_type, data_description)
                st.session_state.plot_summaries_and_paths[plot_key] = {'path': fig_path, 'summary': ai_text}
                st.rerun()

    # Display AI insights
    if plot_key in st.session_state.plot_summaries_and_paths:
        st.markdown("""
        <div class="success-box">
            <h4>🤖 AI-Generated Insights</h4>
        </div>
        """, unsafe_allow_html=True)
        st.info(st.session_state.plot_summaries_and_paths[plot_key]['summary'])

    # Bivariate Analysis
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()

    if len(numeric_cols) >= 2:
        st.markdown('<div class="section-header"><h3>📊 Bivariate & Correlation Analysis</h3></div>', 
                    unsafe_allow_html=True)
        
        bivariate_plot_type = st.selectbox(
            "Select analysis type",
            ('Scatter Plot', 'Correlation Heatmap'),
            key="bivariate_plot_type",
            help="Choose the type of bivariate analysis"
        )
        
        bivariate_plot_key = f"bivariate_{bivariate_plot_type.replace(' ', '_').lower()}"
        fig_path = f"Figures/{bivariate_plot_key}.png"

        if bivariate_plot_type == 'Scatter Plot':
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("📊 X-axis variable", numeric_cols, key="x_axis")
            with col2:
                y_axis_options = [col for col in numeric_cols if col != x_axis]
                y_axis = st.selectbox("📊 Y-axis variable", y_axis_options, key="y_axis")

            if x_axis and y_axis:
                # Calculate correlation
                correlation = df[[x_axis, y_axis]].corr().iloc[0, 1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Correlation Coefficient", f"{correlation:.3f}")
                with col2:
                    corr_strength = "Strong" if abs(correlation) > 0.7 else "Moderate" if abs(correlation) > 0.3 else "Weak"
                    st.metric("Relationship Strength", corr_strength)
                with col3:
                    corr_direction = "Positive" if correlation > 0 else "Negative"
                    st.metric("Direction", corr_direction)
                
                fig = generate_bivariate_plot(df_sampled, x_axis, y_axis, bivariate_plot_type)
                fig.savefig(fig_path, dpi=300, bbox_inches='tight')
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                if st.button("🤖 Generate AI Insights", key="ai_scatter_button"):
                    with st.spinner("🔄 Analyzing relationship..."):
                        data_description = f"Scatter Plot: {x_axis} vs {y_axis}. Correlation: {correlation:.3f}"
                        ai_text = analyze_data_with_gemini("Scatter Plot", data_description)
                        st.session_state.plot_summaries_and_paths[bivariate_plot_key] = {
                            'path': fig_path, 'summary': ai_text
                        }
                        st.rerun()
        
        elif bivariate_plot_type == 'Correlation Heatmap':
            fig = generate_bivariate_plot(df, None, None, bivariate_plot_type)
            fig.savefig(fig_path, dpi=300, bbox_inches='tight')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            
            if st.button("🤖 Generate AI Insights", key="ai_correlation_button"):
                with st.spinner("🔄 Analyzing correlations..."):
                    corr_description = f"Correlation Matrix:\n{df[numeric_cols].corr().to_string()}"
                    ai_text = analyze_data_with_gemini("Correlation Heatmap", corr_description)
                    st.session_state.plot_summaries_and_paths[bivariate_plot_key] = {
                        'path': fig_path, 'summary': ai_text
                    }
                    st.rerun()
        
        # Display bivariate AI insights
        if bivariate_plot_key in st.session_state.plot_summaries_and_paths:
            st.markdown("""
            <div class="success-box">
                <h4>🤖 AI-Generated Insights</h4>
            </div>
            """, unsafe_allow_html=True)
            st.info(st.session_state.plot_summaries_and_paths[bivariate_plot_key]['summary'])
    else:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Insufficient Data:</strong> Need at least 2 numeric columns for bivariate analysis.
        </div>
        """, unsafe_allow_html=True)

    # Report Generation Section
    st.markdown('<div class="section-header"><h3>📄 Professional Report Generation</h3></div>', 
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Generate Overall EDA Summary", key="generate_overall_summary"):
            with st.spinner("🔄 Generating comprehensive analysis..."):
                st.session_state.overall_eda_summary = generate_overall_eda_summary(df)
                st.rerun()
    
    with col2:
        plot_data_for_report = [
            value for key, value in st.session_state.plot_summaries_and_paths.items()
            if value['summary']
        ]
        
        if st.session_state.overall_eda_summary and plot_data_for_report:
            if st.button("📊 Download Complete PDF Report", key="download_pdf_report"):
                with st.spinner("📝 Generating professional PDF report..."):
                    pdf_output = create_pdf_report(
                        df, st.session_state.overall_eda_summary, plot_data_for_report
                    )
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_output,
                        file_name="professional_eda_report.pdf",
                        mime="application/pdf"
                    )
        else:
            st.markdown("""
            <div class="info-box">
                ℹ️ Generate overall summary and individual plot insights to create a complete PDF report.
            </div>
            """, unsafe_allow_html=True)
    
    # Display overall summary
    if st.session_state.overall_eda_summary:
        st.markdown("""
        <div class="success-box">
            <h4>🎯 Executive Summary</h4>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.overall_eda_summary)