"""
SQL Playground UI Widget for Winnie.
Features:
- Multi-schema enterprise database selection (E-Commerce & SaaS, Tech HR, Fintech)
- Interactive Schema Explorer with column definitions, keys, and 1-click sample data previews
- SQL Editor with syntax highlighting (SqlHighlighter) and execution shortcuts (Cmd+Enter)
- Query Results table with execution metrics (ms, row count)
- Physical Query Plan visualizer (parsing SQLite EXPLAIN QUERY PLAN into Scan vs Index trees)
- Logical Execution Order pipeline (FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT)
- Interactive Graded Practice Challenges with automated solution validation
- Dynamic Honey Dark & Honey Light theme support
"""

import time
from typing import Optional, Dict, Any, List

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QPushButton,
    QLabel,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTabWidget,
    QLineEdit,
    QTextEdit,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QMenu,
    QApplication,
)
from PySide6.QtGui import (
    QFont,
    QColor,
    QIcon,
    QAction,
    QCursor,
    QKeySequence,
    QShortcut,
)
from PySide6.QtCore import Qt, Signal, QSize

from editor import CodeEditor
from sql_highlighter import SqlHighlighter
from sql_engine import SqlEngine, QueryResult
from sql_challenges import SQL_CHALLENGES, get_challenges_by_schema, verify_challenge_solution
from theme import DARK_THEME, get_scrollbar_stylesheet, get_code_font
from icons import render_svg_icon, RUN_SVG, CLEAR_SVG, DATABASE_SVG, LIGHTNING_SVG, TABLE_SVG


class SqlCodeEditor(CodeEditor):
    """Code editor specialized for SQL with SqlHighlighter."""

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent, theme=theme)
        # Detach default python highlighter and attach SQL highlighter
        if hasattr(self, "highlighter") and self.highlighter:
            self.highlighter.setDocument(None)
        self.highlighter = SqlHighlighter(self.document(), theme=self.current_theme)

    def apply_theme(self, theme):
        self.current_theme = theme
        if hasattr(self, "highlighter") and self.highlighter:
            self.highlighter.apply_theme(theme)

        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {theme['editor_bg']};
                color: {theme['editor_text']};
                border: none;
                selection-background-color: {theme['editor_selection']};
                padding: 8px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.line_number_area.update()


