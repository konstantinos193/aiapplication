"""
Render Pipeline for Nexlify Engine.

This module implements the rendering pipeline including:
- Pipeline state management
- Render passes
- Post-processing effects
- Performance optimization
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

from .device import GraphicsDevice
from .shaders import ShaderManager
from ..utils.logger import get_logger


class RenderPass(Enum):
    """Render pass types."""
    OPAQUE = "opaque"
    TRANSPARENT = "transparent"
    UI = "ui"
    POST_PROCESS = "post_process"


@dataclass
class PipelineState:
    """Pipeline state configuration."""
    shader_program: str
    blend_mode: str = "opaque"
    depth_test: bool = True
    depth_write: bool = True
    cull_mode: str = "back"
    fill_mode: str = "solid"
    wireframe: bool = False


@dataclass
class RenderPassInfo:
    """Render pass information."""
    name: str
    pass_type: RenderPass
    enabled: bool = True
    clear_color: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    clear_depth: bool = True
    clear_stencil: bool = False


class RenderPipeline:
    """Manages the rendering pipeline and render passes."""
    
    def __init__(self, device: GraphicsDevice, shader_manager: ShaderManager):
        self.device = device
        self.shader_manager = shader_manager
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Pipeline state
        self.current_state: Optional[PipelineState] = None
        self.viewport_width = 0
        self.viewport_height = 0
        
        # Render passes
        self.render_passes: Dict[str, RenderPassInfo] = {}
        self.pass_order: List[str] = []
        
        # Current camera
        self.current_camera = None
        
        # Performance tracking
        self.draw_calls = 0
        self.triangles = 0
        self.vertices = 0
        
    def initialize(self) -> bool:
        """Initialize the render pipeline.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing render pipeline...")
            
            # Setup default render passes
            self._setup_default_passes()
            
            self.is_initialized = True
            self.logger.info("✅ Render pipeline initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize render pipeline: {e}", exc_info=True)
            return False
    
    def _setup_default_passes(self):
        """Setup default render passes."""
        try:
            # Opaque pass
            self.add_render_pass("opaque", RenderPass.OPAQUE, (0.2, 0.3, 0.4, 1.0))
            
            # Transparent pass
            self.add_render_pass("transparent", RenderPass.TRANSPARENT, (0.0, 0.0, 0.0, 0.0))
            
            # UI pass
            self.add_render_pass("ui", RenderPass.UI, (0.0, 0.0, 0.0, 0.0))
            
            # Post-process pass
            self.add_render_pass("post_process", RenderPass.POST_PROCESS, (0.0, 0.0, 0.0, 1.0))
            
            self.logger.info("Default render passes setup complete")
            
        except Exception as e:
            self.logger.error(f"Failed to setup default passes: {e}")
    
    def add_render_pass(self, name: str, pass_type: RenderPass, 
                       clear_color: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)) -> bool:
        """Add a render pass.
        
        Args:
            name: Pass name
            pass_type: Type of render pass
            clear_color: Clear color for this pass
            
        Returns:
            True if pass added successfully, False otherwise
        """
        try:
            pass_info = RenderPassInfo(
                name=name,
                pass_type=pass_type,
                clear_color=clear_color
            )
            
            self.render_passes[name] = pass_info
            self.pass_order.append(name)
            
            self.logger.info(f"Added render pass: {name} ({pass_type.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add render pass {name}: {e}")
            return False
    
    def remove_render_pass(self, name: str) -> bool:
        """Remove a render pass.
        
        Args:
            name: Pass name
            
        Returns:
            True if pass removed successfully, False otherwise
        """
        try:
            if name in self.render_passes:
                del self.render_passes[name]
                if name in self.pass_order:
                    self.pass_order.remove(name)
                
                self.logger.info(f"Removed render pass: {name}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove render pass {name}: {e}")
            return False
    
    def begin_render_pass(self, pass_name: str) -> bool:
        """Begin a render pass.
        
        Args:
            pass_name: Name of the render pass
            
        Returns:
            True if pass began successfully, False otherwise
        """
        try:
            if pass_name not in self.render_passes:
                self.logger.error(f"Render pass not found: {pass_name}")
                return False
            
            pass_info = self.render_passes[pass_name]
            if not pass_info.enabled:
                return True  # Pass is disabled, skip it
            
            # Clear render target
            self.device.clear_render_target(pass_info.clear_color)
            
            # Reset stats for this pass
            self.draw_calls = 0
            self.triangles = 0
            self.vertices = 0
            
            self.logger.debug(f"Began render pass: {pass_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to begin render pass {pass_name}: {e}")
            return False
    
    def end_render_pass(self, pass_name: str) -> bool:
        """End a render pass.
        
        Args:
            pass_name: Name of the render pass
            
        Returns:
            True if pass ended successfully, False otherwise
        """
        try:
            if pass_name not in self.render_passes:
                return False
            
            self.logger.debug(f"Ended render pass: {pass_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to end render pass {pass_name}: {e}")
            return False
    
    def set_pipeline_state(self, state: PipelineState) -> bool:
        """Set the current pipeline state.
        
        Args:
            state: Pipeline state to set
            
        Returns:
            True if state set successfully, False otherwise
        """
        try:
            # Validate shader program
            if not self.shader_manager.get_shader_program(state.shader_program):
                self.logger.error(f"Shader program not found: {state.shader_program}")
                return False
            
            self.current_state = state
            
            # TODO: Apply pipeline state to graphics device
            # This would involve:
            # - Setting shader program
            # - Configuring blend state
            # - Setting depth/stencil state
            # - Configuring rasterizer state
            
            self.logger.debug(f"Set pipeline state: {state.shader_program}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set pipeline state: {e}")
            return False
    
    def set_camera(self, camera):
        """Set the current camera.
        
        Args:
            camera: Camera to set as current
        """
        self.current_camera = camera
        
        # TODO: Update camera matrices in constant buffers
        # This would involve:
        # - Calculating view matrix
        # - Calculating projection matrix
        # - Updating GPU constant buffers
        
        self.logger.debug("Camera set")
    
    def resize_viewport(self, width: int, height: int):
        """Resize the viewport.
        
        Args:
            width: New viewport width
            height: New viewport height
        """
        self.viewport_width = width
        self.viewport_height = height
        
        # Update device viewport
        self.device.set_viewport(0, 0, width, height)
        
        # TODO: Update projection matrices for all cameras
        # This would involve:
        # - Recalculating projection matrices
        # - Updating GPU constant buffers
        
        self.logger.info(f"Viewport resized to {width}x{height}")
    
    def render_all_passes(self, render_func):
        """Render all enabled passes.
        
        Args:
            render_func: Function to call for each pass
        """
        try:
            for pass_name in self.pass_order:
                if self.begin_render_pass(pass_name):
                    # Call render function for this pass
                    render_func(pass_name, self.render_passes[pass_name])
                    self.end_render_pass(pass_name)
                    
        except Exception as e:
            self.logger.error(f"Error rendering passes: {e}")
    
    def draw_mesh(self, mesh_info, material_info, transform_matrix):
        """Draw a mesh with the specified material and transform.
        
        Args:
            mesh_info: Mesh information
            material_info: Material information
            transform_matrix: Transform matrix
        """
        try:
            # TODO: Implement actual mesh drawing
            # This would involve:
            # - Setting vertex/index buffers
            # - Setting material properties
            # - Setting transform matrix
            # - Issuing draw call
            
            # Update stats
            self.draw_calls += 1
            self.triangles += mesh_info.index_count // 3
            self.vertices += mesh_info.vertex_count
            
            self.logger.debug(f"Drew mesh: {mesh_info.vertex_count} vertices, {mesh_info.index_count} indices")
            
        except Exception as e:
            self.logger.error(f"Failed to draw mesh: {e}")
    
    def get_stats(self) -> Dict[str, int]:
        """Get rendering statistics.
        
        Returns:
            Dictionary of rendering stats
        """
        return {
            "draw_calls": self.draw_calls,
            "triangles": self.triangles,
            "vertices": self.vertices
        }
    
    def reset_stats(self):
        """Reset rendering statistics."""
        self.draw_calls = 0
        self.triangles = 0
        self.vertices = 0
    
    def get_render_pass(self, name: str) -> Optional[RenderPassInfo]:
        """Get a render pass by name.
        
        Args:
            name: Pass name
            
        Returns:
            Render pass info or None if not found
        """
        return self.render_passes.get(name)
    
    def enable_render_pass(self, name: str, enabled: bool) -> bool:
        """Enable or disable a render pass.
        
        Args:
            name: Pass name
            enabled: Whether to enable the pass
            
        Returns:
            True if pass state changed successfully, False otherwise
        """
        if name in self.render_passes:
            self.render_passes[name].enabled = enabled
            self.logger.info(f"Render pass {name} {'enabled' if enabled else 'disabled'}")
            return True
        return False
    
    def shutdown(self):
        """Shutdown the render pipeline."""
        if self.is_initialized:
            self.logger.info("Shutting down render pipeline...")
            
            # Clear render passes
            self.render_passes.clear()
            self.pass_order.clear()
            
            # Reset state
            self.current_state = None
            self.current_camera = None
            
            self.is_initialized = False
            self.logger.info("✅ Render pipeline shutdown complete")
