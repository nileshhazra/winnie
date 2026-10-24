import re
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QPushButton,
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Signal
from theme import DARK_THEME


# ==========================================================
# Beginner Error Knowledge Base
# ==========================================================
ERROR_KNOWLEDGE_BASE = {
    "NameError": {
        "title": "Using a variable that hasn't been created yet",
        "explanation": (
            "Python doesn't recognize this name. This usually happens when:\n"
            "• You misspelled a variable or function name (Python is case-sensitive!)\n"
            "• You used a variable before creating (assigning) it\n"
            "• You forgot to put quotes around a word that should be a string (e.g. text instead of 'text')"
        ),
        "tip": "Check the spelling of the name on the highlighted line, or make sure it was defined earlier in your script."
    },
    "IndexError": {
        "title": "Index is out of range",
        "explanation": (
            "You tried to access an element at an index that doesn't exist in the list or string.\n"
            "Remember that Python starts counting from 0:\n"
            "• 1st item is at index [0]\n"
            "• 2nd item is at index [1]\n"
            "• 3rd item is at index [2]"
        ),
        "tip": "If a list has 3 items, the highest valid index is 2. Check len(your_list) to see how many items it contains."
    },
    "TypeError": {
        "title": "Combining incompatible data types",
        "explanation": (
            "An operation was performed on a data type that doesn't support it.\n"
            "Common examples:\n"
            "• Trying to add text and a number together: 'Score: ' + 10 (use f'Score: {10}' or str(10))\n"
            "• Trying to call something that isn't a function: x() when x is a number or string\n"
            "• Calling a function with the wrong number of arguments"
        ),
        "tip": "Look at the types of your variables using type(variable) or check the Variables tab on the right."
    },
    "SyntaxError": {
        "title": "Python grammar / punctuation error",
        "explanation": (
            "Python couldn't understand the structure of this line. Common causes:\n"
            "• Missing a colon (:) at the end of an if, for, while, or def statement\n"
            "• An unclosed parenthesis, bracket, or quotation mark\n"
            "• Using a single '=' (assignment) instead of '==' (comparison) inside an if condition"
        ),
        "tip": "Check the highlighted line (and the line right above it) for missing colons, commas, or unmatched brackets."
    },
    "IndentationError": {
        "title": "Incorrect indentation (spaces/tabs)",
        "explanation": (
            "Python relies on indentation (spaces) to know which lines belong inside a function, loop, or if-statement.\n"
            "This error means lines aren't lined up properly or an expected indented block is missing (e.g. right after a colon :)."
        ),
        "tip": "Make sure lines inside a block are indented with 4 spaces. If a block is currently empty, you can write 'pass'."
    },
    "ZeroDivisionError": {
        "title": "Division by zero",
        "explanation": (
            "You attempted to divide a number by 0 (e.g. x / 0 or x % 0), which is mathematically undefined."
        ),
        "tip": "Check the divisor variable before dividing, or use an if-statement: if divisor != 0: ..."
    },
    "KeyError": {
        "title": "Dictionary key does not exist",
        "explanation": (
            "You tried to look up a key in a dictionary (e.g. user['age']), but that key is not in the dictionary."
        ),
        "tip": "Use your_dict.get('key') to return None safely instead of crashing, or check 'if key in your_dict:' first."
    },
    "AttributeError": {
        "title": "Object does not have this property or method",
        "explanation": (
            "You called a method or property on a variable that doesn't have it.\n"
            "For example, trying to call .append() on a string (append is for lists, not strings), or calling a method on None."
        ),
        "tip": "Verify the type of the object. Check if the variable accidentally became None before this line."
    },
    "ValueError": {
        "title": "Valid type, but invalid value",
        "explanation": (
            "A function received an argument of the right type, but an inappropriate value.\n"
            "For example: int('hello') fails because the string 'hello' cannot be converted into an integer."
        ),
        "tip": "Check what value is being passed to the function. If reading user input with input(), ensure it's numeric before int()."
    },
    "FileNotFoundError": {
        "title": "File not found on disk",
        "explanation": (
            "Python tried to open a file (open('data.txt')), but the file does not exist at that path."
        ),
        "tip": "Check the file name and make sure the file is located in the same directory, or provide an absolute path."
    },
    "UnboundLocalError": {
        "title": "Local variable referenced before assignment",
        "explanation": (
            "Inside a function, you tried to read or modify a variable before assigning a value to it locally."
        ),
        "tip": "Assign a value to the variable at the top of the function, or declare it 'global' if modifying an outside variable."
    },
    "RecursionError": {
        "title": "Function called itself too many times (Infinite Recursion)",
        "explanation": (
            "A recursive function kept calling itself without reaching a stopping condition (base case)."
        ),
        "tip": "Ensure your recursive function has a base case (an if-statement that returns without calling the function again)."
    }
}


