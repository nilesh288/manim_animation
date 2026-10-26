"""
engine_2d/theme.py
Editorial Light Palette and Visual Style System.
Warm off-white / eggshell canvas (#F8F9FA), pure white cards (#FFFFFF),
deep charcoal typography (#1A202C) and high-contrast editorial accents.
"""

class SafePalette(dict):
    """
    Resilient design token dictionary that prevents runtime KeyError exceptions
    from LLM hallucinations or variations in color naming.
    """
    _ALIASES = {
        # Sky / Blue family
        "sky": "sky",
        "blue": "blue",
        "cobalt": "blue",
        "azure": "blue",
        "cyan": "sky",
        "light_blue": "sky",

        # Mint / Green family
        "mint": "mint",
        "green": "mint",
        "teal": "mint",
        "emerald": "mint",

        # Coral / Red / Alert family
        "coral": "coral",
        "red": "coral",
        "crimson": "coral",
        "alert": "coral",
        "danger": "coral",

        # Amber / Orange / Gold family
        "amber": "amber",
        "orange": "amber",
        "gold": "gold",
        "yellow": "gold",

        # Purple / Indigo family
        "indigo": "indigo",
        "purple": "purple",
        "violet": "purple",
        "lavender": "purple",

        # Canvas & Backgrounds
        "bg": "bg",
        "background": "bg",
        "canvas": "bg",
        "surface_card": "surface_card",
        "card": "surface_card",
        "surface_ground": "bg_subtle",
        "bg_subtle": "bg_subtle",
        "surface_dark": "surface_dark",

        # Strokes & Borders
        "stroke": "stroke",
        "stroke_border": "stroke",
        "border": "stroke",
        "border_stroke": "stroke",
        "stroke_light": "stroke_light",
        "stroke_muted": "stroke_muted",

        # Typography
        "text": "text",
        "text_primary": "text",
        "primary": "blue",
        "text_dark": "text",
        "label": "text",
        "title": "text",
        "text_dim": "text_dim",
        "text_muted": "text_dim",
        "text_light": "text_light",
        "white": "white",
    }

    def __getitem__(self, key):
        if not isinstance(key, str):
            return super().__getitem__(key)

        trimmed = key.strip()
        if trimmed.startswith("#"):
            return trimmed

        normalized = trimmed.lower()

        # Support nested dictionary access like PALETTE["accents"]["sky"]
        if normalized in ("accents", "typography", "design_system", "palette", "colors", "tokens"):
            return self

        if normalized in self:
            return super().__getitem__(normalized)

        if normalized in self._ALIASES:
            target = self._ALIASES[normalized]
            if target in self:
                return super().__getitem__(target)

        # Keyword heuristics
        if any(w in normalized for w in ("red", "warn", "alert", "error", "coral", "fire", "danger")):
            return self["coral"]
        if any(w in normalized for w in ("green", "mint", "teal", "pass", "ok", "success")):
            return self["mint"]
        if any(w in normalized for w in ("blue", "sky", "water", "packet", "flow", "network")):
            return self["blue"]
        if any(w in normalized for w in ("purp", "lav", "indig", "token", "ai", "magic", "cipher")):
            return self["indigo"]
        if any(w in normalized for w in ("yel", "gold", "sun")):
            return self["gold"]
        if any(w in normalized for w in ("amb", "oran", "heat", "telemetry")):
            return self["amber"]
        if any(w in normalized for w in ("card", "window", "panel", "surface")):
            return self["surface_card"]
        if any(w in normalized for w in ("border", "stroke", "conduit")):
            return self["stroke"]
        if any(w in normalized for w in ("dim", "sub", "tick", "meta")):
            return self["text_dim"]

        return self["blue"]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default if default is not None else self["blue"]


