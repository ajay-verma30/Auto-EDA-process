import streamlit as st

# Configure the Streamlit page
st.set_page_config(
    page_title="Auto EDA - Transform Your Data",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to style the app, header, and button
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Overall App Styling */
    .stApp {
        background: linear-gradient(135deg, #0d1117, #151a21); /* Dark gradient background */
        font-family: 'Inter', sans-serif;
        color: #f0f6fc; /* Light font color for readability */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        height: 100vh;
        width: 100vw;
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
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ffa726);
        color: #0d1117; 
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
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

# Main content
st.markdown("""
    <div class="hero-title">🚀 Auto EDA</div>
    <div class="hero-subtitle">
        Transform your raw data into powerful insights with our revolutionary 
        one-click automated exploratory data analysis platform
    </div>
""", unsafe_allow_html=True)

# CTA button section
st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
if st.button("🎯 Start Your Data Journey", key="main_cta"):
    st.switch_page("pages/1_Data_Cleaning.py")
st.markdown('</div>', unsafe_allow_html=True)
