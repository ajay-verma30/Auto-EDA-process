import streamlit as st

st.set_page_config(
    page_title="Auto EDA - Transform Your Data",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Overall App Styling */
    .stApp {
        background: linear-gradient(135deg, #0d1117, #151a21); /* Dark gradient background */
        font-family: 'Inter', sans-serif;
        color: #f0f6fc; /* Light font color for readability */
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Center container for all content */
    .center-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: #f0f6fc;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.6;
        font-weight: 300;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Button container centering - more specific selectors */
    .stApp > div > div > div > div {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    
    /* Button Styling with more specific targeting */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 2rem 0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ffa726) !important;
        color: #0d1117 !important; 
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3) !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Force center alignment for button container */
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 2rem 0;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="center-container">
        <div class="hero-title">🚀 Auto EDA</div>
        <div class="hero-subtitle">
            Transform your raw data into powerful insights with our revolutionary 
            one-click automated exploratory data analysis platform
        </div>
    </div>
""", unsafe_allow_html=True)

# Use columns to ensure centering
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🎯 Start Your Data Journey", key="main_cta"):
        st.switch_page("pages/1_Data_Cleaning.py")