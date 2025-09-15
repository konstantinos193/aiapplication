"""
Spacing Utilities for Nexlify GUI

This module provides utility functions for consistent spacing
across the application following the design system.
"""

from PyQt6.QtWidgets import QWidget, QLayout, QSpacerItem
from PyQt6.QtCore import Qt
from typing import Union, Tuple, Optional

from ..design_system.spacing_system import spacing, SpacingUnit


class SpacingUtilities:
    """Utility class for consistent spacing operations."""
    
    @staticmethod
    def add_margin(widget: QWidget, margin: Union[int, SpacingUnit]) -> None:
        """Add consistent margin to a widget.
        
        Args:
            widget: Widget to add margin to
            margin: Margin value (pixels or SpacingUnit)
        """
        if isinstance(margin, SpacingUnit):
            margin_value = margin.value
        else:
            margin_value = margin
        
        # Get current margins
        current_margins = widget.contentsMargins()
        
        # Add margin to all sides
        widget.setContentsMargins(
            current_margins.left() + margin_value,
            current_margins.top() + margin_value,
            current_margins.right() + margin_value,
            current_margins.bottom() + margin_value
        )
    
    @staticmethod
    def add_padding(widget: QWidget, padding: Union[int, SpacingUnit]) -> None:
        """Add consistent padding to a widget.
        
        Args:
            widget: Widget to add padding to
            padding: Padding value (pixels or SpacingUnit)
        """
        if isinstance(padding, SpacingUnit):
            padding_value = padding.value
        else:
            padding_value = padding
        
        # Get current margins
        current_margins = widget.contentsMargins()
        
        # Add padding to all sides
        widget.setContentsMargins(
            current_margins.left() + padding_value,
            current_margins.top() + padding_value,
            current_margins.right() + padding_value,
            current_margins.bottom() + padding_value
        )
    
    @staticmethod
    def set_margins(widget: QWidget, 
                    left: Union[int, SpacingUnit] = None,
                    top: Union[int, SpacingUnit] = None,
                    right: Union[int, SpacingUnit] = None,
                    bottom: Union[int, SpacingUnit] = None) -> None:
        """Set specific margins for a widget.
        
        Args:
            widget: Widget to set margins for
            left: Left margin
            top: Top margin
            right: Right margin
            bottom: Bottom margin
        """
        # Get current margins
        current_margins = widget.contentsMargins()
        
        # Convert SpacingUnit to pixels
        left_value = left.value if isinstance(left, SpacingUnit) else (left or current_margins.left())
        top_value = top.value if isinstance(top, SpacingUnit) else (top or current_margins.top())
        right_value = right.value if isinstance(right, SpacingUnit) else (right or current_margins.right())
        bottom_value = bottom.value if isinstance(bottom, SpacingUnit) else (bottom or current_margins.bottom())
        
        # Set new margins
        widget.setContentsMargins(left_value, top_value, right_value, bottom_value)
    
    @staticmethod
    def set_padding(widget: QWidget,
                    left: Union[int, SpacingUnit] = None,
                    top: Union[int, SpacingUnit] = None,
                    right: Union[int, SpacingUnit] = None,
                    bottom: Union[int, SpacingUnit] = None) -> None:
        """Set specific padding for a widget.
        
        Args:
            widget: Widget to set padding for
            left: Left padding
            top: Top padding
            right: Right padding
            bottom: Bottom padding
        """
        # For Qt widgets, padding is typically handled through stylesheets
        # This is a helper method that can be extended based on needs
        pass
    
    @staticmethod
    def add_spacing_to_layout(layout: QLayout, spacing_value: Union[int, SpacingUnit]) -> None:
        """Add consistent spacing to a layout.
        
        Args:
            layout: Layout to add spacing to
            spacing_value: Spacing value (pixels or SpacingUnit)
        """
        if isinstance(spacing_value, SpacingUnit):
            spacing_value = spacing_value.value
        
        layout.setSpacing(spacing_value)
    
    @staticmethod
    def add_stretch_to_layout(layout: QLayout, stretch_factor: int = 1) -> None:
        """Add stretch to a layout.
        
        Args:
            layout: Layout to add stretch to
            stretch_factor: Stretch factor
        """
        if hasattr(layout, 'addStretch'):
            layout.addStretch(stretch_factor)
    
    @staticmethod
    def add_spacer_to_layout(layout: QLayout, 
                            width: Union[int, SpacingUnit],
                            height: Union[int, SpacingUnit]) -> None:
        """Add a spacer item to a layout.
        
        Args:
            layout: Layout to add spacer to
            width: Spacer width
            height: Spacer height
        """
        if isinstance(width, SpacingUnit):
            width = width.value
        if isinstance(height, SpacingUnit):
            height = height.value
        
        spacer = QSpacerItem(width, height)
        layout.addItem(spacer)


