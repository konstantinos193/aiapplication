"""
Screen reader integration system for accessibility.

This module provides:
- Screen reader announcements
- Accessible descriptions
- Screen reader navigation
- Screen reader testing
- Screen reader optimization
"""

from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import time

from gui.utils.logger import get_logger


class AnnouncementPriority(Enum):
    """Priority levels for screen reader announcements."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class NavigationMode(Enum):
    """Screen reader navigation modes."""
    LINEAR = "linear"
    HIERARCHICAL = "hierarchical"
    LANDMARK = "landmark"
    HEADING = "heading"
    LIST = "list"
    TABLE = "table"
    FORM = "form"


class ScreenReaderType(Enum):
    """Supported screen reader types."""
    NVDA = "nvda"
    JAWS = "jaws"
    VOICEOVER = "voiceover"
    TALKBACK = "talkback"
    ORCA = "orca"
    GENERIC = "generic"


@dataclass
class ScreenReaderAnnouncement:
    """Screen reader announcement configuration."""
    message: str
    priority: AnnouncementPriority = AnnouncementPriority.NORMAL
    context: str = "default"
    timestamp: float = field(default_factory=time.time)
    element_id: Optional[str] = None
    role: Optional[str] = None
    language: str = "en"


@dataclass
class NavigationElement:
    """Navigation element for screen reader navigation."""
    element_id: str
    role: str
    label: str
    description: str = ""
    level: int = 0
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    navigation_type: NavigationMode = NavigationMode.LINEAR
    accessible: bool = True


@dataclass
class ScreenReaderProfile:
    """Screen reader user profile configuration."""
    user_id: str
    screen_reader: ScreenReaderType
    navigation_preference: NavigationMode = NavigationMode.LINEAR
    announcement_preference: AnnouncementPriority = AnnouncementPriority.NORMAL
    language: str = "en"
    custom_shortcuts: Dict[str, str] = field(default_factory=dict)
    accessibility_level: str = "standard"


class ScreenReaderIntegration:
    """Screen reader integration system for accessibility."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self._announcements: List[ScreenReaderAnnouncement] = []
        self._navigation_elements: Dict[str, NavigationElement] = {}
        self._user_profiles: Dict[str, ScreenReaderProfile] = {}
        self._current_user: Optional[str] = None
        self._announcement_queue: List[ScreenReaderAnnouncement] = []
        self._navigation_mode = NavigationMode.LINEAR
        
        # Screen reader settings
        self._announcement_delay = 0.1  # seconds
        self._max_announcement_history = 100
        self._auto_announce_changes = True
        self._navigation_announcements = True
        
        # Setup default user profile
        self._setup_default_profile()
        
        self.logger.info("ScreenReaderIntegration system initialized")
    
    def _setup_default_profile(self):
        """Setup default screen reader user profile."""
        default_profile = ScreenReaderProfile(
            user_id="default",
            screen_reader=ScreenReaderType.GENERIC,
            navigation_preference=NavigationMode.LINEAR,
            announcement_preference=AnnouncementPriority.NORMAL,
            language="en"
        )
        
        self._user_profiles["default"] = default_profile
        self._current_user = "default"
        self.logger.info("Setup default screen reader profile")
    
    def announce(self, message: str, priority: AnnouncementPriority = AnnouncementPriority.NORMAL,
                context: str = "default", element_id: Optional[str] = None, role: Optional[str] = None) -> None:
        """Announce a message to screen readers."""
        announcement = ScreenReaderAnnouncement(
            message=message,
            priority=priority,
            context=context,
            element_id=element_id,
            role=role,
            language=self._get_current_language()
        )
        
        # Add to announcement queue
        self._announcement_queue.append(announcement)
        
        # Add to history
        self._announcements.append(announcement)
        
        # Limit history size
        if len(self._announcements) > self._max_announcement_history:
            self._announcements.pop(0)
        
        # Process announcement queue
        self._process_announcement_queue()
        
        self.logger.info(f"Announced: {message} (priority: {priority.value})")
    
    def announce_change(self, element_id: str, change_type: str, old_value: Any = None, 
                       new_value: Any = None) -> None:
        """Announce a change to an element."""
        if not self._auto_announce_changes:
            return
        
        element = self._navigation_elements.get(element_id)
        if not element:
            return
        
        change_message = f"{element.label} {change_type}"
        if old_value is not None and new_value is not None:
            change_message += f" from {old_value} to {new_value}"
        
        self.announce(
            message=change_message,
            priority=AnnouncementPriority.NORMAL,
            context="change",
            element_id=element_id,
            role=element.role
        )
    
    def announce_navigation(self, element_id: str, navigation_type: str = "focused") -> None:
        """Announce navigation to an element."""
        if not self._navigation_announcements:
            return
        
        element = self._navigation_elements.get(element_id)
        if not element:
            return
        
        navigation_message = f"{element.label}"
        if element.description:
            navigation_message += f", {element.description}"
        
        if navigation_type == "focused":
            navigation_message += ", focused"
        elif navigation_type == "entered":
            navigation_message += ", entered"
        elif navigation_type == "exited":
            navigation_message += ", exited"
        
        self.announce(
            message=navigation_message,
            priority=AnnouncementPriority.LOW,
            context="navigation",
            element_id=element_id,
            role=element.role
        )
    
    def register_navigation_element(self, element: NavigationElement) -> None:
        """Register a navigation element for screen reader navigation."""
        self._navigation_elements[element.element_id] = element
        
        # Update parent's children list
        if element.parent_id and element.parent_id in self._navigation_elements:
            parent = self._navigation_elements[element.parent_id]
            if element.element_id not in parent.children:
                parent.children.append(element.element_id)
        
        self.logger.info(f"Registered navigation element: {element.element_id} ({element.role})")
    
    def unregister_navigation_element(self, element_id: str) -> None:
        """Unregister a navigation element."""
        if element_id in self._navigation_elements:
            element = self._navigation_elements[element_id]
            
            # Remove from parent's children list
            if element.parent_id and element.parent_id in self._navigation_elements:
                parent = self._navigation_elements[element.parent_id]
                if element_id in parent.children:
                    parent.children.remove(element_id)
            
            # Remove children references
            for child_id in element.children:
                if child_id in self._navigation_elements:
                    child = self._navigation_elements[child_id]
                    child.parent_id = None
            
            del self._navigation_elements[element_id]
            self.logger.info(f"Unregistered navigation element: {element_id}")
    
    def navigate_to_element(self, element_id: str, navigation_type: NavigationMode = None) -> bool:
        """Navigate to a specific element."""
        if element_id not in self._navigation_elements:
            self.logger.warning(f"Navigation element not found: {element_id}")
            return False
        
        if navigation_type is None:
            navigation_type = self._navigation_mode
        
        element = self._navigation_elements[element_id]
        
        # Announce navigation
        self.announce_navigation(element_id, "focused")
        
        # Update navigation mode if needed
        if navigation_type != self._navigation_mode:
            self._navigation_mode = navigation_type
            self.logger.info(f"Navigation mode changed to: {navigation_type.value}")
        
        return True
    
    def navigate_next(self, current_element_id: str, navigation_type: NavigationMode = None) -> Optional[str]:
        """Navigate to the next element."""
        if navigation_type is None:
            navigation_type = self._navigation_mode
        
        if navigation_type == NavigationMode.LINEAR:
            return self._navigate_linear_next(current_element_id)
        elif navigation_type == NavigationMode.HIERARCHICAL:
            return self._navigate_hierarchical_next(current_element_id)
        elif navigation_type == NavigationMode.LANDMARK:
            return self._navigate_landmark_next(current_element_id)
        elif navigation_type == NavigationMode.HEADING:
            return self._navigate_heading_next(current_element_id)
        
        return None
    
    def navigate_previous(self, current_element_id: str, navigation_type: NavigationMode = None) -> Optional[str]:
        """Navigate to the previous element."""
        if navigation_type is None:
            navigation_type = self._navigation_mode
        
        if navigation_type == NavigationMode.LINEAR:
            return self._navigate_linear_previous(current_element_id)
        elif navigation_type == NavigationMode.HIERARCHICAL:
            return self._navigate_hierarchical_previous(current_element_id)
        elif navigation_type == NavigationMode.LANDMARK:
            return self._navigate_landmark_previous(current_element_id)
        elif navigation_type == NavigationMode.HEADING:
            return self._navigate_heading_previous(current_element_id)
        
        return None
    
    def _navigate_linear_next(self, current_element_id: str) -> Optional[str]:
        """Navigate to the next element in linear order."""
        element_ids = list(self._navigation_elements.keys())
        if not element_ids:
            return None
        
        try:
            current_index = element_ids.index(current_element_id)
            next_index = (current_index + 1) % len(element_ids)
            next_element_id = element_ids[next_index]
            
            if self.navigate_to_element(next_element_id):
                return next_element_id
        except ValueError:
            pass
        
        return None
    
    def _navigate_linear_previous(self, current_element_id: str) -> Optional[str]:
        """Navigate to the previous element in linear order."""
        element_ids = list(self._navigation_elements.keys())
        if not element_ids:
            return None
        
        try:
            current_index = element_ids.index(current_element_id)
            previous_index = (current_index - 1) % len(element_ids)
            previous_element_id = element_ids[previous_index]
            
            if self.navigate_to_element(previous_element_id):
                return previous_element_id
        except ValueError:
            pass
        
        return None
    
    def _navigate_hierarchical_next(self, current_element_id: str) -> Optional[str]:
        """Navigate to the next element in hierarchical order."""
        current_element = self._navigation_elements.get(current_element_id)
        if not current_element:
            return None
        
        # Try to navigate to first child
        if current_element.children:
            first_child_id = current_element.children[0]
            if self.navigate_to_element(first_child_id):
                return first_child_id
        
        # Try to navigate to next sibling
        if current_element.parent_id:
            parent = self._navigation_elements.get(current_element.parent_id)
            if parent:
                try:
                    current_index = parent.children.index(current_element_id)
                    next_index = (current_index + 1) % len(parent.children)
                    next_sibling_id = parent.children[next_index]
                    
                    if self.navigate_to_element(next_sibling_id):
                        return next_sibling_id
                except ValueError:
                    pass
        
        return None
    
    def _navigate_hierarchical_previous(self, current_element_id: str) -> Optional[str]:
        """Navigate to the previous element in hierarchical order."""
        current_element = self._navigation_elements.get(current_element_id)
        if not current_element:
            return None
        
        # Try to navigate to previous sibling
        if current_element.parent_id:
            parent = self._navigation_elements.get(current_element.parent_id)
            if parent:
                try:
                    current_index = parent.children.index(current_element_id)
                    previous_index = (current_index - 1) % len(parent.children)
                    previous_sibling_id = parent.children[previous_index]
                    
                    if self.navigate_to_element(previous_sibling_id):
                        return previous_sibling_id
                except ValueError:
                    pass
        
        # Try to navigate to parent
        if current_element.parent_id:
            if self.navigate_to_element(current_element.parent_id):
                return current_element.parent_id
        
        return None
    
    def _navigate_landmark_next(self, current_element_id: str) -> Optional[str]:
        """Navigate to the next landmark element."""
        landmark_elements = [
            e for e in self._navigation_elements.values()
            if e.role in ["banner", "navigation", "main", "complementary", "contentinfo", "search"]
        ]
        
        if not landmark_elements:
            return None
        
        try:
            current_index = landmark_elements.index(self._navigation_elements[current_element_id])
            next_index = (current_index + 1) % len(landmark_elements)
            next_landmark = landmark_elements[next_index]
            
            if self.navigate_to_element(next_landmark.element_id):
                return next_landmark.element_id
        except ValueError:
            pass
        
        return None
    
    def _navigate_landmark_previous(self, current_element_id: str) -> Optional[str]:
        """Navigate to the previous landmark element."""
        landmark_elements = [
            e for e in self._navigation_elements.values()
            if e.role in ["banner", "navigation", "main", "complementary", "contentinfo", "search"]
        ]
        
        if not landmark_elements:
            return None
        
        try:
            current_index = landmark_elements.index(self._navigation_elements[current_element_id])
            previous_index = (current_index - 1) % len(landmark_elements)
            previous_landmark = landmark_elements[previous_index]
            
            if self.navigate_to_element(previous_landmark.element_id):
                return previous_landmark.element_id
        except ValueError:
            pass
        
        return None
    
    def _navigate_heading_next(self, current_element_id: str) -> Optional[str]:
        """Navigate to the next heading element."""
        heading_elements = [
            e for e in self._navigation_elements.values()
            if e.role == "heading"
        ]
        
        if not heading_elements:
            return None
        
        try:
            current_index = heading_elements.index(self._navigation_elements[current_element_id])
            next_index = (current_index + 1) % len(heading_elements)
            next_heading = heading_elements[next_index]
            
            if self.navigate_to_element(next_heading.element_id):
                return next_heading.element_id
        except ValueError:
            pass
        
        return None
    
    def _navigate_heading_previous(self, current_element_id: str) -> Optional[str]:
        """Navigate to the previous heading element."""
        heading_elements = [
            e for e in self._navigation_elements.values()
            if e.role == "heading"
        ]
        
        if not heading_elements:
            return None
        
        try:
            current_index = heading_elements.index(self._navigation_elements[current_element_id])
            previous_index = (current_index - 1) % len(heading_elements)
            previous_heading = heading_elements[previous_index]
            
            if self.navigate_to_element(previous_heading.element_id):
                return previous_heading.element_id
        except ValueError:
            pass
        
        return None
    
    def create_user_profile(self, profile: ScreenReaderProfile) -> None:
        """Create a new screen reader user profile."""
        self._user_profiles[profile.user_id] = profile
        self.logger.info(f"Created user profile: {profile.user_id}")
    
    def switch_user_profile(self, user_id: str) -> bool:
        """Switch to a different user profile."""
        if user_id not in self._user_profiles:
            self.logger.warning(f"User profile not found: {user_id}")
            return False
        
        self._current_user = user_id
        profile = self._user_profiles[user_id]
        
        # Update navigation and announcement preferences
        self._navigation_mode = profile.navigation_preference
        self._announcement_delay = self._get_announcement_delay_for_priority(profile.announcement_preference)
        
        self.logger.info(f"Switched to user profile: {user_id}")
        return True
    
    def get_current_user_profile(self) -> Optional[ScreenReaderProfile]:
        """Get the current user profile."""
        if self._current_user:
            return self._user_profiles.get(self._current_user)
        return None
    
    def _get_current_language(self) -> str:
        """Get the current user's language preference."""
        profile = self.get_current_user_profile()
        if profile:
            return profile.language
        return "en"
    
    def _get_announcement_delay_for_priority(self, priority: AnnouncementPriority) -> float:
        """Get announcement delay based on priority."""
        delay_map = {
            AnnouncementPriority.LOW: 0.2,
            AnnouncementPriority.NORMAL: 0.1,
            AnnouncementPriority.HIGH: 0.05,
            AnnouncementPriority.URGENT: 0.0
        }
        return delay_map.get(priority, 0.1)
    
    def _process_announcement_queue(self) -> None:
        """Process the announcement queue."""
        if not self._announcement_queue:
            return
        
        # Process announcements based on priority
        urgent_announcements = [a for a in self._announcement_queue if a.priority == AnnouncementPriority.URGENT]
        high_announcements = [a for a in self._announcement_queue if a.priority == AnnouncementPriority.HIGH]
        normal_announcements = [a for a in self._announcement_queue if a.priority == AnnouncementPriority.NORMAL]
        low_announcements = [a for a in self._announcement_queue if a.priority == AnnouncementPriority.LOW]
        
        # Process in priority order
        for announcement in urgent_announcements + high_announcements + normal_announcements + low_announcements:
            self._process_single_announcement(announcement)
        
        # Clear the queue
        self._announcement_queue.clear()
    
    def _process_single_announcement(self, announcement: ScreenReaderAnnouncement) -> None:
        """Process a single announcement."""
        # In a real implementation, this would send the announcement to the screen reader
        # For now, we just log it
        self.logger.debug(f"Processing announcement: {announcement.message}")
        
        # Simulate screen reader processing delay
        time.sleep(self._announcement_delay)
    
    def get_navigation_summary(self) -> Dict[str, Any]:
        """Get a summary of navigation elements."""
        return {
            'total_elements': len(self._navigation_elements),
            'navigation_mode': self._navigation_mode.value,
            'landmarks': len([e for e in self._navigation_elements.values() if e.role in ["banner", "navigation", "main", "complementary", "contentinfo", "search"]]),
            'headings': len([e for e in self._navigation_elements.values() if e.role == "heading"]),
            'forms': len([e for e in self._navigation_elements.values() if e.role == "form"]),
            'lists': len([e for e in self._navigation_elements.values() if e.role in ["list", "listitem"]]),
            'tables': len([e for e in self._navigation_elements.values() if e.role in ["table", "grid"]])
        }
    
    def get_accessibility_recommendations(self) -> Dict[str, str]:
        """Get accessibility recommendations for screen reader support."""
        return {
            'announcements': "Provide clear, concise announcements for important changes",
            'navigation': "Support multiple navigation modes for different user preferences",
            'landmarks': "Use semantic landmarks to organize page structure",
            'headings': "Maintain proper heading hierarchy for navigation",
            'descriptions': "Provide descriptive text for all interactive elements",
            'changes': "Announce dynamic content changes appropriately"
        }


# Global instance for easy access
screen_reader = ScreenReaderIntegration()
