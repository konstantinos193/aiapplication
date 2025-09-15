#!/usr/bin/env python3
"""
React Theme System for Nexlify Engine.

This module provides the exact color scheme and design tokens
from the React CSS system, including light/dark modes and
ultra-professional IDE styling.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Union
from enum import Enum
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QObject, pyqtSignal


class ThemeMode(Enum):
    """Theme modes matching the CSS system."""
    LIGHT = "light"
    DARK = "dark"


@dataclass
class ReactColorScheme:
    """React color scheme matching the CSS variables exactly."""
    
    # Base colors
    background: str
    foreground: str
    card: str
    card_foreground: str
    popover: str
    popover_foreground: str
    
    # Primary colors
    primary: str
    primary_foreground: str
    secondary: str
    secondary_foreground: str
    
    # Muted colors
    muted: str
    muted_foreground: str
    accent: str
    accent_foreground: str
    
    # Status colors
    destructive: str
    destructive_foreground: str
    
    # UI colors
    border: str
    input: str
    ring: str
    
    # Chart colors
    chart_1: str
    chart_2: str
    chart_3: str
    chart_4: str
    chart_5: str
    
    # Sidebar colors
    sidebar: str
    sidebar_foreground: str
    sidebar_primary: str
    sidebar_primary_foreground: str
    sidebar_accent: str
    sidebar_accent_foreground: str
    sidebar_border: str
    sidebar_ring: str


class ReactThemeSystem(QObject):
    """
    React theme system with exact CSS color matching.
    
    Features:
    - Light and dark mode support
    - Exact color matching with CSS variables
    - Ultra-professional IDE styling
    - Dynamic theme switching
    - Color interpolation and utilities
    """
    
    # Signals
    theme_changed = pyqtSignal(ThemeMode)
    colors_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Initialize with light theme
        self._current_mode = ThemeMode.LIGHT
        self._color_schemes = self._create_color_schemes()
        self._current_colors = self._color_schemes[ThemeMode.LIGHT]
        
        # Border radius system - updated to match new CSS
        self._radius = 12  # 0.75rem = 12px
        self._radius_sm = 8   # calc(var(--radius) - 4px)
        self._radius_md = 10  # calc(var(--radius) - 2px)
        self._radius_lg = 12  # var(--radius)
        self._radius_xl = 16  # calc(var(--radius) + 4px)
        
    def _create_color_schemes(self) -> Dict[ThemeMode, ReactColorScheme]:
        """Create the exact color schemes from the updated CSS."""
        
        # Light theme colors (matching CSS :root)
        light_colors = ReactColorScheme(
            background="#fafafa",
            foreground="#1a1a1a",
            card="#ffffff",
            card_foreground="#1a1a1a",
            popover="#ffffff",
            popover_foreground="#1a1a1a",
            primary="#ea580c",
            primary_foreground="#ffffff",
            secondary="#f4f4f5",
            secondary_foreground="#1a1a1a",
            muted="#f4f4f5",
            muted_foreground="#6b7280",
            accent="#f97316",
            accent_foreground="#ffffff",
            destructive="#dc2626",
            destructive_foreground="#ffffff",
            border="#e4e4e7",
            input="#ffffff",
            ring="rgba(234, 88, 12, 0.3)",
            chart_1="#ea580c",
            chart_2="#f97316",
            chart_3="#6b7280",
            chart_4="#ffffff",
            chart_5="#fafafa",
            sidebar="#ffffff",
            sidebar_foreground="#1a1a1a",
            sidebar_primary="#fafafa",
            sidebar_primary_foreground="#1a1a1a",
            sidebar_accent="#f97316",
            sidebar_accent_foreground="#ffffff",
            sidebar_border="#e4e4e7",
            sidebar_ring="rgba(234, 88, 12, 0.3)"
        )
        
        # Enhanced dark theme colors (matching CSS .dark - ultra-professional IDE look)
        dark_colors = ReactColorScheme(
            background="#0a0a0a",  # Enhanced dark background
            foreground="#fafafa",   # Enhanced light foreground
            card="#1a1a1a",        # Enhanced card background
            card_foreground="#fafafa",
            popover="#1a1a1a",
            popover_foreground="#fafafa",
            primary="#ff6b35",      # Vibrant orange primary
            primary_foreground="#ffffff",
            secondary="#262626",    # Enhanced secondary
            secondary_foreground="#fafafa",
            muted="#262626",        # Enhanced muted
            muted_foreground="#a3a3a3",
            accent="#ff8c42",       # Vibrant orange accent
            accent_foreground="#ffffff",
            destructive="#ef4444",
            destructive_foreground="#ffffff",
            border="#333333",       # Enhanced border
            input="#1a1a1a",        # Enhanced input
            ring="rgba(255, 107, 53, 0.6)",  # Enhanced ring with more opacity
            chart_1="#ff6b35",
            chart_2="#ff8c42",
            chart_3="#a3a3a3",
            chart_4="#1a1a1a",
            chart_5="#0a0a0a",
            sidebar="#1a1a1a",      # Enhanced sidebar
            sidebar_foreground="#fafafa",
            sidebar_primary="#0a0a0a",
            sidebar_primary_foreground="#fafafa",
            sidebar_accent="#ff8c42",
            sidebar_accent_foreground="#ffffff",
            sidebar_border="#333333",
            sidebar_ring="rgba(255, 107, 53, 0.6)"
        )
        
        return {
            ThemeMode.LIGHT: light_colors,
            ThemeMode.DARK: dark_colors
        }
        
    def get_current_mode(self) -> ThemeMode:
        """Get current theme mode."""
        return self._current_mode
        
    def get_current_colors(self) -> ReactColorScheme:
        """Get current color scheme."""
        return self._current_colors
        
    def switch_theme(self, mode: ThemeMode):
        """Switch between light and dark themes."""
        if mode != self._current_mode:
            self._current_mode = mode
            self._current_colors = self._color_schemes[mode]
            self.theme_changed.emit(mode)
            self.colors_updated.emit()
            
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self._current_mode == ThemeMode.LIGHT:
            self.switch_theme(ThemeMode.DARK)
        else:
            self.switch_theme(ThemeMode.LIGHT)
            
    def get_opposite_theme(self) -> ThemeMode:
        """Get the opposite theme mode."""
        return ThemeMode.DARK if self._current_mode == ThemeMode.LIGHT else ThemeMode.LIGHT
        
    def get_color(self, color_name: str) -> QColor:
        """Get a color by name from current theme."""
        color_value = getattr(self._current_colors, color_name, None)
        if color_value:
            return self._parse_color(color_value)
        return QColor(0, 0, 0)  # Fallback
        
    def get_focus_ring_color(self) -> QColor:
        """Get focus ring color for enhanced focus states."""
        return QColor(self._current_colors.ring)
        
    def get_border_color(self) -> QColor:
        """Get border color for enhanced borders."""
        return QColor(self._current_colors.border)
        
    def get_gradient_colors(self) -> Tuple[QColor, QColor]:
        """Get gradient colors for enhanced backgrounds."""
        if self._current_mode == ThemeMode.DARK:
            # Dark mode: sophisticated gradient from card to muted
            return QColor(self._current_colors.card), QColor(self._current_colors.muted)
        else:
            # Light mode: subtle gradient
            return QColor(self._current_colors.card), QColor(self._current_colors.secondary)
            
    def get_glassmorphism_colors(self) -> Tuple[QColor, QColor]:
        """Get glassmorphism colors for modern glass effects."""
        if self._current_mode == ThemeMode.DARK:
            # Dark mode: sophisticated glass effect
            base = QColor(self._current_colors.card)
            overlay = QColor(self._current_colors.background)
            base.setAlpha(180)  # 70% opacity
            overlay.setAlpha(30)  # 12% opacity
            return base, overlay
        else:
            # Light mode: subtle glass effect
            base = QColor(self._current_colors.card)
            overlay = QColor(self._current_colors.background)
            base.setAlpha(200)  # 80% opacity
            overlay.setAlpha(20)  # 8% opacity
            return base, overlay
            
    def get_shadow_colors(self) -> Dict[str, QColor]:
        """Get sophisticated shadow colors for enhanced depth."""
        if self._current_mode == ThemeMode.DARK:
            return {
                "primary": QColor(255, 107, 53, 40),    # Primary shadow
                "secondary": QColor(0, 0, 0, 60),       # Dark shadow
                "accent": QColor(255, 140, 66, 40),     # Accent shadow
                "subtle": QColor(0, 0, 0, 20),          # Subtle shadow
                "glow": QColor(255, 107, 53, 30)        # Glow effect
            }
        else:
            return {
                "primary": QColor(234, 88, 12, 30),
                "secondary": QColor(0, 0, 0, 40),
                "accent": QColor(249, 115, 22, 30),
                "subtle": QColor(0, 0, 0, 15),
                "glow": QColor(234, 88, 12, 20)
            }
            
    def get_radius(self, size: str = "md") -> int:
        """Get border radius for different sizes."""
        radius_map = {
            "sm": self._radius_sm,
            "md": self._radius_md,
            "lg": self._radius_lg,
            "xl": self._radius_xl
        }
        return radius_map.get(size, self._radius_md)
        
    def _parse_color(self, color_value: str) -> QColor:
        """Parse color value to QColor."""
        if color_value.startswith("#"):
            return QColor(color_value)
        elif color_value.startswith("rgba"):
            # Parse rgba(r, g, b, a)
            try:
                values = color_value.replace("rgba(", "").replace(")", "").split(",")
                r = int(float(values[0].strip()))
                g = int(float(values[1].strip()))
                b = int(float(values[2].strip()))
                a = int(float(values[3].strip()) * 255)
                return QColor(r, g, b, a)
            except:
                return QColor(0, 0, 0)
        elif color_value.startswith("rgb"):
            # Parse rgb(r, g, b)
            try:
                values = color_value.replace("rgb(", "").replace(")", "").split(",")
                r = int(float(values[0].strip()))
                g = int(float(values[1].strip()))
                b = int(float(values[2].strip()))
                return QColor(r, g, b)
            except:
                return QColor(0, 0, 0)
        else:
            return QColor(0, 0, 0)
            
    def interpolate_colors(self, color1: QColor, color2: QColor, ratio: float) -> QColor:
        """Interpolate between two colors."""
        return QColor(
            int(color1.red() + (color2.red() - color1.red()) * ratio),
            int(color1.green() + (color2.green() - color1.green()) * ratio),
            int(color1.blue() + (color2.blue() - color1.blue()) * ratio),
            int(color1.alpha() + (color2.alpha() - color1.alpha()) * ratio)
        )
        
    def get_variant_colors(self, variant: str) -> Tuple[QColor, QColor]:
        """Get background and foreground colors for a button variant."""
        if variant == "primary":
            return self.get_color("primary"), self.get_color("primary_foreground")
        elif variant == "secondary":
            return self.get_color("secondary"), self.get_color("secondary_foreground")
        elif variant == "destructive":
            return self.get_color("destructive"), self.get_color("destructive_foreground")
        elif variant == "outline":
            return QColor(0, 0, 0, 0), self.get_color("foreground")  # transparent background
        elif variant == "ghost":
            return QColor(0, 0, 0, 0), self.get_color("foreground")  # transparent background
        else:
            return self.get_color("primary"), self.get_color("primary_foreground")
            
    def get_shadow_color(self, variant: str) -> QColor:
        """Get shadow color for a button variant."""
        if variant == "primary":
            return self.get_color("primary")
        elif variant == "secondary":
            return self.get_color("secondary")
        elif variant == "destructive":
            return self.get_color("destructive")
        else:
            return self.get_color("border")
            
    def get_accent_color(self) -> QColor:
        """Get accent color."""
        return self.get_color("accent")
        
    def get_professional_gradient_colors(self) -> List[QColor]:
        """Get colors for professional gradient effects."""
        return [
            self.get_color("card"),
            self.get_color("muted"),
            self.get_color("primary")
        ]
        
    def get_glass_effect_colors(self) -> Tuple[QColor, QColor]:
        """Get colors for glass effect styling."""
        return self.get_color("card"), self.get_color("border")
        
    def get_panel_shadow_colors(self) -> List[QColor]:
        """Get colors for professional panel shadows."""
        return [
            self.get_color("foreground"),
            self.get_color("foreground"),
            self.get_color("foreground")
        ]

    def get_sidebar_secondary_color(self) -> QColor:
        """Get sidebar secondary color for enhanced styling."""
        if self._current_mode == ThemeMode.DARK:
            # Dark mode: sophisticated secondary
            return QColor("#262626")
        else:
            # Light mode: subtle secondary
            return QColor("#e9ecef")
            
    def get_sidebar_muted_color(self) -> QColor:
        """Get sidebar muted color for enhanced styling."""
        if self._current_mode == ThemeMode.DARK:
            # Dark mode: sophisticated muted
            return QColor("#333333")
        else:
            # Light mode: subtle muted
            return QColor("#f1f3f4")


# Global theme system instance
react_theme = ReactThemeSystem()