PALETTE = SafePalette({
    # Canvas & Foundations (Warm editorial eggshell canvas)
    "bg": "#F8F9FA",               # Warm off-white / eggshell canvas
    "background": "#F8F9FA",       # Alias for canvas
    "bg_subtle": "#EDF2F7",        # Section shading / platform runway
    "surface_ground": "#EDF2F7",   # Runway ground platform
    "surface_card": "#FFFFFF",     # Clean arctic white card fill
    "surface_dark": "#2A3238",     # Deep graphite charcoal (for device bodies)

    # Structure & Ink
    "stroke": "#2D3748",           # Deep charcoal border / outline
    "stroke_light": "#CBD5E0",     # Grid lines and conduits
    "stroke_muted": "#E2E8F0",     # Subtle reference lines

    # Typography (Guaranteed High Contrast on Light Canvas)
    "text": "#1A202C",             # Slate pitch black headline typography
    "text_dim": "#718096",         # Muted secondary labels
    "text_light": "#FFFFFF",       # Pure white text for inside dark badges
    "white": "#FFFFFF",            # Pure white

    # Editorial Accents (Punchy & readable on light backgrounds)
    "indigo": "#5A67D8",           # Primary actors / emitters / nodes
    "blue": "#1E60FF",             # Primary data streams / network routes
    "sky": "#0284C7",              # Cyan-sky network waves
    "mint": "#00C9A7",             # Success / verified states / targets
    "amber": "#ED8936",            # Telemetry / rulers / measurements
    "gold": "#D97706",             # Energy / focal metrics
    "coral": "#E53E3E",            # Focus alerts / receivers / collisions
    "purple": "#805AD5",           # Alternative pathway / logic branch
    "pink": "#D946EF",             # Secondary branch
})

class SafeFonts(dict):
    _ALIASES = {
        "header": "sans",
        "title": "sans",
        "headline": "sans",
        "body": "sans",
        "text": "sans",
        "default": "sans",
        "code": "mono",
        "terminal": "mono",
        "label": "sans",
    }

    def __getitem__(self, key):
        lower_key = str(key).lower().strip()
        if lower_key in self:
            return super().__getitem__(lower_key)
        if lower_key in self._ALIASES:
            canonical = self._ALIASES[lower_key]
            if canonical in self:
                return super().__getitem__(canonical)
        return "sans-serif"

    def get(self, key, default="sans-serif"):
        try:
            return self[key]
        except KeyError:
            return default


FONTS = SafeFonts({
    "sans": "sans-serif",
    "mono": "monospace",
    "label": "sans-serif",
})


class SafeFontSizes(dict):
    """
    Standardized typography scale for 1080p broadcast clarity.
    Guarantees readable, punchy text hierarchy across all scenes.
    """
    _ALIASES = {
        "headline": "hero",
        "h1": "hero",
        "h2": "title",
        "header": "card_header",
        "card_title": "card_header",
        "badge": "pill",
        "status": "pill",
        "text": "body",
        "regular": "body",
        "mono": "code",
        "terminal": "code",
        "sub": "label",
        "subtext": "label",
        "chip": "marking",
        "ic": "marking",
    }

    def __getitem__(self, key):
        if not isinstance(key, str):
            return super().__getitem__(key)
        normalized = key.strip().lower()
        if normalized in self:
            return super().__getitem__(normalized)
        if normalized in self._ALIASES:
            return super().__getitem__(self._ALIASES[normalized])
        return 13

    def get(self, key, default=13):
        try:
            return self[key]
        except KeyError:
            return default


FONT_SIZES = SafeFontSizes({
    "hero": 22,          # Large scene titles / topic announcements
    "title": 18,         # Major section headers / hero window text
    "card_header": 14,   # Card title bars (TechCard / VisualCard)
    "body": 13,          # Primary explanatory text
    "pill": 13,          # Status badges / pill callouts (MacOSPill)
    "code": 12,          # Monospace terminal lines / logs
    "label": 11,         # Component sub-labels / annotations
    "marking": 10,       # Hardware laser markings / IC labels
    "micro": 8,          # Miniature component details
})
