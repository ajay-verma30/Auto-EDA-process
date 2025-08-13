import streamlit as st

st.set_page_config(
    page_title="Auto EDA - Transform Your Data",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
    --dark-bg: #0d1117;
    --light-text: #f0f6fc;
    --button-start: #ff6b6b;
    --button-end: #ffa726;
}

.stApp {
    background: linear-gradient(135deg, var(--dark-bg), #151a21);
    color: var(--light-text);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.stButton{
    margin-top: 20px;
    position: absolute !important;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%)
}
            
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.title-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.custom-title {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin-bottom: 2rem;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    background: linear-gradient(45deg, var(--light-text), #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


.stButton > button {
    background: linear-gradient(45deg, var(--button-start), var(--button-end));
    color: var(--dark-bg);
    border: none !important;
    border-radius: 9999px !important;
    padding: 0.75rem 2.5rem !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3) !important;
    cursor: pointer !important;
    transition: all 0.3s ease-in-out !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 12px 30px rgba(255, 107, 107, 0.5) !important;
}

@media (max-width: 600px) {
    .custom-title {
        font-size: 2rem;
    }
    .stButton > button {
        padding: 0.5rem 2rem !important;
        font-size: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div class='title-container'><h1 class='custom-title'>Auto EDA</h1></div>", unsafe_allow_html=True)
    if st.button("🎯 Start Your Data Journey"):
        st.write("Button clicked!") 

