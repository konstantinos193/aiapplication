"""
Grid Layout System for Nexlify GUI

This module provides a CSS Grid-like layout system with consistent
spacing, alignment, and responsive breakpoints following the design system.
"""

from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List, Tuple, Optional, Dict, Any

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.alignment_system import alignment, HorizontalAlignment, VerticalAlignment


class GridLayout(QWidget):
    """Grid layout system with consistent spacing and alignment."""
    
    # Signals
    layout_changed = pyqtSignal()
    
    def __init__(self, parent=None, columns: int = 12, 
                 gap: int = None, row_gap: int = None, column_gap: int = None):
        """Initialize the grid layout.
        
        Args:
            parent: Parent widget
            columns: Number of columns in the grid (default: 12)
            gap: Uniform gap between grid items (default: 16px)
            row_gap: Gap between rows (overrides gap if specified)
            column_gap: Gap between columns (overrides gap if specified)
        """
        super().__init__(parent)
        
        # Store configuration
        self.columns = columns
        self.gap = gap or spacing.md  # Default to 16px
        self.row_gap = row_gap or self.gap
        self.column_gap = column_gap or self.gap
        
        # Grid items storage
        self.grid_items: List[Dict[str, Any]] = []
        
        # Create layout
        self._create_layout()
        self._apply_styling()
    
    def _create_layout(self):
        """Create the grid layout."""
        # Main container layout
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        
        # Grid layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(self.column_gap)
        self.container_layout.addLayout(self.grid_layout)
    
    def _apply_styling(self):
        """Apply design system styling."""
        # Set consistent spacing
        self.grid_layout.setSpacing(self.column_gap)
        self.grid_layout.setVerticalSpacing(self.row_gap)
        self.grid_layout.setHorizontalSpacing(self.column_gap)
    
    def add_widget(self, widget: QWidget, row: int, column: int, 
                   row_span: int = 1, column_span: int = 1,
                   alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop):
        """Add a widget to the grid at specified position.
        
        Args:
            widget: Widget to add
            row: Row position (0-based)
            column: Column position (0-based)
            row_span: Number of rows to span
            column_span: Number of columns to span
            alignment: Widget alignment within its grid cell
        """
        # Store grid item info
        grid_item = {
            'widget': widget,
            'row': row,
            'column': column,
            'row_span': row_span,
            'column_span': column_span,
            'alignment': alignment
        }
        self.grid_items.append(grid_item)
        
        # Add to grid layout
        self.grid_layout.addWidget(widget, row, column, row_span, column_span, alignment)
        
        # Emit change signal
        self.layout_changed.emit()
    
    def remove_widget(self, widget: QWidget):
        """Remove a widget from the grid.
        
        Args:
            widget: Widget to remove
        """
        # Remove from grid layout
        self.grid_layout.removeWidget(widget)
        widget.setParent(None)
        
        # Remove from storage
        self.grid_items = [item for item in self.grid_items if item['widget'] != widget]
        
        # Emit change signal
        self.layout_changed.emit()
    
    def clear(self):
        """Clear all widgets from the grid."""
        # Remove all widgets
        for item in self.grid_items:
            self.grid_layout.removeWidget(item['widget'])
            item['widget'].setParent(None)
        
        # Clear storage
        self.grid_items.clear()
        
        # Emit change signal
        self.layout_changed.emit()
    
    def set_gap(self, gap: int):
        """Set uniform gap between grid items.
        
        Args:
            gap: Gap in pixels
        """
        self.gap = gap
        self.row_gap = gap
        self.column_gap = gap
        self._apply_styling()
    
    def set_row_gap(self, row_gap: int):
        """Set gap between rows.
        
        Args:
            row_gap: Row gap in pixels
        """
        self.row_gap = row_gap
        self._apply_styling()
    
    def set_column_gap(self, column_gap: int):
        """Set gap between columns.
        
        Args:
            column_gap: Column gap in pixels
        """
        self.column_gap = column_gap
        self._apply_styling()
    
    def get_widget_at(self, row: int, column: int) -> Optional[QWidget]:
        """Get widget at specified grid position.
        
        Args:
            row: Row position
            column: Column position
            
        Returns:
            Widget at position or None if empty
        """
        for item in self.grid_items:
            if (item['row'] == row and item['column'] == column):
                return item['widget']
        return None
    
    def get_widget_position(self, widget: QWidget) -> Optional[Tuple[int, int]]:
        """Get grid position of a widget.
        
        Args:
            widget: Widget to find
            
        Returns:
            Tuple of (row, column) or None if not found
        """
        for item in self.grid_items:
            if item['widget'] == widget:
                return (item['row'], item['column'])
        return None
    
    def set_widget_alignment(self, widget: QWidget, alignment: Qt.AlignmentFlag):
        """Set alignment of a widget within its grid cell.
        
        Args:
            widget: Widget to align
            alignment: New alignment
        """
        # Find and update widget
        for item in self.grid_items:
            if item['widget'] == widget:
                item['alignment'] = alignment
                
                # Remove and re-add with new alignment
                self.grid_layout.removeWidget(widget)
                self.grid_layout.addWidget(widget, item['row'], item['column'], 
                                         item['row_span'], item['column_span'], alignment)
                break
    
    def get_grid_info(self) -> Dict[str, Any]:
        """Get information about the current grid layout.
        
        Returns:
            Dictionary with grid information
        """
        return {
            'columns': self.columns,
            'gap': self.gap,
            'row_gap': self.row_gap,
            'column_gap': self.column_gap,
            'items': len(self.grid_items),
            'grid_items': self.grid_items.copy()
        }


