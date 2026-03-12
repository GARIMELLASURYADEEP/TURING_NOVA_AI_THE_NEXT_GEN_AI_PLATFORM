# tools/education/cover_letter_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Cover Letter Generator", "✉️", 
        "Generate a professional, persuasive cover letter based on the following details (Name, Role, Company, and Key Achievements). Ensure it has a tone appropriate for the company/industry mentioned.",
        "e.g. John Doe applying for Marketing Manager at TechFlow. 5 years experience in growth marketing."
    )
