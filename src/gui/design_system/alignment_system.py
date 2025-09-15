"""
Alignment System for Nexlify GUI

This module provides consistent alignment standards and utilities
for proper visual hierarchy and professional appearance.
"""

from enum import Enum
from typing import Union, Tuple


class HorizontalAlignment(Enum):
    """Horizontal alignment options."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    STRETCH = "stretch"


class VerticalAlignment(Enum):
    """Vertical alignment options."""
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    STRETCH = "stretch"


class TextAlignment(Enum):
    """Text alignment options."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class AlignmentSystem:
    """Centralized alignment system for consistent UI alignment."""
    
    def __init__(self):
        """Initialize the alignment system."""
        # Standard alignment patterns
        self.label_alignment = TextAlignment.RIGHT      # Labels right-aligned
        self.input_alignment = TextAlignment.LEFT       # Inputs left-aligned
        self.button_alignment = HorizontalAlignment.CENTER  # Buttons centered
        self.header_alignment = TextAlignment.LEFT      # Headers left-aligned
        self.status_alignment = TextAlignment.LEFT      # Status text left-aligned
        
        # Component alignment
        self.panel_header_align = HorizontalAlignment.LEFT
        self.panel_content_align = HorizontalAlignment.STRETCH
        self.toolbar_align = HorizontalAlignment.LEFT
        self.statusbar_align = HorizontalAlignment.LEFT
        
    def get_horizontal_alignment(self, alignment: Union[HorizontalAlignment, str]) -> str:
        """Get horizontal alignment value.
        
        Args:
            alignment: Horizontal alignment enum or string value
            
        Returns:
            Alignment string value
        """
        if isinstance(alignment, HorizontalAlignment):
            return alignment.value
        return str(alignment)
    
    def get_vertical_alignment(self, alignment: Union[VerticalAlignment, str]) -> str:
        """Get vertical alignment value.
        
        Args:
            alignment: Vertical alignment enum or string value
            
        Returns:
            Alignment string value
        """
        if isinstance(alignment, VerticalAlignment):
            return alignment.value
        return str(alignment)
    
    def get_text_alignment(self, alignment: Union[TextAlignment, str]) -> str:
        """Get text alignment value.
        
        Args:
            alignment: Text alignment enum or string value
            
        Returns:
            Alignment string value
        """
        if isinstance(alignment, TextAlignment):
            return alignment.value
        return str(alignment)
    
    def get_label_alignment(self) -> str:
        """Get standard label alignment.
        
        Returns:
            Label alignment value
        """
        return self.get_text_alignment(self.label_alignment)
    
    def get_input_alignment(self) -> str:
        """Get standard input alignment.
        
        Returns:
            Input alignment value
        """
        return self.get_text_alignment(self.input_alignment)
    
    def get_button_alignment(self) -> str:
        """Get standard button alignment.
        
        Returns:
            Button alignment value
        """
        return self.get_horizontal_alignment(self.button_alignment)
    
    def get_header_alignment(self) -> str:
        """Get standard header alignment.
        
        Returns:
            Header alignment value
        """
        return self.get_text_alignment(self.header_alignment)
    
    def get_panel_alignment(self) -> Tuple[str, str]:
        """Get standard panel alignment.
        
        Returns:
            Tuple of (header_alignment, content_alignment) values
        """
        return (
            self.get_horizontal_alignment(self.panel_header_align),
            self.get_horizontal_alignment(self.panel_content_align)
        )
    
    def get_toolbar_alignment(self) -> str:
        """Get standard toolbar alignment.
        
        Returns:
            Toolbar alignment value
        """
        return self.get_horizontal_alignment(self.toolbar_align)
    
    def get_statusbar_alignment(self) -> str:
        """Get standard statusbar alignment.
        
        Returns:
            Statusbar alignment value
        """
        return self.get_horizontal_alignment(self.statusbar_align)


# Global alignment system instance
alignment = AlignmentSystem()


# Utility functions for quick access
def h_align(align: Union[HorizontalAlignment, str]) -> str:
    """Quick horizontal alignment access.
    
    Args:
        align: Horizontal alignment enum or string value
        
    Returns:
        Alignment string value
    """
    return alignment.get_horizontal_alignment(align)


def v_align(align: Union[VerticalAlignment, str]) -> str:
    """Quick vertical alignment access.
    
    Args:
        align: Vertical alignment enum or string value
        
    Returns:
        Alignment string value
    """
    return alignment.get_vertical_alignment(align)


def t_align(align: Union[TextAlignment, str]) -> str:
    """Quick text alignment access.
    
    Args:
        align: Text alignment enum or string value
        
    Returns:
        Alignment string value
    """
    return alignment.get_text_alignment(align)
