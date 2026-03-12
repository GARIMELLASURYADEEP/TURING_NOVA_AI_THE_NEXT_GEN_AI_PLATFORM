# tools/business/business_plan_gen.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Business Plan Generator", "📊", 
        "Create a structured business plan outline for a startup with the following description. Include sections for Executive Summary, Market Analysis, Product/Service, and Marketing Strategy.",
        "e.g. A subscription-based platform for organic meal kits"
    )
