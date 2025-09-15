"""
Basic components for Nexlify Engine.

This module provides essential components that can be attached to GameObjects:
- MeshRenderer: Renders 3D meshes
- Light: Provides lighting in the scene
- Camera: Handles viewport rendering and camera controls
- Collider: Basic collision detection
"""

from typing import List, Optional, Dict, Any, TYPE_CHECKING
from .component import Component

if TYPE_CHECKING:
    from .game_object import GameObject

class MeshRenderer(Component):
    """Component for rendering 3D meshes."""
    
    def __init__(self, mesh_path: str = "", material_path: str = ""):
        super().__init__("MeshRenderer")
        self.mesh_path = mesh_path
        self.material_path = material_path
        self.visible = True
        self.cast_shadows = True
        self.receive_shadows = True
        self.sorting_order = 0

    def _on_initialize(self) -> None:
        """Initialize the mesh renderer."""
        pass

    def _on_update(self, delta_time: float) -> None:
        """Update the mesh renderer."""
        pass

    def _on_render(self) -> None:
        """Render the mesh."""
        if not self.visible:
            return
        # In a real engine, this would call the rendering system
        pass

    def set_mesh(self, mesh_path: str) -> None:
        """Set the mesh to render."""
        self.mesh_path = mesh_path

    def set_material(self, material_path: str) -> None:
        """Set the material to use for rendering."""
        self.material_path = material_path

    def set_visible(self, visible: bool) -> None:
        """Set whether the mesh is visible."""
        self.visible = visible

    def set_cast_shadows(self, cast_shadows: bool) -> None:
        """Set whether the mesh casts shadows."""
        self.cast_shadows = cast_shadows

    def set_receive_shadows(self, receive_shadows: bool) -> None:
        """Set whether the mesh receives shadows."""
        self.receive_shadows = receive_shadows

    def serialize(self) -> Dict[str, Any]:
        """Serialize the mesh renderer."""
        data = super().serialize()
        data.update({
            'mesh_path': self.mesh_path,
            'material_path': self.material_path,
            'visible': self.visible,
            'cast_shadows': self.cast_shadows,
            'receive_shadows': self.receive_shadows,
            'sorting_order': self.sorting_order
        })
        return data

    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the mesh renderer."""
        super().deserialize(data)
        self.mesh_path = data.get('mesh_path', self.mesh_path)
        self.material_path = data.get('material_path', self.material_path)
        self.visible = data.get('visible', True)
        self.cast_shadows = data.get('cast_shadows', True)
        self.receive_shadows = data.get('receive_shadows', True)
        self.sorting_order = data.get('sorting_order', 0)


class Light(Component):
    """Component for lighting in the scene."""
    
    def __init__(self, light_type: str = "Point", color: List[float] = None, intensity: float = 1.0):
        super().__init__("Light")
        self.light_type = light_type  # Point, Directional, Spot, Area
        self.color = color or [1.0, 1.0, 1.0]  # RGB
        self.intensity = intensity
        self.range = 10.0
        self.spot_angle = 45.0
        self.cast_shadows = True
        self.enabled = True

    def _on_initialize(self) -> None:
        """Initialize the light."""
        pass

    def _on_update(self, delta_time: float) -> None:
        """Update the light."""
        pass

    def _on_render(self) -> None:
        """Render the light (usually just for debugging)."""
        pass

    def set_color(self, r: float, g: float, b: float) -> None:
        """Set the light color."""
        self.color = [r, g, b]

    def set_intensity(self, intensity: float) -> None:
        """Set the light intensity."""
        self.intensity = intensity

    def set_range(self, range_value: float) -> None:
        """Set the light range (for point and spot lights)."""
        self.range = range_value

    def set_spot_angle(self, angle: float) -> None:
        """Set the spot light angle."""
        self.spot_angle = angle

    def set_cast_shadows(self, cast_shadows: bool) -> None:
        """Set whether the light casts shadows."""
        self.cast_shadows = cast_shadows

    def serialize(self) -> Dict[str, Any]:
        """Serialize the light."""
        data = super().serialize()
        data.update({
            'light_type': self.light_type,
            'color': self.color,
            'intensity': self.intensity,
            'range': self.range,
            'spot_angle': self.spot_angle,
            'cast_shadows': self.cast_shadows
        })
        return data

    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the light."""
        super().deserialize(data)
        self.light_type = data.get('light_type', self.light_type)
        self.color = data.get('color', self.color)
        self.intensity = data.get('intensity', self.intensity)
        self.range = data.get('range', self.range)
        self.spot_angle = data.get('spot_angle', self.spot_angle)
        self.cast_shadows = data.get('cast_shadows', self.cast_shadows)


