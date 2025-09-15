"""
Script Component base class for Nexlify Engine.

This module provides the base class for all scriptable components
that can be attached to GameObjects.
"""

import logging
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

from ..core.component import Component
from ..utils.logger import get_logger


class ScriptComponent(Component, ABC):
    """Base class for all scriptable components."""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(self.__class__.__name__)
        self.instance_id: Optional[int] = None
        self.game_object = None
        self.enabled = True
        
    def set_instance_id(self, instance_id: int):
        """Set the script instance ID.
        
        Args:
            instance_id: Unique instance ID
        """
        self.instance_id = instance_id
    
    def set_game_object(self, game_object):
        """Set the associated GameObject.
        
        Args:
            game_object: GameObject this component is attached to
        """
        self.game_object = game_object
    
    def is_enabled(self) -> bool:
        """Check if the component is enabled.
        
        Returns:
            True if enabled, False otherwise
        """
        return self.enabled
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the component.
        
        Args:
            enabled: Whether to enable the component
        """
        self.enabled = enabled
    
    @abstractmethod
    def initialize(self):
        """Initialize the script component."""
        pass
    
    def update(self, delta_time: float):
        """Update the script component.
        
        Args:
            delta_time: Time since last update
        """
        if not self.enabled:
            return
        
        try:
            self._on_update(delta_time)
        except Exception as e:
            self.logger.error(f"Error in script update: {e}")
    
    def shutdown(self):
        """Shutdown the script component."""
        try:
            self._on_shutdown()
        except Exception as e:
            self.logger.error(f"Error in script shutdown: {e}")
    
    def on_script_reloaded(self):
        """Called when the script is hot-reloaded."""
        try:
            self._on_script_reloaded()
        except Exception as e:
            self.logger.error(f"Error in script reload: {e}")
    
    def _on_update(self, delta_time: float):
        """Override this method to implement update logic.
        
        Args:
            delta_time: Time since last update
        """
        pass
    
    def _on_shutdown(self):
        """Override this method to implement shutdown logic."""
        pass
    
    def _on_script_reloaded(self):
        """Override this method to handle script reloading."""
        pass
