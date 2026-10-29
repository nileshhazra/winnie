from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QFont, QTextCursor, QKeySequence
from PySide6.QtCore import Qt, Signal
from theme import DARK_THEME, get_scrollbar_stylesheet, get_code_font


class InteractiveConsole(QPlainTextEdit):
    """An interactive console with theme switching support."""
    input_submitted = Signal(str)

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        
        font = get_code_font(size=13)
        self.setFont(font)
        self.document().setDefaultFont(font)
        
        self.input_start_pos = 0
        self.is_running = False
        self.apply_theme(theme)

    def apply_theme(self, theme):
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {theme['console_bg']};
                color: {theme['console_text']};
                padding: 10px;
                border: none;
                border-top: 1px solid {theme['console_border']};
                selection-background-color: {theme['editor_selection']};
            }}
            {get_scrollbar_stylesheet(theme)}
        """)

    def append_output(self, text: str):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
        self.input_start_pos = self.textCursor().position()

    def set_running_state(self, running: bool):
        self.is_running = running
        if running:
            self.input_start_pos = self.textCursor().position()

    def keyPressEvent(self, event):
        if not self.is_running:
            if event.matches(QKeySequence.StandardKey.Copy):
                super().keyPressEvent(event)
            return

        cursor = self.textCursor()

        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)
            
            full_text = self.toPlainText()
            user_input = full_text[self.input_start_pos:]
            
            cursor.insertText("\n")
            self.input_start_pos = self.textCursor().position()
            self.input_submitted.emit(user_input + "\n")
            return

        if event.key() == Qt.Key.Key_Backspace and cursor.position() <= self.input_start_pos:
            return

        if cursor.position() < self.input_start_pos:
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)

        super().keyPressEvent(event)
