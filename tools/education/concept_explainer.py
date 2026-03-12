# tools/education/concept_explainer.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Concept Explainer", "💡", 
        "Explain the following complex concept as if the user is 10 years old (ELI10). Use analogies and simple language.",
        "e.g. Quantum Entanglement or How a CPU works"
    )
