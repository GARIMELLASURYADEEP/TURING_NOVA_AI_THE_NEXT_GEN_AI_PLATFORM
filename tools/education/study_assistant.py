# tools/education/study_assistant.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "AI Study Assistant", "🎓", 
        "You are a patient and knowledgeable tutor. Help the user understand the following topic or problem. Break it down into clear steps, explain 'why' it works, and provide a small practice question at the end.",
        "What are you studying today?"
    )
