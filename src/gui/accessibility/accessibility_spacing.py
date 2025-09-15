"""
Accessibility spacing system for improved accessibility.

This module provides:
- High contrast spacing
- Large text spacing adjustments
- Focus indicator spacing
- Screen reader friendly spacing
- Accessibility spacing validation
"""

from typing import Dict, Tuple, Optional, List, Any
from dataclasses import dataclass
from enum import Enum
import logging

from gui.design_system.spacing_system import spacing, SpacingUnit
from gui.utils.logger import get_logger


class AccessibilitySpacingLevel(Enum):
    """Accessibility spacing levels."""
    STANDARD = "standard"
    HIGH_CONTRAST = "high_contrast"
    LARGE_TEXT = "large_text"
    EXTRA_LARGE = "extra_large"
    SCREEN_READER = "screen_reader"


@dataclass(frozen=True)
class AccessibilitySpacingSettings:
    """Accessibility spacing settings."""
    min_touch_target: int = 44  # Minimum touch target size in pixels
    focus_indicator_offset: int = 2  # Focus indicator offset from element
    text_spacing_multiplier: float = 1.5  # Text spacing multiplier
    element_separation: int = 8  # Minimum separation between elements
    group_spacing: int = 16  # Spacing for grouped elements


class AccessibilitySpacing:
    """Accessibility spacing system for improved accessibility."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._current_level = AccessibilitySpacingLevel.STANDARD
        self._touch_friendly_enabled = False
        self._screen_reader_optimized = False
        
        # Accessibility spacing multipliers
        self._spacing_multipliers = {
            AccessibilitySpacingLevel.STANDARD: 1.0,
            AccessibilitySpacingLevel.HIGH_CONTRAST: 1.2,
            AccessibilitySpacingLevel.LARGE_TEXT: 1.4,
            AccessibilitySpacingLevel.EXTRA_LARGE: 1.8,
            AccessibilitySpacingLevel.SCREEN_READER: 1.6
        }
        
        # Touch-friendly spacing adjustments
        self._touch_spacing_adjustments = {
            'button_padding': 12,      # Increased button padding for touch
            'input_height': 48,        # Increased input height for touch
            'element_gap': 16,         # Increased gap between elements
            'group_margin': 24         # Increased margin for groups
        }
        
        # Screen reader spacing optimizations
        self._screen_reader_spacing = {
            'text_line_height': 1.8,   # Increased line height for screen readers
            'paragraph_spacing': 24,    # Increased paragraph spacing
            'section_spacing': 32,      # Increased section spacing
            'navigation_gap': 20        # Increased navigation element gap
        }
        
        self.logger.info("AccessibilitySpacing system initialized")
    
    def get_accessible_spacing(self, base_spacing: int, 
                              level: AccessibilitySpacingLevel = None) -> int:
        """Get accessible spacing based on accessibility level."""
        if level is None:
            level = self._current_level
        
        multiplier = self._spacing_multipliers.get(level, 1.0)
        accessible_spacing = int(base_spacing * multiplier)
        
        # Ensure minimum spacing for accessibility
        min_spacing = self._get_minimum_spacing_for_level(level)
        accessible_spacing = max(accessible_spacing, min_spacing)
        
        return accessible_spacing
    
    def get_accessible_margin(self, base_margin: SpacingUnit, 
                             level: AccessibilitySpacingLevel = None) -> int:
        """Get accessible margin based on accessibility level."""
        base_value = spacing.get_spacing(base_margin)
        return self.get_accessible_spacing(base_value, level)
    
    def get_accessible_padding(self, base_padding: SpacingUnit, 
                              level: AccessibilitySpacingLevel = None) -> int:
        """Get accessible padding based on accessibility level."""
        base_value = spacing.get_spacing(base_padding)
        return self.get_accessible_spacing(base_value, level)
    
    def get_touch_friendly_spacing(self, element_type: str) -> int:
        """Get touch-friendly spacing for given element type."""
        if not self._touch_friendly_enabled:
            return spacing.get_spacing(SpacingUnit.MEDIUM)
        
        adjustments = self._touch_spacing_adjustments
        base_spacing = spacing.get_spacing(SpacingUnit.MEDIUM)
        
        if element_type == 'button':
            return adjustments['button_padding']
        elif element_type == 'input':
            return adjustments['input_height']
        elif element_type == 'element_gap':
            return adjustments['element_gap']
        elif element_type == 'group_margin':
            return adjustments['group_margin']
        else:
            return max(base_spacing, adjustments['element_gap'])
    
    def get_screen_reader_spacing(self, spacing_type: str) -> int:
        """Get screen reader optimized spacing."""
        if not self._screen_reader_optimized:
            return spacing.get_spacing(SpacingUnit.MEDIUM)
        
        base_spacing = spacing.get_spacing(SpacingUnit.MEDIUM)
        sr_adjustments = self._screen_reader_spacing
        
        if spacing_type == 'line_height':
            return int(base_spacing * sr_adjustments['text_line_height'])
        elif spacing_type == 'paragraph':
            return sr_adjustments['paragraph_spacing']
        elif spacing_type == 'section':
            return sr_adjustments['section_spacing']
        elif spacing_type == 'navigation':
            return sr_adjustments['navigation_gap']
        else:
            return base_spacing
    
    def get_focus_indicator_spacing(self, element_size: Tuple[int, int]) -> Dict[str, int]:
        """Get spacing for focus indicators."""
        width, height = element_size
        
        # Ensure focus indicator is clearly visible
        offset = self._get_focus_indicator_offset()
        padding = max(4, min(width, height) // 8)  # Proportional padding
        
        return {
            'offset': offset,
            'padding': padding,
            'border_width': max(2, min(width, height) // 16),
            'min_size': max(width, height) + (offset * 2)
        }
    
    def get_minimum_touch_target_size(self) -> int:
        """Get minimum touch target size for accessibility."""
        return self._touch_spacing_adjustments['input_height']
    
    def validate_touch_target_size(self, width: int, height: int) -> bool:
        """Validate if element meets minimum touch target size."""
        min_size = self.get_minimum_touch_target_size()
        return width >= min_size and height >= min_size
    
    def get_element_separation_guidelines(self) -> Dict[str, int]:
        """Get guidelines for element separation."""
        return {
            'related_elements': self._get_minimum_spacing_for_level(self._current_level),
            'unrelated_elements': self._get_minimum_spacing_for_level(self._current_level) * 2,
            'grouped_elements': self._get_minimum_spacing_for_level(self._current_level) * 3,
            'section_separation': self._get_minimum_spacing_for_level(self._current_level) * 4
        }
    
    def set_accessibility_level(self, level: AccessibilitySpacingLevel) -> None:
        """Set the current accessibility spacing level."""
        self._current_level = level
        self.logger.info(f"Accessibility spacing level set to: {level.value}")
    
    def enable_touch_friendly_mode(self, enabled: bool = True) -> None:
        """Enable or disable touch-friendly spacing mode."""
        self._touch_friendly_enabled = enabled
        self.logger.info(f"Touch-friendly mode {'enabled' if enabled else 'disabled'}")
    
    def is_touch_friendly_enabled(self) -> bool:
        """Check if touch-friendly mode is enabled."""
        return self._touch_friendly_enabled
    
    def enable_screen_reader_optimization(self, enabled: bool = True) -> None:
        """Enable or disable screen reader spacing optimization."""
        self._screen_reader_optimized = enabled
        self.logger.info(f"Screen reader optimization {'enabled' if enabled else 'disabled'}")
    
    def is_screen_reader_optimized(self) -> bool:
        """Check if screen reader optimization is enabled."""
        return self._screen_reader_optimized
    
    def _get_minimum_spacing_for_level(self, level: AccessibilitySpacingLevel) -> int:
        """Get minimum spacing for given accessibility level."""
        base_minimum = 8  # Base minimum spacing
        
        level_multipliers = {
            AccessibilitySpacingLevel.STANDARD: 1.0,
            AccessibilitySpacingLevel.HIGH_CONTRAST: 1.5,
            AccessibilitySpacingLevel.LARGE_TEXT: 2.0,
            AccessibilitySpacingLevel.EXTRA_LARGE: 2.5,
            AccessibilitySpacingLevel.SCREEN_READER: 2.0
        }
        
        multiplier = level_multipliers.get(level, 1.0)
        return int(base_minimum * multiplier)
    
    def _get_focus_indicator_offset(self) -> int:
        """Get focus indicator offset based on current settings."""
        base_offset = 2
        
        if self._current_level in [AccessibilitySpacingLevel.HIGH_CONTRAST, 
                                  AccessibilitySpacingLevel.EXTRA_LARGE]:
            base_offset = 4
        elif self._current_level == AccessibilitySpacingLevel.SCREEN_READER:
            base_offset = 3
        
        return base_offset
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for spacing."""
        return {
            'touch_targets': f"Ensure minimum touch target size of {self.get_minimum_touch_target_size()}px",
            'element_separation': f"Use minimum {self._get_minimum_spacing_for_level(self._current_level)}px between elements",
            'focus_indicators': "Provide clear focus indicators with adequate spacing",
            'text_spacing': f"Use line height of at least {self.get_screen_reader_spacing('line_height')}px for readability",
            'grouping': "Use adequate spacing to group related elements visually"
        }
    
    def validate_spacing_accessibility(self, element_properties: Dict[str, Any]) -> Dict[str, bool]:
        """Validate spacing accessibility of an element."""
        results = {}
        
        # Check touch target size
        width = element_properties.get('width', 0)
        height = element_properties.get('height', 0)
        results['meets_touch_target_size'] = self.validate_touch_target_size(width, height)
        
        # Check element separation
        margin = element_properties.get('margin', 0)
        min_separation = self._get_minimum_spacing_for_level(self._current_level)
        results['has_adequate_separation'] = margin >= min_separation
        
        # Check focus indicator spacing
        focus_offset = element_properties.get('focus_offset', 0)
        required_offset = self._get_focus_indicator_offset()
        results['has_adequate_focus_spacing'] = focus_offset >= required_offset
        
        return results


# Global instance for easy access
accessibility_spacing = AccessibilitySpacing()
