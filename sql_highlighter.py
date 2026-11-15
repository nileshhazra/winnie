"""
SQL Syntax Highlighter for Winnie SQL Playground.
Supports Dark and Light themes with Winnie's signature honey amber accent styling.
"""

import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from theme import DARK_THEME


class SqlHighlighter(QSyntaxHighlighter):
    """Dynamic SQL syntax highlighter supporting case-insensitive SQL keywords, functions, and literals."""

    def __init__(self, document, theme=DARK_THEME):
        super().__init__(document)
        self.rules = []
        self.apply_theme(theme)

    def apply_theme(self, theme):
        self.rules = []

        # 1. Primary SQL Keywords (SELECT, FROM, WHERE, JOIN, GROUP BY, etc.)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(theme.get("syntax_keyword", "#F43F5E")))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            "SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "OUTER", "CROSS",
            "ON", "GROUP BY", "HAVING", "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
            "WITH", "AS", "UNION", "ALL", "INTERSECT", "EXCEPT", "CASE", "WHEN", "THEN", "ELSE", "END",
            "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE", "CREATE", "DROP", "ALTER",
            "TABLE", "VIEW", "INDEX", "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "NOT", "NULL",
            "DEFAULT", "CHECK", "UNIQUE", "AUTOINCREMENT", "EXPLAIN", "QUERY", "PLAN", "PRAGMA"
        ]
        for word in keywords:
            pattern = re.compile(rf"\b{word}\b", re.IGNORECASE)
            self.rules.append((pattern, keyword_format))

        # 2. SQL Logical Operators & Predicates
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(theme.get("syntax_constant", "#38BDF8")))
        operator_format.setFontWeight(QFont.Weight.Medium)
        operators = ["AND", "OR", "IN", "NOT IN", "BETWEEN", "LIKE", "ILIKE", "IS", "IS NOT", "EXISTS", "ANY", "ALL"]
        for op in operators:
            pattern = re.compile(rf"\b{op}\b", re.IGNORECASE)
            self.rules.append((pattern, operator_format))

        # 3. Built-in SQL Aggregate & Window Functions
        func_format = QTextCharFormat()
        func_format.setForeground(QColor(theme.get("syntax_builtin", "#F59E0B")))
        func_format.setFontWeight(QFont.Weight.DemiBold)
        functions = [
            "COUNT", "SUM", "AVG", "MIN", "MAX",
            "ROW_NUMBER", "RANK", "DENSE_RANK", "NTILE", "LEAD", "LAG", "FIRST_VALUE", "LAST_VALUE", "OVER", "PARTITION BY",
            "COALESCE", "NULLIF", "ROUND", "ABS", "UPPER", "LOWER", "LENGTH", "SUBSTR", "TRIM",
            "CAST", "DATE", "TIME", "DATETIME", "STRFTIME", "JULIANDAY"
        ]
        for func in functions:
            pattern = re.compile(rf"\b{func}\b", re.IGNORECASE)
            self.rules.append((pattern, func_format))

        # 4. SQL Data Types
        type_format = QTextCharFormat()
        type_format.setForeground(QColor(theme.get("accent_warning", "#EAB308")))
        types = ["INTEGER", "TEXT", "REAL", "NUMERIC", "BLOB", "VARCHAR", "BOOLEAN", "TIMESTAMP", "DATE", "DECIMAL"]
        for t in types:
            pattern = re.compile(rf"\b{t}\b", re.IGNORECASE)
            self.rules.append((pattern, type_format))

        # 5. Strings ('single quotes' and "double quotes")
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(theme.get("syntax_string", "#34D399")))
        self.rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        self.rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))

        # 6. Numbers (integers, floats)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(theme.get("syntax_number", "#FBBF24")))
        self.rules.append((re.compile(r"\b[0-9]+(\.[0-9]+)?\b"), number_format))

        # 7. SQL Comments (-- line comments and /* block comments */)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(theme.get("syntax_comment", "#6B7280")))
        comment_format.setFontItalic(False)
        self.rules.append((re.compile(r"--[^\n]*"), comment_format))
        self.rules.append((re.compile(r"/\*.*?\*/", re.DOTALL), comment_format))

        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
