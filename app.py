import streamlit as st
import requests
import streamlit.components.v1 as components
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
APP_NAME = "TURING NOVA AI : THE NEXT GEN AI PLATFORM"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "stepfun/step-3.5-flash:free"

# Page configuration
st.set_page_config(
    page_title="Turing Nova AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# Custom CSS — Colorful Animated Design System
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;500;600;700&display=swap');

/* ── Global reset & background ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Animated background gradient */
.stApp {
    background: linear-gradient(135deg, #0a0015 0%, #0d001f 25%, #000d2e 50%, #000a1a 75%, #0a0015 100%);
    background-size: 400% 400%;
    animation: bgShift 15s ease infinite;
}

@keyframes bgShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Hero Banner ── */
.hero-container {
    background: linear-gradient(135deg, #1a0533 0%, #2d0f6b 30%, #0a2a6e 60%, #0d1f4a 100%);
    border-radius: 24px;
    padding: 70px 50px;
    text-align: center;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(167,139,250,0.2);
    box-shadow:
        0 0 60px rgba(124,58,237,0.3),
        0 0 120px rgba(59,130,246,0.15),
        inset 0 1px 0 rgba(255,255,255,0.05);
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -60%;
    left: -10%;
    width: 50%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(167,139,250,0.15) 0%, transparent 60%);
    animation: heroGlow1 6s ease-in-out infinite alternate;
}

.hero-container::after {
    content: '';
    position: absolute;
    top: -60%;
    right: -10%;
    width: 50%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(59,130,246,0.15) 0%, transparent 60%);
    animation: heroGlow2 6s ease-in-out infinite alternate;
}

@keyframes heroGlow1 { from { opacity: 0.5; } to { opacity: 1; } }
@keyframes heroGlow2 { from { opacity: 1; } to { opacity: 0.5; } }

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(59,130,246,0.3));
    border: 1px solid rgba(167,139,250,0.5);
    border-radius: 999px;
    padding: 6px 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 2px;
    color: #c4b5fd;
    text-transform: uppercase;
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
    animation: pulseBadge 3s ease-in-out infinite;
}

@keyframes pulseBadge {
    0%, 100% { box-shadow: 0 0 10px rgba(124,58,237,0.3); }
    50% { box-shadow: 0 0 25px rgba(124,58,237,0.7), 0 0 50px rgba(59,130,246,0.3); }
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #f472b6, #a78bfa, #60a5fa, #34d399, #fbbf24, #f472b6);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
    animation: textShimmer 4s linear infinite;
    position: relative;
    z-index: 1;
    line-height: 1.2;
    text-shadow: none;
}

@keyframes textShimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

.hero-subtitle {
    font-size: 1.15rem;
    color: #a5b4fc;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
    letter-spacing: 0.5px;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    padding-left: 16px;
    margin-bottom: 24px;
    position: relative;
    display: inline-block;
}

.section-header::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #f472b6, #a78bfa, #60a5fa);
    border-radius: 4px;
    animation: rainbowBar 3s linear infinite;
}

