# tools/education/job_analyzer.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Job Description Analyzer", "🔍", 
        "Analyze the following job description. Identify the top 5 required technical skills, top 3 soft skills, and provide 3 suggested keywords the user should add to their resume to pass an ATS scan for this role.",
        "Paste the job description here..."
    )
