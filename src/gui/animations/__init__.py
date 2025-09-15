"""
Animation System Module for Nexlify GUI

This module provides animation capabilities including:
- Smooth spacing transitions and animations
- Easing curves for natural motion
- Animation groups for complex sequences
- Animation management across the application
"""

from .spacing_animations import (
    SpacingAnimation, SpacingAnimationGroup, SpacingAnimationManager,
    AnimationType, EasingType, spacing_animation_manager
)

__all__ = [
    'SpacingAnimation',
    'SpacingAnimationGroup', 
    'SpacingAnimationManager',
    'AnimationType',
    'EasingType',
    'spacing_animation_manager'
]
