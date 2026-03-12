# tools/education/interview_prep.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Interview Prep", "👔", 
        "You are a hiring manager for a top tech company. Provide 5 challenging interview questions based on the the following job role, along with tips on how to structure a winning answer for each.",
        "e.g. Senior Software Engineer at a FinTech startup"
    )
