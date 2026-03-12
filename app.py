# app.py
import streamlit as st
from backend import utils
from backend import database as db
from backend import auth as auth_lib

st.set_page_config(
    page_title="Turing Nova AI",
    page_icon="🌌",
    layout="wide"
)

# Initialize database
db.init_db()

# Custom CSS
utils.inject_custom_css()

def main():
    # Persistent Session State
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None

    # App Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 20px; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🌌 TURING NOVA AI
        </h1>
        <p style="font-size: 1.25rem; color: #94a3b8; max-width: 700px; margin: 0 auto;">
            The Next Gen AI Platform. Reimagined for professionals. 
            Harness the power of decentralized intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Navigation info
    with st.sidebar:
        st.markdown("### 🌌 Turing Nova")
        if st.session_state.user:
            st.success(f"Logged in as: {st.session_state.user}")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.token = None
                st.session_state.user = None
                st.rerun()
        else:
            st.info("Please login to access all tools.")

    # Home Content
    if not st.session_state.user:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🚀 New here?")
            if st.button("Create Account", use_container_width=True):
                 st.switch_page("pages/02_Signup.py")
        with col2:
            st.markdown("### 🔑 Welcome back")
            if st.button("Login to Platform", use_container_width=True):
                st.switch_page("pages/01_Login.py")
    else:
        st.info("Use the sidebar or the Hub to explore tools.")
        if st.button("Go to Creator Hub 🚀", type="primary"):
            st.switch_page("pages/04_Creator_Hub.py")

if __name__ == "__main__":
    main()
