"""
SQL Playground UI Widget for Winnie.
Features:
- Multi-schema enterprise database selection (E-Commerce & SaaS, Tech HR, Fintech)
- Interactive Schema Explorer with column definitions, keys, and 1-click sample data previews
- Structured Step-by-Step Learning Plan / Curriculum with code examples and 1-click load into editor
- SQL Editor with syntax highlighting (SqlHighlighter) and execution shortcuts (Cmd+Enter)
- Query Results table with execution metrics (ms, row count)
- Physical Query Plan visualizer (parsing SQLite EXPLAIN QUERY PLAN into Scan vs Index trees)
- Logical Execution Order pipeline (FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT)
- Dynamic Font Zoom (Cmd + =, Cmd + -) across editor, results, and curriculum views
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
from sql_curriculum import (
    SQL_CURRICULUM,
    get_curriculum_modules,
    get_topics_for_module,
    get_topic_by_id,
)
from theme import DARK_THEME, get_scrollbar_stylesheet, get_code_font
from icons import (
    render_svg_icon,
    RUN_SVG,
    CLEAR_SVG,
    DATABASE_SVG,
    LIGHTNING_SVG,
    TABLE_SVG,
    TARGET_SVG,
    FLOW_SVG,
    CHECK_SVG,
    ALERT_SVG,
    INFO_SVG,
    BOOK_SVG,
    COPY_SVG,
)


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
                padding: 10px 14px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.line_number_area.update()


class SqlPlaygroundWidget(QWidget):
    """Complete SQL Playground interface embedded inside Winnie."""

    exit_requested = Signal()
    zoom_in_requested = Signal()
    zoom_out_requested = Signal()
    reset_zoom_requested = Signal()

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.font_size = 13
        self.engine = SqlEngine("ecommerce")
        self.active_topic: Optional[Dict[str, Any]] = None
        self._last_plan_nodes: List[Dict[str, Any]] = []
        self._last_logical_steps: List[Dict[str, str]] = []

        self._init_ui()
        self.apply_theme(self.current_theme)
        self.refresh_schema_browser()
        self.refresh_curriculum_list()

    def _is_light_theme(self) -> bool:
        """Determines if the active theme is light mode."""
        return (
            self.current_theme.get("name") == "light"
            or self.current_theme.get("window_bg", "").upper() in ("#F9F9FB", "#FFFFFF")
        )

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------------------------------------------------------------
        # 1. Top SQL Toolbar
        # ---------------------------------------------------------------------
        self.toolbar = QWidget(self)
        self.toolbar.setFixedHeight(52)
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(16, 8, 16, 8)
        toolbar_layout.setSpacing(12)

        # Schema Selection Dropdown
        schema_label = QLabel("Schema:", self.toolbar)
        schema_label.setFont(QFont("SF Pro Text", 12, QFont.Weight.DemiBold))
        toolbar_layout.addWidget(schema_label)

        self.schema_combo = QComboBox(self.toolbar)
        self.schema_combo.setFixedHeight(32)
        self.schema_combo.setFont(QFont("SF Pro Text", 12))
        for key, info in SqlEngine.SCHEMAS.items():
            self.schema_combo.addItem(render_svg_icon(DATABASE_SVG, size=13, color="#F59E0B"), info["name"], key)
        self.schema_combo.currentIndexChanged.connect(self._on_schema_changed)
        toolbar_layout.addWidget(self.schema_combo)

        toolbar_layout.addSpacing(6)

        # Run Query Button (Primary Action)
        self.run_btn = QPushButton(" Run Query", self.toolbar)
        self.run_btn.setFixedHeight(32)
        self.run_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Bold))
        self.run_btn.setIcon(render_svg_icon(RUN_SVG, size=13, color="#FFFFFF"))
        self.run_btn.setToolTip("Execute SQL query (Cmd+Enter / Ctrl+Enter)")
        self.run_btn.clicked.connect(self.run_current_query)
        toolbar_layout.addWidget(self.run_btn)

        # Explain Plan Button
        self.explain_btn = QPushButton(" Explain Plan", self.toolbar)
        self.explain_btn.setFixedHeight(32)
        self.explain_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Medium))
        self.explain_btn.setIcon(render_svg_icon(LIGHTNING_SVG, size=13, color="#F59E0B"))
        self.explain_btn.setToolTip("Inspect Physical Plan & Execution Order (Cmd+E)")
        self.explain_btn.clicked.connect(self.explain_current_query)
        toolbar_layout.addWidget(self.explain_btn)

        # Reset Database Button
        self.reset_btn = QPushButton("Reset DB", self.toolbar)
        self.reset_btn.setFixedHeight(32)
        self.reset_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Medium))
        self.reset_btn.setToolTip("Restore pristine seed database data")
        self.reset_btn.clicked.connect(self.reset_database)
        toolbar_layout.addWidget(self.reset_btn)

        # Clear Query Button
        self.clear_btn = QPushButton(" Clear", self.toolbar)
        self.clear_btn.setFixedHeight(32)
        self.clear_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Medium))
        self.clear_btn.setIcon(render_svg_icon(CLEAR_SVG, size=13, color="#9CA3AF"))
        self.clear_btn.clicked.connect(lambda: self.editor.clear())
        toolbar_layout.addWidget(self.clear_btn)

        toolbar_layout.addStretch()

        # Switch back to Python IDE Button
        self.exit_btn = QPushButton(" Back to Python IDE", self.toolbar)
        self.exit_btn.setFixedHeight(32)
        self.exit_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Medium))
        self.exit_btn.clicked.connect(self.exit_requested.emit)
        toolbar_layout.addWidget(self.exit_btn)

        main_layout.addWidget(self.toolbar)

        # ---------------------------------------------------------------------
        # 2. Main Workspace Splitter (Left Sidebar vs Right Work Area)
        # ---------------------------------------------------------------------
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.main_splitter.setHandleWidth(1)

        # Left Sidebar Tabs: Schema Explorer & Learning Plan
        self.sidebar_tabs = QTabWidget(self)
        self.sidebar_tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab 1: Database Schema Explorer
        schema_widget = QWidget(self)
        schema_layout = QVBoxLayout(schema_widget)
        schema_layout.setContentsMargins(8, 8, 8, 8)
        schema_layout.setSpacing(6)

        self.schema_filter = QLineEdit(self)
        self.schema_filter.setPlaceholderText("Filter tables & columns...")
        self.schema_filter.textChanged.connect(self._filter_schema_tree)
        schema_layout.addWidget(self.schema_filter)

        self.schema_tree = QTreeWidget(self)
        self.schema_tree.setHeaderHidden(True)
        self.schema_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.schema_tree.itemDoubleClicked.connect(self._on_tree_item_double_clicked)
        self.schema_tree.customContextMenuRequested.connect(self._show_schema_context_menu)
        schema_layout.addWidget(self.schema_tree)

        self.sidebar_tabs.addTab(schema_widget, "Schema")

        # Tab 2: Step-by-Step Learning Plan
        curriculum_widget = QWidget(self)
        curriculum_layout = QVBoxLayout(curriculum_widget)
        curriculum_layout.setContentsMargins(8, 8, 8, 8)
        curriculum_layout.setSpacing(6)

        self.curriculum_filter = QLineEdit(self)
        self.curriculum_filter.setPlaceholderText("Filter learning topics...")
        self.curriculum_filter.textChanged.connect(self._filter_curriculum_tree)
        curriculum_layout.addWidget(self.curriculum_filter)

        # Splitter between topics list and topic detail/action card
        self.curriculum_splitter = QSplitter(Qt.Orientation.Vertical, self)
        self.curriculum_splitter.setHandleWidth(1)

        self.curriculum_tree = QTreeWidget(self)
        self.curriculum_tree.setHeaderLabels(["Curriculum Topics", "Schema"])
        self.curriculum_tree.itemClicked.connect(self._on_topic_selected)
        self.curriculum_splitter.addWidget(self.curriculum_tree)

        # Topic Detail Panel (Scrollable Card)
        self.topic_scroll = QScrollArea(self)
        self.topic_scroll.setWidgetResizable(True)
        self.topic_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.topic_detail_widget = QWidget(self)
        topic_detail_layout = QVBoxLayout(self.topic_detail_widget)
        topic_detail_layout.setContentsMargins(10, 10, 10, 10)
        topic_detail_layout.setSpacing(8)

        # Header: Title + Schema Tag
        self.topic_header_layout = QHBoxLayout()
        self.topic_title_label = QLabel("Select a topic to start learning", self)
        self.topic_title_label.setFont(QFont("-apple-system", 12, QFont.Weight.Bold))
        self.topic_title_label.setWordWrap(True)
        self.topic_header_layout.addWidget(self.topic_title_label, 1)

        self.topic_schema_badge = QLabel("", self)
        self.topic_schema_badge.setFont(QFont("-apple-system", 10, QFont.Weight.DemiBold))
        self.topic_schema_badge.setStyleSheet("""
            background: rgba(245, 158, 11, 0.15);
            color: #F59E0B;
            border-radius: 4px;
            padding: 2px 6px;
        """)
        self.topic_header_layout.addWidget(self.topic_schema_badge)
        topic_detail_layout.addLayout(self.topic_header_layout)

        # Topic summary
        self.topic_summary_label = QLabel("", self)
        self.topic_summary_label.setWordWrap(True)
        self.topic_summary_label.setFont(QFont("-apple-system", 11))
        topic_detail_layout.addWidget(self.topic_summary_label)

        # Key Takeaway Card (Enterprise Production Insight)
        self.topic_takeaway_card = QFrame(self)
        self.topic_takeaway_card.setObjectName("takeawayCard")
        takeaway_layout = QVBoxLayout(self.topic_takeaway_card)
        takeaway_layout.setContentsMargins(8, 8, 8, 8)
        takeaway_layout.setSpacing(4)

        takeaway_title = QLabel("PRODUCTION INSIGHT", self)
        takeaway_title.setFont(QFont("-apple-system", 9, QFont.Weight.Bold))
        takeaway_title.setStyleSheet("color: #F59E0B; letter-spacing: 0.5px;")
        takeaway_layout.addWidget(takeaway_title)

        self.topic_takeaway_text = QLabel("", self)
        self.topic_takeaway_text.setWordWrap(True)
        self.topic_takeaway_text.setFont(QFont("-apple-system", 11))
        takeaway_layout.addWidget(self.topic_takeaway_text)
        topic_detail_layout.addWidget(self.topic_takeaway_card)

        # Action Buttons Row: "Copy to Editor" and "Run Query"
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        self.copy_example_btn = QPushButton(" Copy to Editor", self)
        self.copy_example_btn.setFixedHeight(28)
        self.copy_example_btn.setFont(QFont("-apple-system", 11, QFont.Weight.DemiBold))
        self.copy_example_btn.setIcon(render_svg_icon(COPY_SVG, size=13, color="#FFFFFF"))
        self.copy_example_btn.clicked.connect(self.copy_active_topic_code)
        btn_row.addWidget(self.copy_example_btn)

        self.run_example_btn = QPushButton(" Run Query", self)
        self.run_example_btn.setFixedHeight(28)
        self.run_example_btn.setFont(QFont("-apple-system", 11, QFont.Weight.DemiBold))
        self.run_example_btn.setStyleSheet("""
            QPushButton {
                background: #F59E0B;
                color: #000000;
                font-weight: 600;
                border: none;
                border-radius: 5px;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background: #FBBF24;
            }
        """)
        self.run_example_btn.setIcon(render_svg_icon(RUN_SVG, size=13, color="#000000"))
        self.run_example_btn.clicked.connect(self.run_active_topic_code)
        btn_row.addWidget(self.run_example_btn)

        topic_detail_layout.addLayout(btn_row)

        # Code Example Preview (Read-only styled snippet)
        code_label = QLabel("CODE EXAMPLE", self)
        code_label.setFont(QFont("-apple-system", 9, QFont.Weight.Bold))
        code_label.setStyleSheet("color: #71717A; letter-spacing: 0.5px;")
        topic_detail_layout.addWidget(code_label)

        self.topic_code_preview = QTextEdit(self)
        self.topic_code_preview.setReadOnly(True)
        self.topic_code_preview.setFont(get_code_font(11))
        self.topic_code_preview.setFixedHeight(115)
        topic_detail_layout.addWidget(self.topic_code_preview)

        topic_detail_layout.addStretch()
        self.topic_scroll.setWidget(self.topic_detail_widget)
        self.curriculum_splitter.addWidget(self.topic_scroll)

        self.curriculum_splitter.setSizes([260, 300])
        curriculum_layout.addWidget(self.curriculum_splitter)

        self.sidebar_tabs.addTab(curriculum_widget, "Learning Plan")

        self.main_splitter.addWidget(self.sidebar_tabs)

        # Right Workspace (Editor on Top, Results/Plans Tabs on Bottom)
        self.workspace_splitter = QSplitter(Qt.Orientation.Vertical, self)
        self.workspace_splitter.setHandleWidth(1)

        # SQL Editor
        self.editor = SqlCodeEditor(self, theme=self.current_theme)
        default_welcome_sql = """-- Welcome to Winnie SQL Playground!
