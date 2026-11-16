from PySide6.QtGui import QFont, QColor
import re

def safe_qcolor(color_val, fallback="#1E2026") -> QColor:
    """Safely converts color strings (including rgba(...)) to a valid QColor without black fallback."""
    if isinstance(color_val, QColor):
        return color_val
    if isinstance(color_val, str):
        if color_val.startswith("rgba"):
            m = re.match(r"rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d\.]+)\s*\)", color_val)
            if m:
                r, g, b, a = m.groups()
                return QColor(int(r), int(g), int(b), int(float(a) * 255))
        c = QColor(color_val)
        if c.isValid() and (c != QColor(0, 0, 0, 255) or color_val.lower() in ("#000000", "#000", "black")):
            return c
    return QColor(fallback)

DARK_THEME = {
    "name": "dark",
    # CodeSandbox Black - Deep Pitch Black Obsidian Canvas
    "window_bg": "#0a0a0c",
    "surface_glass": "rgba(255, 255, 255, 0.05)",
    "surface_glass_hover": "rgba(255, 255, 255, 0.09)",
    "surface_glass_active": "rgba(255, 255, 255, 0.14)",
    "border_color": "rgba(255, 255, 255, 0.08)",
    "border_glass": "rgba(255, 255, 255, 0.08)",
    "border_glass_highlight": "rgba(255, 255, 255, 0.18)",
    "brand_color": "#ffffff",
    
    # Liquid Glass Pill Buttons
    "btn_clear_bg": "rgba(255, 255, 255, 0.05)",
    "btn_clear_hover": "rgba(255, 255, 255, 0.10)",
    "btn_clear_text": "#e4e4e7",
    "btn_clear_border": "rgba(255, 255, 255, 0.09)",
    
    # Accent Glass Highlights
    "accent_emerald": "#50fa7b",
    "accent_emerald_glass": "rgba(80, 250, 123, 0.18)",
    "accent_emerald_border": "rgba(80, 250, 123, 0.40)",
    "accent_emerald_text": "#50fa7b",

    "accent_amber": "#ffb86c",
    "accent_honey": "#ffb86c",
    "accent_amber_glass": "rgba(255, 184, 108, 0.18)",
    "accent_amber_border": "rgba(255, 184, 108, 0.40)",
    "accent_amber_text": "#ffb86c",

    "accent_rose": "#ff5555",
    "accent_rose_glass": "rgba(255, 85, 85, 0.18)",
    "accent_rose_border": "rgba(255, 85, 85, 0.40)",
    "accent_rose_text": "#ff6e6e",

    "accent_violet": "#bd93f9",
    "accent_violet_glass": "rgba(189, 147, 249, 0.18)",
    "accent_violet_border": "rgba(189, 147, 249, 0.40)",
    "accent_violet_text": "#bd93f9",

    # CodeSandbox Black - Pure Pitch Black Editor
    "editor_bg": "#000000",
    "editor_text": "#f8f8f2",
    "editor_selection": "#282a36",
    "gutter_bg": "#000000",
    "gutter_border": "#1a1a1f",
    "gutter_text": "#6272a4",
    
    # Active Line (Subtle slate highlight against pitch black)
    "current_line": "#141418",
    "debug_line_bg": "#2d2006",

    # Pure Black Terminal / Console
    "console_bg": "#000000",
    "console_text": "#f8f8f2",
    "console_border": "rgba(255, 255, 255, 0.08)",

    # Variables & Data Inspector Panel
    "table_bg": "#08080a",
    "table_header_bg": "rgba(255, 255, 255, 0.03)",
    "table_header_text": "#6272a4",
    "table_text": "#f8f8f2",
    "table_border": "rgba(255, 255, 255, 0.06)",
    "var_name": "#8be9fd",
    "var_type": "#ffb86c",
    "var_str": "#f1fa8c",

    # Sleek Rounded Glass Scrollbar
    "scrollbar_track": "transparent",
    "scrollbar_handle": "rgba(255, 255, 255, 0.18)",
    "scrollbar_handle_hover": "rgba(255, 255, 255, 0.32)",
    
    # CodeSandbox Black Iconic Neon Syntax Palette
    "syntax_keyword": "#ff79c6",
    "syntax_constant": "#bd93f9",
    "syntax_builtin": "#50fa7b",
    "syntax_function": "#50fa7b",
    "syntax_string": "#f1fa8c",
    "syntax_number": "#bd93f9",
    "syntax_comment": "#6272a4",
}

