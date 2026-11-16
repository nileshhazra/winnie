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
    # macOS Liquid Glass Smoke Obsidian Canvas
    "window_bg": "#121316",
    "surface_glass": "rgba(255, 255, 255, 0.05)",
    "surface_glass_hover": "rgba(255, 255, 255, 0.09)",
    "surface_glass_active": "rgba(255, 255, 255, 0.13)",
    "border_color": "rgba(255, 255, 255, 0.08)",
    "border_glass": "rgba(255, 255, 255, 0.08)",
    "border_glass_highlight": "rgba(255, 255, 255, 0.16)",
    "brand_color": "#ffffff",
    
    # Liquid Glass Pill Buttons
    "btn_clear_bg": "rgba(255, 255, 255, 0.05)",
    "btn_clear_hover": "rgba(255, 255, 255, 0.10)",
    "btn_clear_text": "#e4e4e7",
    "btn_clear_border": "rgba(255, 255, 255, 0.09)",
    
    # Accent Glass Highlights
    "accent_emerald": "#10b981",
    "accent_emerald_glass": "rgba(16, 185, 129, 0.18)",
    "accent_emerald_border": "rgba(52, 211, 153, 0.40)",
    "accent_emerald_text": "#6ee7b7",

    "accent_amber": "#f59e0b",
    "accent_honey": "#f59e0b",
    "accent_amber_glass": "rgba(245, 158, 11, 0.18)",
    "accent_amber_border": "rgba(251, 191, 36, 0.40)",
    "accent_amber_text": "#fcd34d",

    "accent_rose": "#ef4444",
    "accent_rose_glass": "rgba(239, 68, 68, 0.16)",
    "accent_rose_border": "rgba(248, 113, 113, 0.35)",
    "accent_rose_text": "#fca5a5",

    "accent_violet": "#a855f7",
    "accent_violet_glass": "rgba(168, 85, 247, 0.18)",
    "accent_violet_border": "rgba(192, 132, 252, 0.40)",
    "accent_violet_text": "#d8b4fe",

    # Floating Editor Glass Panel
    "editor_bg": "#16171b",
    "editor_text": "#f4f4f5",
    "editor_selection": "#28344e",
    "gutter_bg": "#141518",
    "gutter_border": "#23252b",
    "gutter_text": "#636366",
    
    # Active Line (Soft subtle highlight, NEVER pitch black)
    "current_line": "#1e2026",
    "debug_line_bg": "#3d2b00",

    # Floating Terminal / Console Glass Panel
    "console_bg": "#0e0f12",
    "console_text": "#f4f4f5",
    "console_border": "rgba(255, 255, 255, 0.07)",

    # Variables & Data Inspector Glass Panel
    "table_bg": "#141518",
    "table_header_bg": "rgba(255, 255, 255, 0.03)",
    "table_header_text": "#8e8e93",
    "table_text": "#f4f4f5",
    "table_border": "rgba(255, 255, 255, 0.06)",
    "var_name": "#38bdf8",
    "var_type": "#fbbf24",
    "var_str": "#34d399",

    # Sleek Rounded Glass Scrollbar
    "scrollbar_track": "transparent",
    "scrollbar_handle": "rgba(255, 255, 255, 0.18)",
    "scrollbar_handle_hover": "rgba(255, 255, 255, 0.32)",
    
    # Modern VS Code / Tokyo Night Syntax Palette
    "syntax_keyword": "#C586C0",
    "syntax_constant": "#569CD6",
    "syntax_builtin": "#DCDCAA",
    "syntax_string": "#CE9178",
    "syntax_number": "#B5CEA8",
    "syntax_comment": "#6A9955",
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


def get_code_font(size: int = 13, bold: bool = False, family: str = "SF Mono") -> QFont:
    """Returns a programming font with ligatures explicitly disabled and native fallbacks."""
    font = QFont(family, size)
    if bold:
        font.setBold(True)
    font.setStyleHint(QFont.StyleHint.Monospace)
    font.setFamilies([family, "SF Mono", "Menlo", "Monaco", "Courier New", "monospace"])
    configure_no_ligatures(font)
    return font
