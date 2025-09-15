"""
Panel widgets for the main window.

This module contains all the panel widgets including:
- Scene panel (GameObject hierarchy)
- Properties panel (component editing)
- Assets panel (asset management)
- Console panel (logging and output)
- Inspector panel (detailed object inspection)
"""

from typing import List, Optional, Dict, Any, TYPE_CHECKING, Union, Tuple
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QMenu, QInputDialog, QMessageBox,
    QSplitter, QFrame, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont, QAction

if TYPE_CHECKING:
    from .main_window import MainWindow
    from ..core.game_object import GameObject
    from ..core.scene import Scene

from ..utils.logger import get_logger
from .responsive import responsive_spacing_manager, Breakpoint
from .animations import spacing_animation_manager, EasingType
from .performance import layout_optimizer, optimized_spacing_calculator, spacing_cache_system
from .design_system.spacing_system import SpacingUnit


class ScenePanel(QWidget):
    """Panel for displaying and managing the scene hierarchy."""
    
    # Signals
    game_object_selected = pyqtSignal(object)  # Emits GameObject when selected
    
    def __init__(self, main_window: 'MainWindow'):
        super().__init__()
        self.main_window = main_window
        self.game_engine = main_window.game_engine
        self.logger = get_logger(__name__)
        
        self._setup_ui()
        self._setup_connections()
        self._setup_timer()
        
        self.logger.info("ScenePanel initialized")
    
    def _setup_ui(self):
        """Setup the user interface using design system."""
        from .design_system.spacing_system import spacing, SpacingUnit
        from .design_system.typography_system import typography, FontSize, FontWeight
        from .design_system.alignment_system import alignment, HorizontalAlignment
        from .components.standard_button import StandardButton
        
        layout = QVBoxLayout()
        
        # Apply panel spacing and professional styling
        panel_margin, panel_padding = spacing.get_panel_spacing()
        layout.setContentsMargins(panel_margin, panel_margin, panel_margin, panel_margin)
        layout.setSpacing(spacing.get_section_spacing())
        
        # Apply panel styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2d2d30;
                color: #cccccc;
            }}
        """)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(spacing.get_item_spacing())
        
        header_label = QLabel("Scene Hierarchy")
        header_font = QFont()
        header_font.setPointSize(typography.get_header_style()[0])
        header_font.setWeight(typography.get_header_style()[1])
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"""
            QLabel {{
                color: #cccccc;
                padding: {spacing.sm}px;
                background-color: #3e3e42;
                border-radius: 4px;
                border: 1px solid #555555;
            }}
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        # Add button using standard button component
        self.add_button = StandardButton("+", size="small", variant="primary")
        self.add_button.setToolTip("Add GameObject")
        self.add_button.clicked.connect(self._show_add_object_menu)
        header_layout.addWidget(self.add_button)
        
        layout.addLayout(header_layout)
        
        # Scene tree with proper spacing
        self.scene_tree = QTreeWidget()
        self.scene_tree.setHeaderLabel("GameObjects")
        self.scene_tree.setAlternatingRowColors(True)
        self.scene_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.scene_tree.customContextMenuRequested.connect(self._show_context_menu)
        self.scene_tree.itemSelectionChanged.connect(self._on_selection_changed)
        
        # Apply tree spacing and professional styling
        self.scene_tree.setIndentation(spacing.tree_indent)
        self.scene_tree.setStyleSheet(f"""
            QTreeWidget {{
                padding: {panel_padding}px;
                border: 1px solid #555555;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: #cccccc;
                font-size: {typography.sm}px;
                font-weight: {typography.normal};
            }}
            QTreeWidget::item {{
                padding: {spacing.selection_padding}px;
                margin: {spacing.xs}px;
                border-radius: 4px;
                min-height: {spacing.button_height}px;
            }}
            QTreeWidget::item:hover {{
                background-color: #3e3e42;
                color: #cccccc;
            }}
            QTreeWidget::item:selected {{
                background-color: #0078d4;
                color: white;
                padding: {spacing.selection_padding}px;
                font-weight: {typography.medium};
            }}
            QTreeWidget::item:alternate {{
                background-color: #2d2d30;
            }}
            QTreeWidget::item:alternate:hover {{
                background-color: #3e3e42;
            }}
            QTreeWidget::item:alternate:selected {{
                background-color: #0078d4;
                color: white;
            }}
        """)
        
        layout.addWidget(self.scene_tree)
        
        # Status bar with proper spacing
        status_layout = QHBoxLayout()
        status_layout.setSpacing(spacing.get_item_spacing())
        
        self.object_count_label = QLabel("Objects: 0")
        self.scene_status_label = QLabel("Scene: Stopped")
        
        # Apply status label styling
        status_font = QFont()
        status_font.setPointSize(typography.get_caption_style()[0])
        status_font.setWeight(typography.get_caption_style()[1])
        
        self.object_count_label.setFont(status_font)
        self.scene_status_label.setFont(status_font)
        
        status_layout.addWidget(self.object_count_label)
        status_layout.addStretch()
        status_layout.addWidget(self.scene_status_label)
        
        layout.addLayout(status_layout)
        
        self.setLayout(layout)
        
        # Connect to responsive spacing manager for breakpoint changes
        responsive_spacing_manager.connect_breakpoint_changed(self._on_breakpoint_changed)
    
    def _on_breakpoint_changed(self, breakpoint_name: str):
        """Handle breakpoint changes from responsive spacing system.
        
        Args:
            breakpoint_name: New breakpoint name
        """
        self.logger.info(f"ScenePanel breakpoint changed to: {breakpoint_name}")
        self._update_responsive_spacing()
    
    def _update_responsive_spacing(self):
        """Update spacing based on current breakpoint."""
        try:
            current_breakpoint = responsive_spacing_manager.get_current_breakpoint()
            
            # Get responsive spacing values
            responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.md)
            responsive_padding = responsive_spacing_manager.get_responsive_spacing(spacing.sm)
            responsive_tree_indent = responsive_spacing_manager.get_responsive_spacing(spacing.tree_indent)
            responsive_item_spacing = responsive_spacing_manager.get_responsive_spacing(spacing.xs)
            
            # Update layout margins
            layout = self.layout()
            if layout:
                layout.setContentsMargins(responsive_margin, responsive_margin, 
                                        responsive_margin, responsive_margin)
                layout.setSpacing(responsive_padding)
            
            # Update tree indentation
            if hasattr(self, 'scene_tree'):
                self.scene_tree.setIndentation(responsive_tree_indent)
            
            # Update tree item spacing
            tree_style = f"""
                QTreeWidget::item {{
                    padding: {responsive_padding}px;
                    margin: {responsive_item_spacing}px;
                    border-radius: 4px;
                    min-height: {spacing.button_height}px;
                }}
            """
            # Apply updated styling
            self._apply_responsive_styling()
            
            self.logger.info(f"Updated ScenePanel spacing for breakpoint: {current_breakpoint.value}")
            
        except Exception as e:
            self.logger.error(f"Failed to update ScenePanel responsive spacing: {e}")
    
    def _apply_responsive_styling(self):
        """Apply responsive styling to the ScenePanel."""
        try:
            current_breakpoint = responsive_spacing_manager.get_current_breakpoint()
            
            # Get responsive spacing values
            responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.md)
            responsive_padding = responsive_spacing_manager.get_responsive_spacing(spacing.sm)
            responsive_tree_indent = responsive_spacing_manager.get_responsive_spacing(spacing.tree_indent)
            responsive_item_spacing = responsive_spacing_manager.get_responsive_spacing(spacing.xs)
            
            # Apply responsive styling
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #2d2d30;
                    color: #cccccc;
                }}
            """)
            
            # Update tree styling with responsive spacing
            if hasattr(self, 'scene_tree'):
                tree_style = f"""
                    QTreeWidget {{
                        padding: {responsive_padding}px;
                        border: 1px solid #555555;
                        border-radius: 6px;
                        background-color: #1e1e1e;
                        color: #cccccc;
                        font-size: {typography.sm}px;
                        font-weight: {typography.normal};
                    }}
                    QTreeWidget::item {{
                        padding: {responsive_padding}px;
                        margin: {responsive_item_spacing}px;
                        border-radius: 4px;
                        min-height: {spacing.button_height}px;
                    }}
                    QTreeWidget::item:hover {{
                        background-color: #3e3e42;
                        color: #cccccc;
                    }}
                    QTreeWidget::item:selected {{
                        background-color: #0078d4;
                        color: white;
                        padding: {responsive_padding}px;
                        font-weight: {typography.medium};
                    }}
                    QTreeWidget::item:alternate {{
                        background-color: #2d2d30;
                    }}
                    QTreeWidget::item:alternate:hover {{
                        background-color: #3e3e42;
                    }}
                    QTreeWidget::item:alternate:selected {{
                        background-color: #0078d4;
                        color: white;
                    }}
                """
                self.scene_tree.setStyleSheet(tree_style)
            
        except Exception as e:
            self.logger.error(f"Failed to apply responsive styling: {e}")
    
    def get_responsive_spacing(self, base_spacing, touch_friendly: bool = False):
        """Get responsive spacing value for current breakpoint.
        
        Args:
            base_spacing: Base spacing value
            touch_friendly: Whether to apply touch-friendly adjustments
            
        Returns:
            Responsive spacing value
        """
        return responsive_spacing_manager.get_responsive_spacing(base_spacing, touch_friendly)
    
    def animate_spacing_change(self, start_spacing: int, end_spacing: int, 
                             duration: int = 300, easing: EasingType = EasingType.EASE_IN_OUT):
        """Animate spacing change for the ScenePanel.
        
        Args:
            start_spacing: Starting spacing value
            end_spacing: Ending spacing value
            duration: Animation duration in milliseconds
            easing: Easing curve type
        """
        return spacing_animation_manager.animate_spacing_change(
            self, start_spacing, end_spacing, duration, easing
        )
    
    def get_current_breakpoint(self) -> str:
        """Get current breakpoint name.
        
        Returns:
            Current breakpoint name
        """
        return responsive_spacing_manager.get_current_breakpoint().value
    
    def _setup_connections(self):
        """Setup signal connections."""
        # Connect to game engine signals if available
        pass
    
    def _setup_timer(self):
        """Setup timer for periodic updates."""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_scene_tree)
        self.update_timer.start(1000)  # Update every second
    
    def _show_add_object_menu(self):
        """Show the menu for adding new GameObjects."""
        menu = QMenu(self)
        
        # Basic objects
        basic_menu = menu.addMenu("Basic Objects")
        basic_menu.addAction("Empty", lambda: self._create_empty())
        basic_menu.addAction("Cube", lambda: self._create_cube())
        basic_menu.addAction("Sphere", lambda: self._create_sphere())
        
        # Lights
        light_menu = menu.addMenu("Lights")
        light_menu.addAction("Point Light", lambda: self._create_light("Point"))
        light_menu.addAction("Directional Light", lambda: self._create_light("Directional"))
        light_menu.addAction("Spot Light", lambda: self._create_light("Spot"))
        
        # Cameras
        camera_menu = menu.addMenu("Cameras")
        camera_menu.addAction("Camera", lambda: self._create_camera())
        
        # Show menu at button position
        menu.exec(self.add_button.mapToGlobal(self.add_button.rect().bottomLeft()))
    
    def _create_empty(self):
        """Create an empty GameObject."""
        try:
            game_object = self.game_engine.create_empty("Empty")
            if game_object:
                self._refresh_scene()
                self.logger.info("Created empty GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create empty GameObject: {e}")
    
    def _create_cube(self):
        """Create a cube GameObject."""
        try:
            game_object = self.game_engine.create_cube("Cube")
            if game_object:
                self._refresh_scene()
                self.logger.info("Created cube GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create cube GameObject: {e}")
    
    def _create_sphere(self):
        """Create a sphere GameObject."""
        try:
            game_object = self.game_engine.create_sphere("Sphere")
            if game_object:
                self._refresh_scene()
                self.logger.info("Created sphere GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create sphere GameObject: {e}")
    
    def _create_light(self, light_type: str):
        """Create a light GameObject."""
        try:
            game_object = self.game_engine.create_light(f"{light_type} Light", light_type)
            if game_object:
                self._refresh_scene()
                self.logger.info(f"Created {light_type} light GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create {light_type} light GameObject: {e}")
    
    def _create_camera(self):
        """Create a camera GameObject."""
        try:
            game_object = self.game_engine.create_camera("Camera")
            if game_object:
                self._refresh_scene()
                self.logger.info("Created camera GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create camera GameObject: {e}")
    
    def _show_context_menu(self, position):
        """Show the context menu for GameObjects."""
        item = self.scene_tree.itemAt(position)
        if not item:
            return
        
        game_object = item.data(0, Qt.ItemDataRole.UserRole)
        if not game_object:
            return
        
        menu = QMenu(self)
        
        # Rename action
        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self._rename_game_object(game_object))
        menu.addAction(rename_action)
        
        # Duplicate action
        duplicate_action = QAction("Duplicate", self)
        duplicate_action.triggered.connect(lambda: self._duplicate_game_object(game_object))
        menu.addAction(duplicate_action)
        
        menu.addSeparator()
        
        # Delete action
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._delete_game_object(game_object))
        menu.addAction(delete_action)
        
        menu.exec(self.scene_tree.mapToGlobal(position))
    
    def _rename_game_object(self, game_object: 'GameObject'):
        """Rename a GameObject."""
        try:
            new_name, ok = QInputDialog.getText(
                self, "Rename GameObject", 
                "Enter new name:", 
                text=game_object.name
            )
            
            if ok and new_name.strip():
                old_name = game_object.name
                game_object.name = new_name.strip()
                self._refresh_scene()
                self.logger.info(f"Renamed GameObject from '{old_name}' to '{new_name}'")
        except Exception as e:
            self.logger.error(f"Failed to rename GameObject: {e}")
    
    def _duplicate_game_object(self, game_object: 'GameObject'):
        """Duplicate a GameObject."""
        try:
            # Create a copy with a new name
            new_name = f"{game_object.name} (Copy)"
            duplicate = self.game_engine.create_empty(new_name)
            
            if duplicate:
                # Copy transform
                duplicate.transform.position = game_object.transform.position.copy()
                duplicate.transform.rotation = game_object.transform.rotation.copy()
                duplicate.transform.scale = game_object.transform.scale.copy()
                
                # Copy components (basic copy for now)
                for component in game_object.components:
                    if hasattr(component, '__class__'):
                        try:
                            new_component = component.__class__()
                            duplicate.add_component(new_component)
                        except Exception as e:
                            self.logger.warning(f"Could not copy component {component.name}: {e}")
                
                self._refresh_scene()
                self.logger.info(f"Duplicated GameObject '{game_object.name}'")
        except Exception as e:
            self.logger.error(f"Failed to duplicate GameObject: {e}")
    
    def _delete_game_object(self, game_object: 'GameObject'):
        """Delete a GameObject."""
        try:
            reply = QMessageBox.question(
                self, "Delete GameObject",
                f"Are you sure you want to delete '{game_object.name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.game_engine.destroy_game_object(game_object)
                self._refresh_scene()
                self.logger.info(f"Deleted GameObject '{game_object.name}'")
        except Exception as e:
            self.logger.error(f"Failed to delete GameObject: {e}")
    
    def _on_selection_changed(self):
        """Handle selection changes in the scene tree."""
        selected_items = self.scene_tree.selectedItems()
        if selected_items:
            game_object = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
            if game_object:
                self.game_object_selected.emit(game_object)
    
    def _refresh_scene(self):
        """Refresh the scene tree display."""
        try:
            self.scene_tree.clear()
            
            if not self.game_engine.current_scene:
                return
            
            scene = self.game_engine.current_scene
            root_objects = scene.get_root_objects()
            
            for game_object in root_objects:
                self._add_game_object_to_tree(game_object, None)
            
            # Update status
            self._update_status()
            
        except Exception as e:
            self.logger.error(f"Failed to refresh scene: {e}")
    
    def _add_game_object_to_tree(self, game_object: 'GameObject', parent_item: Optional[QTreeWidgetItem]):
        """Add a GameObject to the tree widget."""
        try:
            # Create tree item
            item = QTreeWidgetItem()
            item.setText(0, game_object.name)
            item.setData(0, Qt.ItemDataRole.UserRole, game_object)
            
            # Set icon based on component type
            if game_object.has_component(self._get_camera_component_class()):
                item.setIcon(0, self._get_camera_icon())
            elif game_object.has_component(self._get_light_component_class()):
                item.setIcon(0, self._get_light_icon())
            elif game_object.has_component(self._get_mesh_renderer_component_class()):
                item.setIcon(0, self._get_mesh_icon())
            else:
                item.setIcon(0, self._get_empty_icon())
            
            # Add to tree
            if parent_item:
                parent_item.addChild(item)
            else:
                self.scene_tree.addTopLevelItem(item)
            
            # Add children recursively
            for child in game_object.children:
                self._add_game_object_to_tree(child, item)
            
            # Expand the item
            item.setExpanded(True)
            
        except Exception as e:
            self.logger.error(f"Failed to add GameObject to tree: {e}")
    
    def _get_camera_component_class(self):
        """Get the Camera component class for type checking."""
        from ..core.components import Camera
        return Camera
    
    def _get_light_component_class(self):
        """Get the Light component class for type checking."""
        from ..core.components import Light
        return Light
    
    def _get_mesh_renderer_component_class(self):
        """Get the MeshRenderer component class for type checking."""
        from ..core.components import MeshRenderer
        return MeshRenderer
    
    def _get_camera_icon(self):
        """Get the camera icon."""
        # In a real implementation, you'd load actual icons
        return QIcon()
    
    def _get_light_icon(self):
        """Get the light icon."""
        # In a real implementation, you'd load actual icons
        return QIcon()
    
    def _get_mesh_icon(self):
        """Get the mesh icon."""
        # In a real implementation, you'd load actual icons
        return QIcon()
    
    def _get_empty_icon(self):
        """Get the empty GameObject icon."""
        # In a real implementation, you'd load actual icons
        return QIcon()
    
    def _update_status(self):
        """Update the status display."""
        try:
            if self.game_engine.current_scene:
                scene = self.game_engine.current_scene
                object_count = scene.get_object_count()
                self.object_count_label.setText(f"Objects: {object_count}")
                
                if scene.is_scene_playing():
                    if scene.is_scene_paused():
                        self.scene_status_label.setText("Scene: Paused")
                    else:
                        self.scene_status_label.setText("Scene: Playing")
                else:
                    self.scene_status_label.setText("Scene: Stopped")
            else:
                self.object_count_label.setText("Objects: 0")
                self.scene_status_label.setText("Scene: None")
                
        except Exception as e:
            self.logger.error(f"Failed to update status: {e}")
    
    def _update_scene_tree(self):
        """Periodically update the scene tree."""
        try:
            # Only refresh if the scene has changed
            current_scene = self.game_engine.current_scene
            if current_scene and hasattr(self, '_last_scene_count'):
                current_count = current_scene.get_object_count()
                if current_count != self._last_scene_count:
                    self._refresh_scene()
                    self._last_scene_count = current_count
            elif current_scene:
                self._last_scene_count = current_scene.get_object_count()
                
        except Exception as e:
            self.logger.error(f"Failed to update scene tree: {e}")
    
    def refresh(self):
        """Manually refresh the scene panel."""
        self._refresh_scene()
    
    def select_game_object(self, game_object: 'GameObject'):
        """Select a specific GameObject in the tree."""
        try:
            # Find the item in the tree
            for i in range(self.scene_tree.topLevelItemCount()):
                item = self.scene_tree.topLevelItem(i)
                if self._find_game_object_in_item(item, game_object):
                    self.scene_tree.setCurrentItem(item)
                    break
        except Exception as e:
            self.logger.error(f"Failed to select GameObject: {e}")
    
    def _find_game_object_in_item(self, item: QTreeWidgetItem, target_game_object: 'GameObject') -> bool:
        """Recursively search for a GameObject in a tree item."""
        try:
            game_object = item.data(0, Qt.ItemDataRole.UserRole)
            if game_object and game_object.id == target_game_object.id:
                return True
            
            # Search children
            for i in range(item.childCount()):
                child_item = item.child(i)
                if self._find_game_object_in_item(child_item, target_game_object):
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f"Failed to find GameObject in item: {e}")
            return False
    
    # Performance optimization methods
    def optimize_layout_performance(self):
        """Optimize the layout for better performance."""
        try:
            # Optimize the main layout
            layout_optimizer.optimize_layout(
                self.layout(), 
                "scene_panel_main", 
                layout_optimizer.OptimizationLevel.ADAPTIVE
            )
            
            # Cache widget positions
            layout_optimizer.cache_widget_positions(self.layout(), "scene_panel_main")
            
            # Pre-calculate common spacing values
            spacing_cache_system.preload_spacing_values([
                ("scene_panel_margins", SpacingUnit.MEDIUM, {}),
                ("scene_panel_padding", SpacingUnit.SMALL, {}),
                ("scene_tree_spacing", SpacingUnit.XSMALL, {}),
                ("header_spacing", SpacingUnit.SMALL, {})
            ])
            
            self.logger.info("ScenePanel layout performance optimized")
            
        except Exception as e:
            self.logger.error(f"Failed to optimize layout performance: {e}")
    
    def get_optimized_spacing(self, base_spacing: Union[int, SpacingUnit], calculation_type: str) -> int:
        """Get optimized spacing value using the performance calculator.
        
        Args:
            base_spacing: Base spacing value or unit
            calculation_type: Type of calculation for optimization
            
        Returns:
            Optimized spacing value
        """
        try:
            return optimized_spacing_calculator.calculate_optimized_spacing(
                base_spacing,
                optimized_spacing_calculator.CalculationType(calculation_type),
                self
            )
        except Exception as e:
            self.logger.error(f"Failed to get optimized spacing: {e}")
            # Fallback to standard spacing
            if isinstance(base_spacing, SpacingUnit):
                return base_spacing.value
            return base_spacing
    
    def batch_optimize_spacing(self, spacing_calculations: List[Tuple[Union[int, SpacingUnit], str]]) -> List[int]:
        """Batch optimize multiple spacing calculations for better performance.
        
        Args:
            spacing_calculations: List of (base_spacing, calculation_type) tuples
            
        Returns:
            List of optimized spacing values
        """
        try:
            # Convert to the format expected by the batch calculator
            calculations = [
                (spacing, optimized_spacing_calculator.CalculationType(calc_type), self, {})
                for spacing, calc_type in spacing_calculations
            ]
            
            return optimized_spacing_calculator.batch_calculate_spacing(calculations)
            
        except Exception as e:
            self.logger.error(f"Failed to batch optimize spacing: {e}")
            # Fallback to individual calculations
            results = []
            for base_spacing, calc_type in spacing_calculations:
                results.append(self.get_optimized_spacing(base_spacing, calc_type))
            return results
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the ScenePanel.
        
        Returns:
            Dictionary of performance metrics
        """
        try:
            # Get layout performance metrics
            layout_metrics = layout_optimizer.get_layout_performance_metrics("scene_panel_main")
            
            # Get cache performance metrics
            cache_metrics = spacing_cache_system.get_cache_stats()
            
            # Get calculator performance metrics
            calculator_metrics = optimized_spacing_calculator.get_performance_metrics()
            
            return {
                'layout': layout_metrics.__dict__ if layout_metrics else {},
                'cache': cache_metrics,
                'calculator': calculator_metrics,
                'panel_id': 'scene_panel',
                'optimization_level': 'adaptive'
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance metrics: {e}")
            return {}


class PropertiesPanel(QWidget):
    """Panel for editing entity and component properties."""
    
    def __init__(self, game_engine):
        """Initialize the properties panel.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        self.current_entity_id = None
        
        self._setup_ui()
        
        self.logger.info("Properties panel initialized")
    
    def _setup_ui(self):
        """Setup the user interface using design system."""
        from .design_system.spacing_system import spacing, SpacingUnit
        from .design_system.typography_system import typography, FontSize, FontWeight
        from .design_system.alignment_system import alignment, HorizontalAlignment
        from .components.standard_button import StandardButton
        
        layout = QVBoxLayout()
        
        # Apply panel spacing and professional styling
        panel_margin, panel_padding = spacing.get_panel_spacing()
        layout.setContentsMargins(panel_margin, panel_margin, panel_margin, panel_margin)
        layout.setSpacing(spacing.get_section_spacing())
        
        # Apply panel styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2d2d30;
                color: #cccccc;
            }}
        """)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(spacing.get_item_spacing())
        
        header_label = QLabel("Properties")
        header_font = QFont()
        header_font.setPointSize(typography.get_header_style()[0])
        header_font.setWeight(typography.get_header_style()[1])
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"""
            QLabel {{
                color: #cccccc;
                padding: {spacing.sm}px;
                background-color: #3e3e42;
                border-radius: 4px;
                border: 1px solid #555555;
            }}
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Properties content with proper styling
        self.properties_content = QTextEdit()
        self.properties_content.setReadOnly(True)
        self.properties_content.setPlaceholderText("Select an entity to view properties")
        self.properties_content.setStyleSheet(f"""
            QTextEdit {{
                padding: {panel_padding}px;
                border: 1px solid #555555;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: #cccccc;
                font-size: {typography.sm}px;
                font-weight: {typography.normal};
                font-family: 'Consolas', monospace;
            }}
        """)
        layout.addWidget(self.properties_content)
        
        # Apply button using standard button component
        self.apply_btn = StandardButton("Apply Changes", size="medium", variant="primary")
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self._apply_changes)
        layout.addWidget(self.apply_btn)
        
        self.setLayout(layout)
    
    def set_entity(self, entity_id: str):
        """Set the entity to display properties for.
        
        Args:
            entity_id: ID of the entity
        """
        self.current_entity_id = entity_id
        self._update_properties()
    
    def _update_properties(self):
        """Update the properties display."""
        if not self.current_entity_id or not self.game_engine:
            self.properties_content.setPlainText("No entity selected")
            return
        
        entity = self.game_engine.entity_manager.get_entity(self.current_entity_id)
        if not entity:
            self.properties_content.setPlainText("Entity not found")
            return
        
        # Display entity properties
        properties_text = f"Entity: {entity.name}\n"
        properties_text += f"ID: {entity.id}\n"
        properties_text += f"Active: {entity.active}\n"
        properties_text += f"Tags: {', '.join(entity.tags) if entity.tags else 'None'}\n"
        properties_text += f"Created: {entity.created_at}\n\n"
        
        # Display components
        components = self.game_engine.component_manager.get_entity_components(self.current_entity_id)
        if components:
            properties_text += "Components:\n"
            for component in components:
                properties_text += f"- {type(component).__name__}\n"
        else:
            properties_text += "No components"
        
        self.properties_content.setPlainText(properties_text)
    
    def _apply_changes(self):
        """Apply property changes."""
        self.logger.info("Applying property changes")
        # TODO: Implement property application
        self._update_properties()


class AssetsPanel(QWidget):
    """Panel for managing assets."""
    
    asset_selected = pyqtSignal(str)  # Asset path
    
    def __init__(self, game_engine):
        """Initialize the assets panel.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        self._setup_ui()
        
        self.logger.info("Assets panel initialized")
    
    def _setup_ui(self):
        """Setup the user interface using design system."""
        from .design_system.spacing_system import spacing, SpacingUnit
        from .design_system.typography_system import typography, FontSize, FontWeight
        from .design_system.alignment_system import alignment, HorizontalAlignment
        from .components.standard_button import StandardButton
        
        layout = QVBoxLayout()
        
        # Apply panel spacing and professional styling
        panel_margin, panel_padding = spacing.get_panel_spacing()
        layout.setContentsMargins(panel_margin, panel_margin, panel_margin, panel_margin)
        layout.setSpacing(spacing.get_section_spacing())
        
        # Apply panel styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2d2d30;
                color: #cccccc;
            }}
        """)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(spacing.get_item_spacing())
        
        header_label = QLabel("Assets")
        header_font = QFont()
        header_font.setPointSize(typography.get_header_style()[0])
        header_font.setWeight(typography.get_header_style()[1])
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"""
            QLabel {{
                color: #cccccc;
                padding: {spacing.sm}px;
                background-color: #3e3e42;
                border-radius: 4px;
                border: 1px solid #555555;
            }}
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        # Search box with proper styling
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search assets...")
        self.search_box.textChanged.connect(self._filter_assets)
        self.search_box.setStyleSheet(f"""
            QLineEdit {{
                padding: {spacing.sm}px;
                border: 1px solid #333333;
                border-radius: 4px;
                background-color: #1a1a1a;
                color: #fafafa;
                font-size: {typography.sm}px;
            }}
            QLineEdit:focus {{
                border: 1px solid #ff6b35;
                background-color: #262626;
            }}
            QLineEdit:hover {{
                border: 1px solid #ff8c42;
                background-color: #262626;
            }}
            QLineEdit::placeholder {{
                color: #a3a3a3;
            }}
        """)
        header_layout.addWidget(self.search_box)
        
        layout.addLayout(header_layout)
        
        # Assets list with proper styling
        self.assets_list = QListWidget()
        self.assets_list.itemSelectionChanged.connect(self._on_asset_selected)
        self.assets_list.setStyleSheet(f"""
            QListWidget {{
                padding: {panel_padding}px;
                border: 1px solid #555555;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: #cccccc;
                font-size: {typography.sm}px;
            }}
            QListWidget::item {{
                padding: {spacing.sm}px;
                border-radius: 4px;
                min-height: {spacing.button_height}px;
            }}
            QListWidget::item:hover {{
                background-color: #3e3e42;
            }}
            QListWidget::item:selected {{
                background-color: #0078d4;
                color: white;
            }}
        """)
        layout.addWidget(self.assets_list)
        
        # Button layout with proper spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(spacing.get_item_spacing())
        
        # Import button using standard button component
        import_btn = StandardButton("Import Asset", size="medium", variant="primary")
        import_btn.clicked.connect(self._import_asset)
        button_layout.addWidget(import_btn)
        
        # Refresh button using standard button component
        refresh_btn = StandardButton("Refresh", size="medium", variant="secondary")
        refresh_btn.clicked.connect(self._refresh_assets)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _filter_assets(self, text: str):
        """Filter assets based on search text.
        
        Args:
            text: Search text
        """
        # TODO: Implement asset filtering
        pass
    
    def _on_asset_selected(self):
        """Handle asset selection."""
        current_item = self.assets_list.currentItem()
        if current_item:
            asset_path = current_item.data(Qt.ItemDataRole.UserRole)
            self.asset_selected.emit(asset_path)
    
    def _import_asset(self):
        """Import a new asset."""
        self.logger.info("Importing asset")
        # TODO: Implement asset import
        self._refresh_assets()
    
    def _refresh_assets(self):
        """Refresh the assets list."""
        self.assets_list.clear()
        
        # TODO: Load actual assets from the asset manager
        # For now, add some placeholder assets
        placeholder_assets = [
            "models/cube.obj",
            "models/sphere.obj",
            "textures/metal.png",
            "textures/wood.jpg",
            "sounds/explosion.wav"
        ]
        
        for asset_path in placeholder_assets:
            item = QListWidgetItem(asset_path)
            item.setData(Qt.ItemDataRole.UserRole, asset_path)
            self.assets_list.addItem(item)
        
        self.logger.debug("Assets list refreshed")