class Camera(Component):
    """Component for camera functionality."""
    
    def __init__(self, fov: float = 60.0, near_clip: float = 0.1, far_clip: float = 1000.0):
        super().__init__("Camera")
        self.fov = fov  # Field of view in degrees
        self.near_clip = near_clip
        self.far_clip = far_clip
        self.aspect_ratio = 16.0 / 9.0
        self.clear_color = [0.2, 0.3, 0.4, 1.0]
        self.clear_flags = "Skybox"  # Skybox, SolidColor, DepthOnly, Nothing
        self.culling_mask = 0xFFFFFFFF  # All layers
        self.depth = -1  # Camera depth for rendering order

    def _on_initialize(self) -> None:
        """Initialize the camera."""
        pass

    def _on_update(self, delta_time: float) -> None:
        """Update the camera."""
        pass

    def _on_render(self) -> None:
        """Render the camera view."""
        pass

    def set_fov(self, fov: float) -> None:
        """Set the field of view."""
        self.fov = fov

    def set_near_clip(self, near_clip: float) -> None:
        """Set the near clipping plane."""
        self.near_clip = near_clip

    def set_far_clip(self, far_clip: float) -> None:
        """Set the far clipping plane."""
        self.far_clip = far_clip

    def set_aspect_ratio(self, aspect_ratio: float) -> None:
        """Set the aspect ratio."""
        self.aspect_ratio = aspect_ratio

    def set_clear_color(self, r: float, g: float, b: float, a: float = 1.0) -> None:
        """Set the clear color."""
        self.clear_color = [r, g, b, a]

    def set_clear_flags(self, clear_flags: str) -> None:
        """Set the clear flags."""
        self.clear_flags = clear_flags

    def set_culling_mask(self, culling_mask: int) -> None:
        """Set the culling mask."""
        self.culling_mask = culling_mask

    def set_depth(self, depth: int) -> None:
        """Set the camera depth."""
        self.depth = depth

    def get_view_matrix(self) -> List[List[float]]:
        """Get the view matrix for this camera."""
        if not self.game_object:
            return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        
        # In a real engine, this would calculate the proper view matrix
        # based on the camera's position and rotation
        return self.game_object.transform.get_matrix()

    def get_projection_matrix(self) -> List[List[float]]:
        """Get the projection matrix for this camera."""
        # In a real engine, this would calculate the proper projection matrix
        # based on FOV, aspect ratio, and clip planes
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def serialize(self) -> Dict[str, Any]:
        """Serialize the camera."""
        data = super().serialize()
        data.update({
            'fov': self.fov,
            'near_clip': self.near_clip,
            'far_clip': self.far_clip,
            'aspect_ratio': self.aspect_ratio,
            'clear_color': self.clear_color,
            'clear_flags': self.clear_flags,
            'culling_mask': self.culling_mask,
            'depth': self.depth
        })
        return data

    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the camera."""
        super().deserialize(data)
        self.fov = data.get('fov', self.fov)
        self.near_clip = data.get('near_clip', self.near_clip)
        self.far_clip = data.get('far_clip', self.far_clip)
        self.aspect_ratio = data.get('aspect_ratio', self.aspect_ratio)
        self.clear_color = data.get('clear_color', self.clear_color)
        self.clear_flags = data.get('clear_flags', self.clear_flags)
        self.culling_mask = data.get('culling_mask', self.culling_mask)
        self.depth = data.get('depth', self.depth)


class Collider(Component):
    """Base component for collision detection."""
    
    def __init__(self, is_trigger: bool = False, material: str = ""):
        super().__init__("Collider")
        self.is_trigger = is_trigger
        self.material = material
        self.enabled = True
        self.contact_callbacks = []

    def _on_initialize(self) -> None:
        """Initialize the collider."""
        pass

    def _on_update(self, delta_time: float) -> None:
        """Update the collider."""
        pass

    def _on_render(self) -> None:
        """Render the collider (usually just for debugging)."""
        pass

    def set_trigger(self, is_trigger: bool) -> None:
        """Set whether this collider is a trigger."""
        self.is_trigger = is_trigger

    def set_material(self, material: str) -> None:
        """Set the physics material."""
        self.material = material

    def add_contact_callback(self, callback) -> None:
        """Add a contact callback function."""
        if callback not in self.contact_callbacks:
            self.contact_callbacks.append(callback)

    def remove_contact_callback(self, callback) -> None:
        """Remove a contact callback function."""
        if callback in self.contact_callbacks:
            self.contact_callbacks.remove(callback)

    def on_trigger_enter(self, other: 'Collider') -> None:
        """Called when another collider enters this trigger."""
        pass

    def on_trigger_exit(self, other: 'Collider') -> None:
        """Called when another collider exits this trigger."""
        pass

    def on_collision_enter(self, other: 'Collider') -> None:
        """Called when this collider collides with another."""
        pass

    def on_collision_exit(self, other: 'Collider') -> None:
        """Called when this collider stops colliding with another."""
        pass

    def serialize(self) -> Dict[str, Any]:
        """Serialize the collider."""
        data = super().serialize()
        data.update({
            'is_trigger': self.is_trigger,
            'material': self.material
        })
        return data

    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the collider."""
        super().deserialize(data)
        self.is_trigger = data.get('is_trigger', False)
        self.material = data.get('material', "")
