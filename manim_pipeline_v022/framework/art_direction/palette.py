"""Topic-adaptive semantic palettes; these are options, not fixed topic rules."""

PALETTES = {
    "cinematic_navy": {
        "background": "#07111F",
        "structure": "#71899D",
        "text": "#F3F6FA",
        "secondary_text": "#B8C6D4",
        "signal": "#55C7E8",
        "energy": "#FFB454",
        "highlight": "#F7E36D",
        "muted": "#344556",
        "annotation": "#D5DEE7",
    },
    "bright_technical": {
        "background": "#F7F9FC",
        "structure": "#344054",
        "text": "#172033",
        "secondary_text": "#526176",
        "signal": "#087EBA",
        "energy": "#D97706",
        "highlight": "#B42318",
        "muted": "#D0D5DD",
        "annotation": "#667085",
    },
    "scientific_dark": {
        "background": "#101820",
        "structure": "#9AA8B5",
        "text": "#F5F7FA",
        "secondary_text": "#C4CDD5",
        "signal": "#42D6C5",
        "energy": "#FFB454",
        "highlight": "#A7F3D0",
        "muted": "#394957",
        "annotation": "#D7E0E8",
    },
    "industrial": {
        "background": "#151A20",
        "structure": "#A5AFB8",
        "text": "#F4F5F6",
        "secondary_text": "#C2C9D0",
        "signal": "#53C7E8",
        "energy": "#F59E0B",
        "highlight": "#FDE047",
        "muted": "#424B55",
        "annotation": "#D5DCE2",
    },
}


def resolve_palette(name="cinematic_navy", overrides=None):
    """Return a copy of a named palette with validated hex-color overrides."""
    if name not in PALETTES:
        raise KeyError(
            f"Unknown palette {name!r}. Choose one of: {', '.join(sorted(PALETTES))}"
        )
    result = dict(PALETTES[name])
    if overrides:
        for key, value in overrides.items():
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Palette override keys must be non-empty strings")
            if (
                not isinstance(value, str)
                or len(value) != 7
                or not value.startswith("#")
                or any(ch not in "0123456789abcdefABCDEF" for ch in value[1:])
            ):
                raise ValueError(
                    f"Palette override {key!r} must be a hex color like '#A1B2C3'"
                )
            result[key] = value.upper()
    return result
