"""
Scene management system for Nexlify Engine.

This module provides scene-level management for GameObjects, including:
- Scene hierarchy management
- GameObject creation and destruction
- Scene serialization and deserialization
- Scene-wide operations and queries
"""

from typing import List, Optional, Dict, Any, Callable, TYPE_CHECKING
import json
import time

if TYPE_CHECKING:
    from .game_object import GameObject

from ..utils.logger import get_logger

class Scene:
    """Represents a scene containing GameObjects and managing their lifecycle."""
    
    def __init__(self, name: str = "Default Scene"):
        self.name = name
        self.root_objects: List['GameObject'] = []
        self.all_objects: Dict[str, 'GameObject'] = {}
        self.selected_objects: List['GameObject'] = []
        self.is_playing = False
        self.is_paused = False
        self.play_start_time = 0.0
        self.total_play_time = 0.0
        self.logger = get_logger(__name__)

    def add_game_object(self, game_object: 'GameObject', parent: Optional['GameObject'] = None) -> 'GameObject':
        """Add a GameObject to the scene."""
        if game_object.id in self.all_objects:
            self.logger.warning(f"GameObject {game_object.name} already exists in scene")
            return game_object
        
        # Add to all objects dictionary
        self.all_objects[game_object.id] = game_object
        
        # Set parent relationship
        if parent:
            parent.add_child(game_object)
        else:
            # Add as root object
            self.root_objects.append(game_object)
            game_object.parent = None
        
        self.logger.info(f"Added GameObject '{game_object.name}' to scene '{self.name}'")
        return game_object

    def remove_game_object(self, game_object: 'GameObject') -> bool:
        """Remove a GameObject from the scene."""
        if game_object.id not in self.all_objects:
            return False
        
        # Remove from parent
        if game_object.parent:
            game_object.parent.remove_child(game_object)
        else:
            # Remove from root objects
            if game_object in self.root_objects:
                self.root_objects.remove(game_object)
        
        # Remove from selection
        if game_object in self.selected_objects:
            self.selected_objects.remove(game_object)
        
        # Remove from all objects
        del self.all_objects[game_object.id]
        
        # Destroy the GameObject
        game_object.destroy()
        
        self.logger.info(f"Removed GameObject '{game_object.name}' from scene '{self.name}'")
        return True

    def find_game_object(self, name: str) -> Optional['GameObject']:
        """Find a GameObject by name."""
        for game_object in self.all_objects.values():
            if game_object.name == name:
                return game_object
        return None

    def find_game_objects_by_tag(self, tag: str) -> List['GameObject']:
        """Find all GameObjects with a specific tag."""
        return [obj for obj in self.all_objects.values() if obj.tag == tag]

    def find_game_objects_by_layer(self, layer: int) -> List['GameObject']:
        """Find all GameObjects on a specific layer."""
        return [obj for obj in self.all_objects.values() if obj.layer == layer]

    def select_game_object(self, game_object: 'GameObject', add_to_selection: bool = False) -> None:
        """Select a GameObject."""
        if game_object not in self.all_objects.values():
            return
        
        if not add_to_selection:
            self.selected_objects.clear()
        
        if game_object not in self.selected_objects:
            self.selected_objects.append(game_object)

    def deselect_game_object(self, game_object: 'GameObject') -> None:
        """Deselect a GameObject."""
        if game_object in self.selected_objects:
            self.selected_objects.remove(game_object)

    def clear_selection(self) -> None:
        """Clear all selections."""
        self.selected_objects.clear()

    def get_selected_objects(self) -> List['GameObject']:
        """Get all selected GameObjects."""
        return self.selected_objects.copy()

    def get_root_objects(self) -> List['GameObject']:
        """Get all root GameObjects in the scene."""
        return self.root_objects.copy()

    def get_all_objects(self) -> List['GameObject']:
        """Get all GameObjects in the scene."""
        return list(self.all_objects.values())

    def get_object_count(self) -> int:
        """Get the total number of GameObjects in the scene."""
        return len(self.all_objects)

    def play_scene(self) -> None:
        """Start playing the scene."""
        if not self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.play_start_time = time.time()
            self.logger.info(f"Started playing scene '{self.name}'")

    def pause_scene(self) -> None:
        """Pause the scene."""
        if self.is_playing and not self.is_paused:
            self.is_paused = True
            self.total_play_time += time.time() - self.play_start_time
            self.logger.info(f"Paused scene '{self.name}'")

    def resume_scene(self) -> None:
        """Resume the scene."""
        if self.is_playing and self.is_paused:
            self.is_paused = False
            self.play_start_time = time.time()
            self.logger.info(f"Resumed scene '{self.name}'")

    def stop_scene(self) -> None:
        """Stop playing the scene."""
        if self.is_playing:
            self.is_playing = False
            self.is_paused = False
            self.total_play_time = 0.0
            self.logger.info(f"Stopped playing scene '{self.name}'")

    def is_scene_playing(self) -> bool:
        """Check if the scene is currently playing."""
        return self.is_playing

    def is_scene_paused(self) -> bool:
        """Check if the scene is currently paused."""
        return self.is_paused

    def get_play_time(self) -> float:
        """Get the total time the scene has been playing."""
        if not self.is_playing:
            return self.total_play_time
        
        if self.is_paused:
            return self.total_play_time
        
        return self.total_play_time + (time.time() - self.play_start_time)

    def update(self, delta_time: float) -> None:
        """Update all GameObjects in the scene."""
        if not self.is_playing or self.is_paused:
            return
        
        # Update all root objects (children will be updated recursively)
        for game_object in self.root_objects:
            game_object.update(delta_time)

    def render(self) -> None:
        """Render all GameObjects in the scene."""
        # Render all root objects (children will be rendered recursively)
        for game_object in self.root_objects:
            game_object.render()

    def serialize(self) -> Dict[str, Any]:
        """Serialize the scene to a dictionary."""
        return {
            'name': self.name,
            'root_objects': [obj.serialize() for obj in self.root_objects],
            'is_playing': self.is_playing,
            'is_paused': self.is_paused,
            'total_play_time': self.total_play_time
        }

    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the scene from a dictionary."""
        self.name = data.get('name', self.name)
        self.is_playing = data.get('is_playing', False)
        self.is_paused = data.get('is_paused', False)
        self.total_play_time = data.get('total_play_time', 0.0)
        
        # Note: GameObject deserialization would need special handling
        # as it requires the actual GameObject class to be available

    def save_to_file(self, file_path: str) -> bool:
        """Save the scene to a file."""
        try:
            scene_data = self.serialize()
            with open(file_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
            self.logger.info(f"Saved scene '{self.name}' to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save scene '{self.name}': {e}")
            return False

    def load_from_file(self, file_path: str) -> bool:
        """Load the scene from a file."""
        try:
            with open(file_path, 'r') as f:
                scene_data = json.load(f)
            self.deserialize(scene_data)
            self.logger.info(f"Loaded scene '{self.name}' from {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load scene from {file_path}: {e}")
            return False

    def clear(self) -> None:
        """Clear all GameObjects from the scene."""
        # Destroy all objects
        for game_object in list(self.all_objects.values()):
            game_object.destroy()
        
        # Clear collections
        self.root_objects.clear()
        self.all_objects.clear()
        self.selected_objects.clear()
        
        # Reset scene state
        self.is_playing = False
        self.is_paused = False
        self.total_play_time = 0.0
        
        self.logger.info(f"Cleared scene '{self.name}'")

    def __str__(self) -> str:
        """String representation of the scene."""
        return f"Scene('{self.name}', objects={len(self.all_objects)}, playing={self.is_playing})"

    def __repr__(self) -> str:
        """Detailed string representation of the scene."""
        return f"Scene(name='{self.name}', root_objects={len(self.root_objects)}, all_objects={len(self.all_objects)}, selected={len(self.selected_objects)}, playing={self.is_playing}, paused={self.is_paused})"
