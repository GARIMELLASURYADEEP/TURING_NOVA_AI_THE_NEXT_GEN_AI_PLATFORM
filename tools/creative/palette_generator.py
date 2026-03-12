# tools/creative/palette_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Color Palette Generator", "🎨", 
        "Generate a professional color palette (Hex codes and names) based on the following mood or theme. Include 5 colors with descriptions of where to use them in a UI.",
        "e.g. A calm, oceanic theme for a wellness app"
    )
