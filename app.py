import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="AI Code Generator",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("Settings")
    if st.button("Clear Output"):
        st.session_state.clear()
        st.rerun()

# Main UI
st.title("🤖 AI Code Generator")
st.markdown("Generate code using the **OpenRouter API**.")

# Input fields
col1, col2 = st.columns([1, 3])

with col1:
    language = st.selectbox(
        "Select Language",
        ["Python", "Java", "C++", "JavaScript", "Go", "Rust", "TypeScript", "SQL", "HTML/CSS", "Shell Script"]
    )

with col2:
    prompt_text = st.text_area("Enter your coding problem:", height=150)

generate_btn = st.button("Generate Code", type="primary")

# Initialize session state for generated code
if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

def generate_code(language, prompt):
    api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
    
    if not api_key:
        return "Error: OPENROUTER_API_KEY not found. Please set it in .env or Streamlit secrets."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "Streamlit Code Gen", # Optional. Shows in rankings on openrouter.ai.
    }
    
    # Construct the prompt
    final_prompt = f"Write only executable {language} code for the following task. Do not include explanation.\n\nTask: {prompt}"

    data = {
        "model": "stepfun/step-3.5-flash:free",
        "messages": [
            {"role": "user", "content": final_prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: No content returned from API. Response: {result}"
            
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error: {http_err}\nResponse content: {response.text}"
    except Exception as err:
        return f"An error occurred: {err}"

# Handle generation
if generate_btn:
    if not prompt_text:
        st.warning("Please enter a coding problem.")
    else:
        with st.spinner("Generating code..."):
            generated_code = generate_code(language, prompt_text)
            st.session_state.generated_code = generated_code

# Display result
if st.session_state.generated_code:
    st.subheader("Generated Code")
    st.code(st.session_state.generated_code, language=language.lower())
    
    # Check if the code looks like an error message to avoid copying raw error text as code if possible, 
    # but for simplicity we just copy whatever is there.
    st.write("---")
