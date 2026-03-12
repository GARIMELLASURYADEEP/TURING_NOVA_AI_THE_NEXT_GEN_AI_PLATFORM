# backend/utils.py
import streamlit as st
from backend import auth as auth_lib
from backend import database as db
import hashlib

def inject_custom_css():
    """Inject premium SaaS-style CSS."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        * { font-family: 'Plus+Jakarta+Sans', sans-serif !important; }
        
        .main {
            background-color: #05070a;
            color: #ffffff;
        }
        
        /* Glassmorphism Cards */
        .stButton>button {
            border-radius: 12px;
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            color: white;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
            border: none;
            color: white;
        }
        
        /* Result Container */
        .result-container {
            background: #0b1120;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            margin-top: 20px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        }
        
        /* Metric Styling */
        [data-testid="stMetricValue"] {
            font-size: 2.2rem;
            font-weight: 800;
            color: #6366f1;
        }
        
        /* Tool Cards */
        .tool-card {
            background: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .tool-card:hover {
            border-color: #6366f1;
            background: rgba(17, 24, 39, 0.9);
            transform: translateY(-5px);
        }
        /* Expander Styling */
        .stExpander {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            margin-bottom: 10px;
        }
        .stExpander [data-testid="stExpanderHeader"] {
            font-weight: 600;
            color: #e2e8f0;
            padding: 10px 15px;
        }
        
        /* Typography Polish */
        h1, h2, h3 {
            color: #ffffff;
            letter-spacing: -0.02em;
        }
    </style>
    """, unsafe_allow_html=True)

def check_auth():
    """Check if user is logged in via st.session_state."""
    if "token" not in st.session_state or not st.session_state.token:
        return False
    
    payload = auth_lib.decode_token(st.session_state.token)
    if not payload:
        st.session_state.token = None
        return False
    
    st.session_state.user = payload["sub"]
    st.session_state.role = payload.get("role", "user")
    return True

def require_auth():
    """Force redirect to login if not authenticated."""
    if not check_auth():
        st.warning("Please log in to access this page.")
        st.stop()

def log_activity(tool_name, activity_type, content=None, file_path=None):
    """Log user activity and store artifact paths."""
    if "user" not in st.session_state:
        return
    
    conn = db.get_db_connection()
    user = conn.execute("SELECT id FROM users WHERE email=?", (st.session_state.user,)).fetchone()
    if user:
        user_id = user["id"]
        # Ensure we don't log passwords or sensitive data in content for auth logs
        # But for Creator Hub, 'content' is the prompt.
        conn.execute("INSERT INTO analytics (user_id, tool_name, action_type) VALUES (?, ?, ?)", 
                       (user_id, tool_name, activity_type))
        conn.execute("""
            INSERT INTO activity_history (user_id, tool_name, activity_type, content, file_path) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, tool_name, activity_type, content, file_path))
        conn.commit()
    conn.close()