class MarginUtilities:
    """Utility class for margin operations."""
    
    @staticmethod
    def m_1(widget: QWidget) -> None:
        """Add 4px margin to all sides."""
        SpacingUtilities.add_margin(widget, spacing.xs)
    
    @staticmethod
    def m_2(widget: QWidget) -> None:
        """Add 8px margin to all sides."""
        SpacingUtilities.add_margin(widget, spacing.sm)
    
    @staticmethod
    def m_3(widget: QWidget) -> None:
        """Add 12px margin to all sides."""
        SpacingUtilities.add_margin(widget, spacing.md)
    
    @staticmethod
    def m_4(widget: QWidget) -> None:
        """Add 16px margin to all sides."""
        SpacingUtilities.add_margin(widget, spacing.md)
    
    @staticmethod
    def m_5(widget: QWidget) -> None:
        """Add 24px margin to all sides."""
        SpacingUtilities.add_margin(widget, spacing.lg)
    
    @staticmethod
    def m_6(widget: QWidget) -> None:
        """Add 32px margin to all sides."""
        SpacingUtilities.add_margin(widget, spacing.xl)
    
    @staticmethod
    def mt_1(widget: QWidget) -> None:
        """Add 4px top margin."""
        SpacingUtilities.set_margins(widget, top=spacing.xs)
    
    @staticmethod
    def mt_2(widget: QWidget) -> None:
        """Add 8px top margin."""
        SpacingUtilities.set_margins(widget, top=spacing.sm)
    
    @staticmethod
    def mt_3(widget: QWidget) -> None:
        """Add 12px top margin."""
        SpacingUtilities.set_margins(widget, top=spacing.md)
    
    @staticmethod
    def mt_4(widget: QWidget) -> None:
        """Add 16px top margin."""
        SpacingUtilities.set_margins(widget, top=spacing.md)
    
    @staticmethod
    def mt_5(widget: QWidget) -> None:
        """Add 24px top margin."""
        SpacingUtilities.set_margins(widget, top=spacing.lg)
    
    @staticmethod
    def mt_6(widget: QWidget) -> None:
        """Add 32px top margin."""
        SpacingUtilities.set_margins(widget, top=spacing.xl)
    
    @staticmethod
    def mb_1(widget: QWidget) -> None:
        """Add 4px bottom margin."""
        SpacingUtilities.set_margins(widget, bottom=spacing.xs)
    
    @staticmethod
    def mb_2(widget: QWidget) -> None:
        """Add 8px bottom margin."""
        SpacingUtilities.set_margins(widget, bottom=spacing.sm)
    
    @staticmethod
    def mb_3(widget: QWidget) -> None:
        """Add 12px bottom margin."""
        SpacingUtilities.set_margins(widget, bottom=spacing.md)
    
    @staticmethod
    def mb_4(widget: QWidget) -> None:
        """Add 16px bottom margin."""
        SpacingUtilities.set_margins(widget, bottom=spacing.md)
    
    @staticmethod
    def mb_5(widget: QWidget) -> None:
        """Add 24px bottom margin."""
        SpacingUtilities.set_margins(widget, bottom=spacing.lg)
    
    @staticmethod
    def mb_6(widget: QWidget) -> None:
        """Add 32px bottom margin."""
        SpacingUtilities.set_margins(widget, bottom=spacing.xl)
    
    @staticmethod
    def ml_1(widget: QWidget) -> None:
        """Add 4px left margin."""
        SpacingUtilities.set_margins(widget, left=spacing.xs)
    
    @staticmethod
    def ml_2(widget: QWidget) -> None:
        """Add 8px left margin."""
        SpacingUtilities.set_margins(widget, left=spacing.sm)
    
    @staticmethod
    def ml_3(widget: QWidget) -> None:
        """Add 12px left margin."""
        SpacingUtilities.set_margins(widget, left=spacing.md)
    
    @staticmethod
    def ml_4(widget: QWidget) -> None:
        """Add 16px left margin."""
        SpacingUtilities.set_margins(widget, left=spacing.md)
    
    @staticmethod
    def ml_5(widget: QWidget) -> None:
        """Add 24px left margin."""
        SpacingUtilities.set_margins(widget, left=spacing.lg)
    
    @staticmethod
    def ml_6(widget: QWidget) -> None:
        """Add 32px left margin."""
        SpacingUtilities.set_margins(widget, left=spacing.xl)
    
    @staticmethod
    def mr_1(widget: QWidget) -> None:
        """Add 4px right margin."""
        SpacingUtilities.set_margins(widget, right=spacing.xs)
    
    @staticmethod
    def mr_2(widget: QWidget) -> None:
        """Add 8px right margin."""
        SpacingUtilities.set_margins(widget, right=spacing.sm)
    
    @staticmethod
    def mr_3(widget: QWidget) -> None:
        """Add 12px right margin."""
        SpacingUtilities.set_margins(widget, right=spacing.md)
    
    @staticmethod
    def mr_4(widget: QWidget) -> None:
        """Add 16px right margin."""
        SpacingUtilities.set_margins(widget, right=spacing.md)
    
    @staticmethod
    def mr_5(widget: QWidget) -> None:
        """Add 24px right margin."""
        SpacingUtilities.set_margins(widget, right=spacing.lg)
    
    @staticmethod
    def mr_6(widget: QWidget) -> None:
        """Add 32px right margin."""
        SpacingUtilities.set_margins(widget, right=spacing.xl)


