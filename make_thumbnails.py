"""Refined LinkedIn Featured thumbnails with pixel-perfect margins and dual-deck layout."""

import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import (
    QImage,
    QPainter,
    QPainterPath,
    QColor,
    QFont,
    QLinearGradient,
    QRadialGradient,
    QPen,
    QPixmap,
)
from PySide6.QtCore import Qt, QRectF, QPointF

def create_hero_thumbnail(output_path: str):
    """
    Variant 1: Perfected Modern Hero Showcase
    2400 x 1260 px (Exact 1.91:1 LinkedIn ratio in 2x Retina).
    """
    width = 2400
    height = 1260
    img = QImage(width, height, QImage.Format.Format_ARGB32)
    img.fill(QColor("#08080b"))

    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    # 1. Background Gradients & Ambient Glows
    bg_grad = QLinearGradient(0, 0, width, height)
    bg_grad.setColorAt(0.0, QColor("#08080b"))
    bg_grad.setColorAt(0.4, QColor("#0f0f14"))
    bg_grad.setColorAt(1.0, QColor("#09090d"))
    p.fillRect(0, 0, width, height, bg_grad)

    # Ambient warm honey backlight behind the right window
    amber_glow = QRadialGradient(1620, 620, 750)
    amber_glow.setColorAt(0.0, QColor(245, 158, 11, 48))
    amber_glow.setColorAt(0.35, QColor(217, 119, 6, 22))
    amber_glow.setColorAt(0.75, QColor(16, 185, 129, 12))
    amber_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
    p.fillRect(0, 0, width, height, amber_glow)

    # Ambient emerald glow on left side
    left_glow = QRadialGradient(380, 280, 550)
    left_glow.setColorAt(0.0, QColor(16, 185, 129, 28))
    left_glow.setColorAt(0.5, QColor(16, 185, 129, 8))
    left_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
    p.fillRect(0, 0, width, height, left_glow)

    # Subtle grid lines pattern
    p.setPen(QColor(255, 255, 255, 8))
    grid_spacing = 60
    for x in range(0, width, grid_spacing):
        p.drawLine(x, 0, x, height)
    for y in range(0, height, grid_spacing):
        p.drawLine(0, y, width, y)

    # 2. Right Side: Floating App Window Mockup
    sc_path = "/Users/nileshhazra/Documents/winnie/assets/winnie-dark.png"
    if os.path.exists(sc_path):
        sc_img = QImage(sc_path)
        win_w = 1360
        win_h = int(win_w * (1400 / 2200)) # ~865 px
        win_x = 960
        win_y = (height - win_h) // 2

        # Multi-layer deep drop shadow
        for offset, alpha, blur_expand in [(40, 85, 45), (20, 110, 25), (8, 140, 12)]:
            sh_path = QPainterPath()
            sh_path.addRoundedRect(
                QRectF(win_x - blur_expand // 2, win_y + offset - blur_expand // 2, win_w + blur_expand, win_h + blur_expand),
                26, 26
            )
            p.fillPath(sh_path, QColor(0, 0, 0, alpha))

        # Ambient amber outer contour
        glow_path = QPainterPath()
        glow_path.addRoundedRect(QRectF(win_x - 3, win_y - 3, win_w + 6, win_h + 6), 25, 25)
        p.setPen(QPen(QColor(245, 158, 11, 70), 2))
        p.drawPath(glow_path)

        # Draw rounded clipped window
        win_path = QPainterPath()
        win_path.addRoundedRect(QRectF(win_x, win_y, win_w, win_h), 22, 22)
        p.save()
        p.setClipPath(win_path)
        p.drawImage(QRectF(win_x, win_y, win_w, win_h), sc_img)
        p.restore()

        # Window crisp border
        p.setPen(QPen(QColor(255, 255, 255, 45), 2))
        p.drawPath(win_path)

    # 3. Left Side Content Area
    content_x = 110
    content_y = 150

    # App Icon with ambient backing
    icon_path = "/Users/nileshhazra/Documents/winnie/Winnie.png"
    if os.path.exists(icon_path):
        icon_img = QImage(icon_path)
        icon_size = 124
        
        # Soft shadow behind icon
        icon_shadow = QPainterPath()
        icon_shadow.addRoundedRect(QRectF(content_x - 4, content_y + 10, icon_size + 8, icon_size + 8), 28, 28)
        p.fillPath(icon_shadow, QColor(0, 0, 0, 160))
        
        # Amber icon glow
        icon_glow = QRadialGradient(content_x + icon_size // 2, content_y + icon_size // 2, 110)
        icon_glow.setColorAt(0.0, QColor(245, 158, 11, 120))
        icon_glow.setColorAt(0.5, QColor(217, 119, 6, 40))
        icon_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.fillRect(content_x - 30, content_y - 30, icon_size + 60, icon_size + 60, icon_glow)

        p.drawImage(QRectF(content_x, content_y, icon_size, icon_size), icon_img)

    # Platform & Version Badge Beside Icon
    badge_x = content_x + 155
    badge_y = content_y + 20
    badge_rect = QRectF(badge_x, badge_y, 230, 40)
    badge_path = QPainterPath()
    badge_path.addRoundedRect(badge_rect, 20, 20)
    p.fillPath(badge_path, QColor(245, 158, 11, 28))
    p.setPen(QPen(QColor(245, 158, 11, 180), 1.5))
    p.drawPath(badge_path)

    p.setFont(QFont("Inter", 16, QFont.Weight.Bold))
    p.setPen(QColor("#fbbf24"))
    p.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, "macOS • Python IDE")

    # Author credit pill
    auth_rect = QRectF(badge_x, badge_y + 50, 190, 36)
    auth_path = QPainterPath()
    auth_path.addRoundedRect(auth_rect, 18, 18)
    p.fillPath(auth_path, QColor(255, 255, 255, 14))
    p.setPen(QPen(QColor(255, 255, 255, 30), 1))
    p.drawPath(auth_path)
    p.setFont(QFont("Inter", 14, QFont.Weight.Medium))
    p.setPen(QColor("#a1a1aa"))
    p.drawText(auth_rect, Qt.AlignmentFlag.AlignCenter, "By Nilesh Hazra")

    # Brand Title: "Winnie"
    title_y = content_y + 220
    p.setFont(QFont("Helvetica Neue", 84, QFont.Weight.Bold))
    p.setPen(QColor("#ffffff"))
    p.drawText(content_x, title_y, "Winnie")

    # Tagline / Subtitle
    sub_y = title_y + 64
    p.setFont(QFont("Inter", 30, QFont.Weight.Bold))
    p.setPen(QColor("#e4e4e7"))
    p.drawText(content_x, sub_y, "A Lightweight, Beginner-Friendly")
    p.drawText(content_x, sub_y + 44, "Python IDE for macOS")

    # Value Proposition
    desc_y = sub_y + 115
    p.setFont(QFont("Inter", 20, QFont.Weight.Normal))
    p.setPen(QColor("#a1a1aa"))
    p.drawText(content_x, desc_y, "Intuitive stepping, live scopes, and zero configuration.")
    p.drawText(content_x, desc_y + 32, "Built with native Cocoa styling and process isolation.")

    # 4. Feature Cards
    features = [
        ("🐾 Visual Step Debugger", "Interactive statement-by-statement execution via sys.settrace"),
        ("🧩 58 Built-in Problems", "Graphs, trees, linked lists with Big-O complexity curves"),
        ("⚡ Real-Time Scopes", "Live inspection table for local, global, and loop states"),
        ("📦 Graphical pip Manager", "Search, install, inspect, and remove PyPI packages easily"),
    ]

    card_y = desc_y + 75
    card_w = 780
    card_h = 76
    spacing = 18

    for i, (title, subtitle) in enumerate(features):
        cy = card_y + i * (card_h + spacing)
        card_rect = QRectF(content_x, cy, card_w, card_h)
        card_path = QPainterPath()
        card_path.addRoundedRect(card_rect, 16, 16)

        c_grad = QLinearGradient(content_x, cy, content_x + card_w, cy)
        c_grad.setColorAt(0.0, QColor(255, 255, 255, 16))
        c_grad.setColorAt(1.0, QColor(255, 255, 255, 6))
        p.fillPath(card_path, c_grad)
        p.setPen(QPen(QColor(255, 255, 255, 28), 1.2))
        p.drawPath(card_path)

        p.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        p.setPen(QColor("#f4f4f5"))
        p.drawText(content_x + 22, int(cy) + 33, title)

        p.setFont(QFont("Inter", 16, QFont.Weight.Normal))
        p.setPen(QColor("#a1a1aa"))
        p.drawText(content_x + 22, int(cy) + 60, subtitle)

    # Bottom Pill: Open Source / GitHub
    footer_y = height - 75
    p.setFont(QFont("Inter", 17, QFont.Weight.Medium))
    p.setPen(QColor("#71717a"))
    p.drawText(content_x, footer_y, "Open Source  •  MIT License  •  github.com/nileshhazra/winnie")

    p.end()
    img.save(output_path, "PNG")
    print(f"Created hero thumbnail at {output_path}")


def create_dual_deck_thumbnail(output_path: str):
    """
    Variant 2: Dual Deck Showcase
    Shows the Dark IDE alongside the 58 Built-in Problems / Big-O curve modal in a layered 3D deck.
    """
    width = 2400
    height = 1260
    img = QImage(width, height, QImage.Format.Format_ARGB32)
    img.fill(QColor("#08080b"))

    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    # Background
    bg_grad = QLinearGradient(0, 0, width, height)
    bg_grad.setColorAt(0.0, QColor("#08080b"))
    bg_grad.setColorAt(0.5, QColor("#101016"))
    bg_grad.setColorAt(1.0, QColor("#08080c"))
    p.fillRect(0, 0, width, height, bg_grad)

    # Ambient Glows
    amber_glow = QRadialGradient(1550, 580, 800)
    amber_glow.setColorAt(0.0, QColor(245, 158, 11, 45))
    amber_glow.setColorAt(0.4, QColor(217, 119, 6, 20))
    amber_glow.setColorAt(0.8, QColor(56, 189, 248, 10))
    amber_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
    p.fillRect(0, 0, width, height, amber_glow)

    # Left content
    content_x = 110
    content_y = 160

    icon_path = "/Users/nileshhazra/Documents/winnie/Winnie.png"
    if os.path.exists(icon_path):
        icon_img = QImage(icon_path)
        icon_size = 124
        p.drawImage(QRectF(content_x, content_y, icon_size, icon_size), icon_img)

    badge_x = content_x + 155
    badge_y = content_y + 20
    badge_rect = QRectF(badge_x, badge_y, 230, 40)
    badge_path = QPainterPath()
    badge_path.addRoundedRect(badge_rect, 20, 20)
    p.fillPath(badge_path, QColor(245, 158, 11, 28))
    p.setPen(QPen(QColor(245, 158, 11, 180), 1.5))
    p.drawPath(badge_path)
    p.setFont(QFont("Inter", 16, QFont.Weight.Bold))
    p.setPen(QColor("#fbbf24"))
    p.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, "macOS • Python IDE")

    auth_rect = QRectF(badge_x, badge_y + 50, 190, 36)
    auth_path = QPainterPath()
    auth_path.addRoundedRect(auth_rect, 18, 18)
    p.fillPath(auth_path, QColor(255, 255, 255, 14))
    p.setPen(QPen(QColor(255, 255, 255, 30), 1))
    p.drawPath(auth_path)
    p.setFont(QFont("Inter", 14, QFont.Weight.Medium))
    p.setPen(QColor("#a1a1aa"))
    p.drawText(auth_rect, Qt.AlignmentFlag.AlignCenter, "By Nilesh Hazra")

    title_y = content_y + 220
    p.setFont(QFont("Helvetica Neue", 84, QFont.Weight.Bold))
    p.setPen(QColor("#ffffff"))
    p.drawText(content_x, title_y, "Winnie")

    sub_y = title_y + 64
    p.setFont(QFont("Inter", 30, QFont.Weight.Bold))
    p.setPen(QColor("#e4e4e7"))
    p.drawText(content_x, sub_y, "Learn, Code & Debug")
    p.drawText(content_x, sub_y + 44, "Without the Confusion")

    desc_y = sub_y + 115
    p.setFont(QFont("Inter", 20, QFont.Weight.Normal))
    p.setPen(QColor("#a1a1aa"))
    p.drawText(content_x, desc_y, "A beginner-first Python environment designed for intuitive")
    p.drawText(content_x, desc_y + 32, "comprehension of execution flow, state changes, and algorithms.")

    # 4 Feature Pills
    pills = [
        ("🐾 Visual Step Debugger", "#f59e0b"),
        ("⚡ Live Variables Table", "#38bdf8"),
        ("🧩 58 Practice Problems", "#10b981"),
        ("📈 Big-O Complexity Curves", "#c084fc"),
        ("📦 Built-in pip Manager", "#fbbf24"),
        (" Native macOS Blended UI", "#94a3b8"),
    ]
    pill_start_y = desc_y + 80
    pill_w = 360
    pill_h = 56

    for i, (p_text, p_col) in enumerate(pills):
        col = i % 2
        row = i // 2
        px = content_x + col * (pill_w + 20)
        py = pill_start_y + row * (pill_h + 16)
        
        pr = QRectF(px, py, pill_w, pill_h)
        pp = QPainterPath()
        pp.addRoundedRect(pr, 14, 14)
        p.fillPath(pp, QColor(255, 255, 255, 12))
        p.setPen(QPen(QColor(p_col), 1.5))
        p.drawPath(pp)

        p.setFont(QFont("Inter", 17, QFont.Weight.DemiBold))
        p.setPen(QColor("#f4f4f5"))
        p.drawText(pr, Qt.AlignmentFlag.AlignCenter, p_text)

    footer_y = height - 75
    p.setFont(QFont("Inter", 17, QFont.Weight.Medium))
    p.setPen(QColor("#71717a"))
    p.drawText(content_x, footer_y, "Open Source  •  MIT License  •  github.com/nileshhazra/winnie")

    # Layered Deck on Right Side:
    # 1. Back Layer: Problems Dialog Screenshot
    prob_path = "/Users/nileshhazra/Documents/winnie/assets/winnie-problems.png"
    dark_path = "/Users/nileshhazra/Documents/winnie/assets/winnie-dark.png"

    if os.path.exists(prob_path):
        prob_img = QImage(prob_path)
        pw_w = 1100
        pw_h = int(pw_w * (1400 / 2200)) # ~700 px
        pw_x = 1180
        pw_y = 120

        # Back shadow
        for offset, alpha, blur in [(30, 80, 40), (12, 100, 20)]:
            sh = QPainterPath()
            sh.addRoundedRect(QRectF(pw_x - blur//2, pw_y + offset - blur//2, pw_w + blur, pw_h + blur), 22, 22)
            p.fillPath(sh, QColor(0, 0, 0, alpha))

        # Back window
        p_path = QPainterPath()
        p_path.addRoundedRect(QRectF(pw_x, pw_y, pw_w, pw_h), 20, 20)
        p.save()
        p.setClipPath(p_path)
        p.drawImage(QRectF(pw_x, pw_y, pw_w, pw_h), prob_img)
        # Dim back window slightly
        p.fillRect(QRectF(pw_x, pw_y, pw_w, pw_h), QColor(0, 0, 0, 70))
        p.restore()
        p.setPen(QPen(QColor(255, 255, 255, 30), 1.5))
        p.drawPath(p_path)

    # 2. Front Layer: Main Dark IDE
    if os.path.exists(dark_path):
        dark_img = QImage(dark_path)
        dw_w = 1240
        dw_h = int(dw_w * (1400 / 2200)) # ~789 px
        dw_x = 1040
        dw_y = 360

        # Front heavy shadow
        for offset, alpha, blur in [(45, 110, 50), (22, 130, 25), (10, 160, 12)]:
            sh = QPainterPath()
            sh.addRoundedRect(QRectF(dw_x - blur//2, dw_y + offset - blur//2, dw_w + blur, dw_h + blur), 24, 24)
            p.fillPath(sh, QColor(0, 0, 0, alpha))

        # Ambient glow border
        gw = QPainterPath()
        gw.addRoundedRect(QRectF(dw_x - 3, dw_y - 3, dw_w + 6, dw_h + 6), 23, 23)
        p.setPen(QPen(QColor(245, 158, 11, 75), 2))
        p.drawPath(gw)

        d_path = QPainterPath()
        d_path.addRoundedRect(QRectF(dw_x, dw_y, dw_w, dw_h), 20, 20)
        p.save()
        p.setClipPath(d_path)
        p.drawImage(QRectF(dw_x, dw_y, dw_w, dw_h), dark_img)
        p.restore()
        p.setPen(QPen(QColor(255, 255, 255, 50), 2))
        p.drawPath(d_path)

    p.end()
    img.save(output_path, "PNG")
    print(f"Created dual deck thumbnail at {output_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    out_dir = "/Users/nileshhazra/Documents/winnie/assets"
    brain_dir = "/Users/nileshhazra/.gemini/antigravity/brain/e85ba1b6-97ab-4e32-97cd-9b7c4cad042a"
    
    t1_path = os.path.join(out_dir, "linkedin-featured-thumbnail-hero.png")
    t2_path = os.path.join(out_dir, "linkedin-featured-thumbnail-dual-deck.png")

    create_hero_thumbnail(t1_path)
    create_dual_deck_thumbnail(t2_path)

    create_hero_thumbnail(os.path.join(brain_dir, "linkedin_thumbnail_hero.png"))
    create_dual_deck_thumbnail(os.path.join(brain_dir, "linkedin_thumbnail_dual_deck.png"))