class ConsolePanel(QWidget):
    """Panel for displaying console output and logs."""
    
    def __init__(self, game_engine):
        """Initialize the console panel.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        self._setup_ui()
        
        self.logger.info("Console panel initialized")
    
    def _setup_ui(self):
        """Setup the user interface using design system."""
        from .design_system.spacing_system import spacing, SpacingUnit
        from .design_system.typography_system import typography, FontSize, FontWeight
        from .design_system.alignment_system import alignment, HorizontalAlignment
        from .components.standard_button import StandardButton
        
        layout = QVBoxLayout()
        
        # Apply panel spacing and professional styling
        panel_margin, panel_padding = spacing.get_panel_spacing()
        layout.setContentsMargins(panel_margin, panel_margin, panel_margin, panel_margin)
        layout.setSpacing(spacing.get_section_spacing())
        
        # Apply panel styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2d2d30;
                color: #cccccc;
            }}
        """)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(spacing.get_item_spacing())
        
        header_label = QLabel("Console")
        header_font = QFont()
        header_font.setPointSize(typography.get_header_style()[0])
        header_font.setWeight(typography.get_header_style()[1])
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"""
            QLabel {{
                color: #cccccc;
                padding: {spacing.sm}px;
                background-color: #3e3e42;
                border-radius: 4px;
                border: 1px solid #555555;
            }}
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        # Clear button using standard button component
        clear_btn = StandardButton("Clear", size="small", variant="secondary")
        clear_btn.clicked.connect(self._clear_console)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # Console output with proper styling
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setFont(QFont("Consolas", 10))
        self.console_output.setStyleSheet(f"""
            QTextEdit {{
                padding: {panel_padding}px;
                border: 1px solid #555555;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: #cccccc;
                font-size: {typography.sm}px;
                font-family: 'Consolas', monospace;
            }}
        """)
        layout.addWidget(self.console_output)
        
        # Command input layout with proper spacing
        input_layout = QHBoxLayout()
        input_layout.setSpacing(spacing.get_item_spacing())
        
        # Command input with proper styling
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.returnPressed.connect(self._execute_command)
        self.command_input.setStyleSheet(f"""
            QLineEdit {{
                padding: {spacing.sm}px;
                border: 1px solid #333333;
                border-radius: 4px;
                background-color: #1a1a1a;
                color: #fafafa;
                font-size: {typography.sm}px;
            }}
            QLineEdit:focus {{
                border: 1px solid #ff6b35;
                background-color: #262626;
            }}
            QLineEdit:hover {{
                border: 1px solid #ff8c42;
                background-color: #262626;
            }}
            QLineEdit::placeholder {{
                color: #a3a3a3;
            }}
        """)
        input_layout.addWidget(self.command_input)
        
        # Execute button using standard button component
        execute_btn = StandardButton("Execute", size="small", variant="primary")
        execute_btn.clicked.connect(self._execute_command)
        input_layout.addWidget(execute_btn)
        
        layout.addLayout(input_layout)
        
        # Add initial console message
        self._add_message("Console initialized. Type 'help' for available commands.", "INFO")
        
        self.setLayout(layout)
    
    def _add_message(self, message: str, level: str = "INFO"):
        """Add a message to the console.
        
        Args:
            message: Message text
            level: Message level (INFO, WARNING, ERROR, DEBUG)
        """
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Format message with timestamp and level
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] [{level}] {message}\n"
        
        cursor.insertText(formatted_message)
        
        # Auto-scroll to bottom
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()
    
    def _clear_console(self):
        """Clear the console output."""
        self.console_output.clear()
        self._add_message("Console cleared.", "INFO")
    
    def _execute_command(self):
        """Execute a console command."""
        command = self.command_input.text().strip()
        if not command:
            return
        
        self._add_message(f"Executing: {command}", "COMMAND")
        
        # Handle basic commands
        if command.lower() == "help":
            self._show_help()
        elif command.lower() == "clear":
            self._clear_console()
        elif command.lower() == "status":
            self._show_status()
        elif command.lower() == "entities":
            self._show_entities()
        else:
            self._add_message(f"Unknown command: {command}", "ERROR")
        
        self.command_input.clear()
    
    def _show_help(self):
        """Show available commands."""
        help_text = """
