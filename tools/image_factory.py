# tools/image_factory.py
import streamlit as st
import core.ui as ui

def render_image_tool(name, icon, prompt_prefix, placeholder="Describe what you want to create..."):
    """Generic factory for image-based AI tools using Puter.ai.txt2img."""
    ACCENT = st.session_state.get("accent_color", "#6366f1")
    st.markdown(f"### {icon} {name}")
    st.markdown("---")
    
    user_prompt = st.text_input("🎨 Style/Subject:", placeholder=placeholder)
    
    if st.button(f"🪄 Generate {name}", type="primary", use_container_width=True):
        if not user_prompt.strip():
            st.warning("Please provide a description.")
        else:
            full_prompt = f"{prompt_prefix}: {user_prompt}"
            
            # Puter JS Component for image generation
            html_content = f"""
            <div id="status" style="color:#94a3b8; font-family:sans-serif; margin-bottom:15px; display:flex; align-items:center; gap:10px; justify-content:center;">
                <div class="spin" style="width:16px;height:16px;border:2px solid #334155;border-top-color:#fff;border-radius:50%;animation:sp .8s linear infinite;"></div>
                AI is drawing your {name.lower()}...
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:20px;">
                <img id="res" style="width:100%; max-width:400px; border-radius:18px; display:none; border:1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);" />
                <a id="dl" class="btn" style="display:none; background:{ACCENT}; color:#fff; text-decoration:none; padding:12px 30px; border-radius:12px; font-weight:700; font-family:sans-serif; transition: all 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">⬇️ Download Full Resolution</a>
                <button onclick="window.location.reload()" id="gen-again" class="btn" style="display:none; background:transparent; border:1px solid {ACCENT}; color:{ACCENT}; padding:10px 24px; border-radius:12px; font-weight:700; font-family:sans-serif; cursor:pointer;">🔄 Generate Again</button>
            </div>
            
            <style>
            @keyframes sp{{to{{transform:rotate(360deg);}}}}
            .btn:hover {{ opacity: 0.9; transform: translateY(-2px); }}
            </style>
            <script>
            async function run() {{
                try {{
                    const image = await puter.ai.txt2img(`{full_prompt.replace("`","'").replace("\\","\\\\")}`);
                    const img = document.getElementById('res');
                    const dl = document.getElementById('dl');
                    const reg = document.getElementById('gen-again');
                    img.src = image.src;
                    img.style.display = 'block';
                    dl.href = image.src;
                    dl.download = '{name.replace(" ","_").lower()}.png';
                    dl.style.display = 'inline-block';
                    // reg.style.display = 'inline-block';
                    document.getElementById('status').innerHTML = '<span style="color:#10b981; font-weight:700; font-family:sans-serif;">✅ Generation Complete!</span>';
                }} catch(e) {{
                    console.error("Image Error:", e);
                    let errorMsg = e.message || "Unknown error";
                    if (errorMsg.includes("balance") || errorMsg.includes("funding")) {{
                        document.getElementById('status').innerHTML = `⚠️ Low Balance. <button onclick="window.parent.switchAccount()" style="background:#ef4444; border:none; color:white; padding:4px 8px; border-radius:4px; cursor:pointer;">Switch Puter Account</button>`;
                    }} else {{
                        document.getElementById('status').innerHTML = '<span style="color:#ef4444; font-family:sans-serif;">Error: ' + errorMsg + '</span>';
                    }}
                }}
            }}
            run();
            </script>
            """
            ui.puter_component(html_content, height=650)
