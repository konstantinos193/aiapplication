"""
Asset Cache for Nexlify Engine.

This module provides asset caching functionality including
memory management, LRU cache, and asset preloading.
"""

import logging
import os
import time
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path
import threading
from collections import OrderedDict

from .asset_pipeline import AssetInfo, AssetType
from ..utils.logger import get_logger


class AssetCache:
    """Asset caching system with LRU eviction."""
    
    def __init__(self, max_memory_mb: int = 512):
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Cache settings
        self.max_memory_mb = max_memory_mb
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.current_memory_usage = 0
        
        # Cache storage
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.cache_metadata: Dict[str, Dict[str, Any]] = {}
        
        # Thread safety
        self.cache_lock = threading.RLock()
        
        # Performance tracking
        self.cache_hits = 0
        self.cache_misses = 0
        self.assets_loaded = 0
        self.assets_evicted = 0
        
        # Preloading settings
        self.enable_preloading = True
        self.preload_threads = 2
        self.preload_queue = []
        self.preload_lock = threading.Lock()
        
    def initialize(self) -> bool:
        """Initialize the asset cache.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing asset cache...")
            
            # Create cache directory
            Path("assets/cache").mkdir(parents=True, exist_ok=True)
            
            # Start preloading threads
            if self.enable_preloading:
                self._start_preload_threads()
            
            self.is_initialized = True
            self.logger.info("✅ Asset cache initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize asset cache: {e}")
            return False
    
    def get_asset(self, asset_path: str) -> Optional[Any]:
        """Get an asset from cache.
        
        Args:
            asset_path: Path to the asset
            
        Returns:
            Cached asset data or None if not found
        """
        if not self.is_initialized:
            return None
        
        with self.cache_lock:
            if asset_path in self.cache:
                # Move to end (most recently used)
                asset_data = self.cache.pop(asset_path)
                self.cache[asset_path] = asset_data
                
                # Update access time
                self.cache_metadata[asset_path]['last_access'] = time.time()
                self.cache_metadata[asset_path]['access_count'] += 1
                
                self.cache_hits += 1
                self.logger.debug(f"Cache hit: {asset_path}")
                return asset_data
            
            self.cache_misses += 1
            self.logger.debug(f"Cache miss: {asset_path}")
            return None
    
    def put_asset(self, asset_path: str, asset_data: Any, asset_info: AssetInfo) -> bool:
        """Put an asset into cache.
        
        Args:
            asset_path: Path to the asset
            asset_data: Asset data to cache
            asset_info: Asset information
            
        Returns:
            True if cached successfully, False otherwise
        """
        if not self.is_initialized:
            return False
        
        try:
            with self.cache_lock:
                # Calculate memory usage
                memory_usage = self._calculate_memory_usage(asset_data, asset_info)
                
                # Check if we need to evict assets
                while (self.current_memory_usage + memory_usage > self.max_memory_bytes and 
                       len(self.cache) > 0):
                    self._evict_least_recently_used()
                
                # Add to cache
                self.cache[asset_path] = asset_data
                self.cache_metadata[asset_path] = {
                    'size': memory_usage,
                    'type': asset_info.type,
                    'last_access': time.time(),
                    'access_count': 1,
                    'created': time.time()
                }
                
                self.current_memory_usage += memory_usage
                self.assets_loaded += 1
                
                self.logger.debug(f"Cached asset: {asset_path} ({memory_usage} bytes)")
                return True
                
        except Exception as e:
            self.logger.error(f"Error caching asset {asset_path}: {e}")
            return False
    
    def _calculate_memory_usage(self, asset_data: Any, asset_info: AssetInfo) -> int:
        """Calculate memory usage of an asset.
        
        Args:
            asset_data: Asset data
            asset_info: Asset information
            
        Returns:
            Memory usage in bytes
        """
        try:
            if asset_info.type == AssetType.TEXTURE:
                # For PIL images
                if hasattr(asset_data, 'size') and hasattr(asset_data, 'mode'):
                    width, height = asset_data.size
                    channels = len(asset_data.mode)
                    return width * height * channels
                return 1024 * 1024  # Default 1MB for textures
            
            elif asset_info.type == AssetType.MESH:
                # For mesh data
                if isinstance(asset_data, dict):
                    if 'vertices' in asset_data:
                        return len(asset_data['vertices']) * 4 * 3  # 3 floats per vertex
                    if 'indices' in asset_data:
                        return len(asset_data['indices']) * 4  # 1 int per index
                return 512 * 1024  # Default 512KB for meshes
            
            elif asset_info.type == AssetType.AUDIO:
                # For audio data
                if hasattr(asset_data, 'nbytes'):
                    return asset_data.nbytes
                return 256 * 1024  # Default 256KB for audio
            
            elif asset_info.type == AssetType.SCRIPT:
                # For script content
                if isinstance(asset_data, str):
                    return len(asset_data.encode('utf-8'))
                return 1024  # Default 1KB for scripts
            
            elif asset_info.type == AssetType.MATERIAL:
                # For material data
                if isinstance(asset_data, dict):
                    return len(str(asset_data).encode('utf-8'))
                return 1024  # Default 1KB for materials
            
            elif asset_info.type == AssetType.SHADER:
                # For shader source
                if isinstance(asset_data, str):
                    return len(asset_data.encode('utf-8'))
                return 1024  # Default 1KB for shaders
            
            return 1024  # Default 1KB for unknown types
            
        except Exception as e:
            self.logger.error(f"Error calculating memory usage: {e}")
            return 1024
    
    def _evict_least_recently_used(self):
        """Evict the least recently used asset from cache."""
        try:
            if not self.cache:
                return
            
            # Get the least recently used asset (first in OrderedDict)
            asset_path, asset_data = self.cache.popitem(last=False)
            
            # Update memory usage
            if asset_path in self.cache_metadata:
                self.current_memory_usage -= self.cache_metadata[asset_path]['size']
                del self.cache_metadata[asset_path]
            
            self.assets_evicted += 1
            self.logger.debug(f"Evicted asset from cache: {asset_path}")
            
        except Exception as e:
            self.logger.error(f"Error evicting asset from cache: {e}")
    
    def remove_asset(self, asset_path: str) -> bool:
        """Remove an asset from cache.
        
        Args:
            asset_path: Path to the asset
            
        Returns:
            True if removed successfully, False otherwise
        """
        if not self.is_initialized:
            return False
        
        try:
            with self.cache_lock:
                if asset_path in self.cache:
                    # Remove from cache
                    del self.cache[asset_path]
                    
                    # Update memory usage
                    if asset_path in self.cache_metadata:
                        self.current_memory_usage -= self.cache_metadata[asset_path]['size']
                        del self.cache_metadata[asset_path]
                    
                    self.logger.debug(f"Removed asset from cache: {asset_path}")
                    return True
                
                return False
                
        except Exception as e:
            self.logger.error(f"Error removing asset from cache {asset_path}: {e}")
            return False
    
    def clear_cache(self):
        """Clear all assets from cache."""
        if not self.is_initialized:
            return
        
        try:
            with self.cache_lock:
                self.cache.clear()
                self.cache_metadata.clear()
                self.current_memory_usage = 0
                
                self.logger.info("Cleared asset cache")
                
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")
    
    def preload_asset(self, asset_path: str, asset_info: AssetInfo):
        """Add an asset to preload queue.
        
        Args:
            asset_path: Path to the asset
            asset_info: Asset information
        """
        if not self.enable_preloading:
            return
        
        try:
            with self.preload_lock:
                self.preload_queue.append((asset_path, asset_info))
                
        except Exception as e:
            self.logger.error(f"Error adding asset to preload queue {asset_path}: {e}")
    
    def _start_preload_threads(self):
        """Start preloading threads."""
        try:
            for i in range(self.preload_threads):
                thread = threading.Thread(
                    target=self._preload_worker,
                    name=f"AssetPreloader-{i}",
                    daemon=True
                )
                thread.start()
                
        except Exception as e:
            self.logger.error(f"Error starting preload threads: {e}")
    
    def _preload_worker(self):
        """Preload worker thread."""
        while self.is_initialized:
            try:
                # Get next asset to preload
                with self.preload_lock:
                    if not self.preload_queue:
                        time.sleep(0.1)
                        continue
                    
                    asset_path, asset_info = self.preload_queue.pop(0)
                
                # Check if already cached
                if asset_path in self.cache:
                    continue
                
                # Load asset
                asset_data = self._load_asset_for_preload(asset_path, asset_info)
                if asset_data is not None:
                    self.put_asset(asset_path, asset_data, asset_info)
                
            except Exception as e:
                self.logger.error(f"Error in preload worker: {e}")
                time.sleep(0.1)
    
    def _load_asset_for_preload(self, asset_path: str, asset_info: AssetInfo) -> Optional[Any]:
        """Load an asset for preloading.
        
        Args:
            asset_path: Path to the asset
            asset_info: Asset information
            
        Returns:
            Loaded asset data or None if failed
        """
        try:
            if asset_info.type == AssetType.TEXTURE:
                from PIL import Image
                return Image.open(asset_path)
            
            elif asset_info.type == AssetType.SCRIPT:
                with open(asset_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif asset_info.type == AssetType.MATERIAL:
                import json
                with open(asset_path, 'r') as f:
                    return json.load(f)
            
            elif asset_info.type == AssetType.SHADER:
                with open(asset_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            # For other types, just return a placeholder
            return f"Preloaded: {asset_path}"
            
        except Exception as e:
            self.logger.error(f"Error loading asset for preload {asset_path}: {e}")
            return None
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary of cache statistics
        """
        with self.cache_lock:
            return {
                "cache_size": len(self.cache),
                "memory_usage_mb": self.current_memory_usage / (1024 * 1024),
                "max_memory_mb": self.max_memory_mb,
                "memory_usage_percent": (self.current_memory_usage / self.max_memory_bytes) * 100,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "hit_rate": self.cache_hits / max(1, self.cache_hits + self.cache_misses),
                "assets_loaded": self.assets_loaded,
                "assets_evicted": self.assets_evicted,
                "preload_queue_size": len(self.preload_queue)
            }
    
    def get_cache_info(self) -> List[Dict[str, Any]]:
        """Get detailed cache information.
        
        Returns:
            List of cache entry information
        """
        with self.cache_lock:
            cache_info = []
            for asset_path, metadata in self.cache_metadata.items():
                cache_info.append({
                    "path": asset_path,
                    "type": metadata['type'],
                    "size_mb": metadata['size'] / (1024 * 1024),
                    "last_access": metadata['last_access'],
                    "access_count": metadata['access_count'],
                    "created": metadata['created']
                })
            
            return cache_info
    
    def optimize_cache(self):
        """Optimize cache by removing unused assets."""
        if not self.is_initialized:
            return
        
        try:
            with self.cache_lock:
                current_time = time.time()
                assets_to_remove = []
                
                # Find assets that haven't been accessed recently
                for asset_path, metadata in self.cache_metadata.items():
                    time_since_access = current_time - metadata['last_access']
                    if time_since_access > 300:  # 5 minutes
                        assets_to_remove.append(asset_path)
                
                # Remove unused assets
                for asset_path in assets_to_remove:
                    self._evict_least_recently_used()
                
                if assets_to_remove:
                    self.logger.info(f"Optimized cache: removed {len(assets_to_remove)} unused assets")
                
        except Exception as e:
            self.logger.error(f"Error optimizing cache: {e}")
    
    def shutdown(self):
        """Shutdown the asset cache."""
        if self.is_initialized:
            self.logger.info("Shutting down asset cache...")
            
            # Clear cache
            self.clear_cache()
            
            # Stop preloading
            self.enable_preloading = False
            
            self.is_initialized = False
            self.logger.info("✅ Asset cache shutdown complete")
