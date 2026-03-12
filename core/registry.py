# core/registry.py

# Categorized tool registry for Turing Nova Creator Hub
# Each entry: icon, name, description, handler_path (module_path)

TOOLS = {
    "creative": [
        {"id": "img_gen", "name": "AI Image Generator", "icon": "🎨", "desc": "High-quality AI images from text.", "handler": "tools.creative.image_generator"},
        {"id": "logo_gen", "name": "AI Logo Generator", "icon": "💎", "desc": "Professional logos for brands/startups.", "handler": "tools.creative.logo_generator"},
        {"id": "avatar_gen", "name": "Avatar Generator", "icon": "👤", "desc": "Customized AI avatars and characters.", "handler": "tools.creative.avatar_generator"},
        {"id": "poster_gen", "name": "Poster Generator", "icon": "🖼️", "desc": "Creative posters for events or decor.", "handler": "tools.creative.poster_generator"},
        {"id": "thumb_gen", "name": "Thumbnail Generator", "icon": "📺", "desc": "Viral thumbnails for YouTube/social media.", "handler": "tools.creative.thumbnail_generator"},
        {"id": "wall_gen", "name": "Wallpaper Generator", "icon": "🖥️", "desc": "Stunning 4K wallpapers for any device.", "handler": "tools.creative.wallpaper_generator"},
        {"id": "meme_gen", "name": "Meme Generator", "icon": "🎭", "desc": "Instant AI-powered meme creation.", "handler": "tools.creative.meme_generator"},
        {"id": "qr_gen", "name": "QR Code Generator", "icon": "📱", "desc": "Fast, high-res QR code generation.", "handler": "tools.utilities.qr_generator"},
        {"id": "palette_gen", "name": "Color Palette Generator", "icon": "🎨", "desc": "Harmonious color schemes for designers.", "handler": "tools.creative.palette_generator"},
        {"id": "gradient_gen", "name": "Gradient Generator", "icon": "🌈", "desc": "Smooth CSS gradients for web/app design.", "handler": "tools.creative.gradient_generator"},
    ],
    "developer": [
        {"id": "code_gen", "name": "AI Code Generator", "icon": "💻", "desc": "Production-ready code (OpenRouter).", "handler": "tools.developer.code_generator"},
        {"id": "code_explainer", "name": "Code Explainer", "icon": "🔎", "desc": "Understand complex code snippets easily.", "handler": "tools.developer.code_explainer"},
        {"id": "bug_fixer", "name": "Bug Fixing Assistant", "icon": "🐞", "desc": "Identify and resolve software bugs.", "handler": "tools.developer.bug_fixer"},
        {"id": "regex_gen", "name": "Regex Generator", "icon": "⚡", "desc": "Convert text patterns into Regex strings.", "handler": "tools.developer.regex_generator"},
        {"id": "sql_gen", "name": "SQL Query Generator", "icon": "🗄️", "desc": "Generate SQL from plain English.", "handler": "tools.developer.sql_generator"},
        {"id": "api_doc", "name": "API Documentation Gen", "icon": "📚", "desc": "Auto-generate professional API docs.", "handler": "tools.developer.api_doc_generator"},
        {"id": "web_gen", "name": "AI Website Generator", "icon": "🌐", "desc": "Complete HTML/CSS site with preview.", "handler": "tools.developer.website_generator"},
    ],
    "education": [
        {"id": "study_asst", "name": "AI Study Assistant", "icon": "🎓", "desc": "Your personal 24/7 learning tutor.", "handler": "tools.education.study_assistant"},
        {"id": "quiz_gen", "name": "Quiz Generator", "icon": "📝", "desc": "Create interactive quizzes for any topic.", "handler": "tools.education.quiz_generator"},
        {"id": "flash_gen", "name": "Flashcard Generator", "icon": "🗂️", "desc": "Smart flashcards for quick revision.", "handler": "tools.education.flashcard_generator"},
        {"id": "concept_exp", "name": "Concept Explainer", "icon": "💡", "desc": "Simplifying complex ideas instantly.", "handler": "tools.education.concept_explainer"},
        {"id": "interview_prep", "name": "Interview Prep", "icon": "👔", "desc": "Mock interviews and role-specific Q&A.", "handler": "tools.education.interview_prep"},
        {"id": "resume_anal", "name": "Resume Analyzer", "icon": "📄", "desc": "Detailed CV analysis and feedback.", "handler": "tools.education.resume_analyzer"},
        {"id": "cover_gen", "name": "Cover Letter Generator", "icon": "✉️", "desc": "Winning cover letters in seconds.", "handler": "tools.education.cover_letter_generator"},
        {"id": "job_anal", "name": "Job Description Analyzer", "icon": "🔍", "desc": "Extract core skills from any job listing.", "handler": "tools.education.job_analyzer"},
    ],
    "business": [
        {"id": "startup_idea", "name": "Startup Idea Gen", "icon": "🚀", "desc": "Innovative business ideas tailored to you.", "handler": "tools.business.startup_idea_gen"},
        {"id": "biz_plan", "name": "Business Plan Generator", "icon": "📊", "desc": "Comprehensive strategy documents.", "handler": "tools.business.business_plan_gen"},
        {"id": "marketing_copy", "name": "Marketing Copy Gen", "icon": "📣", "desc": "High-converting copy for campaigns.", "handler": "tools.business.marketing_copy_gen"},
        {"id": "product_desc", "name": "Product Description", "icon": "🛒", "desc": "SEO-friendly e-commerce descriptions.", "handler": "tools.business.product_desc_gen"},
        {"id": "ad_copy", "name": "Ad Copy Generator", "icon": "🎯", "desc": "Effective ads for Meta, Google, & more.", "handler": "tools.business.ad_copy_gen"},
        {"id": "name_gen", "name": "Startup Name Gen", "icon": "📛", "desc": "Catchy, brandable business names.", "handler": "tools.business.name_gen"},
        {"id": "pitch_deck", "name": "Pitch Deck Outline", "icon": "📽️", "desc": "Solid foundations for your next big pitch.", "handler": "tools.business.pitch_deck_gen"},
    ],
    "utilities": [
        {"id": "qr_util", "name": "QR Code Generator", "icon": "📱", "desc": "Professional scannable QR codes.", "handler": "tools.utilities.qr_generator"},
        {"id": "tts_util", "name": "Text to Speech", "icon": "🎙️", "desc": "Natural voices for your written text.", "handler": "tools.utilities.tts_generator"},
        {"id": "word_count", "name": "Word Counter", "icon": "🔢", "desc": "Analyze text length and statistics.", "handler": "tools.utilities.word_counter"},
        {"id": "md_conv", "name": "Markdown Converter", "icon": "⬇️", "desc": "Clean HTML to Markdown conversion.", "handler": "tools.utilities.markdown_converter"},
        {"id": "json_format", "name": "JSON Formatter", "icon": "📦", "desc": "Prettify and validate JSON data.", "handler": "tools.utilities.json_formatter"},
        {"id": "pass_gen", "name": "Password Generator", "icon": "🔐", "desc": "Secure, randomized password creation.", "handler": "tools.utilities.password_generator"},
    ]
}

CATEGORIES = {
    "creative": {"name": "Creative Hub", "icon": "🎨", "color": "#8b5cf6"},
    "developer": {"name": "Developer Tools", "icon": "💻", "color": "#6366f1"},
    "education": {"name": "Education & Career", "icon": "🎓", "color": "#10b981"},
    "business": {"name": "Business & Marketing", "icon": "🚀", "color": "#f59e0b"},
    "utilities": {"name": "Utilities", "icon": "🛠️", "color": "#64748b"},
}
