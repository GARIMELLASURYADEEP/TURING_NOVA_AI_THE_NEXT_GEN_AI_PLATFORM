# tools/developer/bug_fixer.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Bug Fixing Assistant", "🐞", 
        "Find the bugs in the following code snippet, explain why they occur, and provide the corrected version of the code.",
        "Paste the buggy code here...",
        "Code with Bugs:"
    )
