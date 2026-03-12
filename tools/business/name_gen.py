# tools/business/name_gen.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Startup Name Gen", "📛", 
        "Generate 10 catchy, modern, and brandable name suggestions for a startup in the following industry or niche. For each name, provide a one-line branding tagline.",
        "e.g. Cloud-based logistics for small businesses"
    )
