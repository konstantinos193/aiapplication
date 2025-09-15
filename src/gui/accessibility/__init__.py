"""
Accessibility module for the GUI system.

This module provides comprehensive accessibility support including:
- Text legibility and visual accessibility
- Keyboard navigation system
- Screen reader support
- Component accessibility
- Accessibility testing and compliance
"""

from .typography_system import TypographyAccessibility
from .color_accessibility import ColorAccessibility
from .visual_accessibility import VisualAccessibility
from .accessibility_spacing import AccessibilitySpacing
from .keyboard_navigation import KeyboardNavigation
from .focus_management import FocusManagement
from .keyboard_shortcuts import KeyboardShortcuts
from .aria_system import AriaSystem
from .screen_reader_integration import ScreenReaderIntegration
from .semantic_structure import SemanticStructure

__all__ = [
    'TypographyAccessibility',
    'ColorAccessibility', 
    'VisualAccessibility',
    'AccessibilitySpacing',
    'KeyboardNavigation',
    'FocusManagement',
    'KeyboardShortcuts',
    'AriaSystem',
    'ScreenReaderIntegration',
    'SemanticStructure'
]
