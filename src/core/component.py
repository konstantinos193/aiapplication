"""
Base Component class for Nexlify Engine.

This module provides the foundation for all components in the GameObject system.
Components are modular pieces of functionality that can be attached to GameObjects.
"""

from typing import Optional, Dict, Any, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .game_object import GameObject

class Component(ABC):
    """Base class for all components in the GameObject system."""
    
    def __init__(self, name: str = None):
        """Initialize a new component."""
        self.name = name or self.__class__.__name__
        self.game_object: Optional['GameObject'] = None
        self.enabled = True
        self.unique = False  # Whether only one instance can exist per GameObject
        
        # Component lifecycle
        self.initialized = False
        self.destroyed = False
    
    def get_game_object(self) -> Optional['GameObject']:
        """Get the GameObject this component is attached to."""
        return self.game_object
    
    def get_transform(self):
        """Get the transform component of the parent GameObject."""
        if self.game_object:
            return self.game_object.transform
        return None
    
    def get_position(self):
        """Get the position of the parent GameObject."""
        transform = self.get_transform()
        if transform:
            return transform.get_position()
        return [0.0, 0.0, 0.0]
    
    def get_rotation(self):
        """Get the rotation of the parent GameObject."""
        transform = self.get_transform()
        if transform:
            return transform.get_rotation()
        return [0.0, 0.0, 0.0]
    
    def get_scale(self):
        """Get the scale of the parent GameObject."""
        transform = self.get_transform()
        if transform:
            return transform.get_scale()
        return [1.0, 1.0, 0.0]
    
    def set_enabled(self, enabled: bool):
        """Enable or disable this component."""
        if self.enabled != enabled:
            self.enabled = enabled
            self._on_enabled_changed(enabled)
    
    def is_enabled(self) -> bool:
        """Check if this component is enabled."""
        return self.enabled and not self.destroyed
    
    def is_initialized(self) -> bool:
        """Check if this component has been initialized."""
        return self.initialized
    
    def is_destroyed(self) -> bool:
        """Check if this component has been destroyed."""
        return self.destroyed
    
    def initialize(self):
        """Initialize the component. Called when added to a GameObject."""
        if not self.initialized and not self.destroyed:
            self._on_initialize()
            self.initialized = True
    
    def destroy(self):
        """Destroy the component. Called when removed from a GameObject."""
        if not self.destroyed:
            self._on_destroy()
            self.destroyed = True
            self.initialized = False
    
    def update(self, delta_time: float):
        """Update the component. Called every frame."""
        if self.is_enabled() and self.initialized:
            self._on_update(delta_time)
    
    def render(self, renderer):
        """Render the component. Called every frame for rendering."""
        if self.is_enabled() and self.initialized:
            self._on_render(renderer)
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize the component to a dictionary."""
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'enabled': self.enabled,
            'unique': self.unique
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'Component':
        """Deserialize a component from a dictionary."""
        component = cls(data.get('name'))
        component.enabled = data.get('enabled', True)
        component.unique = data.get('unique', False)
        return component
    
    # Lifecycle methods - subclasses should override these
    
    def on_added(self):
        """Called when the component is added to a GameObject."""
        pass
    
    def on_removed(self):
        """Called when the component is removed from a GameObject."""
        pass
    
    def on_enable(self):
        """Called when the component is enabled."""
        pass
    
    def on_disable(self):
        """Called when the component is disabled."""
        pass
    
    def on_start(self):
        """Called when the component starts (first update after initialization)."""
        pass
    
    def on_destroy(self):
        """Called when the component is destroyed."""
        pass
    
    # Abstract methods that must be implemented by subclasses
    
    def _on_initialize(self) -> None:
        """Initialize the component. Override this method."""
        pass
    
    def _on_update(self, delta_time: float) -> None:
        """Update the component. Override this method."""
        pass
    
    def _on_render(self, renderer) -> None:
        """Render the component. Override this method."""
        pass
    
    # Optional lifecycle methods - subclasses can override these
    
    def _on_enabled_changed(self, enabled: bool):
        """Called when the enabled state changes."""
        if enabled:
            self.on_enable()
        else:
            self.on_disable()
    
    def _on_destroy(self) -> None:
        """Called when the component is destroyed."""
        self.on_destroy()
    
    def __str__(self) -> str:
        """String representation of the component."""
        game_object_name = self.game_object.name if self.game_object else "None"
        return f"{self.__class__.__name__}('{self.name}', GameObject: {game_object_name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the component."""
        return f"{self.__class__.__name__}(name='{self.name}', enabled={self.enabled}, initialized={self.initialized})"