class PaddingUtilities:
    """Utility class for padding operations."""
    
    @staticmethod
    def p_1(widget: QWidget) -> None:
        """Add 4px padding to all sides."""
        SpacingUtilities.add_padding(widget, spacing.xs)
    
    @staticmethod
    def p_2(widget: QWidget) -> None:
        """Add 8px padding to all sides."""
        SpacingUtilities.add_padding(widget, spacing.sm)
    
    @staticmethod
    def p_3(widget: QWidget) -> None:
        """Add 12px padding to all sides."""
        SpacingUtilities.add_padding(widget, spacing.md)
    
    @staticmethod
    def p_4(widget: QWidget) -> None:
        """Add 16px padding to all sides."""
        SpacingUtilities.add_padding(widget, spacing.md)
    
    @staticmethod
    def p_5(widget: QWidget) -> None:
        """Add 24px padding to all sides."""
        SpacingUtilities.add_padding(widget, spacing.lg)
    
    @staticmethod
    def p_6(widget: QWidget) -> None:
        """Add 32px padding to all sides."""
        SpacingUtilities.add_padding(widget, spacing.xl)
    
    @staticmethod
    def pt_1(widget: QWidget) -> None:
        """Add 4px top padding."""
        SpacingUtilities.set_padding(widget, top=spacing.xs)
    
    @staticmethod
    def pt_2(widget: QWidget) -> None:
        """Add 8px top padding."""
        SpacingUtilities.set_padding(widget, top=spacing.sm)
    
    @staticmethod
    def pt_3(widget: QWidget) -> None:
        """Add 12px top padding."""
        SpacingUtilities.set_padding(widget, top=spacing.md)
    
    @staticmethod
    def pt_4(widget: QWidget) -> None:
        """Add 16px top padding."""
        SpacingUtilities.set_padding(widget, top=spacing.md)
    
    @staticmethod
    def pt_5(widget: QWidget) -> None:
        """Add 24px top padding."""
        SpacingUtilities.set_padding(widget, top=spacing.lg)
    
    @staticmethod
    def pt_6(widget: QWidget) -> None:
        """Add 32px top padding."""
        SpacingUtilities.set_padding(widget, top=spacing.xl)
    
    @staticmethod
    def pb_1(widget: QWidget) -> None:
        """Add 4px bottom padding."""
        SpacingUtilities.set_padding(widget, bottom=spacing.xs)
    
    @staticmethod
    def pb_2(widget: QWidget) -> None:
        """Add 8px bottom padding."""
        SpacingUtilities.set_padding(widget, bottom=spacing.sm)
    
    @staticmethod
    def pb_3(widget: QWidget) -> None:
        """Add 12px bottom padding."""
        SpacingUtilities.set_padding(widget, bottom=spacing.md)
    
    @staticmethod
    def pb_4(widget: QWidget) -> None:
        """Add 16px bottom padding."""
        SpacingUtilities.set_padding(widget, bottom=spacing.md)
    
    @staticmethod
    def pb_5(widget: QWidget) -> None:
        """Add 24px bottom padding."""
        SpacingUtilities.set_padding(widget, bottom=spacing.lg)
    
    @staticmethod
    def pb_6(widget: QWidget) -> None:
        """Add 32px bottom padding."""
        SpacingUtilities.set_padding(widget, bottom=spacing.xl)
    
    @staticmethod
    def pl_1(widget: QWidget) -> None:
        """Add 4px left padding."""
        SpacingUtilities.set_padding(widget, left=spacing.xs)
    
    @staticmethod
    def pl_2(widget: QWidget) -> None:
        """Add 8px left padding."""
        SpacingUtilities.set_padding(widget, left=spacing.sm)
    
    @staticmethod
    def pl_3(widget: QWidget) -> None:
        """Add 12px left padding."""
        SpacingUtilities.set_padding(widget, left=spacing.md)
    
    @staticmethod
    def pl_4(widget: QWidget) -> None:
        """Add 16px left padding."""
        SpacingUtilities.set_padding(widget, left=spacing.md)
    
    @staticmethod
    def pl_5(widget: QWidget) -> None:
        """Add 24px left padding."""
        SpacingUtilities.set_padding(widget, left=spacing.lg)
    
    @staticmethod
    def pl_6(widget: QWidget) -> None:
        """Add 32px left padding."""
        SpacingUtilities.set_padding(widget, left=spacing.xl)
    
    @staticmethod
    def pr_1(widget: QWidget) -> None:
        """Add 4px right padding."""
        SpacingUtilities.set_padding(widget, right=spacing.xs)
    
    @staticmethod
    def pr_2(widget: QWidget) -> None:
        """Add 8px right padding."""
        SpacingUtilities.set_padding(widget, right=spacing.sm)
    
    @staticmethod
    def pr_3(widget: QWidget) -> None:
        """Add 12px right padding."""
        SpacingUtilities.set_padding(widget, right=spacing.md)
    
    @staticmethod
    def pr_4(widget: QWidget) -> None:
        """Add 16px right padding."""
        SpacingUtilities.set_padding(widget, right=spacing.md)
    
    @staticmethod
    def pr_5(widget: QWidget) -> None:
        """Add 24px right padding."""
        SpacingUtilities.set_padding(widget, right=spacing.lg)
    
    @staticmethod
    def pr_6(widget: QWidget) -> None:
        """Add 32px right padding."""
        SpacingUtilities.set_padding(widget, right=spacing.xl)


