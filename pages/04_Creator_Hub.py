# pages/04_Creator_Hub.py
import streamlit as st
from backend import utils
from backend import ai_handler
from backend import database as db
import time

st.set_page_config(page_title="Creator Hub - Turing Nova AI", page_icon="🛠️", layout="wide")
utils.inject_custom_css()
utils.require_auth()

# Categories and Tools Definitions (Standardized & Consolidated)
CATEGORIES = {
    "Creative & Writing": [
        {"name": "Text Generator", "icon": "✍️", "type": "text", "hint": "Write any topic or paragraph idea."},
        {"name": "Story Generator", "icon": "📖", "type": "text", "hint": "Describe the theme or characters."},
        {"name": "Script Generator", "icon": "🎬", "type": "text", "hint": "Describe a topic or scene to generate a script."},
        {"name": "Product Description", "icon": "🛍️", "type": "text", "hint": "Enter product name and features."},
        {"name": "AI Image Generator", "icon": "🎨", "type": "image", "hint": "Describe the image you want to generate."},
        {"name": "Logo Generator", "icon": "💎", "type": "image", "hint": "Describe the logo style and object."},
        {"name": "Poster Generator", "icon": "🖼️", "type": "image", "hint": "Describe the poster theme or event."},
    ],
    "Developer & Code": [
        {"name": "AI Code Generator", "icon": "💻", "type": "text", "hint": "Describe the program you want to build."},
        {"name": "Bug Fix Assistant", "icon": "🐛", "type": "text", "hint": "Paste code with an error to fix."},
        {"name": "SQL Generator", "icon": "💾", "type": "text", "hint": "Describe the database operation."},
        {"name": "API Doc Generator", "icon": "📚", "type": "text", "hint": "Paste functions to generate documentation."},
        {"name": "Game Builder", "icon": "🕹️", "type": "game", "hint": "Describe a simple HTML5 canvas game concept."},
    ],
    "Web & App Builder": [
        {"name": "Website Generator", "icon": "🌐", "type": "website", "hint": "Describe the type of website you want."},
        {"name": "Landing Page Builder", "icon": "🚀", "type": "website", "hint": "Describe the landing page purpose."},
        {"name": "UI Design Generator", "icon": "📱", "type": "ui", "hint": "Describe the interface or app layout."},
    ],
    "Audio & Audio Synthesis": [
        {"name": "Audio Generator", "icon": "🗣️", "type": "audio", "hint": "Enter text to convert into spoken audio."},
        {"name": "AI Voice Generator", "icon": "🎤", "type": "audio", "hint": "Enter text and choose voice style."},
        {"name": "AI Music Concept", "icon": "🎵", "type": "text", "hint": "Describe the music style or mood."},
    ],
    "Business & Professional": [
        {"name": "Invoice Generator", "icon": "🧾", "type": "invoice", "hint": "Describe the details for your invoice (items, price, client)."},
        {"name": "Startup Idea Gen", "icon": "🏢", "type": "text", "hint": "Enter industry or technology keywords."},
        {"name": "Resume Generator", "icon": "📄", "type": "text", "hint": "Provide skills and experience details."},
        {"name": "Business Name Gen", "icon": "🏷️", "type": "text", "hint": "Enter keywords for a business name."},
        {"name": "Ad Copy Generator", "icon": "💹", "type": "text", "hint": "Enter product or service details."},
    ],
    "Utility & Education": [
        {"name": "Quiz Generator", "icon": "📝", "type": "text", "hint": "Enter a topic to generate quiz questions."},
        {"name": "Study Guide Gen", "icon": "📖", "type": "text", "hint": "Enter a subject to generate a study guide."},
        {"name": "Mind Map Gen", "icon": "🕸️", "type": "text", "hint": "Enter a topic for structure generation."},
    ]
}

# Session State Initialization
if "current_category" not in st.session_state:
    st.session_state.current_category = None
if "current_tool" not in st.session_state:
    st.session_state.current_tool = None

def select_category(category):
    st.session_state.current_category = category
    st.session_state.current_tool = None
    st.rerun()

def select_tool(tool):
    st.session_state.current_tool = tool
    st.rerun()

def back_to_categories():
    st.session_state.current_category = None
    st.session_state.current_tool = None
    st.rerun()

def back_to_tools():
    st.session_state.current_tool = None
    st.rerun()


