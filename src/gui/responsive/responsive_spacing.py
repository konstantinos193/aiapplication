"""
Responsive Spacing System for Nexlify GUI

This module provides responsive spacing that automatically adjusts
based on screen size, breakpoints, and device characteristics.
"""

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from typing import Dict, Optional, Union, Tuple
from enum import Enum

from ..design_system.spacing_system import spacing, SpacingUnit


class Breakpoint(Enum):
    """Breakpoint definitions for responsive design."""
    MOBILE = "mobile"      # < 768px
    TABLET = "tablet"      # 768px - 1024px
    DESKTOP = "desktop"    # 1024px - 1440px
    WIDESCREEN = "widescreen"  # > 1440px


class ResponsiveSpacing(QObject):
    """Responsive spacing system that adjusts based on screen size."""
    
    # Signals
    breakpoint_changed = pyqtSignal(str)  # Emits new breakpoint name
    spacing_updated = pyqtSignal()        # Emits when spacing values change
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the responsive spacing system.
        
        Args:
            parent: Parent widget to monitor for size changes
        """
        super().__init__(parent)
        
        # Current breakpoint
        self.current_breakpoint = Breakpoint.DESKTOP
        
        # Breakpoint thresholds (in pixels)
        self.breakpoints = {
            Breakpoint.MOBILE: 768,
            Breakpoint.TABLET: 1024,
            Breakpoint.DESKTOP: 1440,
            Breakpoint.WIDESCREEN: float('inf')
        }
        
        # Responsive spacing multipliers
        self.spacing_multipliers = {
            Breakpoint.MOBILE: 0.75,      # 75% of base spacing
            Breakpoint.TABLET: 0.875,     # 87.5% of base spacing
            Breakpoint.DESKTOP: 1.0,      # 100% of base spacing
            Breakpoint.WIDESCREEN: 1.25   # 125% of base spacing
        }
        
        # Touch-friendly spacing adjustments
        self.touch_spacing_multipliers = {
            Breakpoint.MOBILE: 1.2,       # 20% larger for touch
            Breakpoint.TABLET: 1.1,       # 10% larger for touch
            Breakpoint.DESKTOP: 1.0,      # No change for desktop
            Breakpoint.WIDESCREEN: 1.0    # No change for widescreen
        }
        
        # Initialize
        self._setup_monitoring()
        self._update_breakpoint()
    
    def _setup_monitoring(self):
        """Setup monitoring for screen size changes."""
        # Get the main application instance
        app = QApplication.instance()
        if app:
            # Monitor primary screen
            primary_screen = app.primaryScreen()
            if primary_screen:
                primary_screen.geometryChanged.connect(self._on_screen_changed)
        
        # Setup timer for periodic checks
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self._check_breakpoint)
        self.monitor_timer.start(1000)  # Check every second
    
    def _on_screen_changed(self):
        """Handle screen geometry changes."""
        self._update_breakpoint()
    
    def _check_breakpoint(self):
        """Periodically check if breakpoint has changed."""
        self._update_breakpoint()
    
    def _update_breakpoint(self):
        """Update the current breakpoint based on screen size."""
        screen_width = self._get_screen_width()
        
        # Determine new breakpoint
        new_breakpoint = self._get_breakpoint_for_width(screen_width)
        
        # Update if changed
        if new_breakpoint != self.current_breakpoint:
            self.current_breakpoint = new_breakpoint
            self.breakpoint_changed.emit(new_breakpoint.value)
            self.spacing_updated.emit()
    
    def _get_screen_width(self) -> int:
        """Get the current screen width.
        
        Returns:
            Screen width in pixels
        """
        app = QApplication.instance()
        if app and app.primaryScreen():
            return app.primaryScreen().geometry().width()
        return 1920  # Default fallback
    
    def _get_breakpoint_for_width(self, width: int) -> Breakpoint:
        """Get breakpoint for a given screen width.
        
        Args:
            width: Screen width in pixels
            
        Returns:
            Appropriate breakpoint
        """
        for breakpoint, threshold in self.breakpoints.items():
            if width < threshold:
                return breakpoint
        
        return Breakpoint.WIDESCREEN
    
    def get_responsive_spacing(self, base_spacing: Union[int, SpacingUnit], 
                              touch_friendly: bool = False) -> int:
        """Get responsive spacing value for current breakpoint.
        
        Args:
            base_spacing: Base spacing value
            touch_friendly: Whether to apply touch-friendly adjustments
            
        Returns:
            Responsive spacing value
        """
        # Convert SpacingUnit to pixels if needed
        if isinstance(base_spacing, SpacingUnit):
            base_value = base_spacing.value
        else:
            base_value = base_spacing
        
        # Get base multiplier
        multiplier = self.spacing_multipliers[self.current_breakpoint]
        
        # Apply touch-friendly adjustment if needed
        if touch_friendly:
            touch_multiplier = self.touch_spacing_multipliers[self.current_breakpoint]
            multiplier *= touch_multiplier
        
        # Calculate responsive spacing
        responsive_spacing = int(base_value * multiplier)
        
        # Ensure minimum spacing for usability
        return max(responsive_spacing, 4)  # Minimum 4px
    
    def get_breakpoint_spacing(self, breakpoint: Breakpoint, 
                              base_spacing: Union[int, SpacingUnit],
                              touch_friendly: bool = False) -> int:
        """Get spacing for a specific breakpoint.
        
        Args:
            breakpoint: Target breakpoint
            base_spacing: Base spacing value
            touch_friendly: Whether to apply touch-friendly adjustments
            
        Returns:
            Spacing value for the specified breakpoint
        """
        # Convert SpacingUnit to pixels if needed
        if isinstance(base_spacing, SpacingUnit):
            base_value = base_spacing.value
        else:
            base_value = base_spacing
        
        # Get multiplier for specific breakpoint
        multiplier = self.spacing_multipliers[breakpoint]
        
        # Apply touch-friendly adjustment if needed
        if touch_friendly:
            touch_multiplier = self.touch_spacing_multipliers[breakpoint]
            multiplier *= touch_multiplier
        
        # Calculate spacing
        responsive_spacing = int(base_value * multiplier)
        
        # Ensure minimum spacing
        return max(responsive_spacing, 4)
    
    def get_current_breakpoint(self) -> Breakpoint:
        """Get the current breakpoint.
        
        Returns:
            Current breakpoint
        """
        return self.current_breakpoint
    
    def get_breakpoint_name(self) -> str:
        """Get the current breakpoint name.
        
        Returns:
            Current breakpoint name as string
        """
        return self.current_breakpoint.value
    
    def is_mobile(self) -> bool:
        """Check if current breakpoint is mobile.
        
        Returns:
            True if mobile breakpoint
        """
        return self.current_breakpoint == Breakpoint.MOBILE
    
    def is_tablet(self) -> bool:
        """Check if current breakpoint is tablet.
        
        Returns:
            True if tablet breakpoint
        """
        return self.current_breakpoint == Breakpoint.TABLET
    
    def is_desktop(self) -> bool:
        """Check if current breakpoint is desktop.
        
        Returns:
            True if desktop breakpoint
        """
        return self.current_breakpoint == Breakpoint.DESKTOP
    
    def is_widescreen(self) -> bool:
        """Check if current breakpoint is widescreen.
        
        Returns:
            True if widescreen breakpoint
        """
        return self.current_breakpoint == Breakpoint.WIDESCREEN
    
    def get_spacing_info(self) -> Dict[str, any]:
        """Get information about current responsive spacing.
        
        Returns:
            Dictionary with spacing information
        """
        return {
            'current_breakpoint': self.current_breakpoint.value,
            'screen_width': self._get_screen_width(),
            'base_multiplier': self.spacing_multipliers[self.current_breakpoint],
            'touch_multiplier': self.touch_spacing_multipliers[self.current_breakpoint],
            'effective_multiplier': (
                self.spacing_multipliers[self.current_breakpoint] * 
                self.touch_spacing_multipliers[self.current_breakpoint]
            )
        }


class ResponsiveSpacingManager:
    """Manager class for responsive spacing across the application."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern for responsive spacing manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the responsive spacing manager."""
        if not hasattr(self, 'initialized'):
            self.responsive_spacing = ResponsiveSpacing()
            self.initialized = True
    
    def get_responsive_spacing(self, base_spacing: Union[int, SpacingUnit], 
                              touch_friendly: bool = False) -> int:
        """Get responsive spacing value.
        
        Args:
            base_spacing: Base spacing value
            touch_friendly: Whether to apply touch-friendly adjustments
            
        Returns:
            Responsive spacing value
        """
        return self.responsive_spacing.get_responsive_spacing(base_spacing, touch_friendly)
    
    def get_current_breakpoint(self) -> Breakpoint:
        """Get current breakpoint.
        
        Returns:
            Current breakpoint
        """
        return self.responsive_spacing.get_current_breakpoint()
    
    def connect_breakpoint_changed(self, callback):
        """Connect to breakpoint changed signal.
        
        Args:
            callback: Function to call when breakpoint changes
        """
        self.responsive_spacing.breakpoint_changed.connect(callback)
    
    def connect_spacing_updated(self, callback):
        """Connect to spacing updated signal.
        
        Args:
            callback: Function to call when spacing updates
        """
        self.responsive_spacing.spacing_updated.connect(callback)


# Global instance for easy access
responsive_spacing_manager = ResponsiveSpacingManager()
