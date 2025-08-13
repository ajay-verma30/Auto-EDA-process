import streamlit as st

st.set_page_config(
    page_title="Auto EDA - Transform Your Data",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d1b4e 50%, #1a1f3a 75%, #0a0e27 100%);
        font-family: 'Inter', sans-serif;
        color: #ffffff;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
        z-index: -1;
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-20px) rotate(1deg); }
        66% { transform: translateY(10px) rotate(-1deg); }
    }
    
    .main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        text-align: center;
        padding: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .app-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.5));
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        line-height: 1.2;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
        animation: slideInUp 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.85);
        margin-bottom: 3rem;
        line-height: 1.7;
        font-weight: 400;
        max-width: 700px;
        animation: slideInUp 1s ease-out 0.2s both;
    }
    
    .features {
        display: flex;
        gap: 2rem;
        margin: 2rem 0 3rem 0;
        animation: slideInUp 1s ease-out 0.4s both;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.05);
        padding: 0.75rem 1.25rem;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    .button-container {
        animation: slideInUp 1s ease-out 0.6s both;
    }
    
    .stButton {
        display: flex !important;
        justify-content: center !important;
        margin: 2rem 0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.35),
            0 2px 8px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        min-width: 280px !important;
        height: 60px !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 12px 40px rgba(102, 126, 234, 0.4),
            0 4px 12px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, #7c93ff 0%, #8b5fbf 100%) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    .trust-indicators {
        margin-top: 3rem;
        opacity: 0.7;
        animation: slideInUp 1s ease-out 0.8s both;
    }
    
    .trust-text {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 1rem;
    }
    
    .stats {
        display: flex;
        gap: 3rem;
        justify-content: center;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        display: block;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .features {
            flex-direction: column;
            align-items: center;
        }
        .stats {
            gap: 1.5rem;
        }
        .stButton > button {
            min-width: 250px !important;
            padding: 0.9rem 2.5rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .app-icon {
            font-size: 4rem;
        }
        .main-container {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

if st.button("🎯 Start Your Data Journey"):
    st.switch_page("pages/1_Data_Cleaning.py")

