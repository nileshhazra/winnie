import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from theme import DARK_THEME


class PythonHighlighter(QSyntaxHighlighter):
    """Dynamic Python syntax highlighter accurately matching ziadyjo/codesandbox-black-theme.
    Supports CodeSandbox Black dark mode and macOS porcelain light mode.
    """

    STATE_NORMAL = 0
    STATE_TRIPLE_DOUBLE = 1
    STATE_TRIPLE_SINGLE = 2

    def __init__(self, document, theme=DARK_THEME):
        super().__init__(document)
        self.apply_theme(theme)

    def apply_theme(self, theme):
        self.theme = theme

        # 1. Keywords / Control / Storage (CodeSandbox Lilac/Purple #C678DD)
        self.kw_fmt = QTextCharFormat()
        self.kw_fmt.setForeground(QColor(theme.get("syntax_keyword", "#C678DD")))

        # 2. Classes / Types (Warm Gold/Yellow #E5C07B)
        self.class_fmt = QTextCharFormat()
        self.class_fmt.setForeground(QColor(theme.get("syntax_class", "#E5C07B")))

        # 3. Inherited Classes in class def (Emerald Mint #41B883)
        self.inherited_fmt = QTextCharFormat()
        self.inherited_fmt.setForeground(QColor(theme.get("syntax_inherited", "#41B883")))

        # 4. Functions & Methods (Sky Blue #61AFEF)
        self.func_fmt = QTextCharFormat()
        self.func_fmt.setForeground(QColor(theme.get("syntax_function", "#61AFEF")))

        # 5. Variables (self, cls, dunder) (Coral Red #E06C75)
        self.var_fmt = QTextCharFormat()
        self.var_fmt.setForeground(QColor(theme.get("syntax_variable", "#E06C75")))

        # 6. Function Parameters in def (Warm Orange/Peach #D19A66)
        self.param_fmt = QTextCharFormat()
        self.param_fmt.setForeground(QColor(theme.get("syntax_parameter", "#D19A66")))

        # 7. Constants, Numbers & Booleans (Warm Orange #D19A66)
        self.num_fmt = QTextCharFormat()
        self.num_fmt.setForeground(QColor(theme.get("syntax_number", "#D19A66")))

        self.const_fmt = QTextCharFormat()
        self.const_fmt.setForeground(QColor(theme.get("syntax_constant", "#D19A66")))

        # 8. Builtin Utilities & Exceptions (Cyan #56B6C2)
        self.builtin_fmt = QTextCharFormat()
        self.builtin_fmt.setForeground(QColor(theme.get("syntax_builtin", "#56B6C2")))

        # 9. Strings (Emerald Mint #41B883)
        self.str_fmt = QTextCharFormat()
        self.str_fmt.setForeground(QColor(theme.get("syntax_string", "#41B883")))

        # 10. Comments (Slate Gray #5C6370)
        self.comment_fmt = QTextCharFormat()
        self.comment_fmt.setForeground(QColor(theme.get("syntax_comment", "#5C6370")))
        self.comment_fmt.setFontItalic(False)

        # 11. Punctuation & Operators (Soft Silver #ABB2BF)
        self.op_fmt = QTextCharFormat()
        self.op_fmt.setForeground(QColor(theme.get("syntax_operator", "#ABB2BF")))

        # Compiled Regexes
        self.re_operators = re.compile(r"[+\-*/%&=<>!^~|:;,.?]+|[(){}\[\]]")
        self.re_numbers = re.compile(r"\b0[xX][0-9a-fA-F]+\b|\b0[bB][01]+\b|\b[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?\b")
        self.re_constants = re.compile(r"\b(True|False|None)\b|\b[A-Z_][A-Z0-9_]{1,}\b")
        self.re_classes = re.compile(r"\b[A-Z][a-zA-Z0-9_]*\b")
        self.re_builtin_types = re.compile(r"\b(int|float|str|list|dict|set|tuple|bool|bytes|object|type)\b")
        self.re_builtin_exceptions = re.compile(r"\b(Exception|ValueError|TypeError|KeyError|IndexError|AttributeError|IOError|FileNotFoundError|RuntimeError|ZeroDivisionError|StopIteration)\b")
        self.re_func_calls = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)(?=\s*\()")
        self.re_def_names = re.compile(r"\bdef\s+([A-Za-z_][A-Za-z0-9_]*)")
        self.re_def_params = re.compile(r"\bdef\s+[A-Za-z0-9_]+\s*\(([^)]*)\)")
        self.re_class_def = re.compile(r"\bclass\s+([A-Za-z0-9_]+)\s*(?:\(([^)]*)\))?")
        self.re_self = re.compile(r"\b(self|cls)\b")
        self.re_dunder = re.compile(r"\b__[a-zA-Z0-9_]+__\b")
        self.re_decorators = re.compile(r"@[A-Za-z_][A-Za-z0-9_.]*")

        keywords = [
            "and", "as", "assert", "async", "await", "break", "class", "continue",
            "def", "del", "elif", "else", "except", "finally", "for", "from",
            "global", "if", "import", "in", "is", "lambda", "nonlocal", "not",
            "or", "pass", "raise", "return", "try", "while", "with", "yield",
        ]
        self.re_keywords = re.compile(r"\b(" + "|".join(keywords) + r")\b")

        self.re_single_str = re.compile(r"""[fFrRuUbB]?('[^'\\]*(\\.[^'\\]*)*'|"[^"\\]*(\\.[^"\\]*)*")""")
        self.re_comment = re.compile(r"#[^\n]*")

        self.rehighlight()

    def highlightBlock(self, text):
        if not text:
            self.setCurrentBlockState(self.STATE_NORMAL)
            return

        # 1. Operators & punctuation
        for m in self.re_operators.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.op_fmt)

        # 2. Numbers
        for m in self.re_numbers.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.num_fmt)

        # 3. PascalCase classes & Builtin Types
        for m in self.re_classes.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.class_fmt)
        for m in self.re_builtin_types.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.class_fmt)
        for m in self.re_builtin_exceptions.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.builtin_fmt)

        # 4. UPPER_CASE constants & True, False, None
        for m in self.re_constants.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.const_fmt)

        # 5. Function & method calls
        for m in self.re_func_calls.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.func_fmt)

        # 6. Function definitions & parameter lists
        for m in self.re_def_names.finditer(text):
            self.setFormat(m.start(1), len(m.group(1)), self.func_fmt)

        for m in self.re_def_params.finditer(text):
            param_str = m.group(1)
            offset = m.start(1)
            for pm in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]*\b", param_str):
                p_word = pm.group()
                p_start = offset + pm.start()
                p_len = len(p_word)
                if p_word in ("self", "cls"):
                    self.setFormat(p_start, p_len, self.var_fmt)
                else:
                    self.setFormat(p_start, p_len, self.param_fmt)

        # 7. Class definition and inherited classes
        for m in self.re_class_def.finditer(text):
            c_name = m.group(1)
            self.setFormat(m.start(1), len(c_name), self.class_fmt)
            if m.group(2):
                inh_str = m.group(2)
                offset = m.start(2)
                for im in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]*\b", inh_str):
                    self.setFormat(offset + im.start(), len(im.group()), self.inherited_fmt)

        # 8. Self, cls, and dunder names
        for m in self.re_self.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.var_fmt)
        for m in self.re_dunder.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.var_fmt)

        # 9. Decorators
        for m in self.re_decorators.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.func_fmt)

        # 10. Keywords
        for m in self.re_keywords.finditer(text):
            self.setFormat(m.start(), m.end() - m.start(), self.kw_fmt)

        # 11. Multi-line Strings & Single-line Strings
        self._highlight_strings(text)

        # 12. Comments
        for m in self.re_comment.finditer(text):
            if self.currentBlockState() in (self.STATE_TRIPLE_DOUBLE, self.STATE_TRIPLE_SINGLE):
                continue
            self.setFormat(m.start(), m.end() - m.start(), self.comment_fmt)

    def _highlight_strings(self, text):
        self.setCurrentBlockState(self.STATE_NORMAL)
        prev_state = self.previousBlockState()

        # Handle continuation of multiline triple quotes
        if prev_state == self.STATE_TRIPLE_DOUBLE:
            end_match = re.search(r'"""', text)
            if not end_match:
                self.setCurrentBlockState(self.STATE_TRIPLE_DOUBLE)
                self.setFormat(0, len(text), self.str_fmt)
                return
            else:
                self.setFormat(0, end_match.end(), self.str_fmt)
                self._highlight_single_strings(text[end_match.end():], offset=end_match.end())
                return
        elif prev_state == self.STATE_TRIPLE_SINGLE:
            end_match = re.search(r"'''", text)
            if not end_match:
                self.setCurrentBlockState(self.STATE_TRIPLE_SINGLE)
                self.setFormat(0, len(text), self.str_fmt)
                return
            else:
                self.setFormat(0, end_match.end(), self.str_fmt)
                self._highlight_single_strings(text[end_match.end():], offset=end_match.end())
                return

        t_double = text.find('"""')
        t_single = text.find("'''")

        if t_double != -1 and (t_single == -1 or t_double < t_single):
            closing = text.find('"""', t_double + 3)
            if closing == -1:
                self.setCurrentBlockState(self.STATE_TRIPLE_DOUBLE)
                self.setFormat(t_double, len(text) - t_double, self.str_fmt)
                self._highlight_single_strings(text[:t_double], offset=0)
                return
            else:
                self.setFormat(t_double, closing + 3 - t_double, self.str_fmt)
                self._highlight_single_strings(text[:t_double], offset=0)
                self._highlight_single_strings(text[closing + 3:], offset=closing + 3)
                return
        elif t_single != -1 and (t_double == -1 or t_single < t_double):
            closing = text.find("'''", t_single + 3)
            if closing == -1:
                self.setCurrentBlockState(self.STATE_TRIPLE_SINGLE)
                self.setFormat(t_single, len(text) - t_single, self.str_fmt)
                self._highlight_single_strings(text[:t_single], offset=0)
                return
            else:
                self.setFormat(t_single, closing + 3 - t_single, self.str_fmt)
                self._highlight_single_strings(text[:t_single], offset=0)
                self._highlight_single_strings(text[closing + 3:], offset=closing + 3)
                return

        self._highlight_single_strings(text, offset=0)

    def _highlight_single_strings(self, text, offset=0):
        if not text:
            return
        for m in self.re_single_str.finditer(text):
            self.setFormat(offset + m.start(), m.end() - m.start(), self.str_fmt)
