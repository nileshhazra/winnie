import os
import shutil
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
    QHeaderView,
    QMessageBox,
    QFrame,
    QAbstractItemView,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QFont, QColor, QDrag, QPainter, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, Signal, QPropertyAnimation, QEasingCurve, QRect, QPoint, QMimeData, QByteArray

from theme import DARK_THEME, get_ui_font, get_code_font, get_scrollbar_stylesheet
from icons import (
    render_svg_icon,
    render_svg_pixmap,
    FOLDER_SVG,
    FOLDER_PLUS_SVG,
    FILE_SVG,
    CLEAR_SVG,
    CLOSE_SVG,
    SEARCH_SVG,
    CHEVRON_RIGHT_SVG,
    CHEVRON_DOWN_SVG,
)

# Default location for all Winnie saved projects and files
DEFAULT_FILES_DIR = os.path.expanduser("~/Documents/Winnie Files")


def ensure_default_dir() -> str:
    """Ensures ~/Documents/Winnie Files exists on disk."""
    os.makedirs(DEFAULT_FILES_DIR, exist_ok=True)
    return DEFAULT_FILES_DIR


def get_subfolders() -> list[str]:
    """Returns a sorted list of relative subfolder names inside DEFAULT_FILES_DIR."""
    root = ensure_default_dir()
    folders = []
    try:
        for entry in sorted(os.listdir(root)):
            full = os.path.join(root, entry)
            if os.path.isdir(full) and not entry.startswith("."):
                folders.append(entry)
    except Exception:
        pass
    return folders


