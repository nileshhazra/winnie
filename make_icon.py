import os
import sys
import math
import subprocess
from PySide6.QtGui import (
    QGuiApplication,
    QPixmap,
    QPainter,
    QColor,
    QPainterPath,
    QLinearGradient,
    QPen,
)
from PySide6.QtCore import Qt, QRectF, QPointF

app = QGuiApplication(["-platform", "offscreen"])


def create_rounded_triangle_path(p1: QPointF, p2: QPointF, p3: QPointF, radius: float) -> QPainterPath:
    """
    Creates a closed triangle path with smooth, continuous rounded corners.
    p1: Top-Left vertex
    p2: Bottom-Left vertex
    p3: Right Tip apex
    """
    path = QPainterPath()
    pts = [p1, p2, p3]
    n = len(pts)

    corner_info = []
    for i in range(n):
        prev_pt = pts[(i - 1) % n]
        curr_pt = pts[i]
        next_pt = pts[(i + 1) % n]

        v1 = (prev_pt.x() - curr_pt.x(), prev_pt.y() - curr_pt.y())
        v2 = (next_pt.x() - curr_pt.x(), next_pt.y() - curr_pt.y())
        d1 = math.hypot(*v1)
        d2 = math.hypot(*v2)

        u1 = (v1[0] / d1, v1[1] / d1)
        u2 = (v2[0] / d2, v2[1] / d2)

        dot = max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))
        theta = math.acos(dot)

        max_t = min(d1, d2) * 0.45
        t_dist = min(max_t, radius / math.tan(theta / 2.0))

        tan1 = QPointF(curr_pt.x() + u1[0] * t_dist, curr_pt.y() + u1[1] * t_dist)
        tan2 = QPointF(curr_pt.x() + u2[0] * t_dist, curr_pt.y() + u2[1] * t_dist)
        corner_info.append((curr_pt, tan1, tan2))

    for i in range(n):
        curr_pt, tan1, tan2 = corner_info[i]
        next_pt, next_tan1, next_tan2 = corner_info[(i + 1) % n]

        if i == 0:
            path.moveTo(tan1)
        path.quadTo(curr_pt, tan2)
        path.lineTo(next_tan1)

    path.closeSubpath()
    return path


