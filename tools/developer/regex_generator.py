# tools/developer/regex_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Regex Generator", "🔗", 
        "Generate a Regular Expression (Regex) for the following pattern description. Include an explanation of the regex components and example matches.",
        "e.g. A regex to match phone numbers in the format (123) 456-7890"
    )
