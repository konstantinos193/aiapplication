"""
Transform Component for Nexlify Engine.

This module provides the TransformComponent class for positioning, rotation, and scaling.
"""

from typing import Dict, Any
from .component import Component


class TransformComponent(Component):
    """Transform component for positioning, rotation, and scaling."""
    
    def __init__(self, position=None, rotation=None, scale=None):
        """Initialize the transform component."""
        super().__init__("Transform")
        
        # Set initial values
        if position:
            self.position = list(position)
        else:
            self.position = [0.0, 0.0, 0.0]
            
        if rotation:
            self.rotation = list(rotation)
        else:
            self.rotation = [0.0, 0.0, 0.0]
            
        if scale:
            self.scale = list(scale)
        else:
            self.scale = [1.0, 1.0, 1.0]
    
    def _on_initialize(self) -> None:
        """Initialize the transform component."""
        # Update the GameObject's transform
        if self.game_object:
            self.game_object.transform.position = self.position
            self.game_object.transform.rotation = self.rotation
            self.game_object.transform.scale = self.scale
    
    def _on_update(self, delta_time: float) -> None:
        """Update the transform component."""
        # Sync with GameObject transform
        if self.game_object:
            self.position = self.game_object.transform.position
            self.rotation = self.game_object.transform.rotation
            self.scale = self.game_object.transform.scale
    
    def _on_render(self, renderer) -> None:
        """Render the transform component."""
        # Transform components don't render anything
        pass
    
    def set_position(self, x: float, y: float, z: float) -> None:
        """Set the position."""
        self.position = [x, y, z]
        if self.game_object:
            self.game_object.transform.set_position(x, y, z)
    
    def set_rotation(self, x: float, y: float, z: float) -> None:
        """Set the rotation in degrees."""
        self.rotation = [x, y, z]
        if self.game_object:
            self.game_object.transform.set_rotation(x, y, z)
    
    def set_scale(self, x: float, y: float, z: float) -> None:
        """Set the scale."""
        self.scale = [x, y, z]
        if self.game_object:
            self.game_object.transform.set_scale(x, y, z)
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize the transform component."""
        data = super().serialize()
        data.update({
            'position': self.position,
            'rotation': self.rotation,
            'scale': self.scale
        })
        return data
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'TransformComponent':
        """Deserialize a transform component."""
        component = cls(
            position=data.get('position', [0.0, 0.0, 0.0]),
            rotation=data.get('rotation', [0.0, 0.0, 0.0]),
            scale=data.get('scale', [1.0, 1.0, 1.0])
        )
        component.enabled = data.get('enabled', True)
        return component
