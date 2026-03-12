import streamlit as st
import requests
import streamlit.components.v1 as components
import json
import os
import io
from dotenv import load_dotenv
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

load_dotenv()

APP_NAME   = "TURING NOVA AI"
OPENROUTER_API_KEY  = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "stepfun/step-3.5-flash:free"

st.set_page_config(
    page_title="Turing Nova AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────
# Theme initialisation
# ─────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

IS_DARK = st.session_state["theme"] == "dark"

# ─────────────────────────────────────────────────────────────────
# CSS — full design system, theme-aware
# ─────────────────────────────────────────────────────────────────

# ── colour tokens based on theme ──────────────────────────────────
if IS_DARK:
    BG_BASE       = "linear-gradient(135deg,#050010 0%,#0d001f 30%,#000d2e 65%,#050010 100%)"
    SIDEBAR_BG    = "linear-gradient(180deg,#08001a 0%,#160038 50%,#050d28 100%)"
    HERO_BG       = "linear-gradient(135deg,#150128 0%,#2a0d60 35%,#082362 70%,#0b1940 100%)"
    CARD_CHAT_BG  = "linear-gradient(145deg,#160128 0%,#310866 55%,#18164a 100%)"
    CARD_CODE_BG  = "linear-gradient(145deg,#091438 0%,#1a3470 55%,#0d244f 100%)"
    CARD_IMG_BG   = "linear-gradient(145deg,#08201a 0%,#054d38 55%,#08231a 100%)"
    CARD_TTS_BG      = "linear-gradient(145deg,#1a0e00 0%,#4d2500 55%,#2a1500 100%)"
    CARD_RESUME_BG   = "linear-gradient(145deg,#0d001a 0%,#1e0040 55%,#100030 100%)"
    TEXT_PRIMARY  = "#ffffff"
    TEXT_SECONDARY= "#c4b5fd"
    TEXT_MUTED    = "#7c6aad"
    INPUT_BG      = "rgba(8,0,20,0.85)"
    INPUT_BORDER  = "rgba(167,139,250,0.35)"
    DIVIDER       = "rgba(167,139,250,0.12)"
    CHAT_USER_BG  = "linear-gradient(135deg,#5b21b6,#6d28d9,#4338ca)"
    CHAT_AI_BG    = "linear-gradient(135deg,#0f172a,#1e1b4b)"
    CHAT_AI_COLOR = "#e9d5ff"
    CODE_BORDER   = "rgba(59,130,246,0.25)"
    STAT_BG       = "rgba(124,58,237,0.18)"
    STAT_BORDER   = "rgba(167,139,250,0.22)"
    STAT_COLOR    = "#c4b5fd"
else:
    # Light theme — clean, colourful
    BG_BASE       = "linear-gradient(135deg,#f0e7ff 0%,#e8f0ff 30%,#e0f7fa 65%,#f0e7ff 100%)"
    SIDEBAR_BG    = "linear-gradient(180deg,#ede9fe 0%,#ddd6fe 50%,#bfdbfe 100%)"
    HERO_BG       = "linear-gradient(135deg,#4c1d95 0%,#6d28d9 35%,#1d4ed8 70%,#0e7490 100%)"
    CARD_CHAT_BG  = "linear-gradient(145deg,#ede9fe 0%,#ddd6fe 55%,#c4b5fd 100%)"
    CARD_CODE_BG  = "linear-gradient(145deg,#eff6ff 0%,#bfdbfe 55%,#93c5fd 100%)"
    CARD_IMG_BG   = "linear-gradient(145deg,#ecfdf5 0%,#a7f3d0 55%,#6ee7b7 100%)"
    CARD_TTS_BG      = "linear-gradient(145deg,#fff7ed 0%,#fed7aa 55%,#fdba74 100%)"
    CARD_RESUME_BG   = "linear-gradient(145deg,#f5f3ff 0%,#ede9fe 55%,#ddd6fe 100%)"
    TEXT_PRIMARY  = "#1e1b4b"
    TEXT_SECONDARY= "#4c1d95"
    TEXT_MUTED    = "#7c3aed"
    INPUT_BG      = "rgba(255,255,255,0.85)"
    INPUT_BORDER  = "rgba(109,40,217,0.35)"
    DIVIDER       = "rgba(109,40,217,0.15)"
    CHAT_USER_BG  = "linear-gradient(135deg,#7c3aed,#6d28d9,#4f46e5)"
    CHAT_AI_BG    = "linear-gradient(135deg,#f5f3ff,#ede9fe)"
    CHAT_AI_COLOR = "#3730a3"
    CODE_BORDER   = "rgba(37,99,235,0.25)"
    STAT_BG       = "rgba(109,40,217,0.1)"
    STAT_BORDER   = "rgba(109,40,217,0.25)"
    STAT_COLOR    = "#5b21b6"


st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ── Animated background ── */
.stApp {{
    background: {BG_BASE};
    background-size: 400% 400%;
    animation: bgShift 18s ease infinite;
    transition: background 0.5s ease;
}}
@keyframes bgShift {{
    0%   {{ background-position: 0% 50%; }}
    50%  {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* ── Main block container ── */
.main .block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, #7c3aed, #2563eb);
    border-radius: 4px;
}}

/* ── Hero ── */
.hero-container {{
    background: {HERO_BG};
    border-radius: 28px;
    padding: 72px 50px 60px;
    text-align: center;
    margin-bottom: 44px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow:
        0 0 80px rgba(124,58,237,0.28),
        0 0 160px rgba(59,130,246,0.12),
        inset 0 1px 0 rgba(255,255,255,0.07);
}}
.hero-container::before {{
    content:''; position:absolute; top:-50%; left:-15%;
    width:55%; height:180%;
    background: radial-gradient(ellipse, rgba(167,139,250,0.18) 0%, transparent 60%);
    animation: hg1 7s ease-in-out infinite alternate;
    pointer-events: none;
}}
.hero-container::after {{
    content:''; position:absolute; top:-50%; right:-15%;
    width:55%; height:180%;
    background: radial-gradient(ellipse, rgba(56,189,248,0.18) 0%, transparent 60%);
    animation: hg2 7s ease-in-out infinite alternate;
    pointer-events: none;
}}
@keyframes hg1 {{ from{{opacity:.4}} to{{opacity:1}} }}
@keyframes hg2 {{ from{{opacity:1}} to{{opacity:.4}} }}

.hero-eyebrow {{
    display: inline-block;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 999px;
    padding: 5px 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: rgba(255,255,255,0.75);
    text-transform: uppercase;
    margin-bottom: 22px;
    position: relative; z-index: 1;
    backdrop-filter: blur(8px);
    background: rgba(255,255,255,0.06);
    animation: eyebrowPulse 4s ease-in-out infinite;
}}
@keyframes eyebrowPulse {{
    0%,100% {{ box-shadow: 0 0 12px rgba(167,139,250,0.3); }}
    50%      {{ box-shadow: 0 0 28px rgba(167,139,250,0.7), 0 0 50px rgba(56,189,248,0.3); }}
}}

.hero-title {{
    font-family: 'Orbitron', monospace;
    font-size: 3.6rem;
    font-weight: 900;
    background: linear-gradient(90deg, #f9a8d4, #c4b5fd, #93c5fd, #6ee7b7, #fcd34d, #f9a8d4);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleShimmer 5s linear infinite;
    position: relative; z-index: 1;
    line-height: 1.15;
    margin-bottom: 18px;
}}
@keyframes titleShimmer {{
    0%   {{ background-position: 0% 50%; }}
    100% {{ background-position: 300% 50%; }}
}}

.hero-sub {{
    font-size: 1.1rem;
    color: rgba(255,255,255,0.65);
    position: relative; z-index:1;
    max-width: 560px;
    margin: 0 auto 30px;
    line-height: 1.7;
}}

.particles {{
    display: flex; gap: 12px; justify-content: center;
    margin-bottom: 28px; position: relative; z-index:1;
}}
.dot {{ width:9px; height:9px; border-radius:50%; }}
.dp {{ background:#f472b6; animation: dp 2.2s infinite 0s; }}
.dv {{ background:#a78bfa; animation: dp 2.2s infinite 0.35s; }}
.db {{ background:#60a5fa; animation: dp 2.2s infinite 0.7s; }}
.dg {{ background:#34d399; animation: dp 2.2s infinite 1.05s; }}
.dy {{ background:#fbbf24; animation: dp 2.2s infinite 1.4s; }}
@keyframes dp {{
    0%,100% {{ transform:scale(1); opacity:.5; }}
    50%      {{ transform:scale(1.8); opacity:1; box-shadow:0 0 8px currentColor; }}
}}

.chips {{
    display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;
    position: relative; z-index:1;
}}
.chip {{
    background: {STAT_BG};
    border: 1px solid {STAT_BORDER};
    border-radius: 999px;
    padding: 7px 20px;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.8);
    font-weight: 600;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}}
.chip:hover {{
    background: rgba(167,139,250,0.3);
    transform: scale(1.06);
    box-shadow: 0 0 16px rgba(124,58,237,0.4);
}}

/* ── Section header ── */
.sec-head {{
    font-size: 1.45rem;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    padding-left: 16px;
    margin-bottom: 26px;
    position: relative;
    display: inline-block;
}}
.sec-head::before {{
    content:''; position:absolute; left:0; top:0; bottom:0; width:4px;
    border-radius:4px;
    background: linear-gradient(180deg,#f472b6,#a78bfa,#60a5fa,#34d399);
    animation: rbBar 4s linear infinite;
    background-size: 100% 300%;
}}
@keyframes rbBar {{
    0%   {{ background-position: 0% 0%; }}
    100% {{ background-position: 0% 100%; }}
}}

/* ── Tool cards ── */
.tool-card {{
    border-radius: 22px;
    padding: 40px 28px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
    border: 1px solid rgba(255,255,255,0.09);
}}
.tc-chat  {{ background:{CARD_CHAT_BG}; box-shadow:0 8px 30px rgba(167,139,250,0.15); }}
.tc-code  {{ background:{CARD_CODE_BG}; box-shadow:0 8px 30px rgba(59,130,246,0.15); }}
.tc-image {{ background:{CARD_IMG_BG};  box-shadow:0 8px 30px rgba(52,211,153,0.15); }}

.tool-card:hover {{ transform: translateY(-10px) scale(1.02); }}
.tc-chat:hover  {{ box-shadow:0 22px 55px rgba(167,139,250,0.45); border-color:rgba(167,139,250,0.4); }}
.tc-code:hover  {{ box-shadow:0 22px 55px rgba(59,130,246,0.45);  border-color:rgba(59,130,246,0.4); }}
.tc-image:hover {{ box-shadow:0 22px 55px rgba(52,211,153,0.45);  border-color:rgba(52,211,153,0.4); }}

.tool-card::before {{
    content:''; position:absolute; top:-50%; left:-50%; width:200%; height:200%;
    background: conic-gradient(transparent, rgba(255,255,255,0.03), transparent);
    animation: cRotate 8s linear infinite; pointer-events:none;
}}
@keyframes cRotate {{ to {{ transform:rotate(360deg); }} }}

.ti {{
    font-size: 3.6rem; display:block; margin-bottom:18px;
    animation: iconFloat 3.5s ease-in-out infinite;
}}
@keyframes iconFloat {{
    0%,100% {{ transform:translateY(0); }}
    50%      {{ transform:translateY(-9px); }}
}}

.tt {{
    font-size: 1.35rem; font-weight:700;
    color:{TEXT_PRIMARY};
    margin-bottom: 10px;
    position:relative; z-index:1;
}}

.td {{
    font-size: 0.9rem; color: rgba({'255,255,255,0.6' if IS_DARK else '30,27,75,0.65'});
    line-height:1.65; position:relative; z-index:1;
}}

.badge {{
    display:inline-block;
    font-size:0.68rem; font-weight:700;
    padding:5px 16px; border-radius:999px;
    margin-top:18px; letter-spacing:1.2px;
    text-transform:uppercase; position:relative; z-index:1;
}}
.b-purple {{ background:linear-gradient(90deg,#7c3aed,#a855f7); color:#fff; box-shadow:0 0 14px rgba(124,58,237,0.5); }}
.b-blue   {{ background:linear-gradient(90deg,#2563eb,#06b6d4); color:#fff; box-shadow:0 0 14px rgba(37,99,235,0.5); }}
.b-green  {{ background:linear-gradient(90deg,#059669,#10b981); color:#fff; box-shadow:0 0 14px rgba(5,150,105,0.5); }}
.b-orange {{ background:linear-gradient(90deg,#ea580c,#f59e0b); color:#fff; box-shadow:0 0 14px rgba(234,88,12,0.5); }}
.b-indigo {{ background:linear-gradient(90deg,#4338ca,#7c3aed); color:#fff; box-shadow:0 0 14px rgba(67,56,202,0.5); }}

/* ── Resume card ── */
.tc-resume {{ background:{CARD_RESUME_BG}; box-shadow:0 8px 30px rgba(67,56,202,0.15); }}
.tc-resume:hover {{ box-shadow:0 22px 55px rgba(67,56,202,0.45); border-color:rgba(129,140,248,0.4); }}

/* ── Resume result panels ── */
.res-panel {{
    background: {'rgba(255,255,255,0.03)' if IS_DARK else 'rgba(255,255,255,0.7)'};
    border: 1px solid {DIVIDER};
    border-radius: 14px; padding: 20px 22px; margin-bottom: 14px;
    animation: pgIn 0.4s ease;
}}
.res-panel-title {{
    font-size: 0.72rem; font-weight:700; text-transform:uppercase;
    letter-spacing:1.5px; color:{TEXT_MUTED}; margin-bottom:8px;
}}
.res-panel-body {{ color:{TEXT_PRIMARY}; font-size:0.95rem; line-height:1.7; }}

/* ── TTS card ── */
.tc-tts {{ background:{CARD_TTS_BG}; box-shadow:0 8px 30px rgba(234,88,12,0.15); }}
.tc-tts:hover {{ box-shadow:0 22px 55px rgba(234,88,12,0.45); border-color:rgba(251,146,60,0.4); }}

/* ── Audio player ── */
audio {{ width:100% !important; border-radius:12px !important; margin-top:6px; }}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, #7c3aed, #4f46e5, #2563eb) !important;
    background-size: 200% 200% !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.93rem !important;
    letter-spacing: 0.4px !important;
    transition: all 0.3s ease !important;
    animation: btnAnim 5s ease infinite !important;
}}
@keyframes btnAnim {{
    0%,100% {{ background-position:0% 50%; }}
    50%      {{ background-position:100% 50%; }}
}}
.stButton > button:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(124,58,237,0.55) !important;
}}
.stButton > button[kind="secondary"] {{
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(79,70,229,0.12)) !important;
    border: 1px solid rgba(167,139,250,0.28) !important;
    color: {TEXT_SECONDARY} !important;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {DIVIDER} !important;
    transition: background 0.5s ease;
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT_PRIMARY} !important;
}}

/* ── Inputs ── */
.stSelectbox > div > div {{
    background: {INPUT_BG} !important;
    border: 1px solid {INPUT_BORDER} !important;
    color: {TEXT_PRIMARY} !important;
    border-radius: 10px !important;
}}
.stTextArea > div > textarea {{
    background: {INPUT_BG} !important;
    border: 1px solid {INPUT_BORDER} !important;
    color: {TEXT_PRIMARY} !important;
    border-radius: 10px !important;
    transition: border-color 0.3s, box-shadow 0.3s;
}}
.stTextArea > div > textarea:focus {{
    border-color: #a78bfa !important;
    box-shadow: 0 0 22px rgba(167,139,250,0.22) !important;
}}
.stTextInput > div > input {{
    background: {INPUT_BG} !important;
    border: 1px solid {INPUT_BORDER} !important;
    color: {TEXT_PRIMARY} !important;
    border-radius: 10px !important;
}}

/* ── Code block ── */
.stCode, pre {{
    border: 1px solid {CODE_BORDER} !important;
    border-radius: 14px !important;
    box-shadow: 0 0 28px rgba(59,130,246,0.08) !important;
}}

/* ── Chat ── */
.chat-user {{
    background: {CHAT_USER_BG};
    color: #fff;
    border-radius: 20px 20px 4px 20px;
    padding: 14px 20px;
    margin: 8px 0;
    max-width: 78%;
    margin-left: auto;
    line-height: 1.65;
    box-shadow: 0 4px 20px rgba(124,58,237,0.38);
    border: 1px solid rgba(167,139,250,0.25);
    animation: sRight 0.3s ease;
    word-wrap: break-word;
}}
.chat-ai {{
    background: {CHAT_AI_BG};
    color: {CHAT_AI_COLOR};
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 20px 20px 20px 4px;
    padding: 14px 20px;
    margin: 8px 0;
    max-width: 78%;
    line-height: 1.65;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    animation: sLeft 0.3s ease;
    word-wrap: break-word;
}}
@keyframes sRight {{ from{{opacity:0;transform:translateX(18px)}} to{{opacity:1;transform:none}} }}
@keyframes sLeft  {{ from{{opacity:0;transform:translateX(-18px)}} to{{opacity:1;transform:none}} }}

.chat-label {{
    font-size: 0.7rem; font-weight:700; margin-bottom:5px;
    opacity:.7; text-transform:uppercase; letter-spacing:1px;
}}

/* ── Page enter animation ── */
.pg {{
    animation: pgIn 0.4s ease;
}}
@keyframes pgIn {{
    from {{ opacity:0; transform:translateY(14px); }}
    to   {{ opacity:1; transform:none; }}
}}

/* ── Divider ── */
hr {{ border-color: {DIVIDER} !important; }}

/* ── Alerts ── */
.stAlert {{ border-radius: 12px !important; }}

/* ── Theme toggle pill (sidebar) ── */
.theme-pill {{
    display:flex; align-items:center; gap:10px;
    background: {'rgba(255,255,255,0.05)' if IS_DARK else 'rgba(109,40,217,0.08)'};
    border: 1px solid {DIVIDER};
    border-radius: 14px;
    padding: 12px 16px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}}
.theme-pill:hover {{
    background: {'rgba(167,139,250,0.12)' if IS_DARK else 'rgba(109,40,217,0.15)'};
    box-shadow: 0 0 16px rgba(124,58,237,0.2);
}}
.theme-pill-icon {{
    font-size:1.3rem;
    animation: themeSpin 0.5s ease;
}}
@keyframes themeSpin {{ from{{transform:rotate(-30deg)}} to{{transform:none}} }}
.theme-pill-text {{
    font-size: 0.88rem; font-weight: 600; color: {TEXT_PRIMARY};
}}

/* ── Nav logo ── */
.nav-logo {{
    text-align: center; padding: 8px 0 16px;
}}
.nav-logo-title {{
    font-family: 'Orbitron', monospace;
    font-size: 1.05rem; font-weight: 900;
    background: linear-gradient(90deg,#f472b6,#a78bfa,#60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleShimmer 5s linear infinite;
    background-size: 300% 100%;
}}
.nav-logo-sub {{
    font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase;
    color: {TEXT_MUTED}; margin-top: 2px; font-weight: 600;
}}

.footer-cap {{
    text-align:center; font-size:0.68rem; color:{TEXT_MUTED};
    margin-top: 16px; padding-top: 12px;
    border-top: 1px solid {DIVIDER};
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────
def call_openrouter(messages: list, model: str = MODEL) -> dict:
    if not OPENROUTER_API_KEY:
        return {"error": "API Key not found. Please set OPENROUTER_API_KEY in your .env file."}
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": APP_NAME,
    }
    data = {"model": model, "messages": messages}
    try:
        r = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def extract_content(response: dict) -> str | None:
    if "error" in response:
        return None
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None


# ─────────────────────────────────────────────────────────────────
# Text-to-Speech helper
# ─────────────────────────────────────────────────────────────────
# Voice configurations: (gtts lang, gtts tld, slow)
_VOICE_MAP = {
    "Female Voice (Standard)":  ("en", "com",  False),
    "Female Voice (Australian)":("en", "com.au",False),
    "Male Voice (UK)":          ("en", "co.uk", False),
    "Narrator (Slow & Clear)":  ("en", "com",  True),
    "Spanish Voice":            ("es", "es",   False),
    "French Voice":             ("fr", "fr",   False),
}

def generate_speech(text: str, voice: str) -> bytes | None:
    """Convert text to MP3 bytes using gTTS. Returns bytes or None on error."""
    if not GTTS_AVAILABLE:
        return None
    try:
        lang, tld, slow = _VOICE_MAP.get(voice, ("en", "com", False))
        tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────
# Pages
# ─────────────────────────────────────────────────────────────────
def page_home():
    st.markdown('<div class="pg">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-container">
        <div class="hero-eyebrow">✦ Artificial Intelligence Platform</div>
        <div class="hero-title">TURING NOVA AI</div>
        <div class="hero-sub">
            Your all-in-one creative AI suite. Generate ideas, build code, and craft stunning visuals — all in one place.
        </div>
        <div class="particles">
            <span class="dot dp"></span><span class="dot dv"></span>
            <span class="dot db"></span><span class="dot dg"></span>
            <span class="dot dy"></span>
        </div>
        <div class="chips">
            <span class="chip">💬 Conversational AI</span>
            <span class="chip">💻 Code Generation</span>
            <span class="chip">🎨 Visual Creation</span>
            <span class="chip">⚡ Instant Results</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">✦ Select a Tool</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="tool-card tc-chat">
            <span class="ti">💬</span>
            <div class="tt">AI Chatbot</div>
            <div class="td">Have natural conversations with a smart AI assistant. Ask anything, get clear answers, brainstorm ideas, or just talk.</div>
            <span class="badge b-purple">Conversational AI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Chatbot →", key="btn_chat", use_container_width=True):
            st.session_state["current_page"] = "chatbot"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="tool-card tc-code">
            <span class="ti">💻</span>
            <div class="tt">Code Generator</div>
            <div class="td">Describe your idea in plain language and receive clean, production-ready code in any major programming language.</div>
            <span class="badge b-blue">Code AI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Code Generator →", key="btn_code", use_container_width=True):
            st.session_state["current_page"] = "codegen"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="tool-card tc-image">
            <span class="ti">🎨</span>
            <div class="tt">Image Generator</div>
            <div class="td">Transform any text prompt into a breathtaking AI-generated image. Runs entirely in your browser — fast and seamless.</div>
            <span class="badge b-green">Visual AI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Image Generator →", key="btn_img", use_container_width=True):
            st.session_state["current_page"] = "imagegen"
            st.rerun()

    # ── Second row — TTS + Resume (2 cols) ──
    st.markdown("<br>", unsafe_allow_html=True)
    col_tts2, col_res2 = st.columns(2, gap="large")

    with col_tts2:
        st.markdown("""
        <div class="tool-card tc-tts">
            <span class="ti">🎙️</span>
            <div class="tt">Text to Speech</div>
            <div class="td">Turn any written text into natural-sounding speech. Choose a voice style and download the audio in seconds.</div>
            <span class="badge b-orange">Voice AI</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Text to Speech →", key="btn_tts", use_container_width=True):
            st.session_state["current_page"] = "tts"
            st.rerun()

    with col_res2:
        st.markdown("""
        <div class="tool-card tc-resume">
            <span class="ti">📄</span>
            <div class="tt">Resume Analyzer</div>
            <div class="td">Upload your resume and get instant AI-powered feedback — strengths, gaps, skill match, and improvement tips.</div>
            <span class="badge b-indigo">AI Analyzer</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open Resume Analyzer →", key="btn_resume", use_container_width=True):
            st.session_state["current_page"] = "resume"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def page_chatbot():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">💬 AI Chatbot</div>', unsafe_allow_html=True)
    st.caption("Your AI assistant is ready. Ask anything and get instant, thoughtful answers.")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if st.session_state["chat_history"]:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin:8px 0;">
                    <div class="chat-user">
                        <div class="chat-label">🧑 You</div>
                        {msg['content']}
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-start;margin:8px 0;">
                    <div class="chat-ai">
                        <div class="chat-label">🤖 Nova</div>
                        {msg['content'].replace(chr(10), '<br>')}
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("👋 Start the conversation below — Nova is listening!")

    st.markdown("---")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area("", height=110,
            placeholder="Type your message and press Send…")
        c1, c2 = st.columns([5, 1])
        with c1:
            send  = st.form_submit_button("🚀 Send", use_container_width=True)
        with c2:
            clear = st.form_submit_button("🗑️", use_container_width=True)

    if clear:
        st.session_state["chat_history"] = []
        st.rerun()

    if send:
        if not user_input.strip():
            st.warning("Please type a message first.")
        else:
            st.session_state["chat_history"].append({"role": "user", "content": user_input.strip()})
            api_msgs = [
                {"role": "system", "content":
                    "You are Nova, a brilliant, friendly AI assistant. Be helpful, concise, and engaging."}
            ] + st.session_state["chat_history"]
            with st.spinner("Nova is thinking…"):
                resp    = call_openrouter(api_msgs)
                content = extract_content(resp)
            if content is None:
                st.error(f"Something went wrong: {resp.get('error', 'Unexpected response.')}")
                st.session_state["chat_history"].pop()
            else:
                st.session_state["chat_history"].append({"role": "assistant", "content": content})
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def page_codegen():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">💻 Code Generator</div>', unsafe_allow_html=True)
    st.caption("Tell Nova what you want to build and receive clean, ready-to-run code instantly.")

    c1, c2 = st.columns([1, 3])
    with c1:
        language = st.selectbox("Language", [
            "Python", "Java", "C++", "JavaScript", "Go", "Rust",
            "TypeScript", "SQL", "HTML/CSS", "Shell Script",
            "C#", "PHP", "Ruby", "Swift", "Kotlin", "GDScript", "C",
        ])
    with c2:
        prompt_text = st.text_area("Describe what you want to build:", height=150,
            placeholder="e.g. A Python function that reads a CSV file and outputs a summary report")

    if st.button("⚡ Generate Code", type="primary"):
        if not prompt_text.strip():
            st.warning("Please enter a description first.")
        else:
            final_prompt = (
                f"Write only clean, executable {language} code for the following task. "
                f"Output only the code block — no markdown commentary, no extra text.\n\n"
                f"Task: {prompt_text.strip()}"
            )
            messages = [
                {"role": "system", "content": "You are an expert software engineer. Return only the requested code with no extra commentary."},
                {"role": "user",   "content": final_prompt},
            ]
            with st.spinner("Writing your code…"):
                resp    = call_openrouter(messages)
                content = extract_content(resp)
            if content is None:
                st.error(f"Something went wrong: {resp.get('error', 'Unexpected response.')}")
            else:
                st.markdown("#### ✅ Generated Code")
                st.code(content, language=language.lower().replace("/", "").replace(" ", ""))
                st.success(f"🎉 {language} code generated successfully!")

    st.markdown('</div>', unsafe_allow_html=True)


def page_imagegen():
    PUTER_BG    = "#050010" if IS_DARK else "#f5f3ff"
    PUTER_CARD  = "linear-gradient(135deg,#0d0025 0%,#1a0040 50%,#081830 100%)" if IS_DARK else "linear-gradient(135deg,#ede9fe 0%,#ddd6fe 50%,#bfdbfe 100%)"
    PUTER_TEXT  = "#e9d5ff" if IS_DARK else "#3730a3"
    PUTER_INPUT = "rgba(5,0,18,0.85)" if IS_DARK else "rgba(255,255,255,0.9)"
    PUTER_IBORD = "rgba(167,139,250,0.35)" if IS_DARK else "rgba(109,40,217,0.35)"
    PUTER_MUTED = "#7c6aad" if IS_DARK else "#7c3aed"
    CARD_SHADOW = "0 0 70px rgba(124,58,237,0.18),inset 0 1px 0 rgba(255,255,255,0.04)" if IS_DARK \
                  else "0 8px 48px rgba(109,40,217,0.14)"
    CARD_BORD   = "rgba(167,139,250,0.18)" if IS_DARK else "rgba(109,40,217,0.2)"

    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">🎨 Image Generator</div>', unsafe_allow_html=True)
    st.caption("Describe your vision in words and watch it come to life as a stunning AI-generated image.")
    st.markdown("---")

    puter_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<script src="https://js.puter.com/v2/"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Inter',sans-serif;background:transparent;color:{PUTER_TEXT};padding:0;}}
.card{{
  background:{PUTER_CARD};
  border:1px solid {CARD_BORD};
  border-radius:22px;
  padding:32px 28px 26px;
  box-shadow:{CARD_SHADOW};
  position:relative; overflow:hidden;
}}
.card::before{{
  content:''; position:absolute; top:-40%; left:-20%; width:55%; height:180%;
  background:radial-gradient(ellipse,rgba(167,139,250,0.06) 0%,transparent 60%);
  pointer-events:none;
}}
.card::after{{
  content:''; position:absolute; top:-40%; right:-20%; width:55%; height:180%;
  background:radial-gradient(ellipse,rgba(59,130,246,0.06) 0%,transparent 60%);
  pointer-events:none;
}}
.lbl{{
  font-size:0.72rem; font-weight:700; text-transform:uppercase;
  letter-spacing:2px; color:{PUTER_MUTED}; margin-bottom:10px;
}}
.row{{display:flex;gap:10px;margin-bottom:20px;position:relative;z-index:1;}}
#prompt{{
  flex:1;
  background:{PUTER_INPUT};
  border:1px solid {PUTER_IBORD};
  border-radius:12px;
  color:{PUTER_TEXT};
  font-family:'Inter',sans-serif; font-size:0.94rem;
  padding:13px 16px; outline:none;
  transition:border-color .3s,box-shadow .3s;
}}
#prompt::placeholder{{color:{PUTER_MUTED};}}
#prompt:focus{{border-color:#a78bfa;box-shadow:0 0 22px rgba(167,139,250,0.22);}}
#genBtn{{
  background:linear-gradient(135deg,#7c3aed,#4f46e5,#2563eb);
  background-size:200%;
  color:#fff; border:none; border-radius:12px;
  font-family:'Inter',sans-serif; font-size:0.93rem; font-weight:700;
  padding:13px 24px; cursor:pointer; white-space:nowrap;
  transition:transform .25s,box-shadow .25s;
  animation:bg 5s ease infinite;
}}
@keyframes bg{{0%,100%{{background-position:0% 50%;}}50%{{background-position:100% 50%;}}}}
#genBtn:hover:not(:disabled){{transform:translateY(-3px);box-shadow:0 12px 30px rgba(124,58,237,0.55);}}
#genBtn:disabled{{opacity:.55;cursor:not-allowed;}}
#status{{font-size:.86rem;color:#a78bfa;min-height:22px;margin-bottom:14px;
  display:flex;align-items:center;gap:8px;position:relative;z-index:1;}}
.spin{{display:inline-block;width:16px;height:16px;
  border:2px solid rgba(167,139,250,0.25);border-top-color:#a78bfa;
  border-radius:50%;animation:sp .7s linear infinite;}}
@keyframes sp{{to{{transform:rotate(360deg);}}}}
#imgWrap{{width:100%;text-align:center;position:relative;z-index:1;}}
#imgWrap img{{
  max-width:100%; border-radius:18px;
  box-shadow:0 0 0 1px rgba(167,139,250,0.15),0 18px 55px rgba(103,76,230,0.45),0 0 90px rgba(59,130,246,0.15);
  animation:pop .6s cubic-bezier(.34,1.56,.64,1);
}}
@keyframes pop{{from{{opacity:0;transform:scale(.88);}}to{{opacity:1;transform:scale(1);}}}}
#dlBtn{{
  display:none; margin:18px auto 0;
  background:linear-gradient(135deg,#059669,#10b981);
  color:#fff; border:none; border-radius:12px;
  font-family:'Inter',sans-serif; font-size:.9rem; font-weight:700;
  padding:11px 28px; cursor:pointer;
  transition:transform .25s,box-shadow .25s;
}}
#dlBtn:hover{{transform:translateY(-3px);box-shadow:0 10px 28px rgba(5,150,105,0.5);}}
#errMsg{{
  color:#f87171; font-size:.86rem; margin-top:10px; display:none;
  background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.3);
  border-radius:10px; padding:10px 14px;
}}
.dots{{display:flex;gap:8px;margin-bottom:18px;}}
.d{{width:7px;height:7px;border-radius:50%;}}
.d1{{background:#f472b6;animation:dp 2s infinite 0s;}}
.d2{{background:#a78bfa;animation:dp 2s infinite .3s;}}
.d3{{background:#60a5fa;animation:dp 2s infinite .6s;}}
.d4{{background:#34d399;animation:dp 2s infinite .9s;}}
.d5{{background:#fbbf24;animation:dp 2s infinite 1.2s;}}
@keyframes dp{{0%,100%{{transform:scale(1);opacity:.5;}}50%{{transform:scale(1.7);opacity:1;}}}}
</style>
</head>
<body>
<div class="card">
  <div class="dots">
    <span class="d d1"></span><span class="d d2"></span>
    <span class="d d3"></span><span class="d d4"></span><span class="d d5"></span>
  </div>
  <div class="lbl">✦ Describe your image</div>
  <div class="row">
    <input id="prompt" type="text"
      placeholder="e.g. A futuristic city at sunset — neon lights, cinematic, ultra detailed"/>
    <button id="genBtn" onclick="generate()">🖼️ Generate</button>
  </div>
  <div id="status"></div>
  <div id="imgWrap"></div>
  <button id="dlBtn" onclick="downloadImg()">⬇️ Save Image</button>
  <div id="errMsg"></div>
</div>
<script>
let blob=null,prompt_='';
async function generate(){{
  const p_=document.getElementById('prompt'),
        btn=document.getElementById('genBtn'),
        st=document.getElementById('status'),
        iw=document.getElementById('imgWrap'),
        dl=document.getElementById('dlBtn'),
        er=document.getElementById('errMsg');
  const p=p_.value.trim();
  if(!p){{er.textContent='⚠️ Please enter a description first.';er.style.display='block';return;}}
  er.style.display='none'; prompt_=p; blob=null;
  btn.disabled=true; iw.innerHTML=''; dl.style.display='none';
  st.innerHTML='<span class="spin"></span>&nbsp;Creating your image…';
  try{{
    const img=await puter.ai.txt2img(p);
    img.style.maxWidth='100%'; img.style.borderRadius='18px';
    iw.appendChild(img);
    const r=await fetch(img.src); blob=await r.blob();
    dl.style.display='block';
    st.innerHTML='✅ Image ready!';
  }}catch(e){{
    er.textContent='❌ '+( e.message||String(e)); er.style.display='block'; st.innerHTML='';
  }}finally{{ btn.disabled=false; }}
}}
function downloadImg(){{
  if(!blob)return;
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='nova_'+prompt_.slice(0,38).replace(/\\s+/g,'_')+'.png';
  a.click();
}}
document.getElementById('prompt').addEventListener('keydown',e=>{{if(e.key==='Enter')generate();}});
</script>
</body>
</html>"""

    components.html(puter_html, height=540, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# Page: Text to Speech
# ─────────────────────────────────────────────────────────────────
def page_text_to_speech():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">🎙️ Text to Speech</div>', unsafe_allow_html=True)
    st.caption("Type or paste any text and hear it spoken aloud. Pick a voice, generate, and download your audio.")

    if not GTTS_AVAILABLE:
        st.error(
            "📦 The **gTTS** library is not installed. "
            "Please run `pip install gTTS` and restart the app."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown("---")

    # ── Input area
    text_input = st.text_area(
        "📄 Your text:",
        height=180,
        placeholder="Paste or type the text you'd like converted to speech\u2026",
        key="tts_text_input"
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        voice = st.selectbox(
            "🎤 Voice style:",
            list(_VOICE_MAP.keys()),
            key="tts_voice"
        )
    with c2:
        char_count = len(text_input)
        st.metric("Characters", f"{char_count:,}", help="gTTS works best with texts under 5,000 characters.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Generate Speech", type="primary", use_container_width=True):
        if not text_input.strip():
            st.warning("⚠️ Please enter some text first.")
        elif len(text_input.strip()) > 5000:
            st.warning("⚠️ Text is too long. Please keep it under 5,000 characters for best results.")
        else:
            with st.spinner("🎤 Generating speech\u2026"):
                audio_bytes = generate_speech(text_input.strip(), voice)

            if audio_bytes is None:
                st.error("❌ Speech generation failed. Please try again.")
            else:
                st.success("✅ Speech generated successfully!")

                # ── Audio preview
                st.markdown("#### 🔊 Preview")
                st.audio(audio_bytes, format="audio/mp3")

                # ── Download
                safe_name = text_input.strip()[:30].replace(" ", "_").replace("/", "-")
                st.download_button(
                    label="⬇️ Download Audio (.mp3)",
                    data=audio_bytes,
                    file_name=f"nova_speech_{safe_name}.mp3",
                    mime="audio/mpeg",
                    use_container_width=True,
                )

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# Page: AI Resume Analyzer
# ─────────────────────────────────────────────────────────────────
def extract_resume_text(uploaded_file) -> str | None:
    """Extract plain text from a PDF or TXT uploaded file. Returns text or None."""
    fname = uploaded_file.name.lower()
    try:
        if fname.endswith(".txt"):
            return uploaded_file.read().decode("utf-8", errors="ignore")
        elif fname.endswith(".pdf"):
            if not PYPDF2_AVAILABLE:
                return None
            reader = PyPDF2.PdfReader(uploaded_file)
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            ).strip()
        else:
            return None
    except Exception:
        return None


def page_resume_analyzer():
    st.markdown('<div class="pg">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
    st.caption("Upload your resume, optionally specify a target role, and receive instant AI-powered feedback.")

    if not PYPDF2_AVAILABLE:
        st.warning(
            "📦 **PyPDF2** is not installed. PDF parsing is unavailable. "
            "Run `pip install PyPDF2` and restart the app. TXT files will still work."
        )

    st.markdown("---")

    # ── Upload + job role row
    up_col, role_col = st.columns([3, 2])
    with up_col:
        uploaded = st.file_uploader(
            "📎 Upload your resume (PDF or TXT)",
            type=["pdf", "txt"],
            key="resume_file",
            help="PDF and plain-text formats are supported."
        )
    with role_col:
        job_role = st.text_input(
            "🞯 Target job role (optional)",
            placeholder="e.g. Senior Data Scientist",
            key="resume_role"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

    if analyze_btn:
        if uploaded is None:
            st.warning("⚠️ Please upload a resume first.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        resume_text = extract_resume_text(uploaded)

        if resume_text is None:
            st.error("❌ Unsupported file format or could not read the file. Please upload a PDF or TXT.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        if not resume_text.strip():
            st.error("❌ The uploaded file appears to be empty or the text could not be extracted.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        # Truncate to reasonable length for the AI prompt
        resume_snippet = resume_text[:6000]
        role_line = f"Target Job Role: {job_role.strip()}" if job_role.strip() else "No specific job role provided."

        # Build the analysis prompt
        analysis_prompt = f"""You are an expert career coach and resume analyst. Analyze the following resume and provide structured feedback.

{role_line}

RESUME:
{resume_snippet}

Provide your analysis in EXACTLY this format (use these exact headings):

## 📊 Resume Summary
[2-3 sentence overview of the candidate]

## 🛠️ Skills Detected
[Bullet list of technical and soft skills found]

## ✅ Strengths
[Bullet list of 3-5 clear strengths]

## ⚠️ Weaknesses / Gaps
[Bullet list of 3-5 areas that need improvement]

## 💡 Suggestions for Improvement
[Bullet list of 4-6 specific, actionable suggestions]

## 🎯 Job Match Score
[Give a score out of 10 and explain the reasoning. If no job role was given, provide a general employability score.]"""

        # Store prompt + text in session for Puter.js component
        st.session_state["resume_prompt"] = analysis_prompt
        st.session_state["resume_text_len"] = len(resume_text)
        st.session_state["resume_analyzed"] = True

    # ───────────────────────────── Puter.js AI analysis component
    if st.session_state.get("resume_analyzed") and "resume_prompt" in st.session_state:
        prompt_js = st.session_state["resume_prompt"].replace("`", "'").replace("\\", "\\\\")
        word_count = st.session_state.get("resume_text_len", 0)

        # Colour tokens for HTML component
        CB  = "#050010" if IS_DARK else "#f8f7ff"
        CBG = "linear-gradient(135deg,#0d0025 0%,#1a0045 50%,#08153a 100%)" if IS_DARK \
              else "linear-gradient(135deg,#f0ecff 0%,#e8e0ff 50%,#ddd6fe 100%)"
        CT  = "#e9d5ff" if IS_DARK else "#1e1b4b"
        CM  = "#7c6aad" if IS_DARK else "#5b21b6"
        CIB = "rgba(8,0,20,0.8)" if IS_DARK else "rgba(255,255,255,0.9)"
        CBD = "rgba(119,89,217,0.18)" if IS_DARK else "rgba(109,40,217,0.1)"
        CBR = "rgba(167,139,250,0.2)" if IS_DARK else "rgba(109,40,217,0.2)"

        html_component = f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'/>
<script src='https://js.puter.com/v2/'></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Inter',sans-serif;background:transparent;color:{CT};padding:0;}}
.card{{background:{CBG};border:1px solid {CBR};border-radius:20px;padding:28px 26px;
  box-shadow:0 0 60px rgba(67,56,202,0.12);position:relative;overflow:hidden;}}
.card::before{{content:'';position:absolute;top:-40%;left:-20%;width:55%;height:180%;
  background:radial-gradient(ellipse,rgba(124,58,237,0.06) 0%,transparent 60%);pointer-events:none;}}
#analyzeBtn{{width:100%;background:linear-gradient(135deg,#4338ca,#6d28d9);
  background-size:200%;color:#fff;border:none;border-radius:12px;
  font-family:'Inter',sans-serif;font-size:0.97rem;font-weight:700;
  padding:14px 24px;cursor:pointer;margin-bottom:18px;
  transition:transform .25s,box-shadow .25s;animation:bg 5s ease infinite;}}
@keyframes bg{{0%,100%{{background-position:0% 50%;}}50%{{background-position:100% 50%;}} }}
#analyzeBtn:hover:not(:disabled){{transform:translateY(-3px);box-shadow:0 12px 30px rgba(67,56,202,0.5);}}
#analyzeBtn:disabled{{opacity:.55;cursor:not-allowed;}}
#status{{font-size:.86rem;color:#a78bfa;min-height:22px;margin-bottom:18px;
  display:flex;align-items:center;gap:8px;}}
.spin{{display:inline-block;width:16px;height:16px;
  border:2px solid rgba(167,139,250,0.25);border-top-color:#a78bfa;
  border-radius:50%;animation:sp .7s linear infinite;}}
@keyframes sp{{to{{transform:rotate(360deg);}}}}
#result{{display:none;}}
.section{{background:{CBD};border:1px solid {CBR};
  border-radius:14px;padding:18px 20px;margin-bottom:12px;
  animation:fadeIn .4s ease;}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.section-icon{{font-size:1.1rem;margin-right:6px;}}
.section-title{{font-size:.7rem;font-weight:700;text-transform:uppercase;
  letter-spacing:1.5px;color:{CM};margin-bottom:8px;}}
.section-body{{font-size:.93rem;line-height:1.75;color:{CT};white-space:pre-wrap;word-break:break-word;}}
#dlBtn{{width:100%;margin-top:14px;background:linear-gradient(135deg,#059669,#10b981);
  color:#fff;border:none;border-radius:12px;
  font-family:'Inter',sans-serif;font-size:.92rem;font-weight:700;
  padding:12px 24px;cursor:pointer;display:none;
  transition:transform .25s,box-shadow .25s;}}
#dlBtn:hover{{transform:translateY(-3px);box-shadow:0 10px 26px rgba(5,150,105,0.45);}}
#errMsg{{color:#f87171;font-size:.86rem;margin-top:10px;display:none;
  background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);
  border-radius:10px;padding:10px 14px;}}
.meta{{font-size:.75rem;color:{CM};margin-bottom:14px;}}
</style>
</head>
<body>
<div class='card'>
  <div class='meta'>📄 Resume loaded &nbsp;·&nbsp; {word_count:,} characters extracted</div>
  <button id='analyzeBtn' onclick='runAnalysis()'>🧠 Run AI Analysis</button>
  <div id='status'></div>
  <div id='result'></div>
  <button id='dlBtn' onclick='downloadReport()'>⬇️ Download Report (.txt)</button>
  <div id='errMsg'></div>
</div>
<script>
const PROMPT = `{prompt_js}`;
let reportText = '';
async function runAnalysis() {{
  const btn=document.getElementById('analyzeBtn'),
        st=document.getElementById('status'),
        res=document.getElementById('result'),
        dl=document.getElementById('dlBtn'),
        er=document.getElementById('errMsg');
  er.style.display='none'; res.style.display='none'; dl.style.display='none';
  btn.disabled=true;
  st.innerHTML='<span class="spin"></span>&nbsp;✨ Analyzing your resume… this may take a moment';
  try {{
    const response = await puter.ai.chat(PROMPT);
    const text = typeof response === 'string' ? response
                 : (response?.message?.content || response?.content || JSON.stringify(response));
    reportText = text;
    res.innerHTML = renderSections(text);
    res.style.display='block';
    dl.style.display='block';
    st.innerHTML='✅&nbsp;Analysis complete!';
  }} catch(e) {{
    er.textContent='❌ Analysis failed: '+(e.message||String(e));
    er.style.display='block';
    st.innerHTML='';
  }} finally {{ btn.disabled=false; }}
}}
function renderSections(md) {{
  const iconMap = {{
    'Resume Summary':'📊',
    'Skills Detected':'🛠️',
    'Strengths':'✅',
    'Weaknesses':'⚠️',
    'Suggestions':'💡',
    'Job Match':'🎯',
  }};
  const parts = md.split(/^## /m).filter(Boolean);
  return parts.map(p => {{
    const nl = p.indexOf('\\n');
    const title = nl>-1 ? p.slice(0,nl).replace(/^#+\s*/,'').trim() : p.trim();
    const body  = nl>-1 ? p.slice(nl+1).trim() : '';
    const icon  = Object.entries(iconMap).find(([k])=>title.includes(k))?.[1] || '•';
    return `<div class='section'>
      <div class='section-title'><span class='section-icon'>${{icon}}</span>${{title}}</div>
      <div class='section-body'>${{body.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
                                     .replace(/^[*-]\s+/gm,'• ')}}</div>
    </div>`;
  }}).join('');
}}
function downloadReport() {{
  if(!reportText) return;
  const a=document.createElement('a');
  a.href='data:text/plain;charset=utf-8,'+encodeURIComponent(reportText);
  a.download='nova_resume_analysis.txt';
  a.click();
}}
</script>
</body>
</html>"""

        components.html(html_component, height=900, scrolling=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="nav-logo">
            <div class="nav-logo-title">🚀 TURING NOVA AI</div>
            <div class="nav-logo-sub">Next Gen AI Platform</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Theme toggle
        theme_icon  = "🌙" if IS_DARK else "☀️"
        theme_label = "Switch to Light Mode" if IS_DARK else "Switch to Dark Mode"
        theme_next  = "light" if IS_DARK else "dark"

        if st.button(f"{theme_icon}  {theme_label}", key="theme_toggle", use_container_width=True):
            st.session_state["theme"] = theme_next
            st.rerun()

        st.markdown("---")

        # Navigation
        pages = {
            "🏠  Home":            "home",
            "💬  AI Chatbot":      "chatbot",
            "💻  Code Generator":  "codegen",
            "🎨  Image Generator": "imagegen",
            "🎙️  Text to Speech":  "tts",
            "📄  Resume Analyzer": "resume",
        }
        for label, key in pages.items():
            is_active = st.session_state.get("current_page", "home") == key
            if st.button(label, key=f"nav_{key}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state["current_page"] = key
                st.rerun()

        st.markdown(f'<div class="footer-cap">© 2026 Turing Nova AI</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────
def main():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    sidebar()

    page = st.session_state["current_page"]
    if   page == "home":     page_home()
    elif page == "chatbot":  page_chatbot()
    elif page == "codegen":  page_codegen()
    elif page == "imagegen": page_imagegen()
    elif page == "tts":      page_text_to_speech()
    elif page == "resume":   page_resume_analyzer()


if __name__ == "__main__":
    main()
