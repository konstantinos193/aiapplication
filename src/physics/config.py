"""
Physics Configuration for Nexlify Engine.

This module provides configuration classes for the physics system
to avoid circular import issues.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class PhysicsStepMode(Enum):
    """Physics step modes."""
    FIXED = "fixed"  # Fixed timestep
    VARIABLE = "variable"  # Variable timestep
    ADAPTIVE = "adaptive"  # Adaptive timestep


@dataclass
class PhysicsConfig:
    """Physics engine configuration."""
    gravity: List[float] = None
    fixed_timestep: float = 1.0 / 60.0  # 60 FPS
    max_timestep: float = 1.0 / 30.0  # 30 FPS minimum
    step_mode: PhysicsStepMode = PhysicsStepMode.FIXED
    iterations: int = 10
    tolerance: float = 0.001
    enable_sleeping: bool = True
    sleep_threshold: float = 0.1
    enable_ccd: bool = False  # Continuous collision detection


@dataclass
class PhysicsStats:
    """Physics engine statistics."""
    fps: float = 0.0
    step_time: float = 0.0
    rigid_bodies: int = 0
    active_bodies: int = 0
    sleeping_bodies: int = 0
    collision_pairs: int = 0
    constraints: int = 0
