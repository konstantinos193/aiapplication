"""
Spacing System for Nexlify GUI

This module provides a consistent spacing system based on an 8px grid system
that ensures visual harmony and professional appearance across all UI components.
"""

from typing import Union, Tuple
from enum import Enum


class SpacingUnit(Enum):
    """Standard spacing units based on 8px grid system."""
    XS = 4    # 4px - Minimal spacing
    SM = 8    # 8px - Small spacing
    MD = 12   # 12px - Medium spacing
    LG = 16   # 16px - Large spacing
    XL = 24   # 24px - Extra large spacing
    XXL = 32  # 32px - Double extra large spacing
    XXXL = 48 # 48px - Triple extra large spacing


class SpacingSystem:
    """Centralized spacing system for consistent UI spacing."""
    
    def __init__(self):
        """Initialize the spacing system."""
        # Base spacing values
        self.xs = SpacingUnit.XS.value      # 4px
        self.sm = SpacingUnit.SM.value      # 8px
        self.md = SpacingUnit.MD.value      # 12px
        self.lg = SpacingUnit.LG.value      # 16px
        self.xl = SpacingUnit.XL.value      # 24px
        self.xxl = SpacingUnit.XXL.value    # 32px
        self.xxxl = SpacingUnit.XXXL.value  # 48px
        
        # Common spacing patterns
        self.panel_margin = self.lg         # 16px - Standard panel margin
        self.panel_padding = self.md        # 12px - Standard panel padding
        self.section_spacing = self.lg      # 16px - Between sections
        self.item_spacing = self.sm         # 8px - Between items
        self.field_spacing = self.md        # 12px - Between form fields
        self.button_spacing = self.sm       # 8px - Between buttons
        self.icon_spacing = self.xs         # 4px - Around icons
        
        # Component-specific spacing
        self.button_height = self.xxl       # 32px - Standard button height
        self.input_height = self.xxl        # 32px - Standard input height
        self.tree_indent = self.lg          # 16px - Tree view indentation
        self.selection_padding = self.xs    # 4px - Selection highlight padding
        
    def get_spacing(self, unit: Union[SpacingUnit, int]) -> int:
        """Get spacing value for a given unit.
        
        Args:
            unit: Spacing unit enum or integer value
            
        Returns:
            Spacing value in pixels
        """
        if isinstance(unit, SpacingUnit):
            return unit.value
        return unit
    
    def margin(self, unit: Union[SpacingUnit, int]) -> int:
        """Get margin spacing value.
        
        Args:
            unit: Spacing unit enum or integer value
            
        Returns:
            Margin value in pixels
        """
        return self.get_spacing(unit)
    
    def padding(self, unit: Union[SpacingUnit, int]) -> int:
        """Get padding spacing value.
        
        Args:
            unit: Spacing unit enum or integer value
            
        Returns:
            Padding value in pixels
        """
        return self.get_spacing(unit)
    
    def spacing(self, unit: Union[SpacingUnit, int]) -> int:
        """Get general spacing value.
        
        Args:
            unit: Spacing unit enum or integer value
            
        Returns:
            Spacing value in pixels
        """
        return self.get_spacing(unit)
    
    def get_panel_spacing(self) -> Tuple[int, int]:
        """Get standard panel spacing (margin, padding).
        
        Returns:
            Tuple of (margin, padding) values
        """
        return (self.panel_margin, self.panel_padding)
    
    def get_section_spacing(self) -> int:
        """Get spacing between sections.
        
        Returns:
            Section spacing value in pixels
        """
        return self.section_spacing
    
    def get_item_spacing(self) -> int:
        """Get spacing between items.
        
        Returns:
            Item spacing value in pixels
        """
        return self.item_spacing
    
    def get_field_spacing(self) -> int:
        """Get spacing between form fields.
        
        Returns:
            Field spacing value in pixels
        """
        return self.field_spacing
    
    def get_button_spacing(self) -> int:
        """Get spacing between buttons.
        
        Returns:
            Button spacing value in pixels
        """
        return self.button_spacing
    
    def get_component_heights(self) -> Tuple[int, int]:
        """Get standard component heights.
        
        Returns:
            Tuple of (button_height, input_height) values
        """
        return (self.button_height, self.input_height)


# Global spacing system instance
spacing = SpacingSystem()


# Utility functions for quick access
def m(unit: Union[SpacingUnit, int]) -> int:
    """Quick margin access.
    
    Args:
        unit: Spacing unit enum or integer value
        
    Returns:
        Margin value in pixels
    """
    return spacing.margin(unit)


def p(unit: Union[SpacingUnit, int]) -> int:
    """Quick padding access.
    
    Args:
        unit: Spacing unit enum or integer value
        
    Returns:
        Padding value in pixels
    """
    return spacing.padding(unit)


def s(unit: Union[SpacingUnit, int]) -> int:
    """Quick spacing access.
    
    Args:
        unit: Spacing unit enum or integer value
        
    Returns:
        Spacing value in pixels
    """
    return spacing.spacing(unit)
