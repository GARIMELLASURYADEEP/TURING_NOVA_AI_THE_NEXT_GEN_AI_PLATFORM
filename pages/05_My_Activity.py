# pages/05_My_Activity.py
import streamlit as st
from backend import utils
from backend import database as db

st.set_page_config(page_title="My Activity - Turing Nova AI", page_icon="🕰️", layout="wide")
utils.inject_custom_css()
utils.require_auth()

def history_page():
    st.markdown("<h1>🕰️ My Activity</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Review and reuse your previous generations.</p>", unsafe_allow_html=True)
    
    conn = db.get_db_connection()
    user = conn.execute("SELECT id FROM users WHERE email=?", (st.session_state.user,)).fetchone()
    
    if user:
        history = conn.execute("""
            SELECT * FROM activity_history 
            WHERE user_id=? 
            ORDER BY timestamp DESC
        """, (user["id"],)).fetchall()
        
        if not history:
            st.info("No activity recorded yet. Start using tools in the Hub!")
        else:
            for item in history:
                with st.expander(f"🕒 {item['timestamp']} | {item['tool_name']} ({item['activity_type']})"):
                    st.markdown("**Prompt/Input:**")
                    st.text(item['content'])
                    if item['activity_type'] == 'text_generated' and item['content']:
                        st.markdown("**Result:**")
                        st.code(item['content']) # In reality we should store content/result separately or in a JSON field
                    elif item['activity_type'] == 'image_generated':
                        st.markdown("*Image generated. Check your downloads or regenerate in the Hub.*")
                    
                    if st.button(f"Delete entry {item['id']}", key=f"del_{item['id']}"):
                        conn.execute("DELETE FROM activity_history WHERE id=?", (item['id'],))
                        conn.commit()
                        st.rerun()
    conn.close()

if __name__ == "__main__":
    history_page()