class SpacingHelpers:
    """Helper class for common spacing patterns."""
    
    @staticmethod
    def add_vertical_spacing(layout: QLayout, spacing_value: Union[int, SpacingUnit] = None) -> None:
        """Add vertical spacing to a vertical layout.
        
        Args:
            layout: Layout to add spacing to
            spacing_value: Spacing value (defaults to 8px)
        """
        if spacing_value is None:
            spacing_value = spacing.sm
        
        if isinstance(spacing_value, SpacingUnit):
            spacing_value = spacing_value.value
        
        layout.setSpacing(spacing_value)
    
    @staticmethod
    def add_horizontal_spacing(layout: QLayout, spacing_value: Union[int, SpacingUnit] = None) -> None:
        """Add horizontal spacing to a horizontal layout.
        
        Args:
            layout: Layout to add spacing to
            spacing_value: Spacing value (defaults to 8px)
        """
        if spacing_value is None:
            spacing_value = spacing.sm
        
        if isinstance(spacing_value, SpacingUnit):
            spacing_value = spacing_value.value
        
        layout.setSpacing(spacing_value)
    
    @staticmethod
    def add_consistent_spacing(layout: QLayout, spacing_value: Union[int, SpacingUnit] = None) -> None:
        """Add consistent spacing to any layout.
        
        Args:
            layout: Layout to add spacing to
            spacing_value: Spacing value (defaults to 8px)
        """
        if spacing_value is None:
            spacing_value = spacing.sm
        
        if isinstance(spacing_value, SpacingUnit):
            spacing_value = spacing_value.value
        
        layout.setSpacing(spacing_value)
    
    @staticmethod
    def add_section_spacing(layout: QLayout) -> None:
        """Add section spacing (16px) to a layout.
        
        Args:
            layout: Layout to add section spacing to
        """
        layout.setSpacing(spacing.md)
    
    @staticmethod
    def add_group_spacing(layout: QLayout) -> None:
        """Add group spacing (8px) to a layout.
        
        Args:
            layout: Layout to add group spacing to
        """
        layout.setSpacing(spacing.sm)
    
    @staticmethod
    def add_item_spacing(layout: QLayout) -> None:
        """Add item spacing (4px) to a layout.
        
        Args:
            layout: Layout to add item spacing to
        """
        layout.setSpacing(spacing.xs)