def render_tool_ui(tool):
    st.markdown(f"<h2>{tool['icon']} {tool['name']}</h2>", unsafe_allow_html=True)
    
    if st.button("⬅️ Back to Tools", key="btn_back_to_tools"):
        back_to_tools()

    # Tool persistence key
    tool_key = f"state_{tool['name']}"
    if tool_key not in st.session_state:
        st.session_state[tool_key] = {"input": "", "output": None, "voice": "female"}

    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    

    if tool['type'] in ['text', 'website', 'game', 'ui', 'invoice']:
        user_input = st.text_area(f"Input for {tool['name']}:", 
                                value=st.session_state[tool_key]["input"],
                                placeholder=tool['hint'],
                                height=150,
                                key=f"input_{tool_key}")
    elif tool['type'] == 'audio':
        user_input = st.text_area(f"Enter text to synthesize:", 
                                value=st.session_state[tool_key]["input"],
                                placeholder=tool['hint'],
                                height=120,
                                key=f"input_{tool_key}")
        col1, _ = st.columns([1,2])
        with col1:
            voice_options = ["female", "male", "robotic", "deep"]
            current_voice_index = voice_options.index(st.session_state[tool_key].get("voice", "female"))
            voice = st.selectbox("Select Voice Style", voice_options, index=current_voice_index, key=f"voice_{tool_key}")
            st.session_state[tool_key]["voice"] = voice
    else: # image
        user_input = st.text_input(f"Enter prompt for {tool['name']}:", 
                                  value=st.session_state[tool_key]["input"],
                                  placeholder=tool['hint'],
                                  key=f"input_{tool_key}")
    
    st.session_state[tool_key]["input"] = user_input
    
    # Generate Button
    btn_label = "Generate Artifact ✨" if tool['type'] != 'text' else "Generate Content ⚡"
    if st.button(btn_label, type="primary", use_container_width=True, key=f"gen_{tool_key}"):
        if user_input:
            with st.spinner("AI is crafting your request..."):
                if tool['type'] == 'audio':
                    st.session_state[tool_key]["output"] = ai_handler.get_puter_audio_ui(user_input, st.session_state[tool_key]["voice"])
                    utils.log_activity(tool['name'], 'audio_synthesized', user_input)
                else:
                    st.session_state[tool_key]["output"] = ai_handler.get_standardized_artifact_script(tool['type'], user_input)
                    utils.log_activity(tool['name'], f'{tool["type"]}_generated', user_input)
        else:
            st.warning("Please provide input before generating.")

    # Output Display
    if st.session_state[tool_key]["output"]:
        height = 650 if tool['type'] in ['website', 'game', 'ui', 'invoice'] else 450
        st.components.v1.html(st.session_state[tool_key]["output"], height=height, scrolling=True)
                
    st.markdown("</div>", unsafe_allow_html=True)

def hub_page():
    if st.session_state.current_category:
        cols = st.columns([1, 8])
        with cols[0]:
            if st.button("🔙 Categories", key="btn_back_to_cats"):
                back_to_categories()
        with cols[1]:
            st.markdown(f"### 📂 {st.session_state.current_category}")
    else:
        st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>🛠️ Creator Hub</h1>", unsafe_allow_html=True)

    # Main Router
    if st.session_state.current_tool:
        render_tool_ui(st.session_state.current_tool)
        
    elif st.session_state.current_category:
        tools = CATEGORIES[st.session_state.current_category]
        cols = st.columns(3)
        for i, tool in enumerate(tools):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='tool-card'>
                    <div style='font-size: 3rem; margin-bottom: 20px;'>{tool['icon']}</div>
                    <h3 style='margin-bottom: 10px;'>{tool['name']}</h3>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px;'>Type: {tool['type'].replace('_', ' ').capitalize()}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Launch {tool['name']}", key=f"tool_{i}", use_container_width=True):
                    select_tool(tool)
    else:
        # Show Categories
        cols = st.columns(3)
        for i, (cat_name, tools) in enumerate(CATEGORIES.items()):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='tool-card' style='border-color: rgba(99, 102, 241, 0.3);'>
                    <h2 style='margin-bottom: 15px; font-size: 1.4rem;'>{cat_name}</h2>
                    <p style='color: #94a3b8; font-size: 0.9rem;'>{len(tools)} specialized artifact tools</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Explore {cat_name} 📂", key=f"cat_{i}", use_container_width=True):
                    select_category(cat_name)

if __name__ == "__main__":
    hub_page()
