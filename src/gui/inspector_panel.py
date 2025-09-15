"""
Inspector Panel for Nexlify Engine.

This module provides an inspector interface similar to Unity's Inspector,
showing properties and components of selected GameObjects.
"""

from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame,
    QLabel, QPushButton, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QCheckBox, QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from ..utils.logger import get_logger


class InspectorPanel(QWidget):
    """Collapsible inspector panel for editing GameObject properties."""
    
    # Signals
    property_changed = pyqtSignal(str, str, object)  # component, property, value
    
    def __init__(self, main_window):
        """Initialize the inspector panel.
        
        Args:
            main_window: Reference to the main window
        """
        super().__init__()
        self.main_window = main_window
        self.game_engine = main_window.game_engine
        self.logger = get_logger(__name__)
        
        self.current_game_object = None
        self.is_collapsed = False
        self._init_ui()
        
        self._setup_styles()
        self.logger.info("Inspector panel initialized")
    
    def _init_ui(self):
        """Initialize the user interface."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header with collapse button
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 6, 8, 6)
        header_layout.setSpacing(8)
        
        # Collapse button
        self.collapse_btn = QPushButton("▼")
        self.collapse_btn.setToolTip("Collapse/Expand Inspector Panel")
        self.collapse_btn.setMaximumWidth(20)
        self.collapse_btn.clicked.connect(self._toggle_collapse)
        self.collapse_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d30;
                color: #ffffff;
                border: 1px solid #3e3e42;
                border-radius: 3px;
                padding: 2px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #3e3e42;
                border-color: #5a5a5a;
            }
        """)
        header_layout.addWidget(self.collapse_btn)
        
        # Title
        title_label = QLabel("Inspector")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Selection info
        self.selection_label = QLabel("No Selection")
        self.selection_label.setStyleSheet("color: #cccccc; font-size: 9px;")
        header_layout.addWidget(self.selection_label)
        
        self.main_layout.addWidget(header_frame)
        
        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(8, 8, 8, 8)
        self.content_layout.setSpacing(8)
        
        # Scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.content_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }
            QScrollBar:vertical {
                background-color: #2d2d30;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #5a5a5a;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #7a7a7a;
            }
        """)
        
        self.main_layout.addWidget(self.scroll_area)
        
        # Set initial size
        self.setMaximumHeight(300)
        self.setMinimumHeight(100)
        
        # Show "no selection" message
        self._show_no_selection()
    
    def _setup_styles(self):
        """Setup the panel styles."""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QLabel {
                color: #cccccc;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #1a1a1a;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 6px;
                color: #fafafa;
                selection-background-color: #ff6b35;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border-color: #ff6b35;
                background-color: #262626;
            }
            QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {
                border-color: #ff8c42;
                background-color: #262626;
            }
            QLineEdit::placeholder {
                color: #a3a3a3;
            }
            QCheckBox {
                color: #cccccc;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #3e3e42;
                background-color: #2d2d30;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #ff6b35;
                background-color: #ff6b35;
            }
        """)
    
    def _toggle_collapse(self):
        """Toggle the panel between collapsed and expanded states."""
        if self.is_collapsed:
            self.expand()
        else:
            self.collapse()
    
    def collapse(self):
        """Collapse the panel to show only the header."""
        self.is_collapsed = True
        self.collapse_btn.setText("▶")
        self.scroll_area.hide()
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.logger.info("Inspector panel collapsed")
    
    def expand(self):
        """Expand the panel to show all content."""
        self.is_collapsed = False
        self.collapse_btn.setText("▼")
        self.scroll_area.show()
        self.setMaximumHeight(300)
        self.setMinimumHeight(100)
        self.logger.info("Inspector panel expanded")
    
    def _show_no_selection(self):
        """Show message when no GameObject is selected."""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        # Add no selection message
        no_selection_label = QLabel("No GameObject Selected")
        no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_selection_label.setStyleSheet("""
            color: #888888;
            font-size: 12px;
            padding: 20px;
        """)
        self.content_layout.addWidget(no_selection_label)
        self.content_layout.addStretch()
    
    def inspect_game_object(self, game_object):
        """Inspect a GameObject and show its properties.
        
        Args:
            game_object: The GameObject to inspect
        """
        self.current_game_object = game_object
        self.selection_label.setText(f"Selected: {game_object.name}")
        
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        if not game_object:
            self._show_no_selection()
            return
        
        # Add GameObject header
        self._add_game_object_header(game_object)
        
        # Add Transform component
        self._add_transform_component(game_object)
        
        # Add other components
        for component in game_object.components:
            if component.name != "Transform":
                self._add_component_section(component)
        
        # Add stretch to push content to top
        self.content_layout.addStretch()
    
    def _add_game_object_header(self, game_object):
        """Add the GameObject header section."""
        header_group = QGroupBox("GameObject")
        header_layout = QVBoxLayout(header_group)
        
        # Name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setMinimumWidth(80)
        name_field = QLineEdit(game_object.name)
        name_field.textChanged.connect(lambda text: self._on_name_changed(text))
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_field)
        header_layout.addLayout(name_layout)
        
        # Tag field
        tag_layout = QHBoxLayout()
        tag_label = QLabel("Tag:")
        tag_label.setMinimumWidth(80)
        tag_field = QComboBox()
        tag_field.addItems(["Untagged", "Player", "Enemy", "Environment", "UI"])
        tag_field.setCurrentText(getattr(game_object, 'tag', 'Untagged'))
        tag_field.currentTextChanged.connect(lambda text: self._on_tag_changed(text))
        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(tag_field)
        header_layout.addLayout(tag_layout)
        
        # Active checkbox
        active_layout = QHBoxLayout()
        active_checkbox = QCheckBox("Active")
        active_checkbox.setChecked(getattr(game_object, 'active', True))
        active_checkbox.toggled.connect(lambda checked: self._on_active_changed(checked))
        active_layout.addWidget(active_checkbox)
        active_layout.addStretch()
        header_layout.addLayout(active_layout)
        
        self.content_layout.addWidget(header_group)
    
    def _add_transform_component(self, game_object):
        """Add the Transform component section."""
        transform_group = QGroupBox("Transform")
        transform_layout = QVBoxLayout(transform_group)
        
        # Position
        pos_group = QGroupBox("Position")
        pos_layout = QVBoxLayout(pos_group)
        
        pos_x_layout = QHBoxLayout()
        pos_x_label = QLabel("X:")
        pos_x_spin = QDoubleSpinBox()
        pos_x_spin.setRange(-999999, 999999)
        pos_x_spin.setDecimals(3)
        pos_x_spin.setValue(game_object.transform.position.x)
        pos_x_spin.valueChanged.connect(lambda value: self._on_position_changed('x', value))
        pos_x_layout.addWidget(pos_x_label)
        pos_x_layout.addWidget(pos_x_spin)
        pos_layout.addLayout(pos_x_layout)
        
        pos_y_layout = QHBoxLayout()
        pos_y_label = QLabel("Y:")
        pos_y_spin = QDoubleSpinBox()
        pos_y_spin.setRange(-999999, 999999)
        pos_y_spin.setDecimals(3)
        pos_y_spin.setValue(game_object.transform.position.y)
        pos_y_spin.valueChanged.connect(lambda value: self._on_position_changed('y', value))
        pos_y_layout.addWidget(pos_y_label)
        pos_y_layout.addWidget(pos_y_spin)
        pos_layout.addLayout(pos_y_layout)
        
        pos_z_layout = QHBoxLayout()
        pos_z_label = QLabel("Z:")
        pos_z_spin = QDoubleSpinBox()
        pos_z_spin.setRange(-999999, 999999)
        pos_z_spin.setDecimals(3)
        pos_z_spin.setValue(game_object.transform.position.z)
        pos_z_spin.valueChanged.connect(lambda value: self._on_position_changed('z', value))
        pos_z_layout.addWidget(pos_z_label)
        pos_z_layout.addWidget(pos_z_spin)
        pos_layout.addLayout(pos_z_layout)
        
        transform_layout.addWidget(pos_group)
        
        # Rotation
        rot_group = QGroupBox("Rotation")
        rot_layout = QVBoxLayout(rot_group)
        
        rot_x_layout = QHBoxLayout()
        rot_x_label = QLabel("X:")
        rot_x_spin = QDoubleSpinBox()
        rot_x_spin.setRange(-180, 180)
        rot_x_spin.setDecimals(1)
        rot_x_spin.setValue(game_object.transform.rotation.x)
        rot_x_spin.valueChanged.connect(lambda value: self._on_rotation_changed('x', value))
        rot_x_layout.addWidget(rot_x_label)
        rot_x_layout.addWidget(rot_x_spin)
        rot_layout.addLayout(rot_x_layout)
        
        rot_y_layout = QHBoxLayout()
        rot_y_label = QLabel("Y:")
        rot_y_spin = QDoubleSpinBox()
        rot_y_spin.setRange(-180, 180)
        rot_y_spin.setDecimals(1)
        rot_y_spin.setValue(game_object.transform.rotation.y)
        rot_y_spin.valueChanged.connect(lambda value: self._on_rotation_changed('y', value))
        rot_y_layout.addWidget(rot_y_label)
        rot_y_layout.addWidget(rot_y_spin)
        rot_layout.addLayout(rot_y_layout)
        
        rot_z_layout = QHBoxLayout()
        rot_z_label = QLabel("Z:")
        rot_z_spin = QDoubleSpinBox()
        rot_z_spin.setRange(-180, 180)
        rot_z_spin.setDecimals(1)
        rot_z_spin.setValue(game_object.transform.rotation.z)
        rot_z_spin.valueChanged.connect(lambda value: self._on_rotation_changed('z', value))
        rot_z_layout.addWidget(rot_z_label)
        rot_z_layout.addWidget(rot_z_spin)
        rot_layout.addLayout(rot_z_layout)
        
        transform_layout.addWidget(rot_group)
        
        # Scale
        scale_group = QGroupBox("Scale")
        scale_layout = QVBoxLayout(scale_group)
        
        scale_x_layout = QHBoxLayout()
        scale_x_label = QLabel("X:")
        scale_x_spin = QDoubleSpinBox()
        scale_x_spin.setRange(0.001, 1000)
        scale_x_spin.setDecimals(3)
        scale_x_spin.setValue(game_object.transform.scale.x)
        scale_x_spin.valueChanged.connect(lambda value: self._on_scale_changed('x', value))
        scale_x_layout.addWidget(scale_x_label)
        scale_x_layout.addWidget(scale_x_spin)
        scale_layout.addLayout(scale_x_layout)
        
        scale_y_layout = QHBoxLayout()
        scale_y_label = QLabel("Y:")
        scale_y_spin = QDoubleSpinBox()
        scale_y_spin.setRange(0.001, 1000)
        scale_y_spin.setDecimals(3)
        scale_y_spin.setValue(game_object.transform.scale.y)
        scale_y_spin.valueChanged.connect(lambda value: self._on_scale_changed('y', value))
        scale_y_layout.addWidget(scale_y_label)
        scale_y_layout.addWidget(scale_y_spin)
        scale_layout.addLayout(scale_y_layout)
        
        scale_z_layout = QHBoxLayout()
        scale_z_label = QLabel("Z:")
        scale_z_spin = QDoubleSpinBox()
        scale_z_spin.setRange(0.001, 1000)
        scale_z_spin.setDecimals(3)
        scale_z_spin.setValue(game_object.transform.scale.z)
        scale_z_spin.valueChanged.connect(lambda value: self._on_scale_changed('z', value))
        scale_z_layout.addWidget(scale_z_label)
        scale_z_layout.addWidget(scale_z_spin)
        scale_layout.addLayout(scale_z_layout)
        
        transform_layout.addWidget(scale_group)
        
        self.content_layout.addWidget(transform_group)
    
    def _add_component_section(self, component):
        """Add a component section to the inspector.
        
        Args:
            component: The component to display
        """
        component_group = QGroupBox(component.name)
        component_layout = QVBoxLayout(component_group)
        
        # Add component-specific properties
        if hasattr(component, 'properties'):
            for prop_name, prop_value in component.properties.items():
                self._add_property_field(component_layout, prop_name, prop_value, component)
        
        # Add generic component info
        info_label = QLabel(f"Type: {component.__class__.__name__}")
        info_label.setStyleSheet("color: #888888; font-size: 10px;")
        component_layout.addWidget(info_label)
        
        self.content_layout.addWidget(component_group)
    
    def _add_property_field(self, layout, prop_name, prop_value, component):
        """Add a property field to a component section.
        
        Args:
            layout: The layout to add the field to
            prop_name: Name of the property
            prop_value: Current value of the property
            component: The component this property belongs to
        """
        prop_layout = QHBoxLayout()
        
        # Property label
        prop_label = QLabel(f"{prop_name}:")
        prop_label.setMinimumWidth(80)
        prop_layout.addWidget(prop_label)
        
        # Property value field
        if isinstance(prop_value, bool):
            prop_field = QCheckBox()
            prop_field.setChecked(prop_value)
            prop_field.toggled.connect(lambda checked: self._on_component_property_changed(component, prop_name, checked))
            prop_layout.addWidget(prop_field)
        elif isinstance(prop_value, int):
            prop_field = QSpinBox()
            prop_field.setRange(-999999, 999999)
            prop_field.setValue(prop_value)
            prop_field.valueChanged.connect(lambda value: self._on_component_property_changed(component, prop_name, value))
            prop_layout.addWidget(prop_field)
        elif isinstance(prop_value, float):
            prop_field = QDoubleSpinBox()
            prop_field.setRange(-999999, 999999)
            prop_field.setDecimals(3)
            prop_field.setValue(prop_value)
            prop_field.valueChanged.connect(lambda value: self._on_component_property_changed(component, prop_name, value))
            prop_layout.addWidget(prop_field)
        else:
            prop_field = QLineEdit(str(prop_value))
            prop_field.textChanged.connect(lambda text: self._on_component_property_changed(component, prop_name, text))
            prop_layout.addWidget(prop_field)
        
        prop_layout.addStretch()
        layout.addLayout(prop_layout)
    
    # Event handlers
    def _on_name_changed(self, new_name):
        """Handle GameObject name change."""
        if self.current_game_object:
            self.current_game_object.name = new_name
            self.selection_label.setText(f"Selected: {new_name}")
            self.property_changed.emit("GameObject", "name", new_name)
    
    def _on_tag_changed(self, new_tag):
        """Handle GameObject tag change."""
        if self.current_game_object:
            self.current_game_object.tag = new_tag
            self.property_changed.emit("GameObject", "tag", new_tag)
    
    def _on_active_changed(self, active):
        """Handle GameObject active state change."""
        if self.current_game_object:
            self.current_game_object.active = active
            self.property_changed.emit("GameObject", "active", active)
    
    def _on_position_changed(self, axis, value):
        """Handle position change."""
        if self.current_game_object and self.current_game_object.transform:
            if axis == 'x':
                self.current_game_object.transform.position.x = value
            elif axis == 'y':
                self.current_game_object.transform.position.y = value
            elif axis == 'z':
                self.current_game_object.transform.position.z = value
            self.property_changed.emit("Transform", f"position_{axis}", value)
    
    def _on_rotation_changed(self, axis, value):
        """Handle rotation change."""
        if self.current_game_object and self.current_game_object.transform:
            if axis == 'x':
                self.current_game_object.transform.rotation.x = value
            elif axis == 'y':
                self.current_game_object.transform.rotation.y = value
            elif axis == 'z':
                self.current_game_object.transform.rotation.z = value
            self.property_changed.emit("Transform", f"rotation_{axis}", value)
    
    def _on_scale_changed(self, axis, value):
        """Handle scale change."""
        if self.current_game_object and self.current_game_object.transform:
            if axis == 'x':
                self.current_game_object.transform.scale.x = value
            elif axis == 'y':
                self.current_game_object.transform.scale.y = value
            elif axis == 'z':
                self.current_game_object.transform.scale.z = value
            self.property_changed.emit("Transform", f"scale_{axis}", value)
    
    def _on_component_property_changed(self, component, property_name, value):
        """Handle component property change."""
        if hasattr(component, 'properties'):
            component.properties[property_name] = value
        self.property_changed.emit(component.name, property_name, value)
    
    def clear_selection(self):
        """Clear the current selection."""
        self.current_game_object = None
        self.selection_label.setText("No Selection")
        self._show_no_selection()
    
    def refresh(self):
        """Refresh the inspector display."""
        if self.current_game_object:
            self.inspect_game_object(self.current_game_object)
