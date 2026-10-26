import json
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QSplitter,
    QWidget,
    QMessageBox,
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, QProcess
from theme import DARK_THEME, get_scrollbar_stylesheet


class PackageManagerDialog(QDialog):
    """A graphical package manager dialog for installing and managing pip packages."""

    def __init__(self, parent=None, python_executable="python3", theme=DARK_THEME):
        super().__init__(parent)
        self.python_executable = python_executable
        self.current_theme = theme
        self.setWindowTitle("Manage Python Packages (pip)")
        self.resize(750, 520)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.handle_process_finished)
        self.current_action = None  # 'list', 'install', 'uninstall'

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        # 1. Header: Python Environment Info
        env_label = QLabel(f"Environment: {self.python_executable}")
        env_label.setFont(QFont("Dank Mono", 11))
        env_label.setStyleSheet("color: #71717a;")
        layout.addWidget(env_label)

        # 2. Package Install Bar
        install_bar = QHBoxLayout()
        install_bar.setSpacing(8)

        self.package_input = QLineEdit()
        self.package_input.setPlaceholderText("Enter package name (e.g. requests, pygame, pandas, matplotlib)...")
        self.package_input.setFont(QFont("SF Pro Text", 12))
        self.package_input.returnPressed.connect(self.install_package)
        install_bar.addWidget(self.package_input)

        self.install_btn = QPushButton("Install")
        self.install_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Bold))
        self.install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install_btn.clicked.connect(self.install_package)
        install_bar.addWidget(self.install_btn)

        layout.addLayout(install_bar)

        # 3. Main Splitter: Installed Table on Left, Actions & Log on Right
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top half: Installed Packages Table + Filter
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(6)

        table_header = QHBoxLayout()
        title = QLabel("Installed Packages")
        title.setFont(QFont("SF Pro Display", 12, QFont.Weight.Bold))
        table_header.addWidget(title)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter installed...")
        self.filter_input.setMaximumWidth(200)
        self.filter_input.setFont(QFont("SF Pro Text", 11))
        self.filter_input.textChanged.connect(self.filter_packages)
        table_header.addWidget(self.filter_input)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setFont(QFont("SF Pro Text", 11))
        self.refresh_btn.clicked.connect(self.refresh_installed_packages)
        table_header.addWidget(self.refresh_btn)

        self.uninstall_btn = QPushButton("Uninstall Selected")
        self.uninstall_btn.setFont(QFont("SF Pro Text", 11))
        self.uninstall_btn.setEnabled(False)
        self.uninstall_btn.clicked.connect(self.uninstall_selected_package)
        table_header.addWidget(self.uninstall_btn)

        table_layout.addLayout(table_header)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Package", "Version"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.setFont(QFont("Dank Mono", 12))
        table_layout.addWidget(self.table)
        splitter.addWidget(table_container)

        # Bottom half: Live Log Console
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(4)

        log_label = QLabel("Activity Log")
        log_label.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        log_label.setStyleSheet("color: #71717a;")
        log_layout.addWidget(log_label)

        self.log_console = QPlainTextEdit()
        self.log_console.setFont(QFont("Dank Mono", 11))
        self.log_console.setReadOnly(True)
        log_layout.addWidget(self.log_console)
        splitter.addWidget(log_container)

        splitter.setStretchFactor(0, 6)
        splitter.setStretchFactor(1, 4)
        layout.addWidget(splitter)

        self.all_packages = []
        self.apply_theme(self.current_theme)

        # Initial load of installed packages
        self.refresh_installed_packages()

    def apply_theme(self, theme):
        self.current_theme = theme
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
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 6px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
            QPushButton:disabled {{
                color: #52525b;
                background-color: transparent;
            }}
            QTableWidget {{
                background-color: {theme['table_bg']};
                color: {theme['table_text']};
                gridline-color: {theme['table_border']};
                border: 1px solid {theme['table_border']};
                border-radius: 6px;
            }}
            QHeaderView::section {{
                background-color: {theme['table_header_bg']};
                color: {theme['table_header_text']};
                font-size: 11px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid {theme['table_border']};
                padding: 4px;
            }}
            QPlainTextEdit {{
                background-color: {theme['console_bg']};
                color: {theme['console_text']};
                border: 1px solid {theme['console_border']};
                border-radius: 6px;
                padding: 6px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)

        # Install button emerald styling
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #27272a;
                color: #52525b;
            }
        """)

    def refresh_installed_packages(self):
        """Runs `pip list --format=json` to fetch installed packages."""
        if self.process.state() != QProcess.ProcessState.NotRunning:
            return

        self.current_action = "list"
        self.set_busy(True)
        self.log_console.appendPlainText(">>> Checking installed packages...\n")
        self.process_output_buffer = []
        self.process.start(self.python_executable, ["-m", "pip", "list", "--format=json"])

    def install_package(self):
        """Installs package entered in input box."""
        pkg = self.package_input.text().strip()
        if not pkg or self.process.state() != QProcess.ProcessState.NotRunning:
            return

        self.current_action = "install"
        self.set_busy(True)
        self.log_console.appendPlainText(f"\n>>> pip install {pkg}...\n")
        self.process_output_buffer = []
        self.process.start(self.python_executable, ["-m", "pip", "install", pkg])

    def uninstall_selected_package(self):
        """Uninstalls the currently selected package from table."""
        selected_row = self.table.currentRow()
        if selected_row < 0 or self.process.state() != QProcess.ProcessState.NotRunning:
            return

        pkg_name = self.table.item(selected_row, 0).text()
        reply = QMessageBox.question(
            self,
            "Uninstall Package",
            f"Are you sure you want to uninstall '{pkg_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.current_action = "uninstall"
        self.set_busy(True)
        self.log_console.appendPlainText(f"\n>>> pip uninstall -y {pkg_name}...\n")
        self.process_output_buffer = []
        self.process.start(self.python_executable, ["-m", "pip", "uninstall", "-y", pkg_name])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        if self.current_action == "list":
            self.process_output_buffer.append(data)
        else:
            self.log_console.insertPlainText(data)
            self.log_console.ensureCursorVisible()

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode("utf-8", errors="replace")
        self.log_console.insertPlainText(data)
        self.log_console.ensureCursorVisible()

    def handle_process_finished(self, exit_code, exit_status):
        self.set_busy(False)

        if self.current_action == "list":
            try:
                full_json = "".join(self.process_output_buffer)
                self.all_packages = json.loads(full_json)
                self.populate_table(self.all_packages)
                self.log_console.appendPlainText(f"Found {len(self.all_packages)} installed packages.\n")
            except Exception as e:
                self.log_console.appendPlainText(f"Error parsing packages: {e}\n")
        elif self.current_action in ("install", "uninstall"):
            if exit_code == 0:
                self.log_console.appendPlainText("\n[Operation Completed Successfully!]\n")
                self.package_input.clear()
            else:
                self.log_console.appendPlainText(f"\n[Operation failed with exit code {exit_code}]\n")
            # Refresh list
            self.refresh_installed_packages()

    def populate_table(self, packages):
        self.table.setRowCount(0)
        for row, pkg in enumerate(packages):
            self.table.insertRow(row)

            name_item = QTableWidgetItem(pkg["name"])
            name_item.setForeground(QColor("#38bdf8"))

            ver_item = QTableWidgetItem(pkg["version"])
            ver_item.setForeground(QColor("#a1a1aa"))

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, ver_item)

    def filter_packages(self, text):
        query = text.strip().lower()
        filtered = [p for p in self.all_packages if query in p["name"].lower()]
        self.populate_table(filtered)

    def on_selection_changed(self):
        has_sel = self.table.currentRow() >= 0
        self.uninstall_btn.setEnabled(has_sel)

    def set_busy(self, busy: bool):
        self.install_btn.setEnabled(not busy)
        self.refresh_btn.setEnabled(not busy)
        self.uninstall_btn.setEnabled(not busy and self.table.currentRow() >= 0)
