# tools/developer/code_explainer.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Code Explainer", "📖", 
        "Explain the following code snippet line-by-line in simple terms. Highlight the logic, complexity, and any potential improvements.",
        "Paste your code here...",
        "Code to Explain:"
    )
