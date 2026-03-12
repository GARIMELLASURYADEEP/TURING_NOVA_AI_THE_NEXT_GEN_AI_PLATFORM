# tools/education/resume_analyzer.py
import streamlit as st
import PyPDF2
from io import BytesIO
from tools.text_factory import render_text_tool

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def show():
    st.markdown("### 📄 Resume Analyzer")
    st.markdown('<p style="color:#94a3b8;">Upload your resume (PDF) for a deep dive AI analysis and optimization tips.</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type="pdf")
    
    if uploaded_file:
        with st.status("🔍 Processing Resume...", expanded=True) as status:
            text = extract_text_from_pdf(uploaded_file)
            if text:
                st.write("✅ Text extracted. Preparing for AI analysis...")
                status.update(label="✨ Analysis in progress...", state="running")
                
                # Now use the text factory logic manually to provide the specific analysis prompt
                st.markdown("#### 📈 AI Analysis & Recommendations")
                
                # We inject the text into the Puter JS component
                # We use a summarized version of the text if it's too long
                preview_text = text[:4000].replace("`","'").replace("\\","\\\\")
                
                html_content = f"""
                <div id="analysis" style="color:var(--text-pri); font-family:sans-serif; line-height:1.6; whitespace:pre-wrap;">
                    <div style="display:flex; align-items:center; gap:10px; color:#94a3b8;">
                        <div class="spin" style="width:20px;height:20px;border:2px solid #334155;border-top-color:#fff;border-radius:50%;animation:sp .8s linear infinite;"></div>
                        AI is analyzing your resume...
                    </div>
                </div>
                <style>@keyframes sp{{to{{transform:rotate(360deg);}}}}</style>
                <script>
                async function run() {{
                    try {{
                        const prompt = `Act as an expert technical recruiter and career coach. Thoroughly analyze the following resume text. Provide: 1. A summary of strengths. 2. Critical gaps or weaknesses. 3. Specific suggestions for improvement (keywords, formatting, impact). 4. A score from 1-10 for the role described (if applicable, else for general industry standard). \\n\\nResume Content: {preview_text}`;
                        const response = await puter.ai.chat(prompt);
                        const content = typeof response === 'string' ? response : (response?.message?.content || '');
                        document.getElementById('analysis').innerHTML = content.replace(/\\n/g, '<br>');
                    }} catch(e) {{
                        document.getElementById('analysis').innerHTML = '<span style="color:#ef4444;">Error: ' + e.message + '</span>';
                    }}
                }}
                run();
                </script>
                """
                from core.ui import puter_component
                puter_component(html_content, height=600)
                status.update(label="✅ Analysis Complete", state="complete")
    else:
        st.info("Please upload a PDF file to begin analysis.")
