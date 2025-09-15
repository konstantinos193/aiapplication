#!/usr/bin/env python3
"""
Semantic Structure system for creating accessible document structures.

This module provides semantic markup management, heading hierarchies,
landmark regions, and list structures for screen reader accessibility.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Set, Tuple, Any
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class HeadingLevel(Enum):
    """Heading levels for document structure."""
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6


class LandmarkType(Enum):
    """ARIA landmark types for page structure."""
    BANNER = "banner"
    NAVIGATION = "navigation"
    MAIN = "main"
    COMPLEMENTARY = "complementary"
    CONTENTINFO = "contentinfo"
    SEARCH = "search"
    REGION = "region"
    FORM = "form"
    ARTICLE = "article"
    SECTION = "section"
    ASIDE = "aside"
    HEADER = "header"
    FOOTER = "footer"


class ListType(Enum):
    """Types of lists for semantic structure."""
    UNORDERED = "unordered"
    ORDERED = "ordered"
    DEFINITION = "definition"
    NAVIGATION = "navigation"
    MENU = "menu"
    TOOLBAR = "toolbar"
    TABLIST = "tablist"
    TREE = "tree"


class TableType(Enum):
    """Types of tables for semantic structure."""
    DATA = "data"
    LAYOUT = "layout"
    GRID = "grid"
    TREE_GRID = "treegrid"
    CALENDAR = "calendar"


class FormType(Enum):
    """Types of forms for semantic structure."""
    SEARCH = "search"
    LOGIN = "login"
    REGISTRATION = "registration"
    CONTACT = "contact"
    SETTINGS = "settings"
    CHECKOUT = "checkout"
    SURVEY = "survey"


@dataclass(frozen=True)
class HeadingStructure:
    """Represents a heading in the document hierarchy."""
    element_id: str
    level: HeadingLevel
    text: str
    parent_id: str = ""
    children: List[str] = field(default_factory=list)
    context: str = "default"
    accessible: bool = True
    visible: bool = True
    order: int = 0
    language: str = "en"
    description: str = ""


@dataclass(frozen=True)
class LandmarkRegion:
    """Represents a landmark region for page navigation."""
    element_id: str
    type: LandmarkType
    label: str
    description: str = ""
    level: int = 0
    parent_id: str = ""
    children: List[str] = field(default_factory=list)
    accessible: bool = True
    visible: bool = True
    order: int = 0
    language: str = "en"
    expanded: bool = True


@dataclass(frozen=True)
class ListStructure:
    """Represents a list structure for navigation."""
    element_id: str
    type: ListType
    label: str = ""
    description: str = ""
    items: List[str] = field(default_factory=list)
    parent_id: str = ""
    accessible: bool = True
    visible: bool = True
    order: int = 0
    language: str = "en"
    expanded: bool = True


@dataclass(frozen=True)
class TableStructure:
    """Represents a table structure for data navigation."""
    element_id: str
    type: TableType
    caption: str = ""
    description: str = ""
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    parent_id: str = ""
    accessible: bool = True
    visible: bool = True
    order: int = 0
    language: str = "en"
    sortable: bool = False


@dataclass(frozen=True)
class FormStructure:
    """Represents a form structure for form navigation."""
    element_id: str
    type: FormType
    label: str = ""
    description: str = ""
    fields: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    parent_id: str = ""
    accessible: bool = True
    visible: bool = True
    order: int = 0
    language: str = "en"
    required_fields: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class SemanticNode:
    """Represents a node in the semantic structure tree."""
    element_id: str
    node_type: str
    label: str
    description: str = ""
    level: int = 0
    parent_id: str = ""
    children: List[str] = field(default_factory=list)
    accessible: bool = True
    visible: bool = True
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SemanticStructure:
    """
    Comprehensive semantic structure management system.
    
    This class manages heading hierarchies, landmark regions, lists, tables,
    and forms to create accessible document structures for screen readers.
    """
    
    def __init__(self):
        self._headings: Dict[str, HeadingStructure] = {}
        self._landmarks: Dict[str, LandmarkRegion] = {}
        self._lists: Dict[str, ListStructure] = {}
        self._tables: Dict[str, TableStructure] = {}
        self._forms: Dict[str, FormStructure] = {}
        self._semantic_nodes: Dict[str, SemanticNode] = {}
        self._structure_tree: Dict[str, List[str]] = defaultdict(list)
        self._logger = logging.getLogger(f"{__name__}.SemanticStructure")
        
        self._logger.info("SemanticStructure initialized")
    
    def register_heading(self, heading: HeadingStructure) -> bool:
        """
        Register a heading in the document hierarchy.
        
        Args:
            heading: Heading structure to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._headings[heading.element_id] = heading
            
            # Update structure tree
            if heading.parent_id:
                self._structure_tree[heading.parent_id].append(heading.element_id)
            
            # Update parent's children list
            if heading.parent_id and heading.parent_id in self._headings:
                parent = self._headings[heading.parent_id]
                if heading.element_id not in parent.children:
                    parent.children.append(heading.element_id)
            
            self._logger.debug(f"Registered heading: {heading.text} (level {heading.level.value})")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to register heading {heading.element_id}: {e}")
            return False
    
    def get_heading(self, element_id: str) -> Optional[HeadingStructure]:
        """Get a heading by element ID."""
        return self._headings.get(element_id)
    
    def get_headings_by_level(self, level: HeadingLevel) -> List[HeadingStructure]:
        """Get all headings of a specific level."""
        return [h for h in self._headings.values() if h.level == level]
    
    def get_heading_hierarchy(self) -> Dict[str, Any]:
        """Get the complete heading hierarchy."""
        hierarchy = {}
        
        # Find root headings (no parent)
        root_headings = [h for h in self._headings.values() if not h.parent_id]
        
        def build_hierarchy(heading: HeadingStructure) -> Dict[str, Any]:
            node = {
                'id': heading.element_id,
                'text': heading.text,
                'level': heading.level.value,
                'description': heading.description,
                'children': []
            }
            
            for child_id in heading.children:
                child = self._headings.get(child_id)
                if child:
                    node['children'].append(build_hierarchy(child))
            
            return node
        
        for root in root_headings:
            hierarchy[root.element_id] = build_hierarchy(root)
        
        return {
            'headings': hierarchy,
            'total': len(self._headings),
            'levels': {level.value: len(self.get_headings_by_level(level)) 
                      for level in HeadingLevel}
        }
    
    def register_landmark(self, landmark: LandmarkRegion) -> bool:
        """
        Register a landmark region.
        
        Args:
            landmark: Landmark region to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._landmarks[landmark.element_id] = landmark
            
            # Update structure tree
            if landmark.parent_id:
                self._structure_tree[landmark.parent_id].append(landmark.element_id)
            
            # Update parent's children list
            if landmark.parent_id and landmark.parent_id in self._landmarks:
                parent = self._landmarks[landmark.parent_id]
                if landmark.element_id not in parent.children:
                    parent.children.append(landmark.element_id)
            
            self._logger.debug(f"Registered landmark: {landmark.label} ({landmark.type.value})")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to register landmark {landmark.element_id}: {e}")
            return False
    
    def get_landmark(self, element_id: str) -> Optional[LandmarkRegion]:
        """Get a landmark by element ID."""
        return self._landmarks.get(element_id)
    
    def get_landmarks_by_type(self, landmark_type: LandmarkType) -> List[LandmarkRegion]:
        """Get all landmarks of a specific type."""
        return [l for l in self._landmarks.values() if l.type == landmark_type]
    
    def get_landmark_structure(self) -> Dict[str, Any]:
        """Get the complete landmark structure."""
        structure = {}
        
        # Find root landmarks (no parent)
        root_landmarks = [l for l in self._landmarks.values() if not l.parent_id]
        
        def build_structure(landmark: LandmarkRegion) -> Dict[str, Any]:
            node = {
                'id': landmark.element_id,
                'label': landmark.label,
                'type': landmark.type.value,
                'description': landmark.description,
                'level': landmark.level,
                'children': []
            }
            
            for child_id in landmark.children:
                child = self._landmarks.get(child_id)
                if child:
                    node['children'].append(build_structure(child))
            
            return node
        
        for root in root_landmarks:
            structure[root.element_id] = build_structure(root)
        
        return {
            'landmarks': structure,
            'total': len(self._landmarks),
            'types': {lt.value: len(self.get_landmarks_by_type(lt)) 
                     for lt in LandmarkType}
        }
    
    def register_list(self, list_structure: ListStructure) -> bool:
        """
        Register a list structure.
        
        Args:
            list_structure: List structure to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._lists[list_structure.element_id] = list_structure
            
            # Update structure tree
            if list_structure.parent_id:
                self._structure_tree[list_structure.parent_id].append(list_structure.element_id)
            
            self._logger.debug(f"Registered list: {list_structure.label} ({list_structure.type.value})")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to register list {list_structure.element_id}: {e}")
            return False
    
    def get_list(self, element_id: str) -> Optional[ListStructure]:
        """Get a list by element ID."""
        return self._lists.get(element_id)
    
    def get_lists_by_type(self, list_type: ListType) -> List[ListStructure]:
        """Get all lists of a specific type."""
        return [l for l in self._lists.values() if l.type == list_type]
    
    def register_table(self, table: TableStructure) -> bool:
        """
        Register a table structure.
        
        Args:
            table: Table structure to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._tables[table.element_id] = table
            
            # Update structure tree
            if table.parent_id:
                self._structure_tree[table.parent_id].append(table.element_id)
            
            self._logger.debug(f"Registered table: {table.caption} ({table.type.value})")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to register table {table.element_id}: {e}")
            return False
    
    def get_table(self, element_id: str) -> Optional[TableStructure]:
        """Get a table by element ID."""
        return self._tables.get(element_id)
    
    def get_tables_by_type(self, table_type: TableType) -> List[TableStructure]:
        """Get all tables of a specific type."""
        return [t for t in self._tables.values() if t.type == table_type]
    
    def register_form(self, form: FormStructure) -> bool:
        """
        Register a form structure.
        
        Args:
            form: Form structure to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._forms[form.element_id] = form
            
            # Update structure tree
            if form.parent_id:
                self._structure_tree[form.parent_id].append(form.element_id)
            
            self._logger.debug(f"Registered form: {form.label} ({form.type.value})")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to register form {form.element_id}: {e}")
            return False
    
    def get_form(self, element_id: str) -> Optional[FormStructure]:
        """Get a form by element ID."""
        return self._forms.get(element_id)
    
    def get_forms_by_type(self, form_type: FormType) -> List[FormStructure]:
        """Get all forms of a specific type."""
        return [f for f in self._forms.values() if f.type == form_type]
    
    def register_semantic_node(self, node: SemanticNode) -> bool:
        """
        Register a generic semantic node.
        
        Args:
            node: Semantic node to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._semantic_nodes[node.element_id] = node
            
            # Update structure tree
            if node.parent_id:
                self._structure_tree[node.parent_id].append(node.element_id)
            
            self._logger.debug(f"Registered semantic node: {node.label} ({node.node_type})")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to register semantic node {node.element_id}: {e}")
            return False
    
    def get_semantic_node(self, element_id: str) -> Optional[SemanticNode]:
        """Get a semantic node by element ID."""
        return self._semantic_nodes.get(element_id)
    
    def get_semantic_structure(self) -> Dict[str, Any]:
        """Get the complete semantic structure overview."""
        return {
            'headings': {
                'total': len(self._headings),
                'levels': {level.value: len(self.get_headings_by_level(level)) 
                          for level in HeadingLevel},
                'hierarchy': self.get_heading_hierarchy()
            },
            'landmarks': {
                'total': len(self._landmarks),
                'types': {lt.value: len(self.get_landmarks_by_type(lt)) 
                         for lt in LandmarkType},
                'structure': self.get_landmark_structure()
            },
            'lists': {
                'total': len(self._lists),
                'types': {lt.value: len(self.get_lists_by_type(lt)) 
                         for lt in ListType}
            },
            'tables': {
                'total': len(self._tables),
                'types': {tt.value: len(self.get_tables_by_type(tt)) 
                         for tt in TableType}
            },
            'forms': {
                'total': len(self._forms),
                'types': {ft.value: len(self.get_forms_by_type(ft)) 
                         for ft in FormType}
            },
            'semantic_nodes': {
                'total': len(self._semantic_nodes)
            },
            'structure_tree': dict(self._structure_tree)
        }
    
    def get_navigation_path(self, element_id: str) -> List[str]:
        """
        Get the navigation path to an element.
        
        Args:
            element_id: ID of the element to find path for
            
        Returns:
            List of element IDs representing the path from root to element
        """
        path = []
        current_id = element_id
        
        # Check all structure types
        all_elements = {
            **self._headings,
            **self._landmarks,
            **self._lists,
            **self._tables,
            **self._forms,
            **self._semantic_nodes
        }
        
        while current_id in all_elements:
            path.insert(0, current_id)
            element = all_elements[current_id]
            current_id = element.parent_id
            
            if not current_id:
                break
        
        return path
    
    def get_accessible_elements(self, element_type: str = None) -> List[Dict[str, Any]]:
        """
        Get all accessible elements of a specific type.
        
        Args:
            element_type: Type of elements to retrieve (None for all)
            
        Returns:
            List of accessible elements with their properties
        """
        accessible_elements = []
        
        if element_type is None or element_type == "heading":
            for heading in self._headings.values():
                if heading.accessible and heading.visible:
                    accessible_elements.append({
                        'id': heading.element_id,
                        'type': 'heading',
                        'label': heading.text,
                        'level': heading.level.value,
                        'description': heading.description,
                        'order': heading.order
                    })
        
        if element_type is None or element_type == "landmark":
            for landmark in self._landmarks.values():
                if landmark.accessible and landmark.visible:
                    accessible_elements.append({
                        'id': landmark.element_id,
                        'type': 'landmark',
                        'label': landmark.label,
                        'landmark_type': landmark.type.value,
                        'description': landmark.description,
                        'level': landmark.level,
                        'order': landmark.order
                    })
        
        if element_type is None or element_type == "list":
            for list_elem in self._lists.values():
                if list_elem.accessible and list_elem.visible:
                    accessible_elements.append({
                        'id': list_elem.element_id,
                        'type': 'list',
                        'label': list_elem.label,
                        'list_type': list_elem.type.value,
                        'description': list_elem.description,
                        'item_count': len(list_elem.items),
                        'order': list_elem.order
                    })
        
        if element_type is None or element_type == "table":
            for table in self._tables.values():
                if table.accessible and table.visible:
                    accessible_elements.append({
                        'id': table.element_id,
                        'type': 'table',
                        'label': table.caption,
                        'table_type': table.type.value,
                        'description': table.description,
                        'row_count': len(table.rows),
                        'column_count': len(table.headers) if table.headers else 0,
                        'order': table.order
                    })
        
        if element_type is None or element_type == "form":
            for form in self._forms.values():
                if form.accessible and form.visible:
                    accessible_elements.append({
                        'id': form.element_id,
                        'type': 'form',
                        'label': form.label,
                        'form_type': form.type.value,
                        'description': form.description,
                        'field_count': len(form.fields),
                        'required_fields': len(form.required_fields),
                        'order': form.order
                    })
        
        # Sort by order
        accessible_elements.sort(key=lambda x: x.get('order', 0))
        return accessible_elements
    
    def validate_semantic_structure(self) -> Dict[str, Any]:
        """Validate the semantic structure for accessibility issues."""
        issues = []
        warnings = []
        recommendations = []
        
        # Check heading hierarchy
        heading_levels = [h.level.value for h in self._headings.values()]
        if heading_levels:
            if min(heading_levels) > 1:
                warnings.append("Document starts with heading level greater than 1")
            
            # Check for skipped levels
            for i in range(len(heading_levels) - 1):
                if heading_levels[i + 1] - heading_levels[i] > 1:
                    warnings.append(f"Heading level skipped from {heading_levels[i]} to {heading_levels[i + 1]}")
        
        # Check landmarks
        if not any(l.type == LandmarkType.MAIN for l in self._landmarks.values()):
            issues.append("No main landmark region defined")
            recommendations.append("Add a main landmark region for primary content")
        
        if not any(l.type == LandmarkType.NAVIGATION for l in self._landmarks.values()):
            warnings.append("No navigation landmark region defined")
            recommendations.append("Consider adding a navigation landmark for site navigation")
        
        # Check lists
        for list_elem in self._lists.values():
            if list_elem.type == ListType.NAVIGATION and not list_elem.label:
                warnings.append(f"Navigation list {list_elem.element_id} has no label")
                recommendations.append("Provide descriptive labels for navigation lists")
        
        # Check tables
        for table in self._tables.values():
            if table.type == TableType.DATA and not table.caption:
                warnings.append(f"Data table {table.element_id} has no caption")
                recommendations.append("Provide captions for data tables")
            
            if table.type == TableType.DATA and not table.headers:
                issues.append(f"Data table {table.element_id} has no headers")
                recommendations.append("Add headers to data tables for accessibility")
        
        # Check forms
        for form in self._forms.values():
            if not form.label:
                warnings.append(f"Form {form.element_id} has no label")
                recommendations.append("Provide descriptive labels for forms")
            
            if form.required_fields and not form.description:
                warnings.append(f"Form {form.element_id} has required fields but no description")
                recommendations.append("Describe required fields and validation rules")
        
        return {
            'has_issues': len(issues) > 0,
            'issues': issues,
            'warnings': warnings,
            'recommendations': recommendations,
            'total_elements': len(self._headings) + len(self._landmarks) + len(self._lists) + len(self._tables) + len(self._forms),
            'accessible_elements': len(self.get_accessible_elements()),
            'overall_score': max(0, 100 - len(issues) * 25 - len(warnings) * 10)
        }
    
    def clear_element(self, element_id: str) -> bool:
        """Remove all semantic information for an element."""
        try:
            # Remove from all structures
            if element_id in self._headings:
                del self._headings[element_id]
            if element_id in self._landmarks:
                del self._landmarks[element_id]
            if element_id in self._lists:
                del self._lists[element_id]
            if element_id in self._tables:
                del self._tables[element_id]
            if element_id in self._forms:
                del self._forms[element_id]
            if element_id in self._semantic_nodes:
                del self._semantic_nodes[element_id]
            
            # Remove from structure tree
            if element_id in self._structure_tree:
                del self._structure_tree[element_id]
            
            # Remove from parent children lists
            for structure_dict in [self._headings, self._landmarks, self._lists, 
                                 self._tables, self._forms, self._semantic_nodes]:
                for element in structure_dict.values():
                    if element_id in element.children:
                        element.children.remove(element_id)
            
            self._logger.debug(f"Cleared all semantic info for element {element_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to clear element {element_id}: {e}")
            return False
    
    def export_semantic_markup(self, element_id: str) -> Dict[str, Any]:
        """
        Export semantic markup for an element.
        
        Args:
            element_id: ID of the element to export markup for
            
        Returns:
            Dictionary containing semantic markup information
        """
        markup = {
            'element_id': element_id,
            'semantic_attributes': {},
            'relationships': {},
            'navigation_info': {}
        }
        
        # Check all structure types
        if element_id in self._headings:
            heading = self._headings[element_id]
            markup['semantic_attributes']['role'] = f"heading"
            markup['semantic_attributes']['aria-level'] = heading.level.value
            markup['semantic_attributes']['aria-label'] = heading.text
            if heading.description:
                markup['semantic_attributes']['aria-describedby'] = f"{element_id}-desc"
        
        elif element_id in self._landmarks:
            landmark = self._landmarks[element_id]
            markup['semantic_attributes']['role'] = landmark.type.value
            markup['semantic_attributes']['aria-label'] = landmark.label
            if landmark.description:
                markup['semantic_attributes']['aria-describedby'] = f"{element_id}-desc"
        
        elif element_id in self._lists:
            list_elem = self._lists[element_id]
            markup['semantic_attributes']['role'] = "list"
            if list_elem.label:
                markup['semantic_attributes']['aria-label'] = list_elem.label
            if list_elem.description:
                markup['semantic_attributes']['aria-describedby'] = f"{element_id}-desc"
        
        elif element_id in self._tables:
            table = self._tables[element_id]
            markup['semantic_attributes']['role'] = "table"
            if table.caption:
                markup['semantic_attributes']['aria-label'] = table.caption
            if table.description:
                markup['semantic_attributes']['aria-describedby'] = f"{element_id}-desc"
        
        elif element_id in self._forms:
            form = self._forms[element_id]
            markup['semantic_attributes']['role'] = "form"
            if form.label:
                markup['semantic_attributes']['aria-label'] = form.label
            if form.description:
                markup['semantic_attributes']['aria-describedby'] = f"{element_id}-desc"
        
        # Add navigation information
        path = self.get_navigation_path(element_id)
        if path:
            markup['navigation_info']['path'] = path
            markup['navigation_info']['level'] = len(path)
        
        return markup
