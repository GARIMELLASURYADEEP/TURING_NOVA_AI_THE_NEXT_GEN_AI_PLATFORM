# tools/developer/website_generator.py
import streamlit as st
import core.ui as ui
import config

def show():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown('### 🌐 AI Website Generator')
    st.caption("Generate a complete, responsive HTML/CSS site instantly with Puter.js.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        desc = st.text_area("Describe your website:", height=100, placeholder="e.g. A portfolio for a landscape photographer", key="web_desc")
    with col2:
        style = st.selectbox("Style:", ["Modern", "Minimal", "Dark", "Portfolio"], key="web_style")
        theme = st.selectbox("Theme:", ["Vibrant", "Pastel", "Corporate"], key="web_theme")

    if st.button("⚡ Build Website", type="primary", use_container_width=True):
        if not desc.strip():
            st.warning("Please enter a description.")
        else:
            # We use a stable state-preserved Puter component
            ACCENT = st.session_state.get("accent_color", "#6366f1")
            
            html_content = f"""
            <style>
            .status-msg{{font-family:sans-serif;color:#94a3b8;display:flex;align-items:center;gap:10px;margin:20px 0;}}
            .spin{{width:20px;height:20px;border:2px solid #334155;border-top-color:#fff;border-radius:50%;animation:sp .8s linear infinite;}}
            @keyframes sp{{to{{transform:rotate(360deg);}}}}
            #preview{{width:100%;height:600px;border:4px solid rgba(255,255,255,0.05);border-radius:12px;display:none;margin-top:20px;background:#fff;}}
            .btn{{background:{ACCENT};color:#fff;padding:12px 24px;border-radius:8px;font-weight:700;display:none;text-decoration:none;margin-top:15px;text-align:center;font-family:sans-serif;}}
            </style>
            
            <div id="status"><div class="status-msg"><div class="spin"></div>Building your site...</div></div>
            <iframe id="preview" sandbox="allow-scripts allow-forms allow-same-origin"></iframe>
            <a id="dl" class="btn">⬇️ Download HTML Site</a>
            
            <script>
            async function build() {{
                try {{
                    const prompt = `Create a complete, responsive, single-page website with HTML and internal CSS for: {desc.replace("'","\\'").replace("`","\\'").replace("\\","\\\\")}. Style: {style}, Theme: {theme}. Return only the HTML code.`;
                    const response = await puter.ai.chat(prompt);
                    let html = typeof response === 'string' ? response : (response?.message?.content || '');
                    html = html.replace(/```html\\n/g, '').replace(/```\\n/g, '').replace(/```/g, '').trim();
                    
                    const preview = document.getElementById('preview');
                    const dl = document.getElementById('dl');
                    preview.srcdoc = html;
                    preview.style.display = 'block';
                    
                    const blob = new Blob([html], {{type: 'text/html'}});
                    dl.href = URL.createObjectURL(blob);
                    dl.download = 'website.html';
                    dl.style.display = 'inline-block';
                    
                    document.getElementById('status').innerHTML = '<div style="color:#10b981;font-weight:700;font-family:sans-serif;">✅ Website Ready!</div>';
                }} catch(e) {{
                    document.getElementById('status').innerHTML = '<div style="color:#ef4444;font-family:sans-serif;">Error: '+e.message+'</div>';
                }}
            }}
            build();
            </script>
            """
            ui.puter_component(html_content, height=800)
    st.markdown('</div>', unsafe_allow_html=True)
