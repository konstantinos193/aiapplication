#!/usr/bin/env python3
"""
UI Spacing and Alignment System for consistent layout management.

This module provides comprehensive spacing scales, alignment utilities,
responsive spacing, and integration with accessibility systems.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple, Union, Any
import logging
from threading import Lock

logger = logging.getLogger(__name__)


class SpacingScale(Enum):
    """Standard spacing scale values following 8px grid system."""
    XS = 4      # Extra small - 4px
    SM = 8      # Small - 8px
    MD = 16     # Medium - 16px
    LG = 24     # Large - 24px
    XL = 32     # Extra large - 32px
    XXL = 48    # 2X large - 48px
    XXXL = 64   # 3X large - 64px


class Alignment(Enum):
    """Alignment options for elements."""
    # Horizontal alignment
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    
    # Vertical alignment
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"
    
    # Combined alignments
    TOP_LEFT = "top-left"
    TOP_CENTER = "top-center"
    TOP_RIGHT = "top-right"
    MIDDLE_LEFT = "middle-left"
    MIDDLE_CENTER = "middle-center"
    MIDDLE_RIGHT = "middle-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_CENTER = "bottom-center"
    BOTTOM_RIGHT = "bottom-right"


class SpacingType(Enum):
    """Types of spacing that can be applied."""
    MARGIN = "margin"
    PADDING = "padding"
    GAP = "gap"
    BORDER = "border"
    OUTLINE = "outline"


class ResponsiveBreakpoint(Enum):
    """Responsive breakpoints for different screen sizes."""
    MOBILE = "mobile"      # 0-767px
    TABLET = "tablet"      # 768-1023px
    DESKTOP = "desktop"    # 1024-1439px
    WIDESCREEN = "wide"    # 1440px+


@dataclass(frozen=True)
class SpacingValue:
    """Represents a spacing value with its scale and type."""
    value: int
    scale: SpacingScale
    spacing_type: SpacingType
    responsive: bool = False
    breakpoint: Optional[ResponsiveBreakpoint] = None


@dataclass(frozen=True)
class AlignmentRule:
    """Represents an alignment rule for an element."""
    horizontal: Alignment
    vertical: Alignment
    responsive: bool = False
    breakpoint: Optional[ResponsiveBreakpoint] = None


@dataclass(frozen=True)
class SpacingPreset:
    """Predefined spacing presets for common use cases."""
    name: str
    margin: SpacingValue
    padding: SpacingValue
    gap: SpacingValue
    description: str = ""


@dataclass(frozen=True)
class LayoutGrid:
    """Grid system for consistent layout management."""
    columns: int
    rows: int
    gap: SpacingValue
    margin: SpacingValue
    padding: SpacingValue


class SpacingSystem:
    """
    Comprehensive spacing and alignment system for UI layout management.
    
    This class provides consistent spacing scales, alignment utilities,
    responsive spacing, and integration with accessibility systems.
    """
    
    def __init__(self):
        self._spacing_values: Dict[str, SpacingValue] = {}
        self._alignment_rules: Dict[str, AlignmentRule] = {}
        self._spacing_presets: Dict[str, SpacingPreset] = {}
        self._layout_grids: Dict[str, LayoutGrid] = {}
        self._lock = Lock()
        self._logger = logging.getLogger(f"{__name__}.SpacingSystem")
        
        # Initialize default spacing presets
        self._setup_default_presets()
        self._logger.info("SpacingSystem initialized")
    
    def _setup_default_presets(self):
        """Setup default spacing presets for common use cases."""
        # Card preset
        card_preset = SpacingPreset(
            name="card",
            margin=SpacingValue(16, SpacingScale.MD, SpacingType.MARGIN),
            padding=SpacingValue(16, SpacingScale.MD, SpacingType.PADDING),
            gap=SpacingValue(8, SpacingScale.SM, SpacingType.GAP),
            description="Standard card spacing with 16px margins and padding"
        )
        self._spacing_presets["card"] = card_preset
        
        # Button preset
        button_preset = SpacingPreset(
            name="button",
            margin=SpacingValue(8, SpacingScale.SM, SpacingType.MARGIN),
            padding=SpacingValue(12, SpacingScale.SM, SpacingType.PADDING),  # Custom 12px value
            gap=SpacingValue(4, SpacingScale.XS, SpacingType.GAP),
            description="Standard button spacing with 8px margins and 12px padding"
        )
        self._spacing_presets["button"] = button_preset
        
        # Form preset
        form_preset = SpacingPreset(
            name="form",
            margin=SpacingValue(24, SpacingScale.LG, SpacingType.MARGIN),
            padding=SpacingValue(24, SpacingScale.LG, SpacingType.PADDING),
            gap=SpacingValue(16, SpacingScale.MD, SpacingType.GAP),
            description="Form layout with 24px margins and 16px gaps between elements"
        )
        self._spacing_presets["form"] = form_preset
        
        # Navigation preset
        nav_preset = SpacingPreset(
            name="navigation",
            margin=SpacingValue(16, SpacingScale.MD, SpacingType.MARGIN),
            padding=SpacingValue(8, SpacingScale.SM, SpacingType.PADDING),
            gap=SpacingValue(16, SpacingScale.MD, SpacingType.GAP),
            description="Navigation menu with 16px margins and 8px padding"
        )
        self._spacing_presets["navigation"] = nav_preset
    
    def get_spacing_value(self, scale: SpacingScale, spacing_type: SpacingType = SpacingType.MARGIN) -> int:
        """
        Get a spacing value for a given scale and type.
        
        Args:
            scale: Spacing scale to use
            spacing_type: Type of spacing to apply
            
        Returns:
            Spacing value in pixels
        """
        return scale.value
    
    def get_responsive_spacing(self, scale: SpacingScale, breakpoint: ResponsiveBreakpoint) -> int:
        """
        Get responsive spacing value for a specific breakpoint.
        
        Args:
            scale: Base spacing scale
            breakpoint: Responsive breakpoint
            
        Returns:
            Responsive spacing value in pixels
        """
        # Adjust spacing based on breakpoint
        if breakpoint == ResponsiveBreakpoint.MOBILE:
            return max(4, scale.value - 4)  # Reduce spacing on mobile
        elif breakpoint == ResponsiveBreakpoint.TABLET:
            return scale.value  # Standard spacing on tablet
        elif breakpoint == ResponsiveBreakpoint.DESKTOP:
            return scale.value  # Standard spacing on desktop
        elif breakpoint == ResponsiveBreakpoint.WIDESCREEN:
            return scale.value + 8  # Increase spacing on wide screens
        
        return scale.value
    
    def set_element_spacing(self, element_id: str, spacing_type: SpacingType, 
                           scale: SpacingScale, responsive: bool = False) -> bool:
        """
        Set spacing for a specific element.
        
        Args:
            element_id: ID of the element
            spacing_type: Type of spacing to apply
            scale: Spacing scale to use
            responsive: Whether spacing should be responsive
            
        Returns:
            True if spacing was set successfully, False otherwise
        """
        try:
            with self._lock:
                spacing_value = SpacingValue(
                    value=scale.value,
                    scale=scale,
                    spacing_type=spacing_type,
                    responsive=responsive
                )
                
                key = f"{element_id}_{spacing_type.value}"
                self._spacing_values[key] = spacing_value
                
                self._logger.debug(f"Set {spacing_type.value} spacing for {element_id}: {scale.value}px")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to set spacing for {element_id}: {e}")
            return False
    
    def set_element_spacing_custom(self, element_id: str, spacing_type: SpacingType, 
                                  value: int, scale: SpacingScale = None, responsive: bool = False) -> bool:
        """
        Set spacing for a specific element with a custom value.
        
        Args:
            element_id: ID of the element
            spacing_type: Type of spacing to apply
            value: Custom spacing value in pixels
            scale: Optional scale reference (defaults to closest scale)
            responsive: Whether spacing should be responsive
            
        Returns:
            True if spacing was set successfully, False otherwise
        """
        try:
            with self._lock:
                # Find closest scale if not provided
                if scale is None:
                    scale = self._find_closest_scale(value)
                
                spacing_value = SpacingValue(
                    value=value,
                    scale=scale,
                    spacing_type=spacing_type,
                    responsive=responsive
                )
                
                key = f"{element_id}_{spacing_type.value}"
                self._spacing_values[key] = spacing_value
                
                self._logger.debug(f"Set {spacing_type.value} spacing for {element_id}: {value}px")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to set custom spacing for {element_id}: {e}")
            return False
    
    def _find_closest_scale(self, value: int) -> SpacingScale:
        """Find the closest spacing scale to a given value."""
        scales = list(SpacingScale)
        closest = min(scales, key=lambda s: abs(s.value - value))
        return closest
    
    def get_element_spacing(self, element_id: str, spacing_type: SpacingType) -> Optional[SpacingValue]:
        """
        Get spacing for a specific element.
        
        Args:
            element_id: ID of the element
            spacing_type: Type of spacing to retrieve
            
        Returns:
            Spacing value if found, None otherwise
        """
        key = f"{element_id}_{spacing_type.value}"
        return self._spacing_values.get(key)
    
    def set_element_alignment(self, element_id: str, horizontal: Alignment, 
                             vertical: Alignment, responsive: bool = False) -> bool:
        """
        Set alignment for a specific element.
        
        Args:
            element_id: ID of the element
            horizontal: Horizontal alignment
            vertical: Vertical alignment
            responsive: Whether alignment should be responsive
            
        Returns:
            True if alignment was set successfully, False otherwise
        """
        try:
            with self._lock:
                alignment_rule = AlignmentRule(
                    horizontal=horizontal,
                    vertical=vertical,
                    responsive=responsive
                )
                
                self._alignment_rules[element_id] = alignment_rule
                
                self._logger.debug(f"Set alignment for {element_id}: {horizontal.value}-{vertical.value}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to set alignment for {element_id}: {e}")
            return False
    
    def get_element_alignment(self, element_id: str) -> Optional[AlignmentRule]:
        """
        Get alignment for a specific element.
        
        Args:
            element_id: ID of the element
            
        Returns:
            Alignment rule if found, None otherwise
        """
        return self._alignment_rules.get(element_id)
    
    def apply_spacing_preset(self, element_id: str, preset_name: str) -> bool:
        """
        Apply a predefined spacing preset to an element.
        
        Args:
            element_id: ID of the element
            preset_name: Name of the preset to apply
            
        Returns:
            True if preset was applied successfully, False otherwise
        """
        try:
            if preset_name not in self._spacing_presets:
                self._logger.warning(f"Spacing preset '{preset_name}' not found")
                return False
            
            preset = self._spacing_presets[preset_name]
            
            # Apply all spacing values from the preset using custom values
            self.set_element_spacing_custom(element_id, SpacingType.MARGIN, preset.margin.value, preset.margin.scale)
            self.set_element_spacing_custom(element_id, SpacingType.PADDING, preset.padding.value, preset.padding.scale)
            self.set_element_spacing_custom(element_id, SpacingType.GAP, preset.gap.value, preset.gap.scale)
            
            self._logger.debug(f"Applied spacing preset '{preset_name}' to {element_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to apply spacing preset '{preset_name}' to {element_id}: {e}")
            return False
    
    def create_layout_grid(self, grid_id: str, columns: int, rows: int, 
                          gap: SpacingScale, margin: SpacingScale = SpacingScale.MD,
                          padding: SpacingScale = SpacingScale.MD) -> bool:
        """
        Create a layout grid for consistent element positioning.
        
        Args:
            grid_id: ID of the grid
            columns: Number of columns
            rows: Number of rows
            gap: Gap between grid items
            margin: Margin around the grid
            padding: Padding within grid cells
            
        Returns:
            True if grid was created successfully, False otherwise
        """
        try:
            with self._lock:
                grid = LayoutGrid(
                    columns=columns,
                    rows=rows,
                    gap=SpacingValue(gap.value, gap, SpacingType.GAP),
                    margin=SpacingValue(margin.value, margin, SpacingType.MARGIN),
                    padding=SpacingValue(padding.value, padding, SpacingType.PADDING)
                )
                
                self._layout_grids[grid_id] = grid
                
                self._logger.debug(f"Created layout grid '{grid_id}': {columns}x{rows}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to create layout grid '{grid_id}': {e}")
            return False
    
    def get_layout_grid(self, grid_id: str) -> Optional[LayoutGrid]:
        """
        Get a layout grid by ID.
        
        Args:
            grid_id: ID of the grid
            
        Returns:
            Layout grid if found, None otherwise
        """
        return self._layout_grids.get(grid_id)
    
    def calculate_grid_position(self, grid_id: str, column: int, row: int) -> Tuple[int, int]:
        """
        Calculate the position of an element within a grid.
        
        Args:
            grid_id: ID of the grid
            column: Column index (0-based)
            row: Row index (0-based)
            
        Returns:
            Tuple of (x, y) coordinates in pixels
        """
        grid = self._layout_grids.get(grid_id)
        if not grid:
            return (0, 0)
        
        # Calculate position based on grid dimensions and spacing
        x = column * (100 // grid.columns) + grid.padding.value
        y = row * (100 // grid.rows) + grid.padding.value
        
        return (x, y)
    
    def generate_css_spacing(self, element_id: str) -> Dict[str, str]:
        """
        Generate CSS spacing properties for an element.
        
        Args:
            element_id: ID of the element
            
        Returns:
            Dictionary of CSS properties
        """
        css_properties = {}
        
        # Get spacing values
        margin = self.get_element_spacing(element_id, SpacingType.MARGIN)
        padding = self.get_element_spacing(element_id, SpacingType.PADDING)
        gap = self.get_element_spacing(element_id, SpacingType.GAP)
        
        # Add margin
        if margin:
            css_properties["margin"] = f"{margin.value}px"
        
        # Add padding
        if padding:
            css_properties["padding"] = f"{padding.value}px"
        
        # Add gap (for flexbox/grid)
        if gap:
            css_properties["gap"] = f"{gap.value}px"
        
        return css_properties
    
    def generate_css_alignment(self, element_id: str) -> Dict[str, str]:
        """
        Generate CSS alignment properties for an element.
        
        Args:
            element_id: ID of the element
            
        Returns:
            Dictionary of CSS properties
        """
        css_properties = {}
        alignment = self.get_element_alignment(element_id)
        
        if not alignment:
            return css_properties
        
        # Horizontal alignment
        if alignment.horizontal in [Alignment.LEFT, Alignment.TOP_LEFT, Alignment.MIDDLE_LEFT, Alignment.BOTTOM_LEFT]:
            css_properties["text-align"] = "left"
        elif alignment.horizontal in [Alignment.CENTER, Alignment.TOP_CENTER, Alignment.MIDDLE_CENTER, Alignment.BOTTOM_CENTER]:
            css_properties["text-align"] = "center"
        elif alignment.horizontal in [Alignment.RIGHT, Alignment.TOP_RIGHT, Alignment.MIDDLE_RIGHT, Alignment.BOTTOM_RIGHT]:
            css_properties["text-align"] = "right"
        elif alignment.horizontal == Alignment.JUSTIFY:
            css_properties["text-align"] = "justify"
        
        # Vertical alignment for flexbox
        if alignment.vertical in [Alignment.TOP, Alignment.TOP_LEFT, Alignment.TOP_CENTER, Alignment.TOP_RIGHT]:
            css_properties["align-items"] = "flex-start"
        elif alignment.vertical in [Alignment.MIDDLE, Alignment.MIDDLE_LEFT, Alignment.MIDDLE_CENTER, Alignment.MIDDLE_RIGHT]:
            css_properties["align-items"] = "center"
        elif alignment.vertical in [Alignment.BOTTOM, Alignment.BOTTOM_LEFT, Alignment.BOTTOM_CENTER, Alignment.BOTTOM_RIGHT]:
            css_properties["align-items"] = "flex-end"
        elif alignment.vertical == Alignment.BASELINE:
            css_properties["align-items"] = "baseline"
        
        return css_properties
    
    def get_spacing_summary(self) -> Dict[str, Any]:
        """Get a summary of all spacing and alignment information."""
        return {
            "total_spacing_values": len(self._spacing_values),
            "total_alignment_rules": len(self._alignment_rules),
            "total_spacing_presets": len(self._spacing_presets),
            "total_layout_grids": len(self._layout_grids),
            "available_presets": list(self._spacing_presets.keys()),
            "available_grids": list(self._layout_grids.keys()),
            "spacing_scales": {scale.name: scale.value for scale in SpacingScale},
            "alignment_options": {align.name: align.value for align in Alignment}
        }
    
    def validate_spacing_structure(self) -> Dict[str, Any]:
        """Validate the spacing structure for consistency issues."""
        issues = []
        warnings = []
        
        # Check for orphaned spacing values
        element_ids = set()
        for key in self._spacing_values.keys():
            element_id = key.split('_')[0]
            element_ids.add(element_id)
        
        # Check for orphaned alignment rules
        orphaned_alignments = set(self._alignment_rules.keys()) - element_ids
        if orphaned_alignments:
            warnings.append(f"Orphaned alignment rules: {list(orphaned_alignments)}")
        
        # Check for consistent spacing usage
        spacing_counts = {}
        for key, value in self._spacing_values.items():
            element_id = key.split('_')[0]
            if element_id not in spacing_counts:
                spacing_counts[element_id] = 0
            spacing_counts[element_id] += 1
        
        # Warn about elements with only partial spacing
        for element_id, count in spacing_counts.items():
            if count < 3:  # Less than margin, padding, and gap
                warnings.append(f"Element {element_id} has incomplete spacing ({count}/3 types)")
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues,
            "warnings": warnings,
            "total_elements": len(element_ids),
            "elements_with_spacing": len(spacing_counts),
            "elements_with_alignment": len(self._alignment_rules)
        }
