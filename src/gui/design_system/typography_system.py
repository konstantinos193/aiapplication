"""
Typography System for Nexlify GUI

This module provides consistent typography standards including
font sizes, line heights, and text styling for professional appearance.
"""

from enum import Enum
from typing import Union, Tuple


class FontSize(Enum):
    """Standard font sizes based on 2px increments."""
    XS = 10   # 10px - Very small text (captions, footnotes)
    SM = 12   # 12px - Small text (labels, secondary info)
    MD = 14   # 14px - Medium text (body text, descriptions)
    LG = 16   # 16px - Large text (subheadings, emphasis)
    XL = 18   # 18px - Extra large text (section headers)
    XXL = 20  # 20px - Double extra large text (panel headers)
    XXXL = 24 # 24px - Triple extra large text (main headers)
    TITLE = 32 # 32px - Title text (window headers)


class FontWeight(Enum):
    """Font weight options."""
    LIGHT = 300
    NORMAL = 400
    MEDIUM = 500
    SEMIBOLD = 600
    BOLD = 700
    EXTRABOLD = 800


class LineHeight(Enum):
    """Line height options for text readability."""
    TIGHT = 1.2    # Tight spacing for headers
    NORMAL = 1.4   # Normal spacing for body text
    RELAXED = 1.6  # Relaxed spacing for readability
    LOOSE = 1.8    # Loose spacing for emphasis


class TypographySystem:
    """Centralized typography system for consistent text styling."""
    
    def __init__(self):
        """Initialize the typography system."""
        # Font sizes
        self.xs = FontSize.XS.value      # 10px
        self.sm = FontSize.SM.value      # 12px
        self.md = FontSize.MD.value      # 14px
        self.lg = FontSize.LG.value      # 16px
        self.xl = FontSize.XL.value      # 18px
        self.xxl = FontSize.XXL.value    # 20px
        self.xxxl = FontSize.XXXL.value  # 24px
        self.title = FontSize.TITLE.value # 32px
        
        # Font weights
        self.light = int(FontWeight.LIGHT.value)
        self.normal = int(FontWeight.NORMAL.value)
        self.medium = int(FontWeight.MEDIUM.value)
        self.semibold = int(FontWeight.SEMIBOLD.value)
        self.bold = int(FontWeight.BOLD.value)
        self.extrabold = int(FontWeight.EXTRABOLD.value)
        
        # Line heights
        self.line_tight = LineHeight.TIGHT.value
        self.line_normal = LineHeight.NORMAL.value
        self.line_relaxed = LineHeight.RELAXED.value
        self.line_loose = LineHeight.LOOSE.value
        
        # Standard typography patterns
        self.caption_size = self.xs
        self.caption_weight = self.normal
        self.caption_line_height = self.line_tight
        
        self.label_size = self.sm
        self.label_weight = self.medium
        self.label_line_height = self.line_normal
        
        self.body_size = self.md
        self.body_weight = self.normal
        self.body_line_height = self.line_relaxed
        
        self.header_size = self.lg
        self.header_weight = self.semibold
        self.header_line_height = self.line_tight
        
        self.title_size = self.xxl
        self.title_weight = self.bold
        self.title_line_height = self.line_tight
        
        self.main_title_size = self.title
        self.main_title_weight = self.extrabold
        self.main_title_line_height = self.line_tight
        
    def get_font_size(self, size: Union[FontSize, int]) -> int:
        """Get font size value.
        
        Args:
            size: Font size enum or integer value
            
        Returns:
            Font size value in pixels
        """
        if isinstance(size, FontSize):
            return size.value
        return size
    
    def get_font_weight(self, weight: Union[FontWeight, int]) -> int:
        """Get font weight value.
        
        Args:
            weight: Font weight enum or integer value
            
        Returns:
            Font weight value
        """
        if isinstance(weight, FontWeight):
            return weight.value
        return weight
    
    def get_line_height(self, height: Union[LineHeight, float]) -> float:
        """Get line height value.
        
        Args:
            height: Line height enum or float value
            
        Returns:
            Line height value
        """
        if isinstance(height, LineHeight):
            return height.value
        return float(height)
    
    def get_caption_style(self) -> Tuple[int, int, float]:
        """Get standard caption text style.
        
        Returns:
            Tuple of (size, weight, line_height) values
        """
        return (self.caption_size, int(self.caption_weight), self.caption_line_height)
    
    def get_label_style(self) -> Tuple[int, int, float]:
        """Get standard label text style.
        
        Returns:
            Tuple of (size, weight, line_height) values
        """
        return (self.label_size, int(self.label_weight), self.label_line_height)
    
    def get_body_style(self) -> Tuple[int, int, float]:
        """Get standard body text style.
        
        Returns:
            Tuple of (size, weight, line_height) values
        """
        return (self.body_size, int(self.body_weight), self.body_line_height)
    
    def get_header_style(self) -> Tuple[int, int, float]:
        """Get standard header text style.
        
        Returns:
            Tuple of (size, weight, line_height) values
        """
        return (self.header_size, int(self.header_weight), self.header_line_height)
    
    def get_title_style(self) -> Tuple[int, int, float]:
        """Get standard title text style.
        
        Returns:
            Tuple of (size, weight, line_height) values
        """
        return (self.title_size, int(self.title_weight), self.title_line_height)
    
    def get_main_title_style(self) -> Tuple[int, int, float]:
        """Get standard main title text style.
        
        Returns:
            Tuple of (size, weight, line_height) values
        """
        return (self.main_title_size, int(self.main_title_weight), self.main_title_line_height)
    
    def get_text_style(self, size: Union[FontSize, int], 
                       weight: Union[FontWeight, int] = None,
                       line_height: Union[LineHeight, float] = None) -> Tuple[int, int, float]:
        """Get custom text style.
        
        Args:
            size: Font size enum or integer value
            weight: Font weight enum or integer value (defaults to normal)
            line_height: Line height enum or float value (defaults to normal)
            
        Returns:
            Tuple of (size, weight, line_height) values
        """
        font_size = self.get_font_size(size)
        font_weight = self.get_font_weight(weight) if weight else self.normal
        line_height_val = self.get_line_height(line_height) if line_height else self.normal
        
        return (font_size, font_weight, line_height_val)


# Global typography system instance
typography = TypographySystem()


# Utility functions for quick access
def fs(size: Union[FontSize, int]) -> int:
    """Quick font size access.
    
    Args:
        size: Font size enum or integer value
        
    Returns:
        Font size value in pixels
    """
    return typography.get_font_size(size)


def fw(weight: Union[FontWeight, int]) -> int:
    """Quick font weight access.
    
    Args:
        weight: Font weight enum or integer value
        
    Returns:
        Font weight value
    """
    return typography.get_font_weight(weight)


def lh(height: Union[LineHeight, float]) -> float:
    """Quick line height access.
    
    Args:
        height: Line height enum or float value
        
    Returns:
        Line height value
    """
    return typography.get_line_height(height)
