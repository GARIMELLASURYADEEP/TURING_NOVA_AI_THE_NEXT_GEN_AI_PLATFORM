# pages/01_Login.py
import streamlit as st
from backend import auth as auth_lib
from backend import database as db
from backend import utils
import time

st.set_page_config(page_title="Login - Turing Nova AI", page_icon="🔑", layout="centered")
utils.inject_custom_css()

def login_page():
    st.markdown("<h1 style='text-align: center;'>🔑 Platform Login</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='result-container'>", unsafe_allow_html=True)
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("Login to Platform", use_container_width=True):
            if email and password:
                conn = db.get_db_connection()
                user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
                conn.close()
                
                if user and auth_lib.verify_password(password, user["password_hash"]):
                    token = auth_lib.create_access_token({"sub": user["email"], "role": user["role"]})
                    st.session_state.token = token
                    st.session_state.user = user["email"]
                    st.session_state.role = user["role"]
                    
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
                    
                    if user["role"] == "admin":
                        st.switch_page("pages/06_Admin_Dashboard.py")
                    else:
                        st.switch_page("pages/03_Dashboard.py")
                else:
                    st.error("Invalid email or password.")
            else:
                st.warning("Please fill in all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;'>Don't have an account? <a href='/Signup' target='_self'>Register here</a></p>", unsafe_allow_html=True)
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("app.py")

if __name__ == "__main__":
    login_page()
