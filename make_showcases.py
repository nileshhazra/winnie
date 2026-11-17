"""Generates high-resolution showcase preview graphics for Winnie IDE v1.6.0."""

import os
import sys
from PySide6.QtWidgets import QApplication, QTableWidgetItem
from PySide6.QtGui import (
    QImage,
    QPainter,
    QColor,
    QFont,
    QPainterPath,
    QPen,
    QLinearGradient,
    QPixmap,
)
from PySide6.QtCore import Qt, QRectF, QRect

# Add project root to path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from main import WinnieIDE, setup_qt_logging_filter
from theme import DARK_THEME, LIGHT_THEME
from problems import PROBLEMS_DATA
from package_manager import PackageManagerDialog

def frame_showcase(
    raw_img: QImage,
    title: str,
    subtitle: str,
    badges: list,
    output_path: str,
    glow_color: str = "#f59e0b"
):
    """
    Renders a 2400 x 1680 px showcase image with:
    - Elegant dark canvas background (#0d0d13)
    - Bold display title, explanatory subtitle, and feature pill badges
    - Framed 2200 x 1400 px IDE window with realistic drop shadow, rounded corners, and subtle accent glow
    """
    width = 2400
    height = 1680

    img = QImage(width, height, QImage.Format.Format_ARGB32)
    img.fill(QColor("#0d0d13"))

    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    # 1. Subtle Background Depth
    bg_grad = QLinearGradient(0, 0, width, height)
    bg_grad.setColorAt(0.0, QColor("#0f0f15"))
    bg_grad.setColorAt(0.5, QColor("#0c0c11"))
    bg_grad.setColorAt(1.0, QColor("#08080c"))
    p.fillRect(0, 0, width, height, bg_grad)

    # 2. Header Text
    pad_left = 90
    title_y = 100

    # Title
    title_font = QFont(".AppleSystemUIFont", 42, QFont.Weight.Bold)
    p.setFont(title_font)
    p.setPen(QColor("#ffffff"))
    p.drawText(pad_left, title_y, title)

    # Subtitle
    sub_y = title_y + 44
    sub_font = QFont(".AppleSystemUIFont", 18, QFont.Weight.Normal)
    p.setFont(sub_font)
    p.setPen(QColor("#a1a1aa"))
    p.drawText(pad_left, sub_y, subtitle)

    # 3. Badges on the right side
    badge_h = 44
    badge_y = title_y - 36
    curr_right = width - pad_left

    p.setFont(QFont(".AppleSystemUIFont", 15, QFont.Weight.DemiBold))
    for text, b_color in reversed(badges):
        # Measure text width
        metrics = p.fontMetrics()
        text_w = metrics.horizontalAdvance(text)
        badge_w = text_w + 36
        badge_x = curr_right - badge_w

        rect = QRectF(badge_x, badge_y, badge_w, badge_h)
        path = QPainterPath()
        path.addRoundedRect(rect, 22, 22)

        # Tinted background
        col = QColor(b_color)
        bg_col = QColor(col.red(), col.green(), col.blue(), 26)
        p.fillPath(path, bg_col)

        # Border
        p.setPen(QPen(col, 1.5))
        p.drawPath(path)

        # Text
        p.setPen(col)
        p.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        curr_right -= (badge_w + 14)

    # 4. Framed Inner IDE Window
    win_w = 2200
    win_h = 1400
    win_x = (width - win_w) // 2  # 100
    win_y = 185
    win_radius = 22

    # Drop shadows
    for offset, alpha, blur in [(30, 90, 45), (14, 120, 22), (6, 150, 10)]:
        sh_path = QPainterPath()
        sh_path.addRoundedRect(
            QRectF(win_x - blur // 2, win_y + offset - blur // 2, win_w + blur, win_h + blur),
            win_radius + 4,
            win_radius + 4
        )
        p.fillPath(sh_path, QColor(0, 0, 0, alpha))

    # Glow contour
    glow_col = QColor(glow_color)
    glow_path = QPainterPath()
    glow_path.addRoundedRect(QRectF(win_x - 2, win_y - 2, win_w + 4, win_h + 4), win_radius + 1, win_radius + 1)
    p.setPen(QPen(QColor(glow_col.red(), glow_col.green(), glow_col.blue(), 60), 2))
    p.drawPath(glow_path)

    # Rounded Window Image
    win_path = QPainterPath()
    win_path.addRoundedRect(QRectF(win_x, win_y, win_w, win_h), win_radius, win_radius)
    p.save()
    p.setClipPath(win_path)
    p.drawImage(QRectF(win_x, win_y, win_w, win_h), raw_img)
    p.restore()

    # Subtle inner border line
    p.setPen(QPen(QColor(255, 255, 255, 45), 1.5))
    p.drawPath(win_path)

    p.end()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated showcase: {output_path}")

def generate_all():
    setup_qt_logging_filter()
    app = QApplication(['-platform', 'offscreen'])

    assets_dir = os.path.join(ROOT_DIR, "assets")
    docs_assets_dir = os.path.join(ROOT_DIR, "docs", "assets")
    brain_dir = "/Users/nileshhazra/.gemini/antigravity/brain/e85ba1b6-97ab-4e32-97cd-9b7c4cad042a"

    # =========================================================================
    # 1. Dark Mode Showcase (Visual Step Debugger & Scope Inspector)
    # =========================================================================
    print("Capturing 1. Dark Mode...")
    ide_dark = WinnieIDE()
    ide_dark.resize(1100, 700)
    ide_dark.show()
    app.processEvents()

    ide_dark.create_editor_tab(title="utils.py", content="def calculate_total(items):\n    return sum(items)\n\n# Helper utility\n", file_path="/Users/demo/utils.py")
    ide_dark.editor_tabs.setCurrentIndex(0)
    ide_dark.editor.setPlainText(
        "total = 0\n"
        "items = [10, 20, 30]\n\n"
        "for x in items:\n"
        "    total += x\n"
        "    print(f\"Added {x}, running total is {total}\")\n\n"
        "print(\"All done!\")"
    )
    ide_dark.editor.set_debug_line(4)

    ide_dark.variables_view.update_variables([
        {"name": "total", "type": "int", "value": "10"},
        {"name": "items", "type": "list", "value": "[10, 20, 30]"},
        {"name": "x", "type": "int", "value": "10"},
    ])

    ide_dark.console.setPlainText(
        ">>> python main.py\n"
        "Added 10, running total is 10\n"
        "[Paused at line 4 — Click Step (F7) to advance statement]"
    )
    app.processEvents()

    raw_dark = ide_dark.grab().toImage()
    raw_dark.save(os.path.join(assets_dir, "winnie-dark.png"))
    raw_dark.save(os.path.join(docs_assets_dir, "winnie-dark.png"))

    frame_showcase(
        raw_dark,
        title="Visual Step Debugger & Scope Inspector",
        subtitle="Real-time statement-by-statement execution tracking with dynamic variable memory table.",
        badges=[
            ("🐾 Step Engine", "#f59e0b"),
            ("⚡ Live Scopes", "#38bdf8"),
            (" Cocoa Blended UI", "#c084fc")
        ],
        output_path=os.path.join(assets_dir, "winnie-dark-showcase.png"),
        glow_color="#f59e0b"
    )
    raw_dark.save(os.path.join(brain_dir, "winnie_dark_raw.png"))

    # =========================================================================
    # 2. Sliding My Files Drawer Showcase (NEW IN v1.6.0)
    # =========================================================================
    print("Capturing 2. My Files Drawer...")
    ide_dark.open_my_files_drawer()
    ide_dark.files_drawer.animation.stop()
    cw = ide_dark.centralWidget()
    top_offset = ide_dark.top_bar.y() + ide_dark.top_bar.height() + 10
    h = max(200, cw.height() - top_offset - 18)
    ide_dark.files_drawer.setGeometry(QRect(18, top_offset, ide_dark.files_drawer.drawer_width, h))
    app.processEvents()

    raw_files = ide_dark.grab().toImage()
    raw_files.save(os.path.join(assets_dir, "winnie-files.png"))
    raw_files.save(os.path.join(docs_assets_dir, "winnie-files.png"))

    frame_showcase(
        raw_files,
        title="Sliding 'My Files' Drawer & Quick-Save",
        subtitle="Effortless file management with instant ⌘S quick-save, nested folders, and drag-and-drop organization.",
        badges=[
            ("📁 Sliding Drawer", "#f59e0b"),
            ("⚡ Instant ⌘S", "#10b981"),
            ("⇄ Drag & Drop", "#38bdf8")
        ],
        output_path=os.path.join(assets_dir, "winnie-files-showcase.png"),
        glow_color="#f59e0b"
    )
    raw_files.save(os.path.join(brain_dir, "winnie_files_raw.png"))

    # =========================================================================
    # 3. Light Mode Showcase
    # =========================================================================
    print("Capturing 3. Light Mode...")
    ide_light = WinnieIDE()
    ide_light.resize(1100, 700)
    ide_light.apply_theme(LIGHT_THEME)
    ide_light.show()
    app.processEvents()

    ide_light.create_editor_tab(title="model.py", content="# Data model\nclass Item:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n", file_path="/Users/demo/model.py")
    ide_light.editor_tabs.setCurrentIndex(0)
    ide_light.editor.setPlainText(
        "total = 0\n"
        "items = [10, 20, 30]\n\n"
        "for x in items:\n"
        "    total += x\n"
        "    print(f\"Added {x}, running total is {total}\")\n\n"
        "print(\"All done!\")"
    )
    ide_light.variables_view.update_variables([
        {"name": "total", "type": "int", "value": "60"},
        {"name": "items", "type": "list", "value": "[10, 20, 30]"},
        {"name": "x", "type": "int", "value": "30"},
    ])
    ide_light.console.setPlainText(
        ">>> python main.py\n"
        "Added 10, running total is 10\n"
        "Added 20, running total is 30\n"
        "Added 30, running total is 60\n"
        "All done!\n\n"
        "[Program finished with exit code 0]"
    )
    app.processEvents()

    raw_light = ide_light.grab().toImage()
    raw_light.save(os.path.join(assets_dir, "winnie-light.png"))
    raw_light.save(os.path.join(docs_assets_dir, "winnie-light.png"))

    frame_showcase(
        raw_light,
        title="Native macOS Blended Light Mode",
        subtitle="High-contrast, distraction-free daylight theme with full-height Cocoa content view.",
        badges=[
            ("☀️ Light Theme", "#f59e0b"),
            ("⌘ Multi-Tab Editor", "#38bdf8"),
            (" Full-Size View", "#f43f5e")
        ],
        output_path=os.path.join(assets_dir, "winnie-light-showcase.png"),
        glow_color="#38bdf8"
    )
    raw_light.save(os.path.join(brain_dir, "winnie_light_raw.png"))

    # =========================================================================
    # 4. Curated Practice Problems Showcase (160+ Problems)
    # =========================================================================
    print("Capturing 4. Problems Mode...")
    ide_prob = WinnieIDE()
    ide_prob.resize(1100, 700)
    ide_prob.show()
    app.processEvents()

    tree_prob = next((p for p in PROBLEMS_DATA if p["id"] == "how_high"), PROBLEMS_DATA[0])
    ide_prob.load_problem(tree_prob)
    app.processEvents()

    raw_prob = ide_prob.grab().toImage()
    raw_prob.save(os.path.join(assets_dir, "winnie-problems.png"))
    raw_prob.save(os.path.join(docs_assets_dir, "winnie-problems.png"))

    frame_showcase(
        raw_prob,
        title="160+ Curated Practice Problems & Big-O Curves",
        subtitle="Integrated DSA challenges across 18 topics with interactive complexity graphs and reference solutions.",
        badges=[
            ("🧩 160+ Problems", "#10b981"),
            ("📈 Big-O Curves", "#f59e0b"),
            ("🌳 Trees & Graphs", "#38bdf8")
        ],
        output_path=os.path.join(assets_dir, "winnie-problems-showcase.png"),
        glow_color="#10b981"
    )
    raw_prob.save(os.path.join(brain_dir, "winnie_problems_raw.png"))

    # =========================================================================
    # 5. Graphical Package Manager Showcase
    # =========================================================================
    print("Capturing 5. Package Manager...")
    pkg_dlg = PackageManagerDialog(theme=DARK_THEME)
    pkg_dlg.resize(1100, 700)
    sample_pkgs = [
        ("PySide6", "6.7.0"),
        ("requests", "2.31.0"),
        ("numpy", "1.26.4"),
        ("pandas", "2.2.2"),
        ("matplotlib", "3.8.4"),
        ("scipy", "1.13.0"),
        ("torch", "2.3.0"),
        ("pip", "24.0"),
        ("wheel", "0.43.0"),
    ]
    pkg_dlg.table.setRowCount(len(sample_pkgs))
    for r, (pkg, ver) in enumerate(sample_pkgs):
        item_pkg = QTableWidgetItem(f"📦  {pkg}")
        item_ver = QTableWidgetItem(ver)
        pkg_dlg.table.setItem(r, 0, item_pkg)
        pkg_dlg.table.setItem(r, 1, item_ver)

    pkg_dlg.show()
    app.processEvents()

    raw_pkg = pkg_dlg.grab().toImage()
    raw_pkg.save(os.path.join(assets_dir, "winnie-packages.png"))
    raw_pkg.save(os.path.join(docs_assets_dir, "winnie-packages.png"))

    frame_showcase(
        raw_pkg,
        title="Graphical Python Package Manager (pip)",
        subtitle="Search, install, inspect, and remove PyPI packages directly without touching the terminal.",
        badges=[
            ("📦 One-Click Pip", "#f59e0b"),
            ("⚡ Auto-Detect Venv", "#38bdf8"),
            ("🔒 Dependency Safe", "#10b981")
        ],
        output_path=os.path.join(assets_dir, "winnie-packages-showcase.png"),
        glow_color="#c084fc"
    )
    raw_pkg.save(os.path.join(brain_dir, "winnie_packages_raw.png"))

    # Copy all showcases to docs/assets/
    for fname in [
        "winnie-dark-showcase.png",
        "winnie-light-showcase.png",
        "winnie-files-showcase.png",
        "winnie-problems-showcase.png",
        "winnie-packages-showcase.png",
    ]:
        src = os.path.join(assets_dir, fname)
        dst = os.path.join(docs_assets_dir, fname)
        if os.path.exists(src):
            with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                fdst.write(fsrc.read())
            print(f"Synced {fname} to docs/assets/")

    print("\nAll 5 showcase graphics generated & synchronized successfully!")

if __name__ == "__main__":
    generate_all()
