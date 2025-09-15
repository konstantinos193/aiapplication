#!/usr/bin/env python3
"""
SVG Loader Utility for Nexlify Engine.

This utility provides functions to load SVG files and convert them to QPixmap
objects that can be used as icons in PyQt6 widgets.
"""

import os
from typing import Optional
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import QSize, Qt

# Try to import SVG support, fallback gracefully if not available
try:
    from PyQt6.QtSvg import QSvgRenderer
    SVG_AVAILABLE = True
except ImportError:
    SVG_AVAILABLE = False
    print("Warning: PyQt6.QtSvg not available. SVG icons will not work.")


def load_svg_as_pixmap(svg_path: str, size: QSize = QSize(24, 24), 
                       color: Optional[QColor] = None) -> Optional[QPixmap]:
    """
    Load an SVG file and convert it to a QPixmap.
    
    Args:
        svg_path: Path to the SVG file
        size: Desired size of the pixmap (default: 24x24)
        color: Optional color to override the SVG's currentColor
        
    Returns:
        QPixmap object or None if loading fails
    """
    if not SVG_AVAILABLE:
        print(f"Warning: SVG support not available. Cannot load: {svg_path}")
        return None
        
    try:
        # Check if file exists
        if not os.path.exists(svg_path):
            print(f"Warning: SVG file not found: {svg_path}")
            return None
            
        # Create SVG renderer
        renderer = QSvgRenderer(svg_path)
        if not renderer.isValid():
            print(f"Warning: Invalid SVG file: {svg_path}")
            return None
            
        # Create pixmap
        pixmap = QPixmap(size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        
        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Render SVG first (this will render with default colors)
        renderer.render(painter)
        painter.end()
        
        # If color is specified, create a tinted version
        if color:
            # Create a new pixmap for the result
            result_pixmap = QPixmap(size)
            result_pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
            
            # Create a painter for the result
            result_painter = QPainter(result_pixmap)
            result_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Set the color as the pen and brush
            result_painter.setPen(color)
            result_painter.setBrush(color)
            
            # Draw the SVG with our color
            renderer.render(result_painter)
            
            result_painter.end()
            return result_pixmap
        
        return pixmap
        
    except Exception as e:
        print(f"Error loading SVG {svg_path}: {e}")
        return None


def create_fallback_icon(text: str, size: int = 24, 
                        color: Optional[QColor] = None) -> QPixmap:
    """
    Create a fallback text-based icon when SVG is not available.
    
    Args:
        text: Text to display as icon
        size: Size in pixels (creates square pixmap)
        color: Color for the text (default: white)
        
    Returns:
        QPixmap object with text icon
    """
    if color is None:
        color = QColor(255, 255, 255)  # White default
        
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(color)
    painter.setBrush(color)
    
    # Set font
    font = painter.font()
    font.setPointSize(size // 2)  # Font size is roughly half the icon size
    font.setBold(True)
    painter.setFont(font)
    
    # Center the text
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
    painter.end()
    
    return pixmap


def load_svg_icon(svg_path: str, size: int = 24, 
                  color: Optional[QColor] = None) -> Optional[QPixmap]:
    """
    Convenience function to load SVG as icon with square size.
    
    Args:
        svg_path: Path to the SVG file
        size: Size in pixels (creates square pixmap)
        color: Optional color to override the SVG's currentColor
        
    Returns:
        QPixmap object or None if loading fails
    """
    # Use white color by default for dark themes
    if color is None:
        color = QColor(255, 255, 255)  # White
        
    result = load_svg_as_pixmap(svg_path, QSize(size, size), color)
    
    # If SVG loading fails, create fallback icon
    if result is None:
        # Extract icon name from path for fallback
        icon_name = os.path.basename(svg_path).replace('.svg', '').upper()
        if icon_name == 'PLAY':
            fallback_text = '▶'
        elif icon_name == 'PAUSE':
            fallback_text = '⏸'
        elif icon_name == 'STOP':
            fallback_text = '■'
        else:
            fallback_text = icon_name[0] if icon_name else '?'
            
        result = create_fallback_icon(fallback_text, size, color)
        
    return result
