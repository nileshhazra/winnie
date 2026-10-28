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
    QTabBar,
)
from PySide6.QtGui import QFont, QIcon, QShortcut, QKeySequence, QPalette, QColor
from PySide6.QtCore import Qt, QProcess, QSize

from editor import CodeEditor
from console import InteractiveConsole
from variables_view import VariablesView
from assistant import AssistantView, parse_traceback
from package_manager import PackageManagerDialog
from problems import ProblemsListDialog, ProblemDescriptionWidget, ProblemSolutionWidget
from about_dialog import AboutDialog
from theme import DARK_THEME, LIGHT_THEME, get_scrollbar_stylesheet
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
    PLUS_SVG,
    CLOSE_SVG,
    INFO_SVG,
)


def setup_macos_app_identity():
    """Sets the macOS process name, bundle display name, and dock title to 'Winnie'."""
    if sys.platform != "darwin":
        return
    try:
        from Foundation import NSProcessInfo, NSBundle
        NSProcessInfo.processInfo().setProcessName_("Winnie")
        bundle = NSBundle.mainBundle()
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info is not None:
            info["CFBundleName"] = "Winnie"
            info["CFBundleDisplayName"] = "Winnie"
    except Exception:
        pass


setup_macos_app_identity()


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


class WinnieCentralWidget(QWidget):
    """Central widget that allows dragging from the top header margin area."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() <= 60:
            wh = self.window().windowHandle()
            if wh and wh.startSystemMove():
                event.accept()
                return
            self._drag_pos = event.globalPosition().toPoint() - self.window().pos()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self._drag_pos is not None:
            win = self.window()
            if win.isMaximized():
                win.showNormal()
            win.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() <= 60:
            win = self.window()
            if win.isMaximized():
                win.showNormal()
            else:
                win.showMaximized()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)


class TopActionBar(QWidget):
    """Top action bar that supports native window dragging and double-click zoom."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            wh = self.window().windowHandle()
            if wh and wh.startSystemMove():
                event.accept()
                return
            self._drag_pos = event.globalPosition().toPoint() - self.window().pos()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self._drag_pos is not None:
            win = self.window()
            if win.isMaximized():
                win.showNormal()
            win.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            win = self.window()
            if win.isMaximized():
                win.showNormal()
            else:
                win.showMaximized()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)


class WinnieIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Winnie — Python IDE")
        self.resize(1100, 700)

        # Set Window / Application Icon
        icon_path = get_resource_path("Winnie.png")
        if not os.path.exists(icon_path):
            icon_path = get_resource_path("Winnie.icns")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.current_theme = DARK_THEME

        # Central Widget & Main Layout
        central_widget = WinnieCentralWidget()
        central_widget.setObjectName("centralWidget")
        main_layout = QVBoxLayout(central_widget)
        top_margin = 8 if sys.platform == "darwin" else 8
        main_layout.setContentsMargins(12, top_margin, 12, 12)
        main_layout.setSpacing(8)
        self.setCentralWidget(central_widget)

        # 1. Custom Top Action Bar with Modern Buttons
        top_bar = self.create_action_bar()
        main_layout.addWidget(top_bar, 0)  # Do not allow top bar to expand vertically!

        # Global IDE font size setting
        self.font_size = 13

        # 2. Multi-Tab Code Editor & Console (Left)
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setObjectName("editorTabs")
        self.editor_tabs.setTabsClosable(False)
        self.editor_tabs.setMovable(True)
        self.editor_tabs.setDocumentMode(True)
        self.editor_tabs.setUsesScrollButtons(True)
        self.editor_tabs.tabBar().setElideMode(Qt.TextElideMode.ElideRight)
        self.editor_tabs.tabCloseRequested.connect(self.close_tab)
        self.editor_tabs.currentChanged.connect(self.on_editor_tab_changed)
        self.editor_tabs.tabBarClicked.connect(self.on_tab_bar_clicked)
        self.editor_tabs.tabBar().tabMoved.connect(self.on_tab_moved)

        # Persistent trailing "+" tab placed inline next to opened files
        self.plus_tab_widget = QWidget()

        self.untitled_counter = 0
        self._fallback_editor = CodeEditor(theme=self.current_theme)

        # File Management State
        self.active_problem_title = None
        self.is_problem_mode = False

        self.console = InteractiveConsole(theme=self.current_theme)
        self.console.input_submitted.connect(self.send_stdin)

        self.left_splitter = QSplitter(Qt.Orientation.Vertical)
        self.left_splitter.addWidget(self.editor_tabs)
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

        # Initial demo tab
        self.untitled_counter += 1
        initial_code = (
            'total = 0\n'
            'items = [10, 20, 30]\n\n'
            'for x in items:\n'
            '    total += x\n'
            '    print(f"Added {x}, running total is {total}")\n\n'
            'print("All done!")'
        )
        self.create_editor_tab(title="Untitled", content=initial_code, file_path=None)

        # Append inline "+" tab immediately next to opened files
        plus_idx = self.editor_tabs.addTab(self.plus_tab_widget, "")
        self.editor_tabs.setTabIcon(plus_idx, render_svg_icon(PLUS_SVG, size=11, color=self.current_theme["table_header_text"]))
        self.editor_tabs.tabBar().setTabButton(plus_idx, QTabBar.ButtonPosition.LeftSide, None)
        self.editor_tabs.tabBar().setTabButton(plus_idx, QTabBar.ButtonPosition.RightSide, None)
        self.editor_tabs.setTabToolTip(plus_idx, "New File Tab (⌘N)")
        self.editor_tabs.setCurrentIndex(0)

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

        # Setup native macOS blended titlebar (like Reminders, Safari, Xcode)
        self.setup_macos_unified_titlebar()

        # Apply initial theme styling
        self.apply_theme(self.current_theme)
        self.update_window_title()

    def showEvent(self, event):
        super().showEvent(event)
        self.setup_macos_unified_titlebar()

    def setup_macos_unified_titlebar(self):
        """Blends the top title bar seamlessly into the window background like native macOS apps."""
        if sys.platform != "darwin":
            return
        try:
            import objc
            from AppKit import (
                NSApp,
                NSColor,
                NSAppearance,
                NSAppearanceNameAqua,
                NSAppearanceNameDarkAqua,
                NSWindowTitleHidden,
                NSWindowStyleMaskFullSizeContentView,
            )
            win_id = int(self.winId())
            view = objc.objc_object(c_void_p=win_id)
            nswin = view.window()
            if not nswin:
                windows = NSApp.windows()
                if windows:
                    nswin = windows[0]
            if not nswin:
                return

            nswin.setTitlebarAppearsTransparent_(True)
            nswin.setTitleVisibility_(NSWindowTitleHidden)
            nswin.setStyleMask_(nswin.styleMask() | NSWindowStyleMaskFullSizeContentView)
            nswin.setMovableByWindowBackground_(True)
            if self.current_theme["name"] == "dark":
                nswin.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameDarkAqua))
                nswin.setBackgroundColor_(NSColor.colorWithSRGBRed_green_blue_alpha_(24/255, 24/255, 27/255, 1.0))
            else:
                nswin.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameAqua))
                nswin.setBackgroundColor_(NSColor.colorWithSRGBRed_green_blue_alpha_(244/255, 244/255, 245/255, 1.0))
        except Exception:
            pass

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() <= 60:
            wh = self.windowHandle()
            if wh and wh.startSystemMove():
                event.accept()
                return
            self._drag_pos = event.globalPosition().toPoint() - self.pos()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.MouseButton.LeftButton) and getattr(self, "_drag_pos", None) is not None:
            if self.isMaximized():
                self.showNormal()
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() <= 60:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    # ==========================================
    # Multi-Tab Editor & File Management
    # ==========================================
    @property
    def editor(self) -> CodeEditor:
        """Returns the CodeEditor in the currently active tab."""
        widget = self.editor_tabs.currentWidget()
        if isinstance(widget, CodeEditor):
            return widget
        return self._fallback_editor

    @property
    def current_file_path(self) -> str | None:
        return getattr(self.editor, "file_path", None)

    @current_file_path.setter
    def current_file_path(self, path: str | None):
        if self.editor:
            self.editor.file_path = path

    @property
    def is_modified(self) -> bool:
        return getattr(self.editor, "is_modified", False)

    @is_modified.setter
    def is_modified(self, val: bool):
        if self.editor:
            self.editor.is_modified = val

    def create_editor_tab(
        self,
        title: str = "Untitled",
        content: str = "",
        file_path: str = None,
        problem_data: dict = None
    ) -> CodeEditor:
        """Creates a new code editor tab, sets metadata, attaches listeners, and makes it active."""
        ed = CodeEditor(theme=self.current_theme)
        ed.setPlaceholderText("# Type your Python code here and click Run...")
        ed.file_path = file_path
        ed.problem_data = problem_data
        ed.is_modified = False
        ed.untitled_title = title

        # Apply current zoom font size
        ef = ed.font()
        ef.setPointSize(self.font_size)
        ed.setFont(ef)

        ed.setPlainText(content)
        ed.textChanged.connect(lambda editor=ed: self.on_editor_text_changed(editor))

        plus_idx = self.editor_tabs.indexOf(self.plus_tab_widget) if hasattr(self, "plus_tab_widget") else -1
        if plus_idx != -1:
            idx = self.editor_tabs.insertTab(plus_idx, ed, title)
        else:
            idx = self.editor_tabs.addTab(ed, title)
        if file_path:
            self.editor_tabs.setTabToolTip(idx, file_path)

        # Ensure left button is cleared and right button is our custom monochromatic close button
        self.editor_tabs.tabBar().setTabButton(idx, QTabBar.ButtonPosition.LeftSide, None)
        close_btn = self.create_tab_close_button(ed)
        self.editor_tabs.tabBar().setTabButton(idx, QTabBar.ButtonPosition.RightSide, close_btn)

        # Ensure plus tab has no close button on either side
        if hasattr(self, "plus_tab_widget"):
            p_idx = self.editor_tabs.indexOf(self.plus_tab_widget)
            if p_idx != -1:
                self.editor_tabs.tabBar().setTabButton(p_idx, QTabBar.ButtonPosition.LeftSide, None)
                self.editor_tabs.tabBar().setTabButton(p_idx, QTabBar.ButtonPosition.RightSide, None)

        self.editor_tabs.setCurrentIndex(idx)
        self.update_tab_title(ed)
        self.update_window_title()
        return ed

    def create_tab_close_button(self, editor: CodeEditor) -> QWidget:
        """Creates a custom monochromatic SVG close button for a tab with comfortable right margin."""
        container = QWidget()
        container.setObjectName("tabCloseContainer")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(0)

        btn = QPushButton()
        btn.setIcon(render_svg_icon(CLOSE_SVG, size=9, color=self.current_theme["table_header_text"]))
        btn.setFixedSize(16, 16)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setToolTip("Close Tab (⌘W)")
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 3px;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['btn_clear_hover']};
            }}
        """)
        btn.clicked.connect(lambda _, ed=editor: self.close_editor_tab(ed))
        layout.addWidget(btn)
        return container

    def close_editor_tab(self, editor: CodeEditor):
        """Finds index for given editor and closes its tab."""
        idx = self.editor_tabs.indexOf(editor)
        if idx != -1:
            self.close_tab(idx)

    def on_tab_bar_clicked(self, index: int):
        """Opens a new tab when clicking the trailing '+' tab."""
        if index >= 0 and hasattr(self, "plus_tab_widget") and self.editor_tabs.widget(index) == self.plus_tab_widget:
            self.new_file()

    def on_tab_moved(self, from_idx: int, to_idx: int):
        """Keeps the trailing '+' tab locked to the right end when tabs are dragged."""
        if not hasattr(self, "plus_tab_widget"):
            return
        plus_idx = self.editor_tabs.indexOf(self.plus_tab_widget)
        last_idx = self.editor_tabs.count() - 1
        if plus_idx != -1 and plus_idx != last_idx:
            self.editor_tabs.tabBar().blockSignals(True)
            self.editor_tabs.tabBar().moveTab(plus_idx, last_idx)
            self.editor_tabs.tabBar().blockSignals(False)

    def on_editor_text_changed(self, editor: CodeEditor):
        """Called whenever code inside an editor tab is modified."""
        if not getattr(editor, "is_modified", False):
            editor.is_modified = True
            self.update_tab_title(editor)
            if editor == self.editor:
                self.update_window_title()

    def update_tab_title(self, editor: CodeEditor):
        """Updates tab label with base name and unsaved '●' indicator."""
        idx = self.editor_tabs.indexOf(editor)
        if idx == -1:
            return

        if getattr(editor, "problem_data", None):
            base_name = editor.problem_data.get("raw_title", editor.problem_data.get("title", "Problem"))
        elif getattr(editor, "file_path", None):
            base_name = os.path.basename(editor.file_path)
        else:
            base_name = getattr(editor, "untitled_title", "Untitled")

        marker = " ●" if getattr(editor, "is_modified", False) else ""
        self.editor_tabs.setTabText(idx, f"{base_name}{marker}")
        if getattr(editor, "file_path", None):
            self.editor_tabs.setTabToolTip(idx, editor.file_path)

    def on_editor_tab_changed(self, index: int):
        """Switches context when user switches tabs (toggles between Problem and Variables/Assistant)."""
        if not hasattr(self, "right_tabs"):
            return
        if index < 0 or index >= self.editor_tabs.count():
            return
        if hasattr(self, "plus_tab_widget") and self.editor_tabs.widget(index) == self.plus_tab_widget:
            # Revert to last file tab so plus tab is never selected as active content
            if index > 0:
                self.editor_tabs.setCurrentIndex(index - 1)
            return
        ed = self.editor_tabs.widget(index)
        if not isinstance(ed, CodeEditor):
            return

        prob = getattr(ed, "problem_data", None)
        if prob:
            self.is_problem_mode = True
            self.active_problem_title = prob.get("raw_title", prob.get("title"))
            self.problem_desc_widget.set_problem(prob)
            self.problem_sol_widget.set_problem(prob)
            self.problem_desc_widget.apply_theme(self.current_theme)
            self.problem_sol_widget.apply_theme(self.current_theme)
            self.problem_desc_widget.apply_font_size(self.font_size)
            self.problem_sol_widget.apply_font_size(self.font_size)

            self.right_tabs.clear()
            self.right_tabs.addTab(self.problem_desc_widget, "Description")
            self.right_tabs.addTab(self.problem_sol_widget, "Solution")
            self.right_tabs.addTab(self.variables_view, "Variables")
            self.right_tabs.addTab(self.assistant_view, "Assistant")
            self.right_tabs.setCornerWidget(self.corner_widget, Qt.Corner.TopRightCorner)
            self.tab_toggle_btn.setText("✦ Variables")
            self.tab_toggle_btn.setToolTip("Switch to Variables Inspector")
            if not self.right_tabs.isVisible():
                self.right_tabs.show()
        else:
            self.is_problem_mode = False
            self.active_problem_title = None
            self.right_tabs.setCornerWidget(None)
            self.right_tabs.clear()
            self.right_tabs.addTab(self.variables_view, "Variables")
            self.right_tabs.addTab(self.assistant_view, "Assistant")

        self.update_window_title()

    def close_tab(self, index: int):
        """Closes the tab at index. Keeps at least one tab open."""
        if index < 0 or index >= self.editor_tabs.count():
            return
        if hasattr(self, "plus_tab_widget") and self.editor_tabs.widget(index) == self.plus_tab_widget:
            return
        self.editor_tabs.removeTab(index)
        file_tabs_count = sum(1 for i in range(self.editor_tabs.count()) if isinstance(self.editor_tabs.widget(i), CodeEditor))
        if file_tabs_count == 0:
            self.new_file()

    def close_current_tab(self):
        """Closes the currently active tab (Cmd + W)."""
        idx = self.editor_tabs.currentIndex()
        if idx >= 0:
            if hasattr(self, "plus_tab_widget") and self.editor_tabs.widget(idx) == self.plus_tab_widget:
                return
            self.close_tab(idx)

    def next_tab(self):
        """Cycles to the next file tab (Ctrl + Tab)."""
        file_indices = [i for i in range(self.editor_tabs.count()) if isinstance(self.editor_tabs.widget(i), CodeEditor)]
        if len(file_indices) > 1:
            curr = self.editor_tabs.currentIndex()
            if curr in file_indices:
                curr_pos = file_indices.index(curr)
                next_pos = (curr_pos + 1) % len(file_indices)
                self.editor_tabs.setCurrentIndex(file_indices[next_pos])
            else:
                self.editor_tabs.setCurrentIndex(file_indices[0])

    def prev_tab(self):
        """Cycles to the previous file tab (Ctrl + Shift + Tab)."""
        file_indices = [i for i in range(self.editor_tabs.count()) if isinstance(self.editor_tabs.widget(i), CodeEditor)]
        if len(file_indices) > 1:
            curr = self.editor_tabs.currentIndex()
            if curr in file_indices:
                curr_pos = file_indices.index(curr)
                prev_pos = (curr_pos - 1 + len(file_indices)) % len(file_indices)
                self.editor_tabs.setCurrentIndex(file_indices[prev_pos])
            else:
                self.editor_tabs.setCurrentIndex(file_indices[0])

    def create_menu_bar(self):
        """Creates the native macOS File menu bar with multi-tab support."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_action = file_menu.addAction("New File")
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.new_file)

        open_action = file_menu.addAction("Open File...")
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)

        close_action = file_menu.addAction("Close Tab")
        close_action.setShortcut(QKeySequence("Ctrl+W"))
        close_action.triggered.connect(self.close_current_tab)

        file_menu.addSeparator()

        save_action = file_menu.addAction("Save")
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)

        save_as_action = file_menu.addAction("Save As...")
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_file_as)

        # Tab navigation keyboard shortcuts
        self.shortcut_next_tab = QShortcut(QKeySequence("Ctrl+Tab"), self)
        self.shortcut_next_tab.activated.connect(self.next_tab)
        self.shortcut_prev_tab = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
        self.shortcut_prev_tab.activated.connect(self.prev_tab)

        # Tools Menu
        tools_menu = menubar.addMenu("Tools")
        pkg_action = tools_menu.addAction("Manage Packages...")
        pkg_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        pkg_action.triggered.connect(self.open_package_manager)

        problems_action = tools_menu.addAction("Practice Problems...")
        problems_action.setShortcut(QKeySequence("Ctrl+Shift+R"))
        problems_action.triggered.connect(self.open_problems_dialog)

        # Help Menu
        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About Winnie...")
        about_action.triggered.connect(self.open_about_dialog)

    def open_about_dialog(self):
        """Opens the About Winnie dialog."""
        dlg = AboutDialog(self, theme=self.current_theme)
        dlg.exec()

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
        """Loads a practice problem into its own dedicated tab."""
        prob_id = problem.get("id")
        title = problem.get("raw_title", problem.get("title", "Problem"))
        starter_code = problem.get("starter_code", "")

        # Check if this problem is already open in an existing tab
        for i in range(self.editor_tabs.count()):
            ed = self.editor_tabs.widget(i)
            if not isinstance(ed, CodeEditor):
                continue
            p = getattr(ed, "problem_data", None)
            if p and p.get("id") == prob_id:
                self.editor_tabs.setCurrentIndex(i)
                return

        # Check if current tab is an untouched starter/empty tab
        curr = self.editor
        file_tabs_count = sum(1 for i in range(self.editor_tabs.count()) if isinstance(self.editor_tabs.widget(i), CodeEditor))
        if (
            file_tabs_count == 1
            and not getattr(curr, "file_path", None)
            and not getattr(curr, "problem_data", None)
            and not getattr(curr, "is_modified", False)
            and curr.toPlainText().strip() in (
                "",
                "# Type your Python code here and click Run...",
                (
                    'total = 0\n'
                    'items = [10, 20, 30]\n\n'
                    'for x in items:\n'
                    '    total += x\n'
                    '    print(f"Added {x}, running total is {total}")\n\n'
                    'print("All done!")'
                )
            )
        ):
            curr.setPlainText(starter_code)
            curr.problem_data = problem
            curr.is_modified = False
            curr.untitled_title = title
            self.update_tab_title(curr)
            self.on_editor_tab_changed(self.editor_tabs.currentIndex())
            return

        # Otherwise create a fresh tab for the problem
        self.create_editor_tab(title=title, content=starter_code, file_path=None, problem_data=problem)

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
        """Loads reference solution code into current editor upon request."""
        self.editor.setPlainText(solution_code)
        self.editor.is_modified = True
        self.update_tab_title(self.editor)
        self.update_window_title()
        self.console.append_output("\n[Solution copied to editor — click Step or Variables tab to inspect live]\n")

    def on_text_changed(self):
        """Fallback text change slot."""
        self.on_editor_text_changed(self.editor)

    def update_window_title(self):
        """Updates the macOS window title and native unsaved indicator."""
        ed = self.editor
        if not ed:
            self.setWindowTitle("Winnie")
            self.setWindowModified(False)
            return

        if getattr(ed, "problem_data", None):
            filename = ed.problem_data.get("raw_title", ed.problem_data.get("title", "Problem"))
        elif getattr(ed, "file_path", None):
            filename = os.path.basename(ed.file_path)
        else:
            filename = getattr(ed, "untitled_title", "Untitled")

        is_mod = getattr(ed, "is_modified", False)
        self.setWindowModified(is_mod)
        mod_marker = " ●" if is_mod else ""
        self.setWindowTitle(f"{filename}{mod_marker} — Winnie [*]")

    def maybe_save(self) -> bool:
        """By default do not prompt to save; user can save via Cmd+S or File menu."""
        return True

    def new_file(self):
        """Creates a new empty file in a new tab (Cmd + N)."""
        self.untitled_counter += 1
        title = f"Untitled-{self.untitled_counter}"
        self.create_editor_tab(title=title, content="", file_path=None, problem_data=None)

    def open_file(self):
        """Opens one or multiple existing Python files from disk into separate tabs (Cmd + O)."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open Python Files", "", "Python Files (*.py);;All Files (*)"
        )
        if not paths:
            return
        for path in paths:
            self.open_file_path(path)

    def open_file_path(self, path: str):
        """Opens a single file path into an editor tab."""
        # Check if already open
        for i in range(self.editor_tabs.count()):
            ed = self.editor_tabs.widget(i)
            if getattr(ed, "file_path", None) == path:
                self.editor_tabs.setCurrentIndex(i)
                return

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error Opening File", f"Could not read file '{path}':\n{e}")
            return

        # Check if current single tab is an untouched starter tab
        curr = self.editor
        if (
            self.editor_tabs.count() == 1
            and not getattr(curr, "file_path", None)
            and not getattr(curr, "problem_data", None)
            and not getattr(curr, "is_modified", False)
            and curr.toPlainText().strip() in (
                "",
                "# Type your Python code here and click Run...",
                (
                    'total = 0\n'
                    'items = [10, 20, 30]\n\n'
                    'for x in items:\n'
                    '    total += x\n'
                    '    print(f"Added {x}, running total is {total}")\n\n'
                    'print("All done!")'
                )
            )
        ):
            curr.setPlainText(content)
            curr.file_path = path
            curr.is_modified = False
            self.update_tab_title(curr)
            self.update_window_title()
            return

        filename = os.path.basename(path)
        self.create_editor_tab(title=filename, content=content, file_path=path)

    def save_file(self) -> bool:
        """Saves current active tab to disk (Cmd + S)."""
        ed = self.editor
        if not ed:
            return False
        if not getattr(ed, "file_path", None):
            return self.save_file_as()
        try:
            with open(ed.file_path, "w", encoding="utf-8") as f:
                f.write(ed.toPlainText())
            ed.is_modified = False
            self.update_tab_title(ed)
            self.update_window_title()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error Saving File", f"Could not save file:\n{e}")
            return False

    def save_file_as(self) -> bool:
        """Prompts for a filename and saves current active tab (Cmd + Shift + S)."""
        ed = self.editor
        if not ed:
            return False
        suggested = ""
        if getattr(ed, "file_path", None):
            suggested = ed.file_path
        elif getattr(ed, "problem_data", None):
            suggested = f"{ed.problem_data.get('id', 'solution')}.py"

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Python File", suggested, "Python Files (*.py);;All Files (*)"
        )
        if not path:
            return False
        if not path.endswith(".py"):
            path += ".py"
        ed.file_path = path
        ed.problem_data = None  # once saved as file, it's a regular file
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

        # 1. Update all open Code Editors font & line number gutter width
        for i in range(self.editor_tabs.count()):
            ed = self.editor_tabs.widget(i)
            if isinstance(ed, CodeEditor):
                editor_font = ed.font()
                editor_font.setPointSize(size)
                ed.setFont(editor_font)
                ed.update_line_number_area_width(0)
                ed.line_number_area.update()

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
        bar = TopActionBar(self)
        bar.setFixedHeight(44)
        bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 1. Clean Minimal Brand Name
        self.brand = QLabel("Winnie")
        self.brand.setFont(QFont("SF Pro Display", 16, QFont.Weight.Bold))
        self.brand.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
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

        # 6. Monochromatic Info Button (About Winnie)
        self.info_btn = QPushButton()
        self.info_btn.setToolTip("About Winnie")
        self.info_btn.setFont(QFont("SF Pro Text", 12))
        self.info_btn.setIconSize(QSize(15, 15))
        self.info_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.info_btn.clicked.connect(self.open_about_dialog)
        layout.addWidget(self.info_btn)

        return bar

    def toggle_theme(self):
        """Switches between Dark and Light mode."""
        if self.current_theme["name"] == "dark":
            self.apply_theme(LIGHT_THEME)
        else:
            self.apply_theme(DARK_THEME)

    def apply_theme(self, theme):
        self.current_theme = theme

        # Set application and window palette to ensure Cocoa paints light mode background
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(theme["window_bg"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme["brand_color"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(theme["editor_bg"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(theme["editor_text"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(theme["btn_clear_bg"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme["btn_clear_text"]))
        self.setPalette(palette)
        app_inst = QApplication.instance()
        if app_inst:
            app_inst.setPalette(palette)

        # Update native macOS window appearance and background
        if sys.platform == "darwin":
            try:
                import objc
                from AppKit import (
                    NSApp,
                    NSColor,
                    NSAppearance,
                    NSAppearanceNameAqua,
                    NSAppearanceNameDarkAqua,
                )
                win_id = int(self.winId())
                view = objc.objc_object(c_void_p=win_id)
                nswin = view.window()
                if not nswin:
                    windows = NSApp.windows()
                    if windows:
                        nswin = windows[0]
                if nswin:
                    if theme["name"] == "dark":
                        nswin.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameDarkAqua))
                        nswin.setBackgroundColor_(NSColor.colorWithSRGBRed_green_blue_alpha_(24/255, 24/255, 27/255, 1.0))
                    else:
                        nswin.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameAqua))
                        nswin.setBackgroundColor_(NSColor.colorWithSRGBRed_green_blue_alpha_(244/255, 244/255, 245/255, 1.0))
            except Exception:
                pass

        # Main window and splitters + sleek global scrollbars
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
            {get_scrollbar_stylesheet(theme)}
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

        # Info (About Winnie) button styling & monochromatic icon
        self.info_btn.setIcon(render_svg_icon(INFO_SVG, size=15, color=theme["btn_clear_text"]))
        self.info_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 10px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)

        # Editor Tabs Styling (VS Code / Sublime-like sleek tabs)
        self.editor_tabs.setStyleSheet(f"""
            QTabWidget#editorTabs::pane {{
                border: 1px solid {theme['border_color']};
                background-color: {theme['editor_bg']};
                border-top: none;
            }}
            QTabWidget#editorTabs QTabBar {{
                qproperty-drawBase: 0;
                background-color: {theme['console_bg']};
                border-bottom: 1px solid {theme['border_color']};
            }}
            QTabWidget#editorTabs QTabBar::tab {{
                background-color: {theme['console_bg']};
                color: {theme['table_header_text']};
                padding: 5px 6px 5px 12px;
                margin-right: 2px;
                border: 1px solid transparent;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 11px;
                font-weight: 500;
            }}
            QTabWidget#editorTabs QTabBar::tab:hover {{
                background-color: {theme['btn_clear_hover']};
                color: {theme['brand_color']};
            }}
            QTabWidget#editorTabs QTabBar::tab:selected {{
                background-color: {theme['editor_bg']};
                color: {theme['brand_color']};
                border: 1px solid {theme['border_color']};
                border-bottom: 1px solid {theme['editor_bg']};
                font-weight: 600;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)

        # Update inline "+" tab icon
        if hasattr(self, "plus_tab_widget"):
            plus_idx = self.editor_tabs.indexOf(self.plus_tab_widget)
            if plus_idx != -1:
                self.editor_tabs.setTabIcon(plus_idx, render_svg_icon(PLUS_SVG, size=11, color=theme["table_header_text"]))
                self.editor_tabs.tabBar().setTabButton(plus_idx, QTabBar.ButtonPosition.LeftSide, None)
                self.editor_tabs.tabBar().setTabButton(plus_idx, QTabBar.ButtonPosition.RightSide, None)

        # Update monochromatic close buttons on open file tabs
        for i in range(self.editor_tabs.count()):
            widget = self.editor_tabs.widget(i)
            if isinstance(widget, CodeEditor):
                self.editor_tabs.tabBar().setTabButton(i, QTabBar.ButtonPosition.LeftSide, None)
                tab_btn = self.editor_tabs.tabBar().tabButton(i, QTabBar.ButtonPosition.RightSide)
                btn = tab_btn.findChild(QPushButton) if isinstance(tab_btn, QWidget) else (tab_btn if isinstance(tab_btn, QPushButton) else None)
                if btn:
                    btn.setIcon(render_svg_icon(CLOSE_SVG, size=9, color=theme["table_header_text"]))
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background: transparent;
                            border: none;
                            border-radius: 3px;
                            padding: 0px;
                            margin: 0px;
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
            QTabWidget > QStackedWidget, QTabWidget > QStackedWidget > QWidget {{
                background-color: {theme['table_bg']};
            }}
            QTabBar {{
                qproperty-drawBase: 0;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {theme['table_header_text']};
                padding: 5px 8px;
                margin-right: 2px;
                font-size: 11px;
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
            {get_scrollbar_stylesheet(theme)}
        """)

        # Propagate to child widgets across all open editor tabs
        for i in range(self.editor_tabs.count()):
            ed = self.editor_tabs.widget(i)
            if isinstance(ed, CodeEditor):
                ed.apply_theme(theme)
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
    setup_macos_app_identity()
    app = QApplication(sys.argv)
    app.setApplicationName("Winnie")
    app.setApplicationDisplayName("Winnie")
    app.setDesktopFileName("Winnie")

    icon_path = get_resource_path("Winnie.png")
    if not os.path.exists(icon_path):
        icon_path = get_resource_path("Winnie.icns")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        if sys.platform == "darwin":
            try:
                from AppKit import NSApp, NSImage
                ns_img = NSImage.alloc().initWithContentsOfFile_(icon_path)
                if ns_img:
                    NSApp.setApplicationIconImage_(ns_img)
            except Exception:
                pass

    ide = WinnieIDE()
    ide.show()
    sys.exit(app.exec())