class SqlPlaygroundWidget(QWidget):
    """Complete SQL Playground interface embedded inside Winnie."""

    exit_requested = Signal()

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.engine = SqlEngine("ecommerce")
        self.active_challenge: Optional[Dict[str, Any]] = None

        self._init_ui()
        self.apply_theme(self.current_theme)
        self.refresh_schema_browser()
        self.refresh_challenges_list()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Action Toolbar
        self.toolbar = QWidget(self)
        self.toolbar.setFixedHeight(48)
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(14, 6, 14, 6)
        toolbar_layout.setSpacing(10)

        # Database Schema Selector
        schema_label = QLabel("Schema:", self)
        schema_label.setFont(QFont("-apple-system", 12, QFont.Weight.DemiBold))
        toolbar_layout.addWidget(schema_label)

        self.schema_combo = QComboBox(self)
        self.schema_combo.setFixedHeight(30)
        self.schema_combo.setMinimumWidth(190)
        for key, s_info in SqlEngine.SCHEMAS.items():
            self.schema_combo.addItem(f"{s_info['icon']}  {s_info['name']}", key)
        self.schema_combo.currentIndexChanged.connect(self._on_schema_changed)
        toolbar_layout.addWidget(self.schema_combo)

        # Separator
        sep1 = QFrame(self)
        sep1.setFrameShape(QFrame.Shape.VLine)
        sep1.setFrameShadow(QFrame.Shadow.Sunken)
        toolbar_layout.addWidget(sep1)

        # Action: Run Query Button
        self.run_btn = QPushButton(" Run Query", self)
        self.run_btn.setFixedHeight(32)
        self.run_btn.setIcon(render_svg_icon(RUN_SVG, size=14, color="#111827"))
        self.run_btn.setToolTip("Execute SQL Query (⌘Return)")
        self.run_btn.clicked.connect(self.run_current_query)
        toolbar_layout.addWidget(self.run_btn)

        # Action: Explain Plan Button
        self.explain_btn = QPushButton(" Explain Plan", self)
        self.explain_btn.setFixedHeight(32)
        self.explain_btn.setIcon(render_svg_icon(LIGHTNING_SVG, size=14, color="#F59E0B"))
        self.explain_btn.setToolTip("Analyze Physical & Logical Query Plan (⌘E)")
        self.explain_btn.clicked.connect(self.explain_current_query)
        toolbar_layout.addWidget(self.explain_btn)

        # Action: Reset Database Button
        self.reset_btn = QPushButton(" Reset DB", self)
        self.reset_btn.setFixedHeight(32)
        self.reset_btn.setToolTip("Reset currently active schema to original seed state")
        self.reset_btn.clicked.connect(self.reset_database)
        toolbar_layout.addWidget(self.reset_btn)

        # Action: Clear Editor
        self.clear_btn = QPushButton(" Clear", self)
        self.clear_btn.setFixedHeight(32)
        self.clear_btn.setIcon(render_svg_icon(CLEAR_SVG, size=14, color="#9CA3AF"))
        self.clear_btn.clicked.connect(self.clear_editor)
        toolbar_layout.addWidget(self.clear_btn)

        toolbar_layout.addStretch()

        # Exit / Back to Python Button
        self.exit_btn = QPushButton("← Back to Python IDE", self)
        self.exit_btn.setFixedHeight(32)
        self.exit_btn.clicked.connect(self.exit_requested.emit)
        toolbar_layout.addWidget(self.exit_btn)

        main_layout.addWidget(self.toolbar)

        # 2. Main Horizontal Splitter (Sidebar on left, Workspace on right)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.main_splitter.setHandleWidth(1)

        # Left Sidebar (Schema Explorer & Challenges Tabs)
        self.sidebar_tabs = QTabWidget(self)
        self.sidebar_tabs.setMinimumWidth(260)
        self.sidebar_tabs.setMaximumWidth(420)

        # Tab 1: Schema Explorer
        schema_widget = QWidget(self)
        schema_layout = QVBoxLayout(schema_widget)
        schema_layout.setContentsMargins(8, 8, 8, 8)
        schema_layout.setSpacing(6)

        self.schema_search = QLineEdit(self)
        self.schema_search.setPlaceholderText("Filter tables & columns...")
        self.schema_search.setFixedHeight(28)
        self.schema_search.textChanged.connect(self._filter_schema_tree)
        schema_layout.addWidget(self.schema_search)

        self.schema_tree = QTreeWidget(self)
        self.schema_tree.setHeaderHidden(True)
        self.schema_tree.itemDoubleClicked.connect(self._on_tree_item_double_clicked)
        self.schema_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.schema_tree.customContextMenuRequested.connect(self._show_schema_context_menu)
        schema_layout.addWidget(self.schema_tree)

        self.sidebar_tabs.addTab(schema_widget, "📁 Schema")

        # Tab 2: Practice Challenges
        challenges_widget = QWidget(self)
        challenges_layout = QVBoxLayout(challenges_widget)
        challenges_layout.setContentsMargins(8, 8, 8, 8)
        challenges_layout.setSpacing(6)

        self.challenges_tree = QTreeWidget(self)
        self.challenges_tree.setHeaderLabels(["Challenge", "Difficulty"])
        self.challenges_tree.itemClicked.connect(self._on_challenge_selected)
        challenges_layout.addWidget(self.challenges_tree)

        self.sidebar_tabs.addTab(challenges_widget, "🎯 Challenges")

        self.main_splitter.addWidget(self.sidebar_tabs)

        # Right Workspace (Editor on Top, Results/Plans Tabs on Bottom)
        self.workspace_splitter = QSplitter(Qt.Orientation.Vertical, self)
        self.workspace_splitter.setHandleWidth(1)

        # SQL Editor
        self.editor = SqlCodeEditor(self, theme=self.current_theme)
        default_welcome_sql = (
            "-- Welcome to Winnie SQL Playground!\n"
            "-- In-Memory SQLite with rich enterprise schemas.\n"
            "-- Press Cmd+Enter (Ctrl+Enter) to run queries.\n\n"
            "SELECT \n"
            "  c.name AS category_name,\n"
            "  COUNT(p.product_id) AS total_products,\n"
            "  ROUND(AVG(p.price), 2) AS avg_product_price\n"
            "FROM categories c\n"
            "LEFT JOIN products p ON c.category_id = p.category_id\n"
            "GROUP BY c.name\n"
            "ORDER BY total_products DESC;\n"
        )
        self.editor.setPlainText(default_welcome_sql)
        self.workspace_splitter.addWidget(self.editor)

        # Bottom Inspector / Results Tab Widget
        self.bottom_tabs = QTabWidget(self)

        # Tab 1: Query Results
        results_widget = QWidget(self)
        results_layout = QVBoxLayout(results_widget)
        results_layout.setContentsMargins(6, 6, 6, 6)
        results_layout.setSpacing(4)

        self.results_status_bar = QLabel("Ready to execute query.", self)
        self.results_status_bar.setFont(QFont("-apple-system", 11))
        results_layout.addWidget(self.results_status_bar)

        self.results_table = QTableWidget(self)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.verticalHeader().setDefaultSectionSize(26)
        results_layout.addWidget(self.results_table)

        self.bottom_tabs.addTab(results_widget, "📊 Query Results")

        # Tab 2: Physical Query Plan (EXPLAIN QUERY PLAN)
        plan_widget = QWidget(self)
        plan_layout = QVBoxLayout(plan_widget)
        plan_layout.setContentsMargins(12, 12, 12, 12)
        plan_layout.setSpacing(8)

        plan_header = QLabel("Physical Query Plan & Optimization Analysis (EXPLAIN QUERY PLAN)", self)
        plan_header.setFont(QFont("-apple-system", 12, QFont.Weight.Bold))
        plan_layout.addWidget(plan_header)

        self.plan_scroll = QScrollArea(self)
        self.plan_scroll.setWidgetResizable(True)
        self.plan_content_widget = QWidget(self)
        self.plan_content_layout = QVBoxLayout(self.plan_content_widget)
        self.plan_content_layout.setContentsMargins(0, 0, 0, 0)
        self.plan_content_layout.setSpacing(8)
        self.plan_scroll.setWidget(self.plan_content_widget)
        plan_layout.addWidget(self.plan_scroll)

        self.bottom_tabs.addTab(plan_widget, "⚡ Physical Plan")

        # Tab 3: Logical Order of Execution Pipeline
        logical_widget = QWidget(self)
        logical_layout = QVBoxLayout(logical_widget)
        logical_layout.setContentsMargins(12, 12, 12, 12)
        logical_layout.setSpacing(8)

        logical_header = QLabel("Logical Order of Execution Pipeline", self)
        logical_header.setFont(QFont("-apple-system", 12, QFont.Weight.Bold))
        logical_layout.addWidget(logical_header)

        logical_sub = QLabel(
            "SQL is declarative: while you write SELECT first, the engine evaluates FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.",
            self
        )
        logical_sub.setFont(QFont("-apple-system", 11))
        logical_sub.setWordWrap(True)
        logical_layout.addWidget(logical_sub)

        self.logical_scroll = QScrollArea(self)
        self.logical_scroll.setWidgetResizable(True)
        self.logical_content_widget = QWidget(self)
        self.logical_content_layout = QVBoxLayout(self.logical_content_widget)
        self.logical_content_layout.setContentsMargins(0, 0, 0, 0)
        self.logical_content_layout.setSpacing(8)
        self.logical_scroll.setWidget(self.logical_content_widget)
        logical_layout.addWidget(self.logical_scroll)

        self.bottom_tabs.addTab(logical_widget, "🧩 Execution Order")

        # Tab 4: Challenge Verification & Details
        challenge_tab_widget = QWidget(self)
        challenge_tab_layout = QVBoxLayout(challenge_tab_widget)
        challenge_tab_layout.setContentsMargins(12, 12, 12, 12)
        challenge_tab_layout.setSpacing(8)

        self.challenge_title_label = QLabel("No active challenge selected.", self)
        self.challenge_title_label.setFont(QFont("-apple-system", 14, QFont.Weight.Bold))
        challenge_tab_layout.addWidget(self.challenge_title_label)

        self.challenge_story_text = QTextEdit(self)
        self.challenge_story_text.setReadOnly(True)
        self.challenge_story_text.setFixedHeight(95)
        challenge_tab_layout.addWidget(self.challenge_story_text)

        challenge_btn_row = QHBoxLayout()
        self.test_challenge_btn = QPushButton(" Verify Solution (Run Tests)", self)
        self.test_challenge_btn.setFixedHeight(30)
        self.test_challenge_btn.clicked.connect(self.verify_active_challenge)
        challenge_btn_row.addWidget(self.test_challenge_btn)

        self.show_hint_btn = QPushButton("Show Hint", self)
        self.show_hint_btn.setFixedHeight(30)
        self.show_hint_btn.clicked.connect(self._toggle_hint)
        challenge_btn_row.addWidget(self.show_hint_btn)
        challenge_btn_row.addStretch()
        challenge_tab_layout.addLayout(challenge_btn_row)

        self.challenge_feedback_label = QLabel("", self)
        self.challenge_feedback_label.setFont(QFont("-apple-system", 11))
        self.challenge_feedback_label.setWordWrap(True)
        challenge_tab_layout.addWidget(self.challenge_feedback_label)

        self.bottom_tabs.addTab(challenge_tab_widget, "💡 Challenge Details")

        self.workspace_splitter.addWidget(self.bottom_tabs)

        # Set split ratios
        self.workspace_splitter.setSizes([320, 280])
        self.main_splitter.addWidget(self.workspace_splitter)
        self.main_splitter.setSizes([260, 740])

        main_layout.addWidget(self.main_splitter)

        # Keyboard shortcuts
        self.run_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.run_shortcut.activated.connect(self.run_current_query)
        self.run_mac_shortcut = QShortcut(QKeySequence("Meta+Return"), self)
        self.run_mac_shortcut.activated.connect(self.run_current_query)

        self.explain_shortcut = QShortcut(QKeySequence("Meta+E"), self)
        self.explain_shortcut.activated.connect(self.explain_current_query)

    # -------------------------------------------------------------------------
    # Schema Browser & Challenges Management
    # -------------------------------------------------------------------------

    def _on_schema_changed(self, index: int):
        schema_key = self.schema_combo.currentData()
        self.engine.load_schema(schema_key)
        self.refresh_schema_browser()
        self.refresh_challenges_list()
        self.results_status_bar.setText(f"Switched to schema: {SqlEngine.SCHEMAS[schema_key]['name']} (DB reloaded).")

    def reset_database(self):
        schema_key = self.schema_combo.currentData()
        self.engine.reset_current_schema()
        self.refresh_schema_browser()
        self.results_status_bar.setText(f"Database reset to clean seed state.")

    def refresh_schema_browser(self):
        """Populates the schema tree with tables, columns, data types, and keys."""
        self.schema_tree.clear()
        schema_info = self.engine.get_schema_info()

        for table_name, data in schema_info.items():
            row_count = data["row_count"]
            table_item = QTreeWidgetItem([f"{table_name} ({row_count} rows)"])
            table_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "table", "name": table_name})
            table_item.setFont(0, QFont("-apple-system", 12, QFont.Weight.DemiBold))

            # Add columns as children
            for col in data["columns"]:
                pk_badge = " [PK]" if col["pk"] else ""
                nullable_badge = "" if col["notnull"] else " [NULL]"
                col_text = f"  {col['name']}: {col['type']}{pk_badge}{nullable_badge}"
                col_item = QTreeWidgetItem([col_text])
                col_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "column", "table": table_name, "col": col['name']})
                col_item.setFont(0, QFont(get_code_font().family(), 11))
                table_item.addChild(col_item)

            self.schema_tree.addTopLevelItem(table_item)

        self.schema_tree.expandAll()

    def _filter_schema_tree(self, filter_text: str):
        query = filter_text.strip().lower()
        for i in range(self.schema_tree.topLevelItemCount()):
            table_item = self.schema_tree.topLevelItem(i)
            table_match = query in table_item.text(0).lower()
            any_child_match = False

            for j in range(table_item.childCount()):
                col_item = table_item.child(j)
                col_match = query in col_item.text(0).lower()
                col_item.setHidden(not (query == "" or col_match or table_match))
                if col_match:
                    any_child_match = True

            table_item.setHidden(not (query == "" or table_match or any_child_match))

    def _on_tree_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        if data.get("type") == "table":
            table_name = data.get("name")
            preview_query = f"SELECT * FROM {table_name} LIMIT 10;\n"
            self.editor.setPlainText(preview_query)
            self.run_current_query()

    def _show_schema_context_menu(self, position):
        item = self.schema_tree.itemAt(position)
        if not item:
            return
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return

        menu = QMenu(self)
        if data.get("type") == "table":
            table_name = data.get("name")
            act_select = menu.addAction(f"SELECT * FROM {table_name} LIMIT 10")
            act_count = menu.addAction(f"SELECT COUNT(*) FROM {table_name}")
            act_copy = menu.addAction("Copy Table Name")

            selected = menu.exec(self.schema_tree.viewport().mapToGlobal(position))
            if selected == act_select:
                self.editor.setPlainText(f"SELECT * FROM {table_name} LIMIT 10;\n")
                self.run_current_query()
            elif selected == act_count:
                self.editor.setPlainText(f"SELECT COUNT(*) AS total_rows FROM {table_name};\n")
                self.run_current_query()
            elif selected == act_copy:
                QApplication.clipboard().setText(table_name)

    def refresh_challenges_list(self):
        """Populates the challenges tree for the active schema."""
        self.challenges_tree.clear()
        schema_key = self.schema_combo.currentData()
        challenges = get_challenges_by_schema(schema_key)

        for ch in challenges:
            item = QTreeWidgetItem([ch["title"], ch["difficulty"]])
            item.setData(0, Qt.ItemDataRole.UserRole, ch)

            # Color difficulty column
            diff = ch["difficulty"]
            if diff == "Easy":
                item.setForeground(1, QColor("#10B981"))
            elif diff == "Medium":
                item.setForeground(1, QColor("#F59E0B"))
            elif diff == "Hard":
                item.setForeground(1, QColor("#EF4444"))

            self.challenges_tree.addTopLevelItem(item)

        self.challenges_tree.resizeColumnToContents(0)

    def _on_challenge_selected(self, item: QTreeWidgetItem, column: int):
        ch = item.data(0, Qt.ItemDataRole.UserRole)
        if not ch:
            return
        self.active_challenge = ch
        self.challenge_title_label.setText(f"🎯 {ch['title']} ({ch['difficulty']})")
        self.challenge_story_text.setPlainText(ch["story"])
        self.challenge_feedback_label.setText("Click 'Verify Solution' when ready to test.")
        self.challenge_feedback_label.setStyleSheet("")
        self.editor.setPlainText(ch["initial_sql"])
        self.bottom_tabs.setCurrentIndex(3)  # Switch to Challenge Details tab

    def _toggle_hint(self):
        if not self.active_challenge:
            return
        hint = self.active_challenge.get("hint", "No hint available.")
        self.challenge_feedback_label.setText(f"💡 Hint: {hint}")
        self.challenge_feedback_label.setStyleSheet(f"color: {self.current_theme.get('accent_warning', '#F59E0B')};")

    def verify_active_challenge(self):
        """Executes the user's current query and compares output with expected solution."""
        if not self.active_challenge:
            self.challenge_feedback_label.setText("Please select a challenge first from the left sidebar.")
            return

        user_sql = self.editor.toPlainText().strip()
        result = verify_challenge_solution(self.engine, user_sql, self.active_challenge)

        if result["passed"]:
            opt_tip = self.active_challenge.get("optimization_tip", "")
            msg = f"🎉 ALL TESTS PASSED! Great job!\n\nExecution Insight: {opt_tip}"
            self.challenge_feedback_label.setText(msg)
            self.challenge_feedback_label.setStyleSheet("color: #10B981; font-weight: bold;")
        else:
            self.challenge_feedback_label.setText(f"❌ Test Failed: {result['error']}")
            self.challenge_feedback_label.setStyleSheet("color: #EF4444; font-weight: bold;")

        # Also display user query results in Tab 1
        if result.get("user_res") and result["user_res"].is_success:
            self._render_query_results(result["user_res"])

    # -------------------------------------------------------------------------
    # Execution & Query Plan Visualizers
    # -------------------------------------------------------------------------

    def run_current_query(self):
        """Executes the query currently typed in the SQL editor."""
        sql_text = self.editor.toPlainText().strip()
        if not sql_text:
            self.results_status_bar.setText("Editor is empty. Write a query to execute.")
            return

        result = self.engine.execute_query(sql_text)
        self._render_query_results(result)
        self.bottom_tabs.setCurrentIndex(0)  # Show Query Results tab

    def _render_query_results(self, result: QueryResult):
        """Renders query result columns and rows into QTableWidget."""
        if not result.is_success:
            self.results_status_bar.setText(f"❌ Error: {result.error}")
            self.results_status_bar.setStyleSheet("color: #EF4444; font-weight: bold;")
            self.results_table.clear()
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            return

        status_text = (
            f"✅ Success • {result.row_count} row(s) returned • "
            f"Executed in {result.execution_time_ms:.2f} ms"
        )
        self.results_status_bar.setText(status_text)
        self.results_status_bar.setStyleSheet(f"color: {self.current_theme.get('syntax_builtin', '#10B981')}; font-weight: bold;")

        self.results_table.clear()
        self.results_table.setColumnCount(len(result.columns))
        self.results_table.setRowCount(len(result.rows))
        self.results_table.setHorizontalHeaderLabels(result.columns)

        for row_idx, row in enumerate(result.rows):
            for col_idx, val in enumerate(row):
                cell_text = str(val) if val is not None else "NULL"
                item = QTableWidgetItem(cell_text)
                if val is None:
                    item.setForeground(QColor("#9CA3AF"))
                    font = item.font()
                    font.setItalic(True)
                    item.setFont(font)
                self.results_table.setItem(row_idx, col_idx, item)

        self.results_table.resizeColumnsToContents()

    def explain_current_query(self):
        """Generates both the physical query plan and logical order of execution."""
        sql_text = self.editor.toPlainText().strip()
        if not sql_text:
            return

        # 1. Physical Query Plan
        plan_nodes = self.engine.get_execution_plan(sql_text)
        self._render_physical_plan(plan_nodes)

        # 2. Logical Order of Execution Pipeline
        logical_steps = self.engine.get_logical_execution_steps(sql_text)
        self._render_logical_steps(logical_steps)

        # Switch to Physical Plan tab
        self.bottom_tabs.setCurrentIndex(1)

    def _render_physical_plan(self, plan_nodes: List[Dict[str, Any]]):
        """Builds clean educational cards for each node in EXPLAIN QUERY PLAN."""
        # Clear existing layout
        while self.plan_content_layout.count():
            item = self.plan_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not plan_nodes:
            label = QLabel("No query plan available for this statement.", self)
            self.plan_content_layout.addWidget(label)
            return

        for node in plan_nodes:
            card = QFrame(self.plan_content_widget)
            card.setFrameShape(QFrame.Shape.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.current_theme.get('bg_card', '#1E202B')};
                    border: 1px solid {self.current_theme.get('border_card', 'rgba(255,255,255,0.08)')};
                    border-radius: 8px;
                    padding: 8px;
                }}
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(10, 8, 10, 8)
            c_layout.setSpacing(4)

            header_row = QHBoxLayout()
            badge_label = QLabel(node["badge"], card)
            badge_label.setFont(QFont("-apple-system", 11, QFont.Weight.Bold))

            # Color badge
            cls = node.get("classification")
            if cls == "SCAN":
                badge_label.setStyleSheet("color: #F59E0B; font-weight: bold;")
            elif cls in ("INDEX_SEARCH", "COVERING_INDEX"):
                badge_label.setStyleSheet("color: #10B981; font-weight: bold;")
            elif cls == "TEMP_BTREE":
                badge_label.setStyleSheet("color: #A855F7; font-weight: bold;")
            else:
                badge_label.setStyleSheet("color: #38BDF8; font-weight: bold;")

            header_row.addWidget(badge_label)
            header_row.addStretch()
            c_layout.addLayout(header_row)

            detail_label = QLabel(f"<strong>Operation:</strong> <code>{node['detail']}</code>", card)
            detail_label.setFont(QFont(get_code_font().family(), 11))
            c_layout.addWidget(detail_label)

            expl_label = QLabel(node["explanation"], card)
            expl_label.setFont(QFont("-apple-system", 11))
            expl_label.setWordWrap(True)
            expl_label.setStyleSheet(f"color: {self.current_theme.get('syntax_comment', '#9CA3AF')};")
            c_layout.addWidget(expl_label)

            self.plan_content_layout.addWidget(card)

        self.plan_content_layout.addStretch()

    def _render_logical_steps(self, logical_steps: List[Dict[str, str]]):
        """Builds step-by-step pipeline cards showing the exact logical order of execution."""
        while self.logical_content_layout.count():
            item = self.logical_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not logical_steps:
            label = QLabel("Write a SELECT query to see the logical order of execution pipeline.", self)
            self.logical_content_layout.addWidget(label)
            return

        for step in logical_steps:
            card = QFrame(self.logical_content_widget)
            card.setFrameShape(QFrame.Shape.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.current_theme.get('bg_card', '#1E202B')};
                    border-left: 4px solid {self.current_theme.get('accent_honey', '#F59E0B')};
                    border-top: 1px solid {self.current_theme.get('border_card', 'rgba(255,255,255,0.08)')};
                    border-right: 1px solid {self.current_theme.get('border_card', 'rgba(255,255,255,0.08)')};
                    border-bottom: 1px solid {self.current_theme.get('border_card', 'rgba(255,255,255,0.08)')};
                    border-radius: 6px;
                    padding: 8px;
                }}
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(10, 8, 10, 8)
            c_layout.setSpacing(4)

            title_row = QHBoxLayout()
            title_lbl = QLabel(f"Stage {step['stage_num']}: {step['title']}", card)
            title_lbl.setFont(QFont("-apple-system", 12, QFont.Weight.Bold))
            title_lbl.setStyleSheet(f"color: {self.current_theme.get('accent_honey', '#F59E0B')};")
            title_row.addWidget(title_lbl)
            title_row.addStretch()
            c_layout.addLayout(title_row)

            desc_lbl = QLabel(step["description"], card)
            desc_lbl.setFont(QFont("-apple-system", 11))
            desc_lbl.setWordWrap(True)
            c_layout.addWidget(desc_lbl)

            if step.get("snippet"):
                snip_lbl = QLabel(f"Query Clause: <code>{step['snippet']}</code>", card)
                snip_lbl.setFont(QFont(get_code_font().family(), 11))
                snip_lbl.setStyleSheet(f"color: {self.current_theme.get('syntax_string', '#34D399')};")
                c_layout.addWidget(snip_lbl)

            self.logical_content_layout.addWidget(card)

        self.logical_content_layout.addStretch()

    def clear_editor(self):
        self.editor.clear()
        self.results_table.clear()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)
        self.results_status_bar.setText("Editor cleared.")

    # -------------------------------------------------------------------------
    # Theme Application
    # -------------------------------------------------------------------------

    def apply_theme(self, theme: Dict[str, Any]):
        self.current_theme = theme
        self.editor.apply_theme(theme)

        # Style toolbar
        self.toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['window_bg']};
                border-bottom: 1px solid {theme['border_color']};
            }}
            QLabel {{
                color: {theme['editor_text']};
            }}
            QComboBox {{
                background-color: {theme['console_bg']};
                color: {theme['editor_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 4px 8px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QPushButton {{
                background-color: {theme['console_bg']};
                color: {theme['editor_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {theme.get('accent_honey', '#F59E0B')};
                color: #111827;
                border-color: {theme.get('accent_honey', '#F59E0B')};
            }}
        """)

        # Style Run button with brand amber accent
        self.run_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F59E0B, stop:1 #D97706);
                color: #FFFFFF;
                border: 1px solid #D97706;
                border-radius: 6px;
                padding: 4px 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: #FBBF24;
                color: #111827;
            }}
        """)

        # Style Sidebar Tabs & Trees
        self.sidebar_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {theme['window_bg']};
            }}
            QTabBar::tab {{
                background: {theme['window_bg']};
                color: {theme['syntax_comment']};
                padding: 8px 14px;
                border: none;
                font-weight: 500;
                font-size: 12px;
            }}
            QTabBar::tab:selected {{
                color: {theme['editor_text']};
                border-bottom: 2px solid {theme.get('accent_honey', '#F59E0B')};
            }}
            QTreeWidget {{
                background-color: {theme['editor_bg']};
                color: {theme['editor_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 4px;
            }}
            QLineEdit {{
                background-color: {theme['editor_bg']};
                color: {theme['editor_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 4px 8px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)

        # Style Bottom Results & Plan Tabs
        self.bottom_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border-top: 1px solid {theme['border_color']};
                background-color: {theme['window_bg']};
            }}
            QTabBar::tab {{
                background: {theme['window_bg']};
                color: {theme['syntax_comment']};
                padding: 8px 14px;
                border: none;
                font-weight: 500;
                font-size: 12px;
            }}
            QTabBar::tab:selected {{
                color: {theme['editor_text']};
                border-bottom: 2px solid {theme.get('accent_honey', '#F59E0B')};
            }}
            QTableWidget {{
                background-color: {theme['editor_bg']};
                color: {theme['editor_text']};
                gridline-color: {theme['border_color']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
            }}
            QHeaderView::section {{
                background-color: {theme['window_bg']};
                color: {theme['editor_text']};
                padding: 5px;
                border: 1px solid {theme['border_color']};
                font-weight: 600;
                font-size: 11px;
            }}
            QTextEdit {{
                background-color: {theme['editor_bg']};
                color: {theme['editor_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 6px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)