def parse_traceback(stderr_text: str):
    """Extracts error type, message, line number, and offending code line from standard traceback."""
    if not stderr_text or "Traceback (most recent call last):" not in stderr_text:
        return None

    # Find the last line like "ErrorType: message"
    lines = stderr_text.strip().splitlines()
    error_line = lines[-1]
    
    error_type = None
    error_msg = ""
    if ":" in error_line:
        parts = error_line.split(":", 1)
        error_type = parts[0].strip()
        error_msg = parts[1].strip()
    else:
        error_type = error_line.strip()

    # Find the offending line number (e.g. line 4)
    line_number = None
    code_snippet = None
    line_matches = list(re.finditer(r'line\s+(\d+)', stderr_text, re.IGNORECASE))
    if line_matches:
        line_number = int(line_matches[-1].group(1))

    # Find the code line right above the error
    for i in range(len(lines) - 2, -1, -1):
        stripped = lines[i].strip()
        if stripped and not stripped.startswith("File "):
            code_snippet = stripped
            break

    return {
        "error_type": error_type,
        "error_msg": error_msg,
        "line_number": line_number,
        "code_snippet": code_snippet,
    }


class AssistantView(QWidget):
    """The Beginner Error Assistant panel that explains tracebacks in plain English."""
    jump_to_line_requested = Signal(int)

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.current_error = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # Scroll Area for long explanations
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(4, 4, 4, 4)
        self.container_layout.setSpacing(10)
        scroll.setWidget(self.container)

        layout.addWidget(scroll)

        # Initial Empty State
        self.show_success_state()

    def show_success_state(self):
        """Displays when no errors have occurred."""
        self.clear_container()
        self.current_error = None

        msg_label = QLabel("No errors detected.\nRun your code to check for hints and explanations.")
        msg_label.setFont(QFont("SF Pro Text", 12))
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet("color: #71717a; padding: 40px 10px;")
        self.container_layout.addWidget(msg_label)
        self.container_layout.addStretch()

    def show_error(self, error_info):
        """Formats and displays the parsed error in plain English."""
        self.clear_container()
        self.current_error = error_info

        err_type = error_info["error_type"]
        err_msg = error_info["error_msg"]
        line_num = error_info["line_number"]
        code_snippet = error_info["code_snippet"]

        kb_entry = ERROR_KNOWLEDGE_BASE.get(err_type, {
            "title": f"An unhandled {err_type} occurred",
            "explanation": f"Python encountered: {err_msg}",
            "tip": "Check the highlighted line for unexpected values or unhandled edge cases."
        })

        # 1. Error Badge & Line Button Header
        header = QHBoxLayout()
        badge = QLabel(f"  {err_type}  ")
        badge.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        badge.setStyleSheet("""
            background-color: #ef4444;
            color: #ffffff;
            border-radius: 6px;
            padding: 3px 8px;
        """)
        header.addWidget(badge)

        if line_num:
            line_btn = QPushButton(f"Line {line_num}  →")
            line_btn.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
            line_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            line_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3f3f46;
                    color: #fbbf24;
                    border: none;
                    border-radius: 6px;
                    padding: 3px 8px;
                }
                QPushButton:hover {
                    background-color: #52525b;
                }
            """)
            line_btn.clicked.connect(lambda: self.jump_to_line_requested.emit(line_num))
            header.addWidget(line_btn)

        header.addStretch()
        self.container_layout.addLayout(header)

        # 2. Plain English Title
        title = QLabel(kb_entry["title"])
        title.setFont(QFont("SF Pro Display", 13, QFont.Weight.Bold))
        title.setWordWrap(True)
        title.setStyleSheet(f"color: {self.current_theme['brand_color']};")
        self.container_layout.addWidget(title)

        # 3. Offending Code Snippet Box (if available)
        if code_snippet:
            code_box = QLabel(code_snippet)
            code_box.setFont(QFont("Dank Mono", 12))
            code_box.setStyleSheet(f"""
                background-color: {self.current_theme['table_bg']};
                color: #f87171;
                border: 1px solid {self.current_theme['table_border']};
                border-radius: 6px;
                padding: 8px;
            """)
            self.container_layout.addWidget(code_box)

        # 4. Explanation Card
        exp_header = QLabel("WHAT HAPPENED")
        exp_header.setFont(QFont("SF Pro Text", 10, QFont.Weight.Bold))
        exp_header.setStyleSheet("color: #71717a; letter-spacing: 0.5px;")
        self.container_layout.addWidget(exp_header)

        explanation = QLabel(kb_entry["explanation"])
        explanation.setFont(QFont("SF Pro Text", 12))
        explanation.setWordWrap(True)
        explanation.setStyleSheet(f"color: {self.current_theme['table_text']}; line-height: 1.4;")
        self.container_layout.addWidget(explanation)

        # 5. How to Fix Card
        fix_header = QLabel("HOW TO FIX")
        fix_header.setFont(QFont("SF Pro Text", 10, QFont.Weight.Bold))
        fix_header.setStyleSheet("color: #10b981; letter-spacing: 0.5px; margin-top: 6px;")
        self.container_layout.addWidget(fix_header)

        tip_label = QLabel(kb_entry["tip"])
        tip_label.setFont(QFont("SF Pro Text", 12))
        tip_label.setWordWrap(True)
        tip_label.setStyleSheet(f"color: {self.current_theme['table_text']};")
        self.container_layout.addWidget(tip_label)

        self.container_layout.addStretch()

    def clear_container(self):
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

    def apply_theme(self, theme):
        self.current_theme = theme
        if self.current_error:
            self.show_error(self.current_error)
        else:
            self.show_success_state()
