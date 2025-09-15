"""
Asset Processor for Nexlify Engine.

This module provides asset processing functionality including
format conversion, validation, and preprocessing.
"""

import logging
import os
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import hashlib

from .asset_pipeline import AssetInfo, AssetType
from ..utils.logger import get_logger


class AssetProcessor:
    """Asset processing system."""
    
    def __init__(self, ai_manager=None):
        self.ai_manager = ai_manager
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Processing settings
        self.enable_validation = True
        self.enable_format_conversion = True
        self.enable_preprocessing = True
        
        # Supported formats
        self.supported_formats = {
            AssetType.TEXTURE: ['.png', '.jpg', '.jpeg', '.bmp', '.tga', '.dds'],
            AssetType.MESH: ['.obj', '.fbx', '.dae', '.gltf', '.glb'],
            AssetType.AUDIO: ['.wav', '.mp3', '.ogg', '.flac'],
            AssetType.SCRIPT: ['.py'],
            AssetType.MATERIAL: ['.json', '.mat'],
            AssetType.SHADER: ['.glsl', '.hlsl', '.vert', '.frag']
        }
        
        # Performance tracking
        self.assets_processed = 0
        self.processing_time = 0.0
        self.validation_errors = 0
        
    def initialize(self) -> bool:
        """Initialize the asset processor.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing asset processor...")
            
            # Create processing directories
            Path("assets/processed").mkdir(parents=True, exist_ok=True)
            Path("assets/validated").mkdir(parents=True, exist_ok=True)
            
            self.is_initialized = True
            self.logger.info("✅ Asset processor initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize asset processor: {e}")
            return False
    
    def process_asset(self, asset_info: AssetInfo) -> bool:
        """Process an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if processed successfully, False otherwise
        """
        if not self.is_initialized:
            return False
        
        try:
            # Validate asset
            if self.enable_validation and not self.validate_asset(asset_info):
                return False
            
            # Convert format if needed
            if self.enable_format_conversion:
                self.convert_asset_format(asset_info)
            
            # Preprocess asset
            if self.enable_preprocessing:
                self.preprocess_asset(asset_info)
            
            # Update processing status
            asset_info.processed = True
            self.assets_processed += 1
            
            self.logger.debug(f"Processed asset: {asset_info.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing asset {asset_info.name}: {e}")
            return False
    
    def validate_asset(self, asset_info: AssetInfo) -> bool:
        """Validate an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(asset_info.file_path):
                self.logger.error(f"Asset file not found: {asset_info.file_path}")
                self.validation_errors += 1
                return False
            
            # Check file size
            file_size = os.path.getsize(asset_info.file_path)
            if file_size == 0:
                self.logger.error(f"Asset file is empty: {asset_info.file_path}")
                self.validation_errors += 1
                return False
            
            # Check file extension
            file_ext = Path(asset_info.file_path).suffix.lower()
            if file_ext not in self.supported_formats.get(asset_info.type, []):
                self.logger.warning(f"Unsupported file format: {file_ext} for asset type: {asset_info.type}")
            
            # Type-specific validation
            if asset_info.type == AssetType.TEXTURE:
                return self._validate_texture(asset_info)
            elif asset_info.type == AssetType.MESH:
                return self._validate_mesh(asset_info)
            elif asset_info.type == AssetType.AUDIO:
                return self._validate_audio(asset_info)
            elif asset_info.type == AssetType.SCRIPT:
                return self._validate_script(asset_info)
            elif asset_info.type == AssetType.MATERIAL:
                return self._validate_material(asset_info)
            elif asset_info.type == AssetType.SHADER:
                return self._validate_shader(asset_info)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating asset {asset_info.name}: {e}")
            self.validation_errors += 1
            return False
    
    def _validate_texture(self, asset_info: AssetInfo) -> bool:
        """Validate a texture asset.
        
        Args:
            asset_info: Texture asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            from PIL import Image
            
            # Try to open the image
            with Image.open(asset_info.file_path) as img:
                # Check image dimensions
                width, height = img.size
                if width <= 0 or height <= 0:
                    self.logger.error(f"Invalid texture dimensions: {width}x{height}")
                    return False
                
                # Check if image is too large
                max_size = 8192
                if width > max_size or height > max_size:
                    self.logger.warning(f"Texture is very large: {width}x{height} (max: {max_size})")
                
                # Update metadata
                asset_info.metadata = asset_info.metadata or {}
                asset_info.metadata['width'] = width
                asset_info.metadata['height'] = height
                asset_info.metadata['format'] = img.format
                asset_info.metadata['mode'] = img.mode
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating texture {asset_info.name}: {e}")
            return False
    
    def _validate_mesh(self, asset_info: AssetInfo) -> bool:
        """Validate a mesh asset.
        
        Args:
            asset_info: Mesh asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # TODO: Implement actual mesh validation
            # This would involve:
            # - Checking mesh format
            # - Validating vertex data
            # - Checking for required components (positions, normals, etc.)
            
            # For now, just check if file is readable
            with open(asset_info.file_path, 'rb') as f:
                data = f.read(1024)  # Read first 1KB
                if len(data) == 0:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating mesh {asset_info.name}: {e}")
            return False
    
    def _validate_audio(self, asset_info: AssetInfo) -> bool:
        """Validate an audio asset.
        
        Args:
            asset_info: Audio asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # TODO: Implement actual audio validation
            # This would involve:
            # - Checking audio format
            # - Validating audio data
            # - Checking sample rate, channels, etc.
            
            # For now, just check if file is readable
            with open(asset_info.file_path, 'rb') as f:
                data = f.read(1024)  # Read first 1KB
                if len(data) == 0:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating audio {asset_info.name}: {e}")
            return False
    
    def _validate_script(self, asset_info: AssetInfo) -> bool:
        """Validate a script asset.
        
        Args:
            asset_info: Script asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Read script content
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic syntax validation
            try:
                compile(content, asset_info.file_path, 'exec')
            except SyntaxError as e:
                self.logger.error(f"Syntax error in script {asset_info.name}: {e}")
                return False
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['line_count'] = len(content.splitlines())
            asset_info.metadata['char_count'] = len(content)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating script {asset_info.name}: {e}")
            return False
    
    def _validate_material(self, asset_info: AssetInfo) -> bool:
        """Validate a material asset.
        
        Args:
            asset_info: Material asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            import json
            
            # Read material data
            with open(asset_info.file_path, 'r') as f:
                material_data = json.load(f)
            
            # Check required fields
            required_fields = ['name', 'type']
            for field in required_fields:
                if field not in material_data:
                    self.logger.error(f"Missing required field '{field}' in material {asset_info.name}")
                    return False
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['material_type'] = material_data.get('type')
            asset_info.metadata['has_shader'] = 'shader' in material_data
            asset_info.metadata['has_textures'] = 'textures' in material_data
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating material {asset_info.name}: {e}")
            return False
    
    def _validate_shader(self, asset_info: AssetInfo) -> bool:
        """Validate a shader asset.
        
        Args:
            asset_info: Shader asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Read shader source
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Basic shader validation
            if not source.strip():
                self.logger.error(f"Shader file is empty: {asset_info.name}")
                return False
            
            # Check for basic shader structure
            if 'main(' not in source:
                self.logger.warning(f"Shader may not have main function: {asset_info.name}")
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['line_count'] = len(source.splitlines())
            asset_info.metadata['char_count'] = len(source)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating shader {asset_info.name}: {e}")
            return False
    
    def convert_asset_format(self, asset_info: AssetInfo) -> bool:
        """Convert asset format if needed.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if converted successfully, False otherwise
        """
        try:
            if asset_info.type == AssetType.TEXTURE:
                return self._convert_texture_format(asset_info)
            elif asset_info.type == AssetType.AUDIO:
                return self._convert_audio_format(asset_info)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting asset format {asset_info.name}: {e}")
            return False
    
    def _convert_texture_format(self, asset_info: AssetInfo) -> bool:
        """Convert texture format.
        
        Args:
            asset_info: Texture asset information
            
        Returns:
            True if converted successfully, False otherwise
        """
        try:
            from PIL import Image
            
            # Load original image
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
                
                # Save in optimized format
                converted_path = f"assets/processed/{asset_info.name}_converted.png"
                img.save(converted_path, "PNG", optimize=True)
                
                # Update asset info
                asset_info.metadata = asset_info.metadata or {}
                asset_info.metadata['converted_path'] = converted_path
                asset_info.metadata['original_format'] = Path(asset_info.file_path).suffix
                asset_info.metadata['converted_format'] = '.png'
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting texture format {asset_info.name}: {e}")
            return False
    
    def _convert_audio_format(self, asset_info: AssetInfo) -> bool:
        """Convert audio format.
        
        Args:
            asset_info: Audio asset information
            
        Returns:
            True if converted successfully, False otherwise
        """
        try:
            # TODO: Implement actual audio format conversion
            # This would involve:
            # - Converting to OGG Vorbis for better compression
            # - Normalizing audio levels
            # - Resampling if needed
            
            # For now, just mark as converted
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['converted'] = True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting audio format {asset_info.name}: {e}")
            return False
    
    def preprocess_asset(self, asset_info: AssetInfo) -> bool:
        """Preprocess an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if preprocessed successfully, False otherwise
        """
        try:
            if asset_info.type == AssetType.TEXTURE:
                return self._preprocess_texture(asset_info)
            elif asset_info.type == AssetType.MESH:
                return self._preprocess_mesh(asset_info)
            elif asset_info.type == AssetType.SCRIPT:
                return self._preprocess_script(asset_info)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error preprocessing asset {asset_info.name}: {e}")
            return False
    
    def _preprocess_texture(self, asset_info: AssetInfo) -> bool:
        """Preprocess a texture asset.
        
        Args:
            asset_info: Texture asset information
            
        Returns:
            True if preprocessed successfully, False otherwise
        """
        try:
            from PIL import Image
            
            # Load original image
            with Image.open(asset_info.file_path) as img:
                # Generate mipmaps
                mipmaps = self._generate_mipmaps(img)
                
                # Save mipmaps
                mipmap_paths = []
                for i, mipmap in enumerate(mipmaps):
                    mipmap_path = f"assets/processed/{asset_info.name}_mip_{i}.png"
                    mipmap.save(mipmap_path)
                    mipmap_paths.append(mipmap_path)
                
                # Update asset info
                asset_info.metadata = asset_info.metadata or {}
                asset_info.metadata['mipmaps'] = mipmap_paths
                asset_info.metadata['mipmap_count'] = len(mipmaps)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error preprocessing texture {asset_info.name}: {e}")
            return False
    
    def _generate_mipmaps(self, image):
        """Generate mipmaps for an image.
        
        Args:
            image: PIL Image object
            
        Returns:
            List of mipmap images
        """
        try:
            from PIL import Image
            
            mipmaps = [image]
            current = image
            
            while current.size[0] > 1 and current.size[1] > 1:
                new_size = (max(1, current.size[0] // 2), max(1, current.size[1] // 2))
                current = current.resize(new_size, Image.Resampling.LANCZOS)
                mipmaps.append(current)
            
            return mipmaps
            
        except Exception as e:
            self.logger.error(f"Error generating mipmaps: {e}")
            return [image]
    
    def _preprocess_mesh(self, asset_info: AssetInfo) -> bool:
        """Preprocess a mesh asset.
        
        Args:
            asset_info: Mesh asset information
            
        Returns:
            True if preprocessed successfully, False otherwise
        """
        try:
            # TODO: Implement actual mesh preprocessing
            # This would involve:
            # - Calculating normals
            # - Generating tangents
            # - Optimizing vertex order
            # - Creating LODs
            
            # For now, just mark as preprocessed
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['preprocessed'] = True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error preprocessing mesh {asset_info.name}: {e}")
            return False
    
    def _preprocess_script(self, asset_info: AssetInfo) -> bool:
        """Preprocess a script asset.
        
        Args:
            asset_info: Script asset information
            
        Returns:
            True if preprocessed successfully, False otherwise
        """
        try:
            # Read script content
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic preprocessing
            processed_content = self._preprocess_script_content(content)
            
            # Save processed script
            processed_path = f"assets/processed/{asset_info.name}_processed.py"
            with open(processed_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            # Update asset info
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['processed_path'] = processed_path
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error preprocessing script {asset_info.name}: {e}")
            return False
    
    def _preprocess_script_content(self, content: str) -> str:
        """Preprocess script content.
        
        Args:
            content: Original script content
            
        Returns:
            Preprocessed script content
        """
        try:
            # Basic preprocessing
            lines = content.splitlines()
            processed_lines = []
            
            for line in lines:
                # Remove comments (basic)
                if line.strip().startswith('#'):
                    continue
                
                # Remove empty lines
                if not line.strip():
                    continue
                
                processed_lines.append(line)
            
            return '\n'.join(processed_lines)
            
        except Exception as e:
            self.logger.error(f"Error preprocessing script content: {e}")
            return content
    
    def get_asset_hash(self, asset_info: AssetInfo) -> str:
        """Get hash of an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            Asset hash string
        """
        try:
            hash_md5 = hashlib.md5()
            with open(asset_info.file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Error getting asset hash {asset_info.name}: {e}")
            return ""
    
    def get_stats(self) -> Dict[str, Any]:
        """Get asset processor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "assets_processed": self.assets_processed,
            "processing_time": self.processing_time,
            "validation_errors": self.validation_errors,
            "validation_enabled": self.enable_validation,
            "format_conversion_enabled": self.enable_format_conversion,
            "preprocessing_enabled": self.enable_preprocessing
        }
    
    def shutdown(self):
        """Shutdown the asset processor."""
        if self.is_initialized:
            self.logger.info("Shutting down asset processor...")
            
            self.is_initialized = False
            self.logger.info("✅ Asset processor shutdown complete")
