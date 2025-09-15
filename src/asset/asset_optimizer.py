"""
Asset Optimizer for Nexlify Engine.

This module provides asset optimization functionality including
compression, format conversion, and AI-powered optimization.
"""

import logging
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

from .asset_pipeline import AssetInfo, AssetType
from ..utils.logger import get_logger


class AssetOptimizer:
    """Asset optimization system."""
    
    def __init__(self, ai_manager=None):
        self.ai_manager = ai_manager
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Optimization settings
        self.enable_compression = True
        self.enable_format_conversion = True
        self.enable_ai_optimization = True
        
        # Compression settings
        self.texture_compression_quality = 85
        self.audio_compression_quality = 128
        self.mesh_compression_level = 6
        
        # Performance tracking
        self.assets_optimized = 0
        self.total_size_saved = 0
        self.optimization_time = 0.0
        
    def initialize(self) -> bool:
        """Initialize the asset optimizer.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing asset optimizer...")
            
            # Create optimization directories
            Path("assets/optimized").mkdir(parents=True, exist_ok=True)
            Path("assets/compressed").mkdir(parents=True, exist_ok=True)
            
            self.is_initialized = True
            self.logger.info("✅ Asset optimizer initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize asset optimizer: {e}")
            return False
    
    def optimize_asset(self, asset_info: AssetInfo) -> bool:
        """Optimize an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if optimized successfully, False otherwise
        """
        if not self.is_initialized:
            return False
        
        try:
            # Check if asset is already optimized
            if asset_info.optimized:
                self.logger.debug(f"Asset already optimized: {asset_info.name}")
                return True
            
            # Optimize based on asset type
            if asset_info.type == AssetType.TEXTURE:
                return self._optimize_texture(asset_info)
            elif asset_info.type == AssetType.MESH:
                return self._optimize_mesh(asset_info)
            elif asset_info.type == AssetType.AUDIO:
                return self._optimize_audio(asset_info)
            elif asset_info.type == AssetType.SCRIPT:
                return self._optimize_script(asset_info)
            elif asset_info.type == AssetType.MATERIAL:
                return self._optimize_material(asset_info)
            elif asset_info.type == AssetType.SHADER:
                return self._optimize_shader(asset_info)
            else:
                self.logger.debug(f"No optimization needed for asset type: {asset_info.type}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error optimizing asset {asset_info.name}: {e}")
            return False
    
    def _optimize_texture(self, asset_info: AssetInfo) -> bool:
        """Optimize a texture asset.
        
        Args:
            asset_info: Texture asset information
            
        Returns:
            True if optimized successfully, False otherwise
        """
        try:
            from PIL import Image
            
            # Load original image
            image = Image.open(asset_info.file_path)
            
            # Get original size
            original_size = os.path.getsize(asset_info.file_path)
            
            # Optimize image
            optimized_image = self._optimize_image(image)
            
            # Save optimized image
            optimized_path = f"assets/optimized/{asset_info.name}_optimized.png"
            optimized_image.save(optimized_path, "PNG", optimize=True, quality=self.texture_compression_quality)
            
            # Get optimized size
            optimized_size = os.path.getsize(optimized_path)
            
            # Update asset info
            asset_info.optimized = True
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['optimized_path'] = optimized_path
            asset_info.metadata['original_size'] = original_size
            asset_info.metadata['optimized_size'] = optimized_size
            asset_info.metadata['compression_ratio'] = optimized_size / original_size
            
            # Update statistics
            self.assets_optimized += 1
            self.total_size_saved += original_size - optimized_size
            
            self.logger.info(f"Optimized texture: {asset_info.name} ({original_size} -> {optimized_size} bytes)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing texture {asset_info.name}: {e}")
            return False
    
    def _optimize_image(self, image):
        """Optimize an image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Optimized PIL Image object
        """
        try:
            from PIL import Image
            
            # Convert to RGB if necessary (for JPEG optimization)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large
            max_size = 2048
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            self.logger.error(f"Error optimizing image: {e}")
            return image
    
    def _optimize_mesh(self, asset_info: AssetInfo) -> bool:
        """Optimize a mesh asset.
        
        Args:
            asset_info: Mesh asset information
            
        Returns:
            True if optimized successfully, False otherwise
        """
        try:
            # TODO: Implement actual mesh optimization
            # This would involve:
            # - Vertex optimization
            # - Triangle reduction
            # - UV optimization
            # - Normal recalculation
            
            # For now, mark as optimized
            asset_info.optimized = True
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['optimization_applied'] = 'placeholder'
            
            self.assets_optimized += 1
            self.logger.debug(f"Optimized mesh: {asset_info.name} (placeholder)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing mesh {asset_info.name}: {e}")
            return False
    
    def _optimize_audio(self, asset_info: AssetInfo) -> bool:
        """Optimize an audio asset.
        
        Args:
            asset_info: Audio asset information
            
        Returns:
            True if optimized successfully, False otherwise
        """
        try:
            # TODO: Implement actual audio optimization
            # This would involve:
            # - Audio compression
            # - Format conversion
            # - Quality optimization
            
            # For now, mark as optimized
            asset_info.optimized = True
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['optimization_applied'] = 'placeholder'
            
            self.assets_optimized += 1
            self.logger.debug(f"Optimized audio: {asset_info.name} (placeholder)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing audio {asset_info.name}: {e}")
            return False
    
    def _optimize_script(self, asset_info: AssetInfo) -> bool:
        """Optimize a script asset.
        
        Args:
            asset_info: Script asset information
            
        Returns:
            True if optimized successfully, False otherwise
        """
        try:
            # Read script content
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic script optimization
            optimized_content = self._optimize_script_content(content)
            
            # Save optimized script
            optimized_path = f"assets/optimized/{asset_info.name}_optimized.py"
            with open(optimized_path, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            # Update asset info
            asset_info.optimized = True
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['optimized_path'] = optimized_path
            asset_info.metadata['original_size'] = len(content)
            asset_info.metadata['optimized_size'] = len(optimized_content)
            
            self.assets_optimized += 1
            self.logger.debug(f"Optimized script: {asset_info.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing script {asset_info.name}: {e}")
            return False
    
    def _optimize_script_content(self, content: str) -> str:
        """Optimize script content.
        
        Args:
            content: Original script content
            
        Returns:
            Optimized script content
        """
        try:
            # Basic optimizations
            lines = content.splitlines()
            optimized_lines = []
            
            for line in lines:
                # Remove trailing whitespace
                line = line.rstrip()
                
                # Skip empty lines at the beginning
                if not optimized_lines and not line:
                    continue
                
                optimized_lines.append(line)
            
            # Remove trailing empty lines
            while optimized_lines and not optimized_lines[-1]:
                optimized_lines.pop()
            
            return '\n'.join(optimized_lines)
            
        except Exception as e:
            self.logger.error(f"Error optimizing script content: {e}")
            return content
    
    def _optimize_material(self, asset_info: AssetInfo) -> bool:
        """Optimize a material asset.
        
        Args:
            asset_info: Material asset information
            
        Returns:
            True if optimized successfully, False otherwise
        """
        try:
            import json
            
            # Read material data
            with open(asset_info.file_path, 'r') as f:
                material_data = json.load(f)
            
            # Optimize material data
            optimized_data = self._optimize_material_data(material_data)
            
            # Save optimized material
            optimized_path = f"assets/optimized/{asset_info.name}_optimized.json"
            with open(optimized_path, 'w') as f:
                json.dump(optimized_data, f, separators=(',', ':'))
            
            # Update asset info
            asset_info.optimized = True
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['optimized_path'] = optimized_path
            
            self.assets_optimized += 1
            self.logger.debug(f"Optimized material: {asset_info.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing material {asset_info.name}: {e}")
            return False
    
    def _optimize_material_data(self, material_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize material data.
        
        Args:
            material_data: Original material data
            
        Returns:
            Optimized material data
        """
        try:
            # Remove unnecessary properties
            optimized_data = {}
            
            # Keep essential properties
            essential_props = ['name', 'type', 'properties', 'shader', 'textures']
            for prop in essential_props:
                if prop in material_data:
                    optimized_data[prop] = material_data[prop]
            
            return optimized_data
            
        except Exception as e:
            self.logger.error(f"Error optimizing material data: {e}")
            return material_data
    
    def _optimize_shader(self, asset_info: AssetInfo) -> bool:
        """Optimize a shader asset.
        
        Args:
            asset_info: Shader asset information
            
        Returns:
            True if optimized successfully, False otherwise
        """
        try:
            # Read shader source
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Optimize shader source
            optimized_source = self._optimize_shader_source(source)
            
            # Save optimized shader
            optimized_path = f"assets/optimized/{asset_info.name}_optimized.glsl"
            with open(optimized_path, 'w', encoding='utf-8') as f:
                f.write(optimized_source)
            
            # Update asset info
            asset_info.optimized = True
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['optimized_path'] = optimized_path
            asset_info.metadata['original_size'] = len(source)
            asset_info.metadata['optimized_size'] = len(optimized_source)
            
            self.assets_optimized += 1
            self.logger.debug(f"Optimized shader: {asset_info.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing shader {asset_info.name}: {e}")
            return False
    
    def _optimize_shader_source(self, source: str) -> str:
        """Optimize shader source code.
        
        Args:
            source: Original shader source
            
        Returns:
            Optimized shader source
        """
        try:
            lines = source.splitlines()
            optimized_lines = []
            
            for line in lines:
                # Remove trailing whitespace
                line = line.rstrip()
                
                # Skip empty lines at the beginning
                if not optimized_lines and not line:
                    continue
                
                optimized_lines.append(line)
            
            # Remove trailing empty lines
            while optimized_lines and not optimized_lines[-1]:
                optimized_lines.pop()
            
            return '\n'.join(optimized_lines)
            
        except Exception as e:
            self.logger.error(f"Error optimizing shader source: {e}")
            return source
    
    def compress_asset(self, asset_info: AssetInfo) -> bool:
        """Compress an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if compressed successfully, False otherwise
        """
        if not self.enable_compression:
            return True
        
        try:
            import gzip
            import shutil
            
            # Compress the asset file
            compressed_path = f"assets/compressed/{asset_info.name}.gz"
            
            with open(asset_info.file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Update asset info
            asset_info.compressed = True
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['compressed_path'] = compressed_path
            
            # Get compression ratio
            original_size = os.path.getsize(asset_info.file_path)
            compressed_size = os.path.getsize(compressed_path)
            compression_ratio = compressed_size / original_size
            
            asset_info.metadata['compression_ratio'] = compression_ratio
            
            self.logger.debug(f"Compressed asset: {asset_info.name} (ratio: {compression_ratio:.2f})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error compressing asset {asset_info.name}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get asset optimizer statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "assets_optimized": self.assets_optimized,
            "total_size_saved": self.total_size_saved,
            "optimization_time": self.optimization_time,
            "compression_enabled": self.enable_compression,
            "format_conversion_enabled": self.enable_format_conversion,
            "ai_optimization_enabled": self.enable_ai_optimization
        }
    
    def shutdown(self):
        """Shutdown the asset optimizer."""
        if self.is_initialized:
            self.logger.info("Shutting down asset optimizer...")
            
            self.is_initialized = False
            self.logger.info("✅ Asset optimizer shutdown complete")
