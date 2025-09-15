#!/usr/bin/env python3
"""
Professional Theme System for Nexlify Engine.

This module provides a beautiful, custom-designed UI theme system
with gradients, shadows, and professional aesthetics.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import colorsys


class ColorScheme(Enum):
    """Professional color schemes for the engine."""
    DARK_PRO = "dark_pro"           # Dark professional (default)
    DARK_NEON = "dark_neon"         # Dark with neon accents
    LIGHT_PRO = "light_pro"          # Light professional
    GAMING = "gaming"               # Gaming-focused theme
    CREATIVE = "creative"           # Creative/artistic theme


class ButtonStyle(Enum):
    """Professional button styles."""
    PRIMARY = "primary"             # Main action buttons
    SECONDARY = "secondary"         # Secondary actions
    DANGER = "danger"               # Destructive actions
    SUCCESS = "success"             # Success/confirm actions
    GHOST = "ghost"                 # Subtle background buttons
    ICON = "icon"                   # Icon-only buttons


@dataclass
class ColorPalette:
    """Professional color palette with gradients."""
    
    # Primary colors
    primary: str
    primary_light: str
    primary_dark: str
    
    # Secondary colors
    secondary: str
    secondary_light: str
    secondary_dark: str
    
    # Background colors
    background: str
    background_light: str
    background_dark: str
    surface: str
    surface_light: str
    surface_dark: str
    
    # Text colors
    text_primary: str
    text_secondary: str
    text_muted: str
    
    # Accent colors
    accent: str
    accent_light: str
    accent_dark: str
    
    # Status colors
    success: str
    warning: str
    error: str
    info: str
    
    # Border colors
    border: str
    border_light: str
    border_dark: str


@dataclass
class GradientDefinition:
    """Professional gradient definitions."""
    start_color: str
    end_color: str
    direction: str  # "horizontal", "vertical", "diagonal", "radial"
    stops: List[float] = None


@dataclass
class ShadowDefinition:
    """Professional shadow definitions."""
    color: str
    offset_x: int
    offset_y: int
    blur_radius: int
    spread_radius: int
    opacity: float


class ProfessionalTheme:
    """Professional theme system for Nexlify Engine."""
    
    def __init__(self, scheme: ColorScheme = ColorScheme.DARK_PRO):
        self.scheme = scheme
        self.color_palette = self._get_color_palette(scheme)
        self.gradients = self._get_gradients()
        self.shadows = self._get_shadows()
        self.border_radius = self._get_border_radius()
        self.spacing = self._get_spacing()
        self.typography = self._get_typography()
    
    def _get_color_palette(self, scheme: ColorScheme) -> ColorPalette:
        """Get professional color palette for the selected scheme."""
        if scheme == ColorScheme.DARK_PRO:
            return ColorPalette(
                # Primary - Deep blue with professional feel
                primary="#2563eb",
                primary_light="#3b82f6",
                primary_dark="#1d4ed8",
                
                # Secondary - Sophisticated gray
                secondary="#64748b",
                secondary_light="#94a3b8",
                secondary_dark="#475569",
                
                # Background - Rich dark theme
                background="#0f172a",
                background_light="#1e293b",
                background_dark="#020617",
                surface="#1e293b",
                surface_light="#334155",
                surface_dark="#0f172a",
                
                # Text - High contrast for readability
                text_primary="#f8fafc",
                text_secondary="#cbd5e1",
                text_muted="#64748b",
                
                # Accent - Gold accent for premium feel
                accent="#f59e0b",
                accent_light="#fbbf24",
                accent_dark="#d97706",
                
                # Status colors
                success="#10b981",
                warning="#f59e0b",
                error="#ef4444",
                info="#3b82f6",
                
                # Border colors
                border="#334155",
                border_light="#475569",
                border_dark="#1e293b"
            )
        
        elif scheme == ColorScheme.DARK_NEON:
            return ColorPalette(
                # Primary - Electric blue
                primary="#00d4ff",
                primary_light="#40e0ff",
                primary_dark="#0099cc",
                
                # Secondary - Neon purple
                secondary="#a855f7",
                secondary_light="#c084fc",
                secondary_dark="#7c3aed",
                
                # Background - Deep space
                background="#0a0a0a",
                background_light="#1a1a1a",
                background_dark="#000000",
                surface="#1a1a1a",
                surface_light="#2a2a2a",
                surface_dark="#0a0a0a",
                
                # Text - Bright neon
                text_primary="#ffffff",
                text_secondary="#e0e0e0",
                text_muted="#888888",
                
                # Accent - Neon green
                accent="#00ff88",
                accent_light="#40ffa0",
                accent_dark="#00cc6a",
                
                # Status colors
                success="#00ff88",
                warning="#ffaa00",
                error="#ff0040",
                info="#00d4ff",
                
                # Border colors
                border="#333333",
                border_light="#444444",
                border_dark="#222222"
            )
        
        elif scheme == ColorScheme.GAMING:
            return ColorPalette(
                # Primary - Gaming red
                primary="#dc2626",
                primary_light="#ef4444",
                primary_dark="#b91c1c",
                
                # Secondary - Gaming blue
                secondary="#1d4ed8",
                secondary_light="#3b82f6",
                secondary_dark="#1e40af",
                
                # Background - Dark gaming
                background="#0a0a0a",
                background_light="#1a1a1a",
                background_dark="#000000",
                surface="#1a1a1a",
                surface_light="#2a2a2a",
                surface_dark="#0a0a0a",
                
                # Text - Bright gaming
                text_primary="#ffffff",
                text_secondary="#e0e0e0",
                text_muted="#888888",
                
                # Accent - Gaming orange
                accent="#ea580c",
                accent_light="#f97316",
                accent_dark="#c2410c",
                
                # Status colors
                success="#16a34a",
                warning="#ea580c",
                error="#dc2626",
                info="#2563eb",
                
                # Border colors
                border="#333333",
                border_light="#444444",
                border_dark="#222222"
            )
        
        else:  # Default to DARK_PRO
            return self._get_color_palette(ColorScheme.DARK_PRO)
    
    def _get_gradients(self) -> Dict[str, GradientDefinition]:
        """Get professional gradient definitions."""
        return {
            "primary_button": GradientDefinition(
                start_color=self.color_palette.primary,
                end_color=self.color_palette.primary_dark,
                direction="vertical",
                stops=[0.0, 1.0]
            ),
            "secondary_button": GradientDefinition(
                start_color=self.color_palette.surface,
                end_color=self.color_palette.surface_dark,
                direction="vertical",
                stops=[0.0, 1.0]
            ),
            "header": GradientDefinition(
                start_color=self.color_palette.background,
                end_color=self.color_palette.background_light,
                direction="horizontal",
                stops=[0.0, 1.0]
            ),
            "panel": GradientDefinition(
                start_color=self.color_palette.surface,
                end_color=self.color_palette.surface_dark,
                direction="vertical",
                stops=[0.0, 0.8]
            ),
            "accent": GradientDefinition(
                start_color=self.color_palette.accent,
                end_color=self.color_palette.accent_dark,
                direction="diagonal",
                stops=[0.0, 1.0]
            )
        }
    
    def _get_shadows(self) -> Dict[str, ShadowDefinition]:
        """Get professional shadow definitions."""
        return {
            "small": ShadowDefinition(
                color="#000000",
                offset_x=0,
                offset_y=2,
                blur_radius=4,
                spread_radius=0,
                opacity=0.1
            ),
            "medium": ShadowDefinition(
                color="#000000",
                offset_x=0,
                offset_y=4,
                blur_radius=8,
                spread_radius=0,
                opacity=0.15
            ),
            "large": ShadowDefinition(
                color="#000000",
                offset_x=0,
                offset_y=8,
                blur_radius=16,
                spread_radius=0,
                opacity=0.2
            ),
            "button": ShadowDefinition(
                color="#000000",
                offset_x=0,
                offset_y=2,
                blur_radius=8,
                spread_radius=0,
                opacity=0.25
            ),
            "panel": ShadowDefinition(
                color="#000000",
                offset_x=0,
                offset_y=4,
                blur_radius=12,
                spread_radius=0,
                opacity=0.15
            )
        }
    
    def _get_border_radius(self) -> Dict[str, int]:
        """Get professional border radius values."""
        return {
            "small": 4,
            "medium": 8,
            "large": 12,
            "xl": 16,
            "button": 8,
            "panel": 12,
            "modal": 16
        }
    
    def _get_spacing(self) -> Dict[str, int]:
        """Get professional spacing values."""
        return {
            "xs": 4,
            "sm": 8,
            "md": 16,
            "lg": 24,
            "xl": 32,
            "2xl": 48,
            "3xl": 64
        }
    
    def _get_typography(self) -> Dict[str, Dict]:
        """Get professional typography settings."""
        return {
            "heading1": {"size": 32, "weight": "bold", "line_height": 1.2},
            "heading2": {"size": 24, "weight": "bold", "line_height": 1.3},
            "heading3": {"size": 20, "weight": "semibold", "line_height": 1.4},
            "body": {"size": 14, "weight": "normal", "line_height": 1.5},
            "body_small": {"size": 12, "weight": "normal", "line_height": 1.4},
            "button": {"size": 14, "weight": "semibold", "line_height": 1.0},
            "caption": {"size": 11, "weight": "normal", "line_height": 1.3}
        }
    
    def get_button_style(self, button_type: ButtonStyle) -> Dict:
        """Get professional button styling."""
        base_style = {
            "border_radius": self.border_radius["button"],
            "padding": f"{self.spacing['sm']}px {self.spacing['md']}px",
            "font_family": "'Segoe UI', 'Roboto', sans-serif",
            "font_size": self.typography["button"]["size"],
            "font_weight": self.typography["button"]["weight"],
            "text_transform": "none",
            "letter_spacing": "0.025em",
            "transition": "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            "cursor": "pointer",
            "border": "none",
            "outline": "none"
        }
        
        if button_type == ButtonStyle.PRIMARY:
            return {
                **base_style,
                "background": f"linear-gradient(135deg, {self.color_palette.primary} 0%, {self.color_palette.primary_dark} 100%)",
                "color": self.color_palette.text_primary,
                "box_shadow": f"0 4px 12px {self.color_palette.primary}40",
                "hover": {
                    "background": f"linear-gradient(135deg, {self.color_palette.primary_light} 0%, {self.color_palette.primary} 100%)",
                    "box_shadow": f"0 6px 16px {self.color_palette.primary}60",
                    "transform": "translateY(-1px)"
                }
            }
        
        elif button_type == ButtonStyle.SECONDARY:
            return {
                **base_style,
                "background": f"linear-gradient(135deg, {self.color_palette.surface} 0%, {self.color_palette.surface_dark} 100%)",
                "color": self.color_palette.text_primary,
                "border": f"1px solid {self.color_palette.border}",
                "box_shadow": f"0 2px 8px {self.color_palette.border}20",
                "hover": {
                    "background": f"linear-gradient(135deg, {self.color_palette.surface_light} 0%, {self.color_palette.surface} 100%)",
                    "border_color": self.color_palette.border_light,
                    "box_shadow": f"0 4px 12px {self.color_palette.border}40"
                }
            }
        
        elif button_type == ButtonStyle.DANGER:
            return {
                **base_style,
                "background": f"linear-gradient(135deg, {self.color_palette.error} 0%, {self.color_palette.error}dd 100%)",
                "color": self.color_palette.text_primary,
                "box_shadow": f"0 4px 12px {self.color_palette.error}40",
                "hover": {
                    "background": f"linear-gradient(135deg, {self.color_palette.error}ee 0%, {self.color_palette.error} 100%)",
                    "box_shadow": f"0 6px 16px {self.color_palette.error}60"
                }
            }
        
        elif button_type == ButtonStyle.SUCCESS:
            return {
                **base_style,
                "background": f"linear-gradient(135deg, {self.color_palette.success} 0%, {self.color_palette.success}dd 100%)",
                "color": self.color_palette.text_primary,
                "box_shadow": f"0 4px 12px {self.color_palette.success}40",
                "hover": {
                    "background": f"linear-gradient(135deg, {self.color_palette.success}ee 0%, {self.color_palette.success} 100%)",
                    "box_shadow": f"0 6px 16px {self.color_palette.success}60"
                }
            }
        
        else:  # GHOST and ICON
            return {
                **base_style,
                "background": "transparent",
                "color": self.color_palette.text_secondary,
                "border": "none",
                "box_shadow": "none",
                "hover": {
                    "background": f"{self.color_palette.surface}",
                    "color": self.color_palette.text_primary
                }
            }
    
    def get_panel_style(self) -> Dict:
        """Get professional panel styling."""
        return {
            "background": f"linear-gradient(180deg, {self.color_palette.surface} 0%, {self.color_palette.surface_dark} 100%)",
            "border": f"1px solid {self.color_palette.border}",
            "border_radius": self.border_radius["panel"],
            "box_shadow": f"0 4px 12px {self.color_palette.border}20",
            "padding": f"{self.spacing['md']}px",
            "backdrop_filter": "blur(10px)"
        }
    
    def get_header_style(self) -> Dict:
        """Get professional header styling."""
        return {
            "background": f"linear-gradient(90deg, {self.color_palette.background} 0%, {self.color_palette.background_light} 100%)",
            "border_bottom": f"1px solid {self.color_palette.border}",
            "box_shadow": f"0 2px 8px {self.color_palette.border}20",
            "padding": f"{self.spacing['md']}px {self.spacing['lg']}px",
            "backdrop_filter": "blur(20px)"
        }
    
    def get_input_style(self) -> Dict:
        """Get professional input styling."""
        return {
            "background": self.color_palette.surface,
            "border": f"1px solid {self.color_palette.border}",
            "border_radius": self.border_radius["small"],
            "color": self.color_palette.text_primary,
            "padding": f"{self.spacing['sm']}px {self.spacing['md']}px",
            "font_size": self.typography["body"]["size"],
            "transition": "all 0.2s ease",
            "focus": {
                "border_color": self.color_palette.primary,
                "box_shadow": f"0 0 0 3px {self.color_palette.primary}20",
                "outline": "none"
            }
        }
    
    def get_scrollbar_style(self) -> Dict:
        """Get professional scrollbar styling."""
        return {
            "width": "8px",
            "background": self.color_palette.surface_dark,
            "border_radius": "4px",
            "thumb": {
                "background": f"linear-gradient(180deg, {self.color_palette.border} 0%, {self.color_palette.border_light} 100%)",
                "border_radius": "4px",
                "hover": {
                    "background": f"linear-gradient(180deg, {self.color_palette.border_light} 0%, {self.color_palette.primary} 100%)"
                }
            }
        }
    
    def get_animation_timing(self) -> Dict:
        """Get professional animation timing functions."""
        return {
            "fast": "0.15s cubic-bezier(0.4, 0, 0.2, 1)",
            "normal": "0.25s cubic-bezier(0.4, 0, 0.2, 1)",
            "slow": "0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            "bounce": "0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)",
            "elastic": "0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)"
        }
    
    def generate_css_variables(self) -> str:
        """Generate CSS custom properties for the theme."""
        css = ":root {\n"
        
        # Color variables
        for attr, value in self.color_palette.__dict__.items():
            css += f"  --color-{attr.replace('_', '-')}: {value};\n"
        
        # Spacing variables
        for name, value in self.spacing.items():
            css += f"  --spacing-{name}: {value}px;\n"
        
        # Border radius variables
        for name, value in self.border_radius.items():
            css += f"  --border-radius-{name}: {value}px;\n"
        
        # Typography variables
        for name, props in self.typography.items():
            for prop, value in props.items():
                css += f"  --typography-{name}-{prop.replace('_', '-')}: {value};\n"
        
        css += "}\n"
        return css
    
    def get_theme_info(self) -> Dict:
        """Get comprehensive theme information."""
        return {
            "scheme": self.scheme.value,
            "color_palette": self.color_palette.__dict__,
            "gradients": {k: v.__dict__ for k, v in self.gradients.items()},
            "shadows": {k: v.__dict__ for k, v in self.shadows.items()},
            "border_radius": self.border_radius,
            "spacing": self.spacing,
            "typography": self.typography,
            "animation_timing": self.get_animation_timing()
        }


# Default theme instance
default_theme = ProfessionalTheme(ColorScheme.DARK_PRO)
