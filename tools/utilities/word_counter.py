# tools/utilities/word_counter.py
import streamlit as st

def show():
    st.markdown("### 🔢 Word & Character Counter")
    st.markdown("---")
    
    txt = st.text_area("Paste text to analyze:", height=200)
    
    if txt:
        words = len(txt.split())
        chars = len(txt)
        sentences = txt.count('.') + txt.count('!') + txt.count('?')
        lines = txt.count('\n') + 1 if txt else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Words", words)
        col2.metric("Characters", chars)
        col3.metric("Sentences", sentences)
        col4.metric("Lines", lines)
        
        # Additional Stats
        st.markdown("---")
        st.markdown(f"**Estimated Reading Time:** {max(1, round(words/200))} minute(s)")
    else:
        st.info("Paste some text above to see statistics.")
