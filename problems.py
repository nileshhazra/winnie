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
        "examples": (
            "max_value([4, 7, 2, 8, 10, 9]) # -> 10\n"
            "max_value([10, 5, 40, 40.3])   # -> 40.3\n"
            "max_value([-5, -2, -1, -11])   # -> -1"
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
    },
    {
        "id": "longest_word",
        "title": "2. longest word",
        "raw_title": "longest word",
        "description": (
            "Write a function, longest_word, that takes in a sentence string as an argument. "
            "The function should return the longest word in the sentence. "
            "If there is a tie, return the word that occurs later in the sentence.\n\n"
            "You can assume that the sentence is non-empty."
        ),
        "examples": (
            'longest_word("the quick brown fox jumps") # -> "jumps"\n'
            'longest_word("where there is a will there is a way") # -> "there"\n'
            'longest_word("hello world") # -> "world"'
        ),
        "starter_code": "def longest_word(sentence):\n  pass # todo\n",
        "solution_code": (
            "def longest_word(sentence):\n"
            '    words = sentence.split(" ")\n'
            '    longest = ""\n'
            "    for word in words:\n"
            "        if len(word) >= len(longest):\n"
            "            longest = word\n"
            "    return longest\n\n"
            "# Example test cases:\n"
            'print(longest_word("the quick brown fox jumps")) # -> "jumps"\n'
            'print(longest_word("where there is a will there is a way")) # -> "there"\n'
            'print(longest_word("hello world")) # -> "world"\n'
        ),
    },
    {
        "id": "all_even",
        "title": "3. all even",
        "raw_title": "all even",
        "description": (
            "Write a function, all_even, that takes in a list of numbers as an argument. "
            "The function should return a boolean indicating whether or not every element of the list is an even number.\n\n"
            "You can assume that the list is non-empty."
        ),
        "examples": (
            "all_even([2, 4, 6, 8]) # -> True\n"
            "all_even([2, 3, 4, 6]) # -> False\n"
            "all_even([12])         # -> True"
        ),
        "starter_code": "def all_even(nums):\n  pass # todo\n",
        "solution_code": (
            "def all_even(nums):\n"
            "    for num in nums:\n"
            "        if num % 2 != 0:\n"
            "            return False\n"
            "    return True\n\n"
            "# Example test cases:\n"
            "print(all_even([2, 4, 6, 8])) # -> True\n"
            "print(all_even([2, 3, 4, 6])) # -> False\n"
            "print(all_even([12]))         # -> True\n"
        ),
    },
    {
        "id": "is_prime",
        "title": "4. is prime",
        "raw_title": "is prime",
        "description": (
            "Write a function, is_prime, that takes in a number as an argument. "
            "The function should return a boolean indicating whether or not the given number is prime.\n\n"
            "A prime number is a number that is only divisible by two distinct numbers: 1 and itself.\n\n"
            "For example, 7 is a prime because it is only divisible by 1 and 7. "
            "For example, 6 is not a prime because it is divisible by 1, 2, 3, and 6.\n\n"
            "You can assume that the input number is a positive integer."
        ),
        "examples": (
            "is_prime(2)  # -> True\n"
            "is_prime(7)  # -> True\n"
            "is_prime(4)  # -> False\n"
            "is_prime(1)  # -> False\n"
            "is_prime(25) # -> False"
        ),
        "starter_code": "def is_prime(n):\n  pass # todo\n",
        "solution_code": (
            "from math import sqrt, floor\n\n"
            "def is_prime(n):\n"
            "    if n < 2:\n"
            "        return False\n"
            "    for i in range(2, floor(sqrt(n)) + 1):\n"
            "        if n % i == 0:\n"
            "            return False\n"
            "    return True\n\n"
            "# Example test cases:\n"
            "print(is_prime(2))  # -> True\n"
            "print(is_prime(7))  # -> True\n"
            "print(is_prime(4))  # -> False\n"
            "print(is_prime(1))  # -> False\n"
            "print(is_prime(25)) # -> False\n"
        ),
    },
    {
        "id": "fizz_buzz",
        "title": "5. fizz buzz",
        "raw_title": "fizz buzz",
        "description": (
            "Write a function, fizz_buzz, that takes in a number n as an argument. "
            "The function should return a list containing numbers from 1 to n, replacing certain numbers according to the following rules:\n\n"
            "• if the number is divisible by 3, make the element \"fizz\"\n"
            "• if the number is divisible by 5, make the element \"buzz\"\n"
            "• if the number is divisible by 3 and 5, make the element \"fizzbuzz\""
        ),
        "examples": (
            "fizz_buzz(11)\n"
            "# -> [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11]\n\n"
            "fizz_buzz(16)\n"
            "# -> [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11, 'fizz', 13, 14, 'fizzbuzz', 16]"
        ),
        "starter_code": "def fizz_buzz(n):\n  pass # todo\n",
        "solution_code": (
            "def fizz_buzz(n):\n"
            "    result = []\n"
            "    for i in range(1, n + 1):\n"
            "        if i % 3 == 0 and i % 5 == 0:\n"
            "            result.append(\"fizzbuzz\")\n"
            "        elif i % 3 == 0:\n"
            "            result.append(\"fizz\")\n"
            "        elif i % 5 == 0:\n"
            "            result.append(\"buzz\")\n"
            "        else:\n"
            "            result.append(i)\n"
            "    return result\n\n"
            "# Example test cases:\n"
            "print(fizz_buzz(11))\n"
            "print(fizz_buzz(16))\n"
        ),
    },
    {
        "id": "pairs",
        "title": "6. pairs",
        "raw_title": "pairs",
        "description": (
            "Write a function, pairs, that takes in a list as an argument. "
            "The function should return a list containing all unique pairs of elements.\n\n"
            "You may return the pairs in any order and the order of elements within a single pair does not matter.\n\n"
            "You can assume that the input list contains unique elements."
        ),
        "examples": (
            "pairs([\"a\", \"b\", \"c\"])\n"
            "# -> [['a', 'b'], ['a', 'c'], ['b', 'c']]\n\n"
            "pairs([\"red\", \"silver\", \"green\", \"blue\"])\n"
            "# -> [['red', 'silver'], ['red', 'green'], ['red', 'blue'], ['silver', 'green'], ['silver', 'blue'], ['green', 'blue']]"
        ),
        "starter_code": "def pairs(elements):\n  pass # todo\n",
        "solution_code": (
            "def pairs(elements):\n"
            "    result = []\n"
            "    for i in range(0, len(elements)):\n"
            "        for j in range(i + 1, len(elements)):\n"
            "            pair = [elements[i], elements[j]]\n"
            "            result.append(pair)\n"
            "    return result\n\n"
            "# Example test cases:\n"
            "print(pairs([\"a\", \"b\", \"c\"]))\n"
            "print(pairs([\"red\", \"silver\", \"green\", \"blue\"]))\n"
        ),
    },
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

        # Badge Pill
        self.badge_label = QLabel("Practice Problem")
        self.badge_label.setFont(QFont("SF Pro Text", 10, QFont.Weight.Bold))
        self.badge_label.setStyleSheet("""
            background-color: #0284c7;
            color: #ffffff;
            border-radius: 6px;
            padding: 4px 10px;
            font-weight: 600;
        """)
        self.container_layout.addWidget(self.badge_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Description
        self.desc_label = QLabel()
        self.desc_label.setFont(QFont("SF Pro Text", 12))
        self.desc_label.setWordWrap(True)
        self.container_layout.addWidget(self.desc_label)

        # Examples Header
        self.examples_header = QLabel("Example Test Cases")
        self.examples_header.setFont(QFont("SF Pro Display", 12, QFont.Weight.Bold))
        self.container_layout.addWidget(self.examples_header)

        # Examples Box (Syntax-highlighted code block)
        self.examples_box = QPlainTextEdit()
        self.examples_box.setFont(QFont("Dank Mono", 12))
        self.examples_box.setReadOnly(True)
        self.examples_highlighter = PythonHighlighter(self.examples_box.document(), theme=self.current_theme)
        self.container_layout.addWidget(self.examples_box)

        self.container_layout.addStretch()
        layout.addWidget(scroll)

        self.apply_theme(self.current_theme)

    def set_problem(self, problem):
        self.title_label.setText(problem.get("title", ""))
        self.desc_label.setText(problem.get("description", ""))
        examples = problem.get("examples", "")
        self.examples_box.setPlainText(examples)
        line_count = len(examples.strip().splitlines()) if examples else 2
        target_height = max(60, min(180, line_count * 22 + 20))
        self.examples_box.setFixedHeight(target_height)

    def apply_font_size(self, size: int):
        ex_font = self.examples_box.font()
        ex_font.setPointSize(size)
        self.examples_box.setFont(ex_font)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.title_label.setStyleSheet(f"color: {theme['brand_color']}; font-weight: bold;")
        self.desc_label.setStyleSheet(f"color: {theme['table_text']}; font-size: 13px;")
        self.examples_header.setStyleSheet(f"color: {theme['brand_color']}; font-weight: bold; margin-top: 6px;")
        self.examples_highlighter.apply_theme(theme)
        self.examples_box.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {theme['console_bg']};
                color: {theme['console_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 8px;
            }}
        """)


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

    def apply_font_size(self, size: int):
        sol_font = self.solution_view.font()
        sol_font.setPointSize(size)
        self.solution_view.setFont(sol_font)

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
