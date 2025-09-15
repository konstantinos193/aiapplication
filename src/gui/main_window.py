"""
Main application window for the Nexlify Engine editor.

This has been replaced by the Game Design IDE for a modern, professional interface.
The old main window is kept for backward compatibility but the new IDE is recommended.
"""

from typing import Optional, Dict, Any, TYPE_CHECKING
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QToolBar, QStatusBar, QLabel,
    QPushButton, QMessageBox, QFileDialog, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QKeySequence, QAction

if TYPE_CHECKING:
    from ..core.engine import GameEngine
    from .panels import ScenePanel

from ..utils.logger import get_logger
from .responsive import responsive_spacing_manager, Breakpoint
from .animations import spacing_animation_manager, EasingType
from .design_system.spacing_system import spacing


class MainWindow(QMainWindow):
    """Main application window for the Nexlify Engine editor."""
    
    # Signals
    game_object_created = pyqtSignal(object)  # Emits GameObject when created
    scene_changed = pyqtSignal(str)  # Emits scene name when changed
    
    def __init__(self, game_engine: 'GameEngine'):
        super().__init__()
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        self._setup_ui()
        self._setup_connections()
        self._setup_timer()
        
        self.logger.info("MainWindow initialized successfully")
    
    def show_error_dialog(self, message: str):
        """Show an error dialog with the given message."""
        try:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", message)
        except Exception as e:
            self.logger.error(f"Failed to show error dialog: {e}")
            # Fallback: just log the error
            self.logger.error(f"ERROR: {message}")
    
    def _setup_ui(self):
        """Setup the main user interface."""
        self.logger.info("Setting up UI...")
        self.setWindowTitle("Nexlify Engine - Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        self.logger.info("Creating central widget...")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        self.logger.info("Creating main layout...")
        main_layout = QVBoxLayout(central_widget)
        self.logger.info("Main layout created successfully")
        
        # Create menu bar
        self.logger.info("Creating menu bar...")
        self._create_menu_bar()
        
        # Create tool bar
        self.logger.info("Creating tool bar...")
        self._create_tool_bar()
        
        # Create main splitter for left and center/right
        self.logger.info("Creating main splitter...")
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Create scene panel (left)
        self.logger.info("Creating scene panel...")
        from .panels import ScenePanel
        self.scene_panel = ScenePanel(self)
        main_splitter.addWidget(self.scene_panel)
        
        # Create center/right splitter
        self.logger.info("Creating center/right splitter...")
        center_right_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(center_right_splitter)
        
        # Create 3D Viewport Panel (center)
        self.logger.info("Creating viewport panel...")
        from .viewport_panel import ViewportPanel
        self.viewport_panel = ViewportPanel(self)
        center_right_splitter.addWidget(self.viewport_panel)
        
        # Create AI Chat Panel (right)
        self.logger.info("Creating AI chat panel...")
        from .ai_chat_panel import AIChatPanel
        self.ai_chat_panel = AIChatPanel(self)
        center_right_splitter.addWidget(self.ai_chat_panel)
        
        # Set splitter proportions
        main_splitter.setSizes([400, 1000])
        center_right_splitter.setSizes([800, 400])
        
        # Create bottom splitter for Assets and Inspector
        self.logger.info("Creating bottom splitter...")
        bottom_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(bottom_splitter)
        
        # Create collapsible Assets panel (bottom left)
        self.logger.info("Creating assets panel...")
        self._create_assets_panel()
        bottom_splitter.addWidget(self.assets_panel)
        
        # Create collapsible Inspector panel (bottom right)
        self.logger.info("Creating inspector panel...")
        self._create_inspector_panel()
        bottom_splitter.addWidget(self.inspector_panel)
        
        # Set bottom splitter proportions
        bottom_splitter.setSizes([600, 400])
        
        # Create status bar
        self.logger.info("Creating status bar...")
        self._create_status_bar()
        
        # Connect scene panel signals
        self.scene_panel.game_object_selected.connect(self._on_game_object_selected)
        
        # Connect viewport panel signals
        self.viewport_panel.selection_changed.connect(self._on_viewport_selection_changed)
        
        self.logger.info("UI setup completed successfully")
    
    def _create_menu_bar(self):
        """Create the application menu bar."""
        self.logger.info("Starting menu bar creation...")
        try:
            menubar = self.menuBar()
            self.logger.info("Menu bar created")
            
            # File menu
            self.logger.info("Creating File menu...")
            file_menu = menubar.addMenu("File")
            
            new_scene_action = QAction("New Scene", self)
            new_scene_action.setShortcut(QKeySequence.StandardKey.New)
            new_scene_action.triggered.connect(self._new_scene)
            file_menu.addAction(new_scene_action)
            self.logger.info("New Scene action added")
            
            open_scene_action = QAction("Open Scene", self)
            open_scene_action.setShortcut(QKeySequence.StandardKey.Open)
            open_scene_action.triggered.connect(self._open_scene)
            file_menu.addAction(open_scene_action)
            self.logger.info("Open Scene action added")
            
            save_scene_action = QAction("Save Scene", self)
            save_scene_action.setShortcut(QKeySequence.StandardKey.Save)
            save_scene_action.triggered.connect(self._save_scene)
            file_menu.addAction(save_scene_action)
            self.logger.info("Save Scene action added")
            
            file_menu.addSeparator()
            
            exit_action = QAction("Exit", self)
            exit_action.setShortcut(QKeySequence.StandardKey.Quit)
            exit_action.triggered.connect(self.close)
            file_menu.addAction(exit_action)
            self.logger.info("Exit action added")
            
            # Edit menu
            self.logger.info("Creating Edit menu...")
            edit_menu = menubar.addMenu("Edit")
            
            undo_action = QAction("Undo", self)
            undo_action.setShortcut(QKeySequence.StandardKey.Undo)
            edit_menu.addAction(undo_action)
            
            redo_action = QAction("Redo", self)
            redo_action.setShortcut(QKeySequence.StandardKey.Redo)
            edit_menu.addAction(redo_action)
            
            edit_menu.addSeparator()
            
            select_all_action = QAction("Select All", self)
            select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
            edit_menu.addAction(select_all_action)
            self.logger.info("Edit menu created")
            
            # GameObject menu
            self.logger.info("Creating GameObject menu...")
            gameobject_menu = menubar.addMenu("GameObject")
            
            create_empty_action = QAction("Create Empty", self)
            create_empty_action.triggered.connect(self._create_empty)
            gameobject_menu.addAction(create_empty_action)
            
            create_3d_menu = gameobject_menu.addMenu("3D Object")
            
            create_cube_action = QAction("Cube", self)
            create_cube_action.triggered.connect(self._create_cube)
            create_3d_menu.addAction(create_cube_action)
            
            create_sphere_action = QAction("Sphere", self)
            create_sphere_action.triggered.connect(self._create_sphere)
            create_3d_menu.addAction(create_sphere_action)
            
            create_light_menu = gameobject_menu.addMenu("Light")
            
            create_point_light_action = QAction("Point Light", self)
            create_point_light_action.triggered.connect(lambda: self._create_light("Point"))
            create_light_menu.addAction(create_point_light_action)
            
            create_directional_light_action = QAction("Directional Light", self)
            create_directional_light_action.triggered.connect(lambda: self._create_light("Directional"))
            create_light_menu.addAction(create_directional_light_action)
            
            create_spot_light_action = QAction("Spot Light", self)
            create_spot_light_action.triggered.connect(lambda: self._create_light("Spot"))
            create_light_menu.addAction(create_spot_light_action)
            
            create_camera_action = QAction("Camera", self)
            create_camera_action.triggered.connect(self._create_camera)
            gameobject_menu.addAction(create_camera_action)
            self.logger.info("GameObject menu created")
            
            # AI Tools menu
            self.logger.info("Creating AI Tools menu...")
            ai_menu = menubar.addMenu("AI Tools")
            
            code_generator_action = QAction("Code Generator", self)
            code_generator_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
            code_generator_action.triggered.connect(self._show_code_generator)
            ai_menu.addAction(code_generator_action)
            
            asset_generator_action = QAction("Asset Generator", self)
            asset_generator_action.setShortcut(QKeySequence("Ctrl+Shift+A"))
            asset_generator_action.triggered.connect(self._show_asset_generator)
            ai_menu.addAction(asset_generator_action)
            
            scene_builder_action = QAction("Scene Builder", self)
            scene_builder_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
            scene_builder_action.triggered.connect(self._show_scene_builder)
            ai_menu.addAction(scene_builder_action)
            
            problem_solver_action = QAction("Problem Solver", self)
            problem_solver_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
            problem_solver_action.triggered.connect(self._show_problem_solver)
            ai_menu.addAction(problem_solver_action)
            self.logger.info("AI Tools menu created")
            
            # Window menu
            self.logger.info("Creating Window menu...")
            window_menu = menubar.addMenu("Window")
            
            # Panel visibility toggles
            toggle_scene_panel_action = QAction("Scene Panel", self)
            toggle_scene_panel_action.setCheckable(True)
            toggle_scene_panel_action.setChecked(True)
            toggle_scene_panel_action.triggered.connect(self._toggle_scene_panel)
            window_menu.addAction(toggle_scene_panel_action)
            
            toggle_viewport_panel_action = QAction("Viewport Panel", self)
            toggle_viewport_panel_action.setCheckable(True)
            toggle_viewport_panel_action.setChecked(True)
            toggle_viewport_panel_action.triggered.connect(self._toggle_viewport_panel)
            window_menu.addAction(toggle_viewport_panel_action)
            
            toggle_ai_chat_panel_action = QAction("AI Chat Panel", self)
            toggle_ai_chat_panel_action.setCheckable(True)
            toggle_ai_chat_panel_action.setChecked(True)
            toggle_ai_chat_panel_action.triggered.connect(self._toggle_ai_chat_panel)
            window_menu.addAction(toggle_ai_chat_panel_action)
            
            toggle_assets_panel_action = QAction("Assets Panel", self)
            toggle_assets_panel_action.setCheckable(True)
            toggle_assets_panel_action.setChecked(True)
            toggle_assets_panel_action.triggered.connect(self._toggle_assets_panel)
            window_menu.addAction(toggle_assets_panel_action)
            
            toggle_inspector_panel_action = QAction("Inspector Panel", self)
            toggle_inspector_panel_action.setCheckable(True)
            toggle_inspector_panel_action.setChecked(True)
            toggle_inspector_panel_action.triggered.connect(self._toggle_inspector_panel)
            window_menu.addAction(toggle_inspector_panel_action)
            self.logger.info("Window menu created")
            
            # Help menu
            self.logger.info("Creating Help menu...")
            help_menu = menubar.addMenu("Help")
            
            about_action = QAction("About", self)
            about_action.triggered.connect(self._show_about)
            help_menu.addAction(about_action)
            
            help_action = QAction("Help", self)
            help_action.triggered.connect(self._show_help)
            help_menu.addAction(help_action)
            self.logger.info("Help menu created")
            
            self.logger.info("Menu bar creation completed successfully")
        except Exception as e:
            self.logger.error(f"Error creating menu bar: {e}")
            raise
    
    def _create_assets_panel(self):
        """Create the collapsible assets panel."""
        from .assets_panel import AssetsPanel
        self.assets_panel = AssetsPanel(self)
        self.assets_panel.setMaximumHeight(200)  # Default collapsed height
        self.assets_panel.setMinimumHeight(50)   # Minimum height when collapsed
    
    def _create_inspector_panel(self):
        """Create the collapsible inspector panel."""
        from .inspector_panel import InspectorPanel
        self.inspector_panel = InspectorPanel(self)
        self.inspector_panel.setMaximumHeight(300)  # Default expanded height
        self.inspector_panel.setMinimumHeight(50)   # Minimum height when collapsed
    
    def _create_tool_bar(self):
        """Create the main tool bar."""
        toolbar = self.addToolBar("Main Toolbar")
        
        # Scene controls
        new_scene_btn = QPushButton("New Scene")
        new_scene_btn.clicked.connect(self._new_scene)
        toolbar.addWidget(new_scene_btn)
        
        open_scene_btn = QPushButton("Open Scene")
        open_scene_btn.clicked.connect(self._open_scene)
        toolbar.addWidget(open_scene_btn)
        
        save_scene_btn = QPushButton("Save Scene")
        save_scene_btn.clicked.connect(self._save_scene)
        toolbar.addWidget(save_scene_btn)
        
        toolbar.addSeparator()
        
        # GameObject creation
        create_cube_btn = QPushButton("Cube")
        create_cube_btn.clicked.connect(self._create_cube)
        toolbar.addWidget(create_cube_btn)
        
        create_sphere_btn = QPushButton("Sphere")
        create_sphere_btn.clicked.connect(self._create_sphere)
        toolbar.addWidget(create_sphere_btn)
        
        create_light_btn = QPushButton("Light")
        create_light_btn.clicked.connect(lambda: self._create_light("Point"))
        toolbar.addWidget(create_light_btn)
        
        create_camera_btn = QPushButton("Camera")
        create_camera_btn.clicked.connect(self._create_camera)
        toolbar.addWidget(create_camera_btn)
        
        toolbar.addSeparator()
        
        # AI Tools
        ai_code_btn = QPushButton("AI Code")
        ai_code_btn.setToolTip("AI Code Generator")
        ai_code_btn.clicked.connect(self._show_code_generator)
        toolbar.addWidget(ai_code_btn)
        
        ai_asset_btn = QPushButton("AI Asset")
        ai_asset_btn.setToolTip("AI Asset Generator")
        ai_asset_btn.clicked.connect(self._show_asset_generator)
        toolbar.addWidget(ai_asset_btn)
        
        ai_scene_btn = QPushButton("AI Scene")
        ai_scene_btn.setToolTip("AI Scene Builder")
        ai_scene_btn.clicked.connect(self._show_scene_builder)
        toolbar.addWidget(ai_scene_btn)
        
        toolbar.addSeparator()
        
        # Play controls
        play_btn = QPushButton("▶")
        play_btn.setToolTip("Play Scene")
        play_btn.clicked.connect(self._play_scene)
        toolbar.addWidget(play_btn)
        
        pause_btn = QPushButton("⏸")
        pause_btn.setToolTip("Pause Scene")
        pause_btn.clicked.connect(self._pause_scene)
        toolbar.addWidget(pause_btn)
        
        stop_btn = QPushButton("⏹")
        stop_btn.setToolTip("Stop Scene")
        stop_btn.clicked.connect(self._stop_scene)
        toolbar.addWidget(stop_btn)
    
    def _create_status_bar(self):
        """Create the status bar."""
        status_bar = self.statusBar()
        
        # Scene info
        self.scene_info_label = QLabel("Scene: Default Scene")
        status_bar.addWidget(self.scene_info_label)
        
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Object count
        self.object_count_label = QLabel("GameObjects: 0")
        status_bar.addPermanentWidget(self.object_count_label)
        
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Scene status
        self.scene_status_label = QLabel("Status: Stopped")
        status_bar.addPermanentWidget(self.scene_status_label)
        
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Responsive spacing indicator
        self.responsive_spacing_label = QLabel("Breakpoint: Desktop")
        status_bar.addPermanentWidget(self.responsive_spacing_label)
        
        # Connect to responsive spacing manager
        responsive_spacing_manager.connect_breakpoint_changed(self._on_breakpoint_changed)
    
    def _setup_connections(self):
        """Setup signal connections."""
        # Connect to game engine signals if available
        pass
    
    def _setup_timer(self):
        """Setup timer for periodic updates."""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_ui)
        self.update_timer.start(1000)  # Update every second
    
    def _on_breakpoint_changed(self, breakpoint_name: str):
        """Handle breakpoint changes from responsive spacing system.
        
        Args:
            breakpoint_name: New breakpoint name
        """
        if hasattr(self, 'responsive_spacing_label'):
            self.responsive_spacing_label.setText(f"Breakpoint: {breakpoint_name.title()}")
        
        # Log the breakpoint change
        self.logger.info(f"Breakpoint changed to: {breakpoint_name}")
        
        # Update UI spacing if needed
        self._update_ui_spacing()
    
    def _update_ui_spacing(self):
        """Update UI spacing based on current breakpoint."""
        try:
            current_breakpoint = responsive_spacing_manager.get_current_breakpoint()
            
            # Apply responsive spacing to main components
            if hasattr(self, 'scene_panel'):
                # Update scene panel spacing
                responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.md)
                self.scene_panel.set_content_margins(
                    responsive_margin, responsive_margin, 
                    responsive_margin, responsive_margin
                )
            
            if hasattr(self, 'viewport_panel'):
                # Update viewport panel spacing
                responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.sm)
                # Apply to viewport if it has spacing methods
            
            self.logger.info(f"Updated UI spacing for breakpoint: {current_breakpoint.value}")
            
        except Exception as e:
            self.logger.error(f"Failed to update UI spacing: {e}")
    
    def _new_scene(self):
        """Create a new scene."""
        try:
            scene_name = f"Scene_{len(self.game_engine.scenes) + 1}"
            new_scene = self.game_engine.create_scene(scene_name)
            self.game_engine.set_current_scene(scene_name)
            
            # Refresh the scene panel
            self.scene_panel.refresh()
            
            self.logger.info(f"Created new scene: {scene_name}")
            self.scene_changed.emit(scene_name)
            
        except Exception as e:
            self.logger.error(f"Failed to create new scene: {e}")
            QMessageBox.critical(self, "Error", f"Failed to create new scene: {e}")
    
    def _open_scene(self):
        """Open an existing scene."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open Scene", "", "Scene Files (*.json);;All Files (*)"
            )
            
            if file_path:
                # In a real implementation, this would load the scene from file
                self.logger.info(f"Opening scene from: {file_path}")
                QMessageBox.information(self, "Info", "Scene loading not yet implemented")
                
        except Exception as e:
            self.logger.error(f"Failed to open scene: {e}")
            QMessageBox.critical(self, "Error", f"Failed to open scene: {e}")
    
    def _save_scene(self):
        """Save the current scene."""
        try:
            if not self.game_engine.current_scene:
                QMessageBox.warning(self, "Warning", "No scene to save")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Scene", "", "Scene Files (*.json);;All Files (*)"
            )
            
            if file_path:
                # In a real implementation, this would save the scene to file
                self.logger.info(f"Saving scene to: {file_path}")
                QMessageBox.information(self, "Info", "Scene saving not yet implemented")
                
        except Exception as e:
            self.logger.error(f"Failed to save scene: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save scene: {e}")
    
    def _create_empty(self):
        """Create an empty GameObject."""
        try:
            game_object = self.game_engine.create_empty("Empty")
            if game_object:
                self.scene_panel.refresh()
                self.game_object_created.emit(game_object)
                self.logger.info("Created empty GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create empty GameObject: {e}")
    
    def _create_cube(self):
        """Create a cube GameObject."""
        try:
            game_object = self.game_engine.create_cube("Cube")
            if game_object:
                self.scene_panel.refresh()
                self.game_object_created.emit(game_object)
                self.logger.info("Created cube GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create cube GameObject: {e}")
    
    def _create_sphere(self):
        """Create a sphere GameObject."""
        try:
            game_object = self.game_engine.create_sphere("Sphere")
            if game_object:
                self.scene_panel.refresh()
                self.game_object_created.emit(game_object)
                self.logger.info("Created sphere GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create sphere GameObject: {e}")
    
    def _create_light(self, light_type: str):
        """Create a light GameObject."""
        try:
            game_object = self.game_engine.create_light(f"{light_type} Light", light_type)
            if game_object:
                self.scene_panel.refresh()
                self.game_object_created.emit(game_object)
                self.logger.info(f"Created {light_type} light GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create {light_type} light GameObject: {e}")
    
    def _create_camera(self):
        """Create a camera GameObject."""
        try:
            game_object = self.game_engine.create_camera("Camera")
            if game_object:
                self.scene_panel.refresh()
                self.game_object_created.emit(game_object)
                self.logger.info("Created camera GameObject")
        except Exception as e:
            self.logger.error(f"Failed to create camera GameObject: {e}")
    
    def _play_scene(self):
        """Start playing the current scene."""
        try:
            self.game_engine.play_scene()
            self.logger.info("Started playing scene")
        except Exception as e:
            self.logger.error(f"Failed to play scene: {e}")
    
    def _pause_scene(self):
        """Pause the current scene."""
        try:
            self.game_engine.pause_scene()
            self.logger.info("Paused scene")
        except Exception as e:
            self.logger.error(f"Failed to pause scene: {e}")
    
    def _stop_scene(self):
        """Stop the current scene."""
        try:
            self.game_engine.stop_scene()
            self.logger.info("Stopped scene")
        except Exception as e:
            self.logger.error(f"Failed to stop scene: {e}")
    
    def _on_game_object_selected(self, game_object):
        """Handle when a GameObject is selected."""
        try:
            self.logger.info(f"Selected GameObject: {game_object.name}")
            # Update the inspector panel
            self.inspector_panel.inspect_game_object(game_object)
            # Update the viewport selection
            self.viewport_panel.set_selection(game_object)
        except Exception as e:
            self.logger.error(f"Failed to handle GameObject selection: {e}")
    
    def _on_viewport_selection_changed(self, game_object):
        """Handle when a GameObject is selected in the viewport."""
        try:
            if game_object:
                self.logger.info(f"Viewport selected GameObject: {game_object.name}")
                # Update the inspector panel
                self.inspector_panel.inspect_game_object(game_object)
                # Update the scene panel selection
                self.scene_panel.select_game_object(game_object)
            else:
                self.logger.info("Viewport selection cleared")
                # Clear the inspector panel
                self.inspector_panel.clear_selection()
        except Exception as e:
            self.logger.error(f"Failed to handle viewport selection change: {e}")
    
    # Panel visibility toggle methods
    def _toggle_scene_panel(self, checked: bool):
        """Toggle the visibility of the scene panel."""
        try:
            if checked:
                self.scene_panel.show()
                self.logger.info("Scene panel shown")
            else:
                self.scene_panel.hide()
                self.logger.info("Scene panel hidden")
        except Exception as e:
            self.logger.error(f"Failed to toggle scene panel: {e}")
    
    def _toggle_viewport_panel(self, checked: bool):
        """Toggle the visibility of the viewport panel."""
        try:
            if checked:
                self.viewport_panel.show()
                self.logger.info("Viewport panel shown")
            else:
                self.viewport_panel.hide()
                self.logger.info("Viewport panel hidden")
        except Exception as e:
            self.logger.error(f"Failed to toggle viewport panel: {e}")
    
    def _toggle_ai_chat_panel(self, checked: bool):
        """Toggle the visibility of the AI chat panel."""
        try:
            if checked:
                self.ai_chat_panel.show()
                self.logger.info("AI chat panel shown")
            else:
                self.ai_chat_panel.hide()
                self.logger.info("AI chat panel hidden")
        except Exception as e:
            self.logger.error(f"Failed to toggle AI chat panel: {e}")
    
    def _toggle_assets_panel(self, checked: bool):
        """Toggle the visibility of the assets panel."""
        try:
            if checked:
                self.assets_panel.show()
                self.logger.info("Assets panel shown")
            else:
                self.assets_panel.hide()
                self.logger.info("Assets panel hidden")
        except Exception as e:
            self.logger.error(f"Failed to toggle assets panel: {e}")
    
    def _toggle_inspector_panel(self, checked: bool):
        """Toggle the visibility of the inspector panel."""
        try:
            if checked:
                self.inspector_panel.show()
                self.logger.info("Inspector panel shown")
            else:
                self.inspector_panel.hide()
                self.logger.info("Inspector panel hidden")
        except Exception as e:
            self.logger.error(f"Failed to toggle inspector panel: {e}")
    
    # AI Tools methods
    def _show_code_generator(self):
        """Show the Code Generator tab in the AI Chat panel."""
        try:
            self.ai_chat_panel.tab_widget.setCurrentIndex(1)
            self.logger.info("Switched to Code Generator tab")
        except Exception as e:
            self.logger.error(f"Failed to show Code Generator tab: {e}")
    
    def _show_asset_generator(self):
        """Show the Object Creator tab in the AI Chat panel."""
        try:
            self.ai_chat_panel.tab_widget.setCurrentIndex(2)
            self.logger.info("Switched to Object Creator tab")
        except Exception as e:
            self.logger.error(f"Failed to show Object Creator tab: {e}")
    
    def _show_scene_builder(self):
        """Show the Scene Builder tab in the AI Chat panel."""
        try:
            self.ai_chat_panel.tab_widget.setCurrentIndex(3)
            self.logger.info("Switched to Scene Builder tab")
        except Exception as e:
            self.logger.error(f"Failed to show Scene Builder tab: {e}")
    
    def _show_problem_solver(self):
        """Show the Chat tab in the AI Chat panel."""
        try:
            self.ai_chat_panel.tab_widget.setCurrentIndex(0)
            self.logger.info("Switched to Chat tab")
        except Exception as e:
            self.logger.error(f"Failed to show Chat tab: {e}")
    
    # Help methods
    def _show_help(self):
        """Show the help dialog."""
        try:
            help_text = """
