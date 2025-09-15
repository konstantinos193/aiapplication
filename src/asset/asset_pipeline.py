"""
Asset Pipeline for Nexlify Engine.

This module provides the core asset pipeline functionality including
asset information, lifecycle management, and processing stages.
"""

import logging
import os
import time
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

from ..utils.logger import get_logger


class AssetType(Enum):
    """Asset type enumeration."""
    TEXTURE = "texture"
    MESH = "mesh"
    AUDIO = "audio"
    SCRIPT = "script"
    MATERIAL = "material"
    SHADER = "shader"
    FONT = "font"
    ANIMATION = "animation"
    SCENE = "scene"
    PREFAB = "prefab"


class AssetStatus(Enum):
    """Asset status enumeration."""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    OPTIMIZING = "optimizing"
    OPTIMIZED = "optimized"
    ERROR = "error"


@dataclass
class AssetInfo:
    """Asset information container."""
    name: str
    file_path: str
    type: AssetType
    size: int = 0
    status: AssetStatus = AssetStatus.UNLOADED
    metadata: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)
    imported: bool = False
    processed: bool = False
    optimized: bool = False
    compressed: bool = False
    created_at: float = field(default_factory=time.time)
    modified_at: float = field(default_factory=time.time)
    accessed_at: float = field(default_factory=time.time)
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class AssetPipeline:
    """Asset pipeline system."""
    
    def __init__(self, ai_manager=None):
        self.ai_manager = ai_manager
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Pipeline stages
        self.stages = [
            "import",
            "validate",
            "process",
            "optimize",
            "compress",
            "cache"
        ]
        
        # Asset storage
        self.assets: Dict[str, AssetInfo] = {}
        self.asset_queue: List[AssetInfo] = []
        self.processing_queue: List[AssetInfo] = []
        
        # Pipeline settings
        self.enable_validation = True
        self.enable_processing = True
        self.enable_optimization = True
        self.enable_compression = True
        self.enable_caching = True
        self.enable_ai_optimization = True
        
        # Performance tracking
        self.assets_processed = 0
        self.processing_time = 0.0
        self.pipeline_errors = 0
        
    def initialize(self) -> bool:
        """Initialize the asset pipeline.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing asset pipeline...")
            
            # Create pipeline directories
            Path("assets/pipeline").mkdir(parents=True, exist_ok=True)
            Path("assets/staging").mkdir(parents=True, exist_ok=True)
            Path("assets/processed").mkdir(parents=True, exist_ok=True)
            Path("assets/optimized").mkdir(parents=True, exist_ok=True)
            Path("assets/compressed").mkdir(parents=True, exist_ok=True)
            Path("assets/cache").mkdir(parents=True, exist_ok=True)
            
            self.is_initialized = True
            self.logger.info("✅ Asset pipeline initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize asset pipeline: {e}")
            return False
    
    def add_asset(self, asset_info: AssetInfo) -> bool:
        """Add an asset to the pipeline.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if added successfully, False otherwise
        """
        if not self.is_initialized:
            return False
        
        try:
            # Validate asset info
            if not self._validate_asset_info(asset_info):
                return False
            
            # Add to asset storage
            self.assets[asset_info.name] = asset_info
            
            # Add to processing queue
            self.asset_queue.append(asset_info)
            
            self.logger.info(f"Added asset to pipeline: {asset_info.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding asset to pipeline {asset_info.name}: {e}")
            return False
    
    def process_asset(self, asset_info: AssetInfo) -> bool:
        """Process an asset through the pipeline.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if processed successfully, False otherwise
        """
        if not self.is_initialized:
            return False
        
        try:
            start_time = time.time()
            
            # Update status
            asset_info.status = AssetStatus.PROCESSING
            
            # Process through each stage
            for stage in self.stages:
                if not self._process_stage(asset_info, stage):
                    asset_info.status = AssetStatus.ERROR
                    self.pipeline_errors += 1
                    return False
            
            # Update status
            asset_info.status = AssetStatus.PROCESSED
            asset_info.processed = True
            
            # Update statistics
            self.assets_processed += 1
            self.processing_time += time.time() - start_time
            
            self.logger.info(f"Processed asset through pipeline: {asset_info.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing asset {asset_info.name}: {e}")
            asset_info.status = AssetStatus.ERROR
            self.pipeline_errors += 1
            return False
    
    def _process_stage(self, asset_info: AssetInfo, stage: str) -> bool:
        """Process an asset through a specific stage.
        
        Args:
            asset_info: Asset information
            stage: Pipeline stage name
            
        Returns:
            True if stage processed successfully, False otherwise
        """
        try:
            if stage == "import":
                return self._import_stage(asset_info)
            elif stage == "validate":
                return self._validate_stage(asset_info)
            elif stage == "process":
                return self._process_stage_impl(asset_info)
            elif stage == "optimize":
                return self._optimize_stage(asset_info)
            elif stage == "compress":
                return self._compress_stage(asset_info)
            elif stage == "cache":
                return self._cache_stage(asset_info)
            else:
                self.logger.warning(f"Unknown pipeline stage: {stage}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error processing stage {stage} for asset {asset_info.name}: {e}")
            return False
    
    def _import_stage(self, asset_info: AssetInfo) -> bool:
        """Import stage processing.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if import successful, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(asset_info.file_path):
                self.logger.error(f"Asset file not found: {asset_info.file_path}")
                return False
            
            # Update file size
            asset_info.size = os.path.getsize(asset_info.file_path)
            
            # Mark as imported
            asset_info.imported = True
            
            self.logger.debug(f"Imported asset: {asset_info.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in import stage for asset {asset_info.name}: {e}")
            return False
    
    def _validate_stage(self, asset_info: AssetInfo) -> bool:
        """Validation stage processing.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if validation successful, False otherwise
        """
        if not self.enable_validation:
            return True
        
        try:
            # Basic validation
            if asset_info.size == 0:
                self.logger.error(f"Asset file is empty: {asset_info.name}")
                return False
            
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
            self.logger.error(f"Error in validation stage for asset {asset_info.name}: {e}")
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
                
                # Update metadata
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
            # Check file size
            if asset_info.size > 100 * 1024 * 1024:  # 100MB
                self.logger.warning(f"Mesh file is very large: {asset_info.size} bytes")
            
            # Try to read file header
            with open(asset_info.file_path, 'rb') as f:
                header = f.read(1024)
                if len(header) == 0:
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
            # Check file size
            if asset_info.size > 50 * 1024 * 1024:  # 50MB
                self.logger.warning(f"Audio file is very large: {asset_info.size} bytes")
            
            # Try to read file header
            with open(asset_info.file_path, 'rb') as f:
                header = f.read(1024)
                if len(header) == 0:
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
            
            # Basic syntax validation for Python
            if asset_info.file_path.endswith('.py'):
                try:
                    compile(content, asset_info.file_path, 'exec')
                except SyntaxError as e:
                    self.logger.error(f"Syntax error in script {asset_info.name}: {e}")
                    return False
            
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
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating shader {asset_info.name}: {e}")
            return False
    
    def _process_stage_impl(self, asset_info: AssetInfo) -> bool:
        """Processing stage implementation.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if processing successful, False otherwise
        """
        if not self.enable_processing:
            return True
        
        try:
            # Type-specific processing
            if asset_info.type == AssetType.TEXTURE:
                return self._process_texture(asset_info)
            elif asset_info.type == AssetType.MESH:
                return self._process_mesh(asset_info)
            elif asset_info.type == AssetType.AUDIO:
                return self._process_audio(asset_info)
            elif asset_info.type == AssetType.SCRIPT:
                return self._process_script(asset_info)
            elif asset_info.type == AssetType.MATERIAL:
                return self._process_material(asset_info)
            elif asset_info.type == AssetType.SHADER:
                return self._process_shader(asset_info)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in processing stage for asset {asset_info.name}: {e}")
            return False
    
    def _process_texture(self, asset_info: AssetInfo) -> bool:
        """Process a texture asset.
        
        Args:
            asset_info: Texture asset information
            
        Returns:
            True if processing successful, False otherwise
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
                
                # Update metadata
                asset_info.metadata['mipmaps'] = mipmap_paths
                asset_info.metadata['mipmap_count'] = len(mipmaps)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing texture {asset_info.name}: {e}")
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
    
    def _process_mesh(self, asset_info: AssetInfo) -> bool:
        """Process a mesh asset.
        
        Args:
            asset_info: Mesh asset information
            
        Returns:
            True if processing successful, False otherwise
        """
        try:
            # TODO: Implement actual mesh processing
            # This would involve:
            # - Calculating normals
            # - Generating tangents
            # - Optimizing vertex order
            # - Creating LODs
            
            # For now, just mark as processed
            asset_info.metadata['processed'] = True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing mesh {asset_info.name}: {e}")
            return False
    
    def _process_audio(self, asset_info: AssetInfo) -> bool:
        """Process an audio asset.
        
        Args:
            asset_info: Audio asset information
            
        Returns:
            True if processing successful, False otherwise
        """
        try:
            # TODO: Implement actual audio processing
            # This would involve:
            # - Audio normalization
            # - Format conversion
            # - Compression
            
            # For now, just mark as processed
            asset_info.metadata['processed'] = True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing audio {asset_info.name}: {e}")
            return False
    
    def _process_script(self, asset_info: AssetInfo) -> bool:
        """Process a script asset.
        
        Args:
            asset_info: Script asset information
            
        Returns:
            True if processing successful, False otherwise
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
            
            # Update metadata
            asset_info.metadata['processed_path'] = processed_path
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing script {asset_info.name}: {e}")
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
    
    def _process_material(self, asset_info: AssetInfo) -> bool:
        """Process a material asset.
        
        Args:
            asset_info: Material asset information
            
        Returns:
            True if processing successful, False otherwise
        """
        try:
            import json
            
            # Read material data
            with open(asset_info.file_path, 'r') as f:
                material_data = json.load(f)
            
            # Process material data
            processed_data = self._process_material_data(material_data)
            
            # Save processed material
            processed_path = f"assets/processed/{asset_info.name}_processed.json"
            with open(processed_path, 'w') as f:
                json.dump(processed_data, f, separators=(',', ':'))
            
            # Update metadata
            asset_info.metadata['processed_path'] = processed_path
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing material {asset_info.name}: {e}")
            return False
    
    def _process_material_data(self, material_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process material data.
        
        Args:
            material_data: Original material data
            
        Returns:
            Processed material data
        """
        try:
            # Remove unnecessary properties
            processed_data = {}
            
            # Keep essential properties
            essential_props = ['name', 'type', 'properties', 'shader', 'textures']
            for prop in essential_props:
                if prop in material_data:
                    processed_data[prop] = material_data[prop]
            
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error processing material data: {e}")
            return material_data
    
    def _process_shader(self, asset_info: AssetInfo) -> bool:
        """Process a shader asset.
        
        Args:
            asset_info: Shader asset information
            
        Returns:
            True if processing successful, False otherwise
        """
        try:
            # Read shader source
            with open(asset_info.file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Process shader source
            processed_source = self._process_shader_source(source)
            
            # Save processed shader
            processed_path = f"assets/processed/{asset_info.name}_processed.glsl"
            with open(processed_path, 'w', encoding='utf-8') as f:
                f.write(processed_source)
            
            # Update metadata
            asset_info.metadata['processed_path'] = processed_path
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing shader {asset_info.name}: {e}")
            return False
    
    def _process_shader_source(self, source: str) -> str:
        """Process shader source code.
        
        Args:
            source: Original shader source
            
        Returns:
            Processed shader source
        """
        try:
            lines = source.splitlines()
            processed_lines = []
            
            for line in lines:
                # Remove trailing whitespace
                line = line.rstrip()
                
                # Skip empty lines at the beginning
                if not processed_lines and not line:
                    continue
                
                processed_lines.append(line)
            
            # Remove trailing empty lines
            while processed_lines and not processed_lines[-1]:
                processed_lines.pop()
            
            return '\n'.join(processed_lines)
            
        except Exception as e:
            self.logger.error(f"Error processing shader source: {e}")
            return source
    
    def _optimize_stage(self, asset_info: AssetInfo) -> bool:
        """Optimization stage processing.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if optimization successful, False otherwise
        """
        if not self.enable_optimization:
            return True
        
        try:
            # Type-specific optimization
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
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in optimization stage for asset {asset_info.name}: {e}")
            return False
    
    def _optimize_texture(self, asset_info: AssetInfo) -> bool:
        """Optimize a texture asset.
        
        Args:
            asset_info: Texture asset information
            
        Returns:
            True if optimization successful, False otherwise
        """
        try:
            from PIL import Image
            
            # Load original image
            with Image.open(asset_info.file_path) as img:
                # Optimize image
                optimized_img = self._optimize_image(img)
                
                # Save optimized image
                optimized_path = f"assets/optimized/{asset_info.name}_optimized.png"
                optimized_img.save(optimized_path, "PNG", optimize=True, quality=85)
                
                # Update metadata
                asset_info.metadata['optimized_path'] = optimized_path
                asset_info.optimized = True
            
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
            
            # Convert to RGB if necessary
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
            True if optimization successful, False otherwise
        """
        try:
            # TODO: Implement actual mesh optimization
            # This would involve:
            # - Vertex optimization
            # - Triangle reduction
            # - UV optimization
            # - Normal recalculation
            
            # For now, just mark as optimized
            asset_info.optimized = True
            asset_info.metadata['optimization_applied'] = 'placeholder'
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing mesh {asset_info.name}: {e}")
            return False
    
    def _optimize_audio(self, asset_info: AssetInfo) -> bool:
        """Optimize an audio asset.
        
        Args:
            asset_info: Audio asset information
            
        Returns:
            True if optimization successful, False otherwise
        """
        try:
            # TODO: Implement actual audio optimization
            # This would involve:
            # - Audio compression
            # - Format conversion
            # - Quality optimization
            
            # For now, just mark as optimized
            asset_info.optimized = True
            asset_info.metadata['optimization_applied'] = 'placeholder'
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing audio {asset_info.name}: {e}")
            return False
    
    def _optimize_script(self, asset_info: AssetInfo) -> bool:
        """Optimize a script asset.
        
        Args:
            asset_info: Script asset information
            
        Returns:
            True if optimization successful, False otherwise
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
            
            # Update metadata
            asset_info.metadata['optimized_path'] = optimized_path
            asset_info.optimized = True
            
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
            True if optimization successful, False otherwise
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
            
            # Update metadata
            asset_info.metadata['optimized_path'] = optimized_path
            asset_info.optimized = True
            
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
            True if optimization successful, False otherwise
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
            
            # Update metadata
            asset_info.metadata['optimized_path'] = optimized_path
            asset_info.optimized = True
            
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
    
    def _compress_stage(self, asset_info: AssetInfo) -> bool:
        """Compression stage processing.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if compression successful, False otherwise
        """
        if not self.enable_compression:
            return True
        
        try:
            # Compress the asset
            return self._compress_asset(asset_info)
            
        except Exception as e:
            self.logger.error(f"Error in compression stage for asset {asset_info.name}: {e}")
            return False
    
    def _compress_asset(self, asset_info: AssetInfo) -> bool:
        """Compress an asset.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if compression successful, False otherwise
        """
        try:
            import gzip
            import shutil
            
            # Compress the asset file
            compressed_path = f"assets/compressed/{asset_info.name}.gz"
            
            with open(asset_info.file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Update metadata
            asset_info.metadata['compressed_path'] = compressed_path
            asset_info.compressed = True
            
            # Get compression ratio
            original_size = asset_info.size
            compressed_size = os.path.getsize(compressed_path)
            compression_ratio = compressed_size / original_size
            
            asset_info.metadata['compression_ratio'] = compression_ratio
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error compressing asset {asset_info.name}: {e}")
            return False
    
    def _cache_stage(self, asset_info: AssetInfo) -> bool:
        """Caching stage processing.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if caching successful, False otherwise
        """
        if not self.enable_caching:
            return True
        
        try:
            # TODO: Implement actual caching
            # This would involve:
            # - Adding to cache
            # - Setting cache policies
            # - Managing cache size
            
            # For now, just mark as cached
            asset_info.metadata['cached'] = True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in caching stage for asset {asset_info.name}: {e}")
            return False
    
    def _validate_asset_info(self, asset_info: AssetInfo) -> bool:
        """Validate asset information.
        
        Args:
            asset_info: Asset information
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check required fields
            if not asset_info.name:
                self.logger.error("Asset name is required")
                return False
            
            if not asset_info.file_path:
                self.logger.error("Asset file path is required")
                return False
            
            if not asset_info.type:
                self.logger.error("Asset type is required")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating asset info: {e}")
            return False
    
    def get_asset(self, name: str) -> Optional[AssetInfo]:
        """Get an asset by name.
        
        Args:
            name: Asset name
            
        Returns:
            AssetInfo object or None if not found
        """
        try:
            return self.assets.get(name)
            
        except Exception as e:
            self.logger.error(f"Error getting asset {name}: {e}")
            return None
    
    def get_all_assets(self) -> List[AssetInfo]:
        """Get all assets.
        
        Returns:
            List of all AssetInfo objects
        """
        try:
            return list(self.assets.values())
            
        except Exception as e:
            self.logger.error(f"Error getting all assets: {e}")
            return []
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[AssetInfo]:
        """Get assets by type.
        
        Args:
            asset_type: Asset type
            
        Returns:
            List of AssetInfo objects of the specified type
        """
        try:
            return [asset_info for asset_info in self.assets.values() 
                   if asset_info.type == asset_type]
            
        except Exception as e:
            self.logger.error(f"Error getting assets by type {asset_type}: {e}")
            return []
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics.
        
        Returns:
            Dictionary of pipeline statistics
        """
        try:
            return {
                "total_assets": len(self.assets),
                "assets_processed": self.assets_processed,
                "processing_time": self.processing_time,
                "pipeline_errors": self.pipeline_errors,
                "queue_size": len(self.asset_queue),
                "processing_queue_size": len(self.processing_queue),
                "validation_enabled": self.enable_validation,
                "processing_enabled": self.enable_processing,
                "optimization_enabled": self.enable_optimization,
                "compression_enabled": self.enable_compression,
                "caching_enabled": self.enable_caching,
                "ai_optimization_enabled": self.enable_ai_optimization
            }
            
        except Exception as e:
            self.logger.error(f"Error getting pipeline stats: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown the asset pipeline."""
        if self.is_initialized:
            self.logger.info("Shutting down asset pipeline...")
            
            # Clear queues
            self.asset_queue.clear()
            self.processing_queue.clear()
            
            # Clear assets
            self.assets.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Asset pipeline shutdown complete")