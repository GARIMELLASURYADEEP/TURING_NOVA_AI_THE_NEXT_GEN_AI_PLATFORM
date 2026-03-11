import streamlit as st
import requests
import json
import os
import time
import random
import urllib.parse
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
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hero section */
.hero-container {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    border-radius: 20px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #c4b5fd;
    margin-bottom: 0;
}

/* Tool cards */
.tool-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 24px;
    margin-top: 10px;
}

.tool-card {
    background: linear-gradient(145deg, #1e1b4b, #2d2369);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 16px;
    padding: 36px 28px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.tool-card:hover {
    transform: translateY(-6px);
    border-color: rgba(167,139,250,0.7);
    box-shadow: 0 16px 40px rgba(103,76,230,0.4);
}

.tool-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(167,139,250,0.08) 0%, transparent 60%);
    pointer-events: none;
}

.tool-icon {
    font-size: 3rem;
    margin-bottom: 16px;
    display: block;
}

.tool-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e9d5ff;
    margin-bottom: 8px;
}

.tool-desc {
    font-size: 0.95rem;
    color: #a78bfa;
    line-height: 1.5;
}

.badge {
    display: inline-block;
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 99px;
    margin-top: 14px;
    letter-spacing: 0.5px;
}

/* Section header */
.section-header {
    font-size: 1.6rem;
    font-weight: 700;
    color: #e9d5ff;
    border-left: 4px solid #7c3aed;
    padding-left: 14px;
    margin-bottom: 20px;
}

/* Chat messages */
.chat-user {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    word-wrap: break-word;
    line-height: 1.6;
}

