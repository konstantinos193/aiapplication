"""
Spacing Animation System for Nexlify GUI

This module provides smooth animations and transitions for spacing changes,
creating a polished and professional user experience.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QObject
from PyQt6.QtCore import QParallelAnimationGroup, QSequentialAnimationGroup
from typing import Union, Optional, List, Dict, Any
from enum import Enum

from ..design_system.spacing_system import spacing, SpacingUnit


class AnimationType(Enum):
    """Types of spacing animations."""
    MARGIN = "margin"
    PADDING = "padding"
    SPACING = "spacing"
    SIZE = "size"
    POSITION = "position"


class EasingType(Enum):
    """Easing curve types for animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"


class SpacingAnimation(QObject):
    """Individual spacing animation for a specific property."""
    
    # Signals
    animation_started = pyqtSignal()
    animation_finished = pyqtSignal()
    animation_progress = pyqtSignal(float)  # Progress from 0.0 to 1.0
    
    def __init__(self, widget: QWidget, property_name: str, 
                 start_value: int, end_value: int, duration: int = 300):
        """Initialize the spacing animation.
        
        Args:
            widget: Widget to animate
            property_name: Property to animate (e.g., 'geometry', 'contentsMargins')
            start_value: Starting value
            end_value: Ending value
            duration: Animation duration in milliseconds
        """
        super().__init__()
        
        self.widget = widget
        self.property_name = property_name
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        
        # Create Qt animation
        self.animation = QPropertyAnimation(widget, property_name.encode())
        self.animation.setDuration(duration)
        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        
        # Setup connections
        self.animation.finished.connect(self._on_finished)
        self.animation.valueChanged.connect(self._on_value_changed)
    
    def start(self, easing: EasingType = EasingType.EASE_IN_OUT):
        """Start the animation.
        
        Args:
            easing: Easing curve type
        """
        # Set easing curve
        easing_curve = self._get_easing_curve(easing)
        self.animation.setEasingCurve(easing_curve)
        
        # Emit started signal
        self.animation_started.emit()
        
        # Start animation
        self.animation.start()
    
    def stop(self):
        """Stop the animation."""
        self.animation.stop()
    
    def pause(self):
        """Pause the animation."""
        self.animation.pause()
    
    def resume(self):
        """Resume the animation."""
        self.animation.resume()
    
    def _get_easing_curve(self, easing: EasingType) -> QEasingCurve:
        """Get Qt easing curve for the specified type.
        
        Args:
            easing: Easing type
            
        Returns:
            Qt easing curve
        """
        if easing == EasingType.LINEAR:
            return QEasingCurve.Type.Linear
        elif easing == EasingType.EASE_IN:
            return QEasingCurve.Type.InQuad
        elif easing == EasingType.EASE_OUT:
            return QEasingCurve.Type.OutQuad
        elif easing == EasingType.EASE_IN_OUT:
            return QEasingCurve.Type.InOutQuad
        elif easing == EasingType.BOUNCE:
            return QEasingCurve.Type.OutBounce
        elif easing == EasingType.ELASTIC:
            return QEasingCurve.Type.OutElastic
        else:
            return QEasingCurve.Type.InOutQuad
    
    def _on_finished(self):
        """Handle animation finished."""
        self.animation_finished.emit()
    
    def _on_value_changed(self, value):
        """Handle animation value change."""
        # Calculate progress (0.0 to 1.0)
        if self.end_value != self.start_value:
            progress = (value - self.start_value) / (self.end_value - self.start_value)
            progress = max(0.0, min(1.0, progress))  # Clamp to 0.0-1.0
            self.animation_progress.emit(progress)


