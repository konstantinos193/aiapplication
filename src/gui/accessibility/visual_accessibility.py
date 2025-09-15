"""
Visual accessibility system for improved visual feedback.

This module provides:
- Focus indicators
- Visual error indicators
- Accessible icon system
- Visual hierarchy improvements
- Visual feedback enhancements
"""

from typing import Dict, Tuple, Optional, List, Any
from dataclasses import dataclass
from enum import Enum
import logging

from gui.utils.logger import get_logger


class FocusIndicatorStyle(Enum):
    """Styles for focus indicators."""
    OUTLINE = "outline"
    BACKGROUND = "background"
    UNDERLINE = "underline"
    GLOW = "glow"
    BORDER = "border"


class VisualFeedbackType(Enum):
    """Types of visual feedback."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    NEUTRAL = "neutral"


@dataclass(frozen=True)
class FocusIndicator:
    """Focus indicator configuration."""
    style: FocusIndicatorStyle
    color: str
    width: int
    radius: int
    visible: bool = True


@dataclass(frozen=True)
class VisualFeedback:
    """Visual feedback configuration."""
    type: VisualFeedbackType
    color: str
    icon: str
    message: str
    duration: float = 3.0


class VisualAccessibility:
    """Visual accessibility system for improved visual feedback."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._focus_indicators_enabled = True
        self._high_visibility_mode = False
        self._reduced_motion = False
        
        # Focus indicator styles
        self._focus_indicator_styles = {
            FocusIndicatorStyle.OUTLINE: FocusIndicator(
                style=FocusIndicatorStyle.OUTLINE,
                color="#0078D4",
                width=2,
                radius=4
            ),
            FocusIndicatorStyle.BACKGROUND: FocusIndicator(
                style=FocusIndicatorStyle.BACKGROUND,
                color="#0078D4",
                width=0,
                radius=4
            ),
            FocusIndicatorStyle.UNDERLINE: FocusIndicator(
                style=FocusIndicatorStyle.UNDERLINE,
                color="#0078D4",
                width=3,
                radius=0
            ),
            FocusIndicatorStyle.GLOW: FocusIndicator(
                style=FocusIndicatorStyle.GLOW,
                color="#0078D4",
                width=4,
                radius=8
            ),
            FocusIndicatorStyle.BORDER: FocusIndicator(
                style=FocusIndicatorStyle.BORDER,
                color="#0078D4",
                width=2,
                radius=4
            )
        }
        
        # Visual feedback colors
        self._feedback_colors = {
            VisualFeedbackType.SUCCESS: "#107C10",
            VisualFeedbackType.ERROR: "#D13438",
            VisualFeedbackType.WARNING: "#FF8C00",
            VisualFeedbackType.INFO: "#0078D4",
            VisualFeedbackType.NEUTRAL: "#605E5C"
        }
        
        # High visibility mode colors
        self._high_visibility_colors = {
            'focus': "#FFFF00",      # Bright yellow
            'error': "#FF0000",      # Bright red
            'success': "#00FF00",    # Bright green
            'warning': "#FFA500",    # Bright orange
            'info': "#00FFFF"        # Bright cyan
        }
        
        self.logger.info("VisualAccessibility system initialized")
    
    def get_focus_indicator_style(self, style: FocusIndicatorStyle = None) -> FocusIndicator:
        """Get focus indicator configuration for given style."""
        if style is None:
            style = FocusIndicatorStyle.OUTLINE
        
        base_style = self._focus_indicator_styles.get(style, self._focus_indicator_styles[FocusIndicatorStyle.OUTLINE])
        
        if self._high_visibility_mode:
            # Use high visibility colors
            return FocusIndicator(
                style=base_style.style,
                color=self._high_visibility_colors['focus'],
                width=base_style.width + 1,  # Slightly thicker
                radius=base_style.radius,
                visible=base_style.visible
            )
        
        return base_style
    
    def get_focus_indicator_css(self, style: FocusIndicatorStyle = None) -> str:
        """Get CSS for focus indicator."""
        indicator = self.get_focus_indicator_style(style)
        
        if not indicator.visible:
            return ""
        
        css_parts = []
        
        if indicator.style == FocusIndicatorStyle.OUTLINE:
            css_parts.append(f"outline: {indicator.width}px solid {indicator.color}")
            css_parts.append(f"outline-offset: 2px")
        elif indicator.style == FocusIndicatorStyle.BACKGROUND:
            css_parts.append(f"background-color: {indicator.color}")
            css_parts.append(f"border-radius: {indicator.radius}px")
        elif indicator.style == FocusIndicatorStyle.UNDERLINE:
            css_parts.append(f"border-bottom: {indicator.width}px solid {indicator.color}")
        elif indicator.style == FocusIndicatorStyle.GLOW:
            css_parts.append(f"box-shadow: 0 0 {indicator.width}px {indicator.radius}px {indicator.color}")
        elif indicator.style == FocusIndicatorStyle.BORDER:
            css_parts.append(f"border: {indicator.width}px solid {indicator.color}")
            css_parts.append(f"border-radius: {indicator.radius}px")
        
        return "; ".join(css_parts)
    
    def get_visual_feedback_color(self, feedback_type: VisualFeedbackType) -> str:
        """Get color for visual feedback type."""
        base_color = self._feedback_colors.get(feedback_type, self._feedback_colors[VisualFeedbackType.NEUTRAL])
        
        if self._high_visibility_mode:
            return self._high_visibility_colors.get(feedback_type.value, base_color)
        
        return base_color
    
    def create_error_indicator(self, message: str, severity: str = "error") -> VisualFeedback:
        """Create visual error indicator."""
        feedback_type = VisualFeedbackType.ERROR if severity == "error" else VisualFeedbackType.WARNING
        color = self.get_visual_feedback_color(feedback_type)
        
        return VisualFeedback(
            type=feedback_type,
            color=color,
            icon="⚠️" if severity == "warning" else "❌",
            message=message
        )
    
    def create_success_indicator(self, message: str) -> VisualFeedback:
        """Create visual success indicator."""
        return VisualFeedback(
            type=VisualFeedbackType.SUCCESS,
            color=self.get_visual_feedback_color(VisualFeedbackType.SUCCESS),
            icon="✅",
            message=message
        )
    
    def create_info_indicator(self, message: str) -> VisualFeedback:
        """Create visual info indicator."""
        return VisualFeedback(
            type=VisualFeedbackType.INFO,
            color=self.get_visual_feedback_color(VisualFeedbackType.INFO),
            icon="ℹ️",
            message=message
        )
    
    def enable_focus_indicators(self, enabled: bool = True) -> None:
        """Enable or disable focus indicators."""
        self._focus_indicators_enabled = enabled
        self.logger.info(f"Focus indicators {'enabled' if enabled else 'disabled'}")
    
    def are_focus_indicators_enabled(self) -> bool:
        """Check if focus indicators are enabled."""
        return self._focus_indicators_enabled
    
    def enable_high_visibility_mode(self, enabled: bool = True) -> None:
        """Enable or disable high visibility mode."""
        self._high_visibility_mode = enabled
        self.logger.info(f"High visibility mode {'enabled' if enabled else 'disabled'}")
    
    def is_high_visibility_mode_enabled(self) -> bool:
        """Check if high visibility mode is enabled."""
        return self._high_visibility_mode
    
    def enable_reduced_motion(self, enabled: bool = True) -> None:
        """Enable or disable reduced motion mode."""
        self._reduced_motion = enabled
        self.logger.info(f"Reduced motion mode {'enabled' if enabled else 'disabled'}")
    
    def is_reduced_motion_enabled(self) -> bool:
        """Check if reduced motion mode is enabled."""
        return self._reduced_motion
    
    def get_accessible_icon_style(self, icon_name: str, size: int = 16) -> Dict[str, Any]:
        """Get accessible icon styling."""
        base_style = {
            'size': size,
            'color': self.get_visual_feedback_color(VisualFeedbackType.INFO),
            'background': 'transparent',
            'border_radius': 2,
            'padding': 4
        }
        
        if self._high_visibility_mode:
            base_style['color'] = self._high_visibility_colors['info']
            base_style['background'] = '#000000'
            base_style['border_radius'] = 4
            base_style['padding'] = 6
        
        return base_style
    
    def get_visual_hierarchy_css(self, level: int = 1) -> str:
        """Get CSS for visual hierarchy improvements."""
        css_parts = []
        
        # Increase contrast and size for higher levels
        if level == 1:  # Primary elements
            css_parts.append("font-weight: bold")
            css_parts.append("font-size: 1.2em")
        elif level == 2:  # Secondary elements
            css_parts.append("font-weight: 600")
            css_parts.append("font-size: 1.1em")
        elif level == 3:  # Tertiary elements
            css_parts.append("font-weight: normal")
            css_parts.append("font-size: 1.0em")
        
        # Add spacing for better visual separation
        if level <= 2:
            css_parts.append("margin-bottom: 8px")
        
        return "; ".join(css_parts)
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for visual elements."""
        return {
            'focus': "Always provide visible focus indicators",
            'contrast': "Ensure sufficient contrast for all visual elements",
            'icons': "Don't rely solely on icons - provide text labels",
            'motion': "Respect user's motion preferences",
            'hierarchy': "Use visual hierarchy to organize information clearly",
            'feedback': "Provide clear visual feedback for all user actions"
        }
    
    def validate_visual_accessibility(self, element_type: str, properties: Dict[str, Any]) -> Dict[str, bool]:
        """Validate visual accessibility of an element."""
        results = {}
        
        # Check focus indicators
        results['has_focus_indicator'] = properties.get('focus_visible', False)
        
        # Check contrast
        results['has_sufficient_contrast'] = properties.get('contrast_ratio', 0) >= 4.5
        
        # Check text alternatives for icons
        results['has_text_alternative'] = bool(properties.get('alt_text', '') or properties.get('aria_label', ''))
        
        # Check visual feedback
        results['has_visual_feedback'] = properties.get('feedback_visible', False)
        
        return results


# Global instance for easy access
visual_accessibility = VisualAccessibility()
