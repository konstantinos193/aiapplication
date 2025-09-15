"""
Core game engine for Nexlify.

This module contains the main game engine class that coordinates
all engine systems and manages the game loop.
"""

import time
import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from dataclasses import dataclass
import threading

if TYPE_CHECKING:
    from .game_object import GameObject
    from .component import Component

from .scene import Scene
from ..utils.logger import get_logger


@dataclass
class EngineStats:
    """Engine performance statistics."""
    fps: float = 0.0
    frame_time: float = 0.0
    update_time: float = 0.0
    render_time: float = 0.0
    game_object_count: int = 0
    scene_count: int = 0


class GameEngine:
    """Main game engine class."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the game engine.
        
        Args:
            config: Engine configuration dictionary
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        self.is_initialized = False
        self.is_running = False
        
        # Scene management
        self.current_scene: Optional[Scene] = None
        self.scenes: Dict[str, Scene] = {}
        
        # Performance tracking
        self.stats = EngineStats()
        self.last_frame_time = time.time()
        self.frame_count = 0
        
        # Core systems
        self.renderer = None
        
        self.logger.info("Game Engine created")
    
    def initialize(self) -> bool:
        """Initialize all engine systems.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing Game Engine")
            
            # Initialize core systems
            if not self._init_core_systems():
                return False
            
            # Initialize managers
            if not self._init_managers():
                return False
            
            # Setup default scene
            if not self._setup_default_scene():
                return False
            
            self.is_initialized = True
            self.logger.info("Game Engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize game engine: {e}", exc_info=True)
            return False
    
    def _init_core_systems(self) -> bool:
        """Initialize core engine systems."""
        try:
            # Initialize rendering system
            from ..rendering import Renderer, GraphicsAPI
            self.renderer = Renderer(GraphicsAPI.DIRECTX_12)
            
            # TODO: Initialize other core systems
            # - Audio system
            # - Input system
            # - Physics system
            # - AI system
            
            self.logger.info("Core systems initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize core systems: {e}")
            return False
    
    def _init_managers(self) -> bool:
        """Initialize engine managers."""
        try:
            # In a real engine, this would initialize various managers
            self.logger.info("Managers initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize managers: {e}")
            return False
    
    def _setup_default_scene(self) -> bool:
        """Setup the default scene with basic objects."""
        try:
            # Create default scene
            self.current_scene = Scene("Default Scene")
            self.scenes["Default Scene"] = self.current_scene
            
            # Create main camera
            main_camera = self.create_camera("Main Camera")
            if main_camera:
                main_camera.transform.set_position(0, 5, 10)
                main_camera.transform.set_rotation(0, 0, 0)
            
            # Create directional light
            directional_light = self.create_light("Directional Light", "Directional")
            if directional_light:
                directional_light.transform.set_position(0, 10, 0)
                directional_light.transform.set_rotation(45, 45, 0)
                # Get the light component and set intensity
                light_component = directional_light.get_component(self._get_light_component_class())
                if light_component:
                    light_component.set_intensity(1.5)
            
            # Create ground plane (simple cube for now)
            ground = self.create_cube("Ground")
            if ground:
                ground.transform.set_position(0, -0.5, 0)
                ground.transform.set_scale(20, 1, 20)
            
            self.logger.info("Default scene setup complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup default scene: {e}")
            return False
    
    def _get_light_component_class(self):
        """Get the Light component class for type checking."""
        from .components import Light
        return Light
    
    # Scene management methods
    
    def create_scene(self, name: str) -> Scene:
        """Create a new scene."""
        scene = Scene(name)
        self.scenes[name] = scene
        self.logger.info(f"Created scene: {name}")
        return scene
    
    def load_scene(self, name: str) -> bool:
        """Load a scene by name."""
        if name in self.scenes:
            self.current_scene = self.scenes[name]
            self.logger.info(f"Loaded scene: {name}")
            return True
        return False
    
    def get_current_scene(self) -> Optional[Scene]:
        """Get the current active scene."""
        return self.current_scene
    
    def get_scene_names(self) -> List[str]:
        """Get all available scene names."""
        return list(self.scenes.keys())
    
    # GameObject creation methods
    
    def create_game_object(self, name: str = "GameObject", parent: Optional['GameObject'] = None) -> Optional['GameObject']:
        """Create a new GameObject in the current scene."""
        if not self.current_scene:
            self.logger.error("No active scene")
            return None
        
        from .game_object import GameObject
        game_object = GameObject(name)
        
        if parent:
            parent.add_child(game_object)
        else:
            self.current_scene.add_game_object(game_object)
        
        self.logger.debug(f"Created GameObject: {name}")
        return game_object
    
    def create_cube(self, name: str = "Cube", parent: Optional['GameObject'] = None) -> Optional['GameObject']:
        """Create a cube GameObject."""
        game_object = self.create_game_object(name, parent)
        if not game_object:
            return None
        
        # Add mesh renderer component
        from .components import MeshRenderer
        mesh_renderer = MeshRenderer()
        game_object.add_component(mesh_renderer)
        
        # Add collider component
        from .components import Collider
        collider = Collider()
        game_object.add_component(collider)
        
        return game_object
    
    def create_sphere(self, name: str = "Sphere", parent: Optional['GameObject'] = None) -> Optional['GameObject']:
        """Create a sphere GameObject."""
        game_object = self.create_game_object(name, parent)
        if not game_object:
            return None
        
        # Add mesh renderer component
        from .components import MeshRenderer
        mesh_renderer = MeshRenderer()
        game_object.add_component(mesh_renderer)
        
        # Add collider component
        from .components import Collider
        collider = Collider()
        game_object.add_component(collider)
        
        return game_object
    
    def create_light(self, name: str = "Light", light_type: str = "Point", parent: Optional['GameObject'] = None) -> Optional['GameObject']:
        """Create a light GameObject."""
        game_object = self.create_game_object(name, parent)
        if not game_object:
            return None
        
        # Add light component
        from .components import Light
        light_component = Light(light_type)
        game_object.add_component(light_component)
        
        return game_object
    
    def create_camera(self, name: str = "Camera", parent: Optional['GameObject'] = None) -> Optional['GameObject']:
        """Create a camera GameObject."""
        game_object = self.create_game_object(name, parent)
        if not game_object:
            return None
        
        # Add camera component
        from .components import Camera
        camera_component = Camera()
        game_object.add_component(camera_component)
        
        return game_object
    
    def create_empty(self, name: str = "Empty", parent: Optional['GameObject'] = None) -> Optional['GameObject']:
        """Create an empty GameObject (no visual representation)."""
        return self.create_game_object(name, parent)
    
    def destroy_game_object(self, game_object: 'GameObject') -> bool:
        """Destroy a GameObject."""
        if not self.current_scene:
            return False
        
        return self.current_scene.remove_game_object(game_object)
    
    def find_game_object(self, name: str) -> Optional['GameObject']:
        """Find a GameObject by name in the current scene."""
        if not self.current_scene:
            return None
        
        return self.current_scene.find_game_object(name)
    
    def get_all_game_objects(self) -> List['GameObject']:
        """Get all GameObjects in the current scene."""
        if not self.current_scene:
            return []
        
        return self.current_scene.get_all_objects()
    
    def get_selected_game_objects(self) -> List['GameObject']:
        """Get all selected GameObjects in the current scene."""
        if not self.current_scene:
            return []
        
        return self.current_scene.get_selected_objects()
    
    def select_game_object(self, game_object: 'GameObject', add_to_selection: bool = False):
        """Select a GameObject in the current scene."""
        if self.current_scene:
            self.current_scene.select_game_object(game_object, add_to_selection)
    
    def clear_selection(self):
        """Clear all selected GameObjects."""
        if self.current_scene:
            self.current_scene.clear_selection()
    
    # Scene playback methods
    
    def play_scene(self):
        """Start playing the current scene."""
        if self.current_scene:
            self.current_scene.play_scene()
    
    def pause_scene(self):
        """Pause the current scene."""
        if self.current_scene:
            self.current_scene.pause_scene()
    
    def resume_scene(self):
        """Resume the current scene."""
        if self.current_scene:
            self.current_scene.resume_scene()
    
    def stop_scene(self):
        """Stop the current scene."""
        if self.current_scene:
            self.current_scene.stop_scene()
    
    def is_scene_playing(self) -> bool:
        """Check if the current scene is playing."""
        return self.current_scene.is_scene_playing() if self.current_scene else False
    
    def is_scene_paused(self) -> bool:
        """Check if the current scene is paused."""
        return self.current_scene.is_scene_paused() if self.current_scene else False
    
    # Engine loop methods
    
    def start(self):
        """Start the engine main loop."""
        if not self.is_initialized:
            self.logger.error("Engine not initialized")
            return
        
        self.is_running = True
        self.logger.info("Engine started")
    
    def stop(self):
        """Stop the engine main loop."""
        self.is_running = False
        self.logger.info("🛑 Engine stopped")
    
    def update(self, delta_time: float):
        """Update the engine and all systems."""
        if not self.is_running:
            return
        
        # Update current scene
        if self.current_scene:
            self.current_scene.update(delta_time)
    
    def render(self):
        """Render the current scene."""
        if not self.is_running or not self.renderer:
            return
        
        # Begin render frame
        if not self.renderer.begin_frame():
            return
        
        # Render current scene
        if self.current_scene:
            # Find main camera
            main_camera = self._find_main_camera()
            if main_camera:
                self.renderer.render_scene(self.current_scene, main_camera)
        
        # End render frame
        self.renderer.end_frame()
    
    def run_frame(self, delta_time: float):
        """Run a single frame of the engine."""
        start_time = time.time()
        
        # Update
        update_start = time.time()
        self.update(delta_time)
        update_time = time.time() - update_start
        
        # Render
        render_start = time.time()
        self.render()
        render_time = time.time() - render_start
        
        # Update stats
        self._update_stats(delta_time, update_time, render_time)
    
    def _update_stats(self, delta_time: float, update_time: float, render_time: float):
        """Update engine statistics."""
        self.stats.frame_time = delta_time
        self.stats.update_time = update_time
        self.stats.render_time = render_time
        
        # Calculate FPS
        current_time = time.time()
        if current_time - self.last_frame_time > 0:
            self.stats.fps = 1.0 / (current_time - self.last_frame_time)
        self.last_frame_time = current_time
        
        # Update game object count
        if self.current_scene:
            self.stats.game_object_count = self.current_scene.get_object_count()
        else:
            self.stats.game_object_count = 0
        
        # Update scene count
        self.stats.scene_count = len(self.scenes)
        
        self.frame_count += 1
    
    def get_stats(self) -> EngineStats:
        """Get current engine statistics."""
        return self.stats
    
    def shutdown(self):
        """Shutdown the engine and cleanup resources."""
        self.logger.info("🔄 Shutting down Game Engine")
        
        # Stop the engine
        self.stop()
        
        # Clear scenes
        if self.current_scene:
            self.current_scene.clear()
        
        self.scenes.clear()
        self.current_scene = None
        
        # Shutdown renderer
        if self.renderer:
            self.renderer.shutdown()
            self.renderer = None
        
        self.is_initialized = False
        self.logger.info("Game Engine shutdown complete")
    
    def _find_main_camera(self):
        """Find the main camera in the current scene."""
        if not self.current_scene:
            return None
        
        # Look for camera in scene
        for game_object in self.current_scene.get_all_objects():
            camera_component = game_object.get_component(self._get_camera_component_class())
            if camera_component:
                return camera_component
        
        return None
    
    def _get_camera_component_class(self):
        """Get the Camera component class for type checking."""
        from .components import Camera
        return Camera
    
    def initialize_renderer(self, window_handle: int, width: int, height: int) -> bool:
        """Initialize the renderer with window information.
        
        Args:
            window_handle: Native window handle
            width: Window width
            height: Window height
            
        Returns:
            True if renderer initialized successfully, False otherwise
        """
        if not self.renderer:
            self.logger.error("Renderer not created")
            return False
        
        return self.renderer.initialize(window_handle, width, height)
    
    def resize_renderer(self, width: int, height: int):
        """Resize the renderer viewport.
        
        Args:
            width: New viewport width
            height: New viewport height
        """
        if self.renderer:
            self.renderer.resize_viewport(width, height)
