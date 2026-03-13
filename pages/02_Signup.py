# pages/02_Signup.py
import streamlit as st
from backend import auth as auth_lib
from backend import database as db
from backend import utils
import time

st.set_page_config(page_title="Sign Up - Turing Nova AI", page_icon="✨", layout="centered")
utils.inject_custom_css()

def signup_page():
    st.markdown("<h1 style='text-align: center;'>✨ Join Turing Nova AI</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='result-container'>", unsafe_allow_html=True)
        email = st.text_input("Choose Email")
        password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Create My Account", use_container_width=True):
            if email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    conn = db.get_db_connection()
                    try:
                        # Check if user exists
                        existing = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
                        if existing:
                            st.error("Email already registered.")
                        else:
                            hashed = auth_lib.hash_password(password)
                            # First user or specific email can be admin
                            role = "admin" if email == "final20052025@gmail.com" else "user"
                            conn.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)", 
                                           (email, hashed, role))
                            conn.commit()
                            st.success("✨ Account created successfully! Go to login page to access your dashboard.")
                            if st.button("Go to Login Page", use_container_width=True):
                                st.switch_page("pages/01_Login.py")
                            
                            st.info("Redirecting you to login in 3 seconds...")
                            time.sleep(3)
                            st.switch_page("pages/01_Login.py")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    finally:
                        conn.close()
            else:
                st.warning("Please fill in all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;'>Already have an account? <a href='/Login' target='_self'>Login here</a></p>", unsafe_allow_html=True)
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("app.py")

if __name__ == "__main__":
    signup_page()
