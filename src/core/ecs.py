"""
Entity-Component-System (ECS) architecture for Nexlify.

This module provides the core ECS implementation including:
- Entity management
- Component storage and retrieval
- System processing
- World/Scene management
"""

import uuid
import logging
from typing import Dict, List, Set, Any, Optional, Type, TypeVar, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from ..utils.logger import get_logger

T = TypeVar('T')


@dataclass
class Entity:
    """Represents a game entity with unique ID and name."""
    id: str
    name: str
    active: bool = True
    tags: Set[str] = field(default_factory=set)
    created_at: float = field(default_factory=lambda: __import__('time').time())


class Component:
    """Base class for all components."""
    
    def __init__(self):
        self.entity_id: Optional[str] = None
        self.enabled: bool = True
    
    def on_attach(self, entity_id: str):
        """Called when component is attached to an entity."""
        self.entity_id = entity_id
    
    def on_detach(self):
        """Called when component is detached from an entity."""
        self.entity_id = None


class System(ABC):
    """Base class for all systems."""
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = True
        self.priority = 0
        self.logger = get_logger(f"{__name__}.{name}")
    
    @abstractmethod
    def update(self, delta_time: float):
        """Update the system for one frame."""
        pass
    
    def on_entity_added(self, entity_id: str):
        """Called when an entity is added to the system."""
        pass
    
    def on_entity_removed(self, entity_id: str):
        """Called when an entity is removed from the system."""
        pass