class QuickSaveDialog(QDialog):
    """A fast, streamlined save dialog asking for the filename and optional folder."""

    def __init__(self, parent=None, suggested_name="", current_theme=DARK_THEME, default_folder=None):
        super().__init__(parent)
        self.current_theme = current_theme
        self.setWindowTitle("Save to Winnie")
        self.setFixedSize(420, 240)
        self.setModal(True)
        self.saved_path = None

        ensure_default_dir()
        folders = get_subfolders()

        # Adjust height if folder dropdown is shown
        if folders:
            self.setFixedSize(420, 275)
        else:
            self.setFixedSize(420, 215)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        # 1. Dialog Header (Icon + Title)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(render_svg_pixmap(FILE_SVG, size=22, color=current_theme.get("brand_color", "#F59E0B")))
        header_layout.addWidget(icon_lbl)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title_lbl = QLabel("Save to Winnie Files")
        title_lbl.setFont(QFont("SF Pro Display", 15, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {current_theme['brand_color']};")
        title_col.addWidget(title_lbl)

        sub_lbl = QLabel("Enter a name for your Python script")
        sub_lbl.setFont(get_ui_font(size=11))
        sub_lbl.setStyleSheet("color: #71717a;")
        title_col.addWidget(sub_lbl)
        header_layout.addLayout(title_col)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # 2. File Name Input
        name_col = QVBoxLayout()
        name_col.setSpacing(6)
        name_lbl = QLabel("File Name:")
        name_lbl.setFont(get_ui_font(size=11, bold=True))
        name_lbl.setStyleSheet(f"color: {current_theme['table_text']};")
        name_col.addWidget(name_lbl)

        self.name_input = QLineEdit()
        self.name_input.setFont(get_ui_font(size=13))
        self.name_input.setPlaceholderText("script.py")

        # Format suggested name
        init_name = suggested_name or "untitled.py"
        if not init_name.endswith(".py"):
            init_name += ".py"
        self.name_input.setText(init_name)

        # Select filename part excluding .py extension for fast typing
        base_stem = init_name[:-3] if init_name.endswith(".py") else init_name
        self.name_input.setSelection(0, len(base_stem))

        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {current_theme.get('input_bg', current_theme['surface_glass'])};
                color: {current_theme['brand_color']};
                border: 1px solid {current_theme['border_glass']};
                border-radius: 9px;
                padding: 7px 10px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {current_theme.get('accent_amber', '#F59E0B')};
            }}
        """)
        name_col.addWidget(self.name_input)
        layout.addLayout(name_col)

        # 3. Folder Dropdown (ONLY shown if user has created at least one folder)
        self.folder_combo = None
        if folders:
            folder_col = QVBoxLayout()
            folder_col.setSpacing(6)
            folder_lbl = QLabel("Folder:")
            folder_lbl.setFont(get_ui_font(size=11, bold=True))
            folder_lbl.setStyleSheet(f"color: {current_theme['table_text']};")
            folder_col.addWidget(folder_lbl)

            self.folder_combo = QComboBox()
            self.folder_combo.setFont(get_ui_font(size=12))
            self.folder_combo.addItem("Root (Winnie Files)", None)
            for f in folders:
                self.folder_combo.addItem(f"📁 {f}", f)

            if default_folder and default_folder in folders:
                idx = self.folder_combo.findData(default_folder)
                if idx >= 0:
                    self.folder_combo.setCurrentIndex(idx)

            self.folder_combo.setStyleSheet(f"""
                QComboBox {{
                    background-color: {current_theme.get('input_bg', current_theme['surface_glass'])};
                    color: {current_theme['brand_color']};
                    border: 1px solid {current_theme['border_glass']};
                    border-radius: 9px;
                    padding: 6px 10px;
                }}
                QComboBox:focus {{
                    border: 1.5px solid {current_theme.get('accent_amber', '#F59E0B')};
                }}
                QComboBox QAbstractItemView {{
                    background-color: {current_theme['window_bg']};
                    color: {current_theme['brand_color']};
                    selection-background-color: {current_theme.get('btn_clear_hover', 'rgba(255,255,255,0.1)')};
                    border: 1px solid {current_theme['border_glass']};
                    border-radius: 8px;
                    padding: 4px;
                }}
            """)
            folder_col.addWidget(self.folder_combo)
            layout.addLayout(folder_col)

        layout.addStretch()

        # 4. Action Buttons (Cancel / Save)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(get_ui_font(size=12))
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme['btn_clear_bg']};
                color: {current_theme['btn_clear_text']};
                border: 1px solid {current_theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {current_theme['btn_clear_hover']};
                color: {current_theme['brand_color']};
            }}
        """)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton("Save File")
        self.save_btn.setFont(get_ui_font(size=12, bold=True))
        self.save_btn.setDefault(True)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme.get('accent_amber', '#F59E0B')};
                color: #111111;
                border: none;
                border-radius: 8px;
                padding: 6px 18px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: #e08e00;
            }}
        """)
        self.save_btn.clicked.connect(self.on_save_clicked)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        # Style entire dialog frame
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {current_theme['window_bg']};
                border: 1px solid {current_theme['border_glass_highlight']};
                border-radius: 14px;
            }}
        """)

    def on_save_clicked(self):
        filename = self.name_input.text().strip()
        if not filename:
            QMessageBox.warning(self, "Invalid Name", "Please enter a valid file name.")
            self.name_input.setFocus()
            return

        # Ensure .py extension
        if not filename.endswith(".py"):
            filename += ".py"

        # Sanitize filename
        clean_name = os.path.basename(filename)

        # Determine target folder
        target_dir = DEFAULT_FILES_DIR
        if self.folder_combo and self.folder_combo.currentData():
            sub = self.folder_combo.currentData()
            target_dir = os.path.join(DEFAULT_FILES_DIR, sub)

        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, clean_name)

        # Check overwrite
        if os.path.exists(target_path):
            res = QMessageBox.question(
                self,
                "File Exists",
                f"A file named '{clean_name}' already exists in this folder.\nDo you want to overwrite it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if res != QMessageBox.StandardButton.Yes:
                return

        self.saved_path = target_path
        self.accept()


class DeleteConfirmDialog(QDialog):
    """A clean confirmation dialog when deleting a file or folder."""

    def __init__(self, parent=None, item_name="", is_folder=False, current_theme=DARK_THEME):
        super().__init__(parent)
        self.setWindowTitle("Confirm Delete")
        self.setFixedSize(400, 180)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        header = QHBoxLayout()
        header.setSpacing(10)
        trash_lbl = QLabel()
        trash_lbl.setPixmap(render_svg_pixmap(CLEAR_SVG, size=24, color="#ef4444"))
        header.addWidget(trash_lbl)

        txt_col = QVBoxLayout()
        txt_col.setSpacing(4)
        t_lbl = QLabel(f"Delete {'folder' if is_folder else 'file'}?")
        t_lbl.setFont(QFont("SF Pro Display", 14, QFont.Weight.Bold))
        t_lbl.setStyleSheet(f"color: {current_theme['brand_color']};")
        txt_col.addWidget(t_lbl)

        desc = QLabel(f"Are you sure you want to delete <b>{item_name}</b>?<br>This action cannot be undone.")
        desc.setFont(get_ui_font(size=11))
        desc.setStyleSheet("color: #71717a;")
        desc.setWordWrap(True)
        txt_col.addWidget(desc)
        header.addLayout(txt_col)
        header.addStretch()
        layout.addLayout(header)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(get_ui_font(size=11))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme['btn_clear_bg']};
                color: {current_theme['btn_clear_text']};
                border: 1px solid {current_theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {current_theme['btn_clear_hover']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        del_btn = QPushButton("Delete")
        del_btn.setFont(get_ui_font(size=11, bold=True))
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet("""
            QPushButton {{
                background-color: #ef4444;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
        """)
        del_btn.clicked.connect(self.accept)
        btn_layout.addWidget(del_btn)

        layout.addLayout(btn_layout)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {current_theme['window_bg']};
                border: 1px solid {current_theme['border_glass_highlight']};
                border-radius: 14px;
            }}
        """)


class NewFolderDialog(QDialog):
    """Dialog to create a new subfolder in Winnie Files."""

    def __init__(self, parent=None, current_theme=DARK_THEME):
        super().__init__(parent)
        self.setWindowTitle("New Folder")
        self.setFixedSize(360, 180)
        self.setModal(True)
        self.folder_name = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(12)

        title = QLabel("Create New Folder")
        title.setFont(QFont("SF Pro Display", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {current_theme['brand_color']};")
        layout.addWidget(title)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Folder name (e.g. Algorithms, Data, Scripts)")
        self.input.setFont(get_ui_font(size=12))
        self.input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {current_theme.get('input_bg', current_theme['surface_glass'])};
                color: {current_theme['brand_color']};
                border: 1px solid {current_theme['border_glass']};
                border-radius: 8px;
                padding: 7px 10px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {current_theme.get('accent_amber', '#F59E0B')};
            }}
        """)
        layout.addWidget(self.input)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(get_ui_font(size=11))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme['btn_clear_bg']};
                color: {current_theme['btn_clear_text']};
                border: 1px solid {current_theme['btn_clear_border']};
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {current_theme['btn_clear_hover']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        create_btn = QPushButton("Create Folder")
        create_btn.setFont(get_ui_font(size=11, bold=True))
        create_btn.setDefault(True)
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme.get('accent_amber', '#F59E0B')};
                color: #111111;
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: #e08e00;
            }}
        """)
        create_btn.clicked.connect(self.on_create)
        btn_layout.addWidget(create_btn)

        layout.addLayout(btn_layout)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {current_theme['window_bg']};
                border: 1px solid {current_theme['border_glass_highlight']};
                border-radius: 14px;
            }}
        """)

    def on_create(self):
        name = self.input.text().strip()
        if not name or any(c in name for c in '/\\:*?"<>|'):
            QMessageBox.warning(self, "Invalid Name", "Folder name cannot be empty or contain special characters.")
            self.input.setFocus()
            return

        target = os.path.join(DEFAULT_FILES_DIR, name)
        if os.path.exists(target):
            QMessageBox.warning(self, "Folder Exists", f"A folder named '{name}' already exists.")
            self.input.setFocus()
            return

        try:
            os.makedirs(target, exist_ok=True)
            self.folder_name = name
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not create folder:\n{e}")


