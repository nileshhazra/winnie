from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
)
from PySide6.QtGui import QFont, QColor
from theme import DARK_THEME


class VariablesView(QWidget):
    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.current_vars = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Header Title
        self.title = QLabel("✦ VARIABLES")
        self.title.setFont(QFont("SF Pro Display", 11, QFont.Weight.Bold))
        layout.addWidget(self.title)

        # Variables Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        font = QFont("Dank Mono", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.table.setFont(font)

        layout.addWidget(self.table)
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.title.setStyleSheet(f"color: {theme['table_header_text']}; letter-spacing: 1px; padding: 2px;")
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {theme['table_bg']};
                color: {theme['table_text']};
                gridline-color: {theme['table_border']};
                border: 1px solid {theme['table_border']};
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {theme['table_header_bg']};
                color: {theme['table_header_text']};
                font-size: 11px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid {theme['table_border']};
                padding: 6px;
            }}
        """)
        # Refresh colors of existing items
        if self.current_vars:
            self.update_variables(self.current_vars)

    def update_variables(self, var_list):
        self.current_vars = var_list
        self.table.setRowCount(0)
        for row_idx, var in enumerate(var_list):
            self.table.insertRow(row_idx)

            name_item = QTableWidgetItem(var["name"])
            name_item.setForeground(QColor(self.current_theme["var_name"]))

            type_item = QTableWidgetItem(var["type"])
            type_item.setForeground(QColor(self.current_theme["var_type"]))

            val_item = QTableWidgetItem(var["value"])
            val_color = self.current_theme["var_str"] if var["type"] == "str" else self.current_theme["table_text"]
            val_item.setForeground(QColor(val_color))

            self.table.setItem(row_idx, 0, name_item)
            self.table.setItem(row_idx, 1, type_item)
            self.table.setItem(row_idx, 2, val_item)

    def clear(self):
        self.current_vars = []
        self.table.setRowCount(0)
