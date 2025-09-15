"""
Collision Resolver for Nexlify Physics Engine.

This module provides collision response and resolution including
impulse-based collision response and constraint solving.
"""

import logging
import math
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from .collision_detector import CollisionPair
from .rigid_body import RigidBody
from ..utils.logger import get_logger


@dataclass
class ContactManifold:
    """Contact manifold for collision resolution."""
    body_a: RigidBody
    body_b: RigidBody
    contact_points: List[Dict[str, Any]]
    normal: List[float]
    penetration: float
    restitution: float
    friction: float


class CollisionResolver:
    """Collision resolution system."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Resolution settings
        self.position_iterations = 4
        self.velocity_iterations = 8
        self.bias_factor = 0.2
        self.max_penetration = 0.01
        
        # Performance tracking
        self.collisions_resolved = 0
        self.impulses_applied = 0
        
    def initialize(self) -> bool:
        """Initialize the collision resolver.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing collision resolver...")
            
            self.is_initialized = True
            self.logger.info("✅ Collision resolver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize collision resolver: {e}")
            return False
    
    def resolve_collisions(self, collision_pairs: List[CollisionPair], delta_time: float):
        """Resolve collisions between rigid bodies.
        
        Args:
            collision_pairs: List of collision pairs to resolve
            delta_time: Time step
        """
        if not self.is_initialized:
            return
        
        try:
            # Convert collision pairs to contact manifolds
            contact_manifolds = []
            for pair in collision_pairs:
                manifold = self._create_contact_manifold(pair)
                if manifold:
                    contact_manifolds.append(manifold)
            
            # Resolve positions (penetration correction)
            self._resolve_positions(contact_manifolds, delta_time)
            
            # Resolve velocities (impulse response)
            self._resolve_velocities(contact_manifolds, delta_time)
            
            self.collisions_resolved += len(contact_manifolds)
            
        except Exception as e:
            self.logger.error(f"Error resolving collisions: {e}")
    
    def _create_contact_manifold(self, pair: CollisionPair) -> Optional[ContactManifold]:
        """Create a contact manifold from a collision pair.
        
        Args:
            pair: Collision pair
            
        Returns:
            Contact manifold or None if invalid
        """
        try:
            # Calculate combined material properties
            material_a = pair.body_a.get_material()
            material_b = pair.body_b.get_material()
            
            # Use minimum restitution (more realistic)
            restitution = min(material_a.restitution, material_b.restitution)
            
            # Use geometric mean for friction
            friction = math.sqrt(material_a.friction * material_b.friction)
            
            manifold = ContactManifold(
                body_a=pair.body_a,
                body_b=pair.body_b,
                contact_points=pair.contact_points,
                normal=pair.normal,
                penetration=pair.penetration,
                restitution=restitution,
                friction=friction
            )
            
            return manifold
            
        except Exception as e:
            self.logger.error(f"Error creating contact manifold: {e}")
            return None
    
    def _resolve_positions(self, manifolds: List[ContactManifold], delta_time: float):
        """Resolve position penetrations.
        
        Args:
            manifolds: List of contact manifolds
            delta_time: Time step
        """
        try:
            for iteration in range(self.position_iterations):
                for manifold in manifolds:
                    self._resolve_position_manifold(manifold, delta_time)
                    
        except Exception as e:
            self.logger.error(f"Error resolving positions: {e}")
    
    def _resolve_position_manifold(self, manifold: ContactManifold, delta_time: float):
        """Resolve position penetration for a single manifold.
        
        Args:
            manifold: Contact manifold
            delta_time: Time step
        """
        try:
            body_a = manifold.body_a
            body_b = manifold.body_b
            
            # Skip if both bodies are static
            if body_a.is_static_body() and body_b.is_static_body():
                return
            
            # Calculate separation impulse
            separation = manifold.penetration - self.max_penetration
            if separation <= 0:
                return
            
            # Calculate effective mass
            inv_mass_a = body_a.inverse_mass
            inv_mass_b = body_b.inverse_mass
            total_inv_mass = inv_mass_a + inv_mass_b
            
            if total_inv_mass <= 0:
                return
            
            # Calculate separation impulse
            impulse_magnitude = separation / total_inv_mass * self.bias_factor / delta_time
            
            # Apply separation impulse
            impulse = [manifold.normal[i] * impulse_magnitude for i in range(3)]
            
            if not body_a.is_static_body():
                for i in range(3):
                    body_a.position[i] += impulse[i] * inv_mass_a
            
            if not body_b.is_static_body():
                for i in range(3):
                    body_b.position[i] -= impulse[i] * inv_mass_b
            
        except Exception as e:
            self.logger.error(f"Error resolving position manifold: {e}")
    
    def _resolve_velocities(self, manifolds: List[ContactManifold], delta_time: float):
        """Resolve velocity impulses.
        
        Args:
            manifolds: List of contact manifolds
            delta_time: Time step
        """
        try:
            for iteration in range(self.velocity_iterations):
                for manifold in manifolds:
                    self._resolve_velocity_manifold(manifold, delta_time)
                    
        except Exception as e:
            self.logger.error(f"Error resolving velocities: {e}")
    
    def _resolve_velocity_manifold(self, manifold: ContactManifold, delta_time: float):
        """Resolve velocity impulses for a single manifold.
        
        Args:
            manifold: Contact manifold
            delta_time: Time step
        """
        try:
            body_a = manifold.body_a
            body_b = manifold.body_b
            
            # Skip if both bodies are static
            if body_a.is_static_body() and body_b.is_static_body():
                return
            
            # Calculate relative velocity
            relative_velocity = self._calculate_relative_velocity(body_a, body_b, manifold.normal)
            
            # Calculate separation velocity
            separation_velocity = sum(relative_velocity[i] * manifold.normal[i] for i in range(3))
            
            # Don't resolve if objects are separating
            if separation_velocity > 0:
                return
            
            # Calculate effective mass
            inv_mass_a = body_a.inverse_mass
            inv_mass_b = body_b.inverse_mass
            total_inv_mass = inv_mass_a + inv_mass_b
            
            if total_inv_mass <= 0:
                return
            
            # Calculate impulse magnitude
            impulse_magnitude = -(1 + manifold.restitution) * separation_velocity / total_inv_mass
            
            # Apply normal impulse
            normal_impulse = [manifold.normal[i] * impulse_magnitude for i in range(3)]
            
            if not body_a.is_static_body():
                for i in range(3):
                    body_a.linear_velocity[i] += normal_impulse[i] * inv_mass_a
            
            if not body_b.is_static_body():
                for i in range(3):
                    body_b.linear_velocity[i] -= normal_impulse[i] * inv_mass_b
            
            # Apply friction impulse
            self._apply_friction_impulse(manifold, normal_impulse, delta_time)
            
            self.impulses_applied += 1
            
        except Exception as e:
            self.logger.error(f"Error resolving velocity manifold: {e}")
    
    def _calculate_relative_velocity(self, body_a: RigidBody, body_b: RigidBody, 
                                   normal: List[float]) -> List[float]:
        """Calculate relative velocity between two bodies.
        
        Args:
            body_a: First rigid body
            body_b: Second rigid body
            normal: Contact normal
            
        Returns:
            Relative velocity vector
        """
        try:
            # Simple relative velocity calculation
            # In a real physics engine, this would account for angular velocity
            # and contact point positions
            
            relative_velocity = [
                body_a.linear_velocity[i] - body_b.linear_velocity[i]
                for i in range(3)
            ]
            
            return relative_velocity
            
        except Exception as e:
            self.logger.error(f"Error calculating relative velocity: {e}")
            return [0.0, 0.0, 0.0]
    
    def _apply_friction_impulse(self, manifold: ContactManifold, normal_impulse: List[float], 
                              delta_time: float):
        """Apply friction impulse.
        
        Args:
            manifold: Contact manifold
            normal_impulse: Normal impulse vector
            delta_time: Time step
        """
        try:
            body_a = manifold.body_a
            body_b = manifold.body_b
            
            # Skip if both bodies are static
            if body_a.is_static_body() and body_b.is_static_body():
                return
            
            # Calculate tangent velocity
            relative_velocity = self._calculate_relative_velocity(body_a, body_b, manifold.normal)
            
            # Project relative velocity onto tangent plane
            tangent_velocity = [
                relative_velocity[i] - sum(relative_velocity[j] * manifold.normal[j] for j in range(3)) * manifold.normal[i]
                for i in range(3)
            ]
            
            # Calculate tangent velocity magnitude
            tangent_magnitude = math.sqrt(sum(v * v for v in tangent_velocity))
            
            if tangent_magnitude < 1e-6:
                return
            
            # Normalize tangent velocity
            tangent_direction = [v / tangent_magnitude for v in tangent_velocity]
            
            # Calculate friction impulse magnitude
            normal_impulse_magnitude = math.sqrt(sum(i * i for i in normal_impulse))
            friction_impulse_magnitude = manifold.friction * normal_impulse_magnitude
            
            # Clamp friction impulse
            inv_mass_a = body_a.inverse_mass
            inv_mass_b = body_b.inverse_mass
            total_inv_mass = inv_mass_a + inv_mass_b
            
            if total_inv_mass > 0:
                max_friction_impulse = tangent_magnitude / total_inv_mass
                friction_impulse_magnitude = min(friction_impulse_magnitude, max_friction_impulse)
            
            # Apply friction impulse
            friction_impulse = [tangent_direction[i] * friction_impulse_magnitude for i in range(3)]
            
            if not body_a.is_static_body():
                for i in range(3):
                    body_a.linear_velocity[i] += friction_impulse[i] * inv_mass_a
            
            if not body_b.is_static_body():
                for i in range(3):
                    body_b.linear_velocity[i] -= friction_impulse[i] * inv_mass_b
            
        except Exception as e:
            self.logger.error(f"Error applying friction impulse: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collision resolver statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "collisions_resolved": self.collisions_resolved,
            "impulses_applied": self.impulses_applied,
            "position_iterations": self.position_iterations,
            "velocity_iterations": self.velocity_iterations
        }
    
    def shutdown(self):
        """Shutdown the collision resolver."""
        if self.is_initialized:
            self.logger.info("Shutting down collision resolver...")
            
            self.is_initialized = False
            self.logger.info("✅ Collision resolver shutdown complete")
