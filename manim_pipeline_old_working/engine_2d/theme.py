"""
2d_engine/theme.py
Editorial Pastel Palette and visual style definitions.
"""

PALETTE = {
    # Canvas
    "bg": "#F8F9FA",           # Warm off-white / eggshell
    "bg_subtle": "#EDF2F7",    # Fills & sector shading
    
    # Structure & Ink
    "stroke": "#2D3748",       # Deep charcoal
    "stroke_light": "#CBD5E0", # Grid lines and conduits
    "stroke_muted": "#E2E8F0", # Secondary grid lines
    "text": "#1A202C",         # High-contrast slate black
    "text_dim": "#718096",     # Muted secondary labels
    
    # Editorial Accents (Topic Agnostic)
    "indigo": "#5A67D8",       # Primary actors / emitters / nodes
    "blue": "#4299E1",         # Secondary waves / data streams
    "mint": "#38A169",         # Success / verified states / targets
    "amber": "#ED8936",        # Telemetry / rulers / measurements
    "coral": "#E53E3E",        # Focus alerts / receivers / collisions
    "purple": "#805AD5",       # Alternative pathway / logic branch
}

FONTS = {
    "label": "sans-serif",
    "mono": "monospace",
}
