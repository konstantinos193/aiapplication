#!/usr/bin/env python3
"""
Screen Reader Integration system for comprehensive accessibility support.

This module provides integration with various screen readers, announcement
management, navigation support, and user profile management.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Set, Callable, Any
import logging
import time
from threading import Lock

logger = logging.getLogger(__name__)


class AnnouncementPriority(Enum):
    """Priority levels for screen reader announcements."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class NavigationMode(Enum):
    """Different navigation modes for screen reader users."""
    LINEAR = "linear"
    HIERARCHICAL = "hierarchical"
    LANDMARK = "landmark"
    HEADING = "heading"
    TAB = "tab"
    LIST = "list"
    TABLE = "table"
    FORM = "form"


class ScreenReaderType(Enum):
    """Supported screen reader types."""
    NVDA = "nvda"
    JAWS = "jaws"
    VOICEOVER = "voiceover"
    ORCA = "orca"
    GENERIC = "generic"
    CUSTOM = "custom"


class AnnouncementType(Enum):
    """Types of announcements that can be made."""
    STATUS = "status"
    ERROR = "error"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    INTERACTION = "interaction"
    NAVIGATION = "navigation"
    SYSTEM = "system"


@dataclass(frozen=True)
class ScreenReaderAnnouncement:
    """Represents a screen reader announcement."""
    message: str
    priority: AnnouncementPriority = AnnouncementPriority.NORMAL
    announcement_type: AnnouncementType = AnnouncementType.INFO
    context: str = "default"
    element_id: str = ""
    role: str = ""
    timestamp: float = field(default_factory=time.time)
    user_id: str = "default"
    screen_reader: ScreenReaderType = ScreenReaderType.GENERIC


@dataclass(frozen=True)
class NavigationElement:
    """Represents a navigable element for screen readers."""
    element_id: str
    role: str
    label: str
    description: str = ""
    level: int = 0
    parent_id: str = ""
    children: List[str] = field(default_factory=list)
    accessible: bool = True
    focusable: bool = True
    visible: bool = True
    order: int = 0


@dataclass(frozen=True)
class ScreenReaderProfile:
    """User profile for screen reader preferences."""
    user_id: str
    screen_reader: ScreenReaderType
    navigation_preference: NavigationMode = NavigationMode.LINEAR
    announcement_preference: AnnouncementPriority = AnnouncementPriority.NORMAL
    language: str = "en"
    speech_rate: float = 1.0
    pitch: float = 1.0
    volume: float = 1.0
    enable_sound_effects: bool = True
    enable_braille: bool = False
    custom_shortcuts: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class NavigationContext:
    """Context information for navigation operations."""
    current_element: str
    previous_element: str = ""
    next_element: str = ""
    parent_element: str = ""
    level: int = 0
    mode: NavigationMode = NavigationMode.LINEAR
    history: List[str] = field(default_factory=list)


