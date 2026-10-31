"""Generates an aesthetic macOS visual installation diagram for Winnie IDE."""

import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import (
    QGuiApplication,
    QImage,
    QPainter,
    QColor,
    QFont,
    QPainterPath,
    QPen,
    QRadialGradient,
    QLinearGradient,
    QPixmap,
)
from PySide6.QtCore import Qt, QRectF, QPointF

app = QGuiApplication([])

def generate_installation_diagram(out_path: str):
    # Dimensions: 2400 x 820 px (Retina 2x resolution)
    width = 2400
    height = 820
    img = QImage(width, height, QImage.Format.Format_ARGB32)
    img.fill(QColor("#08080b"))

    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    # 1. Background
    bg_grad = QLinearGradient(0, 0, width, height)
    bg_grad.setColorAt(0.0, QColor("#0a0a0e"))
    bg_grad.setColorAt(0.5, QColor("#111117"))
    bg_grad.setColorAt(1.0, QColor("#08080c"))
    p.fillRect(0, 0, width, height, bg_grad)

    # Subtle grid dots
    p.setPen(QColor(255, 255, 255, 10))
    for gx in range(40, width, 50):
        for gy in range(40, height, 50):
            p.drawPoint(gx, gy)

    # Top Header
    p.setFont(QFont("Helvetica Neue", 36, QFont.Weight.Bold))
    p.setPen(QColor("#ffffff"))
    p.drawText(80, 80, "Quick macOS Installation")

    p.setFont(QFont("Inter", 18, QFont.Weight.Normal))
    p.setPen(QColor("#a1a1aa"))
    p.drawText(80, 118, "Follow these 4 simple steps to run Winnie natively on your Mac in seconds.")

    # 4 Steps Cards layout
    card_w = 520
    card_h = 580
    card_spacing = 38
    start_x = 80
    start_y = 170

    # Steps definition
    steps = [
        {
            "num": "01",
            "title": "Download Release",
            "subtitle": "Download the latest release archive (Winnie.zip) from GitHub Releases.",
            "color": "#38bdf8",
            "tag": "GitHub Release",
            "action_text": "Winnie.zip",
            "icon_type": "download"
        },
        {
            "num": "02",
            "title": "Extract Archive",
            "subtitle": "Double-click Winnie.zip in Finder to extract the Winnie.app application bundle.",
            "color": "#f59e0b",
            "tag": "Finder Unzip",
            "action_text": "Winnie.app",
            "icon_type": "extract"
        },
        {
            "num": "03",
            "title": "Move to Applications",
            "subtitle": "Drag and drop the extracted Winnie.app bundle into your macOS /Applications folder.",
            "color": "#10b981",
            "tag": "Drag & Drop",
            "action_text": "→  /Applications",
            "icon_type": "app_folder"
        },
        {
            "num": "04",
            "title": "Bypass Gatekeeper",
            "subtitle": "Clear the macOS quarantine attribute so Gatekeeper allows the app to launch.",
            "color": "#c084fc",
            "tag": "Terminal Command",
            "action_text": "xattr -cr ...",
            "icon_type": "terminal"
        }
    ]

    for i, s in enumerate(steps):
        cx = start_x + i * (card_w + card_spacing)
        cy = start_y
        col = QColor(s["color"])

        # Card shadow
        for offset, alpha, blur in [(24, 70, 25), (10, 90, 12)]:
            sh = QPainterPath()
            sh.addRoundedRect(QRectF(cx - blur//2, cy + offset - blur//2, card_w + blur, card_h + blur), 22, 22)
            p.fillPath(sh, QColor(0, 0, 0, alpha))

        # Card body
        card_rect = QRectF(cx, cy, card_w, card_h)
        card_path = QPainterPath()
        card_path.addRoundedRect(card_rect, 20, 20)

        c_grad = QLinearGradient(cx, cy, cx, cy + card_h)
        c_grad.setColorAt(0.0, QColor(25, 25, 32, 220))
        c_grad.setColorAt(1.0, QColor(14, 14, 18, 240))
        p.fillPath(card_path, c_grad)

        # Border with subtle glow
        p.setPen(QPen(QColor(col.red(), col.green(), col.blue(), 90), 1.6))
        p.drawPath(card_path)

        # Step Number Badge
        num_rect = QRectF(cx + 28, cy + 28, 56, 34)
        num_path = QPainterPath()
        num_path.addRoundedRect(num_rect, 10, 10)
        p.fillPath(num_path, QColor(col.red(), col.green(), col.blue(), 35))
        p.setPen(QPen(col, 1.4))
        p.drawPath(num_path)

        p.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        p.setPen(col)
        p.drawText(num_rect, Qt.AlignmentFlag.AlignCenter, s["num"])

        # Category Tag
        p.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        p.setPen(QColor("#71717a"))
        p.drawText(int(cx + 96), int(cy + 50), s["tag"].upper())

        # Step Title
        p.setFont(QFont("Inter", 23, QFont.Weight.Bold))
        p.setPen(QColor("#f4f4f5"))
        p.drawText(int(cx + 28), int(cy + 105), s["title"])

        # Step Subtitle
        p.setFont(QFont("Inter", 15, QFont.Weight.Normal))
        p.setPen(QColor("#a1a1aa"))
        sub_rect = QRectF(cx + 28, cy + 120, card_w - 56, 80)
        p.drawText(sub_rect, Qt.TextFlag.TextWordWrap, s["subtitle"])

        # Visual illustration inside each card
        box_rect = QRectF(cx + 28, cy + 225, card_w - 56, 260)
        box_path = QPainterPath()
        box_path.addRoundedRect(box_rect, 16, 16)
        p.fillPath(box_path, QColor(10, 10, 14, 210))
        p.setPen(QPen(QColor(255, 255, 255, 20), 1.2))
        p.drawPath(box_path)

        # Draw specific visual for step
        if s["icon_type"] == "download":
            # Stylized download file card
            file_box = QRectF(cx + 100, cy + 265, card_w - 200, 130)
            f_path = QPainterPath()
            f_path.addRoundedRect(file_box, 14, 14)
            p.fillPath(f_path, QColor(56, 189, 248, 20))
            p.setPen(QPen(QColor(56, 189, 248, 120), 1.5))
            p.drawPath(f_path)

            # Arrow Down icon
            p.setFont(QFont("Inter", 34, QFont.Weight.Bold))
            p.setPen(QColor("#38bdf8"))
            p.drawText(file_box, Qt.AlignmentFlag.AlignCenter, "↓")

            # File label
            p.setFont(QFont("Dank Mono", 15, QFont.Weight.Bold))
            p.setPen(QColor("#e0f2fe"))
            p.drawText(QRectF(cx + 40, cy + 415, card_w - 80, 40), Qt.AlignmentFlag.AlignCenter, "Winnie-v1.3.3.zip")

        elif s["icon_type"] == "extract":
            # Archive icon -> Winnie.app icon
            zip_box = QRectF(cx + 70, cy + 270, 130, 110)
            zp_path = QPainterPath()
            zp_path.addRoundedRect(zip_box, 12, 12)
            p.fillPath(zp_path, QColor(245, 158, 11, 20))
            p.setPen(QPen(QColor(245, 158, 11, 100), 1.5))
            p.drawPath(zp_path)
            p.setFont(QFont("Dank Mono", 14, QFont.Weight.Bold))
            p.setPen(QColor("#fbbf24"))
            p.drawText(zip_box, Qt.AlignmentFlag.AlignCenter, ".ZIP")

            # Arrow
            p.setFont(QFont("Inter", 24, QFont.Weight.Bold))
            p.setPen(QColor("#71717a"))
            p.drawText(QRectF(cx + 205, cy + 270, 60, 110), Qt.AlignmentFlag.AlignCenter, "→")

            # App Icon
            icon_img = QImage("/Users/nileshhazra/Documents/winnie/Winnie.png")
            if not icon_img.isNull():
                p.drawImage(QRectF(cx + 270, cy + 275, 100, 100), icon_img)

            p.setFont(QFont("Inter", 15, QFont.Weight.Bold))
            p.setPen(QColor("#f4f4f5"))
            p.drawText(QRectF(cx + 40, cy + 415, card_w - 80, 40), Qt.AlignmentFlag.AlignCenter, "Extracted Winnie.app")

        elif s["icon_type"] == "app_folder":
            # Drag Winnie.app -> Applications
            icon_img = QImage("/Users/nileshhazra/Documents/winnie/Winnie.png")
            if not icon_img.isNull():
                p.drawImage(QRectF(cx + 70, cy + 275, 95, 95), icon_img)

            # Curved arrow
            p.setFont(QFont("Inter", 24, QFont.Weight.Bold))
            p.setPen(QColor("#10b981"))
            p.drawText(QRectF(cx + 175, cy + 270, 70, 110), Qt.AlignmentFlag.AlignCenter, "➔")

            # Applications folder box
            app_box = QRectF(cx + 255, cy + 270, 140, 110)
            ab_path = QPainterPath()
            ab_path.addRoundedRect(app_box, 14, 14)
            p.fillPath(ab_path, QColor(16, 185, 129, 20))
            p.setPen(QPen(QColor(16, 185, 129, 120), 1.5))
            p.drawPath(ab_path)

            p.setFont(QFont("Inter", 26, QFont.Weight.Bold))
            p.setPen(QColor("#10b981"))
            p.drawText(QRectF(cx + 255, cy + 280, 140, 50), Qt.AlignmentFlag.AlignCenter, "📁")
            p.setFont(QFont("Inter", 13, QFont.Weight.Bold))
            p.drawText(QRectF(cx + 255, cy + 335, 140, 30), Qt.AlignmentFlag.AlignCenter, "/Applications")

            p.setFont(QFont("Inter", 15, QFont.Weight.Bold))
            p.setPen(QColor("#34d399"))
            p.drawText(QRectF(cx + 40, cy + 415, card_w - 80, 40), Qt.AlignmentFlag.AlignCenter, "Install to Applications")

        elif s["icon_type"] == "terminal":
            # macOS Terminal window mockup
            term_box = QRectF(cx + 45, cy + 250, card_w - 90, 150)
            tb_path = QPainterPath()
            tb_path.addRoundedRect(term_box, 10, 10)
            p.fillPath(tb_path, QColor(18, 18, 22))
            p.setPen(QPen(QColor(192, 132, 252, 100), 1.5))
            p.drawPath(tb_path)

            # Window controls
            for c_idx, c_color in enumerate(["#ef4444", "#f59e0b", "#10b981"]):
                p.setBrush(QColor(c_color))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(int(cx + 60 + c_idx * 16), int(cy + 265), 8, 8)
            p.setBrush(Qt.BrushStyle.NoBrush)

            # Terminal Command line
            p.setFont(QFont("Dank Mono", 13, QFont.Weight.Bold))
            p.setPen(QColor("#c084fc"))
            p.drawText(int(cx + 60), int(cy + 315), "$ ")
            p.setPen(QColor("#f4f4f5"))
            p.drawText(int(cx + 80), int(cy + 315), "xattr -cr /Applications/Winnie.app")

            p.setFont(QFont("Inter", 13, QFont.Weight.Normal))
            p.setPen(QColor("#34d399"))
            p.drawText(int(cx + 60), int(cy + 360), "✓ Clears macOS Gatekeeper quarantine")

            p.setFont(QFont("Inter", 15, QFont.Weight.Bold))
            p.setPen(QColor("#c084fc"))
            p.drawText(QRectF(cx + 40, cy + 415, card_w - 80, 40), Qt.AlignmentFlag.AlignCenter, "Run Once in Terminal")

        # Bottom Action Bar inside card
        act_rect = QRectF(cx + 28, cy + 505, card_w - 56, 46)
        act_path = QPainterPath()
        act_path.addRoundedRect(act_rect, 10, 10)
        p.fillPath(act_path, QColor(255, 255, 255, 8))
        p.setPen(QPen(QColor(255, 255, 255, 18), 1))
        p.drawPath(act_path)

        p.setFont(QFont("Dank Mono", 13, QFont.Weight.DemiBold))
        p.setPen(QColor("#e4e4e7"))
        p.drawText(act_rect, Qt.AlignmentFlag.AlignCenter, s["action_text"])

    p.end()
    img.save(out_path, "PNG")
    print("Generated visual installation diagram at:", out_path)

if __name__ == "__main__":
    out_dir = "/Users/nileshhazra/Documents/winnie/assets"
    brain_dir = "/Users/nileshhazra/.gemini/antigravity/brain/e85ba1b6-97ab-4e32-97cd-9b7c4cad042a"
    
    generate_installation_diagram(os.path.join(out_dir, "installation-guide.png"))
    generate_installation_diagram(os.path.join(brain_dir, "installation_guide.png"))
