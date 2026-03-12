# tools/utilities/tts_generator.py
import streamlit as st
from gtts import gTTS
import os
from io import BytesIO

def show():
    st.markdown("### 🎙️ Text to Speech Generator")
    st.markdown('<p style="color:#94a3b8;">Convert your written text into clean, natural audio files.</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    txt = st.text_area("Enter text to convert:", height=150, placeholder="Hello! Welcome to Turing Nova AI.")
    lang = st.selectbox("Select Language:", ["en", "fr", "es", "de", "hi"])
    
    if st.button("🔊 Generate Speech", type="primary", use_container_width=True):
        if not txt.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Converting text to speech..."):
                try:
                    tts = gTTS(text=txt, lang=lang)
                    buf = BytesIO()
                    tts.write_to_fp(buf)
                    st.audio(buf)
                    st.success("Speech generated successfully!")
                    
                    st.download_button(
                        label="⬇️ Download Audio (MP3)",
                        data=buf.getvalue(),
                        file_name="nova_speech.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
