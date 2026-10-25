from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtCore import QByteArray, Qt

# 1. Modern Play / Run Icon
RUN_SVG = """
<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <polygon points="7,4 20,12 7,20"/>
</svg>
"""

# 2. Modern Stop Icon
STOP_SVG = """
<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <rect x="5" y="5" width="14" height="14" rx="2.5"/>
</svg>
"""

# 3. Modern Step Icon (Step down to next line)
STEP_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="18" r="2" fill="currentColor"/>
  <path d="M12 3v10"/>
  <path d="M8 9l4 4 4-4"/>
</svg>
"""

# 4. Modern Package / Box Icon
PACKAGE_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
  <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
  <line x1="12" y1="22.08" x2="12" y2="12"/>
</svg>
"""

# 5. Modern Problems / Practice Icon
PROBLEMS_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M9 11l3 3L22 4"/>
  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
</svg>
"""

# 3. Modern Trash / Clear Bin Icon
CLEAR_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M3 6h18"/>
  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
  <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
  <line x1="10" y1="11" x2="10" y2="17"/>
  <line x1="14" y1="11" x2="14" y2="17"/>
</svg>
"""

# 4. Modern Moon Icon (Dark Mode)
MOON_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
</svg>
"""

# 5. Modern Sun Icon (Light Mode)
SUN_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="5"/>
  <line x1="12" y1="1" x2="12" y2="3"/>
  <line x1="12" y1="21" x2="12" y2="23"/>
  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
  <line x1="1" y1="12" x2="3" y2="12"/>
  <line x1="21" y1="12" x2="23" y2="12"/>
  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
</svg>
"""

# 6. Monotone Time / Clock Icon
TIME_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="9"/>
  <polyline points="12 7 12 12 15.5 14"/>
</svg>
"""

# 7. Monotone Space / Memory Icon
SPACE_SVG = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="16" height="16" rx="2.5"/>
  <rect x="8.5" y="8.5" width="7" height="7" rx="1"/>
  <line x1="9" y1="1" x2="9" y2="4"/>
  <line x1="15" y1="1" x2="15" y2="4"/>
  <line x1="9" y1="20" x2="9" y2="23"/>
  <line x1="15" y1="20" x2="15" y2="23"/>
  <line x1="20" y1="9" x2="23" y2="9"/>
  <line x1="20" y1="15" x2="23" y2="15"/>
  <line x1="1" y1="9" x2="4" y2="9"/>
  <line x1="1" y1="15" x2="4" y2="15"/>
</svg>
"""


def render_svg_icon(svg_str: str, size: int = 18, color: str = "#ffffff") -> QIcon:
    """Renders an SVG string into a crisp, color-tinted QIcon with Retina support."""
    colored_svg = svg_str.replace("currentColor", color)
    renderer = QSvgRenderer(QByteArray(colored_svg.encode("utf-8")))
    
    scale = 2
    pixmap = QPixmap(size * scale, size * scale)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    pixmap.setDevicePixelRatio(scale)
    return QIcon(pixmap)


def render_svg_pixmap(svg_str: str, size: int = 16, color: str = "#ffffff") -> QPixmap:
    """Renders an SVG string into a crisp, color-tinted Retina QPixmap."""
    colored_svg = svg_str.replace("currentColor", color)
    renderer = QSvgRenderer(QByteArray(colored_svg.encode("utf-8")))
    
    scale = 2
    pixmap = QPixmap(size * scale, size * scale)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    pixmap.setDevicePixelRatio(scale)
    return pixmap
