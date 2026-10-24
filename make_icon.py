import os
import subprocess
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QColor,
    QPainterPath,
    QLinearGradient,
    QRadialGradient,
    QPen,
)
from PySide6.QtCore import Qt, QRectF, QPointF

app = QApplication([])


def draw_liquid_glass_blue_icon(size: int) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    # Apple macOS Squircle Dimensions (Standard 82.4% footprint)
    tile_size = size * 0.824
    margin = (size - tile_size) / 2
    radius = tile_size * 0.225
    rect = QRectF(margin, margin, tile_size, tile_size)

    # 1. Multi-Layered Soft Ambient Drop Shadow
    for i in range(1, 6):
        shadow_path = QPainterPath()
        shadow_rect = QRectF(margin, margin + (i * size * 0.012), tile_size, tile_size)
        shadow_path.addRoundedRect(shadow_rect, radius, radius)
        alpha = int(50 / i)
        painter.fillPath(shadow_path, QColor(0, 0, 0, alpha))

    # 2. Main Squircle Base Path
    tile_path = QPainterPath()
    tile_path.addRoundedRect(rect, radius, radius)

    # 3. Deep Midnight-Obsidian Frosted Glass Gradient (Deep Black/Blue)
    bg_grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
    bg_grad.setColorAt(0.0, QColor("#111827"))  # Deep midnight slate
    bg_grad.setColorAt(0.45, QColor("#080c14")) # Obsidian
    bg_grad.setColorAt(1.0, QColor("#020408"))  # Pitch black
    painter.fillPath(tile_path, bg_grad)

    # 4. Internal "Liquid Neon" Aurora Glow (Sapphire & Electric Blue trapped in glass)
    painter.save()
    painter.setClipPath(tile_path)

    # Sapphire / Cobalt Radiant Core
    glow1 = QRadialGradient(rect.center().x() - tile_size * 0.1, rect.center().y() + tile_size * 0.08, tile_size * 0.6)
    glow1.setColorAt(0.0, QColor(37, 99, 235, 150))   # Vibrant Electric Blue
    glow1.setColorAt(0.55, QColor(56, 189, 248, 70))  # Sky Cyan
    glow1.setColorAt(1.0, QColor(0, 0, 0, 0))
    painter.fillRect(rect, glow1)

    # Deep Indigo / Royal Blue Ambient Accent (Top Right)
    glow2 = QRadialGradient(rect.topRight().x() - tile_size * 0.1, rect.topRight().y() + tile_size * 0.1, tile_size * 0.5)
    glow2.setColorAt(0.0, QColor(30, 58, 138, 90))
    glow2.setColorAt(1.0, QColor(0, 0, 0, 0))
    painter.fillRect(rect, glow2)

    # 5. Top Glass Specular Arc Reflection (Frosted Glass Sheen)
    sheen_path = QPainterPath()
    sheen_rect = QRectF(rect.left() - tile_size * 0.2, rect.top() - tile_size * 0.3, tile_size * 1.4, tile_size * 0.85)
    sheen_path.addEllipse(sheen_rect)

    sheen_grad = QLinearGradient(rect.topLeft(), rect.center())
    sheen_grad.setColorAt(0.0, QColor(255, 255, 255, 45))
    sheen_grad.setColorAt(0.6, QColor(255, 255, 255, 10))
    sheen_grad.setColorAt(1.0, QColor(255, 255, 255, 0))
    painter.fillPath(sheen_path, sheen_grad)

    painter.restore()

    # 6. Glass Refraction Rim Bevel (Light hitting the top-left edge)
    bevel_pen = QPen()
    bevel_pen.setWidthF(max(1.0, size * 0.0035))
    bevel_grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
    bevel_grad.setColorAt(0.0, QColor(255, 255, 255, 140))
    bevel_grad.setColorAt(0.5, QColor(255, 255, 255, 40))
    bevel_grad.setColorAt(1.0, QColor(255, 255, 255, 12))
    bevel_pen.setBrush(bevel_grad)
    painter.strokePath(tile_path, bevel_pen)

    # 7. Centerpiece: Illuminated Glass Terminal Glyph `> _` (Electric Blue / Ice Cyan)
    center_x = rect.center().x()
    center_y = rect.center().y()
    scale = tile_size / 200.0

    glyph_pen = QPen()
    glyph_pen.setWidthF(max(2.0, 16.0 * scale))
    glyph_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    glyph_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

    # Gradient for the Glyph
    symbol_grad = QLinearGradient(
        QPointF(center_x - 45 * scale, center_y - 40 * scale),
        QPointF(center_x + 45 * scale, center_y + 40 * scale)
    )
    symbol_grad.setColorAt(0.0, QColor("#60a5fa"))  # Ice Blue
    symbol_grad.setColorAt(1.0, QColor("#38bdf8"))  # Sky Cyan
    glyph_pen.setBrush(symbol_grad)
    painter.setPen(glyph_pen)

    # Chevron `>`
    chevron = QPainterPath()
    chevron.moveTo(center_x - 45 * scale, center_y - 30 * scale)
    chevron.lineTo(center_x - 15 * scale, center_y)
    chevron.lineTo(center_x - 45 * scale, center_y + 30 * scale)
    painter.drawPath(chevron)

    # Underscore `_`
    cursor_line = QPainterPath()
    cursor_line.moveTo(center_x + 5 * scale, center_y + 30 * scale)
    cursor_line.lineTo(center_x + 45 * scale, center_y + 30 * scale)
    painter.drawPath(cursor_line)

    painter.end()
    return pixmap


def create_mac_icon():
    iconset_dir = "Winnie.iconset"
    os.makedirs(iconset_dir, exist_ok=True)

    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        pix = draw_liquid_glass_blue_icon(size)

        if size == 16:
            pix.save(f"{iconset_dir}/icon_16x16.png")
        elif size == 32:
            pix.save(f"{iconset_dir}/icon_16x16@2x.png")
            pix.save(f"{iconset_dir}/icon_32x32.png")
        elif size == 64:
            pix.save(f"{iconset_dir}/icon_32x32@2x.png")
        elif size == 128:
            pix.save(f"{iconset_dir}/icon_128x128.png")
        elif size == 256:
            pix.save(f"{iconset_dir}/icon_128x128@2x.png")
            pix.save(f"{iconset_dir}/icon_256x256.png")
        elif size == 512:
            pix.save(f"{iconset_dir}/icon_256x256@2x.png")
            pix.save(f"{iconset_dir}/icon_512x512.png")
        elif size == 1024:
            pix.save(f"{iconset_dir}/icon_512x512@2x.png")

    subprocess.run(["iconutil", "-c", "icns", iconset_dir], check=True)
    print("✨ Successfully generated Deep Blue & Black Liquid Glass Winnie.icns!")


if __name__ == "__main__":
    create_mac_icon()
