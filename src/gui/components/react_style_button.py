#!/usr/bin/env python3
"""
Enhanced React-Style Professional Button Component for Nexlify Engine.

This component replicates and enhances the React ProfessionalButton
with exact CSS color matching, sophisticated animations, and 100% visual fidelity.
"""

from typing import Optional, Union, Callable, Dict, Any
from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QParallelAnimationGroup
from PyQt6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QColor, QFont, QFontMetrics, QPainterPath, QPixmap, QIcon
from PyQt6.QtCore import QRect, QPoint, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtCore import pyqtProperty

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.typography_system import typography, FontSize, FontWeight
from ..design_system.react_theme_system import react_theme, ThemeMode


class EnhancedReactButton(QPushButton):
    """
    Enhanced React-style professional button with exact CSS color matching.
    
    Features:
    - 4 variants: primary, secondary, outline, ghost
    - 3 sizes: sm (32px), md (36px), lg (40px)
    - Exact CSS color scheme matching
    - Advanced gradient backgrounds with sophisticated hover effects
    - Multi-layer shadow system with dynamic depth
    - Enhanced focus ring effects with animations
    - Smooth state transitions (200ms duration)
    - Advanced disabled states with visual feedback
    - Custom property system for flexible styling
    - Accessibility enhancements
    - Light/dark theme support
    """
    
    # Enhanced signals
    clicked_with_data = pyqtSignal(object)
    state_changed = pyqtSignal(str, str)  # old_state, new_state
    
    def __init__(self, text: str = "", parent: Optional[QWidget] = None,
                 variant: str = "primary", size: str = "md",
                 gradient: bool = True, shadow: bool = True,
                 custom_props: Optional[Dict[str, Any]] = None):
        super().__init__(text, parent)
        
        self.variant = variant
        self.size = size
        self.gradient = gradient
        self.shadow = shadow
        self.custom_props = custom_props or {}
        self._emoji_icon = None
        
        # Animation progress values
        self._hover_progress = 0.0
        self._focus_progress = 0.0
        self._press_progress = 0.0
        self._shadow_progress = 0.0
        
        # Enhanced state tracking
        self._is_hovered = False
        self._is_focused = False
        self._is_pressed = False
        self._is_disabled = False
        self._previous_state = "normal"
        self._current_state = "normal"
        
        # Shadow system
        self._shadow_layers = []
        self._shadow_colors = {}
        
        # Setup enhanced button
        self._setup_enhanced_button()
        self._setup_advanced_animations()
        self._setup_enhanced_connections()
        self._setup_shadow_system()
        
        # Connect to theme system
        react_theme.colors_updated.connect(self.update)
        
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
    def press_progress(self):
        """Get press progress value for animation."""
        return self._press_progress
        
    @press_progress.setter
    def press_progress(self, value):
        """Set press progress value for animation."""
        self._press_progress = value
        self.update()
        
    @pyqtProperty(float)
    def shadow_progress(self):
        """Get shadow progress value for animation."""
        return self._shadow_progress
        
    @shadow_progress.setter
    def shadow_progress(self, value):
        """Set shadow progress value for animation."""
        self._shadow_progress = value
        self.update()
        
    def _setup_advanced_animations(self):
        """Setup sophisticated animation system."""
        # Create animations after properties are defined
        self._hover_animation = QPropertyAnimation(self, b"hover_progress")
        self._focus_animation = QPropertyAnimation(self, b"focus_progress")
        self._press_animation = QPropertyAnimation(self, b"press_progress")
        self._shadow_animation = QPropertyAnimation(self, b"shadow_progress")
        
        # Enhanced animation group
        self._animation_group = QParallelAnimationGroup()
        
        # Configure all animations with enhanced easing
        animations = [
            (self._hover_animation, 200, QEasingCurve.Type.OutCubic),
            (self._focus_animation, 200, QEasingCurve.Type.OutCubic),
            (self._press_animation, 150, QEasingCurve.Type.OutQuart),
            (self._shadow_animation, 250, QEasingCurve.Type.OutCubic)
        ]
        
        for animation, duration, easing in animations:
            animation.setDuration(duration)
            animation.setEasingCurve(easing)
            self._animation_group.addAnimation(animation)
            
        # Connect animation updates
        self._hover_animation.valueChanged.connect(self._on_animation_update)
        self._focus_animation.valueChanged.connect(self._on_animation_update)
        self._press_animation.valueChanged.connect(self._on_animation_update)
        self._shadow_animation.valueChanged.connect(self._on_animation_update)
        
    def _setup_enhanced_button(self):
        """Setup enhanced button properties and styling."""
        # Set size based on size variant with precise measurements
        if self.size == "sm":
            height = 32  # h-8
            font_size = typography.xs  # text-xs
            min_width = 64
        elif self.size == "lg":
            height = 40  # h-10
            font_size = typography.md  # text-base
            min_width = 80
        else:  # md
            height = 36  # h-9
            font_size = typography.sm  # text-sm
            min_width = 72
        
        # Set fixed height and minimum width
        self.setFixedHeight(height)
        self.setMinimumWidth(min_width)
        
        # Enhanced font setup
        font = QFont()
        font.setPointSize(font_size)
        font.setWeight(typography.medium)
        self.setFont(font)
        
        # Remove default styling for custom rendering
        self.setStyleSheet("")
        
        # Enhanced focus policy
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTabOrder(self, self)  # Ensure proper tab order
        
        # Enhanced cursor and tooltip
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"{self.variant.title()} Button ({self.size})")
        
        # Accessibility
        self.setAccessibleName(f"{self.variant} button")
        self.setAccessibleDescription(f"{self.size} size {self.variant} button")
        
    def _setup_enhanced_connections(self):
        """Setup enhanced signal connections."""
        # Connect state change signals
        self.pressed.connect(self._on_pressed)
        self.released.connect(self._on_released)
        self.clicked.connect(self._on_clicked)
        
    def _setup_shadow_system(self):
        """Setup sophisticated multi-layer shadow system."""
        # Define shadow layers for different states
        self._shadow_layers = {
            "normal": [
                {"offset": (0, 2), "blur": 8, "spread": 0, "opacity": 0.15},
                {"offset": (0, 1), "blur": 3, "spread": 0, "opacity": 0.1}
            ],
            "hover": [
                {"offset": (0, 4), "blur": 12, "spread": 0, "opacity": 0.25},
                {"offset": (0, 2), "blur": 6, "spread": 0, "opacity": 0.15}
            ],
            "focus": [
                {"offset": (0, 2), "blur": 8, "spread": 0, "opacity": 0.2},
                {"offset": (0, 0), "blur": 0, "spread": 2, "opacity": 0.3}
            ]
        }
        
        # Shadow colors will be dynamically updated from theme
        self._update_shadow_colors()
        
    def _update_shadow_colors(self):
        """Update shadow colors from current theme."""
        self._shadow_colors = {
            "primary": react_theme.get_shadow_color("primary"),
            "secondary": react_theme.get_shadow_color("secondary"),
            "destructive": react_theme.get_shadow_color("destructive"),
            "outline": react_theme.get_border_color(),
            "ghost": react_theme.get_border_color()
        }
        
    def _on_animation_update(self):
        """Handle animation updates for smooth rendering."""
        self.update()
        
    def _on_pressed(self):
        """Handle button press with enhanced state management."""
        self._previous_state = self._current_state
        self._current_state = "pressed"
        self._is_pressed = True
        
        # Start press animation
        self._press_animation.setStartValue(self._press_progress)
        self._press_animation.setEndValue(1.0)
        self._press_animation.start()
        
        # Emit state change
        self.state_changed.emit(self._previous_state, self._current_state)
        self.update()
        
    def _on_released(self):
        """Handle button release with enhanced state management."""
        self._previous_state = self._current_state
        self._current_state = "normal" if not self._is_hovered else "hover"
        self._is_pressed = False
        
        # Start press animation reverse
        self._press_animation.setStartValue(self._press_progress)
        self._press_animation.setEndValue(0.0)
        self._press_animation.start()
        
        # Emit state change
        self.state_changed.emit(self._previous_state, self._current_state)
        self.update()
        
    def _on_clicked(self):
        """Handle button click with enhanced feedback."""
        # Visual feedback
        self._flash_effect()
        
    def _flash_effect(self):
        """Create a subtle flash effect on click."""
        flash_timer = QTimer()
        flash_timer.setSingleShot(True)
        flash_timer.timeout.connect(self.update)
        flash_timer.start(100)
        
    def enterEvent(self, event):
        """Enhanced mouse enter event."""
        super().enterEvent(event)
        self._previous_state = self._current_state
        self._current_state = "hover"
        self._is_hovered = True
        
        # Start hover animations
        self._hover_animation.setStartValue(self._hover_progress)
        self._hover_animation.setEndValue(1.0)
        self._hover_animation.start()
        
        # Start shadow animation
        self._shadow_animation.setStartValue(self._shadow_progress)
        self._shadow_animation.setEndValue(1.0)
        self._shadow_animation.start()
        
        # Emit state change
        self.state_changed.emit(self._previous_state, self._current_state)
        
    def leaveEvent(self, event):
        """Enhanced mouse leave event."""
        super().leaveEvent(event)
        self._previous_state = self._current_state
        self._current_state = "normal"
        self._is_hovered = False
        
        # Start hover animations reverse
        self._hover_animation.setStartValue(self._hover_progress)
        self._hover_animation.setEndValue(0.0)
        self._hover_animation.start()
        
        # Start shadow animation reverse
        self._shadow_animation.setStartValue(self._shadow_progress)
        self._shadow_animation.setEndValue(0.0)
        self._shadow_animation.start()
        
        # Emit state change
        self.state_changed.emit(self._previous_state, self._current_state)
        
    def focusInEvent(self, event):
        """Enhanced focus in event."""
        super().focusInEvent(event)
        self._previous_state = self._current_state
        self._current_state = "focus"
        self._is_focused = True
        
        # Start focus animation
        self._focus_animation.setStartValue(self._focus_progress)
        self._focus_animation.setEndValue(1.0)
        self._focus_animation.start()
        
        # Emit state change
        self.state_changed.emit(self._previous_state, self._current_state)
        
    def focusOutEvent(self, event):
        """Enhanced focus out event."""
        super().focusOutEvent(event)
        self._previous_state = self._current_state
        self._current_state = "normal" if not self._is_hovered else "hover"
        self._is_focused = False
        
        # Start focus animation reverse
        self._focus_animation.setStartValue(self._focus_progress)
        self._focus_animation.setEndValue(0.0)
        self._focus_animation.start()
        
        # Emit state change
        self.state_changed.emit(self._previous_state, self._current_state)
        
    def paintEvent(self, event):
        """Enhanced custom painting for exact React appearance."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Get button dimensions
        rect = self.rect()
        width = rect.width()
        height = rect.height()
        
        # Calculate enhanced padding based on size
        padding_x = self._get_padding_x()
        
        # Update shadow colors from current theme
        self._update_shadow_colors()
        
        # Draw enhanced shadows
        if self.shadow:
            self._draw_enhanced_shadows(painter, rect, width, height)
            
        # Draw enhanced background
        self._draw_enhanced_background(painter, rect, width, height)
        
        # Draw enhanced focus ring
        if self._is_focused:
            self._draw_enhanced_focus_ring(painter, rect, width, height)
            
        # Draw enhanced text
        self._draw_enhanced_text(painter, rect, width, height, padding_x)
        
        # Draw emoji icon if present
        if self._emoji_icon:
            self._draw_emoji_icon(painter, rect, width, height)
        
        # Draw press effect
        if self._is_pressed:
            self._draw_press_effect(painter, rect, width, height)
            
    def _get_padding_x(self) -> int:
        """Get enhanced padding based on size."""
        if self.size == "sm":
            return 12  # px-3
        elif self.size == "lg":
            return 24  # px-6
        else:  # md
            return 16  # px-4
            
    def _draw_enhanced_shadows(self, painter: QPainter, rect: QRect, width: int, height: int):
        """Draw sophisticated multi-layer shadows."""
        if not self.shadow:
            return
            
        # Determine shadow state
        shadow_state = "hover" if self._is_hovered else "normal"
        if self._is_focused:
            shadow_state = "focus"
            
        # Get shadow layers for current state
        layers = self._shadow_layers.get(shadow_state, self._shadow_layers["normal"])
        
        # Draw each shadow layer
        for layer in layers:
            self._draw_shadow_layer(painter, rect, width, height, layer)
            
    def _draw_shadow_layer(self, painter: QPainter, rect: QRect, width: int, height: int, layer: Dict):
        """Draw a single shadow layer."""
        offset_x, offset_y = layer["offset"]
        blur = layer["blur"]
        spread = layer["spread"]
        opacity = layer["opacity"]
        
        # Get shadow color from theme
        shadow_color = self._shadow_colors.get(self.variant, react_theme.get_border_color())
        shadow_color.setAlpha(int(255 * opacity))
        
        # Create shadow rectangle
        shadow_rect = QRect(
            rect.x() + offset_x - spread,
            rect.y() + offset_y - spread,
            width + spread * 2,
            height + spread * 2
        )
        
        # Draw shadow with blur effect
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(shadow_color))
        
        # Use rounded rectangle for shadow with theme radius
        radius = react_theme.get_radius("md")
        painter.drawRoundedRect(shadow_rect, radius, radius)
        
    def _draw_enhanced_background(self, painter: QPainter, rect: QRect, width: int, height: int):
        """Draw enhanced button background with sophisticated variants."""
        # Get enhanced colors for current variant from theme
        colors = react_theme.get_current_colors()
        
        if self.variant == "primary":
            # Enhanced primary button with sophisticated gradient
            if self.gradient:
                # Sophisticated gradient background
                gradient = QLinearGradient(rect.topLeft().x(), rect.topLeft().y(), rect.bottomRight().x(), rect.bottomRight().y())
                primary_color = QColor(colors.primary)
                accent_color = QColor(colors.accent)
                
                # Enhanced gradient stops for sophisticated look
                gradient.setColorAt(0.0, primary_color)
                gradient.setColorAt(0.3, accent_color)
                gradient.setColorAt(0.7, accent_color)
                gradient.setColorAt(1.0, primary_color)
                
                painter.setBrush(QBrush(gradient))
            else:
                # Solid primary with enhanced color
                painter.setBrush(QBrush(QColor(colors.primary)))
                
        elif self.variant == "secondary":
            # Enhanced secondary button with glassmorphism effect
            if self.gradient:
                # Glassmorphism effect
                base_color, overlay_color = react_theme.get_glassmorphism_colors()
                
                # Draw base layer
                painter.setBrush(QBrush(base_color))
                painter.setPen(QPen(Qt.PenStyle.NoPen))
                radius = react_theme.get_radius("md")
                painter.drawRoundedRect(rect, radius, radius)
                
                # Draw overlay for glass effect
                painter.setBrush(QBrush(overlay_color))
                painter.drawRoundedRect(rect, radius, radius)
                return
            else:
                painter.setBrush(QBrush(QColor(colors.secondary)))
                
        elif self.variant == "outline":
            # Enhanced outline button with sophisticated border
            painter.setBrush(QBrush(Qt.GlobalColor.transparent))
            border_color = QColor(colors.border)
            border_color.setAlpha(200)  # Enhanced opacity
            painter.setPen(QPen(border_color, 2))
            radius = react_theme.get_radius("md")
            painter.drawRoundedRect(rect, radius, radius)
            return
            
        elif self.variant == "ghost":
            # Enhanced ghost button with subtle background
            if self._is_hovered:
                hover_color = QColor(colors.muted)
                hover_color.setAlpha(100)  # Subtle hover effect
                painter.setBrush(QBrush(hover_color))
            else:
                painter.setBrush(QBrush(Qt.GlobalColor.transparent))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            
        else:  # default
            # Enhanced default button
            painter.setBrush(QBrush(QColor(colors.card)))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            
        # Draw rounded rectangle with enhanced radius
        radius = react_theme.get_radius("md")
        painter.drawRoundedRect(rect, radius, radius)
        
    def _draw_enhanced_outline_background(self, painter: QPainter, rect: QRect, width: int, height: int):
        """Draw enhanced outline variant background."""
        # Get border color with hover effect from theme
        border_color = self._get_enhanced_border_color()
        
        # Draw border
        painter.setBrush(QBrush(Qt.GlobalColor.transparent))
        painter.setPen(QPen(border_color, 1))
        radius = react_theme.get_radius("md")
        painter.drawRoundedRect(rect, radius, radius)
        
        # Enhanced hover background
        if self._is_hovered:
            hover_color = react_theme.get_accent_color()
            hover_color.setAlpha(int(25 * self._hover_progress))
            painter.setBrush(QBrush(hover_color))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            painter.drawRoundedRect(rect, radius, radius)
            
    def _draw_enhanced_ghost_background(self, painter: QPainter, rect: QRect, width: int, height: int):
        """Draw enhanced ghost variant background."""
        painter.setBrush(QBrush(Qt.GlobalColor.transparent))
        
        # Enhanced hover background
        if self._is_hovered:
            hover_color = react_theme.get_accent_color()
            hover_color.setAlpha(int(25 * self._hover_progress))
            painter.setBrush(QBrush(hover_color))
            radius = react_theme.get_radius("md")
            painter.drawRoundedRect(rect, radius, radius)
            
    def _draw_enhanced_gradient_background(self, painter: QPainter, rect: QRect, base_color: QColor):
        """Draw enhanced gradient background with sophisticated effects."""
        # Create enhanced horizontal gradient
        gradient = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        
        # Enhanced color stops
        if self._is_hovered:
            # Sophisticated hover effect
            hover_intensity = self._hover_progress
            primary_color = QColor(base_color)
            primary_color.setAlpha(int(base_color.alpha() * (0.8 + 0.2 * hover_intensity)))
            
            secondary_color = QColor(base_color)
            secondary_color.setAlpha(int(base_color.alpha() * (0.7 + 0.3 * hover_intensity)))
            
            gradient.setColorAt(0.0, primary_color)
            gradient.setColorAt(0.5, QColor(base_color))
            gradient.setColorAt(1.0, secondary_color)
        else:
            # Normal gradient
            gradient.setColorAt(0.0, base_color)
            gradient.setColorAt(0.5, QColor(base_color))
            gradient.setColorAt(1.0, QColor(base_color.red(), base_color.green(), base_color.blue(), int(base_color.alpha() * 0.9)))
            
        painter.setBrush(QBrush(gradient))
        radius = react_theme.get_radius("md")
        painter.drawRoundedRect(rect, radius, radius)
        
    def _draw_enhanced_focus_ring(self, painter: QPainter, rect: QRect, width: int, height: int):
        """Draw enhanced focus ring with sophisticated effects."""
        if not self._is_focused:
            return
            
        # Enhanced focus ring properties from theme
        ring_color = react_theme.get_focus_ring_color()
        ring_width = 2
        ring_offset = 2
        
        # Create enhanced focus ring rectangle
        ring_rect = QRect(
            rect.x() - ring_offset,
            rect.y() - ring_offset,
            width + ring_offset * 2,
            height + ring_offset * 2
        )
        
        # Draw enhanced focus ring with opacity
        ring_color.setAlpha(int(255 * self._focus_progress))
        painter.setPen(QPen(ring_color, ring_width))
        painter.setBrush(QBrush(Qt.GlobalColor.transparent))
        radius = react_theme.get_radius("lg")
        painter.drawRoundedRect(ring_rect, radius, radius)
        
    def _draw_enhanced_text(self, painter: QPainter, rect: QRect, width: int, height: int, padding_x: int):
        """Draw enhanced button text with sophisticated positioning."""
        # Get enhanced text color from theme
        _, text_color = react_theme.get_variant_colors(self.variant)
        
        # Enhanced text properties
        painter.setPen(QPen(text_color))
        painter.setFont(self.font())
        
        # Enhanced text positioning with press effect
        text_offset_y = 1 if self._is_pressed else 0
        text_rect = QRect(padding_x, text_offset_y, width - padding_x * 2, height)
        
        # Draw enhanced text
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.text())
        
    def _draw_emoji_icon(self, painter: QPainter, rect: QRect, width: int, height: int):
        """Draw emoji icon centered in the button."""
        if not self._emoji_icon:
            return
            
        # Set font for emoji
        emoji_font = QFont()
        emoji_font.setPointSize(16)  # Default emoji size
        painter.setFont(emoji_font)
        
        # Center the emoji
        text_rect = QRect(0, 0, width, height)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._emoji_icon)
        
    def _draw_press_effect(self, painter: QPainter, rect: QRect, width: int, height: int):
        """Draw sophisticated press effect."""
        if not self._is_pressed:
            return
            
        # Create press overlay
        press_color = QColor(0, 0, 0, int(20 * self._press_progress))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(press_color))
        radius = react_theme.get_radius("md")
        painter.drawRoundedRect(rect, radius, radius)
        
    def _get_enhanced_border_color(self) -> QColor:
        """Get enhanced border color with hover effects."""
        base_color = react_theme.get_border_color()
        
        if self._is_hovered:
            # Enhanced hover border color
            accent_color = react_theme.get_accent_color()
            return react_theme.interpolate_colors(base_color, accent_color, self._hover_progress)
        
        return base_color
        
    def setEnabled(self, enabled: bool):
        """Enhanced setEnabled with sophisticated disabled state."""
        super().setEnabled(enabled)
        self._is_disabled = not enabled
        
        if not enabled:
            self._current_state = "disabled"
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.setToolTip("Button is disabled")
        else:
            self._current_state = "normal"
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setToolTip(f"{self.variant.title()} Button ({self.size})")
            
        self.update()
        
    def sizeHint(self) -> QSize:
        """Enhanced size hint for better layout management."""
        # Calculate enhanced width based on text and padding
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        
        if self.size == "sm":
            padding_x = 12
            min_width = 64
        elif self.size == "lg":
            padding_x = 24
            min_width = 80
        else:  # md
            padding_x = 16
            min_width = 72
            
        # Enhanced width calculation
        width = max(text_width + padding_x * 2, min_width)
        height = self.height()
        
        return QSize(width, height)
        
    def get_current_state(self) -> str:
        """Get current button state."""
        return self._current_state
        
    def get_animation_progress(self) -> Dict[str, float]:
        """Get current animation progress values."""
        return {
            "hover": self._hover_progress,
            "focus": self._focus_progress,
            "press": self._press_progress,
            "shadow": self._shadow_progress
        }
        
    def get_theme_mode(self) -> ThemeMode:
        """Get current theme mode."""
        return react_theme.get_current_mode()
    
    def setIcon(self, icon: Union[str, QPixmap, QIcon]):
        """Set button icon.
        
        Args:
            icon: Icon to set (can be emoji string, QPixmap, or QIcon)
        """
        if isinstance(icon, str):
            # Handle emoji icons
            self._emoji_icon = icon
            self.update()
        else:
            # Handle QPixmap or QIcon
            super().setIcon(icon)
            self.update()


# Alias for backward compatibility
ReactStyleButton = EnhancedReactButton
