"""
GameObject system for Nexlify Engine.

This module implements a Unity-like GameObject system with:
- Hierarchical object structure (parent-child relationships)
- Component-based architecture
- Transform system for positioning, rotation, and scaling
- Scene management integration
"""

from typing import List, Optional, Dict, Any, Type, TYPE_CHECKING
from dataclasses import dataclass, field
import uuid

if TYPE_CHECKING:
    from .component import Component

@dataclass
class Transform:
    """Represents the position, rotation, and scale of a GameObject."""
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    rotation: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    scale: List[float] = field(default_factory=lambda: [1.0, 1.0, 1.0])

    def set_position(self, x: float, y: float, z: float) -> None:
        """Set the position of the transform."""
        self.position = [x, y, z]

    def set_rotation(self, x: float, y: float, z: float) -> None:
        """Set the rotation of the transform in degrees."""
        self.rotation = [x, y, z]

    def set_scale(self, x: float, y: float, z: float) -> None:
        """Set the scale of the transform."""
        self.scale = [x, y, z]

    def translate(self, x: float, y: float, z: float) -> None:
        """Translate the transform by the given offset."""
        self.position[0] += x
        self.position[1] += y
        self.position[2] += z

    def rotate(self, x: float, y: float, z: float) -> None:
        """Rotate the transform by the given angles."""
        self.rotation[0] += x
        self.rotation[1] += y
        self.rotation[2] += z

    def scale_by(self, x: float, y: float, z: float) -> None:
        """Scale the transform by the given factors."""
        self.scale[0] *= x
        self.scale[1] *= y
        self.scale[2] *= z

    def get_matrix(self) -> List[List[float]]:
        """Get the transformation matrix (simplified 4x4 matrix)."""
        # This is a simplified matrix - in a real engine you'd use proper math libraries
        return [
            [self.scale[0], 0, 0, self.position[0]],
            [0, self.scale[1], 0, self.position[1]],
            [0, 0, self.scale[2], self.position[2]],
            [0, 0, 0, 1]
        ]

    def serialize(self) -> Dict[str, Any]:
        """Serialize the transform to a dictionary."""
        return {
            'position': self.position,
            'rotation': self.rotation,
            'scale': self.scale
        }

    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the transform from a dictionary."""
        self.position = data.get('position', self.position)
        self.rotation = data.get('rotation', self.rotation)
        self.scale = data.get('scale', self.scale)


class GameObject:
    """Represents a game object in the scene with components and hierarchy."""
    
    def __init__(self, name: str = "GameObject"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.transform = Transform()
        self.components: List['Component'] = []
        self.children: List['GameObject'] = []
        self.parent: Optional['GameObject'] = None
        self.active = True
        self.tag = ""
        self.layer = 0

    def add_component(self, component: 'Component') -> 'Component':
        """Add a component to this GameObject."""
        if component.game_object:
            raise ValueError(f"Component {component.name} is already attached to another GameObject")
        
        component.game_object = self
        self.components.append(component)
        component._on_initialize()
        return component

    def remove_component(self, component: 'Component') -> bool:
        """Remove a component from this GameObject."""
        if component in self.components:
            component._on_destroy()
            component.game_object = None
            self.components.remove(component)
            return True
        return False

    def get_component(self, component_type: Type['Component']) -> Optional['Component']:
        """Get a component of the specified type."""
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def get_components(self, component_type: Type['Component']) -> List['Component']:
        """Get all components of the specified type."""
        return [comp for comp in self.components if isinstance(comp, component_type)]

    def has_component(self, component_type: Type['Component']) -> bool:
        """Check if this GameObject has a component of the specified type."""
        return self.get_component(component_type) is not None

    def add_child(self, child: 'GameObject') -> None:
        """Add a child GameObject to this GameObject."""
        if child.parent:
            child.parent.remove_child(child)
        
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: 'GameObject') -> bool:
        """Remove a child GameObject from this GameObject."""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            return True
        return False

    def get_child(self, name: str) -> Optional['GameObject']:
        """Get a child GameObject by name."""
        for child in self.children:
            if child.name == name:
                return child
        return None

    def get_children(self) -> List['GameObject']:
        """Get all children of this GameObject."""
        return self.children.copy()

    def set_parent(self, parent: Optional['GameObject']) -> None:
        """Set the parent of this GameObject."""
        if self.parent:
            self.parent.remove_child(self)
        
        if parent:
            parent.add_child(self)

    def get_root(self) -> 'GameObject':
        """Get the root GameObject in the hierarchy."""
        current = self
        while current.parent:
            current = current.parent
        return current

    def get_depth(self) -> int:
        """Get the depth of this GameObject in the hierarchy."""
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth

    def set_active(self, active: bool) -> None:
        """Set whether this GameObject is active."""
        self.active = active

    def is_active(self) -> bool:
        """Check if this GameObject is active."""
        return self.active and (self.parent is None or self.parent.is_active())

    def set_tag(self, tag: str) -> None:
        """Set the tag of this GameObject."""
        self.tag = tag

    def get_tag(self) -> str:
        """Get the tag of this GameObject."""
        return self.tag

    def set_layer(self, layer: int) -> None:
        """Set the layer of this GameObject."""
        self.layer = layer

    def get_layer(self) -> int:
        """Get the layer of this GameObject."""
        return self.layer

    def update(self, delta_time: float) -> None:
        """Update this GameObject and all its components."""
        if not self.is_active():
            return
        
        for component in self.components:
            if component.is_enabled():
                component._on_update(delta_time)
        
        for child in self.children:
            child.update(delta_time)

    def render(self) -> None:
        """Render this GameObject and all its components."""
        if not self.is_active():
            return
        
        for component in self.components:
            if component.is_enabled():
                component._on_render()
        
        for child in self.children:
            child.render()

    def destroy(self) -> None:
        """Destroy this GameObject and all its children."""
        # Destroy all components
        for component in self.components:
            component._on_destroy()
        
        # Destroy all children
        for child in self.children:
            child.destroy()
        
        # Remove from parent
        if self.parent:
            self.parent.remove_child(self)
        
        # Clear references
        self.components.clear()
        self.children.clear()
        self.parent = None

    def find_child_by_name(self, name: str, recursive: bool = True) -> Optional['GameObject']:
        """Find a child GameObject by name, optionally searching recursively."""
        # Check direct children first
        for child in self.children:
            if child.name == name:
                return child
        
        # Recursive search if requested
        if recursive:
            for child in self.children:
                result = child.find_child_by_name(name, recursive=True)
                if result:
                    return result
        
        return None

    def find_children_by_tag(self, tag: str) -> List['GameObject']:
        """Find all children with the specified tag."""
        result = []
        for child in self.children:
            if child.tag == tag:
                result.append(child)
            result.extend(child.find_children_by_tag(tag))
        return result

    def serialize(self) -> Dict[str, Any]:
        """Serialize this GameObject to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'transform': self.transform.serialize(),
            'components': [comp.serialize() for comp in self.components],
            'children': [child.serialize() for child in self.children],
            'active': self.active,
            'tag': self.tag,
            'layer': self.layer
        }

    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize this GameObject from a dictionary."""
        self.id = data.get('id', self.id)
        self.name = data.get('name', self.name)
        self.active = data.get('active', True)
        self.tag = data.get('tag', "")
        self.layer = data.get('layer', 0)
        
        if 'transform' in data:
            self.transform.deserialize(data['transform'])
        
        # Note: Components and children would need special handling
        # as they require the actual Component classes to be available

    def __str__(self) -> str:
        """String representation of the GameObject."""
        return f"GameObject('{self.name}', id={self.id[:8]}, active={self.active})"

    def __repr__(self) -> str:
        """Detailed string representation of the GameObject."""
        return f"GameObject(name='{self.name}', id='{self.id}', components={len(self.components)}, children={len(self.children)})"
