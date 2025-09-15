"""
Physics Engine for Nexlify Engine.

This module provides the main physics engine that coordinates
all physics simulation including rigid bodies, collision detection,
and constraint solving.
"""

import time
import logging
from typing import Dict, Any, Optional, List, Set

from .config import PhysicsConfig, PhysicsStats, PhysicsStepMode
from .world import PhysicsWorld
from .rigid_body import RigidBody
from .collision_detector import CollisionDetector
from .collision_resolver import CollisionResolver
from ..utils.logger import get_logger


class PhysicsEngine:
    """Main physics engine class."""
    
    def __init__(self, config: PhysicsConfig = None):
        self.config = config or PhysicsConfig()
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Core systems
        self.world: Optional[PhysicsWorld] = None
        self.collision_detector: Optional[CollisionDetector] = None
        self.collision_resolver: Optional[CollisionResolver] = None
        
        # Performance tracking
        self.stats = PhysicsStats()
        self.last_step_time = time.time()
        self.step_count = 0
        
        # Timing
        self.accumulator = 0.0
        self.last_time = time.time()
        
        # State
        self.is_running = False
        self.paused = False
        
    def initialize(self) -> bool:
        """Initialize the physics engine.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing physics engine...")
            
            # Initialize physics world
            self.world = PhysicsWorld(self.config)
            if not self.world.initialize():
                self.logger.error("Failed to initialize physics world")
                return False
            
            # Initialize collision detector
            self.collision_detector = CollisionDetector()
            if not self.collision_detector.initialize():
                self.logger.error("Failed to initialize collision detector")
                return False
            
            # Initialize collision resolver
            self.collision_resolver = CollisionResolver()
            if not self.collision_resolver.initialize():
                self.logger.error("Failed to initialize collision resolver")
                return False
            
            # Set default gravity
            if self.config.gravity is None:
                self.config.gravity = [0.0, -9.81, 0.0]
            
            self.world.set_gravity(self.config.gravity)
            
            self.is_initialized = True
            self.logger.info("✅ Physics engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize physics engine: {e}", exc_info=True)
            return False
    
    def start(self):
        """Start the physics simulation."""
        if not self.is_initialized:
            self.logger.error("Physics engine not initialized")
            return
        
        self.is_running = True
        self.paused = False
        self.last_time = time.time()
        self.accumulator = 0.0
        
        self.logger.info("Physics simulation started")
    
    def stop(self):
        """Stop the physics simulation."""
        self.is_running = False
        self.logger.info("Physics simulation stopped")
    
    def pause(self):
        """Pause the physics simulation."""
        self.paused = True
        self.logger.info("Physics simulation paused")
    
    def resume(self):
        """Resume the physics simulation."""
        self.paused = False
        self.logger.info("Physics simulation resumed")
    
    def step(self, delta_time: float = None):
        """Step the physics simulation.
        
        Args:
            delta_time: Time step (if None, uses real time)
        """
        if not self.is_running or self.paused or not self.is_initialized:
            return
        
        try:
            current_time = time.time()
            
            if delta_time is None:
                delta_time = current_time - self.last_time
            
            self.last_time = current_time
            
            # Handle different step modes
            if self.config.step_mode == PhysicsStepMode.FIXED:
                self._step_fixed(delta_time)
            elif self.config.step_mode == PhysicsStepMode.VARIABLE:
                self._step_variable(delta_time)
            elif self.config.step_mode == PhysicsStepMode.ADAPTIVE:
                self._step_adaptive(delta_time)
            
            # Update statistics
            self._update_stats(delta_time)
            
        except Exception as e:
            self.logger.error(f"Error in physics step: {e}", exc_info=True)
    
    def _step_fixed(self, delta_time: float):
        """Step with fixed timestep."""
        self.accumulator += delta_time
        
        while self.accumulator >= self.config.fixed_timestep:
            self._physics_step(self.config.fixed_timestep)
            self.accumulator -= self.config.fixed_timestep
    
    def _step_variable(self, delta_time: float):
        """Step with variable timestep."""
        # Clamp timestep to prevent instability
        clamped_delta = min(delta_time, self.config.max_timestep)
        self._physics_step(clamped_delta)
    
    def _step_adaptive(self, delta_time: float):
        """Step with adaptive timestep."""
        # TODO: Implement adaptive timestep based on simulation stability
        clamped_delta = min(delta_time, self.config.max_timestep)
        self._physics_step(clamped_delta)
    
    def _physics_step(self, delta_time: float):
        """Perform a single physics step.
        
        Args:
            delta_time: Time step
        """
        step_start = time.time()
        
        # Update rigid bodies
        if self.world:
            self.world.update_bodies(delta_time)
        
        # Detect collisions
        collision_pairs = []
        if self.collision_detector and self.world:
            collision_pairs = self.collision_detector.detect_collisions(self.world.get_rigid_bodies())
        
        # Resolve collisions
        if self.collision_resolver and collision_pairs:
            self.collision_resolver.resolve_collisions(collision_pairs, delta_time)
        
        # Update constraints
        if self.world:
            self.world.update_constraints(delta_time)
        
        # Update sleeping bodies
        if self.config.enable_sleeping:
            self._update_sleeping_bodies()
        
        # Update step statistics
        step_time = time.time() - step_start
        self.stats.step_time = step_time
        self.stats.collision_pairs = len(collision_pairs)
        self.step_count += 1
    
    def _update_sleeping_bodies(self):
        """Update sleeping/awake status of rigid bodies."""
        if not self.world:
            return
        
        for body in self.world.get_rigid_bodies():
            if body.is_sleeping():
                continue
            
            # Check if body should sleep
            if body.get_linear_velocity_magnitude() < self.config.sleep_threshold and \
               body.get_angular_velocity_magnitude() < self.config.sleep_threshold:
                body.set_sleeping(True)
            else:
                body.set_sleeping(False)
    
    def _update_stats(self, delta_time: float):
        """Update physics statistics."""
        # Calculate FPS
        if delta_time > 0:
            self.stats.fps = 1.0 / delta_time
        
        # Update body counts
        if self.world:
            bodies = self.world.get_rigid_bodies()
            self.stats.rigid_bodies = len(bodies)
            self.stats.active_bodies = sum(1 for body in bodies if not body.is_sleeping())
            self.stats.sleeping_bodies = sum(1 for body in bodies if body.is_sleeping())
            self.stats.constraints = len(self.world.get_constraints())
    
    def add_rigid_body(self, body: RigidBody) -> bool:
        """Add a rigid body to the simulation.
        
        Args:
            body: Rigid body to add
            
        Returns:
            True if body added successfully, False otherwise
        """
        if not self.world:
            return False
        
        return self.world.add_rigid_body(body)
    
    def remove_rigid_body(self, body: RigidBody) -> bool:
        """Remove a rigid body from the simulation.
        
        Args:
            body: Rigid body to remove
            
        Returns:
            True if body removed successfully, False otherwise
        """
        if not self.world:
            return False
        
        return self.world.remove_rigid_body(body)
    
    def get_rigid_bodies(self) -> List[RigidBody]:
        """Get all rigid bodies in the simulation.
        
        Returns:
            List of rigid bodies
        """
        if not self.world:
            return []
        
        return self.world.get_rigid_bodies()
    
    def set_gravity(self, gravity: List[float]):
        """Set the gravity vector.
        
        Args:
            gravity: Gravity vector [x, y, z]
        """
        self.config.gravity = gravity.copy()
        if self.world:
            self.world.set_gravity(gravity)
    
    def get_gravity(self) -> List[float]:
        """Get the current gravity vector.
        
        Returns:
            Gravity vector [x, y, z]
        """
        return self.config.gravity.copy()
    
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
        if not self.collision_detector or not self.world:
            return None
        
        return self.collision_detector.raycast(
            origin, direction, max_distance, self.world.get_rigid_bodies()
        )
    
    def get_stats(self) -> PhysicsStats:
        """Get physics engine statistics.
        
        Returns:
            Current physics statistics
        """
        return self.stats
    
    def get_config(self) -> PhysicsConfig:
        """Get physics engine configuration.
        
        Returns:
            Current physics configuration
        """
        return self.config
    
    def set_config(self, config: PhysicsConfig):
        """Set physics engine configuration.
        
        Args:
            config: New physics configuration
        """
        self.config = config
        
        # Apply configuration changes
        if self.world:
            self.world.set_gravity(self.config.gravity)
    
    def shutdown(self):
        """Shutdown the physics engine."""
        if self.is_initialized:
            self.logger.info("Shutting down physics engine...")
            
            # Stop simulation
            self.stop()
            
            # Shutdown systems
            if self.collision_resolver:
                self.collision_resolver.shutdown()
                self.collision_resolver = None
            
            if self.collision_detector:
                self.collision_detector.shutdown()
                self.collision_detector = None
            
            if self.world:
                self.world.shutdown()
                self.world = None
            
            self.is_initialized = False
            self.logger.info("✅ Physics engine shutdown complete")