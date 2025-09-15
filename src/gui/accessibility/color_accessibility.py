"""
Color accessibility system for WCAG 2.1 AA compliance.

This module provides:
- WCAG 2.1 AA contrast compliance
- High contrast mode support
- Color blind friendly palettes
- Contrast ratio validation
- Color scheme customization
"""

from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum
import colorsys
import math

from gui.utils.logger import get_logger


class ColorBlindnessType(Enum):
    """Types of color blindness to support."""
    NONE = "none"
    PROTANOPIA = "protanopia"  # Red-green color blindness
    DEUTERANOPIA = "deuteranopia"  # Red-green color blindness
    TRITANOPIA = "tritanopia"  # Blue-yellow color blindness
    ACHROMATOPSIA = "achromatopsia"  # Complete color blindness


@dataclass(frozen=True)
class ColorPair:
    """Foreground and background color pair."""
    foreground: str
    background: str
    contrast_ratio: float


@dataclass(frozen=True)
class AccessibilityColorScheme:
    """Accessibility-focused color scheme."""
    name: str
    primary_text: str
    secondary_text: str
    background: str
    surface: str
    accent: str
    error: str
    success: str
    warning: str
    info: str


class ColorAccessibility:
    """Color accessibility system for WCAG 2.1 AA compliance."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._high_contrast_enabled = False
        self._color_blindness_type = ColorBlindnessType.NONE
        
        # WCAG 2.1 AA contrast requirements
        self._contrast_requirements = {
            'normal_text': 4.5,      # Normal text (12pt+)
            'large_text': 3.0,       # Large text (18pt+ or 14pt+ bold)
            'ui_components': 3.0,    # UI components and graphics
            'decorative': 1.0        # Decorative elements (no requirement)
        }
        
        # High contrast color schemes
        self._high_contrast_schemes = {
            'dark': AccessibilityColorScheme(
                name="High Contrast Dark",
                primary_text="#FFFFFF",
                secondary_text="#CCCCCC",
                background="#000000",
                surface="#1A1A1A",
                accent="#FFFF00",
                error="#FF0000",
                success="#00FF00",
                warning="#FFA500",
                info="#00FFFF"
            ),
            'light': AccessibilityColorScheme(
                name="High Contrast Light",
                primary_text="#000000",
                secondary_text="#333333",
                background="#FFFFFF",
                surface="#F0F0F0",
                accent="#0000FF",
                error="#CC0000",
                success="#006600",
                warning="#CC6600",
                info="#0066CC"
            )
        }
        
        # Color blind friendly palettes
        self._color_blind_friendly_palettes = {
            ColorBlindnessType.PROTANOPIA: [
                "#000000", "#E69F00", "#56B4E9", "#009E73",
                "#F0E442", "#0072B2", "#D55E00", "#CC79A7"
            ],
            ColorBlindnessType.DEUTERANOPIA: [
                "#000000", "#E69F00", "#56B4E9", "#009E73",
                "#F0E442", "#0072B2", "#D55E00", "#CC79A7"
            ],
            ColorBlindnessType.TRITANOPIA: [
                "#000000", "#E69F00", "#56B4E9", "#009E73",
                "#F0E442", "#0072B2", "#D55E00", "#CC79A7"
            ],
            ColorBlindnessType.ACHROMATOPSIA: [
                "#000000", "#333333", "#666666", "#999999",
                "#CCCCCC", "#FFFFFF"
            ]
        }
        
        self.logger.info("ColorAccessibility system initialized")
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color."""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def get_relative_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance for RGB color."""
        def normalize(value):
            value = value / 255.0
            if value <= 0.03928:
                return value / 12.92
            return ((value + 0.055) / 1.055) ** 2.4
        
        r, g, b = normalize(rgb[0]), normalize(rgb[1]), normalize(rgb[2])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors."""
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)
        
        lum1 = self.get_relative_luminance(rgb1)
        lum2 = self.get_relative_luminance(rgb2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        if darker == 0:
            return float('inf')
        
        return (lighter + 0.05) / (darker + 0.05)
    
    def validate_contrast(self, foreground: str, background: str, 
                         text_type: str = 'normal_text') -> Tuple[bool, float]:
        """Validate if color pair meets contrast requirements."""
        contrast_ratio = self.calculate_contrast_ratio(foreground, background)
        required_ratio = self._contrast_requirements.get(text_type, 4.5)
        
        is_accessible = contrast_ratio >= required_ratio
        return is_accessible, contrast_ratio
    
    def get_accessible_color_pair(self, base_foreground: str, base_background: str,
                                text_type: str = 'normal_text') -> ColorPair:
        """Get accessible color pair that meets contrast requirements."""
        is_accessible, current_ratio = self.validate_contrast(
            base_foreground, base_background, text_type
        )
        
        if is_accessible:
            return ColorPair(base_foreground, base_background, current_ratio)
        
        # Try to find accessible colors by adjusting brightness
        required_ratio = self._contrast_requirements.get(text_type, 4.5)
        
        # Adjust foreground color to meet contrast
        accessible_foreground = self._adjust_color_for_contrast(
            base_foreground, base_background, required_ratio
        )
        
        new_ratio = self.calculate_contrast_ratio(accessible_foreground, base_background)
        return ColorPair(accessible_foreground, base_background, new_ratio)
    
    def _adjust_color_for_contrast(self, foreground: str, background: str, 
                                 target_ratio: float) -> str:
        """Adjust foreground color to meet target contrast ratio."""
        fg_rgb = list(self.hex_to_rgb(foreground))
        bg_rgb = self.hex_to_rgb(background)
        
        # Try adjusting brightness
        for adjustment in range(0, 256, 5):
            # Try darker
            darker_rgb = [max(0, c - adjustment) for c in fg_rgb]
            darker_hex = self.rgb_to_hex(tuple(darker_rgb))
            if self.calculate_contrast_ratio(darker_hex, background) >= target_ratio:
                return darker_hex
            
            # Try lighter
            lighter_rgb = [min(255, c + adjustment) for c in fg_rgb]
            lighter_hex = self.rgb_to_hex(tuple(lighter_rgb))
            if self.calculate_contrast_ratio(lighter_hex, background) >= target_ratio:
                return lighter_hex
        
        # Fallback to black or white
        bg_luminance = self.get_relative_luminance(bg_rgb)
        if bg_luminance > 0.5:
            return "#000000"  # Black on light background
        else:
            return "#FFFFFF"   # White on dark background
    
    def enable_high_contrast(self, enabled: bool = True, scheme: str = 'dark') -> None:
        """Enable or disable high contrast mode."""
        self._high_contrast_enabled = enabled
        self.logger.info(f"High contrast mode {'enabled' if enabled else 'disabled'} with {scheme} scheme")
    
    def is_high_contrast_enabled(self) -> bool:
        """Check if high contrast mode is enabled."""
        return self._high_contrast_enabled
    
    def get_high_contrast_scheme(self, scheme: str = 'dark') -> AccessibilityColorScheme:
        """Get high contrast color scheme."""
        return self._high_contrast_schemes.get(scheme, self._high_contrast_schemes['dark'])
    
    def set_color_blindness_type(self, blindness_type: ColorBlindnessType) -> None:
        """Set the type of color blindness to support."""
        self._color_blindness_type = blindness_type
        self.logger.info(f"Color blindness support set to: {blindness_type.value}")
    
    def get_color_blind_friendly_palette(self) -> List[str]:
        """Get color blind friendly palette for current setting."""
        return self._color_blind_friendly_palettes.get(
            self._color_blindness_type, 
            self._color_blind_friendly_palettes[ColorBlindnessType.NONE]
        )
    
    def simulate_color_blindness(self, color: str, blindness_type: ColorBlindnessType) -> str:
        """Simulate how a color appears to someone with color blindness."""
        if blindness_type == ColorBlindnessType.NONE:
            return color
        
        # Simple simulation - in a real implementation, you'd use more sophisticated algorithms
        rgb = self.hex_to_rgb(color)
        
        if blindness_type in [ColorBlindnessType.PROTANOPIA, ColorBlindnessType.DEUTERANOPIA]:
            # Red-green color blindness simulation
            # Reduce red and green channels
            new_rgb = (int(rgb[0] * 0.7), int(rgb[1] * 0.7), rgb[2])
        elif blindness_type == ColorBlindnessType.TRITANOPIA:
            # Blue-yellow color blindness simulation
            # Reduce blue channel
            new_rgb = (rgb[0], rgb[1], int(rgb[2] * 0.7))
        elif blindness_type == ColorBlindnessType.ACHROMATOPSIA:
            # Complete color blindness - convert to grayscale
            gray = int(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
            new_rgb = (gray, gray, gray)
        else:
            return color
        
        return self.rgb_to_hex(new_rgb)
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for colors."""
        return {
            'contrast': f"Ensure contrast ratio of at least {self._contrast_requirements['normal_text']}:1 for normal text",
            'large_text': f"Large text can use {self._contrast_requirements['large_text']}:1 contrast ratio",
            'color_blind': f"Don't rely solely on color to convey information",
            'high_contrast': "Provide high contrast mode option",
            'testing': "Test with color blindness simulation tools"
        }
    
    def validate_color_scheme(self, scheme: AccessibilityColorScheme) -> Dict[str, Tuple[bool, float]]:
        """Validate entire color scheme for accessibility."""
        results = {}
        
        # Test primary text against background
        results['primary_text'] = self.validate_contrast(
            scheme.primary_text, scheme.background, 'normal_text'
        )
        
        # Test secondary text against background
        results['secondary_text'] = self.validate_contrast(
            scheme.secondary_text, scheme.background, 'normal_text'
        )
        
        # Test accent against background
        results['accent'] = self.validate_contrast(
            scheme.accent, scheme.background, 'ui_components'
        )
        
        return results


# Global instance for easy access
color_accessibility = ColorAccessibility()