@keyframes rainbowBar {
    0%   { background: linear-gradient(180deg, #f472b6, #a78bfa, #60a5fa); }
    33%  { background: linear-gradient(180deg, #60a5fa, #34d399, #fbbf24); }
    66%  { background: linear-gradient(180deg, #fbbf24, #f472b6, #a78bfa); }
    100% { background: linear-gradient(180deg, #f472b6, #a78bfa, #60a5fa); }
}

/* ── Tool Cards ── */
.tool-card {
    border-radius: 20px;
    padding: 38px 28px;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    text-align: center;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

.tool-card-chat {
    background: linear-gradient(135deg, #1a0533 0%, #3b0764 50%, #1e1b4b 100%);
    box-shadow: 0 8px 32px rgba(167,139,250,0.2);
}

.tool-card-code {
    background: linear-gradient(135deg, #0c1a3e 0%, #1e3a6e 50%, #0f2d5a 100%);
    box-shadow: 0 8px 32px rgba(59,130,246,0.2);
}

.tool-card-image {
    background: linear-gradient(135deg, #0a2e1a 0%, #065f46 50%, #0a2e1a 100%);
    box-shadow: 0 8px 32px rgba(52,211,153,0.2);
}

.tool-card:hover {
    transform: translateY(-10px) scale(1.02);
}

.tool-card-chat:hover {
    box-shadow: 0 20px 50px rgba(167,139,250,0.5), 0 0 30px rgba(124,58,237,0.3);
    border-color: rgba(167,139,250,0.5);
}

.tool-card-code:hover {
    box-shadow: 0 20px 50px rgba(59,130,246,0.5), 0 0 30px rgba(37,99,235,0.3);
    border-color: rgba(59,130,246,0.5);
}

.tool-card-image:hover {
    box-shadow: 0 20px 50px rgba(52,211,153,0.5), 0 0 30px rgba(16,185,129,0.3);
    border-color: rgba(52,211,153,0.5);
}

.tool-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(transparent, rgba(255,255,255,0.03), transparent);
    animation: cardRotate 6s linear infinite;
}

@keyframes cardRotate { to { transform: rotate(360deg); } }

.tool-icon {
    font-size: 3.5rem;
    margin-bottom: 18px;
    display: block;
    animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}

.tool-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 10px;
    position: relative;
    z-index: 1;
}

.tool-desc {
    font-size: 0.92rem;
    color: rgba(255,255,255,0.65);
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 999px;
    margin-top: 16px;
    letter-spacing: 1px;
    text-transform: uppercase;
    position: relative;
    z-index: 1;
}

.badge-purple {
    background: linear-gradient(90deg, #7c3aed, #a855f7);
    color: white;
    box-shadow: 0 0 15px rgba(124,58,237,0.5);
}

.badge-blue {
    background: linear-gradient(90deg, #2563eb, #06b6d4);
    color: white;
    box-shadow: 0 0 15px rgba(37,99,235,0.5);
}

.badge-green {
    background: linear-gradient(90deg, #059669, #10b981);
    color: white;
    box-shadow: 0 0 15px rgba(5,150,105,0.5);
}

/* ── Chat Messages ── */
.chat-user {
    background: linear-gradient(135deg, #6d28d9, #7c3aed, #4f46e5);
    color: white;
    border-radius: 20px 20px 4px 20px;
    padding: 14px 20px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    word-wrap: break-word;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4);
    border: 1px solid rgba(167,139,250,0.3);
    animation: slideInRight 0.3s ease;
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to   { opacity: 1; transform: translateX(0); }
}

.chat-ai {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    color: #e9d5ff;
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 20px 20px 20px 4px;
    padding: 14px 20px;
    margin: 8px 0;
    max-width: 80%;
    word-wrap: break-word;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    animation: slideInLeft 0.3s ease;
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}

.chat-label {
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 6px;
    opacity: 0.75;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5, #2563eb) !important;
    background-size: 200% 200% !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    padding: 10px 20px !important;
    animation: btnGradient 4s ease infinite !important;
}

@keyframes btnGradient {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(124,58,237,0.6) !important;
}

.stButton > button[data-baseweb="button"][kind="secondary"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(79,70,229,0.15)) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        #0d0020 0%,
        #1a0040 25%,
        #0d1a3e 60%,
        #050d2e 100%) !important;
    border-right: 1px solid rgba(167,139,250,0.15) !important;
}

section[data-testid="stSidebar"] * {
    color: #e9d5ff !important;
}

/* ── Inputs ── */
.stSelectbox > div > div {
    background: linear-gradient(135deg, #1a0533, #1e1b4b) !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    color: #e9d5ff !important;
    border-radius: 10px !important;
}

.stTextArea > div > textarea {
    background: linear-gradient(135deg, #0a0015, #0d001f) !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    color: #e9d5ff !important;
    border-radius: 10px !important;
}

.stTextArea > div > textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 20px rgba(167,139,250,0.25) !important;
}

.stTextInput > div > input {
    background: linear-gradient(135deg, #0a0015, #0d001f) !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    color: #e9d5ff !important;
    border-radius: 10px !important;
}

/* ── Code block ── */
.stCode, pre {
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 30px rgba(59,130,246,0.1) !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(167,139,250,0.15) !important;
    margin: 24px 0 !important;
}

/* ── Info / Warning / Success boxes ── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0015; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #7c3aed, #2563eb);
    border-radius: 4px;
}

/* ── Floating particles decoration ── */
.particle-strip {
    display: flex;
    gap: 14px;
    justify-content: center;
    margin: 18px 0;
    animation: particleDrift 8s ease-in-out infinite;
}

@keyframes particleDrift {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-6px); }
}

.dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    animation: dotPulse 2s ease-in-out infinite;
}
.dot1 { background: #f472b6; animation-delay: 0s; }
.dot2 { background: #a78bfa; animation-delay: 0.3s; }
.dot3 { background: #60a5fa; animation-delay: 0.6s; }
.dot4 { background: #34d399; animation-delay: 0.9s; }
.dot5 { background: #fbbf24; animation-delay: 1.2s; }

@keyframes dotPulse {
    0%,100% { transform: scale(1); opacity: 0.6; }
    50%      { transform: scale(1.6); opacity: 1; }
}

/* ── Page transition ── */
.page-wrapper {
    animation: pageIn 0.4s ease;
}

@keyframes pageIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Stat strip ── */
.stats-strip {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 30px;
}

.stat-chip {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(37,99,235,0.2));
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 999px;
    padding: 8px 22px;
    font-size: 0.85rem;
    color: #c4b5fd;
    font-weight: 600;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

.stat-chip:hover {
    background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(37,99,235,0.4));
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(124,58,237,0.4);
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Core API function
# ──────────────────────────────────────────────
def call_openrouter(messages: list, model: str = MODEL) -> dict:
    """Call OpenRouter API with a list of messages."""
    if not OPENROUTER_API_KEY:
        return {"error": "API Key not found. Please check your .env file."}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": APP_NAME,
    }

    data = {
        "model": model,
        "messages": messages,
    }

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def extract_content(response: dict) -> str | None:
    """Extract text content from an OpenRouter response."""
    if "error" in response:
        return None
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None


# ──────────────────────────────────────────────
# Page: Homepage
# ──────────────────────────────────────────────
def page_home():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">✦ Next Generation AI Platform</div>
        <div class="hero-title">🚀 TURING NOVA AI</div>
        <div class="hero-subtitle">
            Powered by OpenRouter &amp; Puter.js &nbsp;·&nbsp; Create, Chat, and Imagine — all in one place
        </div>
        <div class="particle-strip">
            <div class="dot dot1"></div>
            <div class="dot dot2"></div>
            <div class="dot dot3"></div>
            <div class="dot dot4"></div>
            <div class="dot dot5"></div>
        </div>
        <div class="stats-strip">
            <span class="stat-chip">💬 AI Chatbot</span>
            <span class="stat-chip">💻 Code Generator</span>
            <span class="stat-chip">🎨 Image Generator</span>
            <span class="stat-chip">⚡ Free to Use</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">✦ Choose Your Tool</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="tool-card tool-card-chat">
            <span class="tool-icon">💬</span>
            <div class="tool-title">AI Chatbot</div>
            <div class="tool-desc">Have a full conversation with a powerful AI assistant. Ask questions, get explanations, brainstorm ideas, or just chat freely.</div>
            <span class="badge badge-purple">OpenRouter AI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✦ Open Chatbot", key="btn_chat", use_container_width=True):
            st.session_state["current_page"] = "chatbot"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="tool-card tool-card-code">
            <span class="tool-icon">💻</span>
            <div class="tool-title">Code Generator</div>
            <div class="tool-desc">Describe what you want to build and get clean, executable code in the language of your choice — instantly.</div>
            <span class="badge badge-blue">OpenRouter AI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✦ Open Code Generator", key="btn_code", use_container_width=True):
            st.session_state["current_page"] = "codegen"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="tool-card tool-card-image">
            <span class="tool-icon">🎨</span>
            <div class="tool-title">Image Generator</div>
            <div class="tool-desc">Turn any text prompt into a stunning AI-generated image. Runs in your browser with Puter.js — no API key needed.</div>
            <span class="badge badge-green">Puter.js AI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✦ Open Image Generator", key="btn_img", use_container_width=True):
            st.session_state["current_page"] = "imagegen"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Page: Text-to-Text Chatbot
# ──────────────────────────────────────────────
def page_chatbot():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💬 AI Chatbot</div>', unsafe_allow_html=True)
    st.markdown("Have a free-form conversation with the AI. Your chat history is preserved during this session.")

    # Initialise chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display chat messages
    if st.session_state["chat_history"]:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-end; margin:8px 0;">
                    <div class="chat-user">
                        <div class="chat-label">🧑 You</div>
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-start; margin:8px 0;">
                    <div class="chat-ai">
                        <div class="chat-label">🤖 Nova AI</div>
                        {msg['content'].replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("✨ Say something to start your conversation with Nova AI!")

    st.markdown("---")

    # Input area
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area("Your message:", height=110, placeholder="Ask me anything — I'm here to help! 🚀")
        col_send, col_clear = st.columns([4, 1])
        with col_send:
            send = st.form_submit_button("🚀 Send Message", use_container_width=True)
        with col_clear:
            clear = st.form_submit_button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state["chat_history"] = []
        st.rerun()

    if send:
        if not user_input.strip():
            st.warning("Please type a message first.")
        else:
            st.session_state["chat_history"].append({"role": "user", "content": user_input.strip()})

            api_messages = [
                {"role": "system", "content": "You are Nova, a helpful, friendly, and knowledgeable AI assistant. Answer clearly and concisely with enthusiasm."}
            ] + st.session_state["chat_history"]

            with st.spinner("✦ Nova AI is thinking..."):
                response = call_openrouter(api_messages)
                content = extract_content(response)

            if content is None:
                st.error(f"Error: {response.get('error', 'Unexpected response format.')}")
                st.session_state["chat_history"].pop()
            else:
                st.session_state["chat_history"].append({"role": "assistant", "content": content})

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Page: Text-to-Code Generator
# ──────────────────────────────────────────────
def page_codegen():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💻 AI Code Generator</div>', unsafe_allow_html=True)
    st.markdown("Describe what you want to build and get clean, executable code — powered by OpenRouter AI.")

    col1, col2 = st.columns([1, 3])

    with col1:
        language = st.selectbox(
            "🌐 Language",
            [
                "Python", "Java", "C++", "JavaScript", "Go", "Rust",
                "TypeScript", "SQL", "HTML/CSS", "Shell Script",
                "C#", "PHP", "Ruby", "Swift", "Kotlin", "GDScript", "C",
            ]
        )

    with col2:
        prompt_text = st.text_area(
            "💡 Describe what you want to build:",
            height=150,
            placeholder="e.g. A Python function that sorts a list of dictionaries by a given key"
        )

    if st.button("⚡ Generate Code", type="primary"):
        if not prompt_text.strip():
            st.warning("Please describe a coding task first.")
        else:
            final_prompt = (
                f"Write only clean, executable {language} code for the following task. "
                f"Do NOT include any explanation or markdown prose — only the code block.\n\n"
                f"Task: {prompt_text.strip()}"
            )
            messages = [
                {"role": "system", "content": "You are an expert software engineer. Output only the requested code with no extra commentary."},
                {"role": "user", "content": final_prompt},
            ]

            with st.spinner("✦ Writing your code..."):
                response = call_openrouter(messages)
                content = extract_content(response)

            if content is None:
                st.error(f"Error: {response.get('error', 'Unexpected response format.')}")
            else:
                st.markdown("#### ✅ Generated Code")
                st.code(content, language=language.lower().replace("/", "").replace(" ", ""))
                st.success(f"🎉 {language} code generated successfully!")

    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Page: AI Image Generator (Puter.js)
# ──────────────────────────────────────────────
def page_imagegen():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎨 AI Image Generator</div>', unsafe_allow_html=True)
    st.markdown("Enter a text prompt and let **Puter.js AI** generate a stunning image — right inside your browser, no API key needed.")

    st.markdown("---")

    puter_html = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <script src="https://js.puter.com/v2/"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: transparent;
      color: #e9d5ff;
      padding: 0;
    }

    .card {
      background: linear-gradient(135deg, #0a0020 0%, #1a0040 50%, #0a1a40 100%);
      border: 1px solid rgba(167,139,250,0.2);
      border-radius: 20px;
      padding: 32px 30px 28px;
      box-shadow: 0 0 60px rgba(124,58,237,0.15), inset 0 1px 0 rgba(255,255,255,0.04);
      position: relative;
      overflow: hidden;
    }

    .card::before {
      content: '';
      position: absolute;
      top: -40%;
      left: -20%;
      width: 60%;
      height: 180%;
      background: radial-gradient(ellipse, rgba(167,139,250,0.07) 0%, transparent 60%);
      pointer-events: none;
    }

    .card::after {
      content: '';
      position: absolute;
      top: -40%;
      right: -20%;
      width: 60%;
      height: 180%;
      background: radial-gradient(ellipse, rgba(59,130,246,0.07) 0%, transparent 60%);
      pointer-events: none;
    }

    .label {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #a78bfa;
      margin-bottom: 10px;
    }

    .row {
      display: flex;
      gap: 12px;
      margin-bottom: 20px;
      position: relative;
      z-index: 1;
    }

    #prompt {
      flex: 1;
      background: rgba(10,0,30,0.8);
      border: 1px solid rgba(167,139,250,0.35);
      border-radius: 12px;
      color: #e9d5ff;
      font-size: 0.95rem;
      font-family: 'Inter', sans-serif;
      padding: 14px 18px;
      outline: none;
      transition: border-color 0.3s, box-shadow 0.3s;
    }
    #prompt::placeholder { color: #6b5a8a; }
    #prompt:focus {
      border-color: #a78bfa;
      box-shadow: 0 0 25px rgba(167,139,250,0.25);
    }

    #genBtn {
      background: linear-gradient(135deg, #7c3aed, #4f46e5, #2563eb);
      background-size: 200%;
      color: #fff;
      border: none;
      border-radius: 12px;
      font-family: 'Inter', sans-serif;
      font-size: 0.95rem;
      font-weight: 700;
      padding: 14px 24px;
      cursor: pointer;
      white-space: nowrap;
      transition: transform 0.25s, box-shadow 0.25s;
      letter-spacing: 0.5px;
      animation: btnGrad 4s ease infinite;
    }
    @keyframes btnGrad {
      0%   { background-position: 0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    #genBtn:hover:not(:disabled) {
      transform: translateY(-3px);
      box-shadow: 0 12px 30px rgba(124,58,237,0.6);
    }
    #genBtn:disabled { opacity: 0.55; cursor: not-allowed; }

    #status {
      font-size: 0.88rem;
      color: #a78bfa;
      min-height: 24px;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      gap: 10px;
      position: relative;
      z-index: 1;
    }

    .spinner {
      display: inline-block;
      width: 18px; height: 18px;
      border: 2px solid rgba(167,139,250,0.25);
      border-top-color: #a78bfa;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    #imgWrap {
      width: 100%;
      text-align: center;
      min-height: 0;
      position: relative;
      z-index: 1;
    }

    #imgWrap img {
      max-width: 100%;
      border-radius: 16px;
      box-shadow:
        0 0 0 1px rgba(167,139,250,0.2),
        0 16px 50px rgba(103,76,230,0.5),
        0 0 80px rgba(59,130,246,0.2);
      animation: fadeInImg 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    @keyframes fadeInImg {
      from { opacity: 0; transform: scale(0.9); }
      to   { opacity: 1; transform: scale(1); }
    }

    #dlBtn {
      display: none;
      margin: 20px auto 0;
      background: linear-gradient(135deg, #059669, #10b981);
      color: #fff;
      border: none;
      border-radius: 12px;
      font-family: 'Inter', sans-serif;
      font-size: 0.92rem;
      font-weight: 700;
      padding: 12px 28px;
      cursor: pointer;
      transition: transform 0.25s, box-shadow 0.25s;
      letter-spacing: 0.5px;
    }
    #dlBtn:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 28px rgba(5,150,105,0.5);
    }

    #errMsg {
      color: #f87171;
      font-size: 0.88rem;
      margin-top: 10px;
      display: none;
      background: rgba(239,68,68,0.1);
      border: 1px solid rgba(239,68,68,0.3);
      border-radius: 10px;
      padding: 10px 14px;
    }

    /* Decorative dots */
    .dots-row {
      display: flex; gap: 10px; margin-bottom: 20px; align-items: center;
    }
    .dot { width: 7px; height: 7px; border-radius: 50%; }
    .dp { background: #f472b6; animation: dp 2s infinite 0s; }
    .dv { background: #a78bfa; animation: dp 2s infinite 0.3s; }
    .db { background: #60a5fa; animation: dp 2s infinite 0.6s; }
    .dg { background: #34d399; animation: dp 2s infinite 0.9s; }
    .dy { background: #fbbf24; animation: dp 2s infinite 1.2s; }
    @keyframes dp {
      0%,100% { transform: scale(1); opacity: 0.5; }
      50%      { transform: scale(1.7); opacity: 1; }
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="dots-row">
      <span class="dot dp"></span>
      <span class="dot dv"></span>
      <span class="dot db"></span>
      <span class="dot dg"></span>
      <span class="dot dy"></span>
      <span style="font-size:0.75rem; color:#7c6aad; font-weight:600; letterSpacing:1px; margin-left:6px;">PUTER.JS IMAGE AI</span>
    </div>
    <div class="label">✦ Describe your image</div>
    <div class="row">
      <input id="prompt" type="text"
        placeholder="e.g. A futuristic city at sunset, neon lights, cyberpunk style, ultra detailed" />
      <button id="genBtn" onclick="generate()">🖼️ Generate</button>
    </div>
    <div id="status"></div>
    <div id="imgWrap"></div>
    <button id="dlBtn" onclick="downloadImg()">⬇️ Download Image</button>
    <div id="errMsg"></div>
  </div>

  <script>
    let currentBlob = null;
    let currentPrompt = '';

    async function generate() {
      const promptEl = document.getElementById('prompt');
      const btn      = document.getElementById('genBtn');
      const status   = document.getElementById('status');
      const imgWrap  = document.getElementById('imgWrap');
      const dlBtn    = document.getElementById('dlBtn');
      const errMsg   = document.getElementById('errMsg');

      const p = promptEl.value.trim();
      if (!p) {
        errMsg.textContent = '⚠️ Please enter a prompt first.';
        errMsg.style.display = 'block';
        return;
      }
      errMsg.style.display = 'none';
      currentPrompt = p;
      currentBlob = null;

      btn.disabled = true;
      imgWrap.innerHTML = '';
      dlBtn.style.display = 'none';
      status.innerHTML = '<span class="spinner"></span>&nbsp;✦ Generating your image — please wait…';

      try {
        const img = await puter.ai.txt2img(p);
        img.style.maxWidth = '100%';
        img.style.borderRadius = '16px';
        imgWrap.appendChild(img);

        const resp = await fetch(img.src);
        currentBlob = await resp.blob();
        dlBtn.style.display = 'block';
        status.innerHTML = '✅ &nbsp;Image generated successfully!';
      } catch (e) {
        errMsg.textContent = '❌ Error: ' + (e.message || String(e));
        errMsg.style.display = 'block';
        status.innerHTML = '';
      } finally {
        btn.disabled = false;
      }
    }

    function downloadImg() {
      if (!currentBlob) return;
      const a = document.createElement('a');
      a.href = URL.createObjectURL(currentBlob);
      a.download = 'turing_nova_' + currentPrompt.slice(0, 40).replace(/\s+/g, '_') + '.png';
      a.click();
    }

    document.getElementById('prompt').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') generate();
    });
  </script>
</body>
</html>
"""
    components.html(puter_html, height=540, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Sidebar navigation
# ──────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px;">
            <div style="font-family:'Inter',sans-serif; font-size:1.3rem; font-weight:900;
                        background:linear-gradient(90deg,#f472b6,#a78bfa,#60a5fa);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        background-clip:text; margin-bottom:4px;">🚀 TURING NOVA AI</div>
            <div style="font-size:0.7rem; color:#6b5a8a; letter-spacing:1.5px; text-transform:uppercase; font-weight:600;">Next Gen AI Platform</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        pages = {
            "🏠 Home": "home",
            "💬 AI Chatbot": "chatbot",
            "💻 Code Generator": "codegen",
            "🎨 Image Generator": "imagegen",
        }

        for label, key in pages.items():
            is_active = st.session_state.get("current_page", "home") == key
            if st.button(label, key=f"nav_{key}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state["current_page"] = key
                st.rerun()

        st.markdown("---")

        st.markdown("""
        <div style="text-align:center; padding: 10px 0;">
            <div style="font-size:0.75rem; color:#6b5a8a; margin-bottom:6px;">Powered by</div>
            <div style="display:flex; gap:8px; justify-content:center; flex-wrap:wrap;">
                <span style="font-size:0.72rem; background:linear-gradient(135deg,rgba(124,58,237,0.25),rgba(79,70,229,0.25));
                             border:1px solid rgba(167,139,250,0.3); border-radius:99px;
                             padding:3px 10px; color:#c4b5fd; font-weight:600;">OpenRouter</span>
                <span style="font-size:0.72rem; background:linear-gradient(135deg,rgba(5,150,105,0.25),rgba(16,185,129,0.25));
                             border:1px solid rgba(52,211,153,0.3); border-radius:99px;
                             padding:3px 10px; color:#6ee7b7; font-weight:600;">Puter.js</span>
            </div>
            <div style="font-size:0.7rem; color:#4b3f72; margin-top:14px;">© 2026 Turing Nova AI</div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
def main():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    sidebar()

    page = st.session_state["current_page"]
    if page == "home":
        page_home()
    elif page == "chatbot":
        page_chatbot()
    elif page == "codegen":
        page_codegen()
    elif page == "imagegen":
        page_imagegen()


if __name__ == "__main__":
    main()