class ScreenReaderIntegration:
    """
    Comprehensive screen reader integration system.
    
    This class manages announcements, navigation, user profiles, and provides
    integration with various screen reader technologies.
    """
    
    def __init__(self):
        self._announcements: List[ScreenReaderAnnouncement] = []
        self._navigation_elements: Dict[str, NavigationElement] = {}
        self._user_profiles: Dict[str, ScreenReaderProfile] = {}
        self._current_user: str = "default"
        self._navigation_context: NavigationContext = NavigationContext("")
        self._announcement_callbacks: Dict[ScreenReaderType, Callable] = {}
        self._navigation_callbacks: Dict[ScreenReaderType, Callable] = {}
        self._lock = Lock()
        self._logger = logging.getLogger(f"{__name__}.ScreenReaderIntegration")
        
        # Initialize default user profile
        self._setup_default_profile()
        self._logger.info("ScreenReaderIntegration initialized")
    
    def _setup_default_profile(self):
        """Setup default user profile."""
        default_profile = ScreenReaderProfile(
            user_id="default",
            screen_reader=ScreenReaderType.GENERIC,
            navigation_preference=NavigationMode.LINEAR,
            announcement_preference=AnnouncementPriority.NORMAL
        )
        self._user_profiles["default"] = default_profile
        self._current_user = "default"
    
    def register_screen_reader(self, screen_reader: ScreenReaderType, 
                              announcement_callback: Callable = None,
                              navigation_callback: Callable = None) -> bool:
        """
        Register a screen reader with custom callbacks.
        
        Args:
            screen_reader: Type of screen reader to register
            announcement_callback: Callback for making announcements
            navigation_callback: Callback for navigation operations
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            if announcement_callback:
                self._announcement_callbacks[screen_reader] = announcement_callback
            if navigation_callback:
                self._navigation_callbacks[screen_reader] = navigation_callback
            
            self._logger.info(f"Registered screen reader: {screen_reader.value}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to register screen reader {screen_reader.value}: {e}")
            return False
    
    def announce(self, message: str, priority: AnnouncementPriority = AnnouncementPriority.NORMAL,
                announcement_type: AnnouncementType = AnnouncementType.INFO,
                context: str = "default", element_id: str = "", role: str = "") -> bool:
        """
        Make a screen reader announcement.
        
        Args:
            message: Message to announce
            priority: Priority level of the announcement
            announcement_type: Type of announcement
            context: Context where the announcement is made
            element_id: ID of the element being announced
            role: Role of the element being announced
            
        Returns:
            True if announcement was successful, False otherwise
        """
        try:
            with self._lock:
                announcement = ScreenReaderAnnouncement(
                    message=message,
                    priority=priority,
                    announcement_type=announcement_type,
                    context=context,
                    element_id=element_id,
                    role=role,
                    user_id=self._current_user,
                    screen_reader=self._get_current_screen_reader()
                )
                
                self._announcements.append(announcement)
                
                # Call screen reader specific callback if available
                screen_reader = self._get_current_screen_reader()
                if screen_reader in self._announcement_callbacks:
                    try:
                        self._announcement_callbacks[screen_reader](announcement)
                    except Exception as e:
                        self._logger.error(f"Screen reader callback failed: {e}")
                
                self._logger.debug(f"Announcement: {message} ({priority.value})")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to make announcement: {e}")
            return False
    
    def announce_status(self, message: str, element_id: str = "") -> bool:
        """Announce a status message."""
        return self.announce(message, AnnouncementPriority.NORMAL, AnnouncementType.STATUS, 
                           element_id=element_id)
    
    def announce_error(self, message: str, element_id: str = "") -> bool:
        """Announce an error message."""
        return self.announce(message, AnnouncementPriority.HIGH, AnnouncementType.ERROR, 
                           element_id=element_id)
    
    def announce_success(self, message: str, element_id: str = "") -> bool:
        """Announce a success message."""
        return self.announce(message, AnnouncementPriority.NORMAL, AnnouncementType.SUCCESS, 
                           element_id=element_id)
    
    def announce_warning(self, message: str, element_id: str = "") -> bool:
        """Announce a warning message."""
        return self.announce(message, AnnouncementPriority.HIGH, AnnouncementType.WARNING, 
                           element_id=element_id)
    
    def register_navigation_element(self, element: NavigationElement) -> bool:
        """
        Register a navigable element.
        
        Args:
            element: Navigation element to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            with self._lock:
                self._navigation_elements[element.element_id] = element
                
                # Update parent's children list
                if element.parent_id and element.parent_id in self._navigation_elements:
                    parent = self._navigation_elements[element.parent_id]
                    if element.element_id not in parent.children:
                        parent.children.append(element.element_id)
                
                self._logger.debug(f"Registered navigation element: {element.element_id}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to register navigation element {element.element_id}: {e}")
            return False
    
    def get_navigation_element(self, element_id: str) -> Optional[NavigationElement]:
        """Get a navigation element by ID."""
        return self._navigation_elements.get(element_id)
    
    def get_navigation_elements(self) -> Dict[str, NavigationElement]:
        """Get all registered navigation elements."""
        return self._navigation_elements.copy()
    
    def navigate_to_element(self, element_id: str, mode: NavigationMode = None) -> bool:
        """
        Navigate to a specific element.
        
        Args:
            element_id: ID of the element to navigate to
            mode: Navigation mode to use (uses user preference if None)
            
        Returns:
            True if navigation was successful, False otherwise
        """
        try:
            if element_id not in self._navigation_elements:
                self._logger.warning(f"Navigation element {element_id} not found")
                return False
            
            element = self._navigation_elements[element_id]
            if not element.accessible:
                self._logger.warning(f"Element {element_id} is not accessible")
                return False
            
            # Update navigation context
            with self._lock:
                self._navigation_context.previous_element = self._navigation_context.current_element
                self._navigation_context.current_element = element_id
                self._navigation_context.level = element.level
                self._navigation_context.mode = mode or self._get_current_navigation_preference()
                
                if element_id not in self._navigation_context.history:
                    self._navigation_context.history.append(element_id)
            
            # Announce navigation
            self.announce(f"Navigated to {element.label}", AnnouncementPriority.NORMAL, 
                         AnnouncementType.NAVIGATION, element_id=element_id, role=element.role)
            
            # Call screen reader specific navigation callback if available
            screen_reader = self._get_current_screen_reader()
            if screen_reader in self._navigation_callbacks:
                try:
                    self._navigation_callbacks[screen_reader](element, self._navigation_context)
                except Exception as e:
                    self._logger.error(f"Screen reader navigation callback failed: {e}")
            
            self._logger.debug(f"Navigated to element: {element_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to navigate to element {element_id}: {e}")
            return False
    
    def navigate_next(self, mode: NavigationMode = None) -> bool:
        """Navigate to the next element in the current navigation mode."""
        current_element = self._navigation_context.current_element
        if not current_element:
            return False
        
        # Find next element based on navigation mode
        next_element = self._find_next_element(current_element, mode)
        if next_element:
            return self.navigate_to_element(next_element, mode)
        
        return False
    
    def navigate_previous(self, mode: NavigationMode = None) -> bool:
        """Navigate to the previous element in the current navigation mode."""
        current_element = self._navigation_context.current_element
        if not current_element:
            return False
        
        # Find previous element based on navigation mode
        previous_element = self._find_previous_element(current_element, mode)
        if previous_element:
            return self.navigate_to_element(previous_element, mode)
        
        return False
    
    def _find_next_element(self, current_id: str, mode: NavigationMode = None) -> Optional[str]:
        """Find the next element based on navigation mode."""
        mode = mode or self._get_current_navigation_preference()
        current_element = self._navigation_elements.get(current_id)
        if not current_element:
            return None
        
        if mode == NavigationMode.LINEAR:
            # Find next element by order
            all_elements = sorted(self._navigation_elements.values(), key=lambda x: x.order)
            current_index = next((i for i, elem in enumerate(all_elements) 
                                if elem.element_id == current_id), -1)
            if current_index >= 0 and current_index + 1 < len(all_elements):
                return all_elements[current_index + 1].element_id
        
        elif mode == NavigationMode.HIERARCHICAL:
            # Find next child or sibling
            if current_element.children:
                return current_element.children[0]
            else:
                # Find next sibling
                parent = self._navigation_elements.get(current_element.parent_id)
                if parent and parent.children:
                    current_index = parent.children.index(current_id)
                    if current_index + 1 < len(parent.children):
                        return parent.children[current_index + 1]
        
        return None
    
    def _find_previous_element(self, current_id: str, mode: NavigationMode = None) -> Optional[str]:
        """Find the previous element based on navigation mode."""
        mode = mode or self._get_current_navigation_preference()
        current_element = self._navigation_elements.get(current_id)
        if not current_element:
            return None
        
        if mode == NavigationMode.LINEAR:
            # Find previous element by order
            all_elements = sorted(self._navigation_elements.values(), key=lambda x: x.order)
            current_index = next((i for i, elem in enumerate(all_elements) 
                                if elem.element_id == current_id), -1)
            if current_index > 0:
                return all_elements[current_index - 1].element_id
        
        elif mode == NavigationMode.HIERARCHICAL:
            # Find previous sibling or parent
            if current_element.parent_id:
                parent = self._navigation_elements.get(current_element.parent_id)
                if parent and parent.children:
                    current_index = parent.children.index(current_id)
                    if current_index > 0:
                        return parent.children[current_index - 1]
                    else:
                        return current_element.parent_id
        
        return None
    
    def create_user_profile(self, profile: ScreenReaderProfile) -> bool:
        """
        Create or update a user profile.
        
        Args:
            profile: User profile to create/update
            
        Returns:
            True if profile was created successfully, False otherwise
        """
        try:
            with self._lock:
                self._user_profiles[profile.user_id] = profile
                self._logger.info(f"Created/updated user profile: {profile.user_id}")
                return True
        except Exception as e:
            self._logger.error(f"Failed to create user profile {profile.user_id}: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[ScreenReaderProfile]:
        """Get a user profile by ID."""
        return self._user_profiles.get(user_id)
    
    def set_current_user(self, user_id: str) -> bool:
        """Set the current active user."""
        if user_id not in self._user_profiles:
            self._logger.warning(f"User profile {user_id} not found")
            return False
        
        self._current_user = user_id
        self._logger.info(f"Switched to user: {user_id}")
        return True
    
    def get_current_user(self) -> str:
        """Get the current active user ID."""
        return self._current_user
    
    def _get_current_screen_reader(self) -> ScreenReaderType:
        """Get the screen reader type for the current user."""
        profile = self._user_profiles.get(self._current_user)
        return profile.screen_reader if profile else ScreenReaderType.GENERIC
    
    def _get_current_navigation_preference(self) -> NavigationMode:
        """Get the navigation preference for the current user."""
        profile = self._user_profiles.get(self._current_user)
        return profile.navigation_preference if profile else NavigationMode.LINEAR
    
    def get_announcements(self, user_id: str = None, limit: int = None) -> List[ScreenReaderAnnouncement]:
        """Get announcements for a specific user or all users."""
        user_id = user_id or self._current_user
        
        with self._lock:
            user_announcements = [
                ann for ann in self._announcements
                if ann.user_id == user_id
            ]
            
            if limit:
                return user_announcements[-limit:]
            return user_announcements
    
    def clear_announcements(self, user_id: str = None) -> bool:
        """Clear announcements for a specific user or all users."""
        try:
            with self._lock:
                if user_id:
                    self._announcements = [
                        ann for ann in self._announcements
                        if ann.user_id != user_id
                    ]
                else:
                    self._announcements.clear()
                
                self._logger.debug(f"Cleared announcements for user: {user_id or 'all'}")
                return True
        except Exception as e:
            self._logger.error(f"Failed to clear announcements: {e}")
            return False
    
    def get_navigation_context(self) -> NavigationContext:
        """Get the current navigation context."""
        return self._navigation_context
    
    def get_accessibility_summary(self) -> Dict[str, any]:
        """Get a summary of accessibility information."""
        return {
            "current_user": self._current_user,
            "total_users": len(self._user_profiles),
            "total_navigation_elements": len(self._navigation_elements),
            "total_announcements": len(self._announcements),
            "current_navigation_context": {
                "current_element": self._navigation_context.current_element,
                "mode": self._navigation_context.mode.value,
                "level": self._navigation_context.level
            },
            "registered_screen_readers": [sr.value for sr in self._announcement_callbacks.keys()],
            "user_profiles": {
                uid: {
                    "screen_reader": profile.screen_reader.value,
                    "navigation_preference": profile.navigation_preference.value,
                    "announcement_preference": profile.announcement_preference.value
                }
                for uid, profile in self._user_profiles.items()
            }
        }
    
    def validate_navigation_structure(self) -> Dict[str, any]:
        """Validate the navigation structure for accessibility issues."""
        issues = []
        warnings = []
        
        # Check for orphaned elements
        for element_id, element in self._navigation_elements.items():
            if element.parent_id and element.parent_id not in self._navigation_elements:
                issues.append(f"Element {element_id} has invalid parent {element.parent_id}")
            
            if not element.label:
                warnings.append(f"Element {element_id} has no label")
            
            if not element.accessible:
                warnings.append(f"Element {element_id} is marked as inaccessible")
        
        # Check for circular references
        visited = set()
        def check_circular(element_id: str, path: List[str]) -> bool:
            if element_id in path:
                issues.append(f"Circular reference detected: {' -> '.join(path + [element_id])}")
                return True
            
            if element_id in visited:
                return False
            
            visited.add(element_id)
            element = self._navigation_elements.get(element_id)
            if element and element.parent_id:
                return check_circular(element.parent_id, path + [element_id])
            return False
        
        for element_id in self._navigation_elements:
            if element_id not in visited:
                check_circular(element_id, [])
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues,
            "warnings": warnings,
            "total_elements": len(self._navigation_elements),
            "accessible_elements": sum(1 for elem in self._navigation_elements.values() if elem.accessible),
            "focusable_elements": sum(1 for elem in self._navigation_elements.values() if elem.focusable)
        }
