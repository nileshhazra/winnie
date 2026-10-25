from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QPlainTextEdit,
    QLineEdit,
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Signal
from theme import DARK_THEME
from highlighter import PythonHighlighter


# ==========================================================
# Problems Database (Add new problems here)
# ==========================================================
PROBLEMS_DATA = [
    {
        "id": "max_value",
        "title": "1. max value",
        "raw_title": "max value",
        "description": (
            "Write a function, max_value, that takes in list of numbers as an argument. "
            "The function should return the largest number in the list.\n\n"
            "Solve this without using any built-in list methods. "
            "You can assume that the list is non-empty."
        ),
        "starter_code": "def max_value(nums):\n  pass # todo\n",
        "solution_code": (
            "def max_value(nums):\n"
            "    maximum = nums[0]\n"
            "    for n in nums:\n"
            "        if n > maximum:\n"
            "            maximum = n\n"
            "    return maximum\n\n"
            "# Example test cases:\n"
            "print(max_value([4, 7, 2, 8, 10, 9])) # -> 10\n"
            "print(max_value([10, 5, 40, 40.3]))   # -> 40.3\n"
            "print(max_value([-5, -2, -1, -11]))   # -> -1\n"
        ),
    }
]


# ==========================================================
# Problem Description View (Right Panel Tab 1)
# ==========================================================
class ProblemDescriptionWidget(QWidget):
    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(12)
        scroll.setWidget(container)

        # Title
        self.title_label = QLabel()
        self.title_label.setFont(QFont("SF Pro Display", 15, QFont.Weight.Bold))
        self.title_label.setWordWrap(True)
        self.container_layout.addWidget(self.title_label)

        # Badge
        self.badge_label = QLabel("  Practice Problem  ")
        self.badge_label.setFont(QFont("SF Pro Text", 10, QFont.Weight.Bold))
        self.badge_label.setStyleSheet("""
            background-color: #0284c7;
            color: #ffffff;
            border-radius: 4px;
            padding: 2px 6px;
        """)
        self.container_layout.addWidget(self.badge_label)

        # Description
        self.desc_label = QLabel()
        self.desc_label.setFont(QFont("SF Pro Text", 12))
        self.desc_label.setWordWrap(True)
        self.container_layout.addWidget(self.desc_label)

        self.container_layout.addStretch()
        layout.addWidget(scroll)

        self.apply_theme(self.current_theme)

    def set_problem(self, problem):
        self.title_label.setText(problem.get("title", ""))
        self.desc_label.setText(problem.get("description", ""))

    def apply_theme(self, theme):
        self.current_theme = theme
        self.title_label.setStyleSheet(f"color: {theme['brand_color']}; font-weight: bold;")
        self.desc_label.setStyleSheet(f"color: {theme['table_text']}; font-size: 13px;")


# ==========================================================
# Problem Solution View (Right Panel Tab 2)
# ==========================================================
class ProblemSolutionWidget(QWidget):
    copy_to_editor_requested = Signal(str)

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.current_solution = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        self.header_label = QLabel("Solution Code")
        self.header_label.setFont(QFont("SF Pro Display", 13, QFont.Weight.Bold))
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()

        self.copy_btn = QPushButton("Copy to Editor")
        self.copy_btn.setFont(QFont("SF Pro Text", 11))
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.on_copy_clicked)
        header_layout.addWidget(self.copy_btn)

        layout.addLayout(header_layout)

        self.solution_view = QPlainTextEdit()
        self.solution_view.setFont(QFont("Dank Mono", 12))
        self.solution_view.setReadOnly(True)
        self.highlighter = PythonHighlighter(self.solution_view.document(), theme=self.current_theme)
        layout.addWidget(self.solution_view)

        self.apply_theme(self.current_theme)

    def set_problem(self, problem):
        self.current_solution = problem.get("solution_code", "")
        self.solution_view.setPlainText(self.current_solution)

    def on_copy_clicked(self):
        if self.current_solution:
            self.copy_to_editor_requested.emit(self.current_solution)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.header_label.setStyleSheet(f"color: {theme['brand_color']};")
        self.highlighter.apply_theme(theme)
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 6px;
                padding: 4px 10px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)
        self.solution_view.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {theme['console_bg']};
                color: {theme['console_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 8px;
            }}
        """)


# ==========================================================
# Problems List Selection Dialog
# ==========================================================
class ProblemsListDialog(QDialog):
    problem_selected = Signal(dict)

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.setWindowTitle("Practice Problems")
        self.resize(480, 360)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        self.header_label = QLabel("Choose a Problem")
        self.header_label.setFont(QFont("SF Pro Display", 14, QFont.Weight.Bold))
        layout.addWidget(self.header_label)

        # Search filter
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter problems...")
        self.search_input.setFont(QFont("SF Pro Text", 12))
        self.search_input.textChanged.connect(self.filter_problems)
        layout.addWidget(self.search_input)

        # List of problems
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("SF Pro Text", 13))
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)

        # Open button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.open_btn = QPushButton("Open Problem")
        self.open_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Bold))
        self.open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 7px 18px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.open_btn.clicked.connect(self.on_open_clicked)
        btn_layout.addWidget(self.open_btn)
        layout.addLayout(btn_layout)

        self.apply_theme(self.current_theme)
        self.populate_list(PROBLEMS_DATA)

    def populate_list(self, problems):
        self.list_widget.clear()
        for p in problems:
            item = QListWidgetItem(p["title"])
            item.setData(Qt.ItemDataRole.UserRole, p)
            self.list_widget.addItem(item)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def filter_problems(self, text):
        query = text.strip().lower()
        filtered = [p for p in PROBLEMS_DATA if query in p["title"].lower()]
        self.populate_list(filtered)

    def on_item_double_clicked(self, item):
        problem = item.data(Qt.ItemDataRole.UserRole)
        self.problem_selected.emit(problem)
        self.accept()

    def on_open_clicked(self):
        item = self.list_widget.currentItem()
        if item:
            problem = item.data(Qt.ItemDataRole.UserRole)
            self.problem_selected.emit(problem)
            self.accept()

    def apply_theme(self, theme):
        self.header_label.setStyleSheet(f"color: {theme['brand_color']};")
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['window_bg']};
                color: {theme['brand_color']};
            }}
            QLineEdit {{
                background-color: {theme['table_bg']};
                color: {theme['table_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 6px 10px;
            }}
            QListWidget {{
                background-color: {theme['table_bg']};
                color: {theme['table_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 6px;
            }}
            QListWidget::item {{
                padding: 8px 10px;
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: #2563eb;
                color: #ffffff;
            }}
        """)
