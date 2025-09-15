"""
Keyboard navigation system for improved accessibility.

This module provides:
- Tab order management
- Keyboard shortcut system
- Navigation patterns (arrow keys, enter, space)
- Focus management
- Keyboard event handling
"""

from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

from gui.utils.logger import get_logger


class NavigationDirection(Enum):
    """Navigation directions for keyboard navigation."""
    FORWARD = "forward"
    BACKWARD = "backward"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class NavigationMode(Enum):
    """Navigation modes for different contexts."""
    LINEAR = "linear"          # Tab-based navigation
    GRID = "grid"             # Grid-based navigation
    HIERARCHICAL = "hierarchical"  # Tree-based navigation
    MODAL = "modal"           # Modal dialog navigation


@dataclass
class KeyboardShortcut:
    """Keyboard shortcut definition."""
    key: str
    modifiers: List[str] = field(default_factory=list)
    description: str = ""
    action: Optional[Callable] = None
    context: str = "global"
    enabled: bool = True


@dataclass
class FocusableElement:
    """Focusable element information."""
    widget_id: str
    widget_type: str
    tab_order: int
    navigation_group: str = "default"
    accepts_focus: bool = True
    accepts_tab: bool = True
    accepts_arrow_keys: bool = False
    accepts_enter: bool = False
    accepts_space: bool = False
    custom_actions: Dict[str, Callable] = field(default_factory=dict)


