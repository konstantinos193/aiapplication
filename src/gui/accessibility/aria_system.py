#!/usr/bin/env python3
"""
ARIA (Accessible Rich Internet Applications) system for screen reader support.

This module provides comprehensive ARIA role, state, and property management
for creating accessible user interfaces.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class AriaRole(Enum):
    """Standard ARIA roles for UI elements."""
    BUTTON = "button"
    CHECKBOX = "checkbox"
    DIALOG = "dialog"
    LINK = "link"
    MENU = "menu"
    MENUITEM = "menuitem"
    TAB = "tab"
    TABPANEL = "tabpanel"
    TEXTBOX = "textbox"
    LISTBOX = "listbox"
    OPTION = "option"
    RADIO = "radio"
    RADIOGROUP = "radiogroup"
    SLIDER = "slider"
    SPINBUTTON = "spinbutton"
    COMBOBOX = "combobox"
    GRID = "grid"
    GRIDCELL = "gridcell"
    ROW = "row"
    COLUMNHEADER = "columnheader"
    ROWHEADER = "rowheader"
    NAVIGATION = "navigation"
    BANNER = "banner"
    MAIN = "main"
    COMPLEMENTARY = "complementary"
    CONTENTINFO = "contentinfo"
    SEARCH = "search"
    TOOLBAR = "toolbar"
    TOOLTIP = "tooltip"
    PROGRESSBAR = "progressbar"
    SCROLLBAR = "scrollbar"
    STATUS = "status"
    ALERT = "alert"
    LOG = "log"
    MARQUEE = "marquee"
    TIMER = "timer"


class AriaState(Enum):
    """ARIA state attributes for dynamic content."""
    EXPANDED = "aria-expanded"
    SELECTED = "aria-selected"
    CHECKED = "aria-checked"
    DISABLED = "aria-disabled"
    HIDDEN = "aria-hidden"
    REQUIRED = "aria-required"
    INVALID = "aria-invalid"
    READONLY = "aria-readonly"
    MULTISELECTABLE = "aria-multiselectable"
    ORIENTATION = "aria-orientation"
    SORT = "aria-sort"
    COLSPAN = "aria-colspan"
    ROWSPAN = "aria-rowspan"
    LEVEL = "aria-level"
    POSINSET = "aria-posinset"
    SETSIZE = "aria-setsize"
    CURRENT = "aria-current"
    PRESSED = "aria-pressed"
    DROPEFFECT = "aria-dropeffect"
    DRAGGABLE = "aria-draggable"
    GRABBED = "aria-grabbed"
    AUTCOMPLETE = "aria-autocomplete"
    HASPOPUP = "aria-haspopup"
    MODAL = "aria-modal"
    MULTILINE = "aria-multiline"
    PLACEHOLDER = "aria-placeholder"
    VALUEMIN = "aria-valuemin"
    VALUEMAX = "aria-valuemax"
    VALUENOW = "aria-valuenow"
    VALUETEXT = "aria-valuetext"


class AriaProperty(Enum):
    """ARIA property attributes for element relationships."""
    LABEL = "aria-label"
    LABELLEDBY = "aria-labelledby"
    DESCRIBEDBY = "aria-describedby"
    CONTROLS = "aria-controls"
    OWNS = "aria-owns"
    FLOWTO = "aria-flowto"
    FLOWFROM = "aria-flowfrom"
    ACTIVEDESCENDANT = "aria-activedescendant"
    DESCRIBES = "aria-describes"
    DETAILS = "aria-details"
    ERRORMSG = "aria-errormessage"
    HELP = "aria-help"
    KEYSHORTCUTS = "aria-keyshortcuts"
    ROWINDEX = "aria-rowindex"
    COLUMNINDEX = "aria-columnindex"
    ROWSPAN = "aria-rowspan"
    COLSPAN = "aria-colspan"
    ROWCOUNT = "aria-rowcount"
    COLUMNCOUNT = "aria-columncount"
    ROWGROUP = "aria-rowgroup"
    COLUMNGROUP = "aria-columngroup"


class LiveRegionPriority(Enum):
    """Priority levels for ARIA live regions."""
    OFF = "off"
    POLITE = "polite"
    ASSERTIVE = "assertive"


@dataclass(frozen=True)
class AriaLabel:
    """Represents an ARIA label for an element."""
    element_id: str
    label: str
    description: str = ""
    context: str = "default"
    language: str = "en"
    priority: int = 100
    visible: bool = True


@dataclass(frozen=True)
class AriaLiveRegion:
    """Represents an ARIA live region for dynamic content announcements."""
    element_id: str
    priority: LiveRegionPriority = LiveRegionPriority.POLITE
    atomic: bool = False
    relevant: str = "additions text"
    busy: bool = False
    description: str = ""
    visible: bool = True


@dataclass(frozen=True)
class AriaRelationship:
    """Represents ARIA relationship attributes between elements."""
    source_id: str
    target_id: str
    relationship_type: AriaProperty
    bidirectional: bool = False
    context: str = "default"


class AriaSystem:
    """
    Centralized ARIA management system for creating accessible interfaces.
    
    This class manages ARIA labels, live regions, relationships, and provides
    utilities for generating accessible markup and announcements.
    """
    
    def __init__(self):
        self._aria_labels: Dict[str, AriaLabel] = {}
        self._live_regions: Dict[str, AriaLiveRegion] = {}
        self._relationships: List[AriaRelationship] = []
        self._element_roles: Dict[str, AriaRole] = {}
        self._element_states: Dict[str, Dict[AriaState, str]] = {}
        self._logger = logging.getLogger(f"{__name__}.AriaSystem")
    
    def set_aria_label(self, element_id: str, label: str, description: str = "", 
                      context: str = "default", language: str = "en") -> bool:
        """
        Set an ARIA label for an element.
        
        Args:
            element_id: Unique identifier for the element
            label: Human-readable label text
            description: Additional descriptive text
            context: Context where this label is used
            language: Language code for the label
            
        Returns:
            True if label was set successfully, False otherwise
        """
        try:
            aria_label = AriaLabel(
                element_id=element_id,
                label=label,
                description=description,
                context=context,
                language=language
            )
            self._aria_labels[element_id] = aria_label
            self._logger.debug(f"Set ARIA label for {element_id}: {label}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to set ARIA label for {element_id}: {e}")
            return False
    
    def get_aria_label(self, element_id: str) -> Optional[AriaLabel]:
        """Get the ARIA label for an element."""
        return self._aria_labels.get(element_id)
    
    def remove_aria_label(self, element_id: str) -> bool:
        """Remove an ARIA label for an element."""
        if element_id in self._aria_labels:
            del self._aria_labels[element_id]
            self._logger.debug(f"Removed ARIA label for {element_id}")
            return True
        return False
    
    def create_live_region(self, element_id: str, priority: LiveRegionPriority = LiveRegionPriority.POLITE,
                          atomic: bool = False, description: str = "") -> bool:
        """
        Create an ARIA live region for dynamic content announcements.
        
        Args:
            element_id: Unique identifier for the live region
            priority: Announcement priority level
            atomic: Whether the entire region should be announced as one unit
            description: Description of the live region's purpose
            
        Returns:
            True if live region was created successfully, False otherwise
        """
        try:
            live_region = AriaLiveRegion(
                element_id=element_id,
                priority=priority,
                atomic=atomic,
                description=description
            )
            self._live_regions[element_id] = live_region
            self._logger.debug(f"Created live region {element_id} with priority {priority.value}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to create live region {element_id}: {e}")
            return False
    
    def get_live_region(self, element_id: str) -> Optional[AriaLiveRegion]:
        """Get a live region by element ID."""
        return self._live_regions.get(element_id)
    
    def announce_to_live_region(self, element_id: str, message: str) -> bool:
        """
        Announce a message to a specific live region.
        
        Args:
            element_id: ID of the live region to announce to
            message: Message to announce
            
        Returns:
            True if announcement was successful, False otherwise
        """
        if element_id not in self._live_regions:
            self._logger.warning(f"Live region {element_id} not found")
            return False
        
        live_region = self._live_regions[element_id]
        self._logger.info(f"Announcing to {element_id} ({live_region.priority.value}): {message}")
        return True
    
    def set_element_role(self, element_id: str, role: AriaRole) -> bool:
        """Set the ARIA role for an element."""
        try:
            self._element_roles[element_id] = role
            self._logger.debug(f"Set role {role.value} for element {element_id}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to set role for {element_id}: {e}")
            return False
    
    def get_element_role(self, element_id: str) -> Optional[AriaRole]:
        """Get the ARIA role for an element."""
        return self._element_roles.get(element_id)
    
    def set_element_state(self, element_id: str, state: AriaState, value: str) -> bool:
        """Set an ARIA state for an element."""
        try:
            if element_id not in self._element_states:
                self._element_states[element_id] = {}
            self._element_states[element_id][state] = value
            self._logger.debug(f"Set state {state.value}={value} for element {element_id}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to set state for {element_id}: {e}")
            return False
    
    def get_element_state(self, element_id: str, state: AriaState) -> Optional[str]:
        """Get an ARIA state value for an element."""
        return self._element_states.get(element_id, {}).get(state)
    
    def add_relationship(self, source_id: str, target_id: str, 
                        relationship_type: AriaProperty, bidirectional: bool = False) -> bool:
        """Add an ARIA relationship between elements."""
        try:
            relationship = AriaRelationship(
                source_id=source_id,
                target_id=target_id,
                relationship_type=relationship_type,
                bidirectional=bidirectional
            )
            self._relationships.append(relationship)
            self._logger.debug(f"Added relationship {relationship_type.value} from {source_id} to {target_id}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to add relationship: {e}")
            return False
    
    def get_relationships_for_element(self, element_id: str) -> List[AriaRelationship]:
        """Get all relationships involving a specific element."""
        return [
            rel for rel in self._relationships
            if rel.source_id == element_id or rel.target_id == element_id
        ]
    
    def generate_aria_attributes(self, element_id: str) -> Dict[str, str]:
        """
        Generate a dictionary of ARIA attributes for an element.
        
        Args:
            element_id: ID of the element to generate attributes for
            
        Returns:
            Dictionary of ARIA attribute names and values
        """
        attributes = {}
        
        # Add role
        role = self.get_element_role(element_id)
        if role:
            attributes["role"] = role.value
        
        # Add label
        label = self.get_aria_label(element_id)
        if label:
            attributes["aria-label"] = label.label
            if label.description:
                attributes["aria-describedby"] = f"{element_id}-desc"
        
        # Add states
        element_states = self._element_states.get(element_id, {})
        for state, value in element_states.items():
            attributes[state.value] = value
        
        # Add live region attributes
        live_region = self.get_live_region(element_id)
        if live_region:
            attributes["aria-live"] = live_region.priority.value
            if live_region.atomic:
                attributes["aria-atomic"] = "true"
            if live_region.relevant != "additions text":
                attributes["aria-relevant"] = live_region.relevant
        
        return attributes
    
    def get_accessibility_summary(self) -> Dict[str, any]:
        """Get a summary of all accessibility information managed by the system."""
        return {
            "total_labels": len(self._aria_labels),
            "total_live_regions": len(self._live_regions),
            "total_relationships": len(self._relationships),
            "total_roles": len(self._element_roles),
            "total_states": sum(len(states) for states in self._element_states.values()),
            "labels": {k: {"label": v.label, "description": v.description} 
                      for k, v in self._aria_labels.items()},
            "live_regions": {k: {"priority": v.priority.value, "atomic": v.atomic}
                            for k, v in self._live_regions.items()},
            "roles": {k: v.value for k, v in self._element_roles.items()}
        }
    
    def clear_element(self, element_id: str) -> bool:
        """Remove all accessibility information for an element."""
        try:
            # Remove label
            self.remove_aria_label(element_id)
            
            # Remove live region
            if element_id in self._live_regions:
                del self._live_regions[element_id]
            
            # Remove role
            if element_id in self._element_roles:
                del self._element_roles[element_id]
            
            # Remove states
            if element_id in self._element_states:
                del self._element_states[element_id]
            
            # Remove relationships
            self._relationships = [
                rel for rel in self._relationships
                if rel.source_id != element_id and rel.target_id != element_id
            ]
            
            self._logger.debug(f"Cleared all accessibility info for element {element_id}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to clear element {element_id}: {e}")
            return False
    
    def validate_accessibility(self, element_id: str) -> Dict[str, any]:
        """
        Validate the accessibility configuration for an element.
        
        Args:
            element_id: ID of the element to validate
            
        Returns:
            Dictionary containing validation results and recommendations
        """
        issues = []
        warnings = []
        recommendations = []
        
        # Check if element has a role
        role = self.get_element_role(element_id)
        if not role:
            issues.append("Element has no ARIA role defined")
            recommendations.append("Define an appropriate ARIA role for the element")
        else:
            warnings.append(f"Element has role: {role.value}")
        
        # Check if element has a label
        label = self.get_aria_label(element_id)
        if not label:
            issues.append("Element has no accessible label")
            recommendations.append("Provide an aria-label or aria-labelledby attribute")
        else:
            warnings.append(f"Element has label: {label.label}")
        
        # Check live region configuration
        live_region = self.get_live_region(element_id)
        if live_region:
            if live_region.priority == LiveRegionPriority.ASSERTIVE:
                warnings.append("Live region uses assertive priority - use sparingly")
            if live_region.atomic:
                warnings.append("Live region is atomic - entire content will be announced")
        
        return {
            "element_id": element_id,
            "has_issues": len(issues) > 0,
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations,
            "overall_score": max(0, 100 - len(issues) * 25 - len(warnings) * 10)
        }
