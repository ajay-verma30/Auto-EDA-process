import streamlit as st

st.set_page_config(
    page_title="Data Analysis Journey",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .welcome-container {
        text-align: center;
        padding: 3rem 2rem;
        background-color: #f8f9fa;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .journey-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .step-number {
        background: #667eea;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>🚀 Welcome to Your Data Analysis Journey</h1>
        <p>Transform raw data into meaningful insights</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-container">
        <h2>Ready to Explore Your Data?</h2>
        <p style="font-size: 18px; color: #666; margin-bottom: 2rem;">
            Embark on a comprehensive data analysis journey that will take you from raw data 
            to actionable insights through systematic cleaning and exploratory analysis.
        </p>
    </div>
""", unsafe_allow_html=True)


st.markdown("## 📋 Your Analysis Journey")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3><span class="step-number">1</span>Data Cleaning</h3>
            <p>Clean and preprocess your data by handling missing values, removing duplicates, 
            and ensuring data quality for accurate analysis.</p>
            <ul>
                <li>Handle missing values</li>
                <li>Remove duplicates</li>
                <li>Data type conversions</li>
                <li>Outlier detection</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3><span class="step-number">2</span>Exploratory Data Analysis</h3>
            <p>Discover patterns, relationships, and insights in your cleaned data through 
            comprehensive statistical analysis and visualizations.</p>
            <ul>
                <li>Statistical summaries</li>
                <li>Data visualizations</li>
                <li>Correlation analysis</li>
                <li>Pattern discovery</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Ready to begin?")
    
    if st.button("🚀 Start Your Journey", key="start_journey", use_container_width=True):
        st.switch_page("pages/1_Data_Cleaning.py")
    
    st.markdown("""
        <p style="text-align: center; color: #666; margin-top: 1rem;">
            Click the button above to begin with data cleaning
        </p>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>💡 <strong>Tip:</strong> Make sure your data is ready for analysis. 
        The journey becomes more meaningful with quality data!</p>
    </div>
""", unsafe_allow_html=True)