# tools/utilities/json_formatter.py
import streamlit as st
import json

def show():
    st.markdown("### 📦 JSON Formatter & Validator")
    st.markdown("---")
    
    json_in = st.text_area("Paste raw JSON here:", height=200)
    indent = st.slider("Indentation Spaces:", 1, 8, 4)
    
    if json_in:
        try:
            data = json.loads(json_in)
            formatted = json.dumps(data, indent=indent, sort_keys=True)
            
            st.success("✅ Valid JSON")
            st.markdown("#### Formatted JSON:")
            st.code(formatted, language='json')
            
            st.download_button(
                label="⬇️ Download Formatted JSON",
                data=formatted,
                file_name="nova_data.json",
                mime="application/json",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ Invalid JSON: {e}")
    else:
        st.info("Paste your JSON code above to format and validate.")