class ResponsiveGridLayout(GridLayout):
    """Responsive grid layout with breakpoint-based behavior."""
    
    def __init__(self, parent=None, columns: int = 12, 
                 breakpoints: Dict[str, int] = None):
        """Initialize the responsive grid layout.
        
        Args:
            parent: Parent widget
            columns: Number of columns in the grid
            breakpoints: Dictionary of breakpoint names to column counts
                        (e.g., {'mobile': 4, 'tablet': 8, 'desktop': 12})
        """
        super().__init__(parent, columns)
        
        # Default breakpoints
        self.breakpoints = breakpoints or {
            'mobile': 4,      # 4 columns on mobile
            'tablet': 8,      # 8 columns on tablet
            'desktop': 12     # 12 columns on desktop
        }
        
        # Current breakpoint
        self.current_breakpoint = 'desktop'
        
        # Responsive behavior
        self._setup_responsive_behavior()
    
    def _setup_responsive_behavior(self):
        """Setup responsive behavior."""
        # This would typically connect to window resize events
        # For now, we'll provide manual breakpoint switching
        pass
    
    def set_breakpoint(self, breakpoint: str):
        """Set the current breakpoint.
        
        Args:
            breakpoint: Breakpoint name (must exist in breakpoints)
        """
        if breakpoint in self.breakpoints:
            self.current_breakpoint = breakpoint
            self.columns = self.breakpoints[breakpoint]
            self._apply_responsive_layout()
    
    def _apply_responsive_layout(self):
        """Apply responsive layout changes."""
        # Recalculate layout based on current breakpoint
        # This is a simplified implementation
        self.layout_changed.emit()
    
    def get_current_columns(self) -> int:
        """Get the current number of columns based on breakpoint.
        
        Returns:
            Current column count
        """
        return self.breakpoints.get(self.current_breakpoint, self.columns)
    
    def add_breakpoint(self, name: str, columns: int):
        """Add a new breakpoint.
        
        Args:
            name: Breakpoint name
            columns: Number of columns for this breakpoint
        """
        self.breakpoints[name] = columns
    
    def remove_breakpoint(self, name: str):
        """Remove a breakpoint.
        
        Args:
            name: Breakpoint name to remove
        """
        if name in self.breakpoints and name != 'desktop':
            del self.breakpoints[name]
            if self.current_breakpoint == name:
                self.current_breakpoint = 'desktop'
                self.columns = self.breakpoints['desktop']