.chat-ai {
    background: linear-gradient(135deg, #1e1b4b, #2d2369);
    color: #e9d5ff;
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    margin: 8px 0;
    max-width: 80%;
    word-wrap: break-word;
    line-height: 1.6;
}

.chat-label {
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 4px;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(124, 58, 237, 0.5) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #1e1b4b 100%) !important;
}

section[data-testid="stSidebar"] * {
    color: #e9d5ff !important;
}

.stSelectbox > div > div {
    background-color: #1e1b4b !important;
    border-color: rgba(167,139,250,0.3) !important;
    color: #e9d5ff !important;
}

.stTextArea > div > textarea {
    background-color: #1e1b4b !important;
    border-color: rgba(167,139,250,0.3) !important;
    color: #e9d5ff !important;
}

.stTextInput > div > input {
    background-color: #1e1b4b !important;
    border-color: rgba(167,139,250,0.3) !important;
    color: #e9d5ff !important;
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
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🚀 TURING NOVA AI</div>
        <div class="hero-subtitle">THE NEXT GEN AI PLATFORM — pick a tool and start creating.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Choose Your Tool</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="tool-card">
            <span class="tool-icon">💬</span>
            <div class="tool-title">Text to Text</div>
            <div class="tool-desc">Have a full conversation with an AI assistant. Ask questions, get explanations, brainstorm ideas, or just chat.</div>
            <span class="badge">AI Chatbot</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Chatbot →", key="btn_chat", use_container_width=True):
            st.session_state["current_page"] = "chatbot"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="tool-card">
            <span class="tool-icon">💻</span>
            <div class="tool-title">Text to Code</div>
            <div class="tool-desc">Describe what you want to build and get clean, executable code in the language of your choice — instantly.</div>
            <span class="badge">Code Generator</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Code Generator →", key="btn_code", use_container_width=True):
            st.session_state["current_page"] = "codegen"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="tool-card">
            <span class="tool-icon">🎨</span>
            <div class="tool-title">Image Generator</div>
            <div class="tool-desc">Turn any text prompt into a stunning AI-generated image. Customize size and download your creation instantly.</div>
            <span class="badge">Pollinations AI</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Image Generator →", key="btn_img", use_container_width=True):
            st.session_state["current_page"] = "imagegen"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Page: Text-to-Text Chatbot
# ──────────────────────────────────────────────
def page_chatbot():
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
                <div style="display:flex; justify-content:flex-end; margin:6px 0;">
                    <div class="chat-user">
                        <div class="chat-label">You</div>
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-start; margin:6px 0;">
                    <div class="chat-ai">
                        <div class="chat-label">🤖 AI</div>
                        {msg['content'].replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👋 Say something to start the conversation!")

    st.markdown("---")

    # Input area
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area("Your message:", height=100, placeholder="Type your message here...")
        col_send, col_clear = st.columns([4, 1])
        with col_send:
            send = st.form_submit_button("Send 🚀", use_container_width=True)
        with col_clear:
            clear = st.form_submit_button("Clear 🗑️", use_container_width=True)

    if clear:
        st.session_state["chat_history"] = []
        st.rerun()

    if send:
        if not user_input.strip():
            st.warning("Please type a message first.")
        else:
            # Append user message
            st.session_state["chat_history"].append({"role": "user", "content": user_input.strip()})

            # Build messages for API (system prompt + full history)
            api_messages = [
                {"role": "system", "content": "You are a helpful, friendly, and knowledgeable AI assistant. Answer clearly and concisely."}
            ] + st.session_state["chat_history"]

            with st.spinner("AI is thinking..."):
                response = call_openrouter(api_messages)
                content = extract_content(response)

            if content is None:
                st.error(f"Error: {response.get('error', 'Unexpected response format.')}")
                # Remove the user message we just added since it didn't go through
                st.session_state["chat_history"].pop()
            else:
                st.session_state["chat_history"].append({"role": "assistant", "content": content})

            st.rerun()


# ──────────────────────────────────────────────
# Page: Text-to-Code Generator
# ──────────────────────────────────────────────
def page_codegen():
    st.markdown('<div class="section-header">💻 AI Code Generator</div>', unsafe_allow_html=True)
    st.markdown("Describe what you want to build and get clean, executable code — instantly.")

    col1, col2 = st.columns([1, 3])

    with col1:
        language = st.selectbox(
            "Language",
            [
                "Python", "Java", "C++", "JavaScript", "Go", "Rust",
                "TypeScript", "SQL", "HTML/CSS", "Shell Script",
                "C#", "PHP", "Ruby", "Swift", "Kotlin", "GDScript", "C",
            ]
        )

    with col2:
        prompt_text = st.text_area("Describe what you want to build:", height=150,
                                   placeholder="e.g. A Python function that sorts a list of dictionaries by a given key")

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

            with st.spinner("Writing code..."):
                response = call_openrouter(messages)
                content = extract_content(response)

            if content is None:
                st.error(f"Error: {response.get('error', 'Unexpected response format.')}")
            else:
                st.subheader("Generated Code:")
                st.code(content, language=language.lower().replace("/", "").replace(" ", ""))
                st.success("✅ Code generated successfully!")


# ──────────────────────────────────────────────
# Page: AI Image Generator (Stable Horde)
# ──────────────────────────────────────────────
def page_imagegen():
    import base64

    HORDE_URL = "https://stablehorde.net/api/v2"
    HORDE_HEADERS = {
        "apikey": "0000000000",          # anonymous – no sign-up needed
        "Content-Type": "application/json",
        "Client-Agent": "TuringNovaAI:1.0:contact@turignova.ai",
    }

    st.markdown('<div class="section-header">🎨 AI Image Generator</div>', unsafe_allow_html=True)
    st.markdown("Enter a text prompt below and generate a stunning AI image in seconds.")

    st.markdown("---")

    prompt = st.text_input(
        "📝 Image Prompt",
        placeholder="e.g. A futuristic city at sunset, neon lights, cyberpunk style, ultra detailed",
    )

    col_w, col_h, col_btn = st.columns([1, 1, 2])
    with col_w:
        width = st.selectbox("Width (px)", [512, 768], index=0)
    with col_h:
        height = st.selectbox("Height (px)", [512, 768], index=0)
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        generate = st.button("🖼️ Generate Image", type="primary", use_container_width=True)

    if generate:
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt before generating.")
        else:
            # ── Step 1: Submit generation job ──────────────────────
            payload = {
                "prompt": prompt.strip(),
                "params": {
                    "width": width,
                    "height": height,
                    "steps": 15,                        # conform to requirements
                    "sampler_name": "k_euler",
                    "cfg_scale": 7,
                },
                "nsfw": False,
                "censor_nsfw": True,
                "models": ["stable_diffusion"],
            }

            try:
                submit_r = requests.post(
                    f"{HORDE_URL}/generate/async",
                    json=payload,
                    headers=HORDE_HEADERS,
                    timeout=30,
                )
                submit_r.raise_for_status()
                job_id = submit_r.json().get("id")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not connect to image server: {e}")
                return

            if not job_id:
                st.error("❌ Failed to start generation. Please try again.")
                return

            # ── Step 2: Poll until done ────────────────────────────
            progress_bar = st.progress(0, text="🔄 Waiting for an AI worker...")
            MAX_WAIT = 150   # seconds
            elapsed = 0
            done = False

            # use a spinner to indicate that generation is in progress
            with st.spinner("🔄 Generating image… this may take a minute"):
                while elapsed < MAX_WAIT:
                    time.sleep(5)
                    elapsed += 5
                    try:
                        chk = requests.get(
                            f"{HORDE_URL}/generate/check/{job_id}",
                            headers=HORDE_HEADERS,
                            timeout=10,
                        ).json()
                    except Exception:
                        continue

                    wait_time = chk.get("wait_time", 0)
                    done = chk.get("done", False)
                    pct = min(elapsed / MAX_WAIT, 0.95)
                    progress_bar.progress(pct, text=f"✨ Generating… ~{wait_time}s remaining")

                    if done:
                        break

            progress_bar.progress(1.0, text="✅ Done!")

            if not done:
                st.error("⏰ Timed out. The AI workers are busy — please try again in a moment.")
                return

            # ── Step 3: Fetch the finished image ───────────────────
            try:
                status_r = requests.get(
                    f"{HORDE_URL}/generate/status/{job_id}",
                    headers=HORDE_HEADERS,
                    timeout=30,
                )
                status_r.raise_for_status()
                result = status_r.json()
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not retrieve image: {e}")
                return

            # detect worker faults
            if result.get("faulted", False):
                st.error("Generation faulted on worker. Please try again.")
                return

            generations = result.get("generations", [])
            if not generations:
                st.error("No image returned. The worker may have failed. Please try again.")
                return

            img_b64 = generations[0].get("img")
            if not img_b64:
                st.error("Image generation failed. Try another prompt.")
                return

            # safe to decode now
            try:
                image_bytes = base64.b64decode(img_b64)
            except Exception:
                st.error("Failed to decode image data. The response may be corrupted.")
                return

            st.success("🎉 Image generated successfully!")
            st.image(image_bytes, caption=f'"{prompt.strip()}"', use_container_width=True)
            st.download_button(
                label="⬇️ Download Image",
                data=image_bytes,
                file_name="generated_image.png",
                mime="image/png",
                use_container_width=True,
            )


# ──────────────────────────────────────────────
# Sidebar navigation
# ──────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("### 🚀 Turing Nova AI")
        st.markdown("---")

        pages = {
            "🏠 Home": "home",
            "💬 Text to Text (Chatbot)": "chatbot",
            "💻 Text to Code": "codegen",
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
        st.caption("© 2026 Turing Nova AI · All rights reserved")


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
def main():
    # Default page
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
