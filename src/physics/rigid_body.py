"""
Rigid Body for Nexlify Physics Engine.

This module provides rigid body physics simulation including
mass, velocity, forces, and collision response.
"""

import logging
import math
from typing import List, Optional, Tuple
from dataclasses import dataclass

from ..utils.logger import get_logger


@dataclass
class PhysicsMaterial:
    """Physics material properties."""
    density: float = 1.0
    friction: float = 0.5
    restitution: float = 0.3
    name: str = "default"


class RigidBody:
    """Rigid body for physics simulation."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Position and orientation
        self.position: List[float] = [0.0, 0.0, 0.0]
        self.rotation: List[float] = [0.0, 0.0, 0.0]  # Euler angles
        self.scale: List[float] = [1.0, 1.0, 1.0]
        
        # Linear motion
        self.linear_velocity: List[float] = [0.0, 0.0, 0.0]
        self.linear_acceleration: List[float] = [0.0, 0.0, 0.0]
        self.linear_damping: float = 0.1
        
        # Angular motion
        self.angular_velocity: List[float] = [0.0, 0.0, 0.0]
        self.angular_acceleration: List[float] = [0.0, 0.0, 0.0]
        self.angular_damping: float = 0.1
        
        # Mass and inertia
        self.mass: float = 1.0
        self.inverse_mass: float = 1.0
        self.inertia_tensor: List[List[float]] = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        self.inverse_inertia_tensor: List[List[float]] = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        
        # Forces and torques
        self.accumulated_force: List[float] = [0.0, 0.0, 0.0]
        self.accumulated_torque: List[float] = [0.0, 0.0, 0.0]
        
        # State
        self.is_static: bool = False
        self.is_sleeping: bool = False
        self.sleep_threshold: float = 0.1
        self.sleep_time: float = 0.0
        
        # Material
        self.material: PhysicsMaterial = PhysicsMaterial()
        
        # Collision
        self.collision_enabled: bool = True
        self.trigger: bool = False
        
    def set_position(self, position: List[float]):
        """Set the position of the rigid body.
        
        Args:
            position: Position [x, y, z]
        """
        self.position = position.copy()
        self.wake_up()
    
    def get_position(self) -> List[float]:
        """Get the position of the rigid body.
        
        Returns:
            Position [x, y, z]
        """
        return self.position.copy()
    
    def set_rotation(self, rotation: List[float]):
        """Set the rotation of the rigid body.
        
        Args:
            rotation: Euler angles [x, y, z] in radians
        """
        self.rotation = rotation.copy()
        self.wake_up()
    
    def get_rotation(self) -> List[float]:
        """Get the rotation of the rigid body.
        
        Returns:
            Euler angles [x, y, z] in radians
        """
        return self.rotation.copy()
    
    def set_scale(self, scale: List[float]):
        """Set the scale of the rigid body.
        
        Args:
            scale: Scale [x, y, z]
        """
        self.scale = scale.copy()
        self._update_inertia_tensor()
        self.wake_up()
    
    def get_scale(self) -> List[float]:
        """Get the scale of the rigid body.
        
        Returns:
            Scale [x, y, z]
        """
        return self.scale.copy()
    
    def set_mass(self, mass: float):
        """Set the mass of the rigid body.
        
        Args:
            mass: Mass value
        """
        if mass <= 0:
            self.mass = 0.0
            self.inverse_mass = 0.0
            self.is_static = True
        else:
            self.mass = mass
            self.inverse_mass = 1.0 / mass
            self.is_static = False
        
        self._update_inertia_tensor()
        self.wake_up()
    
    def get_mass(self) -> float:
        """Get the mass of the rigid body.
        
        Returns:
            Mass value
        """
        return self.mass
    
    def set_linear_velocity(self, velocity: List[float]):
        """Set the linear velocity.
        
        Args:
            velocity: Linear velocity [x, y, z]
        """
        self.linear_velocity = velocity.copy()
        self.wake_up()
    
    def get_linear_velocity(self) -> List[float]:
        """Get the linear velocity.
        
        Returns:
            Linear velocity [x, y, z]
        """
        return self.linear_velocity.copy()
    
    def set_angular_velocity(self, velocity: List[float]):
        """Set the angular velocity.
        
        Args:
            velocity: Angular velocity [x, y, z]
        """
        self.angular_velocity = velocity.copy()
        self.wake_up()
    
    def get_angular_velocity(self) -> List[float]:
        """Get the angular velocity.
        
        Returns:
            Angular velocity [x, y, z]
        """
        return self.angular_velocity.copy()
    
    def add_force(self, force: List[float], point: Optional[List[float]] = None):
        """Add a force to the rigid body.
        
        Args:
            force: Force vector [x, y, z]
            point: Point of application (optional, defaults to center of mass)
        """
        if self.is_static or self.is_sleeping:
            return
        
        # Add linear force
        for i in range(3):
            self.accumulated_force[i] += force[i]
        
        # Add torque if force is applied at a point
        if point:
            # Calculate torque = r × F
            r = [point[i] - self.position[i] for i in range(3)]
            torque = self._cross_product(r, force)
            for i in range(3):
                self.accumulated_torque[i] += torque[i]
        
        self.wake_up()
    
    def add_torque(self, torque: List[float]):
        """Add a torque to the rigid body.
        
        Args:
            torque: Torque vector [x, y, z]
        """
        if self.is_static or self.is_sleeping:
            return
        
        for i in range(3):
            self.accumulated_torque[i] += torque[i]
        
        self.wake_up()
    
    def add_impulse(self, impulse: List[float], point: Optional[List[float]] = None):
        """Add an impulse to the rigid body.
        
        Args:
            impulse: Impulse vector [x, y, z]
            point: Point of application (optional)
        """
        if self.is_static or self.is_sleeping:
            return
        
        # Apply linear impulse
        for i in range(3):
            self.linear_velocity[i] += impulse[i] * self.inverse_mass
        
        # Apply angular impulse if applied at a point
        if point:
            r = [point[i] - self.position[i] for i in range(3)]
            angular_impulse = self._cross_product(r, impulse)
            for i in range(3):
                self.angular_velocity[i] += angular_impulse[i] * self.inverse_inertia_tensor[i][i]
        
        self.wake_up()
    
    def add_angular_impulse(self, impulse: List[float]):
        """Add an angular impulse to the rigid body.
        
        Args:
            impulse: Angular impulse vector [x, y, z]
        """
        if self.is_static or self.is_sleeping:
            return
        
        for i in range(3):
            self.angular_velocity[i] += impulse[i] * self.inverse_inertia_tensor[i][i]
        
        self.wake_up()
    
    def set_static(self, is_static: bool):
        """Set whether the rigid body is static.
        
        Args:
            is_static: Whether the body is static
        """
        self.is_static = is_static
        if is_static:
            self.mass = 0.0
            self.inverse_mass = 0.0
            self.linear_velocity = [0.0, 0.0, 0.0]
            self.angular_velocity = [0.0, 0.0, 0.0]
        else:
            if self.mass == 0.0:
                self.mass = 1.0
                self.inverse_mass = 1.0
        
        self.wake_up()
    
    def is_static_body(self) -> bool:
        """Check if the rigid body is static.
        
        Returns:
            True if static, False otherwise
        """
        return self.is_static
    
    def set_sleeping(self, sleeping: bool):
        """Set the sleeping state of the rigid body.
        
        Args:
            sleeping: Whether the body is sleeping
        """
        self.is_sleeping = sleeping
        if sleeping:
            self.linear_velocity = [0.0, 0.0, 0.0]
            self.angular_velocity = [0.0, 0.0, 0.0]
            self.accumulated_force = [0.0, 0.0, 0.0]
            self.accumulated_torque = [0.0, 0.0, 0.0]
    
    def is_sleeping(self) -> bool:
        """Check if the rigid body is sleeping.
        
        Returns:
            True if sleeping, False otherwise
        """
        return self.is_sleeping
    
    def wake_up(self):
        """Wake up the rigid body."""
        self.is_sleeping = False
        self.sleep_time = 0.0
    
    def get_linear_velocity_magnitude(self) -> float:
        """Get the magnitude of linear velocity.
        
        Returns:
            Linear velocity magnitude
        """
        return math.sqrt(sum(v * v for v in self.linear_velocity))
    
    def get_angular_velocity_magnitude(self) -> float:
        """Get the magnitude of angular velocity.
        
        Returns:
            Angular velocity magnitude
        """
        return math.sqrt(sum(v * v for v in self.angular_velocity))
    
    def should_sleep(self) -> bool:
        """Check if the rigid body should go to sleep.
        
        Returns:
            True if should sleep, False otherwise
        """
        if self.is_static:
            return True
        
        linear_speed = self.get_linear_velocity_magnitude()
        angular_speed = self.get_angular_velocity_magnitude()
        
        return linear_speed < self.sleep_threshold and angular_speed < self.sleep_threshold
    
    def update_sleep_time(self, delta_time: float):
        """Update the sleep time.
        
        Args:
            delta_time: Time step
        """
        if self.should_sleep():
            self.sleep_time += delta_time
        else:
            self.sleep_time = 0.0
    
    def set_material(self, material: PhysicsMaterial):
        """Set the physics material.
        
        Args:
            material: Physics material
        """
        self.material = material
        self._update_inertia_tensor()
    
    def get_material(self) -> PhysicsMaterial:
        """Get the physics material.
        
        Returns:
            Physics material
        """
        return self.material
    
    def set_collision_enabled(self, enabled: bool):
        """Enable or disable collision detection.
        
        Args:
            enabled: Whether collision detection is enabled
        """
        self.collision_enabled = enabled
    
    def is_collision_enabled(self) -> bool:
        """Check if collision detection is enabled.
        
        Returns:
            True if enabled, False otherwise
        """
        return self.collision_enabled
    
    def set_trigger(self, is_trigger: bool):
        """Set whether this is a trigger collider.
        
        Args:
            is_trigger: Whether this is a trigger
        """
        self.trigger = is_trigger
    
    def is_trigger(self) -> bool:
        """Check if this is a trigger collider.
        
        Returns:
            True if trigger, False otherwise
        """
        return self.trigger
    
    def _update_inertia_tensor(self):
        """Update the inertia tensor based on mass and scale."""
        # Simple box inertia tensor
        # For a box with dimensions scale[0] x scale[1] x scale[2]
        width, height, depth = self.scale
        
        # Calculate moments of inertia for a box
        Ixx = self.mass * (height * height + depth * depth) / 12.0
        Iyy = self.mass * (width * width + depth * depth) / 12.0
        Izz = self.mass * (width * width + height * height) / 12.0
        
        self.inertia_tensor = [
            [Ixx, 0.0, 0.0],
            [0.0, Iyy, 0.0],
            [0.0, 0.0, Izz]
        ]
        
        # Calculate inverse inertia tensor
        if self.mass > 0:
            self.inverse_inertia_tensor = [
                [1.0 / Ixx, 0.0, 0.0],
                [0.0, 1.0 / Iyy, 0.0],
                [0.0, 0.0, 1.0 / Izz]
            ]
        else:
            self.inverse_inertia_tensor = [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]
            ]
    
    def _cross_product(self, a: List[float], b: List[float]) -> List[float]:
        """Calculate cross product of two 3D vectors.
        
        Args:
            a: First vector
            b: Second vector
            
        Returns:
            Cross product vector
        """
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]
        ]
