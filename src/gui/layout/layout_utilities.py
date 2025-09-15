#!/usr/bin/env python3
"""
Layout utilities for advanced layout management.

This module provides flexbox utilities, grid helpers, responsive layout tools,
and other layout management features to complement the spacing system.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple, Union, Any
import logging
from threading import Lock

logger = logging.getLogger(__name__)


class FlexDirection(Enum):
    """Flexbox direction options."""
    ROW = "row"
    ROW_REVERSE = "row-reverse"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"


class FlexWrap(Enum):
    """Flexbox wrap options."""
    NOWRAP = "nowrap"
    WRAP = "wrap"
    WRAP_REVERSE = "wrap-reverse"


class FlexJustify(Enum):
    """Flexbox justify content options."""
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"


class FlexAlign(Enum):
    """Flexbox align items options."""
    STRETCH = "stretch"
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    BASELINE = "baseline"


class GridTemplate(Enum):
    """Grid template options."""
    AUTO = "auto"
    MIN_CONTENT = "min-content"
    MAX_CONTENT = "max-content"
    FR = "fr"


class LayoutType(Enum):
    """Layout type options."""
    BLOCK = "block"
    INLINE = "inline"
    INLINE_BLOCK = "inline-block"
    FLEX = "flex"
    GRID = "grid"
    TABLE = "table"
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    FIXED = "fixed"
    STICKY = "sticky"


@dataclass(frozen=True)
class FlexboxLayout:
    """Represents a flexbox layout configuration."""
    direction: FlexDirection
    wrap: FlexWrap
    justify: FlexJustify
    align: FlexAlign
    gap: int = 0


@dataclass(frozen=True)
class GridLayout:
    """Represents a grid layout configuration."""
    columns: Union[str, int]
    rows: Union[str, int]
    gap: int = 0
    auto_flow: str = "row"


@dataclass(frozen=True)
class LayoutConfig:
    """Represents a complete layout configuration."""
    layout_type: LayoutType
    flexbox: Optional[FlexboxLayout] = None
    grid: Optional[GridLayout] = None
    width: Optional[str] = None
    height: Optional[str] = None
    min_width: Optional[str] = None
    min_height: Optional[str] = None
    max_width: Optional[str] = None
    max_height: Optional[str] = None


class LayoutUtilities:
    """
    Advanced layout utilities for complex layout management.
    
    This class provides flexbox utilities, grid helpers, responsive layout tools,
    and other layout management features.
    """
    
    def __init__(self):
        self._layout_configs: Dict[str, LayoutConfig] = {}
        self._flexbox_layouts: Dict[str, FlexboxLayout] = {}
        self._grid_layouts: Dict[str, GridLayout] = {}
        self._lock = Lock()
        self._logger = logging.getLogger(f"{__name__}.LayoutUtilities")
        
        self._logger.info("LayoutUtilities initialized")
    
    def create_flexbox_layout(self, layout_id: str, direction: FlexDirection = FlexDirection.ROW,
                            wrap: FlexWrap = FlexWrap.NOWRAP, justify: FlexJustify = FlexJustify.FLEX_START,
                            align: FlexAlign = FlexAlign.STRETCH, gap: int = 0) -> bool:
        """
        Create a flexbox layout configuration.
        
        Args:
            layout_id: ID of the layout
            direction: Flex direction
            wrap: Flex wrap behavior
            justify: Justify content alignment
            align: Align items alignment
            gap: Gap between flex items
            
        Returns:
            True if layout was created successfully, False otherwise
        """
        try:
            with self._lock:
                flexbox_layout = FlexboxLayout(
                    direction=direction,
                    wrap=wrap,
                    justify=justify,
                    align=align,
                    gap=gap
                )
                
                self._flexbox_layouts[layout_id] = flexbox_layout
                
                self._logger.debug(f"Created flexbox layout '{layout_id}': {direction.value}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to create flexbox layout '{layout_id}': {e}")
            return False
    
    def get_flexbox_layout(self, layout_id: str) -> Optional[FlexboxLayout]:
        """Get a flexbox layout by ID."""
        return self._flexbox_layouts.get(layout_id)
    
    def create_grid_layout(self, layout_id: str, columns: Union[str, int], rows: Union[str, int],
                          gap: int = 0, auto_flow: str = "row") -> bool:
        """
        Create a grid layout configuration.
        
        Args:
            layout_id: ID of the layout
            columns: Number of columns or grid template
            rows: Number of rows or grid template
            gap: Gap between grid items
            auto_flow: Grid auto flow direction
            
        Returns:
            True if layout was created successfully, False otherwise
        """
        try:
            with self._lock:
                grid_layout = GridLayout(
                    columns=columns,
                    rows=rows,
                    gap=gap,
                    auto_flow=auto_flow
                )
                
                self._grid_layouts[layout_id] = grid_layout
                
                self._logger.debug(f"Created grid layout '{layout_id}': {columns}x{rows}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to create grid layout '{layout_id}': {e}")
            return False
    
    def get_grid_layout(self, layout_id: str) -> Optional[GridLayout]:
        """Get a grid layout by ID."""
        return self._grid_layouts.get(layout_id)
    
    def set_element_layout(self, element_id: str, layout_config: LayoutConfig) -> bool:
        """
        Set layout configuration for a specific element.
        
        Args:
            element_id: ID of the element
            layout_config: Layout configuration to apply
            
        Returns:
            True if layout was set successfully, False otherwise
        """
        try:
            with self._lock:
                self._layout_configs[element_id] = layout_config
                
                self._logger.debug(f"Set layout for {element_id}: {layout_config.layout_type.value}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to set layout for {element_id}: {e}")
            return False
    
    def get_element_layout(self, element_id: str) -> Optional[LayoutConfig]:
        """Get layout configuration for a specific element."""
        return self._layout_configs.get(element_id)
    
    def generate_flexbox_css(self, layout_id: str) -> Dict[str, str]:
        """
        Generate CSS properties for a flexbox layout.
        
        Args:
            layout_id: ID of the flexbox layout
            
        Returns:
            Dictionary of CSS properties
        """
        flexbox_layout = self._flexbox_layouts.get(layout_id)
        if not flexbox_layout:
            return {}
        
        css_properties = {
            "display": "flex",
            "flex-direction": flexbox_layout.direction.value,
            "flex-wrap": flexbox_layout.wrap.value,
            "justify-content": flexbox_layout.justify.value,
            "align-items": flexbox_layout.align.value
        }
        
        if flexbox_layout.gap > 0:
            css_properties["gap"] = f"{flexbox_layout.gap}px"
        
        return css_properties
    
    def generate_grid_css(self, layout_id: str) -> Dict[str, str]:
        """
        Generate CSS properties for a grid layout.
        
        Args:
            layout_id: ID of the grid layout
            
        Returns:
            Dictionary of CSS properties
        """
        grid_layout = self._grid_layouts.get(layout_id)
        if not grid_layout:
            return {}
        
        css_properties = {
            "display": "grid",
            "grid-auto-flow": grid_layout.auto_flow
        }
        
        # Handle columns
        if isinstance(grid_layout.columns, int):
            css_properties["grid-template-columns"] = f"repeat({grid_layout.columns}, 1fr)"
        else:
            css_properties["grid-template-columns"] = str(grid_layout.columns)
        
        # Handle rows
        if isinstance(grid_layout.rows, int):
            css_properties["grid-template-rows"] = f"repeat({grid_layout.rows}, 1fr)"
        else:
            css_properties["grid-template-rows"] = str(grid_layout.rows)
        
        if grid_layout.gap > 0:
            css_properties["gap"] = f"{grid_layout.gap}px"
        
        return css_properties
    
    def generate_layout_css(self, element_id: str) -> Dict[str, str]:
        """
        Generate complete CSS properties for an element's layout.
        
        Args:
            element_id: ID of the element
            
        Returns:
            Dictionary of CSS properties
        """
        layout_config = self._layout_configs.get(element_id)
        if not layout_config:
            return {}
        
        css_properties = {}
        
        # Add layout type specific properties
        if layout_config.layout_type == LayoutType.FLEX and layout_config.flexbox:
            # Generate flexbox CSS directly from the flexbox config
            css_properties.update({
                "display": "flex",
                "flex-direction": layout_config.flexbox.direction.value,
                "flex-wrap": layout_config.flexbox.wrap.value,
                "justify-content": layout_config.flexbox.justify.value,
                "align-items": layout_config.flexbox.align.value
            })
            if layout_config.flexbox.gap > 0:
                css_properties["gap"] = f"{layout_config.flexbox.gap}px"
        elif layout_config.layout_type == LayoutType.GRID and layout_config.grid:
            # Generate grid CSS directly from the grid config
            css_properties.update({
                "display": "grid",
                "grid-auto-flow": layout_config.grid.auto_flow
            })
            if isinstance(layout_config.grid.columns, int):
                css_properties["grid-template-columns"] = f"repeat({layout_config.grid.columns}, 1fr)"
            else:
                css_properties["grid-template-columns"] = str(layout_config.grid.columns)
            if isinstance(layout_config.grid.rows, int):
                css_properties["grid-template-rows"] = f"repeat({layout_config.grid.rows}, 1fr)"
            else:
                css_properties["grid-template-rows"] = str(layout_config.grid.rows)
            if layout_config.grid.gap > 0:
                css_properties["gap"] = f"{layout_config.grid.gap}px"
        else:
            css_properties["display"] = layout_config.layout_type.value
        
        # Add size properties
        if layout_config.width:
            css_properties["width"] = layout_config.width
        if layout_config.height:
            css_properties["height"] = layout_config.height
        if layout_config.min_width:
            css_properties["min-width"] = layout_config.min_width
        if layout_config.min_height:
            css_properties["min-height"] = layout_config.min_height
        if layout_config.max_width:
            css_properties["max-width"] = layout_config.max_width
        if layout_config.max_height:
            css_properties["max-height"] = layout_config.max_height
        
        return css_properties
    
    def create_responsive_layout(self, base_layout_id: str, responsive_variants: Dict[str, LayoutConfig]) -> bool:
        """
        Create a responsive layout with variants for different breakpoints.
        
        Args:
            base_layout_id: ID of the base layout
            responsive_variants: Dictionary of breakpoint -> layout config
            
        Returns:
            True if responsive layout was created successfully, False otherwise
        """
        try:
            with self._lock:
                # Store responsive variants
                for breakpoint, config in responsive_variants.items():
                    variant_id = f"{base_layout_id}_{breakpoint}"
                    self._layout_configs[variant_id] = config
                
                self._logger.debug(f"Created responsive layout '{base_layout_id}' with {len(responsive_variants)} variants")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to create responsive layout '{base_layout_id}': {e}")
            return False
    
    def get_responsive_layout_variant(self, base_layout_id: str, breakpoint: str) -> Optional[LayoutConfig]:
        """
        Get a responsive layout variant for a specific breakpoint.
        
        Args:
            base_layout_id: ID of the base layout
            breakpoint: Breakpoint identifier
            
        Returns:
            Layout configuration for the breakpoint if found, None otherwise
        """
        variant_id = f"{base_layout_id}_{breakpoint}"
        return self._layout_configs.get(variant_id)
    
    def create_layout_template(self, template_id: str, layout_configs: List[Tuple[str, LayoutConfig]]) -> bool:
        """
        Create a layout template with multiple element configurations.
        
        Args:
            template_id: ID of the template
            layout_configs: List of (element_id, layout_config) tuples
            
        Returns:
            True if template was created successfully, False otherwise
        """
        try:
            with self._lock:
                # Store template configurations
                for element_id, config in layout_configs:
                    template_element_id = f"{template_id}_{element_id}"
                    self._layout_configs[template_element_id] = config
                
                self._logger.debug(f"Created layout template '{template_id}' with {len(layout_configs)} elements")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to create layout template '{template_id}': {e}")
            return False
    
    def apply_layout_template(self, template_id: str, target_element_ids: List[str]) -> bool:
        """
        Apply a layout template to target elements.
        
        Args:
            template_id: ID of the template to apply
            target_element_ids: List of target element IDs
            
        Returns:
            True if template was applied successfully, False otherwise
        """
        try:
            with self._lock:
                # Find template configurations
                template_configs = {}
                for key, config in self._layout_configs.items():
                    if key.startswith(f"{template_id}_"):
                        element_name = key[len(f"{template_id}_"):]
                        template_configs[element_name] = config
                
                if not template_configs:
                    self._logger.warning(f"Layout template '{template_id}' not found")
                    return False
                
                # Apply template to target elements
                for i, target_id in enumerate(target_element_ids):
                    if i < len(template_configs):
                        # Get the first available template config
                        template_config = list(template_configs.values())[i]
                        self._layout_configs[target_id] = template_config
                
                self._logger.debug(f"Applied layout template '{template_id}' to {len(target_element_ids)} elements")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to apply layout template '{template_id}': {e}")
            return False
    
    def get_layout_summary(self) -> Dict[str, Any]:
        """Get a summary of all layout configurations."""
        return {
            "total_layout_configs": len(self._layout_configs),
            "total_flexbox_layouts": len(self._flexbox_layouts),
            "total_grid_layouts": len(self._grid_layouts),
            "available_flexbox_layouts": list(self._flexbox_layouts.keys()),
            "available_grid_layouts": list(self._grid_layouts.keys()),
            "layout_types": [config.layout_type.value for config in self._layout_configs.values()],
            "flexbox_directions": [layout.direction.value for layout in self._flexbox_layouts.values()],
            "grid_dimensions": [(layout.columns, layout.rows) for layout in self._grid_layouts.values()]
        }
    
    def validate_layout_structure(self) -> Dict[str, Any]:
        """Validate the layout structure for consistency issues."""
        issues = []
        warnings = []
        
        # Check for orphaned layout configs
        orphaned_configs = []
        for element_id, config in self._layout_configs.items():
            if config.layout_type == LayoutType.FLEX and not config.flexbox:
                orphaned_configs.append(f"Element {element_id} has flex layout type but no flexbox config")
            elif config.layout_type == LayoutType.GRID and not config.grid:
                orphaned_configs.append(f"Element {element_id} has grid layout type but no grid config")
        
        if orphaned_configs:
            issues.extend(orphaned_configs)
        
        # Check for unused flexbox layouts
        used_flexbox = set()
        for config in self._layout_configs.values():
            if config.flexbox:
                used_flexbox.add(id(config.flexbox))
        
        unused_flexbox = len(self._flexbox_layouts) - len(used_flexbox)
        if unused_flexbox > 0:
            warnings.append(f"{unused_flexbox} unused flexbox layouts")
        
        # Check for unused grid layouts
        used_grid = set()
        for config in self._layout_configs.values():
            if config.grid:
                used_grid.add(id(config.grid))
        
        unused_grid = len(self._grid_layouts) - len(used_grid)
        if unused_grid > 0:
            warnings.append(f"{unused_grid} unused grid layouts")
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues,
            "warnings": warnings,
            "total_elements": len(self._layout_configs),
            "elements_with_flexbox": sum(1 for config in self._layout_configs.values() if config.flexbox),
            "elements_with_grid": sum(1 for config in self._layout_configs.values() if config.grid)
        }
