# tools/developer/sql_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "SQL Query Generator", "🗄️", 
        "Generate a clean, optimized SQL query for the following request. Assume standard table names unless specified.",
        "e.g. Find all customers who spent more than $500 in the last 30 days"
    )
