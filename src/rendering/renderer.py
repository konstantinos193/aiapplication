"""
Main Renderer class for Nexlify Engine.

This module provides the high-level rendering interface that coordinates
all rendering operations and manages the rendering pipeline.
"""

import time
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from .device import GraphicsDevice, GraphicsAPI
from .resources import ResourceManager
from .shaders import ShaderManager
from .pipeline import RenderPipeline
from .scene_renderer import SceneRenderer
from ..utils.logger import get_logger


@dataclass
class RenderStats:
    """Rendering performance statistics."""
    fps: float = 0.0
    frame_time: float = 0.0
    draw_calls: int = 0
    triangles: int = 0
    vertices: int = 0
    memory_used: int = 0
    memory_total: int = 0


class Renderer:
    """Main renderer class that coordinates all rendering operations."""
    
    def __init__(self, api: GraphicsAPI = GraphicsAPI.DIRECTX_12):
        self.api = api
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Core components
        self.device: Optional[GraphicsDevice] = None
        self.resource_manager: Optional[ResourceManager] = None
        self.shader_manager: Optional[ShaderManager] = None
        self.pipeline: Optional[RenderPipeline] = None
        self.scene_renderer: Optional[SceneRenderer] = None
        
        # Performance tracking
        self.stats = RenderStats()
        self.last_frame_time = time.time()
        self.frame_count = 0
        
        # Rendering state
        self.current_camera = None
        self.current_scene = None
        self.viewport_width = 0
        self.viewport_height = 0
        
    def initialize(self, window_handle: int, width: int, height: int) -> bool:
        """Initialize the renderer.
        
        Args:
            window_handle: Native window handle
            width: Initial viewport width
            height: Initial viewport height
            
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing renderer...")
            
            # Store viewport dimensions
            self.viewport_width = width
            self.viewport_height = height
            
            # Initialize graphics device
            self.device = GraphicsDevice(self.api)
            if not self.device.initialize(window_handle, width, height):
                self.logger.error("Failed to initialize graphics device")
                return False
            
            # Initialize resource manager
            self.resource_manager = ResourceManager(self.device)
            if not self.resource_manager.initialize():
                self.logger.error("Failed to initialize resource manager")
                return False
            
            # Initialize shader manager
            self.shader_manager = ShaderManager(self.device)
            if not self.shader_manager.initialize():
                self.logger.error("Failed to initialize shader manager")
                return False
            
            # Initialize render pipeline
            self.pipeline = RenderPipeline(self.device, self.shader_manager)
            if not self.pipeline.initialize():
                self.logger.error("Failed to initialize render pipeline")
                return False
            
            # Initialize scene renderer
            self.scene_renderer = SceneRenderer(self.device, self.pipeline)
            if not self.scene_renderer.initialize():
                self.logger.error("Failed to initialize scene renderer")
                return False
            
            self.is_initialized = True
            self.logger.info("✅ Renderer initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize renderer: {e}", exc_info=True)
            return False
    
    def resize_viewport(self, width: int, height: int):
        """Resize the viewport.
        
        Args:
            width: New viewport width
            height: New viewport height
        """
        if not self.is_initialized:
            return
        
        self.viewport_width = width
        self.viewport_height = height
        
        # Update device viewport
        self.device.set_viewport(0, 0, width, height)
        
        # Update pipeline
        if self.pipeline:
            self.pipeline.resize_viewport(width, height)
        
        self.logger.info(f"Viewport resized to {width}x{height}")
    
    def begin_frame(self) -> bool:
        """Begin rendering frame.
        
        Returns:
            True if frame can be rendered, False otherwise
        """
        if not self.is_initialized:
            return False
        
        # Begin device frame
        if not self.device.begin_frame():
            return False
        
        # Clear render target
        self.device.clear_render_target((0.2, 0.3, 0.4, 1.0))
        
        # Reset stats
        self.stats.draw_calls = 0
        self.stats.triangles = 0
        self.stats.vertices = 0
        
        return True
    
    def end_frame(self) -> bool:
        """End rendering frame and present.
        
        Returns:
            True if frame presented successfully, False otherwise
        """
        if not self.is_initialized:
            return False
        
        # Update performance stats
        self._update_stats()
        
        # Present frame
        return self.device.end_frame()
    
    def render_scene(self, scene, camera):
        """Render a scene with the specified camera.
        
        Args:
            scene: Scene to render
            camera: Camera to render from
        """
        if not self.is_initialized or not self.scene_renderer:
            return
        
        self.current_scene = scene
        self.current_camera = camera
        
        # Render the scene
        self.scene_renderer.render_scene(scene, camera)
        
        # Update stats from scene renderer
        scene_stats = self.scene_renderer.get_stats()
        self.stats.draw_calls += scene_stats.draw_calls
        self.stats.triangles += scene_stats.triangles
        self.stats.vertices += scene_stats.vertices
    
    def render_ui(self, ui_elements: List[Any]):
        """Render UI elements.
        
        Args:
            ui_elements: List of UI elements to render
        """
        if not self.is_initialized:
            return
        
        # TODO: Implement UI rendering
        # This would involve:
        # - Setting up UI render state
        # - Rendering UI elements
        # - Updating draw call stats
        
        self.logger.debug(f"Rendering {len(ui_elements)} UI elements")
    
    def set_camera(self, camera):
        """Set the current camera.
        
        Args:
            camera: Camera to set as current
        """
        self.current_camera = camera
        
        if self.pipeline:
            self.pipeline.set_camera(camera)
    
    def load_shader(self, name: str, vertex_source: str, pixel_source: str) -> bool:
        """Load a shader program.
        
        Args:
            name: Shader name
            vertex_source: Vertex shader source code
            pixel_source: Pixel shader source code
            
        Returns:
            True if shader loaded successfully, False otherwise
        """
        if not self.shader_manager:
            return False
        
        return self.shader_manager.load_shader(name, vertex_source, pixel_source)
    
    def load_texture(self, name: str, path: str) -> bool:
        """Load a texture from file.
        
        Args:
            name: Texture name
            path: Path to texture file
            
        Returns:
            True if texture loaded successfully, False otherwise
        """
        if not self.resource_manager:
            return False
        
        return self.resource_manager.load_texture(name, path)
    
    def load_mesh(self, name: str, path: str) -> bool:
        """Load a mesh from file.
        
        Args:
            name: Mesh name
            path: Path to mesh file
            
        Returns:
            True if mesh loaded successfully, False otherwise
        """
        if not self.resource_manager:
            return False
        
        return self.resource_manager.load_mesh(name, path)
    
    def get_shader(self, name: str):
        """Get a shader by name.
        
        Args:
            name: Shader name
            
        Returns:
            Shader object or None if not found
        """
        if not self.shader_manager:
            return None
        
        return self.shader_manager.get_shader(name)
    
    def get_texture(self, name: str):
        """Get a texture by name.
        
        Args:
            name: Texture name
            
        Returns:
            Texture object or None if not found
        """
        if not self.resource_manager:
            return None
        
        return self.resource_manager.get_texture(name)
    
    def get_mesh(self, name: str):
        """Get a mesh by name.
        
        Args:
            name: Mesh name
            
        Returns:
            Mesh object or None if not found
        """
        if not self.resource_manager:
            return None
        
        return self.resource_manager.get_mesh(name)
    
    def _update_stats(self):
        """Update rendering statistics."""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        
        if frame_time > 0:
            self.stats.fps = 1.0 / frame_time
            self.stats.frame_time = frame_time * 1000.0  # Convert to milliseconds
        
        self.last_frame_time = current_time
        self.frame_count += 1
        
        # Update memory stats
        if self.device:
            used, total = self.device.get_memory_usage()
            self.stats.memory_used = used
            self.stats.memory_total = total
    
    def get_stats(self) -> RenderStats:
        """Get current rendering statistics.
        
        Returns:
            Current rendering statistics
        """
        return self.stats
    
    def get_device_info(self):
        """Get graphics device information.
        
        Returns:
            Device information or None if not initialized
        """
        if not self.device:
            return None
        
        return self.device.get_device_info()
    
    def shutdown(self):
        """Shutdown the renderer."""
        if self.is_initialized:
            self.logger.info("Shutting down renderer...")
            
            # Shutdown components in reverse order
            if self.scene_renderer:
                self.scene_renderer.shutdown()
                self.scene_renderer = None
            
            if self.pipeline:
                self.pipeline.shutdown()
                self.pipeline = None
            
            if self.shader_manager:
                self.shader_manager.shutdown()
                self.shader_manager = None
            
            if self.resource_manager:
                self.resource_manager.shutdown()
                self.resource_manager = None
            
            if self.device:
                self.device.shutdown()
                self.device = None
            
            self.is_initialized = False
            self.logger.info("✅ Renderer shutdown complete")