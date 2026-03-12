# tools/creative/gradient_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Gradient Generator", "🌈", 
        "Generate 3 beautiful CSS linear-gradient values based on the following description. Provide the CSS code for each.",
        "e.g. Sunset colors, warm and vibrant"
    )