class MyFilesTreeWidget(QTreeWidget):
    """Hierarchical files and folders tree supporting internal drag-and-drop."""

    file_opened = Signal(str)
    file_deleted = Signal(str)
    folder_deleted = Signal(str)
    file_moved = Signal(str, str)  # (old_path, new_path)

    def __init__(self, current_theme=DARK_THEME, parent=None):
        super().__init__(parent)
        self.current_theme = current_theme
        self.setHeaderHidden(True)
        self.setIndentation(14)
        self.setRootIsDecorated(True)
        self.setAnimated(True)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Enable Drag and Drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        self.apply_theme(current_theme)

    def apply_theme(self, theme: dict):
        self.current_theme = theme
        self.setStyleSheet(f"""
            QTreeWidget {{
                background-color: transparent;
                border: none;
                color: {theme['table_text']};
                outline: none;
            }}
            QTreeWidget::item {{
                height: 32px;
                padding: 2px 4px;
                border-radius: 6px;
            }}
            QTreeWidget::item:hover {{
                background-color: {theme.get('surface_glass_hover', 'rgba(255, 255, 255, 0.08)')};
            }}
            QTreeWidget::item:selected {{
                background-color: {theme.get('surface_glass_active', 'rgba(255, 255, 255, 0.12)')};
                color: {theme['brand_color']};
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                border-image: none;
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                border-image: none;
            }}
        """ + get_scrollbar_stylesheet(theme))

    def mimeData(self, items):
        mime = QMimeData()
        if not items:
            return mime
        item = items[0]
        path = item.data(0, Qt.ItemDataRole.UserRole)
        is_folder = item.data(0, Qt.ItemDataRole.UserRole + 1)
        if path and not is_folder:
            mime.setText(path)
            mime.setData("application/x-winnie-file", QByteArray(path.encode("utf-8")))
        return mime

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-winnie-file"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        item = self.itemAt(event.position().toPoint())
        # Target must be a folder item or root area
        if item:
            is_folder = item.data(0, Qt.ItemDataRole.UserRole + 1)
            if is_folder:
                event.acceptProposedAction()
                return
        # Or dropping onto root
        event.acceptProposedAction()

    def dropEvent(self, event):
        src_path = event.mimeData().text()
        if not src_path or not os.path.isfile(src_path):
            event.ignore()
            return

        target_item = self.itemAt(event.position().toPoint())
        target_dir = DEFAULT_FILES_DIR

        if target_item:
            is_folder = target_item.data(0, Qt.ItemDataRole.UserRole + 1)
            target_path = target_item.data(0, Qt.ItemDataRole.UserRole)
            if is_folder and target_path:
                target_dir = target_path
            elif not is_folder and target_path:
                parent_dir = os.path.dirname(target_path)
                if os.path.isdir(parent_dir):
                    target_dir = parent_dir

        filename = os.path.basename(src_path)
        dest_path = os.path.join(target_dir, filename)

        if os.path.abspath(src_path) == os.path.abspath(dest_path):
            event.ignore()
            return

        if os.path.exists(dest_path):
            res = QMessageBox.question(
                self,
                "File Exists",
                f"A file named '{filename}' already exists in '{os.path.basename(target_dir)}'.\nDo you want to replace it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if res != QMessageBox.StandardButton.Yes:
                event.ignore()
                return

        try:
            shutil.move(src_path, dest_path)
            event.acceptProposedAction()
            self.file_moved.emit(src_path, dest_path)
        except Exception as e:
            QMessageBox.critical(self, "Move Failed", f"Could not move file:\n{e}")
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            item = self.currentItem()
            if item:
                path = item.data(0, Qt.ItemDataRole.UserRole)
                is_folder = item.data(0, Qt.ItemDataRole.UserRole + 1)
                if path and not is_folder:
                    self.file_opened.emit(path)
                    event.accept()
                    return
                elif path and is_folder:
                    item.setExpanded(not item.isExpanded())
                    event.accept()
                    return
        super().keyPressEvent(event)


class FileRowWidget(QWidget):
    """Custom widget placed on each file or folder tree row with a delete button."""

    opened = Signal(str)
    delete_clicked = Signal(str, bool)  # (path, is_folder)

    def __init__(self, name: str, path: str, is_folder: bool = False, count: int = 0, current_theme: dict = DARK_THEME, parent=None):
        super().__init__(parent)
        self.path = path
        self.is_folder = is_folder
        self.current_theme = current_theme
        self.setMouseTracking(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(8)

        # Icon
        self.icon_lbl = QLabel()
        self.icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        if is_folder:
            self.icon_lbl.setPixmap(render_svg_pixmap(FOLDER_SVG, size=14, color=current_theme.get("accent_amber", "#F59E0B")))
        else:
            self.icon_lbl.setPixmap(render_svg_pixmap(FILE_SVG, size=13, color=current_theme.get("syntax_keyword", "#C678DD")))
        layout.addWidget(self.icon_lbl)

        # Name label
        self.name_lbl = QLabel(name)
        self.name_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.name_lbl.setFont(get_ui_font(size=12, bold=is_folder))
        self.name_lbl.setStyleSheet(f"color: {current_theme['table_text']};")
        layout.addWidget(self.name_lbl)

        if is_folder and count > 0:
            count_lbl = QLabel(f"({count})")
            count_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            count_lbl.setFont(get_ui_font(size=10))
            count_lbl.setStyleSheet("color: #71717a;")
            layout.addWidget(count_lbl)

        layout.addStretch()

        # Delete Button (hidden until hover, or visible on hover)
        self.del_btn = QPushButton()
        self.del_btn.setIcon(render_svg_icon(CLEAR_SVG, size=12, color="#71717a"))
        self.del_btn.setIconSize(QSize(12, 12))
        self.del_btn.setFixedSize(22, 22)
        self.del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.del_btn.setToolTip(f"Delete {'folder' if is_folder else 'file'}")
        self.del_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: rgba(239, 68, 68, 0.20);
            }
        """)
        self.del_btn.clicked.connect(self.on_delete)
        layout.addWidget(self.del_btn)

    def on_delete(self):
        self.delete_clicked.emit(self.path, self.is_folder)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton) or self.is_folder:
            super().mouseMoveEvent(event)
            return

        if hasattr(self, "drag_start_pos"):
            distance = (event.position().toPoint() - self.drag_start_pos).manhattanLength()
            if distance >= QApplication.startDragDistance():
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText(self.path)
                mime.setData("application/x-winnie-file", QByteArray(self.path.encode("utf-8")))
                drag.setMimeData(mime)

                pixmap = self.grab()
                drag.setPixmap(pixmap)
                drag.setHotSpot(event.position().toPoint())
                if hasattr(self, "drag_start_pos"):
                    del self.drag_start_pos
                drag.exec(Qt.DropAction.MoveAction)
                return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "drag_start_pos"):
            del self.drag_start_pos
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if not self.is_folder:
            self.opened.emit(self.path)
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)


class MyFilesBackdrop(QWidget):
    """Semi-transparent backdrop scrim that closes the files drawer when clicked."""
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()

    def mousePressEvent(self, event):
        self.clicked.emit()
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 75))
        painter.end()


class MyFilesOverlayDrawer(QFrame):
    """A sleek, animated sliding overlay drawer that slides from the side displaying user files."""

    file_selected = Signal(str)
    file_deleted = Signal(str)
    file_moved = Signal(str, str)

    def __init__(self, parent=None, current_theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = current_theme
        self.drawer_width = 320
        self.is_open = False

        # Set up frame styling
        self.setObjectName("myFilesDrawer")
        self.apply_theme(current_theme)

        # Drop shadow for depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setColor(QColor(0, 0, 0, 140))
        shadow.setOffset(4, 4)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # 1. Header (My Files + New Folder + Close)
        header = QHBoxLayout()
        header.setSpacing(8)

        self.icon_lbl = QLabel()
        self.icon_lbl.setPixmap(render_svg_pixmap(FOLDER_SVG, size=18, color=current_theme.get("accent_amber", "#F59E0B")))
        header.addWidget(self.icon_lbl)

        self.title_lbl = QLabel("My Files")
        self.title_lbl.setFont(QFont("SF Pro Display", 14, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet(f"color: {current_theme['brand_color']};")
        header.addWidget(self.title_lbl)

        header.addStretch()

        # + Folder button
        self.add_folder_btn = QPushButton("+ Folder")
        self.add_folder_btn.setToolTip("Create New Folder")
        self.add_folder_btn.setFont(get_ui_font(size=11, bold=True))
        self.add_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_folder_btn.setIcon(render_svg_icon(FOLDER_PLUS_SVG, size=12, color=current_theme['btn_clear_text']))
        self.add_folder_btn.setIconSize(QSize(12, 12))
        self.add_folder_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme['btn_clear_bg']};
                color: {current_theme['btn_clear_text']};
                border: 1px solid {current_theme['btn_clear_border']};
                border-radius: 7px;
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {current_theme['btn_clear_hover']};
                color: {current_theme['brand_color']};
            }}
        """)
        self.add_folder_btn.clicked.connect(self.prompt_new_folder)
        header.addWidget(self.add_folder_btn)

        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(render_svg_icon(CLOSE_SVG, size=11, color=current_theme['btn_clear_text']))
        self.close_btn.setIconSize(QSize(11, 11))
        self.close_btn.setFixedSize(26, 26)
        self.close_btn.setToolTip("Close Files Drawer (Esc)")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme['btn_clear_bg']};
                border: 1px solid {current_theme['btn_clear_border']};
                border-radius: 7px;
            }}
            QPushButton:hover {{
                background-color: {current_theme['btn_clear_hover']};
            }}
        """)
        self.close_btn.clicked.connect(self.close_drawer)
        header.addWidget(self.close_btn)

        layout.addLayout(header)

        # 2. Filter / Search Bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(6)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter files...")
        self.search_input.setFont(get_ui_font(size=11))
        self.search_input.textChanged.connect(self.filter_tree)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {current_theme.get('input_bg', current_theme['surface_glass'])};
                color: {current_theme['brand_color']};
                border: 1px solid {current_theme['border_glass']};
                border-radius: 7px;
                padding: 5px 8px;
            }}
            QLineEdit:focus {{
                border: 1px solid {current_theme.get('accent_amber', '#F59E0B')};
            }}
        """)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # 3. File Tree Widget
        self.tree = MyFilesTreeWidget(current_theme=current_theme, parent=self)
        self.tree.file_opened.connect(self.file_selected.emit)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.file_moved.connect(self.on_file_moved)
        layout.addWidget(self.tree, 1)

        # 4. Empty State Placeholder
        self.empty_lbl = QLabel("No saved files yet\nPress ⌘S to save a file here")
        self.empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_lbl.setFont(get_ui_font(size=11))
        self.empty_lbl.setStyleSheet("color: #71717a; padding: 24px;")
        layout.addWidget(self.empty_lbl)
        self.empty_lbl.hide()

        # 5. Bottom hint
        self.hint_lbl = QLabel("Drag files onto folders to organize")
        self.hint_lbl.setFont(get_ui_font(size=10))
        self.hint_lbl.setStyleSheet("color: #52525b;")
        self.hint_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hint_lbl)

        # Slide animation setup
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(220)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.on_animation_finished)

        # Initial hidden state
        self.hide()

    def apply_theme(self, theme: dict):
        self.current_theme = theme
        is_dark = theme.get("name") == "dark"
        bg_color = "rgba(20, 20, 22, 0.96)" if is_dark else "rgba(255, 255, 255, 0.98)"
        border_col = theme.get("border_glass_highlight", "rgba(255, 255, 255, 0.15)" if is_dark else "rgba(0, 0, 0, 0.12)")
        self.setStyleSheet(f"""
            QFrame#myFilesDrawer {{
                background-color: {bg_color};
                border: 1px solid {border_col};
                border-radius: 12px;
            }}
        """)
        if hasattr(self, "title_lbl"):
            self.title_lbl.setStyleSheet(f"color: {theme['brand_color']};")
        if hasattr(self, "icon_lbl"):
            self.icon_lbl.setPixmap(render_svg_pixmap(FOLDER_SVG, size=18, color=theme.get("accent_amber", "#F59E0B")))
        if hasattr(self, "add_folder_btn"):
            self.add_folder_btn.setIcon(render_svg_icon(FOLDER_PLUS_SVG, size=12, color=theme['btn_clear_text']))
            self.add_folder_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme['btn_clear_bg']};
                    color: {theme['btn_clear_text']};
                    border: 1px solid {theme['btn_clear_border']};
                    border-radius: 7px;
                    padding: 4px 8px;
                }}
                QPushButton:hover {{
                    background-color: {theme['btn_clear_hover']};
                    color: {theme['brand_color']};
                }}
            """)
        if hasattr(self, "close_btn"):
            self.close_btn.setIcon(render_svg_icon(CLOSE_SVG, size=11, color=theme['btn_clear_text']))
            self.close_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme['btn_clear_bg']};
                    border: 1px solid {theme['btn_clear_border']};
                    border-radius: 7px;
                }}
                QPushButton:hover {{
                    background-color: {theme['btn_clear_hover']};
                }}
            """)
        if hasattr(self, "search_input"):
            input_bg = theme.get('input_bg', 'rgba(255, 255, 255, 0.05)' if is_dark else '#F3F4F6')
            self.search_input.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {input_bg};
                    color: {theme['brand_color']};
                    border: 1px solid {theme['border_glass']};
                    border-radius: 7px;
                    padding: 5px 8px;
                }}
                QLineEdit:focus {{
                    border: 1px solid {theme.get('accent_amber', '#F59E0B')};
                }}
            """)
        if hasattr(self, "hint_lbl"):
            self.hint_lbl.setStyleSheet("color: #52525b;" if is_dark else "color: #9ca3af;")
        if hasattr(self, "tree"):
            self.tree.apply_theme(theme)
            self.refresh_files()

    def refresh_files(self):
        """Scans DEFAULT_FILES_DIR and builds the tree hierarchy."""
        root = ensure_default_dir()
        self.tree.clear()

        has_any_item = False
        search_filter = self.search_input.text().strip().lower()

        try:
            entries = sorted(os.listdir(root))
        except Exception:
            entries = []

        # 1. Subfolders
        folders = [e for e in entries if os.path.isdir(os.path.join(root, e)) and not e.startswith(".")]
        for folder_name in folders:
            folder_path = os.path.join(root, folder_name)
            try:
                sub_entries = sorted(os.listdir(folder_path))
            except Exception:
                sub_entries = []

            files_in_folder = [f for f in sub_entries if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith(".")]

            # If search filter is active, check if folder or any file matches
            matched_files = [f for f in files_in_folder if (not search_filter or search_filter in f.lower() or search_filter in folder_name.lower())]

            if search_filter and not matched_files and search_filter not in folder_name.lower():
                continue

            has_any_item = True
            folder_item = QTreeWidgetItem(self.tree)
            folder_item.setData(0, Qt.ItemDataRole.UserRole, folder_path)
            folder_item.setData(0, Qt.ItemDataRole.UserRole + 1, True)  # is_folder = True
            folder_item.setFlags(folder_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)

            folder_widget = FileRowWidget(
                name=folder_name,
                path=folder_path,
                is_folder=True,
                count=len(files_in_folder),
                current_theme=self.current_theme,
                parent=self.tree,
            )
            folder_widget.delete_clicked.connect(self.on_delete_requested)
            self.tree.setItemWidget(folder_item, 0, folder_widget)
            folder_item.setExpanded(True)

            for file_name in matched_files:
                file_path = os.path.join(folder_path, file_name)
                child_item = QTreeWidgetItem(folder_item)
                child_item.setData(0, Qt.ItemDataRole.UserRole, file_path)
                child_item.setData(0, Qt.ItemDataRole.UserRole + 1, False)
                child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsDragEnabled)

                file_widget = FileRowWidget(
                    name=file_name,
                    path=file_path,
                    is_folder=False,
                    current_theme=self.current_theme,
                    parent=self.tree,
                )
                file_widget.opened.connect(self.file_selected.emit)
                file_widget.delete_clicked.connect(self.on_delete_requested)
                self.tree.setItemWidget(child_item, 0, file_widget)

        # 2. Root files
        root_files = [e for e in entries if os.path.isfile(os.path.join(root, e)) and not e.startswith(".")]
        for file_name in root_files:
            if search_filter and search_filter not in file_name.lower():
                continue
            has_any_item = True
            file_path = os.path.join(root, file_name)

            root_item = QTreeWidgetItem(self.tree)
            root_item.setData(0, Qt.ItemDataRole.UserRole, file_path)
            root_item.setData(0, Qt.ItemDataRole.UserRole + 1, False)
            root_item.setFlags(root_item.flags() | Qt.ItemFlag.ItemIsDragEnabled)

            file_widget = FileRowWidget(
                name=file_name,
                path=file_path,
                is_folder=False,
                current_theme=self.current_theme,
                parent=self.tree,
            )
            file_widget.opened.connect(self.file_selected.emit)
            file_widget.delete_clicked.connect(self.on_delete_requested)
            self.tree.setItemWidget(root_item, 0, file_widget)

        if has_any_item:
            self.tree.show()
            self.empty_lbl.hide()
        else:
            self.tree.hide()
            self.empty_lbl.show()

    def filter_tree(self, text: str):
        self.refresh_files()

    def prompt_new_folder(self):
        dlg = NewFolderDialog(self, current_theme=self.current_theme)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.refresh_files()

    def on_delete_requested(self, path: str, is_folder: bool):
        name = os.path.basename(path)
        dlg = DeleteConfirmDialog(self, item_name=name, is_folder=is_folder, current_theme=self.current_theme)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            try:
                if is_folder:
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                    self.file_deleted.emit(path)
                self.refresh_files()
            except Exception as e:
                QMessageBox.critical(self, "Delete Error", f"Could not delete:\n{e}")

    def on_item_double_clicked(self, item, column):
        path = item.data(0, Qt.ItemDataRole.UserRole)
        is_folder = item.data(0, Qt.ItemDataRole.UserRole + 1)
        if path and not is_folder:
            self.file_selected.emit(path)

    def on_file_moved(self, old_path: str, new_path: str):
        self.refresh_files()
        self.file_moved.emit(old_path, new_path)

    def open_drawer(self, top_offset: int, height: int):
        """Slides drawer in from left edge."""
        self.refresh_files()
        self.show()
        self.raise_()
        self.is_open = True

        start_rect = QRect(-self.drawer_width - 10, top_offset, self.drawer_width, height)
        end_rect = QRect(18, top_offset, self.drawer_width, height)

        self.setGeometry(start_rect)
        self.animation.stop()
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

    def close_drawer(self):
        """Slides drawer out to left edge."""
        if not self.is_open:
            return
        self.is_open = False
        curr_rect = self.geometry()
        end_rect = QRect(-self.drawer_width - 15, curr_rect.y(), self.drawer_width, curr_rect.height())

        self.animation.stop()
        self.animation.setStartValue(curr_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

    def toggle_drawer(self, top_offset: int, height: int):
        if self.is_open:
            self.close_drawer()
        else:
            self.open_drawer(top_offset, height)

    def on_animation_finished(self):
        if not self.is_open:
            self.hide()
