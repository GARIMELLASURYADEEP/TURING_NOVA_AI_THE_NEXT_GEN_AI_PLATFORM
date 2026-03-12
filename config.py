import os
from dotenv import load_dotenv

load_dotenv()

# Platform Constants
APP_NAME = "TURING NOVA AI"
APP_SUBTITLE = "THE NEXT GEN AI PLATFORM"
VERSION = "2.0.0"

# API Configurations
# Note: Platform now uses browser-native anonymous AI engines via Puter.js
# No external server-side API keys are strictly required for AI generation.

# Color Presets (Shared across modules)
COLOR_PRESETS_DARK = {
    "Indigo":  {"accent": "#6366f1", "hero": "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)", "card": "#1e1b4b", "user": "#4338ca"},
    "Emerald": {"accent": "#10b981", "hero": "linear-gradient(135deg, #064e3b 0%, #065f46 100%)", "card": "#064e3b", "user": "#059669"},
    "Amber":   {"accent": "#f59e0b", "hero": "linear-gradient(135deg, #78350f 0%, #92400e 100%)", "card": "#78350f", "user": "#d97706"},
    "Rose":    {"accent": "#f43f5e", "hero": "linear-gradient(135deg, #881337 0%, #9f1239 100%)", "card": "#881337", "user": "#e11d48"},
    "Cyan":    {"accent": "#06b6d4", "hero": "linear-gradient(135deg, #164e63 0%, #155e75 100%)", "card": "#164e63", "user": "#0891b2"},
}

COLOR_PRESETS_LIGHT = {
    "Violet":  {"accent": "#8b5cf6", "hero": "linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)", "card": "#f5f3ff", "user": "#4f46e5"},
    "Cyan":    {"accent": "#06b6d4", "hero": "linear-gradient(135deg, #0891b2 0%, #06b6d4 100%)", "card": "#ecfeff", "user": "#0891b2"},
    "Green":   {"accent": "#10b981", "hero": "linear-gradient(135deg, #059669 0%, #10b981 100%)", "card": "#f0fdf4", "user": "#059669"},
    "Orange":  {"accent": "#f97316", "hero": "linear-gradient(135deg, #ea580c 0%, #f97316 100%)", "card": "#fff7ed", "user": "#ea580c"},
    "Slate":   {"accent": "#64748b", "hero": "linear-gradient(135deg, #334155 0%, #64748b 100%)", "card": "#f8fafc", "user": "#334155"},
}
