# tools/business/marketing_copy_gen.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Marketing Copy Gen", "📣", 
        "Generate high-converting marketing copy for the following product or service. Targeted at the specific audience mentioned. Include a hook, features/benefits, and a strong call to action.",
        "e.g. A new wireless noise-canceling headphone for busy students"
    )