class KeyboardNavigation:
    """Keyboard navigation engine for improved accessibility."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._focusable_elements: Dict[str, FocusableElement] = {}
        self._current_focus: Optional[str] = None
        self._focus_history: List[str] = []
        self._navigation_mode = NavigationMode.LINEAR
        self._shortcuts: Dict[str, KeyboardShortcut] = {}
        self._navigation_groups: Dict[str, List[str]] = {}
        self._modal_stack: List[str] = []
        
        # Default keyboard shortcuts
        self._setup_default_shortcuts()
        
        self.logger.info("KeyboardNavigation system initialized")
    
    def _setup_default_shortcuts(self):
        """Setup default keyboard shortcuts."""
        default_shortcuts = [
            KeyboardShortcut("Tab", [], "Navigate to next element", context="navigation"),
            KeyboardShortcut("Shift+Tab", ["Shift"], "Navigate to previous element", context="navigation"),
            KeyboardShortcut("Enter", [], "Activate/confirm element", context="activation"),
            KeyboardShortcut("Space", [], "Toggle/activate element", context="activation"),
            KeyboardShortcut("Escape", [], "Cancel/close", context="navigation"),
            KeyboardShortcut("F1", [], "Help", context="help"),
            KeyboardShortcut("Ctrl+S", ["Ctrl"], "Save", context="file"),
            KeyboardShortcut("Ctrl+Z", ["Ctrl"], "Undo", context="edit"),
            KeyboardShortcut("Ctrl+Y", ["Ctrl"], "Redo", context="edit"),
            KeyboardShortcut("Ctrl+C", ["Ctrl"], "Copy", context="edit"),
            KeyboardShortcut("Ctrl+V", ["Ctrl"], "Paste", context="edit"),
            KeyboardShortcut("Ctrl+X", ["Ctrl"], "Cut", context="edit"),
            KeyboardShortcut("Ctrl+A", ["Ctrl"], "Select all", context="edit"),
            KeyboardShortcut("Ctrl+F", ["Ctrl"], "Find", context="search"),
            KeyboardShortcut("Ctrl+H", ["Ctrl"], "Replace", context="search"),
        ]
        
        for shortcut in default_shortcuts:
            self.register_shortcut(shortcut)
    
    def register_focusable_element(self, element: FocusableElement) -> None:
        """Register a focusable element."""
        self._focusable_elements[element.widget_id] = element
        
        # Add to navigation group
        if element.navigation_group not in self._navigation_groups:
            self._navigation_groups[element.navigation_group] = []
        self._navigation_groups[element.navigation_group].append(element.widget_id)
        
        # Sort by tab order
        self._navigation_groups[element.navigation_group].sort(
            key=lambda x: self._focusable_elements[x].tab_order
        )
        
        self.logger.info(f"Registered focusable element: {element.widget_id}")
    
    def unregister_focusable_element(self, widget_id: str) -> None:
        """Unregister a focusable element."""
        if widget_id in self._focusable_elements:
            element = self._focusable_elements[widget_id]
            
            # Remove from navigation group
            if element.navigation_group in self._navigation_groups:
                self._navigation_groups[element.navigation_group].remove(widget_id)
            
            # Remove from focus history
            if widget_id in self._focus_history:
                self._focus_history.remove(widget_id)
            
            # Clear current focus if it was this element
            if self._current_focus == widget_id:
                self._current_focus = None
            
            del self._focusable_elements[widget_id]
            self.logger.info(f"Unregistered focusable element: {widget_id}")
    
    def set_focus(self, widget_id: str) -> bool:
        """Set focus to a specific element."""
        if widget_id not in self._focusable_elements:
            self.logger.warning(f"Cannot set focus to unknown element: {widget_id}")
            return False
        
        element = self._focusable_elements[widget_id]
        if not element.accepts_focus:
            self.logger.warning(f"Element {widget_id} does not accept focus")
            return False
        
        # Update focus history
        if self._current_focus in self._focus_history:
            self._focus_history.remove(self._current_focus)
        self._focus_history.append(self._current_focus)
        
        # Limit history size
        if len(self._focus_history) > 50:
            self._focus_history.pop(0)
        
        self._current_focus = widget_id
        self.logger.info(f"Focus set to: {widget_id}")
        return True
    
    def get_current_focus(self) -> Optional[str]:
        """Get the currently focused element ID."""
        return self._current_focus
    
    def navigate(self, direction: NavigationDirection) -> Optional[str]:
        """Navigate to the next element in the specified direction."""
        if not self._current_focus:
            # If no current focus, focus the first element
            return self._focus_first_element()
        
        current_element = self._focusable_elements.get(self._current_focus)
        if not current_element:
            return None
        
        if direction in [NavigationDirection.FORWARD, NavigationDirection.BACKWARD]:
            return self._navigate_linear(direction)
        elif direction in [NavigationDirection.UP, NavigationDirection.DOWN, 
                          NavigationDirection.LEFT, NavigationDirection.RIGHT]:
            return self._navigate_grid(direction)
        
        return None
    
    def _navigate_linear(self, direction: NavigationDirection) -> Optional[str]:
        """Navigate linearly (forward/backward)."""
        current_element = self._focusable_elements[self._current_focus]
        group = current_element.navigation_group
        
        if group not in self._navigation_groups:
            return None
        
        group_elements = self._navigation_groups[group]
        current_index = group_elements.index(self._current_focus)
        
        if direction == NavigationDirection.FORWARD:
            next_index = (current_index + 1) % len(group_elements)
        else:  # BACKWARD
            next_index = (current_index - 1) % len(group_elements)
        
        next_widget_id = group_elements[next_index]
        next_element = self._focusable_elements[next_widget_id]
        
        # Skip elements that don't accept tab navigation
        attempts = 0
        while not next_element.accepts_tab and attempts < len(group_elements):
            if direction == NavigationDirection.FORWARD:
                next_index = (next_index + 1) % len(group_elements)
            else:
                next_index = (next_index - 1) % len(group_elements)
            next_widget_id = group_elements[next_index]
            next_element = self._focusable_elements[next_widget_id]
            attempts += 1
        
        if next_element.accepts_tab:
            self.set_focus(next_widget_id)
            return next_widget_id
        
        return None
    
    def _navigate_grid(self, direction: NavigationDirection) -> Optional[str]:
        """Navigate in a grid pattern (up/down/left/right)."""
        # This is a simplified grid navigation - in a real implementation,
        # you'd need to know the actual grid layout
        current_element = self._focusable_elements[self._current_focus]
        
        if not current_element.accepts_arrow_keys:
            return None
        
        # For now, fall back to linear navigation
        if direction in [NavigationDirection.DOWN, NavigationDirection.RIGHT]:
            return self._navigate_linear(NavigationDirection.FORWARD)
        else:
            return self._navigate_linear(NavigationDirection.BACKWARD)
    
    def _focus_first_element(self) -> Optional[str]:
        """Focus the first focusable element."""
        if not self._focusable_elements:
            return None
        
        # Find the element with the lowest tab order
        first_element = min(
            self._focusable_elements.values(),
            key=lambda x: x.tab_order
        )
        
        if first_element.accepts_focus:
            self.set_focus(first_element.widget_id)
            return first_element.widget_id
        
        return None
    
    def register_shortcut(self, shortcut: KeyboardShortcut) -> None:
        """Register a keyboard shortcut."""
        shortcut_key = self._create_shortcut_key(shortcut)
        self._shortcuts[shortcut_key] = shortcut
        self.logger.info(f"Registered shortcut: {shortcut_key}")
    
    def unregister_shortcut(self, shortcut: KeyboardShortcut) -> None:
        """Unregister a keyboard shortcut."""
        shortcut_key = self._create_shortcut_key(shortcut)
        if shortcut_key in self._shortcuts:
            del self._shortcuts[shortcut_key]
            self.logger.info(f"Unregistered shortcut: {shortcut_key}")
    
    def _create_shortcut_key(self, shortcut: KeyboardShortcut) -> str:
        """Create a unique key for a shortcut."""
        modifiers = "+".join(sorted(shortcut.modifiers)) if shortcut.modifiers else ""
        if modifiers:
            return f"{modifiers}+{shortcut.key}"
        return shortcut.key
    
    def handle_key_event(self, key: str, modifiers: List[str] = None) -> bool:
        """Handle a key event and execute the appropriate shortcut."""
        if modifiers is None:
            modifiers = []
        
        # Check for navigation keys first
        if self._handle_navigation_key(key, modifiers):
            return True
        
        # Check for registered shortcuts
        shortcut_key = self._create_shortcut_key(KeyboardShortcut(key, modifiers))
        if shortcut_key in self._shortcuts:
            shortcut = self._shortcuts[shortcut_key]
            if shortcut.enabled and shortcut.action:
                try:
                    shortcut.action()
                    self.logger.info(f"Executed shortcut: {shortcut_key}")
                    return True
                except Exception as e:
                    self.logger.error(f"Error executing shortcut {shortcut_key}: {e}")
                    return False
        
        return False
    
    def _handle_navigation_key(self, key: str, modifiers: List[str]) -> bool:
        """Handle navigation-specific key events."""
        if key == "Tab":
            if "Shift" in modifiers:
                self.navigate(NavigationDirection.BACKWARD)
            else:
                self.navigate(NavigationDirection.FORWARD)
            return True
        elif key == "Enter":
            if self._current_focus:
                element = self._focusable_elements[self._current_focus]
                if element.accepts_enter and "enter" in element.custom_actions:
                    element.custom_actions["enter"]()
                    return True
        elif key == " ":
            if self._current_focus:
                element = self._focusable_elements[self._current_focus]
                if element.accepts_space and "space" in element.custom_actions:
                    element.custom_actions["space"]()
                    return True
        
        return False
    
    def set_navigation_mode(self, mode: NavigationMode) -> None:
        """Set the current navigation mode."""
        self._navigation_mode = mode
        self.logger.info(f"Navigation mode set to: {mode.value}")
    
    def get_navigation_mode(self) -> NavigationMode:
        """Get the current navigation mode."""
        return self._navigation_mode
    
    def create_navigation_group(self, group_name: str, element_ids: List[str]) -> None:
        """Create a navigation group with specific elements."""
        self._navigation_groups[group_name] = element_ids
        self.logger.info(f"Created navigation group: {group_name}")
    
    def get_focusable_elements(self) -> Dict[str, FocusableElement]:
        """Get all registered focusable elements."""
        return self._focusable_elements.copy()
    
    def get_navigation_groups(self) -> Dict[str, List[str]]:
        """Get all navigation groups."""
        return self._navigation_groups.copy()
    
    def get_shortcuts(self, context: str = None) -> List[KeyboardShortcut]:
        """Get shortcuts, optionally filtered by context."""
        if context is None:
            return list(self._shortcuts.values())
        
        return [s for s in self._shortcuts.values() if s.context == context]
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for keyboard navigation."""
        return {
            'tab_order': "Ensure logical tab order for all focusable elements",
            'keyboard_shortcuts': "Provide keyboard shortcuts for common actions",
            'focus_indicators': "Always show clear focus indicators",
            'navigation_modes': "Support multiple navigation modes (linear, grid, hierarchical)",
            'custom_actions': "Implement custom keyboard actions for interactive elements"
        }


# Global instance for easy access
keyboard_navigation = KeyboardNavigation()
