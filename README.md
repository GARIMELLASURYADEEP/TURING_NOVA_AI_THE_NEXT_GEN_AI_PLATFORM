# 🚀 TURING NOVA AI — The Next Gen AI Platform

A vibrant, fully animated AI platform built with **Streamlit** featuring three powerful tools:

| Tool | Description | Powered By |
|------|-------------|------------|
| 💬 **AI Chatbot** | Full conversational AI — ask anything, brainstorm, get answers | OpenRouter API |
| 💻 **Code Generator** | Describe a task → get clean, executable code in 17+ languages | OpenRouter API |
| 🎨 **Image Generator** | Text prompt → stunning AI-generated image, browser-native | Puter.js AI |

## ✨ Features

- 🌈 **Fully colorful & animated UI** — gradient hero, floating particles, color-coded tool cards
- 🔄 **Animated backgrounds** — shifting gradients, glowing elements, smooth page transitions
- 💬 **Persistent chat history** per session
- 🖼️ **In-browser image generation** via Puter.js (no API key required for images)
- ⚡ **Instant code generation** across Python, Java, C++, JS, Go, Rust, TypeScript and more

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
> Get a free API key at [openrouter.ai](https://openrouter.ai)

### 3. Run the App
```bash
streamlit run app.py
```

## 🏗️ Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io)
- **AI Backend (Chat + Code)**: [OpenRouter API](https://openrouter.ai) — `stepfun/step-3.5-flash:free`
- **AI Backend (Images)**: [Puter.js](https://puter.com) — browser-native, no key needed
- **Styling**: Custom CSS with keyframe animations, glassmorphism, gradients

## 📁 Project Structure

```
streamlitcodegenerator/
├── app.py            # Main application
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed)
├── .gitignore        # Ignores .env and cache
└── README.md         # This file
```

---
© 2026 Turing Nova AI · Built with ❤️
