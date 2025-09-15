"""
Responsive Design Module for Nexlify GUI

This module provides responsive design capabilities including:
- Responsive spacing that adjusts to screen size
- Breakpoint-based layout adjustments
- Touch-friendly spacing for mobile devices
"""

from .responsive_spacing import (
    ResponsiveSpacing, ResponsiveSpacingManager, 
    Breakpoint, responsive_spacing_manager
)

__all__ = [
    'ResponsiveSpacing',
    'ResponsiveSpacingManager', 
    'Breakpoint',
    'responsive_spacing_manager'
]
