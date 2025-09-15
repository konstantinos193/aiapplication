"""
Keyboard shortcuts system for improved accessibility.

This module provides:
- Common shortcuts (Ctrl+S, Ctrl+Z, etc.)
- Custom shortcut definitions
- Shortcut conflict resolution
- Shortcut help system
- Shortcut customization
"""

from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

from gui.utils.logger import get_logger


class ShortcutCategory(Enum):
    """Categories for keyboard shortcuts."""
    NAVIGATION = "navigation"
    FILE = "file"
    EDIT = "edit"
    VIEW = "view"
    TOOLS = "tools"
    HELP = "help"
    CUSTOM = "custom"


class ShortcutConflictResolution(Enum):
    """Strategies for resolving shortcut conflicts."""
    PRIORITY = "priority"          # Higher priority wins
    CONTEXT = "context"            # Context-specific wins
    DISABLE = "disable"            # Disable conflicting shortcuts
    WARN = "warn"                  # Warn about conflicts
    CUSTOM = "custom"              # Custom resolution logic


@dataclass
class ShortcutDefinition:
    """Detailed shortcut definition."""
    key: str
    modifiers: List[str] = field(default_factory=list)
    description: str = ""
    action: Optional[Callable] = None
    category: ShortcutCategory = ShortcutCategory.CUSTOM
    context: str = "global"
    priority: int = 100
    enabled: bool = True
    help_text: str = ""
    conflict_resolution: ShortcutConflictResolution = ShortcutConflictResolution.PRIORITY


@dataclass
class ShortcutConflict:
    """Information about a shortcut conflict."""
    shortcut_key: str
    conflicting_shortcuts: List[ShortcutDefinition]
    resolution: ShortcutConflictResolution
    resolved: bool = False


