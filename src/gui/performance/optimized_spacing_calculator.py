"""
Optimized Spacing Calculator for high-performance spacing calculations.

This module provides optimized algorithms and caching mechanisms for
spacing calculations to ensure smooth performance even with complex layouts.
"""

from typing import Dict, Tuple, List, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
import time
import weakref
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget, QLayout

from ..design_system.spacing_system import SpacingUnit
from ..responsive import responsive_spacing_manager


class CalculationType(Enum):
    """Types of spacing calculations for optimization."""
    MARGIN = "margin"
    PADDING = "padding"
    SPACING = "spacing"
    ALIGNMENT = "alignment"
    RESPONSIVE = "responsive"
    COMPOSITE = "composite"


@dataclass
class CachedCalculation:
    """Cached spacing calculation result."""
    result: Any
    timestamp: float
    input_hash: int
    calculation_type: CalculationType
    widget_id: Optional[int] = None


class OptimizedSpacingCalculator(QObject):
    """
    High-performance spacing calculator with caching and optimization.
    
    Features:
    - Intelligent caching with TTL
    - Batch calculations
    - Lazy evaluation
    - Memory-efficient storage
    - Performance profiling
    """
    
    # Signals
    cache_hit = pyqtSignal(str, float)  # cache_key, performance_gain
    cache_miss = pyqtSignal(str)
    calculation_completed = pyqtSignal(str, float)  # calculation_type, duration
    
    def __init__(self):
        super().__init__()
        self._cache: Dict[str, CachedCalculation] = {}
        self._cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_saved_time': 0.0
        }
        self._max_cache_size = 1000
        self._cache_ttl = 30.0  # seconds
        self._batch_calculations: List[Tuple[str, callable, Any]] = []
        self._lazy_updates: Dict[int, callable] = {}
        self._performance_metrics: Dict[str, List[float]] = {}
        
        # Setup cleanup timer
        self._cleanup_timer = QTimer()
        self._cleanup_timer.timeout.connect(self._cleanup_expired_cache)
        self._cleanup_timer.start(10000)  # Clean every 10 seconds
        
    def calculate_optimized_spacing(self, 
                                  base_spacing: Union[int, SpacingUnit],
                                  calculation_type: CalculationType,
                                  widget: Optional[QWidget] = None,
                                  **kwargs) -> int:
        """
        Calculate spacing with optimization and caching.
        
        Args:
            base_spacing: Base spacing value or unit
            calculation_type: Type of calculation for optimization
            widget: Optional widget for context-specific calculations
            **kwargs: Additional calculation parameters
            
        Returns:
            Optimized spacing value
        """
        start_time = time.time()
        
        # Generate cache key
        cache_key = self._generate_cache_key(base_spacing, calculation_type, widget, **kwargs)
        
        # Check cache first
        cached_result = self._get_cached_result(cache_key)
        if cached_result is not None:
            performance_gain = time.time() - start_time
            self.cache_hit.emit(cache_key, performance_gain)
            return cached_result
        
        # Cache miss - perform calculation
        self.cache_miss.emit(cache_key)
        
        # Perform optimized calculation
        result = self._perform_optimized_calculation(base_spacing, calculation_type, widget, **kwargs)
        
        # Cache the result
        self._cache_result(cache_key, result, calculation_type, widget)
        
        # Record performance
        duration = time.time() - start_time
        self._record_performance(calculation_type.value, duration)
        self.calculation_completed.emit(calculation_type.value, duration)
        
        return result
    
    def batch_calculate_spacing(self, calculations: List[Tuple[Union[int, SpacingUnit], CalculationType, Optional[QWidget], dict]]) -> List[int]:
        """
        Perform multiple spacing calculations in batch for better performance.
        
        Args:
            calculations: List of (base_spacing, calculation_type, widget, kwargs) tuples
            
        Returns:
            List of calculated spacing values
        """
        start_time = time.time()
        results = []
        
        # Group calculations by type for optimization
        grouped_calculations = self._group_calculations_by_type(calculations)
        
        for calc_type, calc_list in grouped_calculations.items():
            # Use type-specific optimizations
            if calc_type == CalculationType.RESPONSIVE:
                results.extend(self._batch_responsive_calculations(calc_list))
            elif calc_type == CalculationType.COMPOSITE:
                results.extend(self._batch_composite_calculations(calc_list))
            else:
                # Standard batch calculation
                for base_spacing, _, widget, kwargs in calc_list:
                    result = self.calculate_optimized_spacing(base_spacing, calc_type, widget, **kwargs)
                    results.append(result)
        
        duration = time.time() - start_time
        self._record_performance("batch_calculation", duration)
        
        return results
    
    def schedule_lazy_update(self, widget_id: int, update_function: callable, priority: int = 0):
        """
        Schedule a lazy update for a widget to be executed later.
        
        Args:
            widget_id: Unique identifier for the widget
            update_function: Function to call for the update
            priority: Update priority (higher = more important)
        """
        self._lazy_updates[widget_id] = (update_function, priority)
    
    def execute_lazy_updates(self, max_updates: int = 50):
        """
        Execute pending lazy updates with priority ordering.
        
        Args:
            max_updates: Maximum number of updates to execute in this batch
        """
        if not self._lazy_updates:
            return
        
        # Sort by priority (highest first)
        sorted_updates = sorted(
            self._lazy_updates.items(),
            key=lambda x: x[1][1],
            reverse=True
        )
        
        executed = 0
        for widget_id, (update_function, _) in sorted_updates:
            if executed >= max_updates:
                break
                
            try:
                update_function()
                executed += 1
            except Exception as e:
                print(f"Error executing lazy update for widget {widget_id}: {e}")
            finally:
                # Remove executed update
                self._lazy_updates.pop(widget_id, None)
    
    def get_performance_metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Get performance metrics for all calculation types.
        
        Returns:
            Dictionary of performance metrics
        """
        metrics = {}
        for calc_type, durations in self._performance_metrics.items():
            if durations:
                metrics[calc_type] = {
                    'count': len(durations),
                    'total_time': sum(durations),
                    'average_time': sum(durations) / len(durations),
                    'min_time': min(durations),
                    'max_time': max(durations),
                    'last_time': durations[-1]
                }
        
        # Add cache statistics
        metrics['cache'] = {
            'hit_rate': self._cache_stats['hits'] / max(1, self._cache_stats['hits'] + self._cache_stats['misses']),
            'total_hits': self._cache_stats['hits'],
            'total_misses': self._cache_stats['misses'],
            'evictions': self._cache_stats['evictions'],
            'total_saved_time': self._cache_stats['total_saved_time'],
            'cache_size': len(self._cache)
        }
        
        return metrics
    
    def clear_cache(self):
        """Clear all cached calculations."""
        self._cache.clear()
        self._cache_stats['evictions'] += len(self._cache)
    
    def optimize_for_widget(self, widget: QWidget) -> Dict[str, int]:
        """
        Pre-calculate and cache common spacing values for a specific widget.
        
        Args:
            widget: Widget to optimize spacing for
            
        Returns:
            Dictionary of pre-calculated spacing values
        """
        widget_id = id(widget)
        optimized_values = {}
        
        # Common spacing calculations for widgets
        common_spacings = [
            (SpacingUnit.SMALL, CalculationType.MARGIN),
            (SpacingUnit.MEDIUM, CalculationType.PADDING),
            (SpacingUnit.LARGE, CalculationType.SPACING),
            (SpacingUnit.MEDIUM, CalculationType.RESPONSIVE)
        ]
        
        for base_spacing, calc_type in common_spacings:
            cache_key = f"widget_{widget_id}_{calc_type.value}_{base_spacing.value}"
            result = self.calculate_optimized_spacing(base_spacing, calc_type, widget)
            optimized_values[f"{calc_type.value}_{base_spacing.value}"] = result
        
        return optimized_values
    
    def _generate_cache_key(self, 
                           base_spacing: Union[int, SpacingUnit],
                           calculation_type: CalculationType,
                           widget: Optional[QWidget],
                           **kwargs) -> str:
        """Generate a unique cache key for the calculation."""
        widget_id = id(widget) if widget else 0
        spacing_value = base_spacing.value if isinstance(base_spacing, SpacingUnit) else base_spacing
        
        # Create a hash of kwargs for the cache key
        kwargs_hash = hash(frozenset(sorted(kwargs.items())))
        
        return f"{calculation_type.value}_{spacing_value}_{widget_id}_{kwargs_hash}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[int]:
        """Get cached result if valid."""
        if cache_key not in self._cache:
            return None
        
        cached = self._cache[cache_key]
        current_time = time.time()
        
        # Check if cache entry is expired
        if current_time - cached.timestamp > self._cache_ttl:
            del self._cache[cache_key]
            self._cache_stats['evictions'] += 1
            return None
        
        # Cache hit
        self._cache_stats['hits'] += 1
        self._cache_stats['total_saved_time'] += 0.001  # Estimate saved time
        
        return cached.result
    
    def _cache_result(self, 
                     cache_key: str, 
                     result: int, 
                     calculation_type: CalculationType,
                     widget: Optional[QWidget]):
        """Cache a calculation result."""
        # Check cache size limit
        if len(self._cache) >= self._max_cache_size:
            # Remove oldest entries
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k].timestamp)
            del self._cache[oldest_key]
            self._cache_stats['evictions'] += 1
        
        widget_id = id(widget) if widget else None
        self._cache[cache_key] = CachedCalculation(
            result=result,
            timestamp=time.time(),
            input_hash=hash(cache_key),
            calculation_type=calculation_type,
            widget_id=widget_id
        )
    
    def _perform_optimized_calculation(self,
                                     base_spacing: Union[int, SpacingUnit],
                                     calculation_type: CalculationType,
                                     widget: Optional[QWidget],
                                     **kwargs) -> int:
        """Perform the actual spacing calculation with optimizations."""
        spacing_value = base_spacing.value if isinstance(base_spacing, SpacingUnit) else base_spacing
        
        if calculation_type == CalculationType.RESPONSIVE:
            return self._calculate_responsive_spacing(spacing_value, widget, **kwargs)
        elif calculation_type == CalculationType.COMPOSITE:
            return self._calculate_composite_spacing(spacing_value, widget, **kwargs)
        elif calculation_type == CalculationType.ALIGNMENT:
            return self._calculate_alignment_spacing(spacing_value, widget, **kwargs)
        else:
            # Standard spacing calculation
            return spacing_value
    
    def _calculate_responsive_spacing(self, 
                                    base_spacing: int, 
                                    widget: Optional[QWidget],
                                    **kwargs) -> int:
        """Calculate responsive spacing with optimization."""
        touch_friendly = kwargs.get('touch_friendly', False)
        return responsive_spacing_manager.get_responsive_spacing(base_spacing, touch_friendly)
    
    def _calculate_composite_spacing(self, 
                                   base_spacing: int, 
                                   widget: Optional[QWidget],
                                   **kwargs) -> int:
        """Calculate composite spacing (margin + padding + spacing)."""
        margin_multiplier = kwargs.get('margin_multiplier', 1.0)
        padding_multiplier = kwargs.get('padding_multiplier', 1.0)
        spacing_multiplier = kwargs.get('spacing_multiplier', 1.0)
        
        return int(base_spacing * (margin_multiplier + padding_multiplier + spacing_multiplier))
    
    def _calculate_alignment_spacing(self, 
                                   base_spacing: int, 
                                   widget: Optional[QWidget],
                                   **kwargs) -> int:
        """Calculate alignment-specific spacing."""
        alignment_type = kwargs.get('alignment_type', 'center')
        
        if alignment_type == 'left':
            return base_spacing
        elif alignment_type == 'right':
            return -base_spacing
        elif alignment_type == 'center':
            return base_spacing // 2
        else:
            return base_spacing
    
    def _group_calculations_by_type(self, 
                                   calculations: List[Tuple[Union[int, SpacingUnit], CalculationType, Optional[QWidget], dict]]) -> Dict[CalculationType, List]:
        """Group calculations by type for batch optimization."""
        grouped = {}
        for calc in calculations:
            calc_type = calc[1]
            if calc_type not in grouped:
                grouped[calc_type] = []
            grouped[calc_type].append(calc)
        return grouped
    
    def _batch_responsive_calculations(self, 
                                     calculations: List[Tuple[Union[int, SpacingUnit], CalculationType, Optional[QWidget], dict]]) -> List[int]:
        """Optimized batch calculation for responsive spacing."""
        results = []
        current_breakpoint = responsive_spacing_manager.get_current_breakpoint()
        
        for base_spacing, _, widget, kwargs in calculations:
            spacing_value = base_spacing.value if isinstance(base_spacing, SpacingUnit) else base_spacing
            touch_friendly = kwargs.get('touch_friendly', False)
            
            # Use breakpoint-specific optimization
            if current_breakpoint == 'mobile' and touch_friendly:
                result = int(spacing_value * 1.5)  # Touch-friendly spacing
            else:
                result = responsive_spacing_manager.get_responsive_spacing(spacing_value, touch_friendly)
            
            results.append(result)
        
        return results
    
    def _batch_composite_calculations(self, 
                                    calculations: List[Tuple[Union[int, SpacingUnit], CalculationType, Optional[QWidget], dict]]) -> List[int]:
        """Optimized batch calculation for composite spacing."""
        results = []
        
        for base_spacing, _, widget, kwargs in calculations:
            spacing_value = base_spacing.value if isinstance(base_spacing, SpacingUnit) else base_spacing
            margin_multiplier = kwargs.get('margin_multiplier', 1.0)
            padding_multiplier = kwargs.get('padding_multiplier', 1.0)
            spacing_multiplier = kwargs.get('spacing_multiplier', 1.0)
            
            result = int(spacing_value * (margin_multiplier + padding_multiplier + spacing_multiplier))
            results.append(result)
        
        return results
    
    def _record_performance(self, calculation_type: str, duration: float):
        """Record performance metrics for a calculation type."""
        if calculation_type not in self._performance_metrics:
            self._performance_metrics[calculation_type] = []
        
        self._performance_metrics[calculation_type].append(duration)
        
        # Keep only last 100 measurements to prevent memory bloat
        if len(self._performance_metrics[calculation_type]) > 100:
            self._performance_metrics[calculation_type] = self._performance_metrics[calculation_type][-100:]
    
    def _cleanup_expired_cache(self):
        """Clean up expired cache entries."""
        current_time = time.time()
        expired_keys = [
            key for key, cached in self._cache.items()
            if current_time - cached.timestamp > self._cache_ttl
        ]
        
        for key in expired_keys:
            del self._cache[key]
            self._cache_stats['evictions'] += 1


# Global instance for easy access
optimized_spacing_calculator = OptimizedSpacingCalculator()