def draw_modern_play_icon(size: int = 512) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    # 1. Apple macOS Squircle Dimensions (Standard 82.4% footprint)
    tile_size = size * 0.824
    margin = (size - tile_size) / 2.0
    radius = tile_size * 0.224
    rect = QRectF(margin, margin, tile_size, tile_size)

    # 2. Multi-Layered Soft Ambient Drop Shadow under the squircle
    for i in range(1, 7):
        shadow_path = QPainterPath()
        shadow_rect = QRectF(margin, margin + (i * size * 0.011), tile_size, tile_size)
        shadow_path.addRoundedRect(shadow_rect, radius, radius)
        alpha = int(45 / i)
        painter.fillPath(shadow_path, QColor(0, 0, 0, alpha))

    # 3. Main Squircle Base Path
    tile_path = QPainterPath()
    tile_path.addRoundedRect(rect, radius, radius)

    # 4. Matte Charcoal / Obsidian Gradient Background with subtle warm undertone
    bg_grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
    bg_grad.setColorAt(0.0, QColor("#302f35"))  # Top-left warm slate highlight
    bg_grad.setColorAt(0.35, QColor("#242328")) # Matte dark charcoal body
    bg_grad.setColorAt(0.85, QColor("#1c1b20")) # Deep obsidian
    bg_grad.setColorAt(1.0, QColor("#141317"))  # Bottom-right shadow
    painter.fillPath(tile_path, bg_grad)

    # Subtle inner top lighting sheen with warm touch
    painter.save()
    painter.setClipPath(tile_path)
    top_sheen = QLinearGradient(rect.topLeft(), QPointF(rect.topLeft().x(), rect.center().y()))
    top_sheen.setColorAt(0.0, QColor(254, 243, 199, 25))
    top_sheen.setColorAt(0.4, QColor(255, 255, 255, 8))
    top_sheen.setColorAt(1.0, QColor(255, 255, 255, 0))
    painter.fillRect(rect, top_sheen)
    painter.restore()

    # 5. Squircle Hardware Edge Rim (Warm golden-tinted perimeter bevel)
    rim_pen = QPen()
    rim_pen.setWidthF(max(1.0, size * 0.003))
    rim_grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
    rim_grad.setColorAt(0.0, QColor(254, 240, 138, 70))
    rim_grad.setColorAt(0.5, QColor(255, 255, 255, 20))
    rim_grad.setColorAt(1.0, QColor(0, 0, 0, 50))
    rim_pen.setBrush(rim_grad)
    painter.strokePath(tile_path, rim_pen)

    # 6. Central Glyph Coordinates
    ox, oy = rect.x(), rect.y()
    w, h = rect.width(), rect.height()
    cy = oy + h * 0.50

    pill_w = w * 0.095
    pill_radius = pill_w / 2.0

    # 6a. Left Dot / Short Pill
    dot_x = ox + w * 0.205
    dot_h = h * 0.118
    dot_rect = QRectF(dot_x, cy - dot_h / 2.0, pill_w, dot_h)
    dot_path = QPainterPath()
    dot_path.addRoundedRect(dot_rect, pill_radius, pill_radius)

    # 6b. Middle Pill (Taller)
    mid_x = ox + w * 0.340
    mid_h = h * 0.335
    mid_rect = QRectF(mid_x, cy - mid_h / 2.0, pill_w, mid_h)
    mid_path = QPainterPath()
    mid_path.addRoundedRect(mid_rect, pill_radius, pill_radius)

    # 6c. Right Play Triangle (Proportionally matched to user's icon)
    tri_left = ox + w * 0.475
    tri_right = ox + w * 0.840
    tri_h = h * 0.415
    p1 = QPointF(tri_left, cy - tri_h / 2.0)
    p2 = QPointF(tri_left, cy + tri_h / 2.0)
    p3 = QPointF(tri_right, cy)
    tri_corner_r = w * 0.052
    tri_path = create_rounded_triangle_path(p1, p2, p3, tri_corner_r)

    # 7. Render Soft Ambient Drop Shadows under the 3 glyphs
    shadow_offset = size * 0.012
    for offset_mult, alpha in [(1.5, 40), (0.9, 75), (0.4, 95)]:
        s_off = shadow_offset * offset_mult
        s_color = QColor(10, 5, 0, alpha)

        painter.save()
        painter.translate(0, s_off)
        painter.fillPath(dot_path, s_color)
        painter.fillPath(mid_path, s_color)
        painter.fillPath(tri_path, s_color)
        painter.restore()

    # 8. Render Left Dot: Caramel Honey
    dot_grad = QLinearGradient(dot_rect.topLeft(), dot_rect.bottomLeft())
    dot_grad.setColorAt(0.0, QColor("#f59e0b")) # Golden amber
    dot_grad.setColorAt(0.35, QColor("#d97706")) # Warm honey
    dot_grad.setColorAt(0.70, QColor("#b45309")) # Caramel
    dot_grad.setColorAt(1.0, QColor("#78350f"))  # Rich deep bronze
    painter.fillPath(dot_path, dot_grad)

    dot_rim_pen = QPen(QColor(254, 243, 199, 65), max(1.0, size * 0.002))
    painter.strokePath(dot_path, dot_rim_pen)

    # 9. Render Middle Pill: Vibrant Warm Honey Amber
    mid_grad = QLinearGradient(mid_rect.topLeft(), mid_rect.bottomLeft())
    mid_grad.setColorAt(0.0, QColor("#fbbf24"))  # Bright honey gold
    mid_grad.setColorAt(0.30, QColor("#f59e0b")) # Vibrant amber
    mid_grad.setColorAt(0.65, QColor("#d97706")) # Rich honey
    mid_grad.setColorAt(1.0, QColor("#92400e"))  # Deep caramel amber
    painter.fillPath(mid_path, mid_grad)

    mid_rim_pen = QPen(QColor(254, 243, 199, 75), max(1.0, size * 0.002))
    painter.strokePath(mid_path, mid_rim_pen)

    # 10. Render Right Play Triangle: Radiant Sunburst Gold to Rich Amber
    tri_grad = QLinearGradient(
        QPointF(tri_left, cy - tri_h / 2.0),
        QPointF(tri_right, cy + tri_h / 2.0)
    )
    tri_grad.setColorAt(0.0, QColor("#fef08a"))  # Sunburst electric gold
    tri_grad.setColorAt(0.18, QColor("#facc15")) # Vivid honey yellow
    tri_grad.setColorAt(0.42, QColor("#f59e0b")) # Radiant warm amber
    tri_grad.setColorAt(0.75, QColor("#d97706")) # Rich golden caramel
    tri_grad.setColorAt(1.0, QColor("#92400e"))  # Deep honey bronze
    painter.fillPath(tri_path, tri_grad)

    # Subtle inner top reflection highlight on triangle
    painter.save()
    painter.setClipPath(tri_path)
    tri_highlight = QLinearGradient(QPointF(tri_left, cy - tri_h / 2.0), QPointF(tri_left, cy))
    tri_highlight.setColorAt(0.0, QColor(255, 255, 255, 110))
    tri_highlight.setColorAt(0.25, QColor(254, 240, 138, 40))
    tri_highlight.setColorAt(1.0, QColor(255, 255, 255, 0))
    painter.fillPath(tri_path, tri_highlight)
    painter.restore()

    # Specular rim on triangle
    tri_rim_pen = QPen()
    tri_rim_pen.setWidthF(max(1.0, size * 0.0025))
    tri_rim_grad = QLinearGradient(QPointF(tri_left, cy - tri_h / 2.0), QPointF(tri_right, cy + tri_h / 2.0))
    tri_rim_grad.setColorAt(0.0, QColor(255, 255, 255, 150))
    tri_rim_grad.setColorAt(0.5, QColor(254, 240, 138, 50))
    tri_rim_grad.setColorAt(1.0, QColor(0, 0, 0, 40))
    tri_rim_pen.setBrush(tri_rim_grad)
    painter.strokePath(tri_path, tri_rim_pen)

    painter.end()
    return pixmap


def create_mac_icon():
    winnie_dir = os.path.dirname(os.path.abspath(__file__))
    iconset_dir = os.path.join(winnie_dir, "Winnie.iconset")
    os.makedirs(iconset_dir, exist_ok=True)

    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        pix = draw_modern_play_icon(size)

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
            # Save standalone PNG as well
            pix.save(os.path.join(winnie_dir, "Winnie.png"))
        elif size == 1024:
            pix.save(f"{iconset_dir}/icon_512x512@2x.png")

    icns_path = os.path.join(winnie_dir, "Winnie.icns")
    subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path], check=True)
    print(f"✨ Successfully generated modern play icon: {icns_path}")


if __name__ == "__main__":
    create_mac_icon()
