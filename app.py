import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
APP_NAME = "Devil's Code Generator"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "stepfun/step-3.5-flash:free"

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_code(prompt, model):
    """
    Generates code using OpenRouter API.
    """
    if not OPENROUTER_API_KEY:
        return {"error": "API Key not found. Please checks your .env file."}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501", # Localhost for now
        "X-Title": APP_NAME,
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    st.header("💻 AI Code Generator")
    st.markdown(f"Generate code snippets, functions, or debug existing code using **{MODEL}**.")

    # Sidebar for any future settings, keeping it simple for now
    with st.sidebar:
        st.title(APP_NAME)
        st.info("get code from AI and make it better")

    col1, col2 = st.columns([1, 3])
    
    with col1:
        language = st.selectbox(
            "Language",
            ["Python", "Java", "C++", "JavaScript", "Go", "Rust", "TypeScript", "SQL", "HTML/CSS", "Shell Script","C#","PHP","Ruby","Swift","Kotlin","gdscript","c",]
        )
    
    with col2:
        prompt_text = st.text_area("Enter your coding task:", height=150)
    
    if st.button("Generate Code", type="primary"):
        if not prompt_text:
            st.warning("Please enter a coding task.")
            return
        
        with st.spinner("Writing code..."):
            final_prompt = f"Write only executable {language} code for the following task. Do not include explanation.\n\nTask: {prompt_text}"
            
            response = generate_code(final_prompt, MODEL)
            
            if "error" in response:
                st.error(f"Error: {response['error']}")
            else:
                try:
                    content = response['choices'][0]['message']['content']
                    st.subheader("Generated Code:")
                    st.code(content, language=language.lower())
                    st.success(f"Generated successfully!")
                except (KeyError, IndexError, TypeError):
                     st.error(f"Unexpected response format from API: {response}")

if __name__ == "__main__":
    main()
