import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from theme import DARK_THEME


class PythonHighlighter(QSyntaxHighlighter):
    """Dynamic Python syntax highlighter that supports Dark and Light themes."""

    def __init__(self, document, theme=DARK_THEME):
        super().__init__(document)
        self.rules = []
        self.apply_theme(theme)

    def apply_theme(self, theme):
        self.rules = []

        # 1. Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(theme["syntax_keyword"]))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "finally", "for", "from",
            "global", "if", "import", "in", "is", "lambda", "not", "or",
            "pass", "raise", "return", "try", "while", "with", "yield",
        ]
        for word in keywords:
            pattern = re.compile(rf"\b{word}\b")
            self.rules.append((pattern, keyword_format))

        # 2. Built-in constants
        const_format = QTextCharFormat()
        const_format.setForeground(QColor(theme["syntax_constant"]))
        for word in ["True", "False", "None"]:
            pattern = re.compile(rf"\b{word}\b")
            self.rules.append((pattern, const_format))

        # 3. Built-in functions
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(theme["syntax_builtin"]))
        for word in ["print", "range", "len", "input", "int", "str", "float", "list", "dict", "set", "type"]:
            pattern = re.compile(rf"\b{word}\b")
            self.rules.append((pattern, builtin_format))

        # 4. Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(theme["syntax_string"]))
        self.rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # 5. Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(theme["syntax_number"]))
        self.rules.append((re.compile(r"\b[0-9]+(\.[0-9]+)?\b"), number_format))

        # 6. Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(theme["syntax_comment"]))
        comment_format.setFontItalic(True)
        self.rules.append((re.compile(r"#[^\n]*"), comment_format))

        # Trigger rehighlighting
        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
