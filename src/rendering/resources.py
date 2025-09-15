"""
Resource Manager for Nexlify Engine.

This module handles loading, caching, and management of GPU resources
including textures, meshes, and other assets.
"""

import os
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
import numpy as np

from .device import GraphicsDevice
from ..utils.logger import get_logger


@dataclass
class TextureInfo:
    """Texture information."""
    width: int
    height: int
    format: str
    mip_levels: int
    handle: int


@dataclass
class MeshInfo:
    """Mesh information."""
    vertex_count: int
    index_count: int
    vertex_buffer: int
    index_buffer: int
    material_count: int


class ResourceManager:
    """Manages GPU resources and asset loading."""
    
    def __init__(self, device: GraphicsDevice):
        self.device = device
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Resource caches
        self.textures: Dict[str, TextureInfo] = {}
        self.meshes: Dict[str, MeshInfo] = {}
        self.materials: Dict[str, Dict[str, Any]] = {}
        
        # Asset paths
        self.asset_paths: List[str] = [
            "assets/textures",
            "assets/meshes", 
            "assets/materials",
            "assets/shaders"
        ]
        
    def initialize(self) -> bool:
        """Initialize the resource manager.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing resource manager...")
            
            # Create asset directories if they don't exist
            for path in self.asset_paths:
                Path(path).mkdir(parents=True, exist_ok=True)
            
            # Load default resources
            self._load_default_resources()
            
            self.is_initialized = True
            self.logger.info("✅ Resource manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resource manager: {e}", exc_info=True)
            return False
    
    def _load_default_resources(self):
        """Load default resources."""
        try:
            # Create default white texture
            self._create_default_texture()
            
            # Create default cube mesh
            self._create_default_cube()
            
            # Create default sphere mesh
            self._create_default_sphere()
            
            self.logger.info("Default resources loaded")
            
        except Exception as e:
            self.logger.error(f"Failed to load default resources: {e}")
    
    def _create_default_texture(self):
        """Create a default white texture."""
        try:
            # Create 1x1 white texture
            white_data = np.array([255, 255, 255, 255], dtype=np.uint8)
            texture_handle = self.device.create_texture(1, 1, "RGBA8", white_data.tobytes())
            
            self.textures["default_white"] = TextureInfo(
                width=1,
                height=1,
                format="RGBA8",
                mip_levels=1,
                handle=texture_handle
            )
            
            self.logger.debug("Created default white texture")
            
        except Exception as e:
            self.logger.error(f"Failed to create default texture: {e}")
    
    def _create_default_cube(self):
        """Create a default cube mesh."""
        try:
            # Define cube vertices (position + normal + UV)
            vertices = np.array([
                # Front face
                -1.0, -1.0,  1.0,  0.0,  0.0,  1.0,  0.0, 0.0,
                 1.0, -1.0,  1.0,  0.0,  0.0,  1.0,  1.0, 0.0,
                 1.0,  1.0,  1.0,  0.0,  0.0,  1.0,  1.0, 1.0,
                -1.0,  1.0,  1.0,  0.0,  0.0,  1.0,  0.0, 1.0,
                
                # Back face
                -1.0, -1.0, -1.0,  0.0,  0.0, -1.0,  1.0, 0.0,
                -1.0,  1.0, -1.0,  0.0,  0.0, -1.0,  1.0, 1.0,
                 1.0,  1.0, -1.0,  0.0,  0.0, -1.0,  0.0, 1.0,
                 1.0, -1.0, -1.0,  0.0,  0.0, -1.0,  0.0, 0.0,
                
                # Top face
                -1.0,  1.0, -1.0,  0.0,  1.0,  0.0,  0.0, 1.0,
                -1.0,  1.0,  1.0,  0.0,  1.0,  0.0,  0.0, 0.0,
                 1.0,  1.0,  1.0,  0.0,  1.0,  0.0,  1.0, 0.0,
                 1.0,  1.0, -1.0,  0.0,  1.0,  0.0,  1.0, 1.0,
                
                # Bottom face
                -1.0, -1.0, -1.0,  0.0, -1.0,  0.0,  1.0, 1.0,
                 1.0, -1.0, -1.0,  0.0, -1.0,  0.0,  0.0, 1.0,
                 1.0, -1.0,  1.0,  0.0, -1.0,  0.0,  0.0, 0.0,
                -1.0, -1.0,  1.0,  0.0, -1.0,  0.0,  1.0, 0.0,
                
                # Right face
                 1.0, -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 0.0,
                 1.0,  1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 1.0,
                 1.0,  1.0,  1.0,  1.0,  0.0,  0.0,  0.0, 1.0,
                 1.0, -1.0,  1.0,  1.0,  0.0,  0.0,  0.0, 0.0,
                
                # Left face
                -1.0, -1.0, -1.0, -1.0,  0.0,  0.0,  0.0, 0.0,
                -1.0, -1.0,  1.0, -1.0,  0.0,  0.0,  1.0, 0.0,
                -1.0,  1.0,  1.0, -1.0,  0.0,  0.0,  1.0, 1.0,
                -1.0,  1.0, -1.0, -1.0,  0.0,  0.0,  0.0, 1.0,
            ], dtype=np.float32)
            
            # Define cube indices
            indices = np.array([
                0,  1,  2,   0,  2,  3,   # front
                4,  5,  6,   4,  6,  7,   # back
                8,  9, 10,   8, 10, 11,   # top
                12, 13, 14,  12, 14, 15,  # bottom
                16, 17, 18,  16, 18, 19,  # right
                20, 21, 22,  20, 22, 23,  # left
            ], dtype=np.uint32)
            
            # Create GPU buffers
            vertex_buffer = self.device.create_buffer(
                vertices.nbytes, "vertex", vertices.tobytes()
            )
            index_buffer = self.device.create_buffer(
                indices.nbytes, "index", indices.tobytes()
            )
            
            self.meshes["default_cube"] = MeshInfo(
                vertex_count=24,
                index_count=36,
                vertex_buffer=vertex_buffer,
                index_buffer=index_buffer,
                material_count=1
            )
            
            self.logger.debug("Created default cube mesh")
            
        except Exception as e:
            self.logger.error(f"Failed to create default cube: {e}")
    
    def _create_default_sphere(self):
        """Create a default sphere mesh."""
        try:
            # Generate sphere vertices and indices
            segments = 32
            rings = 16
            
            vertices = []
            indices = []
            
            # Generate vertices
            for ring in range(rings + 1):
                v = ring / rings
                phi = v * np.pi
                
                for segment in range(segments + 1):
                    u = segment / segments
                    theta = u * 2.0 * np.pi
                    
                    x = np.cos(theta) * np.sin(phi)
                    y = np.cos(phi)
                    z = np.sin(theta) * np.sin(phi)
                    
                    # Position
                    vertices.extend([x, y, z])
                    # Normal (same as position for unit sphere)
                    vertices.extend([x, y, z])
                    # UV
                    vertices.extend([u, v])
            
            # Generate indices
            for ring in range(rings):
                for segment in range(segments):
                    current = ring * (segments + 1) + segment
                    next_ring = current + segments + 1
                    
                    indices.extend([
                        current, next_ring, current + 1,
                        current + 1, next_ring, next_ring + 1
                    ])
            
            vertices_array = np.array(vertices, dtype=np.float32)
            indices_array = np.array(indices, dtype=np.uint32)
            
            # Create GPU buffers
            vertex_buffer = self.device.create_buffer(
                vertices_array.nbytes, "vertex", vertices_array.tobytes()
            )
            index_buffer = self.device.create_buffer(
                indices_array.nbytes, "index", indices_array.tobytes()
            )
            
            self.meshes["default_sphere"] = MeshInfo(
                vertex_count=len(vertices) // 8,  # 8 floats per vertex
                index_count=len(indices),
                vertex_buffer=vertex_buffer,
                index_buffer=index_buffer,
                material_count=1
            )
            
            self.logger.debug("Created default sphere mesh")
            
        except Exception as e:
            self.logger.error(f"Failed to create default sphere: {e}")
    
    def load_texture(self, name: str, path: str) -> bool:
        """Load a texture from file.
        
        Args:
            name: Texture name
            path: Path to texture file
            
        Returns:
            True if texture loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(path):
                self.logger.error(f"Texture file not found: {path}")
                return False
            
            # Load image using PIL
            image = Image.open(path)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            width, height = image.size
            data = np.array(image, dtype=np.uint8)
            
            # Create GPU texture
            texture_handle = self.device.create_texture(
                width, height, "RGBA8", data.tobytes()
            )
            
            self.textures[name] = TextureInfo(
                width=width,
                height=height,
                format="RGBA8",
                mip_levels=1,  # TODO: Generate mipmaps
                handle=texture_handle
            )
            
            self.logger.info(f"Loaded texture: {name} ({width}x{height})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load texture {name}: {e}")
            return False
    
    def load_mesh(self, name: str, path: str) -> bool:
        """Load a mesh from file.
        
        Args:
            name: Mesh name
            path: Path to mesh file
            
        Returns:
            True if mesh loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(path):
                self.logger.error(f"Mesh file not found: {path}")
                return False
            
            # TODO: Implement actual mesh loading
            # This would involve:
            # - Loading .obj, .fbx, .gltf files
            # - Parsing vertex data
            # - Creating GPU buffers
            
            self.logger.warning(f"Mesh loading not implemented yet: {path}")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to load mesh {name}: {e}")
            return False
    
    def get_texture(self, name: str) -> Optional[TextureInfo]:
        """Get a texture by name.
        
        Args:
            name: Texture name
            
        Returns:
            Texture info or None if not found
        """
        return self.textures.get(name)
    
    def get_mesh(self, name: str) -> Optional[MeshInfo]:
        """Get a mesh by name.
        
        Args:
            name: Mesh name
            
        Returns:
            Mesh info or None if not found
        """
        return self.meshes.get(name)
    
    def get_material(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a material by name.
        
        Args:
            name: Material name
            
        Returns:
            Material data or None if not found
        """
        return self.materials.get(name)
    
    def create_material(self, name: str, properties: Dict[str, Any]) -> bool:
        """Create a material.
        
        Args:
            name: Material name
            properties: Material properties
            
        Returns:
            True if material created successfully, False otherwise
        """
        try:
            self.materials[name] = properties.copy()
            self.logger.info(f"Created material: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create material {name}: {e}")
            return False
    
    def get_resource_count(self) -> Dict[str, int]:
        """Get resource counts.
        
        Returns:
            Dictionary of resource counts
        """
        return {
            "textures": len(self.textures),
            "meshes": len(self.meshes),
            "materials": len(self.materials)
        }
    
    def clear_cache(self):
        """Clear all cached resources."""
        self.textures.clear()
        self.meshes.clear()
        self.materials.clear()
        self.logger.info("Resource cache cleared")
    
    def shutdown(self):
        """Shutdown the resource manager."""
        if self.is_initialized:
            self.logger.info("Shutting down resource manager...")
            
            # Clear all resources
            self.clear_cache()
            
            self.is_initialized = False
            self.logger.info("✅ Resource manager shutdown complete")