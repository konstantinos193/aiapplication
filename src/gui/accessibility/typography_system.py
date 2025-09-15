"""
Typography accessibility system for improved text legibility.

This module provides:
- Scalable font sizing system
- High contrast font options
- Font family accessibility guidelines
- Minimum font size enforcement
- Font scaling controls
"""

from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

from gui.design_system.typography_system import typography, FontSize, FontWeight
from gui.utils.logger import get_logger


class AccessibilityLevel(Enum):
    """Accessibility levels for typography."""
    STANDARD = "standard"
    HIGH_CONTRAST = "high_contrast"
    LARGE_TEXT = "large_text"
    EXTRA_LARGE = "extra_large"


@dataclass(frozen=True)
class FontAccessibilitySettings:
    """Font accessibility settings for different user needs."""
    min_size: int = 12
    preferred_size: int = 16
    line_height_multiplier: float = 1.5
    letter_spacing: float = 0.0
    font_weight: FontWeight = FontWeight.NORMAL
    high_contrast: bool = False


class TypographyAccessibility:
    """Typography accessibility system for improved text legibility."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._current_level = AccessibilityLevel.STANDARD
        self._font_scale_factor = 1.0
        self._high_contrast_enabled = False
        
        # Accessibility font guidelines
        self._accessibility_fonts = {
            'primary': ['Segoe UI', 'Arial', 'Helvetica'],
            'monospace': ['Consolas', 'Monaco', 'Courier New'],
            'fallback': ['sans-serif']
        }
        
        # Font size accessibility ranges
        self._accessible_font_sizes = {
            AccessibilityLevel.STANDARD: range(12, 33),
            AccessibilityLevel.HIGH_CONTRAST: range(14, 36),
            AccessibilityLevel.LARGE_TEXT: range(16, 40),
            AccessibilityLevel.EXTRA_LARGE: range(18, 48)
        }
        
        self.logger.info("TypographyAccessibility system initialized")
    
    def get_accessible_font_size(self, base_size: FontSize, level: AccessibilityLevel = None) -> int:
        """Get accessible font size based on accessibility level."""
        if level is None:
            level = self._current_level
        
        base_value = typography.get_font_size(base_size)
        min_size = min(self._accessible_font_sizes[level])
        
        # Apply accessibility scaling
        scaled_size = max(base_value * self._font_scale_factor, min_size)
        
        # Ensure size is within accessible range for the level
        accessible_range = self._accessible_font_sizes[level]
        if scaled_size not in accessible_range:
            # Find closest accessible size
            scaled_size = min(accessible_range, key=lambda x: abs(x - scaled_size))
        
        return int(scaled_size)
    
    def get_accessible_line_height(self, font_size: int, level: AccessibilityLevel = None) -> float:
        """Get accessible line height for given font size."""
        if level is None:
            level = self._current_level
        
        # WCAG guidelines: line height should be at least 1.5 for body text
        base_line_height = 1.5
        
        # Adjust line height based on accessibility level
        level_multipliers = {
            AccessibilityLevel.STANDARD: 1.5,
            AccessibilityLevel.HIGH_CONTRAST: 1.6,
            AccessibilityLevel.LARGE_TEXT: 1.7,
            AccessibilityLevel.EXTRA_LARGE: 1.8
        }
        
        multiplier = level_multipliers.get(level, 1.5)
        return base_line_height * multiplier
    
    def get_accessible_font_family(self, category: str = 'primary') -> str:
        """Get accessible font family for given category."""
        fonts = self._accessibility_fonts.get(category, self._accessibility_fonts['fallback'])
        
        # Return first available font, with fallbacks
        font_stack = ', '.join(fonts)
        return font_stack
    
    def set_accessibility_level(self, level: AccessibilityLevel) -> None:
        """Set the current accessibility level."""
        self._current_level = level
        self.logger.info(f"Accessibility level set to: {level.value}")
    
    def set_font_scale_factor(self, factor: float) -> None:
        """Set font scaling factor (1.0 = normal, 1.2 = 20% larger, etc.)."""
        if factor < 0.5 or factor > 3.0:
            raise ValueError("Font scale factor must be between 0.5 and 3.0")
        
        self._font_scale_factor = factor
        self.logger.info(f"Font scale factor set to: {factor}")
    
    def get_font_scale_factor(self) -> float:
        """Get current font scale factor."""
        return self._font_scale_factor
    
    def enable_high_contrast(self, enabled: bool = True) -> None:
        """Enable or disable high contrast mode."""
        self._high_contrast_enabled = enabled
        if enabled:
            self._current_level = AccessibilityLevel.HIGH_CONTRAST
        self.logger.info(f"High contrast mode {'enabled' if enabled else 'disabled'}")
    
    def is_high_contrast_enabled(self) -> bool:
        """Check if high contrast mode is enabled."""
        return self._high_contrast_enabled
    
    def get_minimum_font_size(self, level: AccessibilityLevel = None) -> int:
        """Get minimum font size for current accessibility level."""
        if level is None:
            level = self._current_level
        
        return min(self._accessible_font_sizes[level])
    
    def validate_font_size(self, size: int, level: AccessibilityLevel = None) -> bool:
        """Validate if font size meets accessibility requirements."""
        if level is None:
            level = self._current_level
        
        return size in self._accessible_font_sizes[level]
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for typography."""
        return {
            'minimum_size': f"Use minimum {self.get_minimum_font_size()}px font size",
            'line_height': f"Use line height of at least {self.get_accessible_line_height(16):.1f}",
            'font_family': f"Use accessible fonts: {self.get_accessible_font_family()}",
            'contrast': "Ensure sufficient contrast ratio (4.5:1 for normal text)",
            'spacing': "Use adequate letter and word spacing for readability"
        }
    
    def get_current_settings(self) -> FontAccessibilitySettings:
        """Get current font accessibility settings."""
        return FontAccessibilitySettings(
            min_size=self.get_minimum_font_size(),
            preferred_size=self.get_accessible_font_size(FontSize.MEDIUM),
            line_height_multiplier=self.get_accessible_line_height(16),
            font_weight=FontWeight.BOLD if self._high_contrast_enabled else FontWeight.NORMAL,
            high_contrast=self._high_contrast_enabled
        )


# Global instance for easy access
typography_accessibility = TypographyAccessibility()