LIGHT_THEME = {
    "name": "light",
    # macOS Liquid Glass Porcelain Canvas
    "window_bg": "#f7f7f8",
    "surface_glass": "#ffffff",
    "surface_glass_hover": "#f0f0f2",
    "surface_glass_active": "#e8e8ea",
    "border_color": "rgba(0, 0, 0, 0.08)",
    "border_glass": "rgba(0, 0, 0, 0.08)",
    "border_glass_highlight": "rgba(0, 0, 0, 0.14)",
    "brand_color": "#18181b",

    # Liquid Glass Pill Buttons
    "btn_clear_bg": "#ffffff",
    "btn_clear_hover": "#f2f2f4",
    "btn_clear_text": "#18181b",
    "btn_clear_border": "rgba(0, 0, 0, 0.10)",

    # Accent Glass Highlights
    "accent_emerald": "#059669",
    "accent_emerald_glass": "#ecfdf5",
    "accent_emerald_border": "#a7f3d0",
    "accent_emerald_text": "#065f46",

    "accent_amber": "#d97706",
    "accent_honey": "#d97706",
    "accent_amber_glass": "#fffbeb",
    "accent_amber_border": "#fde68a",
    "accent_amber_text": "#92400e",

    "accent_rose": "#dc2626",
    "accent_rose_glass": "#fef2f2",
    "accent_rose_border": "#fecaca",
    "accent_rose_text": "#991b1b",

    "accent_violet": "#7c3aed",
    "accent_violet_glass": "#f5f3ff",
    "accent_violet_border": "#ddd6fe",
    "accent_violet_text": "#5b21b6",

    # Floating Editor Glass Panel
    "editor_bg": "#ffffff",
    "editor_text": "#18181b",
    "editor_selection": "#cfe2ff",
    "gutter_bg": "#fcfcfd",
    "gutter_border": "#e5e5ea",
    "gutter_text": "#a1a1aa",
    
    # Active Line in Light Mode
    "current_line": "#ededf2",
    "debug_line_bg": "#fef08a",

    # Floating Terminal / Console Glass Panel
    "console_bg": "#fafafa",
    "console_text": "#18181b",
    "console_border": "rgba(0, 0, 0, 0.08)",

    # Variables & Data Inspector Glass Panel
    "table_bg": "#ffffff",
    "table_header_bg": "#f8f8fa",
    "table_header_text": "#71717a",
    "table_text": "#18181b",
    "table_border": "rgba(0, 0, 0, 0.07)",
    "var_name": "#0284c7",
    "var_type": "#b45309",
    "var_str": "#059669",

    # Sleek Rounded Glass Scrollbar
    "scrollbar_track": "transparent",
    "scrollbar_handle": "rgba(0, 0, 0, 0.16)",
    "scrollbar_handle_hover": "rgba(0, 0, 0, 0.28)",
    
    # Clean Light Syntax Highlighting
    "syntax_keyword": "#AF00DB",
    "syntax_constant": "#0000FF",
    "syntax_builtin": "#795E26",
    "syntax_string": "#A31515",
    "syntax_number": "#098658",
    "syntax_comment": "#008000",
}


def get_scrollbar_stylesheet(theme: dict) -> str:
    """Returns modern, sleek, rounded glass scrollbar styling consistent with the active theme."""
    handle = theme.get("scrollbar_handle", "rgba(255, 255, 255, 0.18)")
    handle_hover = theme.get("scrollbar_handle_hover", "rgba(255, 255, 255, 0.32)")
    return f"""
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 8px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {handle};
            min-height: 28px;
            border-radius: 4px;
            margin: 2px 1px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {handle_hover};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}

        QScrollBar:horizontal {{
            border: none;
            background: transparent;
            height: 8px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {handle};
            min-width: 28px;
            border-radius: 4px;
            margin: 1px 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {handle_hover};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            border: none;
            background: none;
            width: 0px;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}
        QScrollBar::corner {{
            background: transparent;
        }}
    """


def configure_no_ligatures(font: QFont) -> QFont:
    """Disables all OpenType ligatures and contextual alternates on a QFont."""
    if hasattr(QFont, "Tag") and hasattr(font, "setFeature"):
        try:
            for tag_name in ("calt", "liga", "dlig", "clig", "hlig"):
                font.setFeature(QFont.Tag(tag_name), 0)
        except Exception:
            pass
    font.setKerning(False)
    return font


def get_code_font(size: int = 13, bold: bool = False, family: str = "Dank Mono") -> QFont:
    """Returns a character-rich programming font (Dank Mono) with native fallbacks and ligatures disabled."""
    font = QFont(family, size)
    if bold:
        font.setBold(True)
    font.setStyleHint(QFont.StyleHint.Monospace)
    font.setFamilies([family, "Dank Mono", "JetBrains Mono", "Fira Code", "SF Mono", "Menlo", "Monaco", "Courier New", "monospace"])
    configure_no_ligatures(font)
    return font


def get_ui_font(size: int = 12, weight = QFont.Weight.Normal, bold: bool = False) -> QFont:
    """Returns a distinctive, modern UI font (Inter / Avenir Next) with clean fallbacks."""
    font = QFont("Inter", size)
    if bold or weight == QFont.Weight.Bold:
        font.setBold(True)
    else:
        font.setWeight(weight)
    font.setFamilies(["Inter", "Avenir Next", "SF Pro Text", "-apple-system", "Helvetica Neue", "sans-serif"])
    return font
