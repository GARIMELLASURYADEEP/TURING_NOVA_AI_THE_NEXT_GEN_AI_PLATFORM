# tools/business/product_desc_gen.py
from tools.text_factory import render_text_tool

def show():
    render_text_tool(
        "Product Description", "🛒", 
        "Generate an SEO-optimized, engaging product description for an e-commerce store based on the following item details.",
        "e.g. Handmade vegan leather travel bag, waterproof, with laptop compartment"
    )