Nexlify Engine - Game Development Editor

Keyboard Shortcuts:
- Ctrl+N: New Scene
- Ctrl+O: Open Scene  
- Ctrl+S: Save Scene
- Ctrl+Shift+C: AI Code Generator
- Ctrl+Shift+A: AI Asset Generator
- Ctrl+Shift+S: AI Scene Builder
- Ctrl+Shift+P: AI Problem Solver
- F5: Play Scene
- F6: Pause Scene
- F7: Stop Scene

Panel Controls:
- Use Window menu to toggle panel visibility
- Drag panel borders to resize
- Use Viewport toolbar for camera and view controls
            """
            QMessageBox.information(self, "Help", help_text)
            self.logger.info("Help dialog shown")
        except Exception as e:
            self.logger.error(f"Failed to show help dialog: {e}")
    
    def _show_about(self):
        """Show the about dialog."""
        try:
            about_text = """
Nexlify Engine v1.0.0

A Unity-like game development editor built with Python and PyQt6.

Features:
- 3D Scene Editor
- GameObject Management
- AI-Powered Development Tools
- Asset Management
- Real-time Inspector
- Professional UI Layout

Built with modern Python technologies for game development.
            """
            QMessageBox.about(self, "About Nexlify Engine", about_text)
            self.logger.info("About dialog shown")
        except Exception as e:
            self.logger.error(f"Failed to show about dialog: {e}")
    
    def _update_ui(self):
        """Update the UI elements."""
        try:
            # Update scene info
            if self.game_engine.current_scene:
                scene = self.game_engine.current_scene
                self.scene_info_label.setText(f"Scene: {scene.name}")
                
                # Update object count
                object_count = scene.get_object_count()
                self.object_count_label.setText(f"GameObjects: {object_count}")
                
                # Update scene status
                if scene.is_scene_playing():
                    if scene.is_scene_paused():
                        self.scene_status_label.setText("Status: Paused")
                    else:
                        self.scene_status_label.setText("Status: Playing")
                else:
                    self.scene_status_label.setText("Status: Stopped")
            else:
                self.scene_info_label.setText("Scene: None")
                self.object_count_label.setText("GameObjects: 0")
                self.scene_status_label.setText("Status: No Scene")
                
        except Exception as e:
            self.logger.error(f"Failed to update UI: {e}")
    
    def closeEvent(self, event):
        """Handle window close event."""
        try:
            # Shutdown the game engine
            self.game_engine.shutdown()
            self.logger.info("MainWindow closed")
            event.accept()
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            event.accept()
