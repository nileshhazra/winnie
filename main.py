import sys
import tempfile
import os
import json
import shutil
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSplitter,
    QLabel,
    QSizePolicy,
    QFileDialog,
    QMessageBox,
    QTabWidget,
)
from PySide6.QtGui import QFont, QIcon, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QProcess, QSize

from editor import CodeEditor
from console import InteractiveConsole
from variables_view import VariablesView
from assistant import AssistantView, parse_traceback
from package_manager import PackageManagerDialog
from problems import ProblemsListDialog, ProblemDescriptionWidget, ProblemSolutionWidget
from theme import DARK_THEME, LIGHT_THEME
from icons import (
    render_svg_icon,
    RUN_SVG,
    STOP_SVG,
    STEP_SVG,
    PACKAGE_SVG,
    PROBLEMS_SVG,
    CLEAR_SVG,
    MOON_SVG,
    SUN_SVG,
)


def get_resource_path(relative_path):
    """Finds resource path whether running from source or inside a frozen .app bundle."""
    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        res = os.path.join(base_path, relative_path)
        if os.path.exists(res):
            return res
        res_app = os.path.join(os.path.dirname(sys.executable), "..", "Resources", relative_path)
        if os.path.exists(res_app):
            return res_app
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def get_python_interpreter():
    """Returns the Python interpreter to execute user code."""
    if not getattr(sys, "frozen", False):
        return sys.executable
    for candidate in ["/opt/homebrew/bin/python3", "/usr/local/bin/python3", "/usr/bin/python3"]:
        if os.path.exists(candidate):
            return candidate
    which_py = shutil.which("python3")
    return which_py if which_py else "python3"


class WinnieIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Winnie — Python IDE")
        self.resize(1100, 700)

        self.current_theme = DARK_THEME

        # Central Widget & Main Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 8, 12, 12)
        main_layout.setSpacing(8)
        self.setCentralWidget(central_widget)

        # 1. Custom Top Action Bar with Modern Buttons
        top_bar = self.create_action_bar()
        main_layout.addWidget(top_bar, 0)  # Do not allow top bar to expand vertically!

        # 2. Editor & Console (Left)
        self.editor = CodeEditor(theme=self.current_theme)
        self.editor.setPlaceholderText("# Type your Python code here and click Run...")
        self.editor.setPlainText(
            'total = 0\n'
            'items = [10, 20, 30]\n\n'
            'for x in items:\n'
            '    total += x\n'
            '    print(f"Added {x}, running total is {total}")\n\n'
            'print("All done!")'
        )

        # File Management State
        self.current_file_path = None
        self.is_modified = False
        self.editor.textChanged.connect(self.on_text_changed)

        self.console = InteractiveConsole(theme=self.current_theme)
        self.console.input_submitted.connect(self.send_stdin)

        self.left_splitter = QSplitter(Qt.Orientation.Vertical)
        self.left_splitter.addWidget(self.editor)
        self.left_splitter.addWidget(self.console)
        self.left_splitter.setStretchFactor(0, 7)
        self.left_splitter.setStretchFactor(1, 3)

        # 3. Right-Side Inspector Tabs (Variables & Error Assistant)
        self.variables_view = VariablesView(theme=self.current_theme)
        self.assistant_view = AssistantView(theme=self.current_theme)
        self.assistant_view.jump_to_line_requested.connect(self.jump_to_line)

        # Practice Problems views & state
        self.active_problem_title = None
        self.is_problem_mode = False
        self.problem_desc_widget = ProblemDescriptionWidget(theme=self.current_theme)
        self.problem_sol_widget = ProblemSolutionWidget(theme=self.current_theme)
        self.problem_sol_widget.copy_to_editor_requested.connect(self.load_solution_to_editor)

        # Tab Corner Controls (Toggle Variables / Problem + Exit)
        self.corner_widget = QWidget()
        corner_layout = QHBoxLayout(self.corner_widget)
        corner_layout.setContentsMargins(0, 0, 6, 0)
        corner_layout.setSpacing(4)

        self.tab_toggle_btn = QPushButton("✦ Variables")
        self.tab_toggle_btn.setFont(QFont("SF Pro Text", 11))
        self.tab_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tab_toggle_btn.setToolTip("Switch to Variables Inspector")
        self.tab_toggle_btn.clicked.connect(self.toggle_problem_variables_tab)
        corner_layout.addWidget(self.tab_toggle_btn)

        self.exit_problem_btn = QPushButton("✕")
        self.exit_problem_btn.setFont(QFont("SF Pro Text", 11))
        self.exit_problem_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit_problem_btn.setToolTip("Exit Problem Mode")
        self.exit_problem_btn.clicked.connect(self.exit_problem_mode)
        corner_layout.addWidget(self.exit_problem_btn)

        self.right_tabs = QTabWidget()
        self.right_tabs.tabBar().setElideMode(Qt.TextElideMode.ElideNone)
        self.right_tabs.setMinimumWidth(260)
        self.right_tabs.addTab(self.variables_view, "Variables")
        self.right_tabs.addTab(self.assistant_view, "Assistant")
        self.right_tabs.currentChanged.connect(self.on_right_tab_changed)

        # 4. Master Horizontal Splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.left_splitter)
        self.main_splitter.addWidget(self.right_tabs)
        self.main_splitter.setStretchFactor(0, 7)
        self.main_splitter.setStretchFactor(1, 3)
        self.main_splitter.setSizes([720, 340])
        main_layout.addWidget(self.main_splitter, 1)  # Takes 100% of remaining vertical space!

        # Background Process Runner & Stderr Tracking
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.handle_finished)
        self.stderr_buffer = []

        # Debugger Stepping State
        self.is_stepping = False
        self.is_paused_at_step = False

        # 6. Keyboard Shortcuts:
        # Cmd + J: Toggle Bottom Terminal
        self.shortcut_terminal = QShortcut(QKeySequence("Ctrl+J"), self)
        self.shortcut_terminal.activated.connect(self.toggle_terminal)

        # Cmd + L: Toggle Right Variables Panel
        self.shortcut_variables = QShortcut(QKeySequence("Ctrl+L"), self)
        self.shortcut_variables.activated.connect(self.toggle_variables)

        # F7 / Cmd + Alt + S: Step Execution (Thonny style)
        self.shortcut_step1 = QShortcut(QKeySequence(Qt.Key.Key_F7), self)
        self.shortcut_step1.activated.connect(self.step_code)
        self.shortcut_step2 = QShortcut(QKeySequence("Ctrl+Alt+S"), self)
        self.shortcut_step2.activated.connect(self.step_code)

        # Cmd + + / Cmd + =: Zoom in font
        self.font_size = 13
        self.apply_font_size(self.font_size)
        self.shortcut_zoom_in1 = QShortcut(QKeySequence("Ctrl++"), self)
        self.shortcut_zoom_in1.activated.connect(self.zoom_in)
        self.shortcut_zoom_in2 = QShortcut(QKeySequence("Ctrl+="), self)
        self.shortcut_zoom_in2.activated.connect(self.zoom_in)

        # Cmd + -: Zoom out font
        self.shortcut_zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        self.shortcut_zoom_out.activated.connect(self.zoom_out)

        # Cmd + 0: Reset font zoom
        self.shortcut_zoom_reset = QShortcut(QKeySequence("Ctrl+0"), self)
        self.shortcut_zoom_reset.activated.connect(self.reset_zoom)

        # Cmd + Return / Cmd + Enter: Run Code
        self.shortcut_run1 = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut_run1.activated.connect(self.run_code)
        self.shortcut_run2 = QShortcut(QKeySequence("Ctrl+Enter"), self)
        self.shortcut_run2.activated.connect(self.run_code)

        # Cmd + . / Cmd + Esc: Stop Program (Classic Mac halt shortcut)
        self.shortcut_stop1 = QShortcut(QKeySequence("Ctrl+."), self)
        self.shortcut_stop1.activated.connect(self.stop_code)
        self.shortcut_stop2 = QShortcut(QKeySequence("Ctrl+Escape"), self)
        self.shortcut_stop2.activated.connect(self.stop_code)

        # Cmd + K: Clear Console & Variables (Standard Mac terminal clear)
        self.shortcut_clear = QShortcut(QKeySequence("Ctrl+K"), self)
        self.shortcut_clear.activated.connect(self.clear_all)

        # Cmd + Shift + T / Cmd + T: Toggle Dark/Light Theme
        self.shortcut_theme1 = QShortcut(QKeySequence("Ctrl+Shift+T"), self)
        self.shortcut_theme1.activated.connect(self.toggle_theme)
        self.shortcut_theme2 = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_theme2.activated.connect(self.toggle_theme)

        # Native macOS Menu Bar
        self.create_menu_bar()

        # Apply initial theme styling
        self.apply_theme(self.current_theme)
        self.update_window_title()

    # ==========================================
    # File Management Methods
    # ==========================================
    def create_menu_bar(self):
        """Creates the native macOS File menu bar."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_action = file_menu.addAction("New File")
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.new_file)

        open_action = file_menu.addAction("Open File...")
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)

        file_menu.addSeparator()

        save_action = file_menu.addAction("Save")
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)

        save_as_action = file_menu.addAction("Save As...")
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_file_as)

        # Tools Menu
        tools_menu = menubar.addMenu("Tools")
        pkg_action = tools_menu.addAction("Manage Packages...")
        pkg_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        pkg_action.triggered.connect(self.open_package_manager)

        problems_action = tools_menu.addAction("Practice Problems...")
        problems_action.setShortcut(QKeySequence("Ctrl+Shift+R"))
        problems_action.triggered.connect(self.open_problems_dialog)

    def open_package_manager(self):
        """Opens the graphical pip package manager dialog."""
        python_bin = get_python_interpreter()
        dlg = PackageManagerDialog(self, python_executable=python_bin, theme=self.current_theme)
        dlg.exec()

    def open_problems_dialog(self):
        """Opens the practice problems selection dialog."""
        dlg = ProblemsListDialog(self, theme=self.current_theme)
        dlg.problem_selected.connect(self.load_problem)
        dlg.exec()

    def load_problem(self, problem: dict):
        """Loads a practice problem into the editor and sets right panel to Description/Solution."""
        if not self.maybe_save():
            return

        starter_code = problem.get("starter_code", "")
        self.editor.setPlainText(starter_code)
        self.current_file_path = None
        self.is_modified = False
        self.active_problem_title = problem.get("raw_title", problem.get("title"))
        self.update_window_title()

        self.problem_desc_widget.set_problem(problem)
        self.problem_sol_widget.set_problem(problem)
        self.problem_desc_widget.apply_font_size(self.font_size)
        self.problem_sol_widget.apply_font_size(self.font_size)

        self.is_problem_mode = True
        self.right_tabs.clear()
        self.right_tabs.addTab(self.problem_desc_widget, "Description")
        self.right_tabs.addTab(self.problem_sol_widget, "Solution")
        self.right_tabs.addTab(self.variables_view, "Variables")
        self.right_tabs.addTab(self.assistant_view, "Assistant")
        self.right_tabs.setCornerWidget(self.corner_widget, Qt.Corner.TopRightCorner)
        self.right_tabs.setCurrentWidget(self.problem_desc_widget)
        self.tab_toggle_btn.setText("✦ Variables")
        self.tab_toggle_btn.setToolTip("Switch to Variables Inspector")

        if not self.right_tabs.isVisible():
            self.right_tabs.show()

        # Ensure right panel has ample room for all 4 tabs + corner controls
        sizes = self.main_splitter.sizes()
        if len(sizes) == 2 and sizes[1] < 420:
            total = sum(sizes) if sum(sizes) > 0 else 1060
            self.main_splitter.setSizes([max(500, total - 420), 420])

    def exit_problem_mode(self):
        """Exits problem mode and restores the standard Variables & Assistant tabs."""
        self.is_problem_mode = False
        self.active_problem_title = None
        self.right_tabs.setCornerWidget(None)
        self.right_tabs.clear()
        self.right_tabs.addTab(self.variables_view, "Variables")
        self.right_tabs.addTab(self.assistant_view, "Assistant")
        self.update_window_title()

    def on_right_tab_changed(self, index: int):
        """Updates the corner toggle button label based on which tab is active."""
        if not self.is_problem_mode:
            return
        current = self.right_tabs.currentWidget()
        if current in (self.problem_desc_widget, self.problem_sol_widget):
            self.tab_toggle_btn.setText("✦ Variables")
            self.tab_toggle_btn.setToolTip("Switch to Variables Inspector")
        else:
            self.tab_toggle_btn.setText("📝 Problem")
            self.tab_toggle_btn.setToolTip("Switch to Problem Description")

    def toggle_problem_variables_tab(self):
        """One-click toggle between Problem View and Variables Inspector."""
        if not self.is_problem_mode:
            return
        current = self.right_tabs.currentWidget()
        if current in (self.problem_desc_widget, self.problem_sol_widget):
            self.right_tabs.setCurrentWidget(self.variables_view)
        else:
            self.right_tabs.setCurrentWidget(self.problem_desc_widget)

    def load_solution_to_editor(self, solution_code: str):
        """Loads reference solution code into editor upon request."""
        self.editor.setPlainText(solution_code)
        self.is_modified = True
        self.update_window_title()
        self.console.append_output("\n[Solution copied to editor — click Step or Variables tab to inspect live]\n")

    def on_text_changed(self):
        """Called whenever code in the editor is modified."""
        if not self.is_modified:
            self.is_modified = True
            self.update_window_title()

    def update_window_title(self):
        """Updates the macOS window title and native unsaved indicator."""
        if self.active_problem_title:
            filename = self.active_problem_title
        else:
            filename = os.path.basename(self.current_file_path) if self.current_file_path else "Untitled"
        self.setWindowModified(self.is_modified)
        mod_marker = " ●" if self.is_modified else ""
        self.setWindowTitle(f"{filename}{mod_marker} — Winnie")

    def maybe_save(self) -> bool:
        """Prompts to save if there are unsaved changes. Returns False if cancelled."""
        if not self.is_modified:
            return True

        filename = self.active_problem_title if self.active_problem_title else (os.path.basename(self.current_file_path) if self.current_file_path else "Untitled")
        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            f"Do you want to save changes to '{filename}'?",
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save
        )

        if reply == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif reply == QMessageBox.StandardButton.Cancel:
            return False
        return True  # Discard changes

    def new_file(self):
        """Creates a new empty file (Cmd + N)."""
        if not self.maybe_save():
            return
        if self.is_problem_mode:
            self.exit_problem_mode()
        self.current_file_path = None
        self.editor.setPlainText("")
        self.is_modified = False
        self.update_window_title()

    def open_file(self):
        """Opens an existing Python file from disk (Cmd + O)."""
        if not self.maybe_save():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Python File", "", "Python Files (*.py);;All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if self.is_problem_mode:
                self.exit_problem_mode()
            self.current_file_path = path
            self.editor.setPlainText(content)
            self.is_modified = False
            self.update_window_title()
        except Exception as e:
            QMessageBox.critical(self, "Error Opening File", f"Could not read file:\n{e}")

    def save_file(self) -> bool:
        """Saves current file to disk (Cmd + S)."""
        if not self.current_file_path:
            return self.save_file_as()
        try:
            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.is_modified = False
            self.update_window_title()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error Saving File", f"Could not save file:\n{e}")
            return False

    def save_file_as(self) -> bool:
        """Prompts for a filename and saves (Cmd + Shift + S)."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Python File", "", "Python Files (*.py);;All Files (*)"
        )
        if not path:
            return False
        if not path.endswith(".py"):
            path += ".py"
        self.current_file_path = path
        return self.save_file()

    def closeEvent(self, event):
        """Asks to save unsaved changes before exiting the app."""
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    def zoom_in(self):
        """Increases font size for editor, console, and variables (Cmd + +)."""
        if self.font_size < 32:
            self.apply_font_size(self.font_size + 1)

    def zoom_out(self):
        """Decreases font size for editor, console, and variables (Cmd + -)."""
        if self.font_size > 9:
            self.apply_font_size(self.font_size - 1)

    def reset_zoom(self):
        """Resets font size back to default 13pt (Cmd + 0)."""
        self.apply_font_size(13)

    def apply_font_size(self, size: int):
        self.font_size = size

        # 1. Update Code Editor font & line number gutter width
        editor_font = self.editor.font()
        editor_font.setPointSize(size)
        self.editor.setFont(editor_font)
        self.editor.update_line_number_area_width(0)
        self.editor.line_number_area.update()

        # 2. Update Console font
        console_font = self.console.font()
        console_font.setPointSize(size)
        self.console.setFont(console_font)

        # 3. Update Variables Table font
        var_font = self.variables_view.table.font()
        var_font.setPointSize(max(9, size - 1))
        self.variables_view.table.setFont(var_font)
        self.variables_view.table.resizeRowsToContents()

        # 4. Update Problem Views fonts (Solution code & Description examples)
        self.problem_sol_widget.apply_font_size(size)
        self.problem_desc_widget.apply_font_size(size)

    def toggle_terminal(self):
        """Toggles the bottom terminal / console visibility (Cmd + J)."""
        if self.console.isVisible():
            self.console.hide()
        else:
            self.console.show()
            sizes = self.left_splitter.sizes()
            # If collapsed to 0, restore default proportions
            if len(sizes) > 1 and sizes[1] == 0:
                total = sum(sizes) if sum(sizes) > 0 else 600
                self.left_splitter.setSizes([int(total * 0.7), int(total * 0.3)])

    def toggle_variables(self):
        """Toggles the right inspector panel visibility (Cmd + L)."""
        if self.right_tabs.isVisible():
            self.right_tabs.hide()
        else:
            self.right_tabs.show()
            sizes = self.main_splitter.sizes()
            # If collapsed to 0, restore default proportions
            if len(sizes) > 1 and sizes[1] == 0:
                total = sum(sizes) if sum(sizes) > 0 else 900
                self.main_splitter.setSizes([int(total * 0.75), int(total * 0.25)])

    def jump_to_line(self, line_num: int):
        """Scrolls editor to line and highlights it."""
        self.editor.set_debug_line(line_num)

    def create_action_bar(self):
        """Creates a modern top bar with sleek monochromatic icons."""
        bar = QWidget()
        bar.setFixedHeight(44)
        bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 1. Clean Minimal Brand Name
        self.brand = QLabel("Winnie")
        self.brand.setFont(QFont("SF Pro Display", 16, QFont.Weight.Bold))
        layout.addWidget(self.brand)

        # 2. ▶ Run Button (Modern Emerald Pill with Monochromatic SVG Icon)
        self.run_btn = QPushButton(" Run")
        self.run_btn.setToolTip("Run Code (⌘⏎)")
        self.run_btn.setIcon(render_svg_icon(RUN_SVG, size=12, color="#ffffff"))
        self.run_btn.setIconSize(QSize(12, 12))
        self.run_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Bold))
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 7px 16px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
            QPushButton:disabled {
                background-color: #27272a;
                color: #52525b;
            }
        """)
        self.run_btn.clicked.connect(self.run_code)
        layout.addWidget(self.run_btn)

        # 3. 🐾 Step Button (Warm Amber Pill for Line-by-Line Debugging)
        self.step_btn = QPushButton(" Step")
        self.step_btn.setToolTip("Step Line-by-Line (F7 or ⌘⌥S)")
        self.step_btn.setIcon(render_svg_icon(STEP_SVG, size=13, color="#ffffff"))
        self.step_btn.setIconSize(QSize(13, 13))
        self.step_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Bold))
        self.step_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.step_btn.setStyleSheet("""
            QPushButton {
                background-color: #d97706;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 7px 16px;
            }
            QPushButton:hover {
                background-color: #b45309;
            }
            QPushButton:pressed {
                background-color: #92400e;
            }
            QPushButton:disabled {
                background-color: #27272a;
                color: #52525b;
            }
        """)
        self.step_btn.clicked.connect(self.step_code)
        layout.addWidget(self.step_btn)

        # 4. ⏹ Stop Button (Modern Crimson Pill with Monochromatic SVG Icon)
        self.stop_btn = QPushButton(" Stop")
        self.stop_btn.setToolTip("Stop Program (⌘. or ⎋)")
        self.stop_btn.setIcon(render_svg_icon(STOP_SVG, size=11, color="#ffffff"))
        self.stop_btn.setIconSize(QSize(11, 11))
        self.stop_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Bold))
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 7px 16px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
            QPushButton:pressed {
                background-color: #b91c1c;
            }
            QPushButton:disabled {
                background-color: #27272a;
                color: #52525b;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_code)
        layout.addWidget(self.stop_btn)

        # 5. Clear Button (Monochromatic Trash SVG Icon)
        self.clear_btn = QPushButton(" Clear")
        self.clear_btn.setToolTip("Clear Console & Variables (⌘K)")
        self.clear_btn.setFont(QFont("SF Pro Text", 12))
        self.clear_btn.setIconSize(QSize(14, 14))
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn)

        # 6. Packages Button (Manage pip packages)
        self.packages_btn = QPushButton(" Packages")
        self.packages_btn.setToolTip("Manage Python Packages (⌘⇧P)")
        self.packages_btn.setFont(QFont("SF Pro Text", 12))
        self.packages_btn.setIconSize(QSize(14, 14))
        self.packages_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.packages_btn.clicked.connect(self.open_package_manager)
        layout.addWidget(self.packages_btn)

        # 7. Problems Button (Practice Problems)
        self.problems_btn = QPushButton(" Problems")
        self.problems_btn.setToolTip("Explore Practice Problems (⌘⇧R)")
        self.problems_btn.setFont(QFont("SF Pro Text", 12))
        self.problems_btn.setIconSize(QSize(14, 14))
        self.problems_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.problems_btn.clicked.connect(self.open_problems_dialog)
        layout.addWidget(self.problems_btn)

        layout.addStretch()  # Spacer

        # 5. Monochromatic Theme Toggle Button (Moon / Sun SVG)
        self.theme_btn = QPushButton()
        self.theme_btn.setToolTip("Toggle Theme (⌘T or ⌘⇧T)")
        self.theme_btn.setFont(QFont("SF Pro Text", 12))
        self.theme_btn.setIconSize(QSize(15, 15))
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)

        return bar

    def toggle_theme(self):
        """Switches between Dark and Light mode."""
        if self.current_theme["name"] == "dark":
            self.apply_theme(LIGHT_THEME)
        else:
            self.apply_theme(DARK_THEME)

    def apply_theme(self, theme):
        self.current_theme = theme

        # Main window and splitters
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme['window_bg']};
            }}
            QSplitter::handle {{
                background-color: {theme['border_color']};
            }}
            QSplitter::handle:hover {{
                background-color: #3b82f6;
            }}
        """)

        # Brand styling
        self.brand.setStyleSheet(f"color: {theme['brand_color']}; margin-right: 12px;")

        # Clear button styling & icon
        self.clear_btn.setIcon(render_svg_icon(CLEAR_SVG, size=14, color=theme["btn_clear_text"]))
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)

        # Packages button styling & icon
        self.packages_btn.setIcon(render_svg_icon(PACKAGE_SVG, size=13, color=theme["btn_clear_text"]))
        self.packages_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)

        # Problems button styling & icon
        self.problems_btn.setIcon(render_svg_icon(PROBLEMS_SVG, size=13, color=theme["btn_clear_text"]))
        self.problems_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)

        # Tab corner controls (Toggle Variables / Problem + Exit button)
        self.tab_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 5px;
                padding: 3px 8px;
                font-size: 11px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)

        self.exit_problem_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 5px;
                padding: 3px 7px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ef4444;
                color: #ffffff;
                border-color: #dc2626;
            }}
        """)

        # Theme toggle button styling & monochromatic icon
        if theme["name"] == "dark":
            self.theme_btn.setText(" Light")
            self.theme_btn.setIcon(render_svg_icon(SUN_SVG, size=15, color=theme["btn_clear_text"]))
        else:
            self.theme_btn.setText(" Dark")
            self.theme_btn.setIcon(render_svg_icon(MOON_SVG, size=15, color=theme["btn_clear_text"]))

        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)

        # Tab styling
        self.right_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {theme['border_color']};
                background-color: {theme['table_bg']};
                border-radius: 8px;
            }}
            QTabBar {{
                qproperty-drawBase: 0;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {theme['table_header_text']};
                padding: 6px 12px;
                margin-right: 4px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                color: {theme['brand_color']};
                border-bottom: 2px solid #10b981;
            }}
            QTabBar::tab:hover {{
                color: {theme['brand_color']};
            }}
        """)

        # Propagate to child widgets
        self.editor.apply_theme(theme)
        self.console.apply_theme(theme)
        self.variables_view.apply_theme(theme)
        self.assistant_view.apply_theme(theme)
        self.problem_desc_widget.apply_theme(theme)
        self.problem_sol_widget.apply_theme(theme)

    def clear_all(self):
        self.console.clear()
        self.variables_view.clear()
        self.assistant_view.show_success_state()
        self.stderr_buffer = []

    def run_code(self):
        # If currently paused in step mode, clicking Run resumes normal full-speed execution!
        if self.process.state() != QProcess.ProcessState.NotRunning:
            if self.is_stepping and self.is_paused_at_step:
                self.process.write(b"CONTINUE\n")
                self.is_stepping = False
                self.is_paused_at_step = False
                self.editor.clear_debug_line()
                self.run_btn.setEnabled(False)
                self.step_btn.setEnabled(False)
            return

        code = self.editor.toPlainText().strip()
        if not code:
            return

        # Auto-reveal terminal if it was hidden
        if not self.console.isVisible():
            self.toggle_terminal()

        # If working on a saved file, auto-save before running
        if self.current_file_path:
            self.save_file()
            target_path = self.current_file_path
        else:
            self.temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False)
            self.temp_file.write(code)
            self.temp_file.close()
            target_path = self.temp_file.name

        self.editor.clear_debug_line()
        self.variables_view.clear()
        self.stderr_buffer = []
        filename_display = os.path.basename(target_path)
        self.console.append_output(f">>> Running {filename_display}...\n")
        self.console.set_running_state(True)
        self.is_stepping = False
        self.is_paused_at_step = False
        self.run_btn.setEnabled(False)
        self.step_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        runner_path = get_resource_path("runner.py")
        python_bin = get_python_interpreter()
        self.process.start(python_bin, ["-u", runner_path, target_path])

    def step_code(self):
        """Advances one line or launches debugger in step mode (F7 or ⌘⌥S)."""
        # If already paused at a step, tell runner to execute the next line!
        if self.process.state() != QProcess.ProcessState.NotRunning:
            if self.is_paused_at_step:
                self.is_paused_at_step = False
                self.process.write(b"STEP\n")
            return

        # Start execution in step mode
        code = self.editor.toPlainText().strip()
        if not code:
            return

        if not self.console.isVisible():
            self.toggle_terminal()

        if self.current_file_path:
            self.save_file()
            target_path = self.current_file_path
        else:
            self.temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False)
            self.temp_file.write(code)
            self.temp_file.close()
            target_path = self.temp_file.name

        self.editor.clear_debug_line()
        self.variables_view.clear()
        self.stderr_buffer = []
        filename_display = os.path.basename(target_path)
        self.console.append_output(f">>> Debugging {filename_display} (Step mode)...\n")
        self.console.set_running_state(True)
        self.is_stepping = True
        self.is_paused_at_step = False
        self.run_btn.setEnabled(True)  # Allow switching to Run at any time
        self.step_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)

        # Auto-switch right tabs to Variables view when stepping
        if self.right_tabs.indexOf(self.variables_view) != -1:
            self.right_tabs.setCurrentWidget(self.variables_view)
        if not self.right_tabs.isVisible():
            self.right_tabs.show()

        runner_path = get_resource_path("runner.py")
        python_bin = get_python_interpreter()
        self.process.start(python_bin, ["-u", runner_path, "--step", target_path])

    def stop_code(self):
        if self.process.state() != QProcess.ProcessState.NotRunning:
            self.console.append_output("\n⏹ Stopping program...\n")
            if self.is_stepping and self.is_paused_at_step:
                self.process.write(b"STOP\n")
            self.editor.clear_debug_line()
            self.process.terminate()
            if not self.process.waitForFinished(1000):
                self.process.kill()

    def send_stdin(self, text: str):
        if self.process.state() != QProcess.ProcessState.NotRunning:
            self.process.write(text.encode("utf-8"))

    def handle_stdout(self):
        raw_data = self.process.readAllStandardOutput().data().decode("utf-8", errors="replace")

        clean_lines = []
        for line in raw_data.splitlines(keepends=True):
            if "__WINNIE_STEP__:" in line:
                try:
                    _, json_str = line.split("__WINNIE_STEP__:", 1)
                    step_data = json.loads(json_str.strip())
                    line_num = step_data.get("line")
                    vars_list = step_data.get("vars", [])
                    self.editor.set_debug_line(line_num)
                    self.variables_view.update_variables(vars_list)
                    if self.right_tabs.indexOf(self.variables_view) != -1 and self.right_tabs.currentWidget() not in (self.variables_view, self.assistant_view):
                        self.right_tabs.setCurrentWidget(self.variables_view)
                    self.is_paused_at_step = True
                    self.step_btn.setEnabled(True)
                    self.run_btn.setEnabled(True)
                except Exception:
                    pass
            elif "__WINNIE_VARS__:" in line:
                try:
                    _, json_str = line.split("__WINNIE_VARS__:", 1)
                    var_list = json.loads(json_str.strip())
                    self.variables_view.update_variables(var_list)
                except Exception:
                    pass
            else:
                clean_lines.append(line)

        if clean_lines:
            self.console.append_output("".join(clean_lines))

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode("utf-8", errors="replace")
        self.stderr_buffer.append(data)
        self.console.append_output(data)

    def handle_finished(self, exit_code, exit_status):
        self.console.append_output(f"\n[Program finished with exit code {exit_code}]\n")
        self.console.set_running_state(False)
        self.is_stepping = False
        self.is_paused_at_step = False
        self.run_btn.setEnabled(True)
        self.step_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        # Parse stderr for beginner error assistance
        full_stderr = "".join(self.stderr_buffer)
        error_info = parse_traceback(full_stderr)
        if error_info:
            self.assistant_view.show_error(error_info)
            if self.right_tabs.indexOf(self.assistant_view) != -1:
                self.right_tabs.setCurrentWidget(self.assistant_view)
            if error_info.get("line_number"):
                self.editor.set_debug_line(error_info["line_number"])
        elif exit_code == 0:
            self.editor.clear_debug_line()
            self.assistant_view.show_success_state()

        if hasattr(self, "temp_file") and self.temp_file and os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except OSError:
                pass
            self.temp_file = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = WinnieIDE()
    ide.show()
    sys.exit(app.exec())
