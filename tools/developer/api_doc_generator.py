# tools/developer/api_doc_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "API Documentation Gen", "📝", 
        "Generate professional API documentation for the following code or endpoint description. Include sections for Headers, Parameters, Request Body (JSON), and Example Responses.",
        "Paste code or describe the endpoint..."
    )
