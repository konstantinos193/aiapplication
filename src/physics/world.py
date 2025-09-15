"""
Physics World for Nexlify Engine.

This module manages the physics simulation world including
rigid bodies, constraints, and collision detection.
"""

import logging
import time
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass

from .rigid_body import RigidBody
from .config import PhysicsConfig
from ..utils.logger import get_logger


@dataclass
class Constraint:
    """Physics constraint."""
    body_a: RigidBody
    body_b: RigidBody
    constraint_type: str
    parameters: Dict[str, Any]


class PhysicsWorld:
    """Physics simulation world."""
    
    def __init__(self, config: PhysicsConfig):
        self.config = config
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # World properties
        self.gravity: List[float] = [0.0, -9.81, 0.0]
        self.time_scale: float = 1.0
        
        # Rigid bodies
        self.rigid_bodies: List[RigidBody] = []
        self.static_bodies: List[RigidBody] = []
        self.dynamic_bodies: List[RigidBody] = []
        
        # Constraints
        self.constraints: List[Constraint] = []
        
        # Performance tracking
        self.update_count = 0
        self.last_update_time = time.time()
        
    def initialize(self) -> bool:
        """Initialize the physics world.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing physics world...")
            
            # Set gravity from config
            if self.config.gravity:
                self.gravity = self.config.gravity.copy()
            
            self.is_initialized = True
            self.logger.info("✅ Physics world initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize physics world: {e}")
            return False
    
    def set_gravity(self, gravity: List[float]):
        """Set the gravity vector.
        
        Args:
            gravity: Gravity vector [x, y, z]
        """
        self.gravity = gravity.copy()
        self.logger.debug(f"Set gravity: {gravity}")
    
    def get_gravity(self) -> List[float]:
        """Get the gravity vector.
        
        Returns:
            Gravity vector [x, y, z]
        """
        return self.gravity.copy()
    
    def set_time_scale(self, time_scale: float):
        """Set the time scale for physics simulation.
        
        Args:
            time_scale: Time scale factor
        """
        self.time_scale = max(0.0, time_scale)
        self.logger.debug(f"Set time scale: {time_scale}")
    
    def get_time_scale(self) -> float:
        """Get the time scale.
        
        Returns:
            Time scale factor
        """
        return self.time_scale
    
    def add_rigid_body(self, body: RigidBody) -> bool:
        """Add a rigid body to the world.
        
        Args:
            body: Rigid body to add
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            if body in self.rigid_bodies:
                self.logger.warning("Rigid body already in world")
                return False
            
            self.rigid_bodies.append(body)
            
            # Categorize body
            if body.is_static_body():
                self.static_bodies.append(body)
            else:
                self.dynamic_bodies.append(body)
            
            self.logger.debug(f"Added rigid body to world")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding rigid body: {e}")
            return False
    
    def remove_rigid_body(self, body: RigidBody) -> bool:
        """Remove a rigid body from the world.
        
        Args:
            body: Rigid body to remove
            
        Returns:
            True if removed successfully, False otherwise
        """
        try:
            if body not in self.rigid_bodies:
                self.logger.warning("Rigid body not in world")
                return False
            
            self.rigid_bodies.remove(body)
            
            # Remove from categories
            if body in self.static_bodies:
                self.static_bodies.remove(body)
            if body in self.dynamic_bodies:
                self.dynamic_bodies.remove(body)
            
            # Remove from constraints
            self.constraints = [c for c in self.constraints 
                              if c.body_a != body and c.body_b != body]
            
            self.logger.debug(f"Removed rigid body from world")
            return True
            
        except Exception as e:
            self.logger.error(f"Error removing rigid body: {e}")
            return False
    
    def get_rigid_bodies(self) -> List[RigidBody]:
        """Get all rigid bodies in the world.
        
        Returns:
            List of rigid bodies
        """
        return self.rigid_bodies.copy()
    
    def get_dynamic_bodies(self) -> List[RigidBody]:
        """Get all dynamic rigid bodies.
        
        Returns:
            List of dynamic rigid bodies
        """
        return self.dynamic_bodies.copy()
    
    def get_static_bodies(self) -> List[RigidBody]:
        """Get all static rigid bodies.
        
        Returns:
            List of static rigid bodies
        """
        return self.static_bodies.copy()
    
    def add_constraint(self, constraint: Constraint) -> bool:
        """Add a constraint to the world.
        
        Args:
            constraint: Constraint to add
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            # Validate constraint bodies are in world
            if constraint.body_a not in self.rigid_bodies or constraint.body_b not in self.rigid_bodies:
                self.logger.error("Constraint bodies must be in world")
                return False
            
            self.constraints.append(constraint)
            self.logger.debug(f"Added constraint: {constraint.constraint_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding constraint: {e}")
            return False
    
    def remove_constraint(self, constraint: Constraint) -> bool:
        """Remove a constraint from the world.
        
        Args:
            constraint: Constraint to remove
            
        Returns:
            True if removed successfully, False otherwise
        """
        try:
            if constraint in self.constraints:
                self.constraints.remove(constraint)
                self.logger.debug(f"Removed constraint: {constraint.constraint_type}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error removing constraint: {e}")
            return False
    
    def get_constraints(self) -> List[Constraint]:
        """Get all constraints in the world.
        
        Returns:
            List of constraints
        """
        return self.constraints.copy()
    
    def update_bodies(self, delta_time: float):
        """Update all rigid bodies in the world.
        
        Args:
            delta_time: Time step
        """
        if not self.is_initialized:
            return
        
        try:
            # Apply time scale
            scaled_delta_time = delta_time * self.time_scale
            
            # Update dynamic bodies
            for body in self.dynamic_bodies:
                if not body.is_sleeping():
                    self._update_rigid_body(body, scaled_delta_time)
                else:
                    body.update_sleep_time(scaled_delta_time)
            
            # Update constraints
            self.update_constraints(scaled_delta_time)
            
            # Update statistics
            self.update_count += 1
            self.last_update_time = time.time()
            
        except Exception as e:
            self.logger.error(f"Error updating bodies: {e}")
    
    def _update_rigid_body(self, body: RigidBody, delta_time: float):
        """Update a single rigid body.
        
        Args:
            body: Rigid body to update
            delta_time: Time step
        """
        try:
            # Apply gravity
            if not body.is_static_body():
                gravity_force = [self.gravity[i] * body.mass for i in range(3)]
                body.add_force(gravity_force)
            
            # Update linear motion
            for i in range(3):
                # Apply accumulated force
                body.linear_acceleration[i] = body.accumulated_force[i] * body.inverse_mass
                
                # Update velocity with damping
                body.linear_velocity[i] += body.linear_acceleration[i] * delta_time
                body.linear_velocity[i] *= (1.0 - body.linear_damping * delta_time)
                
                # Update position
                body.position[i] += body.linear_velocity[i] * delta_time
            
            # Update angular motion
            for i in range(3):
                # Apply accumulated torque
                body.angular_acceleration[i] = body.accumulated_torque[i] * body.inverse_inertia_tensor[i][i]
                
                # Update angular velocity with damping
                body.angular_velocity[i] += body.angular_acceleration[i] * delta_time
                body.angular_velocity[i] *= (1.0 - body.angular_damping * delta_time)
                
                # Update rotation
                body.rotation[i] += body.angular_velocity[i] * delta_time
            
            # Clear accumulated forces
            body.accumulated_force = [0.0, 0.0, 0.0]
            body.accumulated_torque = [0.0, 0.0, 0.0]
            
            # Check for sleeping
            if body.should_sleep():
                body.update_sleep_time(delta_time)
                if body.sleep_time > 2.0:  # Sleep after 2 seconds of inactivity
                    body.set_sleeping(True)
            
        except Exception as e:
            self.logger.error(f"Error updating rigid body: {e}")
    
    def update_constraints(self, delta_time: float):
        """Update all constraints in the world.
        
        Args:
            delta_time: Time step
        """
        try:
            # Simple constraint solving (placeholder)
            # In a real physics engine, this would implement proper constraint solving
            # like sequential impulse or position-based dynamics
            
            for constraint in self.constraints:
                self._solve_constraint(constraint, delta_time)
                
        except Exception as e:
            self.logger.error(f"Error updating constraints: {e}")
    
    def _solve_constraint(self, constraint: Constraint, delta_time: float):
        """Solve a single constraint.
        
        Args:
            constraint: Constraint to solve
            delta_time: Time step
        """
        try:
            # Placeholder constraint solving
            # This would implement actual constraint solving algorithms
            # based on the constraint type
            
            if constraint.constraint_type == "distance":
                # Distance constraint
                pass
            elif constraint.constraint_type == "hinge":
                # Hinge constraint
                pass
            elif constraint.constraint_type == "ball_socket":
                # Ball socket constraint
                pass
            
        except Exception as e:
            self.logger.error(f"Error solving constraint: {e}")
    
    def raycast(self, origin: List[float], direction: List[float], 
                max_distance: float = float('inf')) -> Optional[Dict[str, Any]]:
        """Perform a raycast query.
        
        Args:
            origin: Ray origin [x, y, z]
            direction: Ray direction [x, y, z]
            max_distance: Maximum ray distance
            
        Returns:
            Hit information or None if no hit
        """
        try:
            # Simple raycast implementation
            # In a real physics engine, this would use spatial partitioning
            # and proper collision detection
            
            closest_hit = None
            closest_distance = max_distance
            
            for body in self.rigid_bodies:
                if not body.collision_enabled:
                    continue
                
                # Simple AABB raycast
                hit_distance = self._raycast_aabb(origin, direction, body)
                
                if hit_distance is not None and hit_distance < closest_distance:
                    closest_distance = hit_distance
                    closest_hit = {
                        "body": body,
                        "distance": hit_distance,
                        "point": [origin[i] + direction[i] * hit_distance for i in range(3)],
                        "normal": [0.0, 1.0, 0.0]  # Placeholder normal
                    }
            
            return closest_hit
            
        except Exception as e:
            self.logger.error(f"Error in raycast: {e}")
            return None
    
    def _raycast_aabb(self, origin: List[float], direction: List[float], 
                     body: RigidBody) -> Optional[float]:
        """Perform AABB raycast against a rigid body.
        
        Args:
            origin: Ray origin
            direction: Ray direction
            body: Rigid body to test
            
        Returns:
            Hit distance or None if no hit
        """
        try:
            # Simple AABB raycast
            # This is a placeholder implementation
            
            # Get AABB bounds (simplified)
            half_size = [s * 0.5 for s in body.scale]
            min_bounds = [body.position[i] - half_size[i] for i in range(3)]
            max_bounds = [body.position[i] + half_size[i] for i in range(3)]
            
            # Ray-AABB intersection test
            t_min = 0.0
            t_max = float('inf')
            
            for i in range(3):
                if abs(direction[i]) < 1e-6:
                    # Ray is parallel to the plane
                    if origin[i] < min_bounds[i] or origin[i] > max_bounds[i]:
                        return None
                else:
                    t1 = (min_bounds[i] - origin[i]) / direction[i]
                    t2 = (max_bounds[i] - origin[i]) / direction[i]
                    
                    if t1 > t2:
                        t1, t2 = t2, t1
                    
                    t_min = max(t_min, t1)
                    t_max = min(t_max, t2)
                    
                    if t_min > t_max:
                        return None
            
            return t_min if t_min >= 0 else None
            
        except Exception as e:
            self.logger.error(f"Error in AABB raycast: {e}")
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get physics world statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "total_bodies": len(self.rigid_bodies),
            "dynamic_bodies": len(self.dynamic_bodies),
            "static_bodies": len(self.static_bodies),
            "constraints": len(self.constraints),
            "update_count": self.update_count,
            "time_scale": self.time_scale
        }
    
    def clear(self):
        """Clear all bodies and constraints from the world."""
        self.rigid_bodies.clear()
        self.static_bodies.clear()
        self.dynamic_bodies.clear()
        self.constraints.clear()
        self.logger.info("Physics world cleared")
    
    def shutdown(self):
        """Shutdown the physics world."""
        if self.is_initialized:
            self.logger.info("Shutting down physics world...")
            
            # Clear all data
            self.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Physics world shutdown complete")
