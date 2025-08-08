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
    }
    
    /* Main Content Container */
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
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
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    /* Feature Card */
    .feature-card {
        background: rgba(255, 255, 255, 0.08); /* Slightly darker card background */
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        color: #f0f6fc;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15); /* More subtle border */
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff6b6b, #ffa726, #48cae4);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #f0f6fc;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.5;
        font-size: 0.95rem;
    }
    
    /* CTA Section */
    .cta-section {
        text-align: center;
        margin: 4rem 0;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 1rem;
    }
    
    .cta-description {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Stats Container */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        text-align: center;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.08); /* Consistent card background */
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem 1rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .stat-number {
        color: #f0f6fc;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ff6b6b, #ffa726);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #f0f6fc;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Floating background shapes */
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-shape {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        animation: float 6s ease-in-out infinite;
    }
    
    .shape-1 {
        width: 80px;
        height: 80px;
        top: 10%;
        left: 10%;
        animation-delay: 0s;
    }
    
    .shape-2 {
        width: 120px;
        height: 120px;
        top: 60%;
        right: 15%;
        animation-delay: 2s;
    }
    
    .shape-3 {
        width: 60px;
        height: 60px;
        bottom: 20%;
        left: 20%;
        animation-delay: 4s;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
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
        display: block;
        margin: 0 auto;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
    }

    /* Column Boxes */
    .column-box {
        text-align: center; 
        padding: 2rem; 
        background: rgba(255, 255, 255, 0.08); /* Dark card background */
        border-radius: 15px; 
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15); /* Subtle border */
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
        .feature-grid {
            grid-template-columns: 1fr;
        }
        .main-container {
            margin: 1rem;
            padding: 2rem 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown("""
    <div class="floating-elements">
        <div class="floating-shape shape-1"></div>
        <div class="floating-shape shape-2"></div>
        <div class="floating-shape shape-3"></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-title">🚀 Auto EDA</div>
    <div class="hero-subtitle">
        Transform your raw data into powerful insights with our revolutionary 
        one-click automated exploratory data analysis platform
    </div>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
if st.button("🎯 Start Your Data Journey", key="main_cta"):
    st.switch_page("pages/1_Data_Cleaning.py")
st.markdown('</div>', unsafe_allow_html=True)



st.markdown("""
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-number">10K+</div>
            <div class="stat-label">Datasets Analyzed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">25+</div>
            <div class="stat-label">Chart Types</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">99.9%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">500+</div>
            <div class="stat-label">Happy Users</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to Unlock Your Data's Potential?</div>
        <div class="cta-description">
            Join thousands of data professionals who trust Auto EDA for their 
            exploratory data analysis needs. Start your journey today!
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
        <div class="column-box">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📤</div>
            <div style="color: #f0f6fc; font-weight: 600; margin-bottom: 0.5rem;">Upload Data</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                Drop your CSV, Excel, or JSON files
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="column-box">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🔄</div>
            <div style="color: #f0f6fc; font-weight: 600; margin-bottom: 0.5rem;">Auto Analysis</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                AI processes and analyzes your data
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="column-box">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📋</div>
            <div style="color: #f0f6fc; font-weight: 600; margin-bottom: 0.5rem;">Get Insights</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                Download reports and visualizations
            </div>
        </div>
    """, unsafe_allow_html=True)
st.markdown("""
    <div class="column-box" style="margin-top: 2rem; margin-bottom: 2rem; text-align: center; border: 1px solid rgba(255,255,255,0.15);">
        <div style="font-size: 1.2rem; color: #f0f6fc; margin-bottom: 1rem;">
            🚀 <strong>Click "Start Your Data Journey" to begin with Data Cleaning</strong>
        </div>
        <div style="color: rgba(255,255,255,0.8);">
            Our guided workflow will take you through each step of the analysis process
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.6); 
    border-top: 1px solid rgba(255,255,255,0.1); margin-top: 3rem;">
        <p>© 2025 Auto EDA Tool - Empowering Data-Driven Decisions 🚀</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)