Available commands:
- help: Show this help
- clear: Clear console
- status: Show engine status
- entities: List all entities
        """
        for line in help_text.strip().split('\n'):
            self._add_message(line, "HELP")
    
    def _show_status(self):
        """Show engine status."""
        if self.game_engine and self.game_engine.is_initialized:
            stats = self.game_engine.get_stats()
            self._add_message(f"Engine Status: FPS={stats.fps:.1f}, Entities={stats.entity_count}", "INFO")
        else:
            self._add_message("Engine not initialized", "WARNING")
    
    def _show_entities(self):
        """List all entities."""
        if self.game_engine and self.game_engine.entity_manager:
            entities = self.game_engine.entity_manager.entities
            self._add_message(f"Total entities: {len(entities)}", "INFO")
            for entity_id, entity in entities.items():
                self._add_message(f"- {entity.name} (ID: {entity_id[:8]}...)", "INFO")
        else:
            self._add_message("Entity manager not available", "WARNING")


class InspectorPanel(QWidget):
    """Panel for detailed object inspection."""
    
    def __init__(self, game_engine):
        """Initialize the inspector panel.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        self.current_object = None
        
        self._setup_ui()
        
        self.logger.info("Inspector panel initialized")
    
    def _setup_ui(self):
        """Setup the user interface using design system."""
        from .design_system.spacing_system import spacing, SpacingUnit
        from .design_system.typography_system import typography, FontSize, FontWeight
        from .design_system.alignment_system import alignment, HorizontalAlignment
        from .components.standard_button import StandardButton
        
        layout = QVBoxLayout()
        
        # Apply panel spacing and professional styling
        panel_margin, panel_padding = spacing.get_panel_spacing()
        layout.setContentsMargins(panel_margin, panel_margin, panel_margin, panel_margin)
        layout.setSpacing(spacing.get_section_spacing())
        
        # Apply panel styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2d2d30;
                color: #cccccc;
            }}
        """)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(spacing.get_item_spacing())
        
        header_label = QLabel("Inspector")
        header_font = QFont()
        header_font.setPointSize(typography.get_header_style()[0])
        header_font.setWeight(typography.get_header_style()[1])
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"""
            QLabel {{
                color: #cccccc;
                padding: {spacing.sm}px;
                background-color: #3e3e42;
                border-radius: 4px;
                border: 1px solid #555555;
            }}
        """)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        # Refresh button using standard button component
        refresh_btn = StandardButton("Refresh", size="small", variant="secondary")
        refresh_btn.clicked.connect(self._refresh_inspector)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Inspector content with proper styling
        self.inspector_content = QTextEdit()
        self.inspector_content.setReadOnly(True)
        self.inspector_content.setPlaceholderText("Select an object to inspect")
        self.inspector_content.setStyleSheet(f"""
            QTextEdit {{
                padding: {panel_padding}px;
                border: 1px solid #555555;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: #cccccc;
                font-size: {typography.sm}px;
                font-weight: {typography.normal};
                font-family: 'Consolas', monospace;
            }}
        """)
        layout.addWidget(self.inspector_content)
        
        self.setLayout(layout)
        
        # Connect to responsive spacing manager for breakpoint changes
        responsive_spacing_manager.connect_breakpoint_changed(self._on_breakpoint_changed)
    
    def _on_breakpoint_changed(self, breakpoint_name: str):
        """Handle breakpoint changes from responsive spacing system.
        
        Args:
            breakpoint_name: New breakpoint name
        """
        self.logger.info(f"InspectorPanel breakpoint changed to: {breakpoint_name}")
        self._update_responsive_spacing()
    
    def _update_responsive_spacing(self):
        """Update spacing based on current breakpoint."""
        try:
            current_breakpoint = responsive_spacing_manager.get_current_breakpoint()
            
            # Get responsive spacing values
            responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.md)
            responsive_padding = responsive_spacing_manager.get_responsive_spacing(spacing.sm)
            responsive_section_spacing = responsive_spacing_manager.get_responsive_spacing(spacing.get_section_spacing())
            
            # Update layout margins
            layout = self.layout()
            if layout:
                layout.setContentsMargins(responsive_margin, responsive_margin, 
                                        responsive_margin, responsive_margin)
                layout.setSpacing(responsive_section_spacing)
            
            # Apply updated styling
            self._apply_responsive_styling()
            
            self.logger.info(f"Updated InspectorPanel spacing for breakpoint: {current_breakpoint.value}")
            
        except Exception as e:
            self.logger.error(f"Failed to update InspectorPanel responsive spacing: {e}")
    
    def _apply_responsive_styling(self):
        """Apply responsive styling to the InspectorPanel."""
        try:
            current_breakpoint = responsive_spacing_manager.get_current_breakpoint()
            
            # Get responsive spacing values
            responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.md)
            responsive_padding = responsive_spacing_manager.get_responsive_spacing(spacing.sm)
            
            # Update inspector content styling with responsive spacing
            if hasattr(self, 'inspector_content'):
                content_style = f"""
                    QTextEdit {{
                        padding: {responsive_padding}px;
                        border: 1px solid #555555;
                        border-radius: 6px;
                        background-color: #1e1e1e;
                        color: #cccccc;
                        font-size: {typography.sm}px;
                        font-weight: {typography.normal};
                        font-family: 'Consolas', monospace;
                    }}
                """
                self.inspector_content.setStyleSheet(content_style)
            
        except Exception as e:
            self.logger.error(f"Failed to apply responsive styling: {e}")
    
    def get_responsive_spacing(self, base_spacing, touch_friendly: bool = False):
        """Get responsive spacing value for current breakpoint.
        
        Args:
            base_spacing: Base spacing value
            touch_friendly: Whether to apply touch-friendly adjustments
            
        Returns:
            Responsive spacing value
        """
        return responsive_spacing_manager.get_responsive_spacing(base_spacing, touch_friendly)
    
    def animate_spacing_change(self, start_spacing: int, end_spacing: int, 
                             duration: int = 300, easing: EasingType = EasingType.EASE_IN_OUT):
        """Animate spacing change for the InspectorPanel.
        
        Args:
            start_spacing: Starting spacing value
            end_spacing: Ending spacing value
            duration: Animation duration in milliseconds
            easing: Easing curve type
        """
        return spacing_animation_manager.animate_spacing_change(
            self, start_spacing, end_spacing, duration, easing
        )
    
    def get_current_breakpoint(self) -> str:
        """Get current breakpoint name.
        
        Returns:
            Current breakpoint name
        """
        return responsive_spacing_manager.get_current_breakpoint().value
    
    # Performance optimization methods
    def optimize_layout_performance(self):
        """Optimize the layout for better performance."""
        try:
            # Optimize the main layout
            layout_optimizer.optimize_layout(
                self.layout(), 
                "inspector_panel_main", 
                layout_optimizer.OptimizationLevel.ADAPTIVE
            )
            
            # Cache widget positions
            layout_optimizer.cache_widget_positions(self.layout(), "inspector_panel_main")
            
            # Pre-calculate common spacing values
            spacing_cache_system.preload_spacing_values([
                ("inspector_panel_margins", SpacingUnit.MEDIUM, {}),
                ("inspector_panel_padding", SpacingUnit.SMALL, {}),
                ("inspector_content_spacing", SpacingUnit.XSMALL, {}),
                ("header_spacing", SpacingUnit.SMALL, {})
            ])
            
            self.logger.info("InspectorPanel layout performance optimized")
            
        except Exception as e:
            self.logger.error(f"Failed to optimize layout performance: {e}")
    
    def get_optimized_spacing(self, base_spacing: Union[int, SpacingUnit], calculation_type: str) -> int:
        """Get optimized spacing value using the performance calculator.
        
        Args:
            base_spacing: Base spacing value or unit
            calculation_type: Type of calculation for optimization
            
        Returns:
            Optimized spacing value
        """
        try:
            return optimized_spacing_calculator.calculate_optimized_spacing(
                base_spacing,
                optimized_spacing_calculator.CalculationType(calculation_type),
                self
            )
        except Exception as e:
            self.logger.error(f"Failed to get optimized spacing: {e}")
            # Fallback to standard spacing
            if isinstance(base_spacing, SpacingUnit):
                return base_spacing.value
            return base_spacing
    
    def batch_optimize_spacing(self, spacing_calculations: List[Tuple[Union[int, SpacingUnit], str]]) -> List[int]:
        """Batch optimize multiple spacing calculations for better performance.
        
        Args:
            spacing_calculations: List of (base_spacing, calculation_type) tuples
            
        Returns:
            List of optimized spacing values
        """
        try:
            # Convert to the format expected by the batch calculator
            calculations = [
                (spacing, optimized_spacing_calculator.CalculationType(calc_type), self, {})
                for spacing, calc_type in spacing_calculations
            ]
            
            return optimized_spacing_calculator.batch_calculate_spacing(calculations)
            
        except Exception as e:
            self.logger.error(f"Failed to batch optimize spacing: {e}")
            # Fallback to individual calculations
            results = []
            for base_spacing, calc_type in spacing_calculations:
                results.append(self.get_optimized_spacing(base_spacing, calc_type))
            return results
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the InspectorPanel.
        
        Returns:
            Dictionary of performance metrics
        """
        try:
            # Get layout performance metrics
            layout_metrics = layout_optimizer.get_layout_performance_metrics("inspector_panel_main")
            
            # Get cache performance metrics
            cache_metrics = spacing_cache_system.get_cache_stats()
            
            # Get calculator performance metrics
            calculator_metrics = optimized_spacing_calculator.get_performance_metrics()
            
            return {
                'layout': layout_metrics.__dict__ if layout_metrics else {},
                'cache': cache_metrics,
                'calculator': calculator_metrics,
                'panel_id': 'inspector_panel',
                'optimization_level': 'adaptive'
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance metrics: {e}")
            return {}
    
    def inspect_object(self, obj):
        """Inspect a specific object.
        
        Args:
            obj: Object to inspect
        """
        self.current_object = obj
        self._update_inspector()
    
    def _update_inspector(self):
        """Update the inspector display."""
        if not self.current_object:
            self.inspector_content.setPlainText("No object selected")
            return
        
        # Display object information
        obj_info = f"Object: {type(self.current_object).__name__}\n"
        obj_info += f"ID: {id(self.current_object)}\n\n"
        
        # Display object attributes
        obj_info += "Attributes:\n"
        for attr_name in dir(self.current_object):
            if not attr_name.startswith('_'):
                try:
                    attr_value = getattr(self.current_object, attr_name)
                    if not callable(attr_value):
                        obj_info += f"- {attr_name}: {attr_value}\n"
                except Exception:
                    obj_info += f"- {attr_name}: <error>\n"
        
        self.inspector_content.setPlainText(obj_info)
    
    def _refresh_inspector(self):
        """Refresh the inspector display."""
        self._update_inspector()
