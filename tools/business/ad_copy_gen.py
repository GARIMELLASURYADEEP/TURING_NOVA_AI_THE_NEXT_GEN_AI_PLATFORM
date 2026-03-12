# tools/business/ad_copy_gen.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Ad Copy Generator", "🎯", 
        "Generate 3 variations of ad copy for social media (Instagram, Facebook) for the following campaign. Include headlines and primary text for each.",
        "e.g. Early bird discount for a local meditation workshop"
    )
