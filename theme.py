import sys
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
    # CodeSandbox Black (https://github.com/ziadyjo/codesandbox-black-theme)
    "window_bg": "#111111",
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
    "btn_clear_text": "#ABB2BF",
    "btn_clear_border": "rgba(255, 255, 255, 0.09)",
    
    # Accent Glass Highlights
    "accent_emerald": "#41B883",
    "accent_emerald_glass": "rgba(65, 184, 131, 0.18)",
    "accent_emerald_border": "rgba(65, 184, 131, 0.40)",
    "accent_emerald_text": "#41B883",

    "accent_amber": "#D19A66",
    "accent_honey": "#D19A66",
    "accent_amber_glass": "rgba(209, 154, 102, 0.18)",
    "accent_amber_border": "rgba(209, 154, 102, 0.40)",
    "accent_amber_text": "#D19A66",

    "accent_rose": "#E06C75",
    "accent_rose_glass": "rgba(224, 108, 117, 0.18)",
    "accent_rose_border": "rgba(224, 108, 117, 0.40)",
    "accent_rose_text": "#E06C75",

    "accent_violet": "#C678DD",
    "accent_violet_glass": "rgba(198, 120, 221, 0.18)",
    "accent_violet_border": "rgba(198, 120, 221, 0.40)",
    "accent_violet_text": "#C678DD",

    # CodeSandbox Black - Deep Obsidian Editor Canvas
    "editor_bg": "#151515",
    "editor_text": "#ABB2BF",
    "editor_selection": "#1D2F3E",
    "gutter_bg": "#151515",
    "gutter_border": "#242424",
    "gutter_text": "#5C6370",
    
    # Active Line & Debug Line
    "current_line": "#1E1E1E",
    "debug_line_bg": "#2d2006",

    # Pure Black Terminal / Console
    "console_bg": "#151515",
    "console_text": "#ABB2BF",
    "console_border": "#242424",

    # Variables & Data Inspector Panel
    "table_bg": "#151515",
    "table_header_bg": "rgba(255, 255, 255, 0.03)",
    "table_header_text": "#5C6370",
    "table_text": "#ABB2BF",
    "table_border": "rgba(255, 255, 255, 0.06)",
    "var_name": "#E06C75",
    "var_type": "#D19A66",
    "var_str": "#41B883",

    # Sleek Rounded Glass Scrollbar
    "scrollbar_track": "transparent",
    "scrollbar_handle": "rgba(255, 255, 255, 0.18)",
    "scrollbar_handle_hover": "rgba(255, 255, 255, 0.32)",
    
    # Official ziadyjo/codesandbox-black-theme Token Colors
    "syntax_keyword": "#C678DD",
    "syntax_class": "#E5C07B",
    "syntax_inherited": "#41B883",
    "syntax_function": "#61AFEF",
    "syntax_variable": "#E06C75",
    "syntax_parameter": "#D19A66",
    "syntax_constant": "#D19A66",
    "syntax_number": "#D19A66",
    "syntax_string": "#41B883",
    "syntax_comment": "#5C6370",
    "syntax_operator": "#ABB2BF",
    "syntax_builtin": "#56B6C2",
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
    "syntax_keyword": "#A626A4",
    "syntax_class": "#C18401",
    "syntax_inherited": "#50A14F",
    "syntax_function": "#4078F2",
    "syntax_variable": "#E45649",
    "syntax_parameter": "#986801",
    "syntax_constant": "#986801",
    "syntax_number": "#986801",
    "syntax_string": "#50A14F",
    "syntax_comment": "#A0A1A7",
    "syntax_operator": "#383A42",
    "syntax_builtin": "#0184BC",
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
    """Returns a distinctive, modern UI font with clean native fallbacks without font alias cost."""
    default_fam = ".AppleSystemUIFont" if sys.platform == "darwin" else "Inter"
    font = QFont(default_fam, size)
    if bold or weight == QFont.Weight.Bold:
        font.setBold(True)
    else:
        font.setWeight(weight)
    font.setFamilies([".AppleSystemUIFont", "Helvetica Neue", "Arial"])
    return font
