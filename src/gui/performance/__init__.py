"""
Performance optimization module for the spacing system.

This module provides comprehensive performance optimization tools including:
- Optimized spacing calculations
- Advanced caching systems
- Layout optimization
- Performance profiling and analysis
"""

from .optimized_spacing_calculator import (
    OptimizedSpacingCalculator,
    CalculationType,
    CachedCalculation,
    optimized_spacing_calculator
)

from .spacing_cache_system import (
    SpacingCacheSystem,
    CacheStrategy,
    CachePriority,
    CachedSpacingItem,
    spacing_cache_system
)

from .layout_optimizer import (
    LayoutOptimizer,
    LayoutType,
    OptimizationLevel,
    LayoutMetrics,
    layout_optimizer
)

from .spacing_performance_profiler import (
    SpacingPerformanceProfiler,
    ProfilerMode,
    PerformanceMetric,
    ProfilerSample,
    PerformanceReport,
    spacing_performance_profiler
)

__all__ = [
    # Optimized Spacing Calculator
    'OptimizedSpacingCalculator',
    'CalculationType',
    'CachedCalculation',
    'optimized_spacing_calculator',
    
    # Spacing Cache System
    'SpacingCacheSystem',
    'CacheStrategy',
    'CachePriority',
    'CachedSpacingItem',
    'spacing_cache_system',
    
    # Layout Optimizer
    'LayoutOptimizer',
    'LayoutType',
    'OptimizationLevel',
    'LayoutMetrics',
    'layout_optimizer',
    
    # Performance Profiler
    'SpacingPerformanceProfiler',
    'ProfilerMode',
    'PerformanceMetric',
    'ProfilerSample',
    'PerformanceReport',
    'spacing_performance_profiler'
]