class KeyboardShortcuts:
    """Keyboard shortcuts system for improved accessibility."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._shortcuts: Dict[str, ShortcutDefinition] = {}
        self._shortcuts_by_category: Dict[ShortcutCategory, List[str]] = {}
        self._shortcuts_by_context: Dict[str, List[str]] = {}
        self._conflicts: Dict[str, ShortcutConflict] = {}
        self._custom_resolvers: Dict[str, Callable] = {}
        
        # Shortcut settings
        self._conflict_detection_enabled = True
        self._auto_resolve_conflicts = True
        self._shortcut_help_enabled = True
        
        # Setup default shortcuts
        self._setup_default_shortcuts()
        
        self.logger.info("KeyboardShortcuts system initialized")
    
    def _setup_default_shortcuts(self):
        """Setup default keyboard shortcuts."""
        default_shortcuts = [
            # Navigation shortcuts
            ShortcutDefinition("Tab", [], "Navigate to next element", 
                             category=ShortcutCategory.NAVIGATION, context="navigation", priority=1000),
            ShortcutDefinition("Shift+Tab", ["Shift"], "Navigate to previous element", 
                             category=ShortcutCategory.NAVIGATION, context="navigation", priority=1000),
            ShortcutDefinition("Enter", [], "Activate/confirm element", 
                             category=ShortcutCategory.NAVIGATION, context="activation", priority=900),
            ShortcutDefinition("Space", [], "Toggle/activate element", 
                             category=ShortcutCategory.NAVIGATION, context="activation", priority=900),
            ShortcutDefinition("Escape", [], "Cancel/close", 
                             category=ShortcutCategory.NAVIGATION, context="navigation", priority=950),
            
            # File shortcuts
            ShortcutDefinition("Ctrl+S", ["Ctrl"], "Save", 
                             category=ShortcutCategory.FILE, context="file", priority=800),
            ShortcutDefinition("Ctrl+O", ["Ctrl"], "Open", 
                             category=ShortcutCategory.FILE, context="file", priority=800),
            ShortcutDefinition("Ctrl+N", ["Ctrl"], "New", 
                             category=ShortcutCategory.FILE, context="file", priority=800),
            ShortcutDefinition("Ctrl+W", ["Ctrl"], "Close", 
                             category=ShortcutCategory.FILE, context="file", priority=800),
            
            # Edit shortcuts
            ShortcutDefinition("Ctrl+Z", ["Ctrl"], "Undo", 
                             category=ShortcutCategory.EDIT, context="edit", priority=700),
            ShortcutDefinition("Ctrl+Y", ["Ctrl"], "Redo", 
                             category=ShortcutCategory.EDIT, context="edit", priority=700),
            ShortcutDefinition("Ctrl+C", ["Ctrl"], "Copy", 
                             category=ShortcutCategory.EDIT, context="edit", priority=700),
            ShortcutDefinition("Ctrl+V", ["Ctrl"], "Paste", 
                             category=ShortcutCategory.EDIT, context="edit", priority=700),
            ShortcutDefinition("Ctrl+X", ["Ctrl"], "Cut", 
                             category=ShortcutCategory.EDIT, context="edit", priority=700),
            ShortcutDefinition("Ctrl+A", ["Ctrl"], "Select all", 
                             category=ShortcutCategory.EDIT, context="edit", priority=700),
            
            # View shortcuts
            ShortcutDefinition("Ctrl+Plus", ["Ctrl"], "Zoom in", 
                             category=ShortcutCategory.VIEW, context="view", priority=600),
            ShortcutDefinition("Ctrl+Minus", ["Ctrl"], "Zoom out", 
                             category=ShortcutCategory.VIEW, context="view", priority=600),
            ShortcutDefinition("Ctrl+0", ["Ctrl"], "Reset zoom", 
                             category=ShortcutCategory.VIEW, context="view", priority=600),
            ShortcutDefinition("F11", [], "Toggle fullscreen", 
                             category=ShortcutCategory.VIEW, context="view", priority=600),
            
            # Tools shortcuts
            ShortcutDefinition("Ctrl+F", ["Ctrl"], "Find", 
                             category=ShortcutCategory.TOOLS, context="search", priority=500),
            ShortcutDefinition("Ctrl+H", ["Ctrl"], "Replace", 
                             category=ShortcutCategory.TOOLS, context="search", priority=500),
            ShortcutDefinition("Ctrl+D", ["Ctrl"], "Duplicate", 
                             category=ShortcutCategory.TOOLS, context="edit", priority=500),
            
            # Help shortcuts
            ShortcutDefinition("F1", [], "Help", 
                             category=ShortcutCategory.HELP, context="help", priority=400),
            ShortcutDefinition("Ctrl+Shift+H", ["Ctrl", "Shift"], "Context help", 
                             category=ShortcutCategory.HELP, context="help", priority=400),
        ]
        
        for shortcut in default_shortcuts:
            self.register_shortcut(shortcut)
    
    def register_shortcut(self, shortcut: ShortcutDefinition) -> str:
        """Register a keyboard shortcut."""
        shortcut_key = self._create_shortcut_key(shortcut)
        
        # Check for conflicts
        if self._conflict_detection_enabled:
            conflict = self._detect_conflict(shortcut_key, shortcut)
            if conflict:
                self._handle_conflict(conflict)
        
        # Register the shortcut
        self._shortcuts[shortcut_key] = shortcut
        
        # Add to category index
        if shortcut.category not in self._shortcuts_by_category:
            self._shortcuts_by_category[shortcut.category] = []
        self._shortcuts_by_category[shortcut.category].append(shortcut_key)
        
        # Add to context index
        if shortcut.context not in self._shortcuts_by_context:
            self._shortcuts_by_context[shortcut.context] = []
        self._shortcuts_by_context[shortcut.context].append(shortcut_key)
        
        self.logger.info(f"Registered shortcut: {shortcut_key} ({shortcut.description})")
        return shortcut_key
    
    def unregister_shortcut(self, shortcut_key: str) -> bool:
        """Unregister a keyboard shortcut."""
        if shortcut_key not in self._shortcuts:
            return False
        
        shortcut = self._shortcuts[shortcut_key]
        
        # Remove from category index
        if shortcut.category in self._shortcuts_by_category:
            self._shortcuts_by_category[shortcut.category].remove(shortcut_key)
        
        # Remove from context index
        if shortcut.context in self._shortcuts_by_context:
            self._shortcuts_by_context[shortcut.context].remove(shortcut_key)
        
        # Remove from conflicts
        if shortcut_key in self._conflicts:
            del self._conflicts[shortcut_key]
        
        del self._shortcuts[shortcut_key]
        self.logger.info(f"Unregistered shortcut: {shortcut_key}")
        return True
    
    def _create_shortcut_key(self, shortcut: ShortcutDefinition) -> str:
        """Create a unique key for a shortcut."""
        modifiers = "+".join(sorted(shortcut.modifiers)) if shortcut.modifiers else ""
        if modifiers:
            return f"{modifiers}+{shortcut.key}"
        return shortcut.key
    
    def _detect_conflict(self, shortcut_key: str, new_shortcut: ShortcutDefinition) -> Optional[ShortcutConflict]:
        """Detect conflicts with existing shortcuts."""
        if shortcut_key not in self._shortcuts:
            return None
        
        existing_shortcut = self._shortcuts[shortcut_key]
        conflicting_shortcuts = [existing_shortcut, new_shortcut]
        
        return ShortcutConflict(
            shortcut_key=shortcut_key,
            conflicting_shortcuts=conflicting_shortcuts,
            resolution=new_shortcut.conflict_resolution
        )
    
    def _handle_conflict(self, conflict: ShortcutConflict) -> None:
        """Handle a shortcut conflict."""
        self._conflicts[conflict.shortcut_key] = conflict
        
        if self._auto_resolve_conflicts:
            self._resolve_conflict(conflict)
        else:
            self.logger.warning(f"Shortcut conflict detected: {conflict.shortcut_key}")
    
    def _resolve_conflict(self, conflict: ShortcutConflict) -> None:
        """Resolve a shortcut conflict automatically."""
        if conflict.resolution == ShortcutConflictResolution.PRIORITY:
            # Keep the shortcut with higher priority
            highest_priority = max(conflict.conflicting_shortcuts, key=lambda x: x.priority)
            for shortcut in conflict.conflicting_shortcuts:
                if shortcut != highest_priority:
                    shortcut.enabled = False
                    self.logger.info(f"Disabled conflicting shortcut: {shortcut.description}")
        
        elif conflict.resolution == ShortcutConflictResolution.CONTEXT:
            # Keep context-specific shortcuts, disable global ones
            for shortcut in conflict.conflicting_shortcuts:
                if shortcut.context == "global":
                    shortcut.enabled = False
                    self.logger.info(f"Disabled global conflicting shortcut: {shortcut.description}")
        
        elif conflict.resolution == ShortcutConflictResolution.DISABLE:
            # Disable all conflicting shortcuts
            for shortcut in conflict.conflicting_shortcuts:
                shortcut.enabled = False
                self.logger.info(f"Disabled conflicting shortcut: {shortcut.description}")
        
        conflict.resolved = True
        self.logger.info(f"Resolved shortcut conflict: {conflict.shortcut_key}")
    
    def execute_shortcut(self, shortcut_key: str) -> bool:
        """Execute a keyboard shortcut."""
        if shortcut_key not in self._shortcuts:
            return False
        
        shortcut = self._shortcuts[shortcut_key]
        if not shortcut.enabled:
            return False
        
        if shortcut.action:
            try:
                shortcut.action()
                self.logger.info(f"Executed shortcut: {shortcut_key} ({shortcut.description})")
                return True
            except Exception as e:
                self.logger.error(f"Error executing shortcut {shortcut_key}: {e}")
                return False
        
        return False
    
    def get_shortcuts_by_category(self, category: ShortcutCategory) -> List[ShortcutDefinition]:
        """Get shortcuts by category."""
        if category not in self._shortcuts_by_category:
            return []
        
        shortcut_keys = self._shortcuts_by_category[category]
        return [self._shortcuts[key] for key in shortcut_keys if key in self._shortcuts]
    
    def get_shortcuts_by_context(self, context: str) -> List[ShortcutDefinition]:
        """Get shortcuts by context."""
        if context not in self._shortcuts_by_context:
            return []
        
        shortcut_keys = self._shortcuts_by_context[context]
        return [self._shortcuts[key] for key in shortcut_keys if key in self._shortcuts]
    
    def get_all_shortcuts(self) -> List[ShortcutDefinition]:
        """Get all registered shortcuts."""
        return list(self._shortcuts.values())
    
    def get_enabled_shortcuts(self) -> List[ShortcutDefinition]:
        """Get all enabled shortcuts."""
        return [s for s in self._shortcuts.values() if s.enabled]
    
    def get_shortcut_help(self, category: ShortcutCategory = None) -> Dict[str, List[str]]:
        """Get help information for shortcuts."""
        if not self._shortcut_help_enabled:
            return {}
        
        if category:
            shortcuts = self.get_shortcuts_by_category(category)
        else:
            shortcuts = self.get_enabled_shortcuts()
        
        help_info = {}
        for shortcut in shortcuts:
            cat = shortcut.category.value
            if cat not in help_info:
                help_info[cat] = []
            
            shortcut_key = self._create_shortcut_key(shortcut)
            help_text = f"{shortcut_key}: {shortcut.description}"
            if shortcut.help_text:
                help_text += f" - {shortcut.help_text}"
            
            help_info[cat].append(help_text)
        
        return help_info
    
    def get_conflicts(self) -> List[ShortcutConflict]:
        """Get all shortcut conflicts."""
        return list(self._conflicts.values())
    
    def get_unresolved_conflicts(self) -> List[ShortcutConflict]:
        """Get unresolved shortcut conflicts."""
        return [c for c in self._conflicts.values() if not c.resolved]
    
    def resolve_conflict_manually(self, shortcut_key: str, resolution: ShortcutConflictResolution) -> bool:
        """Manually resolve a shortcut conflict."""
        if shortcut_key not in self._conflicts:
            return False
        
        conflict = self._conflicts[shortcut_key]
        conflict.resolution = resolution
        self._resolve_conflict(conflict)
        return True
    
    def register_custom_resolver(self, conflict_type: str, resolver: Callable) -> None:
        """Register a custom conflict resolver."""
        self._custom_resolvers[conflict_type] = resolver
        self.logger.info(f"Registered custom resolver for: {conflict_type}")
    
    def enable_conflict_detection(self, enabled: bool = True) -> None:
        """Enable or disable conflict detection."""
        self._conflict_detection_enabled = enabled
        self.logger.info(f"Conflict detection {'enabled' if enabled else 'disabled'}")
    
    def enable_auto_resolve_conflicts(self, enabled: bool = True) -> None:
        """Enable or disable automatic conflict resolution."""
        self._auto_resolve_conflicts = enabled
        self.logger.info(f"Auto conflict resolution {'enabled' if enabled else 'disabled'}")
    
    def enable_shortcut_help(self, enabled: bool = True) -> None:
        """Enable or disable shortcut help system."""
        self._shortcut_help_enabled = enabled
        self.logger.info(f"Shortcut help {'enabled' if enabled else 'disabled'}")
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for keyboard shortcuts."""
        return {
            'standard_shortcuts': "Use standard keyboard shortcuts (Ctrl+S, Ctrl+Z, etc.)",
            'conflict_resolution': "Resolve shortcut conflicts to avoid user confusion",
            'help_system': "Provide help system for all keyboard shortcuts",
            'context_specific': "Use context-specific shortcuts when appropriate",
            'priority_system': "Implement priority system for conflicting shortcuts"
        }


# Global instance for easy access
keyboard_shortcuts = KeyboardShortcuts()
