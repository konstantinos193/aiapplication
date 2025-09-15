"""
Asset Loader for Nexlify Engine.

This module provides asset loading functionality including
format-specific loaders and data conversion.
"""

import logging
import os
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path
import time

from .asset_pipeline import AssetInfo, AssetType
from ..utils.logger import get_logger


class AssetLoader:
    """Asset loading system."""
    
    def __init__(self, ai_manager=None):
        self.ai_manager = ai_manager
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Loader settings
        self.enable_caching = True
        self.enable_validation = True
        self.enable_conversion = True
        
        # Loader registry
        self.loaders = {
            AssetType.TEXTURE: self._load_texture,
            AssetType.MESH: self._load_mesh,
            AssetType.AUDIO: self._load_audio,
            AssetType.SCRIPT: self._load_script,
            AssetType.MATERIAL: self._load_material,
            AssetType.SHADER: self._load_shader
        }
        
        # Performance tracking
        self.assets_loaded = 0
        self.load_time = 0.0
        self.load_errors = 0
        
    def initialize(self) -> bool:
        """Initialize the asset loader.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing asset loader...")
            
            # Create loader directories
            Path("assets/loaded").mkdir(parents=True, exist_ok=True)
            Path("assets/converted").mkdir(parents=True, exist_ok=True)
            
            self.is_initialized = True
            self.logger.info("✅ Asset loader initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize asset loader: {e}")
            return False
    
    def load_asset(self, asset_info: AssetInfo) -> Optional[Any]:
        """Load an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            Loaded asset data or None if failed
        """
        if not self.is_initialized:
            return None
        
        try:
            start_time = time.time()
            
            # Validate asset info
            if not self._validate_asset_info(asset_info):
                return None
            
            # Get loader for asset type
            loader = self.loaders.get(asset_info.type)
            if loader is None:
                self.logger.error(f"No loader available for asset type: {asset_info.type}")
                self.load_errors += 1
                return None
            
            # Load the asset
            asset_data = loader(asset_info)
            if asset_data is None:
                self.load_errors += 1
                return None
            
            # Update statistics
            self.assets_loaded += 1
            self.load_time += time.time() - start_time
            
            # Update access time
            asset_info.accessed_at = time.time()
            
            self.logger.debug(f"Loaded asset: {asset_info.name}")
            return asset_data
            
        except Exception as e:
            self.logger.error(f"Error loading asset {asset_info.name}: {e}")
            self.load_errors += 1
            return None
    
    def _validate_asset_info(self, asset_info: AssetInfo) -> bool:
        """Validate asset information.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(asset_info.file_path):
                self.logger.error(f"Asset file not found: {asset_info.file_path}")
                return False
            
            # Check file size
            if asset_info.size == 0:
                self.logger.error(f"Asset file is empty: {asset_info.name}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating asset info {asset_info.name}: {e}")
            return False
    
    def _load_texture(self, asset_info: AssetInfo) -> Optional[Any]:
        """Load a texture asset.
        
        Args:
            asset_info: Texture asset information
            
        Returns:
            Loaded texture data or None if failed
        """
        try:
            from PIL import Image
            
            # Load the image
            with Image.open(asset_info.file_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Update metadata
                asset_info.metadata = asset_info.metadata or {}
                asset_info.metadata['width'] = img.size[0]
                asset_info.metadata['height'] = img.size[1]
                asset_info.metadata['format'] = img.format
                asset_info.metadata['mode'] = img.mode
                
                return img
                
        except Exception as e:
            self.logger.error(f"Error loading texture {asset_info.name}: {e}")
            return None
    
    def _load_mesh(self, asset_info: AssetInfo) -> Optional[Any]:
        """Load a mesh asset.
        
        Args:
            asset_info: Mesh asset information
            
        Returns:
            Loaded mesh data or None if failed
        """
        try:
            # TODO: Implement actual mesh loading
            # This would involve:
            # - Loading with assimp or similar library
            # - Extracting vertices, normals, UVs, indices
            # - Converting to engine format
            
            # For now, return a placeholder
            mesh_data = {
                'vertices': [],
                'normals': [],
                'uvs': [],
                'indices': [],
                'materials': []
            }
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['vertex_count'] = 0
            asset_info.metadata['face_count'] = 0
            asset_info.metadata['material_count'] = 0
            
            return mesh_data
            
        except Exception as e:
            self.logger.error(f"Error loading mesh {asset_info.name}: {e}")
            return None
    
    def _load_audio(self, asset_info: AssetInfo) -> Optional[Any]:
        """Load an audio asset.
        
        Args:
            asset_info: Audio asset information
            
        Returns:
            Loaded audio data or None if failed
        """
        try:
            # TODO: Implement actual audio loading
            # This would involve:
            # - Loading with librosa or similar library
            # - Extracting audio data, sample rate, channels
            # - Converting to engine format
            
            # For now, return a placeholder
            audio_data = {
                'data': None,
                'sample_rate': 44100,
                'channels': 2,
                'duration': 0.0
            }
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['sample_rate'] = 44100
            asset_info.metadata['channels'] = 2
            asset_info.metadata['duration'] = 0.0
            
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Error loading audio {asset_info.name}: {e}")
            return None
    
    def _load_script(self, asset_info: AssetInfo) -> Optional[Any]:
        """Load a script asset.
        
        Args:
            asset_info: Script asset information
            
        Returns:
            Loaded script data or None if failed
        """
        try:
            # Read script content
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['line_count'] = len(content.splitlines())
            asset_info.metadata['char_count'] = len(content)
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error loading script {asset_info.name}: {e}")
            return None
    
    def _load_material(self, asset_info: AssetInfo) -> Optional[Any]:
        """Load a material asset.
        
        Args:
            asset_info: Material asset information
            
        Returns:
            Loaded material data or None if failed
        """
        try:
            import json
            
            # Read material data
            with open(asset_info.file_path, 'r') as f:
                material_data = json.load(f)
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['material_type'] = material_data.get('type')
            asset_info.metadata['has_shader'] = 'shader' in material_data
            asset_info.metadata['has_textures'] = 'textures' in material_data
            asset_info.metadata['property_count'] = len(material_data.get('properties', {}))
            
            return material_data
            
        except Exception as e:
            self.logger.error(f"Error loading material {asset_info.name}: {e}")
            return None
    
    def _load_shader(self, asset_info: AssetInfo) -> Optional[Any]:
        """Load a shader asset.
        
        Args:
            asset_info: Shader asset information
            
        Returns:
            Loaded shader data or None if failed
        """
        try:
            # Read shader source
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['line_count'] = len(source.splitlines())
            asset_info.metadata['char_count'] = len(source)
            asset_info.metadata['has_vertex'] = 'gl_Position' in source or 'SV_Position' in source
            asset_info.metadata['has_fragment'] = 'gl_FragColor' in source or 'SV_Target' in source
            
            return source
            
        except Exception as e:
            self.logger.error(f"Error loading shader {asset_info.name}: {e}")
            return None
    
    def get_loader_stats(self) -> Dict[str, Any]:
        """Get loader statistics.
        
        Returns:
            Dictionary of loader statistics
        """
        try:
            return {
                "assets_loaded": self.assets_loaded,
                "load_time": self.load_time,
                "load_errors": self.load_errors,
                "average_load_time": self.load_time / max(1, self.assets_loaded),
                "caching_enabled": self.enable_caching,
                "validation_enabled": self.enable_validation,
                "conversion_enabled": self.enable_conversion
            }
            
        except Exception as e:
            self.logger.error(f"Error getting loader stats: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown the asset loader."""
        if self.is_initialized:
            self.logger.info("Shutting down asset loader...")
            
            self.is_initialized = False
            self.logger.info("✅ Asset loader shutdown complete")