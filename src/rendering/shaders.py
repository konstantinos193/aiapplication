"""
Shader Manager for Nexlify Engine.

This module handles shader compilation, management, and hot-reloading
for different graphics APIs (DirectX 12, Vulkan, OpenGL).
"""

import os
import logging
import hashlib
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from .device import GraphicsDevice
from ..utils.logger import get_logger


class ShaderStage(Enum):
    """Shader stages."""
    VERTEX = "vertex"
    PIXEL = "pixel"
    GEOMETRY = "geometry"
    COMPUTE = "compute"
    HULL = "hull"
    DOMAIN = "domain"


@dataclass
class ShaderInfo:
    """Shader information."""
    name: str
    stage: ShaderStage
    source: str
    handle: int
    compiled: bool
    last_modified: float


class ShaderManager:
    """Manages shader compilation and loading."""
    
    def __init__(self, device: GraphicsDevice):
        self.device = device
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Shader storage
        self.shaders: Dict[str, ShaderInfo] = {}
        self.shader_programs: Dict[str, List[str]] = {}  # program_name -> [shader_names]
        
        # Shader paths
        self.shader_paths: List[str] = [
            "assets/shaders",
            "src/rendering/shaders"
        ]
        
        # Hot reloading
        self.hot_reload_enabled = True
        self.watched_files: Dict[str, float] = {}  # file_path -> last_modified
        
    def initialize(self) -> bool:
        """Initialize the shader manager.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing shader manager...")
            
            # Create shader directories
            for path in self.shader_paths:
                Path(path).mkdir(parents=True, exist_ok=True)
            
            # Load default shaders
            self._load_default_shaders()
            
            self.is_initialized = True
            self.logger.info("✅ Shader manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize shader manager: {e}", exc_info=True)
            return False
    
    def _load_default_shaders(self):
        """Load default shaders."""
        try:
            # Basic vertex shader
            vertex_source = """
            struct VSInput {
                float3 position : POSITION;
                float3 normal : NORMAL;
                float2 uv : TEXCOORD0;
            };
            
            struct VSOutput {
                float4 position : SV_POSITION;
                float3 worldPos : TEXCOORD0;
                float3 normal : TEXCOORD1;
                float2 uv : TEXCOORD2;
            };
            
            cbuffer PerObject : register(b0) {
                float4x4 worldMatrix;
                float4x4 viewMatrix;
                float4x4 projectionMatrix;
            };
            
            VSOutput main(VSInput input) {
                VSOutput output;
                
                float4 worldPos = mul(float4(input.position, 1.0), worldMatrix);
                output.worldPos = worldPos.xyz;
                
                output.position = mul(worldPos, viewMatrix);
                output.position = mul(output.position, projectionMatrix);
                
                output.normal = mul(input.normal, (float3x3)worldMatrix);
                output.uv = input.uv;
                
                return output;
            }
            """
            
            # Basic pixel shader
            pixel_source = """
            struct PSInput {
                float4 position : SV_POSITION;
                float3 worldPos : TEXCOORD0;
                float3 normal : TEXCOORD1;
                float2 uv : TEXCOORD2;
            };
            
            cbuffer PerFrame : register(b0) {
                float3 lightDirection;
                float3 lightColor;
                float3 ambientColor;
            };
            
            Texture2D diffuseTexture : register(t0);
            SamplerState textureSampler : register(s0);
            
            float4 main(PSInput input) : SV_TARGET {
                float3 normal = normalize(input.normal);
                float3 lightDir = normalize(-lightDirection);
                
                // Sample texture
                float4 diffuse = diffuseTexture.Sample(textureSampler, input.uv);
                
                // Calculate lighting
                float NdotL = max(0.0, dot(normal, lightDir));
                float3 lighting = ambientColor + lightColor * NdotL;
                
                return float4(diffuse.rgb * lighting, diffuse.a);
            }
            """
            
            # Load default shaders
            self.load_shader("default_vertex", vertex_source, ShaderStage.VERTEX)
            self.load_shader("default_pixel", pixel_source, ShaderStage.PIXEL)
            
            # Create default shader program
            self.create_shader_program("default", ["default_vertex", "default_pixel"])
            
            self.logger.info("Default shaders loaded")
            
        except Exception as e:
            self.logger.error(f"Failed to load default shaders: {e}")
    
    def load_shader(self, name: str, source: str, stage: ShaderStage) -> bool:
        """Load a shader from source code.
        
        Args:
            name: Shader name
            source: Shader source code
            stage: Shader stage
            
        Returns:
            True if shader loaded successfully, False otherwise
        """
        try:
            # Compile shader
            shader_handle = self.device.create_shader(source, stage.value)
            if shader_handle == 0:
                self.logger.error(f"Failed to compile shader: {name}")
                return False
            
            # Store shader info
            self.shaders[name] = ShaderInfo(
                name=name,
                stage=stage,
                source=source,
                handle=shader_handle,
                compiled=True,
                last_modified=0.0
            )
            
            self.logger.info(f"Loaded shader: {name} ({stage.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load shader {name}: {e}")
            return False
    
    def load_shader_from_file(self, name: str, file_path: str, stage: ShaderStage) -> bool:
        """Load a shader from file.
        
        Args:
            name: Shader name
            file_path: Path to shader file
            stage: Shader stage
            
        Returns:
            True if shader loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"Shader file not found: {file_path}")
                return False
            
            # Read shader source
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Load shader
            success = self.load_shader(name, source, stage)
            
            if success:
                # Track file for hot reloading
                self.watched_files[file_path] = os.path.getmtime(file_path)
                self.shaders[name].last_modified = os.path.getmtime(file_path)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to load shader from file {file_path}: {e}")
            return False
    
    def create_shader_program(self, name: str, shader_names: List[str]) -> bool:
        """Create a shader program from multiple shaders.
        
        Args:
            name: Program name
            shader_names: List of shader names to link
            
        Returns:
            True if program created successfully, False otherwise
        """
        try:
            # Validate all shaders exist
            for shader_name in shader_names:
                if shader_name not in self.shaders:
                    self.logger.error(f"Shader not found: {shader_name}")
                    return False
            
            # Store program
            self.shader_programs[name] = shader_names.copy()
            
            self.logger.info(f"Created shader program: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create shader program {name}: {e}")
            return False
    
    def get_shader(self, name: str) -> Optional[ShaderInfo]:
        """Get a shader by name.
        
        Args:
            name: Shader name
            
        Returns:
            Shader info or None if not found
        """
        return self.shaders.get(name)
    
    def get_shader_program(self, name: str) -> Optional[List[str]]:
        """Get a shader program by name.
        
        Args:
            name: Program name
            
        Returns:
            List of shader names or None if not found
        """
        return self.shader_programs.get(name)
    
    def reload_shader(self, name: str) -> bool:
        """Reload a shader.
        
        Args:
            name: Shader name
            
        Returns:
            True if shader reloaded successfully, False otherwise
        """
        try:
            if name not in self.shaders:
                self.logger.error(f"Shader not found: {name}")
                return False
            
            shader_info = self.shaders[name]
            
            # Recompile shader
            new_handle = self.device.create_shader(shader_info.source, shader_info.stage.value)
            if new_handle == 0:
                self.logger.error(f"Failed to recompile shader: {name}")
                return False
            
            # Update shader handle
            shader_info.handle = new_handle
            shader_info.compiled = True
            
            self.logger.info(f"Reloaded shader: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to reload shader {name}: {e}")
            return False
    
    def check_hot_reload(self):
        """Check for shader file changes and reload if necessary."""
        if not self.hot_reload_enabled:
            return
        
        try:
            for file_path, last_modified in self.watched_files.items():
                if os.path.exists(file_path):
                    current_modified = os.path.getmtime(file_path)
                    if current_modified > last_modified:
                        # Find shader using this file
                        for shader_name, shader_info in self.shaders.items():
                            if shader_info.last_modified == last_modified:
                                self.logger.info(f"Hot reloading shader: {shader_name}")
                                self.reload_shader(shader_name)
                                self.watched_files[file_path] = current_modified
                                break
                        
        except Exception as e:
            self.logger.error(f"Error during hot reload check: {e}")
    
    def enable_hot_reload(self, enabled: bool):
        """Enable or disable hot reloading.
        
        Args:
            enabled: Whether to enable hot reloading
        """
        self.hot_reload_enabled = enabled
        self.logger.info(f"Hot reloading {'enabled' if enabled else 'disabled'}")
    
    def get_shader_count(self) -> Dict[str, int]:
        """Get shader counts.
        
        Returns:
            Dictionary of shader counts
        """
        return {
            "shaders": len(self.shaders),
            "programs": len(self.shader_programs)
        }
    
    def list_shaders(self) -> List[str]:
        """List all loaded shader names.
        
        Returns:
            List of shader names
        """
        return list(self.shaders.keys())
    
    def list_programs(self) -> List[str]:
        """List all shader program names.
        
        Returns:
            List of program names
        """
        return list(self.shader_programs.keys())
    
    def shutdown(self):
        """Shutdown the shader manager."""
        if self.is_initialized:
            self.logger.info("Shutting down shader manager...")
            
            # Clear shaders
            self.shaders.clear()
            self.shader_programs.clear()
            self.watched_files.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Shader manager shutdown complete")
