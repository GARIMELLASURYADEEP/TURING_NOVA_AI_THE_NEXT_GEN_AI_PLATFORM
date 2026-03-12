# tools/text_factory.py
import streamlit as st
import core.ui as ui

def render_text_tool(name, icon, system_prompt, placeholder="Enter details here...", text_area_label="Your Input:"):
    """Generic factory for text-based AI tools using Puter.ai.chat."""
    ACCENT = st.session_state.get("accent_color", "#6366f1")
    st.markdown(f"### {icon} {name}")
    st.markdown("---")
    
    user_input = st.text_area(text_area_label, placeholder=placeholder, height=150)
    
    if st.button(f"✨ Generate {name}", type="primary", use_container_width=True):
        if not user_input.strip():
            st.warning("Please provide some input.")
        else:
            prompt = f"{system_prompt}\n\nUser Input: {user_input}"
            
            # Puter JS Component for text generation
            html_content = f"""
            <div id="output" style="color:var(--text-pri); font-family:sans-serif; line-height:1.6; whitespace:pre-wrap;">
                <div style="display:flex; align-items:center; gap:10px; color:#94a3b8;">
                    <div class="spin" style="width:20px;height:20px;border:2px solid #334155;border-top-color:#fff;border-radius:50%;animation:sp .8s linear infinite;"></div>
                    AI is writing...
                </div>
            </div>
            <style>@keyframes sp{{to{{transform:rotate(360deg);}}}}</style>
            <script>
            async function run() {{
                try {{
                    const response = await puter.ai.chat(`{prompt.replace("`","'").replace("\\","\\\\")}`);
                    const content = typeof response === 'string' ? response : (response?.message?.content || response?.content || '');
                    document.getElementById('output').innerHTML = content.replace(/\\n/g, '<br>');
                }} catch(e) {{
                    document.getElementById('output').innerHTML = '<span style="color:#ef4444;">Error: ' + e.message + '</span>';
                }}
            }}
            run();
            </script>
            """
            ui.puter_component(html_content, height=400)
