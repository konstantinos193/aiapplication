"""
Nexlify Physics Engine

This package provides comprehensive physics simulation including:
- Rigid body dynamics
- Collision detection and response
- Joint systems
- Fluid simulation
- Cloth simulation
"""

from .config import PhysicsConfig, PhysicsStats, PhysicsStepMode
from .physics_engine import PhysicsEngine
from .rigid_body import RigidBody
from .collision_detector import CollisionDetector
from .collision_resolver import CollisionResolver
from .world import PhysicsWorld

__all__ = [
    'PhysicsConfig',
    'PhysicsStats', 
    'PhysicsStepMode',
    'PhysicsEngine',
    'RigidBody',
    'CollisionDetector', 
    'CollisionResolver',
    'PhysicsWorld'
]