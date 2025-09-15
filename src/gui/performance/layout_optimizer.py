"""
Layout Optimizer for efficient widget positioning and layout calculations.

This module provides advanced layout optimization techniques to reduce
layout passes and improve rendering performance.
"""

from typing import Dict, List, Tuple, Optional, Set, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import time
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QRect, QSize, QPoint
from PyQt6.QtWidgets import QWidget, QLayout, QLayoutItem, QGridLayout, QVBoxLayout, QHBoxLayout

from ..design_system.spacing_system import SpacingUnit
from ..responsive import responsive_spacing_manager


class LayoutType(Enum):
    """Types of layouts for optimization."""
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    GRID = "grid"
    FORM = "form"
    CUSTOM = "custom"


class OptimizationLevel(Enum):
    """Levels of layout optimization."""
    NONE = 0
    BASIC = 1
    AGGRESSIVE = 2
    ADAPTIVE = 3


@dataclass
class LayoutMetrics:
    """Metrics for layout performance analysis."""
    total_widgets: int = 0
    layout_passes: int = 0
    calculation_time: float = 0.0
    memory_usage: int = 0
    optimization_level: OptimizationLevel = OptimizationLevel.NONE
    last_optimization: float = field(default_factory=time.time)


class LayoutOptimizer(QObject):
    """
    Advanced layout optimizer for improved performance.
    
    Features:
    - Intelligent layout batching
    - Reduced layout passes
    - Widget position caching
    - Adaptive optimization levels
    - Performance monitoring
    - Memory-efficient calculations
    """
    
    # Signals
    layout_optimized = pyqtSignal(str, float)  # layout_id, performance_gain
    optimization_level_changed = pyqtSignal(str, OptimizationLevel)  # layout_id, new_level
    performance_metrics_updated = pyqtSignal(dict)  # metrics
    
    def __init__(self):
        super().__init__()
        self._optimized_layouts: Dict[str, LayoutMetrics] = {}
        self._widget_positions: Dict[int, QRect] = {}
        self._layout_cache: Dict[str, Dict[str, Any]] = {}
        self._dirty_regions: Set[str] = set()
        self._optimization_timer = QTimer()
        self._optimization_timer.timeout.connect(self._perform_optimization_cycle)
        self._optimization_timer.start(1000)  # Optimize every second
        
        # Performance tracking
        self._performance_history: List[Tuple[float, float]] = []  # (timestamp, performance_score)
        self._max_history_size = 100
        
        # Global optimization settings
        self._global_optimization_level = OptimizationLevel.ADAPTIVE
        self._enable_widget_caching = True
        self._enable_layout_batching = True
        self._enable_adaptive_optimization = True
    
    def optimize_layout(self, 
                       layout: QLayout,
                       layout_id: str,
                       optimization_level: Optional[OptimizationLevel] = None) -> bool:
        """
        Optimize a specific layout for better performance.
        
        Args:
            layout: The layout to optimize
            layout_id: Unique identifier for the layout
            optimization_level: Specific optimization level (None for adaptive)
            
        Returns:
            True if optimization was successful
        """
        start_time = time.time()
        
        if optimization_level is None:
            optimization_level = self._determine_optimal_level(layout)
        
        # Initialize metrics if needed
        if layout_id not in self._optimized_layouts:
            self._optimized_layouts[layout_id] = LayoutMetrics()
        
        metrics = self._optimized_layouts[layout_id]
        metrics.optimization_level = optimization_level
        metrics.last_optimization = time.time()
        
        try:
            # Apply optimization based on level
            if optimization_level == OptimizationLevel.BASIC:
                self._apply_basic_optimizations(layout, layout_id)
            elif optimization_level == OptimizationLevel.AGGRESSIVE:
                self._apply_aggressive_optimizations(layout, layout_id)
            elif optimization_level == OptimizationLevel.ADAPTIVE:
                self._apply_adaptive_optimizations(layout, layout_id)
            
            # Update metrics
            performance_gain = time.time() - start_time
            metrics.calculation_time = performance_gain
            metrics.total_widgets = self._count_widgets_in_layout(layout)
            
            # Emit signals
            self.layout_optimized.emit(layout_id, performance_gain)
            self.optimization_level_changed.emit(layout_id, optimization_level)
            
            return True
            
        except Exception as e:
            print(f"Error optimizing layout '{layout_id}': {e}")
            return False
    
    def batch_optimize_layouts(self, 
                              layouts: List[Tuple[QLayout, str, Optional[OptimizationLevel]]]) -> Dict[str, bool]:
        """
        Optimize multiple layouts in batch for better performance.
        
        Args:
            layouts: List of (layout, layout_id, optimization_level) tuples
            
        Returns:
            Dictionary mapping layout_id to success status
        """
        results = {}
        
        # Group layouts by type for optimization
        grouped_layouts = self._group_layouts_by_type(layouts)
        
        for layout_type, layout_list in grouped_layouts.items():
            # Apply type-specific batch optimizations
            if layout_type == LayoutType.GRID:
                self._batch_optimize_grid_layouts(layout_list, results)
            elif layout_type == LayoutType.VERTICAL:
                self._batch_optimize_vertical_layouts(layout_list, results)
            elif layout_type == LayoutType.HORIZONTAL:
                self._batch_optimize_horizontal_layouts(layout_list, results)
            else:
                # Individual optimization for other types
                for layout, layout_id, opt_level in layout_list:
                    results[layout_id] = self.optimize_layout(layout, layout_id, opt_level)
        
        return results
    
    def cache_widget_positions(self, layout: QLayout, layout_id: str) -> int:
        """
        Cache widget positions for a layout to reduce recalculation.
        
        Args:
            layout: The layout to cache positions for
            layout_id: Unique identifier for the layout
            
        Returns:
            Number of positions cached
        """
        if not self._enable_widget_caching:
            return 0
        
        cached_count = 0
        layout_cache = self._layout_cache.setdefault(layout_id, {})
        
        # Cache positions for all widgets in the layout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                widget_id = id(widget)
                
                # Cache current position and size
                position = QRect(widget.geometry())
                self._widget_positions[widget_id] = position
                layout_cache[f"widget_{widget_id}_pos"] = position
                cached_count += 1
        
        return cached_count
    
    def invalidate_layout_cache(self, 
                               layout_id: Optional[str] = None,
                               widget_id: Optional[int] = None):
        """
        Invalidate cached layout information.
        
        Args:
            layout_id: Specific layout to invalidate (None for all)
            widget_id: Specific widget to invalidate (None for all)
        """
        if layout_id is None:
            # Invalidate all layouts
            self._layout_cache.clear()
            self._widget_positions.clear()
            self._dirty_regions.clear()
        elif widget_id is None:
            # Invalidate specific layout
            self._layout_cache.pop(layout_id, None)
            self._dirty_regions.add(layout_id)
        else:
            # Invalidate specific widget
            self._widget_positions.pop(widget_id, None)
            if layout_id in self._layout_cache:
                self._layout_cache[layout_id].pop(f"widget_{widget_id}_pos", None)
    
    def get_layout_performance_metrics(self, layout_id: str) -> Optional[LayoutMetrics]:
        """
        Get performance metrics for a specific layout.
        
        Args:
            layout_id: Layout identifier
            
        Returns:
            Layout metrics or None if not found
        """
        return self._optimized_layouts.get(layout_id)
    
    def get_global_performance_metrics(self) -> Dict[str, Any]:
        """
        Get global performance metrics across all layouts.
        
        Returns:
            Dictionary of global performance metrics
        """
        total_widgets = sum(m.total_widgets for m in self._optimized_layouts.values())
        total_layouts = len(self._optimized_layouts)
        avg_calculation_time = sum(m.calculation_time for m in self._optimized_layouts.values()) / max(1, total_layouts)
        
        # Calculate performance score (lower is better)
        performance_score = self._calculate_performance_score()
        
        # Update history
        self._update_performance_history(performance_score)
        
        return {
            'total_layouts': total_layouts,
            'total_widgets': total_widgets,
            'average_calculation_time': avg_calculation_time,
            'performance_score': performance_score,
            'optimization_level': self._global_optimization_level.value,
            'cache_enabled': self._enable_widget_caching,
            'batching_enabled': self._enable_layout_batching,
            'adaptive_enabled': self._enable_adaptive_optimization
        }
    
    def set_global_optimization_level(self, level: OptimizationLevel):
        """Set the global optimization level for all layouts."""
        self._global_optimization_level = level
        
        # Apply to all existing layouts
        for layout_id in self._optimized_layouts:
            self._optimized_layouts[layout_id].optimization_level = level
    
    def enable_widget_caching(self, enabled: bool):
        """Enable or disable widget position caching."""
        self._enable_widget_caching = enabled
        if not enabled:
            self._widget_positions.clear()
    
    def enable_layout_batching(self, enabled: bool):
        """Enable or disable layout batching optimizations."""
        self._enable_layout_batching = enabled
    
    def enable_adaptive_optimization(self, enabled: bool):
        """Enable or disable adaptive optimization."""
        self._enable_adaptive_optimization = enabled
    
    def _determine_optimal_level(self, layout: QLayout) -> OptimizationLevel:
        """Determine the optimal optimization level for a layout."""
        if not self._enable_adaptive_optimization:
            return self._global_optimization_level
        
        # Analyze layout complexity
        widget_count = self._count_widgets_in_layout(layout)
        layout_type = self._identify_layout_type(layout)
        
        if widget_count < 10:
            return OptimizationLevel.BASIC
        elif widget_count < 50:
            return OptimizationLevel.AGGRESSIVE
        else:
            return OptimizationLevel.ADAPTIVE
    
    def _apply_basic_optimizations(self, layout: QLayout, layout_id: str):
        """Apply basic layout optimizations."""
        # Minimize layout passes
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Cache widget positions
        self.cache_widget_positions(layout, layout_id)
        
        # Mark as optimized
        self._dirty_regions.discard(layout_id)
    
    def _apply_aggressive_optimizations(self, layout: QLayout, layout_id: str):
        """Apply aggressive layout optimizations."""
        # Apply basic optimizations first
        self._apply_basic_optimizations(layout, layout_id)
        
        # Optimize spacing calculations
        self._optimize_layout_spacing(layout, layout_id)
        
        # Reduce layout updates
        layout.update()
    
    def _apply_adaptive_optimizations(self, layout: QLayout, layout_id: str):
        """Apply adaptive optimizations based on layout characteristics."""
        # Apply aggressive optimizations first
        self._apply_aggressive_optimizations(layout, layout_id)
        
        # Layout-specific optimizations
        layout_type = self._identify_layout_type(layout)
        
        if layout_type == LayoutType.GRID:
            self._optimize_grid_layout(layout, layout_id)
        elif layout_type == LayoutType.VERTICAL:
            self._optimize_vertical_layout(layout, layout_id)
        elif layout_type == LayoutType.HORIZONTAL:
            self._optimize_horizontal_layout(layout, layout_id)
    
    def _optimize_layout_spacing(self, layout: QLayout, layout_id: str):
        """Optimize spacing calculations for a layout."""
        # Use responsive spacing for layout margins
        responsive_margins = responsive_spacing_manager.get_responsive_spacing(
            SpacingUnit.MEDIUM, 
            touch_friendly=False
        )
        
        # Apply optimized margins
        layout.setContentsMargins(
            responsive_margins,
            responsive_margins,
            responsive_margins,
            responsive_margins
        )
        
        # Cache spacing values
        layout_cache = self._layout_cache.setdefault(layout_id, {})
        layout_cache['optimized_margins'] = responsive_margins
    
    def _optimize_grid_layout(self, layout: QLayout, layout_id: str):
        """Apply grid-specific optimizations."""
        if isinstance(layout, QGridLayout):
            # Optimize grid spacing
            grid_spacing = responsive_spacing_manager.get_responsive_spacing(
                SpacingUnit.SMALL,
                touch_friendly=False
            )
            layout.setSpacing(grid_spacing)
            
            # Cache grid-specific data
            layout_cache = self._layout_cache.setdefault(layout_id, {})
            layout_cache['grid_spacing'] = grid_spacing
            layout_cache['grid_columns'] = layout.columnCount()
            layout_cache['grid_rows'] = layout.rowCount()
    
    def _optimize_vertical_layout(self, layout: QLayout, layout_id: str):
        """Apply vertical layout optimizations."""
        if isinstance(layout, QVBoxLayout):
            # Optimize vertical spacing
            vertical_spacing = responsive_spacing_manager.get_responsive_spacing(
                SpacingUnit.SMALL,
                touch_friendly=False
            )
            layout.setSpacing(vertical_spacing)
            
            # Cache vertical-specific data
            layout_cache = self._layout_cache.setdefault(layout_id, {})
            layout_cache['vertical_spacing'] = vertical_spacing
    
    def _optimize_horizontal_layout(self, layout: QLayout, layout_id: str):
        """Apply horizontal layout optimizations."""
        if isinstance(layout, QHBoxLayout):
            # Optimize horizontal spacing
            horizontal_spacing = responsive_spacing_manager.get_responsive_spacing(
                SpacingUnit.SMALL,
                touch_friendly=False
            )
            layout.setSpacing(horizontal_spacing)
            
            # Cache horizontal-specific data
            layout_cache = self._layout_cache.setdefault(layout_id, {})
            layout_cache['horizontal_spacing'] = horizontal_spacing
    
    def _count_widgets_in_layout(self, layout: QLayout) -> int:
        """Count the number of widgets in a layout."""
        count = 0
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                count += 1
        return count
    
    def _identify_layout_type(self, layout: QLayout) -> LayoutType:
        """Identify the type of layout for optimization purposes."""
        if isinstance(layout, QGridLayout):
            return LayoutType.GRID
        elif isinstance(layout, QVBoxLayout):
            return LayoutType.VERTICAL
        elif isinstance(layout, QHBoxLayout):
            return LayoutType.HORIZONTAL
        else:
            return LayoutType.CUSTOM
    
    def _group_layouts_by_type(self, layouts: List[Tuple[QLayout, str, Optional[OptimizationLevel]]]) -> Dict[LayoutType, List]:
        """Group layouts by type for batch optimization."""
        grouped = {}
        for layout, layout_id, opt_level in layouts:
            layout_type = self._identify_layout_type(layout)
            if layout_type not in grouped:
                grouped[layout_type] = []
            grouped[layout_type].append((layout, layout_id, opt_level))
        return grouped
    
    def _batch_optimize_grid_layouts(self, 
                                    layouts: List[Tuple[QLayout, str, Optional[OptimizationLevel]]],
                                    results: Dict[str, bool]):
        """Batch optimize grid layouts."""
        for layout, layout_id, opt_level in layouts:
            results[layout_id] = self.optimize_layout(layout, layout_id, opt_level)
    
    def _batch_optimize_vertical_layouts(self, 
                                        layouts: List[Tuple[QLayout, str, Optional[OptimizationLevel]]],
                                        results: Dict[str, bool]):
        """Batch optimize vertical layouts."""
        for layout, layout_id, opt_level in layouts:
            results[layout_id] = self.optimize_layout(layout, layout_id, opt_level)
    
    def _batch_optimize_horizontal_layouts(self, 
                                          layouts: List[Tuple[QLayout, str, Optional[OptimizationLevel]]],
                                          results: Dict[str, bool]):
        """Batch optimize horizontal layouts."""
        for layout, layout_id, opt_level in layouts:
            results[layout_id] = self.optimize_layout(layout, layout_id, opt_level)
    
    def _calculate_performance_score(self) -> float:
        """Calculate overall performance score (lower is better)."""
        if not self._optimized_layouts:
            return 0.0
        
        # Calculate weighted performance score
        total_score = 0.0
        total_weight = 0.0
        
        for metrics in self._optimized_layouts.values():
            # Weight by widget count (more widgets = higher weight)
            weight = max(1, metrics.total_widgets)
            score = metrics.calculation_time * weight
            
            total_score += score
            total_weight += weight
        
        return total_score / max(1, total_weight)
    
    def _update_performance_history(self, performance_score: float):
        """Update performance history."""
        current_time = time.time()
        self._performance_history.append((current_time, performance_score))
        
        # Keep only recent history
        if len(self._performance_history) > self._max_history_size:
            self._performance_history = self._performance_history[-self._max_history_size:]
    
    def _perform_optimization_cycle(self):
        """Perform periodic optimization cycle."""
        # Update performance metrics
        metrics = self.get_global_performance_metrics()
        self.performance_metrics_updated.emit(metrics)
        
        # Adaptive optimization adjustments
        if self._enable_adaptive_optimization:
            self._adjust_optimization_strategy(metrics)
    
    def _adjust_optimization_strategy(self, metrics: Dict[str, Any]):
        """Adjust optimization strategy based on performance metrics."""
        performance_score = metrics.get('performance_score', 0.0)
        
        # Adjust global optimization level based on performance
        if performance_score > 0.1:  # High performance score (bad)
            if self._global_optimization_level != OptimizationLevel.AGGRESSIVE:
                self.set_global_optimization_level(OptimizationLevel.AGGRESSIVE)
        elif performance_score < 0.01:  # Low performance score (good)
            if self._global_optimization_level != OptimizationLevel.BASIC:
                self.set_global_optimization_level(OptimizationLevel.BASIC)


# Global instance for easy access
layout_optimizer = LayoutOptimizer()
