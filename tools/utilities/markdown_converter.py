# tools/utilities/markdown_converter.py
import streamlit as st
import html2text

def show():
    st.markdown("### ⬇️ HTML to Markdown Converter")
    st.markdown("---")
    
    html_input = st.text_area("Paste HTML Code:", height=200, placeholder="<p>Hello <b>World</b></p>")
    
    if st.button("🔄 Convert to Markdown", use_container_width=True):
        if not html_input.strip():
            st.warning("Please paste some HTML.")
        else:
            try:
                h = html2text.HTML2Text()
                h.ignore_links = False
                h.bypass_tables = False
                md = h.handle(html_input)
                
                st.markdown("#### Resulting Markdown:")
                st.code(md, language='markdown')
                
                st.download_button(
                    label="⬇️ Download Markdown (.md)",
                    data=md,
                    file_name="converted.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Conversion Error: {e}")
