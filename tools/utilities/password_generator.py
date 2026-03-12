# tools/utilities/password_generator.py
import streamlit as st
import random
import string

def show():
    st.markdown("### 🔐 Secure Password Generator")
    st.markdown("---")
    
    length = st.slider("Password Length:", 8, 64, 16)
    
    col1, col2 = st.columns(2)
    with col1:
        use_upper = st.checkbox("Uppercase Letters (A-Z)", value=True)
        use_lower = st.checkbox("Lowercase Letters (a-z)", value=True)
    with col2:
        use_numbers = st.checkbox("Numbers (0-9)", value=True)
        use_symbols = st.checkbox("Symbols (!@#$%^&*)", value=True)
    
    if st.button("🔄 Generate Password", type="primary", use_container_width=True):
        chars = ""
        if use_upper: chars += string.ascii_uppercase
        if use_lower: chars += string.ascii_lowercase
        if use_numbers: chars += string.digits
        if use_symbols: chars += string.punctuation
        
        if not chars:
            st.error("Please select at least one character set.")
        else:
            pwd = "".join(random.choice(chars) for _ in range(length))
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:12px; border:1px solid rgba(255,255,255,0.1); margin:20px 0; text-align:center;">
                <code style="font-size:1.5rem; color:#10b981;">{pwd}</code>
            </div>
            """, unsafe_allow_html=True)
            st.button("📋 Copy to Clipboard (Simulated)", on_click=lambda: st.toast("Password copied!"))
