# core/state.py
import streamlit as st
import config

def init_state():
    # Theme & Style
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    if "accent_color" not in st.session_state:
        # Default to Indigo for Dark, Violet for Light
        st.session_state["accent_color"] = config.COLOR_PRESETS_DARK["Indigo"]["accent"]
    
    # Navigation View
    if "view" not in st.session_state:
        st.session_state["view"] = "chat" # chat, hub
    
    # Hub Context
    if "hub_category" not in st.session_state:
        st.session_state["hub_category"] = None
    if "hub_tool" not in st.session_state:
        st.session_state["hub_tool"] = None

    # Chat History
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # Search Query
    if "tool_search" not in st.session_state:
        st.session_state["tool_search"] = ""

def set_view(view):
    st.session_state["view"] = view
    st.session_state["hub_tool"] = None # Reset tool when switching main views

def set_category(cat):
    st.session_state["hub_category"] = cat
    st.session_state["hub_tool"] = None

def set_tool(tool_id):
    st.session_state["hub_tool"] = tool_id