class SpacingAnimationGroup(QObject):
    """Group of spacing animations that can run together."""
    
    # Signals
    group_started = pyqtSignal()
    group_finished = pyqtSignal()
    group_progress = pyqtSignal(float)  # Overall progress
    
    def __init__(self):
        """Initialize the animation group."""
        super().__init__()
        
        self.animations: List[SpacingAnimation] = []
        self.parallel_group = QParallelAnimationGroup()
        self.sequential_group = QSequentialAnimationGroup()
        
        # Setup connections
        self.parallel_group.finished.connect(self._on_group_finished)
        self.sequential_group.finished.connect(self._on_group_finished)
    
    def add_animation(self, animation: SpacingAnimation):
        """Add an animation to the group.
        
        Args:
            animation: Animation to add
        """
        self.animations.append(animation)
        self.parallel_group.addAnimation(animation.animation)
    
    def add_sequential_animation(self, animation: SpacingAnimation):
        """Add an animation to run sequentially.
        
        Args:
            animation: Animation to add
        """
        self.animations.append(animation)
        self.sequential_group.addAnimation(animation.animation)
    
    def start_parallel(self, easing: EasingType = EasingType.EASE_IN_OUT):
        """Start all animations in parallel.
        
        Args:
            easing: Easing curve type for all animations
        """
        # Set easing for all animations
        for animation in self.animations:
            animation.animation.setEasingCurve(self._get_easing_curve(easing))
        
        # Emit started signal
        self.group_started.emit()
        
        # Start parallel group
        self.parallel_group.start()
    
    def start_sequential(self, easing: EasingType = EasingType.EASE_IN_OUT):
        """Start all animations sequentially.
        
        Args:
            easing: Easing curve type for all animations
        """
        # Set easing for all animations
        for animation in self.animations:
            animation.animation.setEasingCurve(self._get_easing_curve(easing))
        
        # Emit started signal
        self.group_started.emit()
        
        # Start sequential group
        self.sequential_group.start()
    
    def stop(self):
        """Stop all animations."""
        self.parallel_group.stop()
        self.sequential_group.stop()
    
    def pause(self):
        """Pause all animations."""
        self.parallel_group.pause()
        self.sequential_group.pause()
    
    def resume(self):
        """Resume all animations."""
        self.parallel_group.resume()
        self.sequential_group.resume()
    
    def _get_easing_curve(self, easing: EasingType) -> QEasingCurve.Type:
        """Get Qt easing curve type.
        
        Args:
            easing: Easing type
            
        Returns:
            Qt easing curve type
        """
        if easing == EasingType.LINEAR:
            return QEasingCurve.Type.Linear
        elif easing == EasingType.EASE_IN:
            return QEasingCurve.Type.InQuad
        elif easing == EasingType.EASE_OUT:
            return QEasingCurve.Type.OutQuad
        elif easing == EasingType.EASE_IN_OUT:
            return QEasingCurve.Type.InOutQuad
        elif easing == EasingType.BOUNCE:
            return QEasingCurve.Type.OutBounce
        elif easing == EasingType.ELASTIC:
            return QEasingCurve.Type.OutElastic
        else:
            return QEasingCurve.Type.InOutQuad
    
    def _on_group_finished(self):
        """Handle group animation finished."""
        self.group_finished.emit()


class SpacingAnimationManager:
    """Manager for spacing animations across the application."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern for animation manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the animation manager."""
        if not hasattr(self, 'initialized'):
            self.active_animations: List[SpacingAnimation] = []
            self.animation_groups: List[SpacingAnimationGroup] = []
            self.initialized = True
    
    def animate_margin_change(self, widget: QWidget, 
                            start_margins: tuple, end_margins: tuple,
                            duration: int = 300, easing: EasingType = EasingType.EASE_IN_OUT):
        """Animate margin change for a widget.
        
        Args:
            widget: Widget to animate
            start_margins: Starting margins (left, top, right, bottom)
            end_margins: Ending margins (left, top, right, bottom)
            duration: Animation duration in milliseconds
            easing: Easing curve type
            
        Returns:
            Created animation
        """
        # Create animation for each margin direction
        animations = []
        
        # Left margin
        left_anim = SpacingAnimation(widget, "leftMargin", start_margins[0], end_margins[0], duration)
        animations.append(left_anim)
        
        # Top margin
        top_anim = SpacingAnimation(widget, "topMargin", start_margins[1], end_margins[1], duration)
        animations.append(top_anim)
        
        # Right margin
        right_anim = SpacingAnimation(widget, "rightMargin", start_margins[2], end_margins[2], duration)
        animations.append(right_anim)
        
        # Bottom margin
        bottom_anim = SpacingAnimation(widget, "bottomMargin", start_margins[3], end_margins[3], duration)
        animations.append(bottom_anim)
        
        # Create group and start
        group = SpacingAnimationGroup()
        for anim in animations:
            group.add_animation(anim)
        
        group.start_parallel(easing)
        
        # Store references
        self.active_animations.extend(animations)
        self.animation_groups.append(group)
        
        return group
    
    def animate_spacing_change(self, widget: QWidget, 
                             start_spacing: int, end_spacing: int,
                             duration: int = 300, easing: EasingType = EasingType.EASE_IN_OUT):
        """Animate spacing change for a widget.
        
        Args:
            widget: Widget to animate
            start_spacing: Starting spacing value
            end_spacing: Ending spacing value
            duration: Animation duration in milliseconds
            easing: Easing curve type
            
        Returns:
            Created animation
        """
        animation = SpacingAnimation(widget, "spacing", start_spacing, end_spacing, duration)
        animation.start(easing)
        
        # Store reference
        self.active_animations.append(animation)
        
        return animation
    
    def stop_all_animations(self):
        """Stop all active animations."""
        for animation in self.active_animations:
            animation.stop()
        
        for group in self.animation_groups:
            group.stop()
        
        self.active_animations.clear()
        self.animation_groups.clear()
    
    def get_active_animations_count(self) -> int:
        """Get count of active animations.
        
        Returns:
            Number of active animations
        """
        return len(self.active_animations)
    
    def cleanup_finished_animations(self):
        """Remove finished animations from tracking."""
        self.active_animations = [anim for anim in self.active_animations if anim.animation.state() != QPropertyAnimation.State.Stopped]
        self.animation_groups = [group for group in self.animation_groups if group.parallel_group.state() != QPropertyAnimation.State.Stopped]


# Global instance for easy access
spacing_animation_manager = SpacingAnimationManager()
