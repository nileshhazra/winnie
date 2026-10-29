from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget
from PySide6.QtGui import QColor, QPainter, QPainterPath, QTextFormat, QFont, QTextCursor
from PySide6.QtCore import Qt, QRect, QSize
from highlighter import PythonHighlighter
from theme import DARK_THEME, get_scrollbar_stylesheet, get_code_font


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.line_number_area = LineNumberArea(self)
        self.debug_line = None

        # Tab & File metadata
        self.file_path = None
        self.is_modified = False
        self.problem_data = None
        self.untitled_title = "Untitled"

        # Dank Mono with Menlo fallback, font ligatures explicitly turned off
        font = get_code_font(size=13)
        self.setFont(font)
        self.document().setDefaultFont(font)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Attach syntax highlighter
        self.highlighter = PythonHighlighter(self.document(), theme=self.current_theme)

        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.highlighter.apply_theme(theme)

        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {theme['editor_bg']};
                color: {theme['editor_text']};
                border: none;
                selection-background-color: {theme['editor_selection']};
                padding: 6px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.line_number_area.update()

    def line_number_area_width(self):
        digits = max(1, len(str(self.blockCount())))
        # Dedicated indicator space (24px) + digit width + right padding (12px)
        space = 36 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []

        # 1. Debug line highlight (amber/yellow)
        if self.debug_line is not None and self.debug_line > 0:
            block = self.document().findBlockByNumber(self.debug_line - 1)
            if block.isValid():
                debug_sel = QTextEdit.ExtraSelection()
                debug_sel.format.setBackground(QColor(self.current_theme["debug_line_bg"]))
                debug_sel.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
                debug_cursor = self.textCursor()
                debug_cursor.setPosition(block.position())
                debug_cursor.clearSelection()
                debug_sel.cursor = debug_cursor
                extra_selections.append(debug_sel)

        # 2. Normal cursor line highlight
        if not self.isReadOnly() and self.debug_line is None:
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(self.current_theme["current_line"]))
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def set_debug_line(self, line_number: int):
        """Highlights the active debugging line and scrolls to it."""
        self.debug_line = line_number
        self.highlight_current_line()
        self.line_number_area.update()
        if line_number is not None and line_number > 0:
            block = self.document().findBlockByNumber(line_number - 1)
            if block.isValid():
                cursor = self.textCursor()
                cursor.setPosition(block.position())
                self.setTextCursor(cursor)
                self.ensureCursorVisible()

    def clear_debug_line(self):
        """Clears the debugging line highlight."""
        self.debug_line = None
        self.highlight_current_line()
        self.line_number_area.update()

    def keyPressEvent(self, event):
        """Smart Python auto-indentation and tab handling."""
        # 1. Auto-indentation after ':' or preserving current indentation on Enter
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            current_line = cursor.block().text()[:cursor.positionInBlock()]

            # Determine existing indentation
            indent = ""
            for char in current_line:
                if char in (" ", "\t"):
                    indent += char
                else:
                    break

            # If the statement ends with ':', indent an extra 4 spaces
            code_part = current_line.split("#")[0].rstrip()
            if code_part.endswith(":"):
                indent += "    "

            cursor.insertText("\n" + indent)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            return

        # 2. Tab key inserts 4 spaces (PEP 8)
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
            return

        # 3. Backspace deletes 4 spaces of indentation at once
        if event.key() == Qt.Key.Key_Backspace:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                pos = cursor.positionInBlock()
                line_prefix = cursor.block().text()[:pos]
                if line_prefix and line_prefix.isspace() and len(line_prefix) % 4 == 0:
                    cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, 4)
                    cursor.removeSelectedText()
                    return

        super().keyPressEvent(event)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.setFont(self.font())
        painter.fillRect(event.rect(), QColor(self.current_theme["gutter_bg"]))

        # Subtle vertical separator line
        painter.setPen(QColor(self.current_theme["gutter_border"]))
        painter.drawLine(self.line_number_area.width() - 1, event.rect().top(),
                         self.line_number_area.width() - 1, event.rect().bottom())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                
                font_h = self.fontMetrics().height()

                # If this is the active debug execution line, draw the clean amber step pointer
                if self.debug_line == block_number + 1:
                    painter.save()
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    arrow_h = min(11.0, font_h * 0.62)
                    arrow_w = arrow_h * 0.85
                    arrow_x = 7.0
                    arrow_y = top + (font_h - arrow_h) / 2.0

                    arrow = QPainterPath()
                    arrow.moveTo(arrow_x, arrow_y)
                    arrow.lineTo(arrow_x + arrow_w, arrow_y + arrow_h / 2.0)
                    arrow.lineTo(arrow_x, arrow_y + arrow_h)
                    arrow.closeSubpath()

                    painter.fillPath(arrow, QColor("#fbbf24"))
                    painter.restore()

                    # Highlight the active line number in matching amber
                    painter.setPen(QColor("#fbbf24"))
                else:
                    painter.setPen(QColor(self.current_theme["gutter_text"]))

                painter.drawText(
                    0, top, self.line_number_area.width() - 10,
                    font_h,
                    Qt.AlignmentFlag.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
