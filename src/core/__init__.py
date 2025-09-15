"""
Core module for Nexlify Engine.

This module contains the fundamental classes and systems that form
the backbone of the engine, including GameObjects, Components, Scenes,
and the main GameEngine.
"""

from .game_object import GameObject, Transform
from .component import Component
from .transform_component import TransformComponent
from .scene import Scene
from .components import MeshRenderer, Light, Camera, Collider
from .engine import GameEngine, EngineStats

__all__ = [
    'GameObject',
    'Transform', 
    'Component',
    'TransformComponent',
    'Scene',
    'MeshRenderer',
    'Light',
    'Camera',
    'Collider',
    'GameEngine',
    'EngineStats'
]
