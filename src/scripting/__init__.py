"""
Nexlify Scripting System

This package provides Python-based scripting functionality including:
- Component scripting
- Game logic scripting
- Event handling
- Hot reloading
- Script debugging
"""

from .scripting_engine import ScriptingEngine
from .script_component import ScriptComponent
from .event_system import EventSystem

__all__ = [
    'ScriptingEngine',
    'ScriptComponent',
    'EventSystem'
]
