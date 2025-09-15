"""
Focus management system for improved accessibility.

This module provides:
- Logical focus order
- Focus trapping for modals
- Focus restoration
- Focus indicators
- Focus debugging tools
"""

from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

from gui.utils.logger import get_logger


class FocusState(Enum):
    """Focus states for elements."""
    UNFOCUSED = "unfocused"
    FOCUSED = "focused"
    FOCUS_VISIBLE = "focus_visible"
    FOCUS_WITHIN = "focus_within"


class FocusTrapMode(Enum):
    """Focus trap modes for different contexts."""
    NONE = "none"
    MODAL = "modal"
    DIALOG = "dialog"
    MENU = "menu"
    TOOLTIP = "tooltip"


@dataclass
class FocusTrap:
    """Focus trap configuration."""
    container_id: str
    mode: FocusTrapMode
    first_focusable: str
    last_focusable: str
    escape_handler: Optional[Callable] = None
    return_focus: Optional[str] = None
    active: bool = True


@dataclass
class FocusHistory:
    """Focus history entry."""
    element_id: str
    timestamp: float
    context: str
    navigation_type: str


class FocusManagement:
    """Focus management system for improved accessibility."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._focus_traps: Dict[str, FocusTrap] = {}
        self._focus_history: List[FocusHistory] = []
        self._focus_restoration_stack: List[str] = []
        self._current_focus_trap: Optional[str] = None
        self._focus_debug_mode = False
        self._focus_logging_enabled = True
        
        # Focus management settings
        self._max_history_size = 100
        self._focus_restoration_enabled = True
        self._auto_focus_management = True
        
        self.logger.info("FocusManagement system initialized")
    
    def create_focus_trap(self, trap: FocusTrap) -> str:
        """Create a focus trap for modal dialogs or menus."""
        trap_id = f"trap_{trap.container_id}_{trap.mode.value}"
        self._focus_traps[trap_id] = trap
        
        if trap.active:
            self._activate_focus_trap(trap_id)
        
        self.logger.info(f"Created focus trap: {trap_id}")
        return trap_id
    
    def activate_focus_trap(self, trap_id: str) -> bool:
        """Activate a focus trap."""
        if trap_id not in self._focus_traps:
            self.logger.warning(f"Cannot activate unknown focus trap: {trap_id}")
            return False
        
        trap = self._focus_traps[trap_id]
        
        # Store current focus for restoration
        if self._focus_restoration_enabled:
            self._focus_restoration_stack.append(self._get_current_focus())
        
        # Set the trap as active
        self._current_focus_trap = trap_id
        
        # Focus the first focusable element in the trap
        if trap.first_focusable:
            self._set_focus_to_element(trap.first_focusable)
        
        self.logger.info(f"Activated focus trap: {trap_id}")
        return True
    
    def deactivate_focus_trap(self, trap_id: str) -> bool:
        """Deactivate a focus trap."""
        if trap_id not in self._focus_traps:
            self.logger.warning(f"Cannot deactivate unknown focus trap: {trap_id}")
            return False
        
        trap = self._focus_traps[trap_id]
        
        # Restore focus if available
        if self._focus_restoration_enabled and self._focus_restoration_stack:
            previous_focus = self._focus_restoration_stack.pop()
            if previous_focus:
                self._set_focus_to_element(previous_focus)
        
        # Clear current trap
        if self._current_focus_trap == trap_id:
            self._current_focus_trap = None
        
        self.logger.info(f"Deactivated focus trap: {trap_id}")
        return True
    
    def is_focus_trapped(self) -> bool:
        """Check if focus is currently trapped."""
        return self._current_focus_trap is not None
    
    def get_current_focus_trap(self) -> Optional[FocusTrap]:
        """Get the currently active focus trap."""
        if self._current_focus_trap:
            return self._focus_traps[self._current_focus_trap]
        return None
    
    def handle_escape_key(self) -> bool:
        """Handle escape key press in focus trap context."""
        if not self._current_focus_trap:
            return False
        
        trap = self._focus_traps[self._current_focus_trap]
        if trap.escape_handler:
            try:
                trap.escape_handler()
                self.logger.info("Executed escape handler for focus trap")
                return True
            except Exception as e:
                self.logger.error(f"Error executing escape handler: {e}")
                return False
        
        # Default: deactivate the trap
        self.deactivate_focus_trap(self._current_focus_trap)
        return True
    
    def set_focus_order(self, container_id: str, focus_order: List[str]) -> None:
        """Set the logical focus order for elements in a container."""
        # This would integrate with the keyboard navigation system
        # to ensure logical tab order
        self.logger.info(f"Set focus order for container {container_id}: {focus_order}")
    
    def get_focus_order(self, container_id: str) -> List[str]:
        """Get the logical focus order for elements in a container."""
        # This would return the logical focus order
        # For now, return empty list
        return []
    
    def save_focus_state(self, element_id: str, context: str = "default") -> None:
        """Save the current focus state for restoration."""
        if not self._focus_restoration_enabled:
            return
        
        focus_state = FocusHistory(
            element_id=element_id,
            timestamp=self._get_current_timestamp(),
            context=context,
            navigation_type="manual"
        )
        
        self._focus_history.append(focus_state)
        
        # Limit history size
        if len(self._focus_history) > self._max_history_size:
            self._focus_history.pop(0)
        
        if self._focus_logging_enabled:
            self.logger.debug(f"Saved focus state: {element_id} in {context}")
    
    def restore_focus_state(self, context: str = "default") -> Optional[str]:
        """Restore focus to the last saved state for a context."""
        if not self._focus_restoration_enabled:
            return None
        
        # Find the most recent focus state for the context
        for focus_state in reversed(self._focus_history):
            if focus_state.context == context:
                if self._set_focus_to_element(focus_state.element_id):
                    self.logger.info(f"Restored focus to {focus_state.element_id} in {context}")
                    return focus_state.element_id
        
        self.logger.warning(f"No focus state found for context: {context}")
        return None
    
    def get_focus_history(self, context: str = None) -> List[FocusHistory]:
        """Get focus history, optionally filtered by context."""
        if context is None:
            return self._focus_history.copy()
        
        return [f for f in self._focus_history if f.context == context]
    
    def clear_focus_history(self, context: str = None) -> None:
        """Clear focus history, optionally filtered by context."""
        if context is None:
            self._focus_history.clear()
            self.logger.info("Cleared all focus history")
        else:
            self._focus_history = [f for f in self._focus_history if f.context != context]
            self.logger.info(f"Cleared focus history for context: {context}")
    
    def enable_focus_debug_mode(self, enabled: bool = True) -> None:
        """Enable or disable focus debug mode."""
        self._focus_debug_mode = enabled
        self.logger.info(f"Focus debug mode {'enabled' if enabled else 'disabled'}")
    
    def is_focus_debug_mode_enabled(self) -> bool:
        """Check if focus debug mode is enabled."""
        return self._focus_debug_mode
    
    def enable_focus_logging(self, enabled: bool = True) -> None:
        """Enable or disable focus logging."""
        self._focus_logging_enabled = enabled
        self.logger.info(f"Focus logging {'enabled' if enabled else 'disabled'}")
    
    def is_focus_logging_enabled(self) -> bool:
        """Check if focus logging is enabled."""
        return self._focus_logging_enabled
    
    def get_focus_debug_info(self) -> Dict[str, Any]:
        """Get debug information about the current focus state."""
        debug_info = {
            'current_focus_trap': self._current_focus_trap,
            'focus_traps_count': len(self._focus_traps),
            'focus_history_size': len(self._focus_history),
            'focus_restoration_stack_size': len(self._focus_restoration_stack),
            'focus_restoration_enabled': self._focus_restoration_enabled,
            'auto_focus_management': self._auto_focus_management,
            'focus_debug_mode': self._focus_debug_mode,
            'focus_logging_enabled': self._focus_logging_enabled
        }
        
        if self._current_focus_trap:
            trap = self._focus_traps[self._current_focus_trap]
            debug_info['active_trap'] = {
                'container_id': trap.container_id,
                'mode': trap.mode.value,
                'first_focusable': trap.first_focusable,
                'last_focusable': trap.last_focusable,
                'active': trap.active
            }
        
        return debug_info
    
    def validate_focus_trap(self, trap_id: str) -> Dict[str, bool]:
        """Validate a focus trap configuration."""
        if trap_id not in self._focus_traps:
            return {'exists': False}
        
        trap = self._focus_traps[trap_id]
        validation = {
            'exists': True,
            'has_first_focusable': bool(trap.first_focusable),
            'has_last_focusable': bool(trap.last_focusable),
            'has_escape_handler': trap.escape_handler is not None,
            'has_return_focus': bool(trap.return_focus),
            'is_active': trap.active
        }
        
        return validation
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for focus management."""
        return {
            'focus_traps': "Use focus traps for modal dialogs and menus",
            'focus_restoration': "Always restore focus when closing modals",
            'logical_order': "Ensure logical focus order for all elements",
            'escape_handling': "Provide escape key handlers for all focus traps",
            'focus_indicators': "Show clear focus indicators for all focusable elements"
        }
    
    def _get_current_focus(self) -> Optional[str]:
        """Get the currently focused element ID."""
        # This would integrate with the keyboard navigation system
        # For now, return None
        return None
    
    def _set_focus_to_element(self, element_id: str) -> bool:
        """Set focus to a specific element."""
        # This would integrate with the keyboard navigation system
        # For now, just log the action
        if self._focus_logging_enabled:
            self.logger.info(f"Setting focus to element: {element_id}")
        return True
    
    def _get_current_timestamp(self) -> float:
        """Get current timestamp for focus history."""
        import time
        return time.time()


# Global instance for easy access
focus_management = FocusManagement()