-- In-Memory SQLite with rich enterprise schemas.
-- Press Cmd+Enter (Ctrl+Enter) to run queries.

SELECT 
  c.name AS category_name,
  COUNT(p.product_id) AS total_products,
  ROUND(AVG(p.price), 2) AS avg_product_price
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.name
ORDER BY total_products DESC;
"""
        self.editor.setPlainText(default_welcome_sql)
        self.workspace_splitter.addWidget(self.editor)

        # Bottom Dock (Tabs: Results, Physical Plan, Execution Order)
        self.bottom_tabs = QTabWidget(self)
        self.bottom_tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab 1: Query Results
        results_widget = QWidget(self)
        results_layout = QVBoxLayout(results_widget)
        results_layout.setContentsMargins(6, 6, 6, 6)
        results_layout.setSpacing(6)

        self.results_status_bar = QLabel("Ready. Write or select a query to execute.", self)
        self.results_status_bar.setFont(QFont("-apple-system", 11))
        results_layout.addWidget(self.results_status_bar)

        self.results_table = QTableWidget(self)
        self.results_table.setFont(get_code_font(12))
        self.results_table.setAlternatingRowColors(True)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.verticalHeader().setDefaultSectionSize(30)
        self.results_table.verticalHeader().setVisible(False)
        results_layout.addWidget(self.results_table)

        self.bottom_tabs.addTab(results_widget, "Results")

        # Tab 2: Physical Query Plan (Scan vs Index Analysis)
        plan_widget = QWidget(self)
        plan_layout = QVBoxLayout(plan_widget)
        plan_layout.setContentsMargins(10, 10, 10, 10)
        plan_layout.setSpacing(8)

        self.plan_header = QLabel("Physical Query Plan & Optimization Analysis (EXPLAIN QUERY PLAN)", self)
        self.plan_header.setFont(QFont("-apple-system", 12, QFont.Weight.Bold))
        plan_layout.addWidget(self.plan_header)

        self.plan_scroll = QScrollArea(self)
        self.plan_scroll.setWidgetResizable(True)
        self.plan_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.plan_content_widget = QWidget(self)
        self.plan_content_widget.setObjectName("planContentWidget")
        self.plan_content_layout = QVBoxLayout(self.plan_content_widget)
        self.plan_content_layout.setContentsMargins(0, 0, 0, 0)
        self.plan_content_layout.setSpacing(8)
        self.plan_scroll.setWidget(self.plan_content_widget)
        plan_layout.addWidget(self.plan_scroll)

        self.bottom_tabs.addTab(plan_widget, "Physical Plan")

        # Tab 3: Logical Order of Execution Pipeline
        logical_widget = QWidget(self)
        logical_layout = QVBoxLayout(logical_widget)
        logical_layout.setContentsMargins(10, 10, 10, 10)
        logical_layout.setSpacing(8)

        self.logical_header = QLabel("Logical Order of Execution Pipeline", self)
        self.logical_header.setFont(QFont("-apple-system", 12, QFont.Weight.Bold))
        logical_layout.addWidget(self.logical_header)

        self.logical_sub = QLabel(
            "SQL is declarative: while you write SELECT first, the engine evaluates "
            "FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.",
            self
        )
        self.logical_sub.setFont(QFont("-apple-system", 11))
        self.logical_sub.setWordWrap(True)
        logical_layout.addWidget(self.logical_sub)

        self.logical_scroll = QScrollArea(self)
        self.logical_scroll.setWidgetResizable(True)
        self.logical_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.logical_content_widget = QWidget(self)
        self.logical_content_widget.setObjectName("logicalContentWidget")
        self.logical_content_layout = QVBoxLayout(self.logical_content_widget)
        self.logical_content_layout.setContentsMargins(0, 0, 0, 0)
        self.logical_content_layout.setSpacing(8)
        self.logical_scroll.setWidget(self.logical_content_widget)
        logical_layout.addWidget(self.logical_scroll)

        self.bottom_tabs.addTab(logical_widget, "Execution Order")

        self.workspace_splitter.addWidget(self.bottom_tabs)

        # Set split ratios
        self.workspace_splitter.setSizes([320, 280])
        self.main_splitter.addWidget(self.workspace_splitter)
        self.main_splitter.setSizes([260, 740])

        main_layout.addWidget(self.main_splitter)

        # Keyboard shortcuts for Execution
        self.run_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.run_shortcut.activated.connect(self.run_current_query)
        self.run_mac_shortcut = QShortcut(QKeySequence("Meta+Return"), self)
        self.run_mac_shortcut.activated.connect(self.run_current_query)

        self.explain_shortcut = QShortcut(QKeySequence("Meta+E"), self)
        self.explain_shortcut.activated.connect(self.explain_current_query)

        # Keyboard shortcuts for Font Zoom (Cmd+=, Cmd+-, Cmd+0)
        self.shortcut_zoom_in1 = QShortcut(QKeySequence("Ctrl++"), self)
        self.shortcut_zoom_in1.activated.connect(self.zoom_in_requested.emit)
        self.shortcut_zoom_in2 = QShortcut(QKeySequence("Ctrl+="), self)
        self.shortcut_zoom_in2.activated.connect(self.zoom_in_requested.emit)
        self.shortcut_zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        self.shortcut_zoom_out.activated.connect(self.zoom_out_requested.emit)
        self.shortcut_zoom_reset = QShortcut(QKeySequence("Ctrl+0"), self)
        self.shortcut_zoom_reset.activated.connect(self.reset_zoom_requested.emit)

    # -------------------------------------------------------------------------
    # Font Zoom Handling
    # -------------------------------------------------------------------------

    def apply_font_size(self, size: int):
        """Applies dynamic font size across the SQL editor, results table, and curriculum."""
        self.font_size = size

        # 1. Update SQL Editor font & line numbers
        editor_font = get_code_font(size)
        self.editor.setFont(editor_font)
        self.editor.document().setDefaultFont(editor_font)
        self.editor.update_line_number_area_width(0)
        self.editor.line_number_area.update()

        # 2. Update Results Table font
        table_font = get_code_font(max(10, size - 1))
        self.results_table.setFont(table_font)
        self.results_table.horizontalHeader().setFont(table_font)
        self.results_table.resizeRowsToContents()

        # 3. Update Curriculum Code Preview font
        if hasattr(self, "topic_code_preview") and self.topic_code_preview:
            preview_font = get_code_font(max(10, size - 2))
            self.topic_code_preview.setFont(preview_font)

        # 4. Update Schema & Curriculum Tree fonts
        tree_font = QFont("-apple-system", max(10, size - 2))
        self.schema_tree.setFont(tree_font)
        if hasattr(self, "curriculum_tree") and self.curriculum_tree:
            self.curriculum_tree.setFont(tree_font)

    # -------------------------------------------------------------------------
    # Schema Browser Management
    # -------------------------------------------------------------------------

    def _on_schema_changed(self, index: int):
        schema_key = self.schema_combo.currentData()
        self.engine.load_schema(schema_key)
        self.refresh_schema_browser()
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

    # -------------------------------------------------------------------------
    # Curriculum / Learning Plan Management
    # -------------------------------------------------------------------------

    def refresh_curriculum_list(self):
        """Populates the curriculum tree grouped by modules with topics as children."""
        self.curriculum_tree.clear()
        modules = get_curriculum_modules()

        schema_labels = {
            "ecommerce": "E-Commerce",
            "tech_hr": "Tech HR",
            "fintech": "Fintech"
        }

        for module_name in modules:
            mod_item = QTreeWidgetItem([module_name, ""])
            mod_item.setFont(0, QFont("-apple-system", 11, QFont.Weight.Bold))
            mod_item.setFlags(mod_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)

            topics = get_topics_for_module(module_name)
            for t in topics:
                schema_name = schema_labels.get(t.get("schema", ""), "")
                topic_item = QTreeWidgetItem([t["title"], schema_name])
                topic_item.setData(0, Qt.ItemDataRole.UserRole, t["id"])
                topic_item.setFont(0, QFont("-apple-system", 11))
                topic_item.setFont(1, QFont("-apple-system", 10))
                mod_item.addChild(topic_item)

            self.curriculum_tree.addTopLevelItem(mod_item)

        self.curriculum_tree.expandAll()
        self.curriculum_tree.resizeColumnToContents(0)

        # Select first topic by default
        if self.curriculum_tree.topLevelItemCount() > 0:
            first_mod = self.curriculum_tree.topLevelItem(0)
            if first_mod.childCount() > 0:
                first_topic_item = first_mod.child(0)
                self.curriculum_tree.setCurrentItem(first_topic_item)
                self._on_topic_selected(first_topic_item, 0)

    def _filter_curriculum_tree(self, filter_text: str):
        query = filter_text.strip().lower()
        for i in range(self.curriculum_tree.topLevelItemCount()):
            mod_item = self.curriculum_tree.topLevelItem(i)
            mod_match = query in mod_item.text(0).lower()
            any_child_match = False

            for j in range(mod_item.childCount()):
                topic_item = mod_item.child(j)
                topic_match = (
                    query in topic_item.text(0).lower()
                    or query in topic_item.text(1).lower()
                )
                topic_item.setHidden(not (query == "" or topic_match or mod_match))
                if topic_match:
                    any_child_match = True

            mod_item.setHidden(not (query == "" or mod_match or any_child_match))

    def _on_topic_selected(self, item: QTreeWidgetItem, column: int):
        topic_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not topic_id:
            return
        topic = get_topic_by_id(topic_id)
        if not topic:
            return

        self.active_topic = topic
        self.topic_title_label.setText(topic["title"])

        schema_labels = {
            "ecommerce": "E-Commerce & SaaS",
            "tech_hr": "Tech HR",
            "fintech": "Fintech"
        }
        self.topic_schema_badge.setText(schema_labels.get(topic.get("schema", "ecommerce"), "DB"))
        self.topic_summary_label.setText(topic["summary"])
        self.topic_takeaway_text.setText(topic["takeaway"])
        self.topic_code_preview.setPlainText(topic["code_example"])

    def copy_active_topic_code(self):
        """Copies the active topic SQL example into the SQL editor, matching the target schema."""
        if not self.active_topic:
            return

        # Ensure schema matches topic target
        target_schema = self.active_topic.get("schema")
        if target_schema:
            idx = self.schema_combo.findData(target_schema)
            if idx != -1 and idx != self.schema_combo.currentIndex():
                self.schema_combo.setCurrentIndex(idx)

        self.editor.setPlainText(self.active_topic["code_example"])
        self.editor.setFocus()
        self.results_status_bar.setText(
            f"Loaded '{self.active_topic['title']}' example into editor. Press Cmd+Enter to run."
        )

    def run_active_topic_code(self):
        """Loads and immediately executes the active curriculum topic code."""
        self.copy_active_topic_code()
        self.run_current_query()
        self.explain_current_query()

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
            self.results_status_bar.setText(f"Error: {result.error}")
            self.results_status_bar.setStyleSheet("color: #EF4444; font-weight: bold;")
            self.results_table.clear()
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            return

        status_text = (
            f"Success • {result.row_count} row(s) returned • "
            f"Executed in {result.execution_time_ms:.2f} ms"
        )
        self.results_status_bar.setText(status_text)
        self.results_status_bar.setStyleSheet(
            f"color: {self.current_theme.get('syntax_builtin', '#10B981')}; font-weight: bold;"
        )

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
        self._last_plan_nodes = plan_nodes
        self._render_physical_plan(plan_nodes)

        # 2. Logical Order of Execution Pipeline
        logical_steps = self.engine.get_logical_execution_steps(sql_text)
        self._last_logical_steps = logical_steps
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
            label.setStyleSheet(f"color: {self.current_theme['editor_text']};")
            self.plan_content_layout.addWidget(label)
            return

        is_light = self._is_light_theme()
        card_bg = "#FFFFFF" if is_light else self.current_theme.get("table_bg", "#181922")
        card_border = self.current_theme.get("border_color", "#E4E4E7" if is_light else "#27272A")
        text_primary = self.current_theme.get("editor_text", "#18181B" if is_light else "#F4F4F5")
        text_secondary = "#52525B" if is_light else "#A1A1AA"
        code_bg = "#F4F4F5" if is_light else "#111218"

        for node in plan_nodes:
            card = QFrame(self.plan_content_widget)
            card.setFrameShape(QFrame.Shape.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    border: 1px solid {card_border};
                    border-radius: 8px;
                }}
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(12, 10, 12, 10)
            c_layout.setSpacing(6)

            header_row = QHBoxLayout()
            badge_label = QLabel(node["badge"], card)
            badge_label.setFont(QFont("-apple-system", 10, QFont.Weight.Bold))

            # Modern minimal badge tag styling
            cls = node.get("classification")
            if cls == "SCAN":
                badge_style = (
                    "color: #B45309; background-color: #FEF3C7; border: 1px solid #FCD34D;" if is_light
                    else "color: #F59E0B; background-color: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4);"
                )
            elif cls in ("INDEX_SEARCH", "COVERING_INDEX"):
                badge_style = (
                    "color: #047857; background-color: #D1FAE5; border: 1px solid #6EE7B7;" if is_light
                    else "color: #10B981; background-color: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4);"
                )
            elif cls == "TEMP_BTREE":
                badge_style = (
                    "color: #6D28D9; background-color: #EDE9FE; border: 1px solid #C4B5FD;" if is_light
                    else "color: #C084FC; background-color: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.4);"
                )
            elif cls == "ERROR":
                badge_style = (
                    "color: #B91C1C; background-color: #FEE2E2; border: 1px solid #FCA5A5;" if is_light
                    else "color: #EF4444; background-color: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4);"
                )
            else:
                badge_style = (
                    "color: #1D4ED8; background-color: #DBEAFE; border: 1px solid #93C5FD;" if is_light
                    else "color: #38BDF8; background-color: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4);"
                )

            badge_label.setStyleSheet(f"""
                QLabel {{
                    {badge_style}
                    border-radius: 4px;
                    padding: 2px 8px;
                }}
            """)
            header_row.addWidget(badge_label)
            header_row.addStretch()
            c_layout.addLayout(header_row)

            # Raw Detail / Operation
            op_label = QLabel(f"Operation: {node['detail']}", card)
            op_label.setFont(QFont(get_code_font().family(), 11))
            op_label.setStyleSheet(f"""
                QLabel {{
                    color: {text_primary};
                    background-color: {code_bg};
                    padding: 4px 6px;
                    border-radius: 4px;
                }}
            """)
            c_layout.addWidget(op_label)

            # Educational Insight
            tip_label = QLabel(node.get("explanation", node.get("insight", "")), card)
            tip_label.setWordWrap(True)
            tip_label.setFont(QFont("-apple-system", 11))
            tip_label.setStyleSheet(f"color: {text_secondary};")
            c_layout.addWidget(tip_label)

            self.plan_content_layout.addWidget(card)

        self.plan_content_layout.addStretch()

    def _render_logical_steps(self, logical_steps: List[Dict[str, str]]):
        """Builds ordered pipeline flow cards showing stage-by-stage logical execution."""
        # Clear existing layout
        while self.logical_content_layout.count():
            item = self.logical_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not logical_steps:
            label = QLabel("Enter a valid SELECT query to see its logical execution pipeline.", self)
            label.setStyleSheet(f"color: {self.current_theme['editor_text']};")
            self.logical_content_layout.addWidget(label)
            return

        is_light = self._is_light_theme()
        card_bg = "#FFFFFF" if is_light else self.current_theme.get("table_bg", "#181922")
        card_border = self.current_theme.get("border_color", "#E4E4E7" if is_light else "#27272A")
        text_primary = self.current_theme.get("editor_text", "#18181B" if is_light else "#F4F4F5")
        text_secondary = "#52525B" if is_light else "#A1A1AA"
        code_bg = "#F4F4F5" if is_light else "#111218"

        for step in logical_steps:
            card = QFrame(self.logical_content_widget)
            card.setFrameShape(QFrame.Shape.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    border: 1px solid {card_border};
                    border-left: 4px solid #F59E0B;
                    border-radius: 6px;
                }}
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(12, 10, 12, 10)
            c_layout.setSpacing(4)

            # Step Title & Stage
            stage_title = step.get("title") or f"Stage {step.get('stage_num', 1)}: {step.get('keyword', '')}"
            title_label = QLabel(stage_title, card)
            title_label.setFont(QFont("-apple-system", 11, QFont.Weight.Bold))
            title_label.setStyleSheet(f"color: {self.current_theme.get('accent_honey', '#F59E0B')};")
            c_layout.addWidget(title_label)

            # Explanation
            exp_text = step.get("description") or step.get("explanation", "")
            exp_label = QLabel(exp_text, card)
            exp_label.setWordWrap(True)
            exp_label.setFont(QFont("-apple-system", 11))
            exp_label.setStyleSheet(f"color: {text_secondary};")
            c_layout.addWidget(exp_label)

            # Associated Query Clause
            clause_text = step.get("snippet") or step.get("clause", "")
            clause_label = QLabel(f"Query Clause: {clause_text}", card)
            clause_label.setWordWrap(True)
            clause_label.setFont(QFont(get_code_font().family(), 10))
            clause_label.setStyleSheet(f"""
                QLabel {{
                    color: {text_primary};
                    background-color: {code_bg};
                    padding: 4px 6px;
                    border-radius: 4px;
                }}
            """)
            c_layout.addWidget(clause_label)

            self.logical_content_layout.addWidget(card)

        self.logical_content_layout.addStretch()

    # -------------------------------------------------------------------------
    # Theme Application
    # -------------------------------------------------------------------------

    def apply_theme(self, theme):
        self.current_theme = theme
        self.editor.apply_theme(theme)

        # Tab icons styling
        tab_icon_color = "#52525B" if self._is_light_theme() else "#A1A1AA"
        self.sidebar_tabs.setTabIcon(0, render_svg_icon(TABLE_SVG, size=13, color=tab_icon_color))
        self.sidebar_tabs.setTabIcon(1, render_svg_icon(BOOK_SVG, size=13, color=tab_icon_color))

        self.bottom_tabs.setTabIcon(0, render_svg_icon(TABLE_SVG, size=13, color=tab_icon_color))
        self.bottom_tabs.setTabIcon(1, render_svg_icon(LIGHTNING_SVG, size=13, color=tab_icon_color))
        self.bottom_tabs.setTabIcon(2, render_svg_icon(FLOW_SVG, size=13, color=tab_icon_color))

        is_dark = not self._is_light_theme()
        glass_border = theme.get("border_glass", "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(0, 0, 0, 0.08)")
        glass_highlight = theme.get("border_glass_highlight", "rgba(255, 255, 255, 0.16)" if is_dark else "rgba(0, 0, 0, 0.14)")
        glass_hover = theme.get("surface_glass_hover", "rgba(255, 255, 255, 0.09)" if is_dark else "#F0F0F2")
        selected_tab_bg = "rgba(255, 255, 255, 0.08)" if is_dark else "#FFFFFF"
        selected_tab_border = glass_highlight if is_dark else "rgba(0, 0, 0, 0.10)"

        # Style toolbar (Liquid Glass Pill Toolbar)
        self.toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border-bottom: 1px solid {glass_border};
            }}
            QLabel {{
                color: {theme['editor_text']};
            }}
            QComboBox {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['editor_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 16px;
                padding: 4px 14px;
                font-size: 12.5px;
                font-weight: 500;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 16px;
                padding: 6px 16px;
                font-size: 12.5px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
                border: 1px solid {glass_highlight};
                color: #FFFFFF;
            }}
        """)

        # Style Run Query button with luminous amber glass capsule
        if is_dark:
            self.run_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(245, 158, 11, 0.22), stop:1 rgba(217, 119, 6, 0.35));
                    color: #FCD34D;
                    border: 1px solid rgba(251, 191, 36, 0.45);
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-weight: 600;
                    font-size: 12.5px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(245, 158, 11, 0.36), stop:1 rgba(217, 119, 6, 0.50));
                    border: 1px solid rgba(252, 211, 77, 0.70);
                    color: #FFFFFF;
                }
            """)
        else:
            self.run_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F59E0B, stop:1 #D97706);
                    color: #FFFFFF;
                    border: 1px solid #B45309;
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-weight: 600;
                    font-size: 12.5px;
                }
                QPushButton:hover {
                    background: #B45309;
                }
            """)

        # Style Sidebar Tabs & Trees (Floating Glass Tabs)
        self.sidebar_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {glass_border};
                background-color: {theme['editor_bg']};
                border-radius: 12px;
            }}
            QTabBar {{
                qproperty-drawBase: 0;
                background-color: transparent;
                margin-bottom: 6px;
            }}
            QTabBar::tab {{
                background: transparent;
                color: {theme['table_header_text']};
                padding: 6px 16px;
                margin-right: 6px;
                border: 1px solid transparent;
                border-radius: 9px;
                font-weight: 500;
                font-size: 12px;
            }}
            QTabBar::tab:hover {{
                background-color: {glass_hover};
                color: {theme['brand_color']};
            }}
            QTabBar::tab:selected {{
                background-color: {selected_tab_bg};
                color: {theme['brand_color']};
                border: 1px solid {selected_tab_border};
                font-weight: 600;
            }}
            QTreeWidget {{
                background-color: {theme['table_bg']};
                color: {theme['editor_text']};
                border: 1px solid {glass_border};
                border-radius: 10px;
                padding: 6px;
            }}
            QTreeWidget::item {{
                min-height: 28px;
                padding: 4px 8px;
                margin: 2px 2px;
                border-radius: 6px;
            }}
            QTreeWidget::item:hover {{
                background-color: rgba(255, 255, 255, 0.05);
            }}
            QTreeWidget::item:selected {{
                background-color: rgba(255, 255, 255, 0.10);
                border: 1px solid rgba(255, 255, 255, 0.14);
                color: #FFFFFF;
            }}
            QLineEdit {{
                background-color: {theme['console_bg']};
                color: {theme['editor_text']};
                border: 1px solid {glass_border};
                border-radius: 14px;
                padding: 6px 14px;
                font-size: 12px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)

        # Style Bottom Results & Plan Tabs (Floating Glass Tabs)
        self.bottom_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {glass_border};
                background-color: {theme['editor_bg']};
                border-radius: 12px;
            }}
            QTabBar {{
                qproperty-drawBase: 0;
                background-color: transparent;
                margin-bottom: 6px;
            }}
            QTabBar::tab {{
                background: transparent;
                color: {theme['table_header_text']};
                padding: 6px 16px;
                margin-right: 6px;
                border: 1px solid transparent;
                border-radius: 9px;
                font-weight: 500;
                font-size: 12px;
            }}
            QTabBar::tab:hover {{
                background-color: {glass_hover};
                color: {theme['brand_color']};
            }}
            QTabBar::tab:selected {{
                background-color: {selected_tab_bg};
                color: {theme['brand_color']};
                border: 1px solid {selected_tab_border};
                font-weight: 600;
            }}
            QTableWidget {{
                background-color: {theme['table_bg']};
                color: {theme['editor_text']};
                gridline-color: transparent;
                border: 1px solid {glass_border};
                border-radius: 10px;
            }}
            QTableWidget::item {{
                padding: 6px 10px;
            }}
            QHeaderView::section {{
                background-color: {theme['table_header_bg']};
                color: {theme['table_header_text']};
                padding: 8px 10px;
                border: none;
                border-bottom: 1px solid {glass_border};
                font-weight: 600;
                font-size: 11px;
            }}
            QTextEdit {{
                background-color: {theme['table_bg']};
                color: {theme['editor_text']};
                border: 1px solid {glass_border};
                border-radius: 10px;
                padding: 8px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)

        # Update topic takeaway card and code preview styling
        is_light = self._is_light_theme()
        card_border = "#E4E4E7" if is_light else "#27272A"
        preview_bg = "#F4F4F5" if is_light else "#121214"
        text_color = theme['editor_text']
        takeaway_bg = "rgba(245, 158, 11, 0.12)" if is_light else "rgba(245, 158, 11, 0.08)"
        takeaway_border = "#FDE68A" if is_light else "rgba(245, 158, 11, 0.25)"
        takeaway_text = "#78350F" if is_light else "#FDE68A"

        if hasattr(self, "topic_takeaway_card") and self.topic_takeaway_card:
            self.topic_takeaway_card.setStyleSheet(f"""
                QFrame#takeawayCard {{
                    background-color: {takeaway_bg};
                    border: 1px solid {takeaway_border};
                    border-radius: 6px;
                }}
            """)
        if hasattr(self, "topic_takeaway_text") and self.topic_takeaway_text:
            self.topic_takeaway_text.setStyleSheet(f"color: {takeaway_text};")
        if hasattr(self, "topic_code_preview") and self.topic_code_preview:
            self.topic_code_preview.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {preview_bg};
                    color: {text_color};
                    border: 1px solid {card_border};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
        if hasattr(self, "copy_example_btn") and self.copy_example_btn:
            self.copy_example_btn.setIcon(render_svg_icon(COPY_SVG, size=13, color=tab_icon_color))

        # Update plan & execution order header labels
        if hasattr(self, "plan_header") and self.plan_header:
            self.plan_header.setStyleSheet(f"color: {theme['editor_text']};")
        if hasattr(self, "logical_header") and self.logical_header:
            self.logical_header.setStyleSheet(f"color: {theme['editor_text']};")
        if hasattr(self, "logical_sub") and self.logical_sub:
            sub_color = "#52525B" if self._is_light_theme() else "#A1A1AA"
            self.logical_sub.setStyleSheet(f"color: {sub_color};")

        # Scroll areas background & styling
        scroll_style = f"""
            QScrollArea {{
                border: none;
                background-color: {theme['window_bg']};
            }}
            QWidget#planContentWidget, QWidget#logicalContentWidget {{
                background-color: {theme['window_bg']};
            }}
            {get_scrollbar_stylesheet(theme)}
        """
        self.plan_scroll.setStyleSheet(scroll_style)
        self.logical_scroll.setStyleSheet(scroll_style)
        if hasattr(self, "topic_scroll") and self.topic_scroll:
            self.topic_scroll.setStyleSheet(scroll_style)

        # Re-render active cards with the new theme colors if present
        if hasattr(self, "_last_plan_nodes") and self._last_plan_nodes:
            self._render_physical_plan(self._last_plan_nodes)
        if hasattr(self, "_last_logical_steps") and self._last_logical_steps:
            self._render_logical_steps(self._last_logical_steps)
