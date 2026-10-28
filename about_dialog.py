"""About Winnie Dialog - Minimal, modern app info with social links."""

import os
import sys
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QWidget,
)
from PySide6.QtGui import (
    QFont,
    QPixmap,
    QColor,
    QDesktopServices,
)
from PySide6.QtCore import Qt, QUrl, QSize
from theme import DARK_THEME
from icons import (
    render_svg_icon,
    GITHUB_SVG,
    LINKEDIN_SVG,
    MAIL_SVG,
    EXTERNAL_LINK_SVG,
)


def get_resource_path(relative_path: str) -> str:
    """Finds resource path whether running from source or inside a frozen .app bundle."""
    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        res = os.path.join(base_path, relative_path)
        if os.path.exists(res):
            return res
        res_app = os.path.join(os.path.dirname(sys.executable), "..", "Resources", relative_path)
        if os.path.exists(res_app):
            return res_app
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


class SocialLinkButton(QPushButton):
    """A clean monochromatic social link card with title, handle, and external link indicator."""

    def __init__(self, icon_svg: str, title: str, handle: str, target_url: str, theme: dict, parent=None):
        super().__init__(parent)
        self.target_url = target_url
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(12)

        # 1. Monochromatic SVG Icon
        icon_label = QLabel()
        icon_pixmap = render_svg_icon(icon_svg, size=20, color=theme["editor_text"]).pixmap(20, 20)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(22, 22)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        layout.addWidget(icon_label)

        # 2. Text layout: Title + Handle/URL
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(1)

        muted_color = theme.get("table_header_text", "#71717a")

        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Text", 12, QFont.Weight.DemiBold))
        title_label.setStyleSheet(f"color: {theme['editor_text']}; background: transparent; border: none;")
        title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        handle_label = QLabel(handle)
        handle_label.setFont(QFont("SF Pro Text", 10))
        handle_label.setStyleSheet(f"color: {muted_color}; background: transparent; border: none;")
        handle_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        text_layout.addWidget(title_label)
        text_layout.addWidget(handle_label)
        layout.addLayout(text_layout, stretch=1)

        # 3. Monochromatic External Link Arrow
        arrow_label = QLabel()
        arrow_pixmap = render_svg_icon(EXTERNAL_LINK_SVG, size=13, color=muted_color).pixmap(13, 13)
        arrow_label.setPixmap(arrow_pixmap)
        arrow_label.setFixedSize(14, 14)
        arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        layout.addWidget(arrow_label)

        # Interactive Card Styling
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                border: 1px solid {theme['border_color']};
                border-radius: 10px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
                border-color: {theme['btn_clear_border']};
            }}
            QPushButton:pressed {{
                background-color: {theme['border_color']};
            }}
        """)

        self.clicked.connect(self.open_url)

    def open_url(self):
        QDesktopServices.openUrl(QUrl(self.target_url))


class AboutDialog(QDialog):
    """Modern, minimalist About modal showcasing app version, credits, and monochromatic social links."""

    def __init__(self, parent=None, theme: dict = DARK_THEME):
        super().__init__(parent)
        self.theme = theme
        self.setWindowTitle("About Winnie")
        self.setFixedSize(380, 520)
        self.setModal(True)

        # macOS standard dialog hints
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['window_bg']};
                color: {theme['editor_text']};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 26, 28, 24)
        main_layout.setSpacing(12)

        # 1. Header: App Icon
        icon_path = get_resource_path("Winnie.png")
        if not os.path.exists(icon_path):
            icon_path = get_resource_path("Winnie.icns")

        icon_label = QLabel()
        if os.path.exists(icon_path):
            pm = QPixmap(icon_path)
            if not pm.isNull():
                pm = pm.scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                icon_label.setPixmap(pm)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_label)

        # 2. App Name & Version Badge (Horizontal layout)
        name_badge_layout = QHBoxLayout()
        name_badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_badge_layout.setSpacing(8)

        title_label = QLabel("Winnie")
        title_label.setFont(QFont("SF Pro Display", 20, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {theme['brand_color']};")
        name_badge_layout.addWidget(title_label)

        version_badge = QLabel("v1.3.3")
        version_badge.setFont(QFont("SF Pro Text", 10, QFont.Weight.Bold))
        version_badge.setStyleSheet(f"""
            background-color: {theme['btn_clear_bg']};
            color: {theme['btn_clear_text']};
            border: 1px solid {theme['border_color']};
            border-radius: 9px;
            padding: 2px 7px;
        """)
        name_badge_layout.addWidget(version_badge)
        main_layout.addLayout(name_badge_layout)

        # 3. Subtitle / Tagline
        muted_color = theme.get("table_header_text", "#71717a")
        subtitle = QLabel("A lightweight, beginner-friendly Python IDE for macOS")
        subtitle.setFont(QFont("SF Pro Text", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"color: {muted_color};")
        main_layout.addWidget(subtitle)

        # 4. Subtle Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Plain)
        divider.setStyleSheet(f"background-color: {theme['border_color']}; border: none; max-height: 1px;")
        main_layout.addWidget(divider)

        # 5. Author / "Made with love" credit
        author_label = QLabel("Made with ❤️ by Nilesh Hazra")
        author_label.setFont(QFont("SF Pro Text", 12, QFont.Weight.Medium))
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author_label.setStyleSheet(f"color: {theme['editor_text']}; margin-top: 2px; margin-bottom: 2px;")
        main_layout.addWidget(author_label)

        # 6. Monochromatic Social Links
        socials_layout = QVBoxLayout()
        socials_layout.setSpacing(8)

        github_btn = SocialLinkButton(
            icon_svg=GITHUB_SVG,
            title="GitHub",
            handle="github.com/nileshhazra",
            target_url="https://github.com/nileshhazra",
            theme=theme,
            parent=self,
        )
        socials_layout.addWidget(github_btn)

        linkedin_btn = SocialLinkButton(
            icon_svg=LINKEDIN_SVG,
            title="LinkedIn",
            handle="linkedin.com/in/nileshhazra",
            target_url="https://www.linkedin.com/in/nileshhazra",
            theme=theme,
            parent=self,
        )
        socials_layout.addWidget(linkedin_btn)

        email_btn = SocialLinkButton(
            icon_svg=MAIL_SVG,
            title="Email",
            handle="nilesh.hazra@icloud.com",
            target_url="mailto:nilesh.hazra@icloud.com",
            theme=theme,
            parent=self,
        )
        socials_layout.addWidget(email_btn)

        main_layout.addLayout(socials_layout)

        main_layout.addStretch()

        # 7. Footer note
        footer = QLabel("Open Source • MIT License")
        footer.setFont(QFont("SF Pro Text", 10))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(f"color: {muted_color};")
        main_layout.addWidget(footer)
