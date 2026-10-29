from PySide6.QtGui import QFont

DARK_THEME = {
    "name": "dark",
    "window_bg": "#18181b",
    "border_color": "#27272a",
    "brand_color": "#f4f4f5",
    "btn_clear_bg": "#27272a",
    "btn_clear_hover": "#3f3f46",
    "btn_clear_text": "#d4d4d8",
    "btn_clear_border": "#3f3f46",
    
    # Editor
    "editor_bg": "#141416",
    "editor_text": "#e4e4e7",
    "editor_selection": "#2e384d",
    "gutter_bg": "#18181b",
    "gutter_border": "#27272a",
    "gutter_text": "#52525b",
    "current_line": "#1e1e24",
    "debug_line_bg": "#3f2e00",

    # Console
    "console_bg": "#0f0f11",
    "console_text": "#f4f4f5",
    "console_border": "#27272a",

    # Variables Inspector
    "table_bg": "#141416",
    "table_header_bg": "#18181b",
    "table_header_text": "#71717a",
    "table_text": "#e4e4e7",
    "table_border": "#27272a",
    "var_name": "#38bdf8",
    "var_type": "#fbbf24",
    "var_str": "#34d399",

    # Scrollbar
    "scrollbar_track": "#141416",
    "scrollbar_handle": "#3f3f46",
    "scrollbar_handle_hover": "#52525b",
    
    # Syntax Highlighting
    "syntax_keyword": "#C586C0",
    "syntax_constant": "#569CD6",
    "syntax_builtin": "#DCDCAA",
    "syntax_string": "#CE9178",
    "syntax_number": "#B5CEA8",
    "syntax_comment": "#6A9955",
}

LIGHT_THEME = {
    "name": "light",
    "window_bg": "#f4f4f5",
    "border_color": "#e4e4e7",
    "brand_color": "#18181b",
    "btn_clear_bg": "#ffffff",
    "btn_clear_hover": "#e4e4e7",
    "btn_clear_text": "#27272a",
    "btn_clear_border": "#d4d4d8",

    # Editor
    "editor_bg": "#ffffff",
    "editor_text": "#18181b",
    "editor_selection": "#b4d5fe",
    "gutter_bg": "#f4f4f5",
    "gutter_border": "#e4e4e7",
    "gutter_text": "#a1a1aa",
    "current_line": "#f5f5f7",
    "debug_line_bg": "#fef08a",

    # Console
    "console_bg": "#fcfcfd",
    "console_text": "#18181b",
    "console_border": "#e4e4e7",

    # Variables Inspector
    "table_bg": "#ffffff",
    "table_header_bg": "#f4f4f5",
    "table_header_text": "#71717a",
    "table_text": "#18181b",
    "table_border": "#e4e4e7",
    "var_name": "#0284c7",
    "var_type": "#b45309",
    "var_str": "#059669",

    # Scrollbar
    "scrollbar_track": "#ffffff",
    "scrollbar_handle": "#d4d4d8",
    "scrollbar_handle_hover": "#a1a1aa",
    
    # Syntax Highlighting
    "syntax_keyword": "#AF00DB",
    "syntax_constant": "#0000FF",
    "syntax_builtin": "#795E26",
    "syntax_string": "#A31515",
    "syntax_number": "#098658",
    "syntax_comment": "#008000",
}


def get_scrollbar_stylesheet(theme: dict) -> str:
    """Returns modern, sleek, rounded scrollbar styling consistent with the active theme."""
    handle = theme.get("scrollbar_handle", "#3f3f46")
    handle_hover = theme.get("scrollbar_handle_hover", "#52525b")
    return f"""
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {handle};
            min-height: 24px;
            border-radius: 4px;
            margin: 1px 2px;
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
            height: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {handle};
            min-width: 24px;
            border-radius: 4px;
            margin: 2px 1px;
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
    """Returns a programming font with ligatures explicitly disabled and native fallbacks."""
    font = QFont(family, size)
    if bold:
        font.setBold(True)
    font.setStyleHint(QFont.StyleHint.Monospace)
    font.setFamilies([family, "Menlo", "Monaco", "Courier New", "monospace"])
    configure_no_ligatures(font)
    return font


