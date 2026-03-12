# core/ui.py
import streamlit as st
import config

def inject_custom_css():
    """Inject global professional styling with dynamic accent colors."""
    ACCENT = st.session_state.get("accent_color", "#6366f1")
    THEME = st.session_state.get("theme", "dark")
    
    # Theme-based color tokens
    if THEME == "dark":
        BG_BASE = "#0f172a"
        HERO_BG = "rgba(30, 27, 75, 0.4)"
        CARD_BG = "rgba(30, 41, 59, 0.7)"
        TEXT_PRI = "#f8fafc"
        TEXT_SEC = "#94a3b8"
        DIVIDER = "rgba(255,255,255,0.1)"
        INPUT_BG = "#1e293b"
    else:
        BG_BASE = "#f8fafc"
        HERO_BG = "rgba(238, 242, 255, 0.8)"
        CARD_BG = "#ffffff"
        TEXT_PRI = "#1e293b"
        TEXT_SEC = "#64748b"
        DIVIDER = "rgba(0,0,0,0.1)"
        INPUT_BG = "#f1f5f9"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    :root {{
        --accent: {ACCENT};
        --bg-base: {BG_BASE};
        --text-pri: {TEXT_PRI};
        --text-sec: {TEXT_SEC};
        --card-bg: {CARD_BG};
    }}

    .stApp {{ background-color: var(--bg-base); font-family: 'Plus Jakarta Sans', sans-serif; }}
    
    .main-header {{
        font-size: 2.5rem; font-weight: 800; color: var(--text-pri);
        text-align: center; margin-bottom: 2rem;
    }}

    .tool-card-box {{
        background: var(--card-bg);
        border-radius: 18px;
        padding: 30px 20px;
        border: 1px solid {DIVIDER};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }}
    
    .tool-card-box:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        border-color: var(--accent);
    }}
    
    .tool-card-icon {{
        font-size: 3.5rem; 
        margin-bottom: 15px;
        line-height: 1;
    }}
    
    .tool-card-title {{ 
        font-size: 1.3rem; 
        font-weight: 700; 
        color: var(--text-pri); 
        margin-bottom: 10px;
        letter-spacing: -0.01em;
    }}
    
    .tool-card-desc {{ 
        font-size: 0.95rem; 
        color: var(--text-sec); 
        line-height: 1.5;
        margin: 0;
    }}
    
    .cat-badge {{
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
        background: var(--accent); color: white; margin-bottom: 15px;
    }}
    
    /* Center Streamlit buttons under cards */
    .stButton {{ display: flex; justify-content: center; margin-bottom: 30px; }}
    .stButton>button {{
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        width: auto !important;
        min-width: 180px;
    }}
    
    [data-testid="stSidebar"] {{ background-color: #0f172a; border-right: 1px solid rgba(255,255,255,0.05); }}
    
    /* Animations */
    .fade-in {{ animation: fadeIn 0.5s ease-out forwards; }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(100); }} }} /* Minor tweak */
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }} 

    /* Fix image previews */
    .stImage {{ display: flex; justify-content: center; }}
    .stImage img {{ border-radius: 18px; border: 1px solid {DIVIDER}; }}
    </style>
    """, unsafe_allow_html=True)

def render_tool_card(name, icon, desc, category_name=None):
    """Render a professional tool card using st.html for foolproof output."""
    badge = f'<div class="cat-badge">{category_name}</div>' if category_name else ''
    card_html = f"""
    <div class="tool-card-box">
        {badge}
        <div class="tool-card-icon">{icon}</div>
        <div class="tool-card-title">{name}</div>
        <div class="tool-card-desc">{desc}</div>
    </div>
    """
    st.html(card_html)

def puter_component(html_content, height=600):
    """Wrapper for Puter.js components."""
    full_html = f"""<!DOCTYPE html>
    <html>
    <head>
        <script src="https://js.puter.com/v2/"></script>
        <style>body{{margin:0;padding:0;background:transparent;}}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>"""
    st.components.v1.html(full_html, height=height, scrolling=True)