class EntityManager:
    """Manages entity creation, destruction, and lifecycle."""
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.next_entity_id = 1
        self.logger = get_logger(__name__)
    
    def create_entity(self, name: str, tags: Optional[Set[str]] = None) -> str:
        """Create a new entity.
        
        Args:
            name: Entity name
            tags: Optional set of tags
            
        Returns:
            Entity ID
        """
        entity_id = str(uuid.uuid4())
        entity = Entity(
            id=entity_id,
            name=name,
            tags=tags or set()
        )
        
        self.entities[entity_id] = entity
        self.logger.debug(f"Created entity: {name} (ID: {entity_id})")
        
        return entity_id
    
    def destroy_entity(self, entity_id: str) -> bool:
        """Destroy an entity.
        
        Args:
            entity_id: ID of entity to destroy
            
        Returns:
            True if entity was destroyed, False otherwise
        """
        if entity_id in self.entities:
            entity = self.entities[entity_id]
            self.logger.debug(f"Destroyed entity: {entity.name} (ID: {entity_id})")
            del self.entities[entity_id]
            return True
        return False
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Entity object or None if not found
        """
        return self.entities.get(entity_id)
    
    def get_entities_by_tag(self, tag: str) -> List[str]:
        """Get all entity IDs with a specific tag.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of entity IDs
        """
        return [
            entity_id for entity_id, entity in self.entities.items()
            if tag in entity.tags
        ]
    
    def get_entities_by_name(self, name: str) -> List[str]:
        """Get all entity IDs with a specific name.
        
        Args:
            name: Entity name to search for
            
        Returns:
            List of entity IDs
        """
        return [
            entity_id for entity_id, entity in self.entities.items()
            if entity.name == name
        ]
    
    def get_entity_count(self) -> int:
        """Get total number of entities.
        
        Returns:
            Entity count
        """
        return len(self.entities)
    
    def clear_all(self):
        """Clear all entities."""
        self.entities.clear()
        self.logger.info("Cleared all entities")


class ComponentManager:
    """Manages component storage and retrieval."""
    
    def __init__(self):
        self.components: Dict[Type[Component], Dict[str, Component]] = {}
        self.entity_components: Dict[str, Set[Type[Component]]] = {}
        self.logger = get_logger(__name__)
    
    def add_component(self, entity_id: str, component: Component) -> bool:
        """Add a component to an entity.
        
        Args:
            entity_id: Entity ID
            component: Component to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            component_type = type(component)
            
            # Initialize component type storage if needed
            if component_type not in self.components:
                self.components[component_type] = {}
            
            # Add component
            self.components[component_type][entity_id] = component
            component.on_attach(entity_id)
            
            # Track entity's components
            if entity_id not in self.entity_components:
                self.entity_components[entity_id] = set()
            self.entity_components[entity_id].add(component_type)
            
            self.logger.debug(f"Added {component_type.__name__} to entity {entity_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add component: {e}")
            return False
    
    def remove_component(self, entity_id: str, component_type: Type[T]) -> bool:
        """Remove a component from an entity.
        
        Args:
            entity_id: Entity ID
            component_type: Type of component to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if component_type in self.components and entity_id in self.components[component_type]:
                component = self.components[component_type][entity_id]
                component.on_detach()
                
                del self.components[component_type][entity_id]
                
                # Remove from entity tracking
                if entity_id in self.entity_components:
                    self.entity_components[entity_id].discard(component_type)
                
                self.logger.debug(f"Removed {component_type.__name__} from entity {entity_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove component: {e}")
            return False
    
    def get_component(self, entity_id: str, component_type: Type[T]) -> Optional[T]:
        """Get a component from an entity.
        
        Args:
            entity_id: Entity ID
            component_type: Type of component to get
            
        Returns:
            Component instance or None if not found
        """
        if component_type in self.components:
            return self.components[component_type].get(entity_id)
        return None
    
    def get_entities_with_component(self, component_type: Type[Component]) -> List[str]:
        """Get all entity IDs that have a specific component.
        
        Args:
            component_type: Component type to search for
            
        Returns:
            List of entity IDs
        """
        if component_type in self.components:
            return list(self.components[component_type].keys())
        return []
    
    def get_entity_components(self, entity_id: str) -> List[Component]:
        """Get all components for an entity.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            List of components
        """
        components = []
        if entity_id in self.entity_components:
            for component_type in self.entity_components[entity_id]:
                if component_type in self.components and entity_id in self.components[component_type]:
                    components.append(self.components[component_type][entity_id])
        return components
    
    def clear_entity_components(self, entity_id: str):
        """Clear all components for an entity.
        
        Args:
            entity_id: Entity ID
        """
        if entity_id in self.entity_components:
            for component_type in self.entity_components[entity_id]:
                if component_type in self.components and entity_id in self.components[component_type]:
                    component = self.components[component_type][entity_id]
                    component.on_detach()
                    del self.components[component_type][entity_id]
            
            del self.entity_components[entity_id]


class SystemManager:
    """Manages system execution and entity-system relationships."""
    
    def __init__(self):
        self.systems: List[System] = []
        self.system_entities: Dict[str, Set[str]] = {}
        self.logger = get_logger(__name__)
    
    def add_system(self, system: System):
        """Add a system to the manager.
        
        Args:
            system: System to add
        """
        self.systems.append(system)
        self.system_entities[system.name] = set()
        
        # Sort systems by priority
        self.systems.sort(key=lambda s: s.priority)
        
        self.logger.debug(f"Added system: {system.name}")
    
    def remove_system(self, system_name: str) -> bool:
        """Remove a system from the manager.
        
        Args:
            system_name: Name of system to remove
            
        Returns:
            True if successful, False otherwise
        """
        for i, system in enumerate(self.systems):
            if system.name == system_name:
                del self.systems[i]
                if system_name in self.system_entities:
                    del self.system_entities[system_name]
                
                self.logger.debug(f"Removed system: {system_name}")
                return True
        
        return False
    
    def update_all(self, delta_time: float):
        """Update all systems.
        
        Args:
            delta_time: Time since last update
        """
        for system in self.systems:
            if system.enabled:
                try:
                    system.update(delta_time)
                except Exception as e:
                    self.logger.error(f"Error updating system {system.name}: {e}")
    
    def get_system(self, system_name: str) -> Optional[System]:
        """Get a system by name.
        
        Args:
            system_name: Name of system
            
        Returns:
            System instance or None if not found
        """
        for system in self.systems:
            if system.name == system_name:
                return system
        return None
    
    def get_system_count(self) -> int:
        """Get total number of systems.
        
        Returns:
            System count
        """
        return len(self.systems)
