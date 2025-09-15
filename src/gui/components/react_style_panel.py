#!/usr/bin/env python3
"""
React-Style Professional Panel Component for Nexlify Engine.

This component replicates the React ProfessionalPanel with:
- Exact CSS color scheme matching
- Light/dark theme support
- Gradient backgrounds
- Professional shadows
- Title bar with icon support
- 100% visual fidelity
"""

from typing import Optional, Union, Dict, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect
from PyQt6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QColor, QFont, QPixmap, QIcon

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.typography_system import typography, FontSize, FontWeight
from ..design_system.react_theme_system import react_theme, ThemeMode


class ReactStylePanel(QFrame):
    """
    React-style professional panel component with exact visual fidelity.
    
    Features:
    - Card background with border
    - Rounded corners (rounded-lg)
    - Optional gradient background
    - Professional shadows
    - Title bar with icon support
    - Light/dark theme support
    - 100% visual fidelity with React component
    """
    
    # Signals
    title_changed = pyqtSignal(str)
    icon_changed = pyqtSignal()
    gradient_toggled = pyqtSignal(bool)
    shadow_toggled = pyqtSignal(bool)
    
    def __init__(self, parent: Optional[QWidget] = None,
                 title: Optional[str] = None,
                 icon: Optional[Union[str, QPixmap, QIcon]] = None,
                 gradient: bool = False,
                 shadow: bool = True,
                 custom_props: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        
        self.title_text = title
        self.icon_data = icon
        self.gradient_enabled = gradient
        self.shadow_enabled = shadow
        self.custom_props = custom_props or {}
        
        # Animation properties
        self._hover_progress = 0.0
        self._hover_animation = QPropertyAnimation(self, b"hover_progress")
        
        # State tracking
        self._is_hovered = False
        
        # Setup panel
        self._setup_panel()
        self._setup_animations()
        self._setup_connections()
        
        # Connect to theme system
        react_theme.colors_updated.connect(self.update)
        
        # Set frame properties
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(0)  # We'll draw our own border
        
    @pyqtProperty(float)
    def hover_progress(self):
        """Get hover progress value for animation."""
        return self._hover_progress
        
    @hover_progress.setter
    def hover_progress(self, value):
        """Set hover progress value for animation."""
        self._hover_progress = value
        self.update()
        
    def _setup_panel(self):
        """Setup panel properties and layout."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title bar (if title exists)
        if self.title_text:
            self.title_bar = self._create_title_bar()
            self.main_layout.addWidget(self.title_bar)
        else:
            self.title_bar = None
            
        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
        
        # Apply initial styling
        self._apply_panel_styling()
        
    def _create_title_bar(self) -> QWidget:
        """Create the title bar with icon and title."""
        title_bar = QWidget()
        title_bar.setFixedHeight(40)  # h-10 = 40px
        
        # Layout
        title_layout = QHBoxLayout(title_bar)
        title_layout.setSpacing(8)  # mr-2 = 8px
        title_layout.setContentsMargins(12, 0, 12, 0)  # px-3 = 12px horizontal
        
        # Icon
        if self.icon_data:
            self.icon_label = QLabel()
            self._update_icon()
            title_layout.addWidget(self.icon_label)
        else:
            self.icon_label = None
            
        # Title
        self.title_label = QLabel(self.title_text)
        self.title_label.setFont(self._get_title_font())
        self._update_title_styling()
        title_layout.addWidget(self.title_label)
        
        title_layout.addStretch()
        
        return title_bar
        
    def _setup_animations(self):
        """Setup hover animation system."""
        self._hover_animation.setDuration(200)  # duration-200
        self._hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._hover_animation.valueChanged.connect(self._on_hover_animation_update)
        
    def _setup_connections(self):
        """Setup signal connections."""
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
    def _get_title_font(self) -> QFont:
        """Get title font matching React styling."""
        font = QFont()
        font.setPointSize(typography.sm)  # text-sm
        font.setWeight(typography.medium)  # font-medium
        return font
        
    def _update_title_styling(self):
        """Update title styling with current theme colors."""
        if self.title_label:
            colors = react_theme.get_current_colors()
            self.title_label.setStyleSheet(f"color: {colors.foreground};")
            
    def _update_icon(self):
        """Update icon display."""
        if not self.icon_label or not self.icon_data:
            return
            
        if isinstance(self.icon_data, str):
            # String path to icon
            pixmap = QPixmap(self.icon_data)
            if not pixmap.isNull():
                self.icon_label.setPixmap(pixmap.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        elif isinstance(self.icon_data, QPixmap):
            # QPixmap
            self.icon_label.setPixmap(self.icon_data.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        elif isinstance(self.icon_data, QIcon):
            # QIcon
            pixmap = self.icon_data.pixmap(16, 16)
            self.icon_label.setPixmap(pixmap)
            
    def _apply_panel_styling(self):
        """Apply panel styling with theme colors."""
        colors = react_theme.get_current_colors()
        
        # Panel styling - exactly matching React
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {colors.card};
                border: 1px solid {colors.border};
                border-radius: 8px;  /* rounded-lg = 8px in Tailwind */
            }}
        """)
        
        # Title bar styling - EXACTLY matching React: bg-gradient-to-r from-muted/50 to-muted/30
        if self.title_bar:
            # from-muted/50 = 50% opacity, to-muted/30 = 30% opacity
            muted_color = react_theme.get_color("muted")
            muted_50 = QColor(muted_color)
            muted_50.setAlpha(int(255 * 0.5))  # 50% opacity
            muted_30 = QColor(muted_color)
            muted_30.setAlpha(int(255 * 0.3))  # 30% opacity
            
            self.title_bar.setStyleSheet(f"""
                QWidget {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                              stop:0 {muted_50.name()}, 
                                              stop:1 {muted_30.name()});
                    border-bottom: 1px solid {colors.border};
                }}
            """)
            
    def paintEvent(self, event):
        """Custom painting for exact React appearance."""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get panel geometry
        rect = self.rect()
        
        # Draw gradient background if enabled
        if self.gradient_enabled:
            self._draw_gradient_background(painter, rect)
            
        # Draw shadows if enabled
        if self.shadow_enabled:
            self._draw_panel_shadows(painter, rect)
            
    def _draw_gradient_background(self, painter: QPainter, rect: QRect):
        """Draw enhanced gradient background with sophisticated effects."""
        colors = react_theme.get_current_colors()
        
        # Get enhanced gradient colors
        from_color, to_color = react_theme.get_gradient_colors()
        
        # Create sophisticated gradient from bottom-right (to-br)
        gradient = QLinearGradient(rect.topLeft().x(), rect.topLeft().y(), rect.bottomRight().x(), rect.bottomRight().y())
        
        # Enhanced gradient stops for sophisticated look
        gradient.setColorAt(0.0, from_color)           # from-card (100% opacity)
        gradient.setColorAt(0.3, to_color)             # Enhanced middle stop
        gradient.setColorAt(0.7, to_color)             # Enhanced middle stop
        gradient.setColorAt(1.0, to_color)             # to-card (main color)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        
        # Use exact React border radius (12px = rounded-xl)
        radius = react_theme.get_radius("lg")
        painter.drawRoundedRect(rect, radius, radius)
        
    def _draw_panel_shadows(self, painter: QPainter, rect: QRect):
        """Draw sophisticated panel shadows with enhanced depth."""
        if not self.shadow_enabled:
            return
            
        # Get sophisticated shadow colors
        shadow_colors = react_theme.get_shadow_colors()
        
        # Enhanced shadow layers for professional depth
        shadow_layers = [
            {"color": shadow_colors["subtle"], "offset": (0, 1), "blur": 2, "spread": 0},
            {"color": shadow_colors["subtle"], "offset": (0, 2), "blur": 4, "spread": 0},
            {"color": shadow_colors["secondary"], "offset": (0, 4), "blur": 8, "spread": 0},
            {"color": shadow_colors["primary"], "offset": (0, 8), "blur": 16, "spread": 0},
            {"color": shadow_colors["glow"], "offset": (0, 16), "blur": 24, "spread": 0}
        ]
        
        # Draw each shadow layer with enhanced effects
        for layer in shadow_layers:
            self._draw_enhanced_shadow_layer(painter, rect, layer)
            
    def _draw_enhanced_shadow_layer(self, painter: QPainter, rect: QRect, layer: Dict):
        """Draw an enhanced shadow layer with sophisticated effects."""
        color = layer["color"]
        offset_x, offset_y = layer["offset"]
        blur = layer["blur"]
        spread = layer["spread"]
        
        # Create shadow rectangle with offset and spread
        shadow_rect = QRect(
            rect.x() + offset_x - spread,
            rect.y() + offset_y - spread,
            rect.width() + spread * 2,
            rect.height() + spread * 2
        )
        
        # Draw shadow with enhanced effects
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(color))
        
        # Use exact React border radius
        radius = react_theme.get_radius("lg")
        painter.drawRoundedRect(shadow_rect, radius, radius)
            
    def enterEvent(self, event):
        """Handle mouse enter event for hover effects."""
        self._is_hovered = True
        self._hover_animation.setStartValue(self._hover_progress)
        self._hover_animation.setEndValue(1.0)
        self._hover_animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Handle mouse leave event for hover effects."""
        self._is_hovered = False
        self._hover_animation.setStartValue(self._hover_progress)
        self._hover_animation.setEndValue(0.0)
        self._hover_animation.start()
        super().leaveEvent(event)
        
    def _on_hover_animation_update(self):
        """Handle hover animation updates."""
        self.update()
        
    # Public API methods
    def setTitle(self, title: str):
        """Set panel title."""
        self.title_text = title
        if self.title_label:
            self.title_label.setText(title)
        elif title:
            # Create title bar if it doesn't exist
            self.title_bar = self._create_title_bar()
            self.main_layout.insertWidget(0, self.title_bar)
            self._apply_panel_styling()
        self.title_changed.emit(title)
        
    def setIcon(self, icon: Union[str, QPixmap, QIcon]):
        """Set panel icon."""
        self.icon_data = icon
        if self.icon_label:
            self._update_icon()
        elif icon and self.title_bar:
            # Create icon if it doesn't exist
            self.icon_label = QLabel()
            self._update_icon()
            self.title_bar.layout().insertWidget(0, self.icon_label)
        self.icon_changed.emit()
        
    def setGradient(self, enabled: bool):
        """Enable or disable gradient background."""
        self.gradient_enabled = enabled
        self.gradient_toggled.emit(enabled)
        self.update()
        
    def setShadow(self, enabled: bool):
        """Enable or disable shadows."""
        self.shadow_enabled = enabled
        self.shadow_toggled.emit(enabled)
        self.update()
        
    def addWidget(self, widget: QWidget):
        """Add widget to panel content area."""
        self.content_layout.addWidget(widget)
        
    def addLayout(self, layout):
        """Add layout to panel content area."""
        self.content_layout.addLayout(layout)
        
    def addStretch(self, stretch: int = 0):
        """Add stretch to panel content area."""
        self.content_layout.addStretch(stretch)
        
    def setContentSpacing(self, spacing: int):
        """Set spacing between content items."""
        self.content_layout.setSpacing(spacing)
        
    def setContentMargins(self, left: int, top: int, right: int, bottom: int):
        """Set content area margins."""
        self.content_layout.setContentsMargins(left, top, right, bottom)
        
    def setContent(self, widget: QWidget):
        """Set the content widget."""
        # Clear existing content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add the new content widget
        self.content_layout.addWidget(widget)
        
    def getContentWidget(self) -> QWidget:
        """Get the content widget for direct manipulation."""
        return self.content_widget
        
    def getContentLayout(self):
        """Get the content layout for direct manipulation."""
        return self.content_layout


# Alias for backward compatibility
ProfessionalPanel = ReactStylePanel
