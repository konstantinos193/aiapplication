"""
Asset Importer for Nexlify Engine.

This module provides asset importing functionality including
format detection, validation, and conversion.
"""

import logging
import os
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import mimetypes

from .asset_pipeline import AssetInfo, AssetType
from ..utils.logger import get_logger


class AssetImporter:
    """Asset importing system."""
    
    def __init__(self, ai_manager=None):
        self.ai_manager = ai_manager
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Import settings
        self.enable_auto_detection = True
        self.enable_validation = True
        self.enable_conversion = True
        
        # Supported formats
        self.supported_formats = {
            AssetType.TEXTURE: ['.png', '.jpg', '.jpeg', '.bmp', '.tga', '.dds', '.hdr', '.exr'],
            AssetType.MESH: ['.obj', '.fbx', '.dae', '.gltf', '.glb', '.3ds', '.blend', '.max'],
            AssetType.AUDIO: ['.wav', '.mp3', '.ogg', '.flac', '.aac', '.m4a'],
            AssetType.SCRIPT: ['.py', '.lua', '.js'],
            AssetType.MATERIAL: ['.json', '.mat', '.mtl'],
            AssetType.SHADER: ['.glsl', '.hlsl', '.vert', '.frag', '.comp', '.geom', '.tesc', '.tese']
        }
        
        # File type detection
        self.mime_type_map = {
            'image/png': AssetType.TEXTURE,
            'image/jpeg': AssetType.TEXTURE,
            'image/bmp': AssetType.TEXTURE,
            'image/targa': AssetType.TEXTURE,
            'image/vnd.ms-dds': AssetType.TEXTURE,
            'image/vnd.radiance': AssetType.TEXTURE,
            'image/x-exr': AssetType.TEXTURE,
            'audio/wav': AssetType.AUDIO,
            'audio/mpeg': AssetType.AUDIO,
            'audio/ogg': AssetType.AUDIO,
            'audio/flac': AssetType.AUDIO,
            'audio/aac': AssetType.AUDIO,
            'text/x-python': AssetType.SCRIPT,
            'application/json': AssetType.MATERIAL,
            'text/plain': AssetType.SHADER
        }
        
        # Performance tracking
        self.assets_imported = 0
        self.import_errors = 0
        self.conversion_count = 0
        
    def initialize(self) -> bool:
        """Initialize the asset importer.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing asset importer...")
            
            # Create import directories
            Path("assets/imported").mkdir(parents=True, exist_ok=True)
            Path("assets/converted").mkdir(parents=True, exist_ok=True)
            
            self.is_initialized = True
            self.logger.info("✅ Asset importer initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize asset importer: {e}")
            return False
    
    def import_asset(self, file_path: str, target_type: Optional[AssetType] = None) -> Optional[AssetInfo]:
        """Import an asset from file.
        
        Args:
            file_path: Path to the asset file
            target_type: Target asset type (auto-detected if None)
            
        Returns:
            AssetInfo object or None if import failed
        """
        if not self.is_initialized:
            return None
        
        try:
            # Validate file path
            if not os.path.exists(file_path):
                self.logger.error(f"Asset file not found: {file_path}")
                self.import_errors += 1
                return None
            
            # Detect asset type
            if target_type is None:
                target_type = self.detect_asset_type(file_path)
                if target_type is None:
                    self.logger.error(f"Could not detect asset type: {file_path}")
                    self.import_errors += 1
                    return None
            
            # Create asset info
            asset_info = AssetInfo(
                name=Path(file_path).stem,
                file_path=file_path,
                type=target_type,
                size=os.path.getsize(file_path),
                imported=True
            )
            
            # Validate asset
            if self.enable_validation and not self.validate_asset(asset_info):
                self.import_errors += 1
                return None
            
            # Convert if needed
            if self.enable_conversion:
                self.convert_asset(asset_info)
            
            # Update metadata
            self._update_asset_metadata(asset_info)
            
            self.assets_imported += 1
            self.logger.info(f"Imported asset: {asset_info.name} ({asset_info.type})")
            return asset_info
            
        except Exception as e:
            self.logger.error(f"Error importing asset {file_path}: {e}")
            self.import_errors += 1
            return None
    
    def detect_asset_type(self, file_path: str) -> Optional[AssetType]:
        """Detect asset type from file path and content.
        
        Args:
            file_path: Path to the asset file
            
        Returns:
            Detected asset type or None if detection failed
        """
        try:
            # Get file extension
            file_ext = Path(file_path).suffix.lower()
            
            # Check extension-based detection
            for asset_type, extensions in self.supported_formats.items():
                if file_ext in extensions:
                    return asset_type
            
            # Try MIME type detection
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type in self.mime_type_map:
                return self.mime_type_map[mime_type]
            
            # Try content-based detection
            return self._detect_asset_type_by_content(file_path)
            
        except Exception as e:
            self.logger.error(f"Error detecting asset type for {file_path}: {e}")
            return None
    
    def _detect_asset_type_by_content(self, file_path: str) -> Optional[AssetType]:
        """Detect asset type by examining file content.
        
        Args:
            file_path: Path to the asset file
            
        Returns:
            Detected asset type or None if detection failed
        """
        try:
            # Read first few bytes
            with open(file_path, 'rb') as f:
                header = f.read(1024)
            
            # Check for common file signatures
            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                return AssetType.TEXTURE
            elif header.startswith(b'\xff\xd8\xff'):
                return AssetType.TEXTURE
            elif header.startswith(b'BM'):
                return AssetType.TEXTURE
            elif header.startswith(b'RIFF') and b'WAVE' in header:
                return AssetType.AUDIO
            elif header.startswith(b'ID3') or header.startswith(b'\xff\xfb'):
                return AssetType.AUDIO
            elif header.startswith(b'OggS'):
                return AssetType.AUDIO
            elif header.startswith(b'fLaC'):
                return AssetType.AUDIO
            elif header.startswith(b'#') and b'version' in header:
                return AssetType.SHADER
            elif header.startswith(b'{') or header.startswith(b'['):
                return AssetType.MATERIAL
            elif header.startswith(b'#') and b'python' in header.lower():
                return AssetType.SCRIPT
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error detecting asset type by content for {file_path}: {e}")
            return None
    
    def validate_asset(self, asset_info: AssetInfo) -> bool:
        """Validate an imported asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check file size
            if asset_info.size == 0:
                self.logger.error(f"Asset file is empty: {asset_info.name}")
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
                max_size = 16384
                if width > max_size or height > max_size:
                    self.logger.warning(f"Texture is very large: {width}x{height} (max: {max_size})")
                
                # Update metadata
                asset_info.metadata = asset_info.metadata or {}
                asset_info.metadata['width'] = width
                asset_info.metadata['height'] = height
                asset_info.metadata['format'] = img.format
                asset_info.metadata['mode'] = img.mode
                asset_info.metadata['has_alpha'] = img.mode in ('RGBA', 'LA', 'P')
            
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
            # Check file size (meshes should be reasonably sized)
            if asset_info.size > 100 * 1024 * 1024:  # 100MB
                self.logger.warning(f"Mesh file is very large: {asset_info.size} bytes")
            
            # Try to read file header
            with open(asset_info.file_path, 'rb') as f:
                header = f.read(1024)
                if len(header) == 0:
                    return False
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['file_size_mb'] = asset_info.size / (1024 * 1024)
            
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
            # Check file size
            if asset_info.size > 50 * 1024 * 1024:  # 50MB
                self.logger.warning(f"Audio file is very large: {asset_info.size} bytes")
            
            # Try to read file header
            with open(asset_info.file_path, 'rb') as f:
                header = f.read(1024)
                if len(header) == 0:
                    return False
            
            # Update metadata
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['file_size_mb'] = asset_info.size / (1024 * 1024)
            
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
            
            # Basic syntax validation for Python
            if asset_info.file_path.endswith('.py'):
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
            asset_info.metadata['property_count'] = len(material_data.get('properties', {}))
            
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
            asset_info.metadata['has_vertex'] = 'gl_Position' in source or 'SV_Position' in source
            asset_info.metadata['has_fragment'] = 'gl_FragColor' in source or 'SV_Target' in source
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating shader {asset_info.name}: {e}")
            return False
    
    def convert_asset(self, asset_info: AssetInfo) -> bool:
        """Convert asset to engine format if needed.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if converted successfully, False otherwise
        """
        try:
            if asset_info.type == AssetType.TEXTURE:
                return self._convert_texture(asset_info)
            elif asset_info.type == AssetType.AUDIO:
                return self._convert_audio(asset_info)
            elif asset_info.type == AssetType.MESH:
                return self._convert_mesh(asset_info)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting asset {asset_info.name}: {e}")
            return False
    
    def _convert_texture(self, asset_info: AssetInfo) -> bool:
        """Convert texture to engine format.
        
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
                
                # Save in engine format
                converted_path = f"assets/converted/{asset_info.name}_converted.png"
                img.save(converted_path, "PNG", optimize=True)
                
                # Update asset info
                asset_info.metadata = asset_info.metadata or {}
                asset_info.metadata['converted_path'] = converted_path
                asset_info.metadata['original_format'] = Path(asset_info.file_path).suffix
                asset_info.metadata['converted_format'] = '.png'
                
                self.conversion_count += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting texture {asset_info.name}: {e}")
            return False
    
    def _convert_audio(self, asset_info: AssetInfo) -> bool:
        """Convert audio to engine format.
        
        Args:
            asset_info: Audio asset information
            
        Returns:
            True if converted successfully, False otherwise
        """
        try:
            # TODO: Implement actual audio conversion
            # This would involve:
            # - Converting to OGG Vorbis for better compression
            # - Normalizing audio levels
            # - Resampling if needed
            
            # For now, just mark as converted
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['converted'] = True
            
            self.conversion_count += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting audio {asset_info.name}: {e}")
            return False
    
    def _convert_mesh(self, asset_info: AssetInfo) -> bool:
        """Convert mesh to engine format.
        
        Args:
            asset_info: Mesh asset information
            
        Returns:
            True if converted successfully, False otherwise
        """
        try:
            # TODO: Implement actual mesh conversion
            # This would involve:
            # - Converting to engine mesh format
            # - Optimizing vertex data
            # - Generating normals if missing
            
            # For now, just mark as converted
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['converted'] = True
            
            self.conversion_count += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting mesh {asset_info.name}: {e}")
            return False
    
    def _update_asset_metadata(self, asset_info: AssetInfo):
        """Update asset metadata with import information.
        
        Args:
            asset_info: Asset information
        """
        try:
            import time
            
            asset_info.metadata = asset_info.metadata or {}
            asset_info.metadata['imported_at'] = time.time()
            asset_info.metadata['import_version'] = '1.0'
            asset_info.metadata['file_extension'] = Path(asset_info.file_path).suffix
            
        except Exception as e:
            self.logger.error(f"Error updating asset metadata {asset_info.name}: {e}")
    
    def get_supported_formats(self) -> Dict[AssetType, List[str]]:
        """Get supported file formats for each asset type.
        
        Returns:
            Dictionary mapping asset types to supported extensions
        """
        return self.supported_formats.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get asset importer statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "assets_imported": self.assets_imported,
            "import_errors": self.import_errors,
            "conversion_count": self.conversion_count,
            "auto_detection_enabled": self.enable_auto_detection,
            "validation_enabled": self.enable_validation,
            "conversion_enabled": self.enable_conversion
        }
    
    def shutdown(self):
        """Shutdown the asset importer."""
        if self.is_initialized:
            self.logger.info("Shutting down asset importer...")
            
            self.is_initialized = False
            self.logger.info("✅ Asset importer shutdown complete")
