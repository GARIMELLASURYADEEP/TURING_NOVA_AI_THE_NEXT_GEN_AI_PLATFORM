# pages/06_Admin_Dashboard.py
import streamlit as st
from backend import utils
from backend import database as db

st.set_page_config(page_title="Admin Console - Turing Nova AI", page_icon="📊", layout="wide")
utils.inject_custom_css()
utils.require_auth()

if st.session_state.role != "admin":
    st.error("Access Denied. Admins only.")
    st.stop()

def admin_page():
    st.markdown("<h1>📊 Global Analytics Console</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Monitor platform health and user engagement.</p>", unsafe_allow_html=True)
    
    conn = db.get_db_connection()
    
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_images = conn.execute("SELECT COUNT(*) FROM activity_history WHERE activity_type='image_generated'").fetchone()[0]
    total_tools = conn.execute("SELECT COUNT(*) FROM activity_history").fetchone()[0]
    
    # Active users today (mock logic or actual if timestamps are parsed)
    active_today = conn.execute("SELECT COUNT(DISTINCT user_id) FROM login_history WHERE date(login_time) = date('now')").fetchone()[0]
    # If login_history is empty, fall back to 1 for this demo
    active_today = max(active_today, 1)

    conn.close()
    
    # Global Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Users", total_users)
    with c2:
        st.metric("Images Generated", total_images)
    with c3:
        st.metric("Tool Executions", total_tools)
    with c4:
        st.metric("Active Users Today", active_today)
        
    st.markdown("---")
    
    st.markdown("### 📋 System Audit Log")
    # Fetch recent global activity
    conn = db.get_db_connection()
    recent = conn.execute("""
        SELECT h.*, u.email 
        FROM activity_history h 
        JOIN users u ON h.user_id = u.id 
        ORDER BY h.timestamp DESC LIMIT 10
    """).fetchall()
    conn.close()
    
    if recent:
        st.table([{
            "User": r["email"],
            "Tool": r["tool_name"],
            "Action": r["activity_type"],
            "Time": r["timestamp"]
        } for r in recent])
    else:
        st.info("No activity logs available.")

if __name__ == "__main__":
    admin_page()
