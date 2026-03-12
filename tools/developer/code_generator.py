# tools/developer/code_generator.py
import streamlit as st
import pages.chatbot as chatbot

def show():
    """AI Code Generator powered by OpenRouter."""
    st.markdown("### 💻 AI Code Generator")
    st.markdown('<p style="color:#94a3b8;">High-quality production code powered by Llama 3.2 via OpenRouter.</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    prompt = st.text_area("What would you like to build?", placeholder="e.g. A Python script to scrape news from a website using BeautifulSoup", height=150)
    language = st.selectbox("Target Language:", ["Python", "JavaScript", "React", "HTML/CSS", "Java", "C++", "Go", "SQL"])
    
    if st.button("🚀 Generate Code", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please describe the code you need.")
        else:
            system_msg = {"role": "system", "content": f"You are an expert software engineer. Generate clean, documented, and production-ready {language} code. Wrap the code in a markdown block."}
            user_msg = {"role": "user", "content": prompt}
            
            with st.spinner(f"Generating {language} code..."):
                result = chatbot.call_openrouter([system_msg, user_msg])
                if result:
                    st.markdown(result)
                    st.success("Code generated successfully!")
