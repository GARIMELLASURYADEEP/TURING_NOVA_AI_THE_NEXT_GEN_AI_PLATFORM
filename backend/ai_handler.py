# backend/ai_handler.py
import json

def get_standardized_artifact_script(tool_type, prompt, config=None, file_data=None):
    """Standardized JS component for Multimodal AI Generation & Editing."""
    prompt_safe = prompt.replace('"', '\\"').replace('\n', ' ')
    file_data_safe = f'"{file_data}"' if file_data else "null"
    
    # Define specialized rendering logic
    render_logic = ""
    
    if tool_type in ["website", "game", "ui", "invoice"]:
        render_logic = f"""
            const systemPrompt = "You are an expert developer. Return ONLY valid, single-file HTML (including CSS/JS) for the request. No markdown. Just raw code. If it is an invoice, make it look professional with tables and totals.";
            const res = await puter.ai.chat(systemPrompt + " Request: " + "{prompt_safe}");
            let code = typeof res === 'string' ? res : (res.message?.content || '');
            code = code.replace(/```html/g, '').replace(/```/g, '').trim();
            
            document.getElementById('preview-box').innerHTML = '<iframe id="live-frame" style="width:100%; height:500px; border:none; background:white;"></iframe>';
            document.getElementById('live-frame').srcdoc = code;
            
            saveToServer(code, "{tool_type}_" + Date.now() + ".html");
            setupDownload(code, "{tool_type}_project", "zip");
        """
    elif tool_type == "image":
        render_logic = f"""
            const img = await puter.ai.txt2img("{prompt_safe}");
            document.getElementById('preview-box').innerHTML = `<img src="${{img.src}}" style="max-width:100%; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.5);">`;
            setupDownload(img.src, "generated_art.png", "png");
        """
    elif tool_type == "audio":
        voice_style = (config or {}).get("voice", "female")
        render_logic = f"""
            document.getElementById('preview-box').innerHTML = `
                <div style="text-align:center; padding:40px;">
                    <div style="font-size:4rem; margin-bottom:20px;">🎙️</div>
                    <button id="play-btn" style="background:#6366f1; border:none; padding:15px 40px; border-radius:50px; color:white; cursor:pointer; font-weight:700; font-size:1.2rem;">Play Audio ▶️</button>
                    <p id="audio-meta" style="color:#94a3b8; margin-top:20px;">Voice Style: {voice_style.capitalize()}</p>
                </div>
            `;
            const msg = new SpeechSynthesisUtterance("{prompt_safe}");
            document.getElementById('play-btn').onclick = () => {{
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(msg);
            }};
            setupDownload("{prompt_safe}", "script.txt", "txt");
        """
    else: # Text/Default
        render_logic = f"""
            const res = await puter.ai.chat("{prompt_safe}");
            const text = typeof res === 'string' ? res : (res.message?.content || '');
            document.getElementById('preview-box').innerHTML = `<div style="white-space:pre-wrap; background:rgba(0,0,0,0.2); padding:20px; border-radius:12px; border:1px solid rgba(255,255,255,0.05); font-family:monospace;">${{text}}</div>`;
            setupDownload(text, "content.txt", "txt");
        """

    return f"""
    <script src="https://js.puter.com/v2/"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <div style="background:#0b1120; color:white; padding:25px; border-radius:20px; border:1px solid rgba(255,255,255,0.08); font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <div id="ai-status" style="color:#6366f1; font-weight:800; font-size:14px; letter-spacing:0.05em;">⚡ BUILDING ARTIFACT...</div>
            <div id="ai-actions" style="display:none; gap:10px;">
                <button id="main-dl" style="background:#10b981; border:none; padding:10px 22px; border-radius:10px; color:white; cursor:pointer; font-weight:700; font-size:14px;">Download 📦</button>
                <button onclick="copyToClipboard()" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); padding:10px 22px; border-radius:10px; color:white; cursor:pointer; font-size:14px;">Copy 📋</button>
            </div>
        </div>
        <div id="preview-box" style="min-height:300px; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,0.3); border-radius:16px; border:1px dashed rgba(255,255,255,0.1); overflow:hidden;">
            <span style="color:#475569;">Initializing generation...</span>
        </div>
    </div>

    <script>
        let rawContent = "";
        
        async function saveToServer(content, filename) {{
            try {{
                await fetch('http://localhost:8000/api/save-artifact', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ content, filename }})
                }});
            }} catch (e) {{}}
        }}

        function copyToClipboard() {{
            navigator.clipboard.writeText(rawContent);
            alert("Copied to clipboard!");
        }}

        async function setupDownload(content, filename, type) {{
            rawContent = (type === 'png' || type === 'video') ? "Downloaded via link" : content;
            const btn = document.getElementById('main-dl');
            document.getElementById('ai-actions').style.display = 'flex';
            
            btn.onclick = async () => {{
                if(type === 'zip') {{
                    const zip = new JSZip();
                    zip.file("index.html", content);
                    const blob = await zip.generateAsync({{type:"blob"}});
                    saveBlob(blob, filename + ".zip");
                }} else if(type === 'png' || type === 'video') {{
                    const a = document.createElement('a');
                    a.href = content; a.download = filename; a.click();
                }} else {{
                    const blob = new Blob([content], {{type: 'text/plain'}});
                    saveBlob(blob, filename);
                }}
            }};
        }}

        function saveBlob(blob, name) {{
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = name; a.click();
        }}

        (async () => {{
            try {{
                {render_logic}
                document.getElementById('ai-status').innerText = "✅ READY";
            }} catch (e) {{
                document.getElementById('ai-status').innerText = "❌ ERROR";
            }}
        }})();
    </script>
    """

def get_puter_audio_ui(text, voice="female"):
    return get_standardized_artifact_script("audio", text, config={"voice": voice})

def get_puter_image_script(prompt):
    return get_standardized_artifact_script("image", prompt)

def get_puter_preview_ui(prompt):
    return get_standardized_artifact_script("website", prompt)

def get_puter_text_ui(prompt):
    return get_standardized_artifact_script("text", prompt)
