"""
AI Manager for Nexlify Engine.

This module coordinates all AI functionality including:
- Asset generation
- Code assistance
- Procedural content generation
- AI-powered game logic
"""

import logging
from typing import Dict, Any, Optional, List

from .asset_generator import AIAssetGenerator, GenerationRequest, GenerationResult
from ..utils.logger import get_logger


class AIManager:
    """Manages AI functionality for code generation and asset creation."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.logger = get_logger(__name__)
        self.initialized = False
        self.config = config or {}
        
        # AI subsystems
        self.asset_generator: Optional[AIAssetGenerator] = None
        
        # Generation history
        self.generation_history: List[GenerationResult] = []
        
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the AI manager."""
        try:
            self.logger.info("Initializing AI manager...")
            
            # Initialize asset generator
            self.asset_generator = AIAssetGenerator()
            if not self.asset_generator.initialize():
                self.logger.error("Failed to initialize asset generator")
                return False
            
            # TODO: Initialize other AI services
            # - Code completion
            # - Procedural generation
            # - AI-powered game logic
            
            self.initialized = True
            self.logger.info("✅ AI manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize AI manager: {e}")
            return False
    
    def generate_asset(self, asset_type: str, prompt: str, parameters: Dict[str, Any] = None, 
                      output_path: str = None) -> GenerationResult:
        """Generate an asset using AI.
        
        Args:
            asset_type: Type of asset to generate ("texture", "material", "mesh", "code")
            prompt: Description of what to generate
            parameters: Additional generation parameters
            output_path: Optional output path
            
        Returns:
            Generation result
        """
        if not self.initialized or not self.asset_generator:
            return GenerationResult(False, error_message="AI Manager not initialized")
        
        try:
            # Create generation request
            request = GenerationRequest(
                asset_type=asset_type,
                prompt=prompt,
                parameters=parameters or {},
                output_path=output_path or ""
            )
            
            # Generate asset
            result = self.asset_generator.generate_asset(request)
            
            # Add to history
            self.generation_history.append(result)
            
            # Keep only last 100 generations
            if len(self.generation_history) > 100:
                self.generation_history = self.generation_history[-100:]
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating asset: {e}")
            return GenerationResult(False, error_message=str(e))
    
    def generate_texture(self, prompt: str, width: int = 512, height: int = 512, 
                        texture_type: str = "noise") -> GenerationResult:
        """Generate a texture using AI.
        
        Args:
            prompt: Description of the texture
            width: Texture width
            height: Texture height
            texture_type: Type of texture ("noise", "gradient", "pattern")
            
        Returns:
            Generation result
        """
        parameters = {
            "width": width,
            "height": height,
            "type": texture_type
        }
        
        return self.generate_asset("texture", prompt, parameters)
    
    def generate_material(self, prompt: str, material_type: str = "standard") -> GenerationResult:
        """Generate a material using AI.
        
        Args:
            prompt: Description of the material
            material_type: Type of material ("standard", "pbr", "unlit")
            
        Returns:
            Generation result
        """
        parameters = {
            "type": material_type
        }
        
        return self.generate_asset("material", prompt, parameters)
    
    def generate_code(self, prompt: str, language: str = "python", 
                     code_type: str = "component") -> GenerationResult:
        """Generate code using AI.
        
        Args:
            prompt: Description of the code to generate
            language: Programming language ("python", "javascript", "csharp")
            code_type: Type of code ("component", "script", "shader")
            
        Returns:
            Generation result
        """
        parameters = {
            "language": language,
            "code_type": code_type
        }
        
        return self.generate_asset("code", prompt, parameters)
    
    def get_generation_history(self) -> List[GenerationResult]:
        """Get the generation history.
        
        Returns:
            List of generation results
        """
        return self.generation_history.copy()
    
    def get_supported_asset_types(self) -> List[str]:
        """Get list of supported asset types.
        
        Returns:
            List of supported asset types
        """
        if self.asset_generator:
            return self.asset_generator.get_supported_types()
        return []
    
    def get_output_directories(self) -> Dict[str, str]:
        """Get output directories for generated assets.
        
        Returns:
            Dictionary of asset type to output directory
        """
        if self.asset_generator:
            return self.asset_generator.get_output_directories()
        return {}
    
    def update(self, delta_time: float) -> None:
        """Update AI manager state."""
        if not self.initialized:
            return
        
        # TODO: Update AI services
        # - Check for hot reloading
        # - Update AI models
        # - Process background tasks
    
    def shutdown(self) -> None:
        """Shutdown the AI manager."""
        if self.initialized:
            self.logger.info("Shutting down AI manager...")
            
            # Shutdown asset generator
            if self.asset_generator:
                self.asset_generator.shutdown()
                self.asset_generator = None
            
            # Clear history
            self.generation_history.clear()
            
            self.initialized = False
            self.logger.info("✅ AI manager shutdown complete")
