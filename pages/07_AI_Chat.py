# pages/07_AI_Chat.py
import streamlit as st
from backend import utils
from backend import ai_handler

st.set_page_config(page_title="AI Chat - Turing Nova AI", page_icon="💬", layout="wide")
utils.inject_custom_css()
utils.require_auth()

def chat_page():
    st.markdown("<h1>💬 AI Direct Chat</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Powered by decentralized intelligence. No API key required.</p>", unsafe_allow_html=True)

    # Initialize session state for chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "bot", "content": "Hello! I'm your AI assistant. How can I help you today?"}]

    # Escape messages for JS
    import json
    history_json = json.dumps(st.session_state.chat_history)

    # Puter.js Chat Component
    chat_html = f"""
    <script src="https://js.puter.com/v2/"></script>
    <style>
        body {{ background: #05070a; color: white; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; padding: 0; }}
        #chat-container {{ height: 75vh; display: flex; flex-direction: column; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; background: #0b1120; }}
        #messages {{ flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }}
        .msg {{ padding: 12px 18px; border-radius: 12px; max-width: 80%; line-height: 1.5; font-size: 14px; word-wrap: break-word; }}
        .user {{ align-self: flex-end; background: #6366f1; color: white; }}
        .bot {{ align-self: flex-start; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }}
        #input-area {{ padding: 20px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; gap: 10px; }}
        input {{ flex: 1; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px 15px; color: white; outline: none; }}
        button {{ background: #6366f1; border: none; padding: 10px 20px; border-radius: 8px; color: white; cursor: pointer; font-weight: 600; }}
    </style>
    <div id="chat-container">
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="user-input" placeholder="Type your message..." autocomplete="off">
            <button id="send-btn">Send 🚀</button>
        </div>
    </div>
    <script>
        const chat = document.getElementById('messages');
        const input = document.getElementById('user-input');
        const btn = document.getElementById('send-btn');
        let history = {history_json};

        // Load history
        history.forEach(m => addMsg(m.content, m.role, false));

        async function send() {{
            const text = input.value.trim();
            if(!text) return;
            
            input.value = '';
            addMsg(text, 'user');
            
            const botMsg = addMsg("Thinking...", 'bot');
            
            try {{
                const res = await puter.ai.chat(text);
                const content = typeof res === 'string' ? res : (res.message?.content || '');
                botMsg.innerText = content;
                saveMsg(content, 'bot');
            }} catch (e) {{
                botMsg.innerText = "Error: " + e.message;
            }}
            chat.scrollTop = chat.scrollHeight;
        }}

        function addMsg(text, role, save = true) {{
            const div = document.createElement('div');
            div.className = 'msg ' + role;
            div.innerText = text;
            chat.appendChild(div);
            if(save) saveMsg(text, role);
            chat.scrollTop = chat.scrollHeight;
            return div;
        }}

        function saveMsg(content, role) {{
             history.push({{role, content}});
             window.parent.postMessage({{type: 'chat_update', history}}, '*');
        }}

        btn.onclick = send;
        input.onkeypress = (e) => {{ if(e.key === 'Enter') send(); }};
    </script>
    """
    
    st.components.v1.html(chat_html, height=700)

if __name__ == "__main__":
    chat_page()
