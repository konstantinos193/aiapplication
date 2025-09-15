"""
Asset Manager for Nexlify Engine.

This module provides asset management functionality including
loading, caching, and lifecycle management.
"""

import logging
import os
import time
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path
import threading

from .asset_pipeline import AssetInfo, AssetType
from .asset_loader import AssetLoader
from .asset_cache import AssetCache
from .asset_importer import AssetImporter
from .asset_processor import AssetProcessor
from .asset_optimizer import AssetOptimizer
from ..utils.logger import get_logger


class AssetManager:
    """Asset management system."""
    
    def __init__(self, ai_manager=None):
        self.ai_manager = ai_manager
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Asset storage
        self.assets: Dict[str, AssetInfo] = {}
        self.asset_lock = threading.RLock()
        
        # Subsystems
        self.loader = AssetLoader(ai_manager)
        self.cache = AssetCache()
        self.importer = AssetImporter(ai_manager)
        self.processor = AssetProcessor(ai_manager)
        self.optimizer = AssetOptimizer(ai_manager)
        
        # Settings
        self.enable_caching = True
        self.enable_processing = True
        self.enable_optimization = True
        self.enable_auto_import = True
        
        # Performance tracking
        self.assets_loaded = 0
        self.assets_imported = 0
        self.load_time = 0.0
        self.import_time = 0.0
        
    def initialize(self) -> bool:
        """Initialize the asset manager.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing asset manager...")
            
            # Initialize subsystems
            if not self.loader.initialize():
                return False
            
            if not self.cache.initialize():
                return False
            
            if not self.importer.initialize():
                return False
            
            if not self.processor.initialize():
                return False
            
            if not self.optimizer.initialize():
                return False
            
            # Create asset directories
            Path("assets").mkdir(parents=True, exist_ok=True)
            Path("assets/textures").mkdir(parents=True, exist_ok=True)
            Path("assets/meshes").mkdir(parents=True, exist_ok=True)
            Path("assets/audio").mkdir(parents=True, exist_ok=True)
            Path("assets/scripts").mkdir(parents=True, exist_ok=True)
            Path("assets/materials").mkdir(parents=True, exist_ok=True)
            Path("assets/shaders").mkdir(parents=True, exist_ok=True)
            
            self.is_initialized = True
            self.logger.info("✅ Asset manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize asset manager: {e}")
            return False
    
    def load_asset(self, asset_path: str, asset_type: Optional[AssetType] = None) -> Optional[Any]:
        """Load an asset.
        
        Args:
            asset_path: Path to the asset
            asset_type: Asset type (auto-detected if None)
            
        Returns:
            Loaded asset data or None if failed
        """
        if not self.is_initialized:
            return None
        
        try:
            start_time = time.time()
            
            # Check cache first
            if self.enable_caching:
                cached_data = self.cache.get_asset(asset_path)
                if cached_data is not None:
                    self.assets_loaded += 1
                    self.load_time += time.time() - start_time
                    return cached_data
            
            # Get or create asset info
            asset_info = self.get_asset_info(asset_path)
            if asset_info is None:
                if self.enable_auto_import:
                    asset_info = self.import_asset(asset_path, asset_type)
                    if asset_info is None:
                        return None
                else:
                    return None
            
            # Load asset data
            asset_data = self.loader.load_asset(asset_info)
            if asset_data is None:
                return None
            
            # Cache the asset
            if self.enable_caching:
                self.cache.put_asset(asset_path, asset_data, asset_info)
            
            self.assets_loaded += 1
            self.load_time += time.time() - start_time
            
            self.logger.debug(f"Loaded asset: {asset_info.name}")
            return asset_data
            
        except Exception as e:
            self.logger.error(f"Error loading asset {asset_path}: {e}")
            return None
    
    def import_asset(self, file_path: str, asset_type: Optional[AssetType] = None) -> Optional[AssetInfo]:
        """Import an asset from file.
        
        Args:
            file_path: Path to the asset file
            asset_type: Asset type (auto-detected if None)
            
        Returns:
            AssetInfo object or None if import failed
        """
        if not self.is_initialized:
            return None
        
        try:
            start_time = time.time()
            
            # Import the asset
            asset_info = self.importer.import_asset(file_path, asset_type)
            if asset_info is None:
                return None
            
            # Process the asset
            if self.enable_processing:
                self.processor.process_asset(asset_info)
            
            # Optimize the asset
            if self.enable_optimization:
                self.optimizer.optimize_asset(asset_info)
            
            # Store asset info
            with self.asset_lock:
                self.assets[asset_info.name] = asset_info
            
            self.assets_imported += 1
            self.import_time += time.time() - start_time
            
            self.logger.info(f"Imported asset: {asset_info.name}")
            return asset_info
            
        except Exception as e:
            self.logger.error(f"Error importing asset {file_path}: {e}")
            return None
    
    def get_asset_info(self, asset_path: str) -> Optional[AssetInfo]:
        """Get asset information.
        
        Args:
            asset_path: Path to the asset
            
        Returns:
            AssetInfo object or None if not found
        """
        try:
            with self.asset_lock:
                # Try to find by path
                for asset_info in self.assets.values():
                    if asset_info.file_path == asset_path:
                        return asset_info
                
                # Try to find by name
                asset_name = Path(asset_path).stem
                if asset_name in self.assets:
                    return self.assets[asset_name]
                
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting asset info {asset_path}: {e}")
            return None
    
    def get_asset_by_name(self, name: str) -> Optional[AssetInfo]:
        """Get asset information by name.
        
        Args:
            name: Asset name
            
        Returns:
            AssetInfo object or None if not found
        """
        try:
            with self.asset_lock:
                return self.assets.get(name)
                
        except Exception as e:
            self.logger.error(f"Error getting asset by name {name}: {e}")
            return None
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[AssetInfo]:
        """Get all assets of a specific type.
        
        Args:
            asset_type: Asset type
            
        Returns:
            List of AssetInfo objects
        """
        try:
            with self.asset_lock:
                return [asset_info for asset_info in self.assets.values() 
                       if asset_info.type == asset_type]
                
        except Exception as e:
            self.logger.error(f"Error getting assets by type {asset_type}: {e}")
            return []
    
    def get_all_assets(self) -> List[AssetInfo]:
        """Get all assets.
        
        Returns:
            List of all AssetInfo objects
        """
        try:
            with self.asset_lock:
                return list(self.assets.values())
                
        except Exception as e:
            self.logger.error(f"Error getting all assets: {e}")
            return []
    
    def unload_asset(self, asset_path: str) -> bool:
        """Unload an asset.
        
        Args:
            asset_path: Path to the asset
            
        Returns:
            True if unloaded successfully, False otherwise
        """
        try:
            # Remove from cache
            if self.enable_caching:
                self.cache.remove_asset(asset_path)
            
            # Remove from asset storage
            with self.asset_lock:
                asset_name = Path(asset_path).stem
                if asset_name in self.assets:
                    del self.assets[asset_name]
                    self.logger.debug(f"Unloaded asset: {asset_name}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error unloading asset {asset_path}: {e}")
            return False
    
    def reload_asset(self, asset_path: str) -> bool:
        """Reload an asset.
        
        Args:
            asset_path: Path to the asset
            
        Returns:
            True if reloaded successfully, False otherwise
        """
        try:
            # Unload first
            self.unload_asset(asset_path)
            
            # Reload
            asset_data = self.load_asset(asset_path)
            return asset_data is not None
            
        except Exception as e:
            self.logger.error(f"Error reloading asset {asset_path}: {e}")
            return False
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[AssetInfo]:
        """Scan directory for assets.
        
        Args:
            directory: Directory to scan
            recursive: Whether to scan recursively
            
        Returns:
            List of found AssetInfo objects
        """
        try:
            found_assets = []
            directory_path = Path(directory)
            
            if not directory_path.exists():
                self.logger.warning(f"Directory not found: {directory}")
                return found_assets
            
            # Get file pattern
            pattern = "**/*" if recursive else "*"
            
            # Scan for files
            for file_path in directory_path.glob(pattern):
                if file_path.is_file():
                    # Try to import the asset
                    asset_info = self.import_asset(str(file_path))
                    if asset_info is not None:
                        found_assets.append(asset_info)
            
            self.logger.info(f"Scanned directory {directory}: found {len(found_assets)} assets")
            return found_assets
            
        except Exception as e:
            self.logger.error(f"Error scanning directory {directory}: {e}")
            return []
    
    def preload_assets(self, asset_paths: List[str]):
        """Preload assets.
        
        Args:
            asset_paths: List of asset paths to preload
        """
        try:
            for asset_path in asset_paths:
                asset_info = self.get_asset_info(asset_path)
                if asset_info is not None and self.enable_caching:
                    self.cache.preload_asset(asset_path, asset_info)
            
            self.logger.info(f"Preloading {len(asset_paths)} assets")
            
        except Exception as e:
            self.logger.error(f"Error preloading assets: {e}")
    
    def optimize_cache(self):
        """Optimize asset cache."""
        try:
            if self.enable_caching:
                self.cache.optimize_cache()
            
            self.logger.info("Optimized asset cache")
            
        except Exception as e:
            self.logger.error(f"Error optimizing cache: {e}")
    
    def get_asset_stats(self) -> Dict[str, Any]:
        """Get asset statistics.
        
        Returns:
            Dictionary of asset statistics
        """
        try:
            with self.asset_lock:
                stats = {
                    "total_assets": len(self.assets),
                    "assets_by_type": {},
                    "assets_loaded": self.assets_loaded,
                    "assets_imported": self.assets_imported,
                    "load_time": self.load_time,
                    "import_time": self.import_time,
                    "caching_enabled": self.enable_caching,
                    "processing_enabled": self.enable_processing,
                    "optimization_enabled": self.enable_optimization
                }
                
                # Count assets by type
                for asset_info in self.assets.values():
                    asset_type = asset_info.type
                    if asset_type not in stats["assets_by_type"]:
                        stats["assets_by_type"][asset_type] = 0
                    stats["assets_by_type"][asset_type] += 1
                
                return stats
                
        except Exception as e:
            self.logger.error(f"Error getting asset stats: {e}")
            return {}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary of cache statistics
        """
        try:
            if self.enable_caching:
                return self.cache.get_cache_stats()
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting cache stats: {e}")
            return {}
    
    def get_supported_formats(self) -> Dict[AssetType, List[str]]:
        """Get supported file formats.
        
        Returns:
            Dictionary mapping asset types to supported extensions
        """
        try:
            return self.importer.get_supported_formats()
            
        except Exception as e:
            self.logger.error(f"Error getting supported formats: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown the asset manager."""
        if self.is_initialized:
            self.logger.info("Shutting down asset manager...")
            
            # Shutdown subsystems
            self.optimizer.shutdown()
            self.processor.shutdown()
            self.importer.shutdown()
            self.cache.shutdown()
            self.loader.shutdown()
            
            # Clear assets
            with self.asset_lock:
                self.assets.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Asset manager shutdown complete")