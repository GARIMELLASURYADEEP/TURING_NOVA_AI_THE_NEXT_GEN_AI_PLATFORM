# tools/education/quiz_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Quiz Generator", "📝", 
        "Generate a 5-question multiple-choice quiz based on the following topic. Include the correct answers at the very end.",
        "e.g. Modern Web Development with React"
    )
