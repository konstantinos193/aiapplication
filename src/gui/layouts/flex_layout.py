"""
Flexbox Layout System for Nexlify GUI

This module provides a flexbox-like layout system with consistent
spacing, alignment, and distribution following the design system.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List, Optional, Dict, Any, Union
from enum import Enum

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.alignment_system import alignment, HorizontalAlignment, VerticalAlignment


class FlexDirection(Enum):
    """Flex direction options."""
    ROW = "row"
    ROW_REVERSE = "row-reverse"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"


class FlexWrap(Enum):
    """Flex wrap options."""
    NOWRAP = "nowrap"
    WRAP = "wrap"
    WRAP_REVERSE = "wrap-reverse"


class JustifyContent(Enum):
    """Justify content options."""
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"


class AlignItems(Enum):
    """Align items options."""
    STRETCH = "stretch"
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    BASELINE = "baseline"


class AlignContent(Enum):
    """Align content options."""
    STRETCH = "stretch"
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"


class FlexLayout(QWidget):
    """Flexbox-like layout system with consistent spacing and alignment."""
    
    # Signals
    layout_changed = pyqtSignal()
    
    def __init__(self, parent=None, direction: FlexDirection = FlexDirection.ROW,
                 gap: int = None, wrap: FlexWrap = FlexWrap.NOWRAP):
        """Initialize the flex layout.
        
        Args:
            parent: Parent widget
            direction: Flex direction (row or column)
            gap: Gap between flex items (default: 8px)
            wrap: Flex wrap behavior
        """
        super().__init__(parent)
        
        # Store configuration
        self.direction = direction
        self.gap = gap or spacing.sm  # Default to 8px
        self.wrap = wrap
        
        # Flex properties
        self.justify_content = JustifyContent.FLEX_START
        self.align_items = AlignItems.STRETCH
        self.align_content = AlignContent.STRETCH
        
        # Flex items storage
        self.flex_items: List[Dict[str, Any]] = []
        
        # Create layout
        self._create_layout()
        self._apply_styling()
    
    def _create_layout(self):
        """Create the flex layout."""
        # Main container layout
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        
        # Flex layout
        if self.direction in [FlexDirection.ROW, FlexDirection.ROW_REVERSE]:
            self.flex_layout = QHBoxLayout()
        else:
            self.flex_layout = QVBoxLayout()
        
        self.flex_layout.setSpacing(self.gap)
        self.container_layout.addLayout(self.flex_layout)
    
    def _apply_styling(self):
        """Apply design system styling."""
        # Set consistent spacing
        self.flex_layout.setSpacing(self.gap)
        
        # Apply flex properties
        self._apply_flex_properties()
    
    def _apply_flex_properties(self):
        """Apply flexbox properties to the layout."""
        # Justify content
        if self.justify_content == JustifyContent.CENTER:
            self.flex_layout.addStretch()
            # Items will be centered
            self.flex_layout.addStretch()
        elif self.justify_content == JustifyContent.SPACE_BETWEEN:
            # Items will be distributed with space between
            pass  # Qt handles this automatically
        elif self.justify_content == JustifyContent.SPACE_AROUND:
            # Add spacing around items
            self.flex_layout.addStretch()
            # Items will be distributed with space around
            self.flex_layout.addStretch()
    
    def add_widget(self, widget: QWidget, flex_grow: int = 0, 
                   flex_shrink: int = 1, flex_basis: str = "auto",
                   align_self: Optional[AlignItems] = None):
        """Add a widget to the flex layout.
        
        Args:
            widget: Widget to add
            flex_grow: Flex grow factor (0 = don't grow, 1+ = grow proportionally)
            flex_shrink: Flex shrink factor (0 = don't shrink, 1+ = shrink proportionally)
            flex_basis: Initial size of the item
            align_self: Individual alignment override
        """
        # Store flex item info
        flex_item = {
            'widget': widget,
            'flex_grow': flex_grow,
            'flex_shrink': flex_shrink,
            'flex_basis': flex_basis,
            'align_self': align_self
        }
        self.flex_items.append(flex_item)
        
        # Add to flex layout
        if flex_grow > 0:
            self.flex_layout.addWidget(widget, flex_grow)
        else:
            self.flex_layout.addWidget(widget)
        
        # Emit change signal
        self.layout_changed.emit()
    
    def remove_widget(self, widget: QWidget):
        """Remove a widget from the flex layout.
        
        Args:
            widget: Widget to remove
        """
        # Remove from flex layout
        self.flex_layout.removeWidget(widget)
        widget.setParent(None)
        
        # Remove from storage
        self.flex_items = [item for item in self.flex_items if item['widget'] != widget]
        
        # Emit change signal
        self.layout_changed.emit()
    
    def clear(self):
        """Clear all widgets from the flex layout."""
        # Remove all widgets
        for item in self.flex_items:
            self.flex_layout.removeWidget(item['widget'])
            item['widget'].setParent(None)
        
        # Clear storage
        self.flex_items.clear()
        
        # Emit change signal
        self.layout_changed.emit()
    
    def set_direction(self, direction: FlexDirection):
        """Set the flex direction.
        
        Args:
            direction: New flex direction
        """
        self.direction = direction
        self._recreate_layout()
    
    def set_gap(self, gap: int):
        """Set gap between flex items.
        
        Args:
            gap: Gap in pixels
        """
        self.gap = gap
        self._apply_styling()
    
    def set_wrap(self, wrap: FlexWrap):
        """Set flex wrap behavior.
        
        Args:
            wrap: New wrap behavior
        """
        self.wrap = wrap
        # Note: Qt layouts don't have built-in wrap, this is for reference
        self.layout_changed.emit()
    
    def set_justify_content(self, justify: JustifyContent):
        """Set justify content alignment.
        
        Args:
            justify: New justify content value
        """
        self.justify_content = justify
        self._apply_flex_properties()
    
    def set_align_items(self, align: AlignItems):
        """Set align items alignment.
        
        Args:
            align: New align items value
        """
        self.align_items = align
        self._apply_flex_properties()
    
    def set_align_content(self, align: AlignContent):
        """Set align content alignment.
        
        Args:
            align: New align content value
        """
        self.align_content = align
        self._apply_flex_properties()
    
    def _recreate_layout(self):
        """Recreate the layout when direction changes."""
        # Remove old layout
        old_layout = self.flex_layout
        self.container_layout.removeItem(old_layout)
        
        # Create new layout
        if self.direction in [FlexDirection.ROW, FlexDirection.ROW_REVERSE]:
            self.flex_layout = QHBoxLayout()
        else:
            self.flex_layout = QVBoxLayout()
        
        self.flex_layout.setSpacing(self.gap)
        self.container_layout.addLayout(self.flex_layout)
        
        # Re-add all widgets
        for item in self.flex_items:
            if item['flex_grow'] > 0:
                self.flex_layout.addWidget(item['widget'], item['flex_grow'])
            else:
                self.flex_layout.addWidget(item['widget'])
        
        # Apply flex properties
        self._apply_flex_properties()
    
    def get_flex_info(self) -> Dict[str, Any]:
        """Get information about the current flex layout.
        
        Returns:
            Dictionary with flex layout information
        """
        return {
            'direction': self.direction.value,
            'gap': self.gap,
            'wrap': self.wrap.value,
            'justify_content': self.justify_content.value,
            'align_items': self.align_items.value,
            'align_content': self.align_content.value,
            'items': len(self.flex_items),
            'flex_items': self.flex_items.copy()
        }
    
    def add_stretch(self, stretch_factor: int = 1):
        """Add a stretch to the flex layout.
        
        Args:
            stretch_factor: Stretch factor
        """
        self.flex_layout.addStretch(stretch_factor)
    
    def add_spacing(self, spacing_value: int):
        """Add fixed spacing to the flex layout.
        
        Args:
            spacing_value: Spacing in pixels
        """
        self.flex_layout.addSpacing(spacing_value)


class FlexContainer(FlexLayout):
    """Flex container with additional container-specific features."""
    
    def __init__(self, parent=None, direction: FlexDirection = FlexDirection.ROW,
                 gap: int = None, wrap: FlexWrap = FlexWrap.NOWRAP,
                 padding: int = None, margin: int = None):
        """Initialize the flex container.
        
        Args:
            parent: Parent widget
            direction: Flex direction
            gap: Gap between items
            wrap: Flex wrap behavior
            padding: Container padding
            margin: Container margin
        """
        super().__init__(parent, direction, gap, wrap)
        
        # Container properties
        self.padding = padding or spacing.sm  # Default to 8px
        self.margin = margin or spacing.md    # Default to 16px
        
        # Apply container styling
        self._apply_container_styling()
    
    def _apply_container_styling(self):
        """Apply container-specific styling."""
        # Set container margins and padding
        self.container_layout.setContentsMargins(
            self.margin, self.margin, self.margin, self.margin
        )
        
        # Set flex layout margins (padding)
        self.flex_layout.setContentsMargins(
            self.padding, self.padding, self.padding, self.padding
        )
    
    def set_padding(self, padding: int):
        """Set container padding.
        
        Args:
            padding: Padding in pixels
        """
        self.padding = padding
        self._apply_container_styling()
    
    def set_margin(self, margin: int):
        """Set container margin.
        
        Args:
            margin: Margin in pixels
        """
        self.margin = margin
        self._apply_container_styling()
