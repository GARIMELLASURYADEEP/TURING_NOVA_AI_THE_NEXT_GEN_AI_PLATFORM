# pages/03_Dashboard.py
import streamlit as st
from backend import utils
from backend import database as db

st.set_page_config(page_title="Dashboard - Turing Nova AI", page_icon="🚀", layout="wide")
utils.inject_custom_css()
utils.require_auth()

def dashboard_page():
    st.markdown(f"<h1>🚀 Welcome, {st.session_state.user}!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Here's your personal overview of AI activity.</p>", unsafe_allow_html=True)
    
    # Fetch user data
    conn = db.get_db_connection()
    user_id_row = conn.execute("SELECT id, created_at FROM users WHERE email=?", (st.session_state.user,)).fetchone()
    user_id = user_id_row["id"]
    join_date = user_id_row["created_at"]
    
    img_count = conn.execute("SELECT COUNT(*) FROM activity_history WHERE user_id=? AND activity_type='image_generated'", (user_id,)).fetchone()[0]
    total_tools = conn.execute("SELECT COUNT(*) FROM activity_history WHERE user_id=?", (user_id,)).fetchone()[0]
    conn.close()
    
    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Images Generated", img_count)
    with col2:
        st.metric("Tools Used", total_tools)
    with col3:
        st.metric("Downloads", "8") # Placeholder as in previous requirement
    with col4:
        st.metric("Account Created", join_date.split()[0])
        
    st.markdown("---")
    
    st.markdown("### 🌟 Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Explore Creator Hub 🛠️", use_container_width=True):
            st.switch_page("pages/04_Creator_Hub.py")
    with c2:
        if st.button("Start AI Chat 💬", use_container_width=True):
            st.switch_page("pages/07_AI_Chat.py")
    with c3:
        if st.button("View My Activity 🕰️", use_container_width=True):
            st.switch_page("pages/05_My_Activity.py")

if __name__ == "__main__":
    dashboard_page()
