"""
Spacing Cache System for efficient storage and retrieval of spacing values.

This module provides a sophisticated caching system that optimizes
spacing calculations and reduces redundant computations.
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import hashlib
import weakref
from collections import OrderedDict
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QThread, QMutex, QMutexLocker
from PyQt6.QtWidgets import QWidget

from ..design_system.spacing_system import SpacingUnit
from ..responsive import responsive_spacing_manager


class CacheStrategy(Enum):
    """Different caching strategies for spacing values."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    ADAPTIVE = "adaptive"  # Adaptive strategy based on usage patterns


class CachePriority(Enum):
    """Priority levels for cached items."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class CachedSpacingItem:
    """A cached spacing calculation item."""
    value: Any
    timestamp: float
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    priority: CachePriority = CachePriority.NORMAL
    size_bytes: int = 0
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SpacingCacheSystem(QObject):
    """
    Advanced spacing cache system with multiple strategies and optimizations.
    
    Features:
    - Multiple caching strategies (LRU, LFU, TTL, Adaptive)
    - Priority-based caching
    - Memory management and cleanup
    - Dependency tracking
    - Background cleanup thread
    - Cache statistics and monitoring
    """
    
    # Signals
    cache_hit = pyqtSignal(str, float)  # key, performance_gain
    cache_miss = pyqtSignal(str)
    cache_eviction = pyqtSignal(str, str)  # key, reason
    memory_warning = pyqtSignal(int)  # current_memory_usage
    performance_update = pyqtSignal(dict)  # performance_metrics
    
    def __init__(self, 
                 max_memory_mb: int = 100,
                 strategy: CacheStrategy = CacheStrategy.ADAPTIVE):
        super().__init__()
        self._max_memory_bytes = max_memory_mb * 1024 * 1024
        self._strategy = strategy
        self._cache: OrderedDict[str, CachedSpacingItem] = OrderedDict()
        self._access_frequency: Dict[str, int] = {}
        self._memory_usage = 0
        self._mutex = QMutex()
        
        # Statistics
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_saved_time': 0.0,
            'memory_usage': 0,
            'cache_size': 0
        }
        
        # Strategy-specific data
        self._lru_order: List[str] = []
        self._lfu_counts: Dict[str, int] = {}
        self._ttl_expiry: Dict[str, float] = {}
        
        # Setup cleanup
        self._cleanup_timer = QTimer()
        self._cleanup_timer.timeout.connect(self._perform_cleanup)
        self._cleanup_timer.start(5000)  # Clean every 5 seconds
        
        # Performance monitoring
        self._performance_timer = QTimer()
        self._performance_timer.timeout.connect(self._update_performance_metrics)
        self._performance_timer.start(10000)  # Update every 10 seconds
    
    def get_cached_spacing(self, 
                          key: str,
                          default_calculator: Optional[Callable] = None,
                          **kwargs) -> Any:
        """
        Get cached spacing value or calculate and cache if not present.
        
        Args:
            key: Cache key for the spacing value
            default_calculator: Function to calculate value if not cached
            **kwargs: Arguments for the calculator function
            
        Returns:
            Cached or calculated spacing value
        """
        start_time = time.time()
        
        # Check cache first
        cached_item = self._get_from_cache(key)
        if cached_item is not None:
            # Update access statistics
            self._update_access_stats(key)
            performance_gain = time.time() - start_time
            self.cache_hit.emit(key, performance_gain)
            self._stats['hits'] += 1
            self._stats['total_saved_time'] += performance_gain
            return cached_item.value
        
        # Cache miss
        self.cache_miss.emit(key)
        self._stats['misses'] += 1
        
        # Calculate if calculator provided
        if default_calculator:
            try:
                value = default_calculator(**kwargs)
                self._cache_spacing(key, value, **kwargs)
                return value
            except Exception as e:
                print(f"Error calculating spacing for key '{key}': {e}")
                return None
        
        return None
    
    def cache_spacing(self, 
                     key: str, 
                     value: Any, 
                     priority: CachePriority = CachePriority.NORMAL,
                     ttl_seconds: Optional[float] = None,
                     dependencies: Optional[List[str]] = None,
                     **metadata) -> bool:
        """
        Cache a spacing value with specified parameters.
        
        Args:
            key: Unique cache key
            value: Value to cache
            priority: Cache priority level
            ttl_seconds: Time to live in seconds (None for no expiry)
            dependencies: List of dependency keys
            **metadata: Additional metadata
            
        Returns:
            True if successfully cached, False otherwise
        """
        with QMutexLocker(self._mutex):
            # Check memory constraints
            if not self._can_cache_item(key, value):
                self._evict_items_for_new(key, value)
            
            # Create cache item
            item = CachedSpacingItem(
                value=value,
                timestamp=time.time(),
                priority=priority,
                size_bytes=self._estimate_size(value),
                dependencies=dependencies or [],
                metadata=metadata
            )
            
            # Add to cache
            self._cache[key] = item
            self._memory_usage += item.size_bytes
            self._stats['cache_size'] = len(self._cache)
            self._stats['memory_usage'] = self._memory_usage
            
            # Update strategy-specific data
            self._update_strategy_data(key, item, ttl_seconds)
            
            return True
    
    def invalidate_cache(self, 
                        pattern: Optional[str] = None,
                        dependencies: Optional[List[str]] = None) -> int:
        """
        Invalidate cache entries based on pattern or dependencies.
        
        Args:
            pattern: String pattern to match keys (None for all)
            dependencies: List of dependency keys to invalidate
            
        Returns:
            Number of invalidated entries
        """
        with QMutexLocker(self._mutex):
            invalidated_count = 0
            
            if pattern:
                # Pattern-based invalidation
                keys_to_remove = [
                    key for key in self._cache.keys()
                    if pattern in key
                ]
            elif dependencies:
                # Dependency-based invalidation
                keys_to_remove = [
                    key for key, item in self._cache.items()
                    if any(dep in item.dependencies for dep in dependencies)
                ]
            else:
                # Invalidate all
                keys_to_remove = list(self._cache.keys())
            
            for key in keys_to_remove:
                self._remove_cache_item(key, "invalidation")
                invalidated_count += 1
            
            return invalidated_count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        with QMutexLocker(self._mutex):
            stats = self._stats.copy()
            
            # Calculate additional metrics
            total_requests = stats['hits'] + stats['misses']
            stats['hit_rate'] = stats['hits'] / max(1, total_requests)
            stats['memory_usage_mb'] = stats['memory_usage'] / (1024 * 1024)
            stats['max_memory_mb'] = self._max_memory_bytes / (1024 * 1024)
            stats['memory_usage_percent'] = (stats['memory_usage'] / self._max_memory_bytes) * 100
            
            # Strategy-specific stats
            stats['strategy'] = self._strategy.value
            stats['lru_order_length'] = len(self._lru_order)
            stats['lfu_unique_counts'] = len(set(self._lfu_counts.values()))
            stats['ttl_expiry_count'] = len(self._ttl_expiry)
            
            return stats
    
    def optimize_cache(self) -> Dict[str, Any]:
        """
        Perform cache optimization based on current strategy.
        
        Returns:
            Optimization results and recommendations
        """
        with QMutexLocker(self._mutex):
            optimization_results = {
                'items_removed': 0,
                'memory_freed': 0,
                'strategy_changed': False,
                'recommendations': []
            }
            
            # Analyze cache performance
            hit_rate = self._stats['hits'] / max(1, self._stats['hits'] + self._stats['misses'])
            
            # Adaptive strategy adjustment
            if self._strategy == CacheStrategy.ADAPTIVE:
                if hit_rate < 0.3:  # Low hit rate
                    self._strategy = CacheStrategy.LRU
                    optimization_results['strategy_changed'] = True
                    optimization_results['recommendations'].append("Switched to LRU strategy due to low hit rate")
                elif hit_rate > 0.8:  # High hit rate
                    self._strategy = CacheStrategy.TTL
                    optimization_results['strategy_changed'] = True
                    optimization_results['recommendations'].append("Switched to TTL strategy due to high hit rate")
            
            # Strategy-specific optimization
            if self._strategy == CacheStrategy.LRU:
                removed = self._optimize_lru()
            elif self._strategy == CacheStrategy.LFU:
                removed = self._optimize_lfu()
            elif self._strategy == CacheStrategy.TTL:
                removed = self._optimize_ttl()
            else:
                removed = self._optimize_adaptive()
            
            optimization_results['items_removed'] = removed
            optimization_results['memory_freed'] = self._stats['memory_usage'] - self._memory_usage
            
            return optimization_results
    
    def preload_spacing_values(self, 
                              spacing_keys: List[Tuple[str, SpacingUnit, dict]],
                              priority: CachePriority = CachePriority.LOW) -> int:
        """
        Preload common spacing values into cache.
        
        Args:
            spacing_keys: List of (key, spacing_unit, kwargs) tuples
            priority: Priority for preloaded items
            
        Returns:
            Number of successfully preloaded items
        """
        preloaded_count = 0
        
        for key, spacing_unit, kwargs in spacing_keys:
            try:
                # Calculate spacing value
                base_value = spacing_unit.value
                responsive_value = responsive_spacing_manager.get_responsive_spacing(
                    base_value, 
                    kwargs.get('touch_friendly', False)
                )
                
                # Cache with low priority
                if self.cache_spacing(key, responsive_value, priority=priority):
                    preloaded_count += 1
                    
            except Exception as e:
                print(f"Error preloading spacing for key '{key}': {e}")
        
        return preloaded_count
    
    def _get_from_cache(self, key: str) -> Optional[CachedSpacingItem]:
        """Get item from cache if it exists and is valid."""
        if key not in self._cache:
            return None
        
        item = self._cache[key]
        
        # Check TTL if applicable
        if key in self._ttl_expiry and time.time() > self._ttl_expiry[key]:
            self._remove_cache_item(key, "ttl_expired")
            return None
        
        return item
    
    def _update_access_stats(self, key: str):
        """Update access statistics for a cache key."""
        if key in self._cache:
            item = self._cache[key]
            item.access_count += 1
            item.last_access = time.time()
            
            # Update LRU order
            if key in self._lru_order:
                self._lru_order.remove(key)
            self._lru_order.append(key)
            
            # Update LFU counts
            self._lfu_counts[key] = self._lfu_counts.get(key, 0) + 1
    
    def _can_cache_item(self, key: str, value: Any) -> bool:
        """Check if we can cache an item without exceeding memory limits."""
        estimated_size = self._estimate_size(value)
        return (self._memory_usage + estimated_size) <= self._max_memory_bytes
    
    def _evict_items_for_new(self, key: str, value: Any):
        """Evict items to make room for a new cache entry."""
        estimated_size = self._estimate_size(value)
        required_space = estimated_size - (self._max_memory_bytes - self._memory_usage)
        
        if required_space <= 0:
            return
        
        # Evict items based on strategy
        evicted_size = 0
        while evicted_size < required_space and self._cache:
            if self._strategy == CacheStrategy.LRU:
                evicted_key = self._lru_order[0] if self._lru_order else None
            elif self._strategy == CacheStrategy.LFU:
                evicted_key = min(self._lfu_counts.keys(), 
                                key=lambda k: self._lfu_counts[k]) if self._lfu_counts else None
            elif self._strategy == CacheStrategy.TTL:
                evicted_key = min(self._ttl_expiry.keys(), 
                                key=lambda k: self._ttl_expiry[k]) if self._ttl_expiry else None
            else:
                evicted_key = next(iter(self._cache.keys()), None)
            
            if evicted_key and evicted_key in self._cache:
                evicted_size += self._cache[evicted_key].size_bytes
                self._remove_cache_item(evicted_key, "memory_pressure")
            else:
                break
    
    def _remove_cache_item(self, key: str, reason: str):
        """Remove a cache item and update statistics."""
        if key in self._cache:
            item = self._cache[key]
            self._memory_usage -= item.size_bytes
            
            # Remove from strategy-specific data
            self._lru_order = [k for k in self._lru_order if k != key]
            self._lfu_counts.pop(key, None)
            self._ttl_expiry.pop(key, None)
            
            # Remove from main cache
            del self._cache[key]
            
            # Update statistics
            self._stats['evictions'] += 1
            self._stats['cache_size'] = len(self._cache)
            self._stats['memory_usage'] = self._memory_usage
            
            # Emit signal
            self.cache_eviction.emit(key, reason)
    
    def _estimate_size(self, value: Any) -> int:
        """Estimate memory size of a value in bytes."""
        if isinstance(value, (int, float)):
            return 8
        elif isinstance(value, str):
            return len(value.encode('utf-8'))
        elif isinstance(value, (list, tuple)):
            return sum(self._estimate_size(item) for item in value)
        elif isinstance(value, dict):
            return sum(self._estimate_size(k) + self._estimate_size(v) 
                      for k, v in value.items())
        else:
            return 64  # Default estimate for unknown types
    
    def _update_strategy_data(self, key: str, item: CachedSpacingItem, ttl_seconds: Optional[float]):
        """Update strategy-specific data structures."""
        # LRU
        self._lru_order.append(key)
        
        # LFU
        self._lfu_counts[key] = 0
        
        # TTL
        if ttl_seconds:
            self._ttl_expiry[key] = time.time() + ttl_seconds
    
    def _perform_cleanup(self):
        """Perform periodic cache cleanup."""
        with QMutexLocker(self._mutex):
            # Remove expired TTL items
            current_time = time.time()
            expired_keys = [
                key for key, expiry in self._ttl_expiry.items()
                if current_time > expiry
            ]
            
            for key in expired_keys:
                self._remove_cache_item(key, "ttl_expired")
            
            # Memory pressure cleanup
            if self._memory_usage > self._max_memory_bytes * 0.9:  # 90% threshold
                self._evict_items_for_new("", None)
    
    def _update_performance_metrics(self):
        """Update and emit performance metrics."""
        stats = self.get_cache_stats()
        self.performance_update.emit(stats)
        
        # Memory warning if usage is high
        if stats['memory_usage_percent'] > 80:
            self.memory_warning.emit(stats['memory_usage'])
    
    def _optimize_lru(self) -> int:
        """Optimize cache using LRU strategy."""
        removed_count = 0
        target_size = len(self._cache) // 2  # Remove 50% of items
        
        while len(self._cache) > target_size and self._lru_order:
            key = self._lru_order.pop(0)
            if key in self._cache:
                self._remove_cache_item(key, "lru_optimization")
                removed_count += 1
        
        return removed_count
    
    def _optimize_lfu(self) -> int:
        """Optimize cache using LFU strategy."""
        removed_count = 0
        target_size = len(self._cache) // 2
        
        # Sort by frequency (ascending)
        sorted_keys = sorted(self._lfu_counts.keys(), 
                           key=lambda k: self._lfu_counts[k])
        
        for key in sorted_keys:
            if removed_count >= target_size:
                break
            if key in self._cache:
                self._remove_cache_item(key, "lfu_optimization")
                removed_count += 1
        
        return removed_count
    
    def _optimize_ttl(self) -> int:
        """Optimize cache using TTL strategy."""
        removed_count = 0
        current_time = time.time()
        
        # Remove items that are close to expiry
        for key, expiry in self._ttl_expiry.items():
            if expiry - current_time < 60:  # Remove if expires within 1 minute
                if key in self._cache:
                    self._remove_cache_item(key, "ttl_optimization")
                    removed_count += 1
        
        return removed_count
    
    def _optimize_adaptive(self) -> int:
        """Optimize cache using adaptive strategy."""
        # Use current strategy for optimization
        if self._strategy == CacheStrategy.LRU:
            return self._optimize_lru()
        elif self._strategy == CacheStrategy.LFU:
            return self._optimize_lfu()
        elif self._strategy == CacheStrategy.TTL:
            return self._optimize_ttl()
        else:
            return 0


# Global instance for easy access
spacing_cache_system = SpacingCacheSystem()
