"""
Collision Detector for Nexlify Physics Engine.

This module provides collision detection between rigid bodies
including broad phase and narrow phase collision detection.
"""

import logging
import math
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from .rigid_body import RigidBody
from ..utils.logger import get_logger


@dataclass
class CollisionPair:
    """Collision pair information."""
    body_a: RigidBody
    body_b: RigidBody
    contact_points: List[Dict[str, Any]]
    normal: List[float]
    penetration: float


@dataclass
class ContactPoint:
    """Contact point information."""
    position: List[float]
    normal: List[float]
    penetration: float
    separation_velocity: float


class CollisionDetector:
    """Collision detection system."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Collision detection settings
        self.broad_phase_enabled = True
        self.narrow_phase_enabled = True
        self.contact_generation_enabled = True
        
        # Spatial partitioning (placeholder)
        self.spatial_grid_size = 10.0
        self.spatial_grid: Dict[Tuple[int, int, int], List[RigidBody]] = {}
        
        # Performance tracking
        self.broad_phase_pairs = 0
        self.narrow_phase_pairs = 0
        self.contact_points_generated = 0
        
    def initialize(self) -> bool:
        """Initialize the collision detector.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing collision detector...")
            
            # Clear spatial grid
            self.spatial_grid.clear()
            
            self.is_initialized = True
            self.logger.info("✅ Collision detector initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize collision detector: {e}")
            return False
    
    def detect_collisions(self, bodies: List[RigidBody]) -> List[CollisionPair]:
        """Detect collisions between rigid bodies.
        
        Args:
            bodies: List of rigid bodies to test
            
        Returns:
            List of collision pairs
        """
        if not self.is_initialized:
            return []
        
        try:
            collision_pairs = []
            
            # Broad phase collision detection
            if self.broad_phase_enabled:
                potential_pairs = self._broad_phase_detection(bodies)
            else:
                # Test all pairs if broad phase is disabled
                potential_pairs = []
                for i in range(len(bodies)):
                    for j in range(i + 1, len(bodies)):
                        potential_pairs.append((bodies[i], bodies[j]))
            
            self.broad_phase_pairs = len(potential_pairs)
            
            # Narrow phase collision detection
            if self.narrow_phase_enabled:
                for body_a, body_b in potential_pairs:
                    collision_pair = self._narrow_phase_detection(body_a, body_b)
                    if collision_pair:
                        collision_pairs.append(collision_pair)
            
            self.narrow_phase_pairs = len(collision_pairs)
            
            return collision_pairs
            
        except Exception as e:
            self.logger.error(f"Error in collision detection: {e}")
            return []
    
    def _broad_phase_detection(self, bodies: List[RigidBody]) -> List[Tuple[RigidBody, RigidBody]]:
        """Broad phase collision detection using spatial partitioning.
        
        Args:
            bodies: List of rigid bodies
            
        Returns:
            List of potential collision pairs
        """
        try:
            potential_pairs = []
            
            # Clear spatial grid
            self.spatial_grid.clear()
            
            # Insert bodies into spatial grid
            for body in bodies:
                if not body.collision_enabled:
                    continue
                
                # Get AABB bounds
                half_size = [s * 0.5 for s in body.scale]
                min_bounds = [body.position[i] - half_size[i] for i in range(3)]
                max_bounds = [body.position[i] + half_size[i] for i in range(3)]
                
                # Calculate grid cells
                min_cell = self._world_to_grid(min_bounds)
                max_cell = self._world_to_grid(max_bounds)
                
                # Insert body into all overlapping cells
                for x in range(min_cell[0], max_cell[0] + 1):
                    for y in range(min_cell[1], max_cell[1] + 1):
                        for z in range(min_cell[2], max_cell[2] + 1):
                            cell = (x, y, z)
                            if cell not in self.spatial_grid:
                                self.spatial_grid[cell] = []
                            self.spatial_grid[cell].append(body)
            
            # Find potential pairs within each cell
            for cell_bodies in self.spatial_grid.values():
                if len(cell_bodies) < 2:
                    continue
                
                # Test all pairs within the cell
                for i in range(len(cell_bodies)):
                    for j in range(i + 1, len(cell_bodies)):
                        body_a, body_b = cell_bodies[i], cell_bodies[j]
                        
                        # Skip if both bodies are static
                        if body_a.is_static_body() and body_b.is_static_body():
                            continue
                        
                        # Skip if both bodies are sleeping
                        if body_a.is_sleeping() and body_b.is_sleeping():
                            continue
                        
                        potential_pairs.append((body_a, body_b))
            
            return potential_pairs
            
        except Exception as e:
            self.logger.error(f"Error in broad phase detection: {e}")
            return []
    
    def _world_to_grid(self, position: List[float]) -> Tuple[int, int, int]:
        """Convert world position to grid coordinates.
        
        Args:
            position: World position [x, y, z]
            
        Returns:
            Grid coordinates (x, y, z)
        """
        return (
            int(position[0] // self.spatial_grid_size),
            int(position[1] // self.spatial_grid_size),
            int(position[2] // self.spatial_grid_size)
        )
    
    def _narrow_phase_detection(self, body_a: RigidBody, body_b: RigidBody) -> Optional[CollisionPair]:
        """Narrow phase collision detection between two bodies.
        
        Args:
            body_a: First rigid body
            body_b: Second rigid body
            
        Returns:
            Collision pair if collision detected, None otherwise
        """
        try:
            # Simple AABB-AABB collision detection
            # In a real physics engine, this would support various collision shapes
            
            # Get AABB bounds for body A
            half_size_a = [s * 0.5 for s in body_a.scale]
            min_a = [body_a.position[i] - half_size_a[i] for i in range(3)]
            max_a = [body_a.position[i] + half_size_a[i] for i in range(3)]
            
            # Get AABB bounds for body B
            half_size_b = [s * 0.5 for s in body_b.scale]
            min_b = [body_b.position[i] - half_size_b[i] for i in range(3)]
            max_b = [body_b.position[i] + half_size_b[i] for i in range(3)]
            
            # Check for AABB overlap
            overlap = True
            for i in range(3):
                if max_a[i] < min_b[i] or min_a[i] > max_b[i]:
                    overlap = False
                    break
            
            if not overlap:
                return None
            
            # Calculate collision information
            contact_points = self._generate_contact_points(body_a, body_b, min_a, max_a, min_b, max_b)
            
            if not contact_points:
                return None
            
            # Calculate collision normal and penetration
            normal, penetration = self._calculate_collision_normal_and_penetration(
                body_a, body_b, min_a, max_a, min_b, max_b
            )
            
            collision_pair = CollisionPair(
                body_a=body_a,
                body_b=body_b,
                contact_points=contact_points,
                normal=normal,
                penetration=penetration
            )
            
            self.contact_points_generated += len(contact_points)
            
            return collision_pair
            
        except Exception as e:
            self.logger.error(f"Error in narrow phase detection: {e}")
            return None
    
    def _generate_contact_points(self, body_a: RigidBody, body_b: RigidBody,
                               min_a: List[float], max_a: List[float],
                               min_b: List[float], max_b: List[float]) -> List[Dict[str, Any]]:
        """Generate contact points between two AABBs.
        
        Args:
            body_a: First rigid body
            body_b: Second rigid body
            min_a: Minimum bounds of body A
            max_a: Maximum bounds of body A
            min_b: Minimum bounds of body B
            max_b: Maximum bounds of body B
            
        Returns:
            List of contact points
        """
        try:
            contact_points = []
            
            if not self.contact_generation_enabled:
                # Return a single contact point at the center of overlap
                overlap_center = [
                    (min(max_a[i], max_b[i]) + max(min_a[i], min_b[i])) * 0.5
                    for i in range(3)
                ]
                
                contact_point = {
                    "position": overlap_center,
                    "normal": [0.0, 1.0, 0.0],  # Placeholder normal
                    "penetration": 0.0,  # Will be calculated separately
                    "separation_velocity": 0.0
                }
                contact_points.append(contact_point)
            else:
                # Generate multiple contact points for AABB-AABB collision
                # This is a simplified implementation
                
                # Find the overlapping region
                overlap_min = [max(min_a[i], min_b[i]) for i in range(3)]
                overlap_max = [min(max_a[i], max_b[i]) for i in range(3)]
                
                # Generate contact points at corners of overlap region
                corners = [
                    [overlap_min[0], overlap_min[1], overlap_min[2]],
                    [overlap_max[0], overlap_min[1], overlap_min[2]],
                    [overlap_min[0], overlap_max[1], overlap_min[2]],
                    [overlap_max[0], overlap_max[1], overlap_min[2]],
                    [overlap_min[0], overlap_min[1], overlap_max[2]],
                    [overlap_max[0], overlap_min[1], overlap_max[2]],
                    [overlap_min[0], overlap_max[1], overlap_max[2]],
                    [overlap_max[0], overlap_max[1], overlap_max[2]]
                ]
                
                for corner in corners:
                    contact_point = {
                        "position": corner,
                        "normal": [0.0, 1.0, 0.0],  # Placeholder normal
                        "penetration": 0.0,  # Will be calculated separately
                        "separation_velocity": 0.0
                    }
                    contact_points.append(contact_point)
            
            return contact_points
            
        except Exception as e:
            self.logger.error(f"Error generating contact points: {e}")
            return []
    
    def _calculate_collision_normal_and_penetration(self, body_a: RigidBody, body_b: RigidBody,
                                                  min_a: List[float], max_a: List[float],
                                                  min_b: List[float], max_b: List[float]) -> Tuple[List[float], float]:
        """Calculate collision normal and penetration depth.
        
        Args:
            body_a: First rigid body
            body_b: Second rigid body
            min_a: Minimum bounds of body A
            max_a: Maximum bounds of body A
            min_b: Minimum bounds of body B
            max_b: Maximum bounds of body B
            
        Returns:
            Tuple of (normal, penetration)
        """
        try:
            # Calculate overlap in each axis
            overlaps = [
                min(max_a[i], max_b[i]) - max(min_a[i], min_b[i])
                for i in range(3)
            ]
            
            # Find the axis with minimum overlap (collision normal)
            min_overlap_axis = 0
            min_overlap = overlaps[0]
            
            for i in range(1, 3):
                if overlaps[i] < min_overlap:
                    min_overlap = overlaps[i]
                    min_overlap_axis = i
            
            # Determine collision normal direction
            normal = [0.0, 0.0, 0.0]
            normal[min_overlap_axis] = 1.0
            
            # Check which body is on which side
            center_a = [(min_a[i] + max_a[i]) * 0.5 for i in range(3)]
            center_b = [(min_b[i] + max_b[i]) * 0.5 for i in range(3)]
            
            if center_a[min_overlap_axis] < center_b[min_overlap_axis]:
                normal[min_overlap_axis] = -1.0
            
            return normal, min_overlap
            
        except Exception as e:
            self.logger.error(f"Error calculating collision normal: {e}")
            return [0.0, 1.0, 0.0], 0.0
    
    def raycast(self, origin: List[float], direction: List[float], 
                max_distance: float, bodies: List[RigidBody]) -> Optional[Dict[str, Any]]:
        """Perform a raycast against rigid bodies.
        
        Args:
            origin: Ray origin [x, y, z]
            direction: Ray direction [x, y, z]
            max_distance: Maximum ray distance
            bodies: List of rigid bodies to test
            
        Returns:
            Hit information or None if no hit
        """
        try:
            closest_hit = None
            closest_distance = max_distance
            
            for body in bodies:
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
            # Get AABB bounds
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
        """Get collision detector statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "broad_phase_pairs": self.broad_phase_pairs,
            "narrow_phase_pairs": self.narrow_phase_pairs,
            "contact_points_generated": self.contact_points_generated,
            "spatial_grid_cells": len(self.spatial_grid)
        }
    
    def shutdown(self):
        """Shutdown the collision detector."""
        if self.is_initialized:
            self.logger.info("Shutting down collision detector...")
            
            # Clear spatial grid
            self.spatial_grid.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Collision detector shutdown complete")
