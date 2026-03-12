# tools/education/flashcard_generator.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Flashcard Generator", "🗂️", 
        "Create a set of 10 digital flashcards (Front: Concept, Back: Detailed Answer) for the following subject. Format them clearly.",
        "e.g. Fundamental Physics: Newton's Laws"
    )
