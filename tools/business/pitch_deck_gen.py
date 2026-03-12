# tools/business/pitch_deck_gen.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Pitch Deck Outline", "📽️", 
        "Create a 10-slide pitch deck outline for the following startup idea. For each slide, describe the title and the core content/data points to be shown.",
        "e.g. A marketplace for local farmers to sell directly to restaurants"
    )
