#!/usr/bin/env python3
"""
React-Style Toolbar Button Component for Nexlify Engine.

This component replicates the React ToolbarButton with:
- Exact CSS color scheme matching
- Light/dark theme support
- Active state with gradient background
- Professional shadows and focus rings
- Hover effects and transitions
- 100% visual fidelity
"""

from typing import Optional, Union, Dict, Any
from PyQt6.QtWidgets import QPushButton, QToolTip, QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QColor, QFont, QIcon, QPixmap

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.typography_system import typography, FontSize, FontWeight
from ..design_system.react_theme_system import react_theme, ThemeMode


class ReactStyleToolbarButton(QPushButton):
    """
    React-style toolbar button component with exact visual fidelity.
    
    Features:
    - Fixed size (h-8 w-8 = 32x32px)
    - Active state with gradient background
    - Professional shadows and focus rings
    - Hover effects and smooth transitions
    - Light/dark theme support
    - 100% visual fidelity with React component
    """
    
    # Signals
    active_changed = pyqtSignal(bool)
    tooltip_changed = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None,
                 text: str = "",
                 icon: Optional[Union[str, QPixmap, QIcon]] = None,
                 active: bool = False,
                 tooltip: str = "",
                 custom_props: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        
        # Button properties
        self._button_text = text
        self._icon_data = icon
        self._is_active = active
        self._tooltip_text = tooltip
        self._custom_props = custom_props or {}
        
        # Animation properties
        self._hover_progress = 0.0
        self._focus_progress = 0.0
        self._glow_intensity = 0.0
        self._hover_animation = QPropertyAnimation(self, b"hover_progress")
        self._focus_animation = QPropertyAnimation(self, b"focus_progress")
        
        # State tracking
        self._is_hovered = False
        self._is_focused = False
        
        # Setup button
        self._setup_button()
        self._setup_animations()
        self._setup_connections()
        
        # Connect to theme system
        react_theme.colors_updated.connect(self.update)
        
        # Set button properties - EXACTLY matching React
        self.setFixedSize(32, 32)  # h-8 w-8 = 32x32px (back to original size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Set tooltip
        if tooltip:
            self.setToolTip(tooltip)
            
        # Ensure icon is properly displayed
        if self._icon_data:
            self._update_icon()
            
    @pyqtProperty(float)
    def hover_progress(self):
        """Get hover progress value for animation."""
        return self._hover_progress
        
    @hover_progress.setter
    def hover_progress(self, value):
        """Set hover progress value for animation."""
        self._hover_progress = value
        self.update()
        
    @pyqtProperty(float)
    def focus_progress(self):
        """Get focus progress value for animation."""
        return self._focus_progress
        
    @focus_progress.setter
    def focus_progress(self, value):
        """Set focus progress value for animation."""
        self._focus_progress = value
        self.update()
        
    @pyqtProperty(float)
    def glow_intensity(self):
        """Get glow intensity value for animation."""
        return self._glow_intensity
        
    @glow_intensity.setter
    def glow_intensity(self, value):
        """Set glow intensity value for animation."""
        self._glow_intensity = value
        self.update()
        
    def _setup_button(self):
        """Setup button properties and styling."""
        # Set text and icon
        if self._button_text:
            self.setText(self._button_text)
            
        if self._icon_data:
            self._update_icon()
            
        # Apply initial styling
        self._apply_button_styling()
        
    def _setup_animations(self):
        """Setup animation system."""
        # Hover animation
        self._hover_animation.setDuration(200)  # duration-200
        self._hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._hover_animation.valueChanged.connect(self._on_hover_animation_update)
        
        # Focus animation
        self._focus_animation.setDuration(200)  # duration-200
        self._focus_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._focus_animation.valueChanged.connect(self._on_focus_animation_update)
        
    def _setup_connections(self):
        """Setup signal connections."""
        # Connect button signals
        self.clicked.connect(self._on_button_clicked)
        
    def _update_icon(self):
        """Update icon display."""
        if self._icon_data is None:
            return
            
        # Calculate icon size based on button size
        icon_size = min(16, self.width() - 8)  # Back to original size
        
        if isinstance(self._icon_data, str):
            # String path to icon
            pixmap = QPixmap(self._icon_data)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                super().setIcon(QIcon(scaled_pixmap))
        elif isinstance(self._icon_data, QPixmap):
            # QPixmap
            scaled_pixmap = self._icon_data.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            super().setIcon(QIcon(scaled_pixmap))
        elif isinstance(self._icon_data, QIcon):
            # QIcon - get the pixmap and scale it
            pixmap = self._icon_data.pixmap(icon_size, icon_size)
            if not pixmap.isNull():
                super().setIcon(self._icon_data)
            else:
                # If icon doesn't have a pixmap, create one
                super().setIcon(self._icon_data)
            
    def _apply_button_styling(self):
        """Apply button styling with theme colors - EXACTLY matching React."""
        colors = react_theme.get_current_colors()
        
        # Base button styling - EXACTLY matching React
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 6px;  /* rounded-md = 6px in Tailwind */
                padding: 0;  /* p-0 = 0px padding */
                font-size: 14px;  /* Back to original size */
                color: {colors.foreground};
                font-weight: 500;  /* Back to original weight */
                /* transition-all duration-200 - handled by QPropertyAnimation */
            }}
            QPushButton:disabled {{
                opacity: 0.5;         /* disabled:opacity-50 */
            }}
            QPushButton:focus {{
                outline: none;  /* focus-visible:outline-none */
            }}
        """)
        
    def paintEvent(self, event):
        """Custom painting for exact React appearance."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get button geometry
        rect = self.rect()
        
        # Draw background based on state
        if self._is_active:
            self._draw_active_background(painter, rect)
        else:
            self._draw_normal_background(painter, rect)
            
        # Draw focus ring if focused
        if self._is_focused:
            self._draw_focus_ring(painter, rect)
            
        # Draw icon or text
        self._draw_content(painter, rect)
        
    def _draw_active_background(self, painter: QPainter, rect: QRect):
        """Draw active state background - bg-gradient-to-b from-primary to-primary/90."""
        colors = react_theme.get_current_colors()
        
        # Create gradient from top to bottom (to-b)
        gradient = QLinearGradient(rect.topLeft().x(), rect.topLeft().y(), rect.bottomLeft().x(), rect.bottomLeft().y())
        
        # from-primary to-primary/90 (90% opacity)
        primary_color = react_theme.get_color("primary")
        primary_color_90 = QColor(primary_color)
        primary_color_90.setAlpha(int(255 * 0.9))  # 90% opacity
        
        gradient.setColorAt(0.0, primary_color)      # from-primary
        gradient.setColorAt(1.0, primary_color_90)   # to-primary/90
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        
        # Use rounded rectangle
        radius = 6  # rounded-md = 6px
        painter.drawRoundedRect(rect, radius, radius)
        
        # Draw shadow - shadow-md shadow-primary/25
        self._draw_active_shadow(painter, rect)
        
    def _draw_normal_background(self, painter: QPainter, rect: QRect):
        """Draw normal state background with hover effects."""
        colors = react_theme.get_current_colors()
        
        if self._is_hovered:
            # hover:bg-accent/20 hover:shadow-sm
            accent_color = react_theme.get_color("accent")
            hover_color = QColor(accent_color)
            hover_color.setAlpha(int(255 * 0.2))  # 20% opacity
            
            painter.setBrush(QBrush(hover_color))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            
            radius = 6  # rounded-md = 6px
            painter.drawRoundedRect(rect, radius, radius)
            
            # Draw hover shadow
            self._draw_hover_shadow(painter, rect)
        else:
            # bg-transparent
            painter.setBrush(QBrush(Qt.GlobalColor.transparent))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            
    def _draw_active_shadow(self, painter: QPainter, rect: QRect):
        """Draw active state shadow - shadow-md shadow-primary/25 with glow effect."""
        colors = react_theme.get_current_colors()
        
        # shadow-primary/25 = 25% opacity
        primary_color = react_theme.get_color("primary")
        shadow_color = QColor(primary_color)
        shadow_color.setAlpha(int(255 * 0.25))  # 25% opacity
        
        # shadow-md effect with offset
        shadow_rect = QRect(
            rect.x() + 1,
            rect.y() + 1,
            rect.width(),
            rect.height()
        )
        
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(shadow_color))
        
        radius = 6  # rounded-md = 6px
        painter.drawRoundedRect(shadow_rect, radius, radius)
        
        # EXACTLY matching React animate-glow effect
        if self.objectName() == "playButton" and self._glow_intensity > 0:
            # Create glow effect based on intensity
            glow_color = QColor(primary_color)
            glow_color.setAlpha(int(255 * self._glow_intensity * 0.6))
            
            # Draw multiple glow layers for the animate-glow effect
            for i in range(3):
                glow_alpha = int(255 * self._glow_intensity * (0.8 - i * 0.2))
                glow_color.setAlpha(glow_alpha)
                glow_rect = QRect(
                    rect.x() - (i + 1) * 2,
                    rect.y() - (i + 1) * 2,
                    rect.width() + (i + 1) * 4,
                    rect.height() + (i + 1) * 4
                )
                
                painter.setBrush(QBrush(glow_color))
                painter.drawRoundedRect(glow_rect, radius + (i + 1) * 2, radius + (i + 1) * 2)
        
    def _draw_hover_shadow(self, painter: QPainter, rect: QRect):
        """Draw hover state shadow - shadow-sm."""
        # shadow-sm effect with subtle offset
        shadow_color = QColor(0, 0, 0, int(255 * 0.1))  # 10% black opacity
        
        shadow_rect = QRect(
            rect.x() + 1,
            rect.y() + 1,
            rect.width(),
            rect.height()
        )
        
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(shadow_color))
        
        radius = 6  # rounded-md = 6px
        painter.drawRoundedRect(shadow_rect, radius, radius)
        
    def _draw_focus_ring(self, painter: QPainter, rect: QRect):
        """Draw focus ring - focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1."""
        colors = react_theme.get_current_colors()
        
        # focus-visible:ring-2 = 2px ring
        # focus-visible:ring-ring = ring color
        # focus-visible:ring-offset-1 = 1px offset
        ring_color = react_theme.get_color("ring")
        ring_width = 2
        ring_offset = 1
        
        # Create focus ring rectangle with offset
        ring_rect = QRect(
            rect.x() - ring_offset,
            rect.y() - ring_offset,
            rect.width() + ring_offset * 2,
            rect.height() + ring_offset * 2
        )
        
        # Draw focus ring with opacity based on focus progress
        ring_color.setAlpha(int(255 * self._focus_progress))
        painter.setPen(QPen(ring_color, ring_width))
        painter.setBrush(QBrush(Qt.GlobalColor.transparent))
        
        # Use rounded rectangle
        radius = 6  # rounded-md = 6px
        painter.drawRoundedRect(ring_rect, radius, radius)
        
    def _draw_content(self, painter: QPainter, rect: QRect):
        """Draw button content (icon or text) - EXACTLY matching React."""
        # Center the content
        painter.setFont(self.font())
        
        if self.icon() and not self.icon().isNull():
            # Draw icon centered - EXACTLY matching React icon sizes
            if self.objectName() == "stopButton":
                # Stop button: h-3 w-3 = 12x12px (smaller)
                icon_size = min(12, rect.width() - 8)
            else:
                # Other buttons: h-4 w-4 = 16x16px
                icon_size = min(16, rect.width() - 8)
                
            icon_x = rect.x() + (rect.width() - icon_size) // 2
            icon_y = rect.y() + (rect.height() - icon_size) // 2
            icon_rect = QRect(icon_x, icon_y, icon_size, icon_size)
            
            # For icons, we don't set the pen color as the icon has its own colors
            self.icon().paint(painter, icon_rect)
        elif self._button_text:
            # Draw text centered with appropriate color - EXACTLY matching React
            if self._is_active:
                # Active state uses primary-foreground color
                painter.setPen(QPen(react_theme.get_color("primary_foreground")))
            else:
                # Normal state uses foreground color
                foreground_color = react_theme.get_color("foreground")
                painter.setPen(QPen(foreground_color))
            
            # Set font for text icons - EXACTLY matching React sizing
            font = painter.font()
            font.setBold(False)
            
            # EXACTLY match React icon sizes
            if self.objectName() == "stopButton":
                # Stop button: h-3 w-3 equivalent
                font.setPointSize(10)
            else:
                # Other buttons: h-4 w-4 equivalent
                font.setPointSize(12)
                
            painter.setFont(font)
            
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self._button_text)
            
    def _on_button_clicked(self):
        """Handle button click."""
        # Toggle active state if needed
        if self._custom_props.get("toggleable", False):
            self.setActive(not self._is_active)
            
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
        
    def focusInEvent(self, event):
        """Handle focus in event for focus ring."""
        self._is_focused = True
        self._focus_animation.setStartValue(self._focus_progress)
        self._focus_animation.setEndValue(1.0)
        self._focus_animation.start()
        super().focusInEvent(event)
        
    def focusOutEvent(self, event):
        """Handle focus out event for focus ring."""
        self._is_focused = False
        self._focus_animation.setStartValue(self._focus_progress)
        self._focus_animation.setEndValue(0.0)
        self._focus_animation.start()
        super().focusOutEvent(event)
        
    def _on_hover_animation_update(self):
        """Handle hover animation updates."""
        self.update()
        
    def _on_focus_animation_update(self):
        """Handle focus animation updates."""
        self.update()
        
    # Public API methods
    def setActive(self, active: bool):
        """Set button active state."""
        if active != self._is_active:
            self._is_active = active
            self.active_changed.emit(active)
            self.update()
            
    def isActive(self) -> bool:
        """Get button active state."""
        return self._is_active
        
    def setTooltip(self, tooltip: str):
        """Set button tooltip."""
        self._tooltip_text = tooltip
        self.setToolTip(tooltip)
        self.tooltip_changed.emit(tooltip)
        
    def getTooltip(self) -> str:
        """Get button tooltip."""
        return self._tooltip_text
        
    def getIcon(self) -> Optional[Union[str, QPixmap, QIcon]]:
        """Get button icon data."""
        return self._icon_data
        
    def setIcon(self, icon: Union[str, QPixmap, QIcon]):
        """Set button icon."""
        self._icon_data = icon
        self._update_icon()
        self.update()  # Trigger a repaint to show the new icon
        
    def clearIcon(self):
        """Clear the button icon."""
        self._icon_data = None
        super().setIcon(QIcon())
        self.update()
        
    def setText(self, text: str):
        """Set button text."""
        self._button_text = text
        super().setText(text)
        
    def setToggleable(self, toggleable: bool):
        """Set whether button can be toggled."""
        self._custom_props["toggleable"] = toggleable
        
    def isToggleable(self) -> bool:
        """Get whether button can be toggled."""
        return self._custom_props.get("toggleable", False)


# Alias for backward compatibility
ToolbarButton = ReactStyleToolbarButton
