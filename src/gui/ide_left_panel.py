#!/usr/bin/env python3
"""
IDE Left Panel - Scene Hierarchy and Inspector Components.

This replicates the React left panel exactly using QWebEngineView
for pixel-perfect reproduction, just like the header.
"""

from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMenu, QInputDialog
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QKeyEvent, QWheelEvent, QAction
from PyQt6.QtCore import QEvent

from .utils.svg_loader import load_svg_icon


class SceneHierarchyWebView(QWidget):
    """
    Scene Hierarchy Web View - EXACTLY matching React component.
    
    Uses QWebEngineView to embed the React component directly,
    ensuring pixel-perfect reproduction.
    """
    
    # Signals
    object_selected = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._selected_object = "Player"
        self._expanded_nodes = {"environment"}
        self._search_query = ""
        
        # Game engine reference
        self.game_engine = None
        
        # Setup UI
        self._setup_ui()
        self._setup_zoom_prevention()
        self._setup_connections()
    
    def set_game_engine(self, game_engine):
        """Set the game engine reference."""
        self.game_engine = game_engine
        print(f"DEBUG: Game engine reference set: {game_engine}")
        
    def _setup_ui(self):
        """Setup the scene hierarchy web view interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setObjectName("sceneHierarchyWebView")
        
        # Create custom web page
        self.web_page = self._create_custom_web_page()
        self.web_view.setPage(self.web_page)
        
        # Load the React component
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "assets")
        scene_hierarchy_path = os.path.join(assets_dir, "scene_hierarchy.html")
        print(f"DEBUG: Loading Scene Hierarchy from: {scene_hierarchy_path}")
        print(f"DEBUG: File exists: {os.path.exists(scene_hierarchy_path)}")
        self.web_view.load(QUrl.fromLocalFile(scene_hierarchy_path))
        
        # Connect load finished signal
        self.web_view.loadFinished.connect(self._on_web_loaded)
        
        # Add to layout
        main_layout.addWidget(self.web_view)
        
    def _create_custom_web_page(self) -> QWebEnginePage:
        """Create a custom web page with zoom prevention."""
        web_page = QWebEnginePage()
        
        # Get settings
        settings = web_page.settings()
        
        # DISABLE ZOOM FUNCTIONALITY
        try:
            if hasattr(QWebEngineSettings, 'ZoomTextOnly'):
                settings.setAttribute(QWebEngineSettings.ZoomTextOnly, False)
                print("DEBUG: Zoom text only disabled")
        except:
            pass

        try:
            zoom_attributes = [
                'ZoomTextOnly', 'ZoomFactor', 'ZoomLevel', 'DefaultZoomLevel',
                'MinimumZoomLevel', 'MaximumZoomLevel'
            ]
            for attr_name in zoom_attributes:
                if hasattr(QWebEngineSettings, attr_name):
                    try:
                        if attr_name in ['ZoomTextOnly']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), False)
                        elif attr_name in ['DefaultZoomLevel', 'ZoomLevel']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), 1.0)
                        print(f"DEBUG: {attr_name} setting configured")
                    except Exception as e:
                        print(f"DEBUG: Could not configure {attr_name}: {e}")
        except Exception as e:
            print(f"DEBUG: Error configuring zoom settings: {e}")
        
        return web_page
        
    def _setup_zoom_prevention(self):
        """Setup zoom prevention mechanisms."""
        # Install event filter
        self.installEventFilter(self)
        
        # Setup timer for zoom prevention
        self._setup_zoom_prevention_timer()
        
        # Set initial zoom factor
        self.web_view.setZoomFactor(1.0)
        
        # ENABLE context menu for real functionality
        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.web_view.customContextMenuRequested.connect(self._show_real_context_menu)
        
    def _setup_zoom_prevention_timer(self):
        """Setup timer to enforce zoom prevention."""
        self._zoom_prevention_timer = QTimer()
        self._zoom_prevention_timer.timeout.connect(self._enforce_zoom_prevention)
        self._zoom_prevention_timer.start(100)
        
    def _enforce_zoom_prevention(self):
        """Enforce zoom prevention by resetting zoom factor."""
        if hasattr(self, 'web_view') and self.web_view:
            current_zoom = self.web_view.zoomFactor()
            if current_zoom != 1.0:
                print(f"DEBUG: Zoom factor was {current_zoom}, resetting to 1.0")
                self.web_view.setZoomFactor(1.0)
    
    def _show_real_context_menu(self, position):
        """Show a real context menu with actual functionality."""
        try:
            print(f"DEBUG: Showing context menu at position: {position}")
            print(f"DEBUG: Game engine reference: {self.game_engine}")
            
            # Create context menu
            menu = QMenu(self)
            
            # Add Entity section
            menu.addSection("Entity")
            
            # Create Empty GameObject
            create_empty_action = QAction("Create Empty GameObject", self)
            create_empty_action.triggered.connect(self._create_empty_game_object)
            menu.addAction(create_empty_action)
            
            # Create 3D Object submenu
            create_3d_menu = QMenu("3D Object", self)
            
            # 3D Object types
            cube_action = QAction("Cube", self)
            cube_action.triggered.connect(lambda: self._create_3d_object("Cube"))
            create_3d_menu.addAction(cube_action)
            
            sphere_action = QAction("Sphere", self)
            sphere_action.triggered.connect(lambda: self._create_3d_object("Sphere"))
            create_3d_menu.addAction(sphere_action)
            
            cylinder_action = QAction("Cylinder", self)
            cylinder_action.triggered.connect(lambda: self._create_3d_object("Cylinder"))
            create_3d_menu.addAction(cylinder_action)
            
            plane_action = QAction("Plane", self)
            plane_action.triggered.connect(lambda: self._create_3d_object("Plane"))
            create_3d_menu.addAction(plane_action)
            
            menu.addMenu(create_3d_menu)
            
            # Create Light submenu
            create_light_menu = QMenu("Light", self)
            
            directional_action = QAction("Directional Light", self)
            directional_action.triggered.connect(lambda: self._create_light("Directional"))
            create_light_menu.addAction(directional_action)
            
            point_action = QAction("Point Light", self)
            point_action.triggered.connect(lambda: self._create_light("Point"))
            create_light_menu.addAction(point_action)
            
            spot_action = QAction("Spot Light", self)
            spot_action.triggered.connect(lambda: self._create_light("Spot"))
            create_light_menu.addAction(spot_action)
            
            menu.addMenu(create_light_menu)
            
            # Create Camera
            camera_action = QAction("Camera", self)
            camera_action.triggered.connect(self._create_camera)
            menu.addAction(camera_action)
            
            menu.addSeparator()
            
            # Add Component section
            menu.addSection("Component")
            
            # Add Component action
            add_component_action = QAction("Add Component...", self)
            add_component_action.triggered.connect(self._show_add_component_menu)
            menu.addAction(add_component_action)
            
            # Show the menu at the cursor position
            menu.exec(self.web_view.mapToGlobal(position))
            
        except Exception as e:
            print(f"ERROR: Failed to show context menu: {e}")
    
    def _create_empty_game_object(self):
        """Create an empty GameObject."""
        try:
            name, ok = QInputDialog.getText(self, "Create GameObject", "Enter name:")
            if ok and name.strip():
                print(f"DEBUG: Creating empty GameObject: {name}")
                if self.game_engine:
                    # TODO: Actually create the GameObject in the engine
                    print(f"DEBUG: Would create GameObject '{name}' in engine")
                else:
                    print("DEBUG: No game engine reference available")
                self._refresh_scene_hierarchy()
        except Exception as e:
            print(f"ERROR: Failed to create empty GameObject: {e}")
    
    def _create_3d_object(self, object_type: str):
        """Create a 3D object of the specified type."""
        try:
            name, ok = QInputDialog.getText(self, f"Create {object_type}", f"Enter {object_type} name:")
            if ok and name.strip():
                print(f"DEBUG: Creating {object_type}: {name}")
                # TODO: Actually create the 3D object in the engine
                self._refresh_scene_hierarchy()
        except Exception as e:
            print(f"ERROR: Failed to create {object_type}: {e}")
    
    def _create_light(self, light_type: str):
        """Create a light of the specified type."""
        try:
            name, ok = QInputDialog.getText(self, f"Create {light_type} Light", f"Enter {light_type} Light name:")
            if ok and name.strip():
                print(f"DEBUG: Creating {light_type} Light: {name}")
                # TODO: Actually create the light in the engine
                self._refresh_scene_hierarchy()
        except Exception as e:
            print(f"ERROR: Failed to create {light_type} Light: {e}")
    
    def _create_camera(self):
        """Create a camera GameObject."""
        try:
            name, ok = QInputDialog.getText(self, "Create Camera", "Enter camera name:")
            if ok and name.strip():
                print(f"DEBUG: Creating Camera: {name}")
                # TODO: Actually create the camera in the engine
                self._refresh_scene_hierarchy()
        except Exception as e:
            print(f"ERROR: Failed to create Camera: {e}")
    
    def _show_add_component_menu(self):
        """Show the add component menu."""
        try:
            from PyQt6.QtWidgets import QMenu, QAction
            
            # Create component submenu
            component_menu = QMenu(self)
            
            # Physics components
            component_menu.addSection("Physics")
            
            rigidbody_action = QAction("Rigidbody", self)
            rigidbody_action.triggered.connect(lambda: self._add_component("Rigidbody"))
            component_menu.addAction(rigidbody_action)
            
            collider_action = QAction("Collider", self)
            collider_action.triggered.connect(lambda: self._add_component("Collider"))
            component_menu.addAction(collider_action)
            
            # Rendering components
            component_menu.addSection("Rendering")
            
            mesh_renderer_action = QAction("Mesh Renderer", self)
            mesh_renderer_action.triggered.connect(lambda: self._add_component("Mesh Renderer"))
            component_menu.addAction(mesh_renderer_action)
            
            # Audio components
            component_menu.addSection("Audio")
            
            audio_source_action = QAction("Audio Source", self)
            audio_source_action.triggered.connect(lambda: self._add_component("Audio Source"))
            component_menu.addAction(audio_source_action)
            
            # Script components
            component_menu.addSection("Scripts")
            
            script_action = QAction("Script", self)
            script_action.triggered.connect(lambda: self._add_component("Script"))
            component_menu.addAction(script_action)
            
            # Show the component menu
            component_menu.exec(self.mapToGlobal(self.rect().center()))
            
        except Exception as e:
            print(f"ERROR: Failed to show add component menu: {e}")
    
    def _add_component(self, component_type: str):
        """Add a component of the specified type to the selected object."""
        try:
            print(f"DEBUG: Adding {component_type} component to {self._selected_object}")
            # TODO: Actually add the component in the engine
        except Exception as e:
            print(f"ERROR: Failed to add {component_type} component: {e}")
    
    def _refresh_scene_hierarchy(self):
        """Refresh the scene hierarchy display."""
        try:
            print("DEBUG: Refreshing scene hierarchy")
            # TODO: Actually refresh the scene hierarchy
            # This would update the web view with new objects
        except Exception as e:
            print(f"ERROR: Failed to refresh scene hierarchy: {e}")
    
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.RightButton:
            # Show context menu on right-click
            self._show_real_context_menu(event.pos())
        else:
            super().mousePressEvent(event)
        
    def _setup_connections(self):
        """Setup signal connections."""
        # Search input connection will be handled via JavaScript
        pass
        
    def _on_web_loaded(self):
        """Handle web page load completion."""
        print("DEBUG: Scene Hierarchy web page loaded")
        self._inject_zoom_prevention_script()
        self._inject_python_bridge()
        
    def _inject_zoom_prevention_script(self):
        """Inject JavaScript to prevent zooming."""
        zoom_prevention_script = """
        // Disable zoom through JavaScript
        (function() {
            'use strict';
            
            // Prevent keyboard shortcuts
            document.addEventListener('keydown', function(e) {
                if ((e.ctrlKey || e.metaKey) && 
                    (e.key === '+' || e.key === '-' || e.key === '=' || e.key === '0')) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('DEBUG: Zoom shortcut prevented');
                    return false;
                }
            }, true);
            
            // Prevent wheel zoom
            document.addEventListener('wheel', function(e) {
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('DEBUG: Ctrl+wheel zoom prevented');
                    return false;
                }
            }, { passive: false });
            
            // Prevent touch zoom
            document.addEventListener('gesturestart', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('DEBUG: Touch zoom prevented');
                return false;
            }, { passive: false });
            
            // Prevent double-tap zoom
            document.addEventListener('touchend', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('DEBUG: Double-tap zoom prevented');
                return false;
            }, false);
            
            // Set viewport meta tag
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) {
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
            } else {
                const meta = document.createElement('meta');
                meta.name = 'viewport';
                meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                document.head.appendChild(meta);
            }
            
            console.log('DEBUG: Zoom prevention JavaScript injected successfully');
        })();
        """
        
        self.web_view.page().runJavaScript(zoom_prevention_script)
        
    def _inject_python_bridge(self):
        """Inject Python bridge for communication."""
        bridge_script = """
        // Python bridge for scene hierarchy
        window.pythonBridge = {
            // Object selection
            selectObject: function(objectName) {
                console.log('DEBUG: Object selected:', objectName);
                // This will be connected to PyQt signals
            },
            
            // Search query
            setSearchQuery: function(query) {
                console.log('DEBUG: Search query:', query);
                // This will be connected to PyQt signals
            },
            
            // Node expansion
            toggleNode: function(nodeId) {
                console.log('DEBUG: Toggle node:', nodeId);
                // This will be connected to PyQt signals
            }
        };
        
        console.log('DEBUG: Python bridge injected successfully');
        """
        
        self.web_view.page().runJavaScript(bridge_script)
        
    def eventFilter(self, obj, event):
        """Event filter to prevent zoom events."""
        if event.type() == QEvent.Type.Wheel:
            wheel_event = QWheelEvent(event)
            if wheel_event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                print("DEBUG: Ctrl+wheel zoom prevented")
                return True
        elif event.type() == QEvent.Type.KeyPress:
            if hasattr(event, 'key') and hasattr(event, 'modifiers'):
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal, Qt.Key.Key_0]:
                        print("DEBUG: Ctrl+Plus/Minus/0 zoom prevented")
                        return True
        return super().eventFilter(obj, event)
        
    def wheelEvent(self, event):
        """Handle wheel events to prevent zoom."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            print("DEBUG: Ctrl+wheel zoom prevented in wheelEvent")
            event.accept()
            return
        super().wheelEvent(event)
        
    def keyPressEvent(self, event):
        """Handle key press events to prevent zoom."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal, Qt.Key.Key_0]:
                print("DEBUG: Ctrl+Plus/Minus/0 zoom prevented in keyPressEvent")
                event.accept()
                return
        super().keyPressEvent(event)
        
    # Public API methods
    def setSelectedObject(self, object_name: str):
        """Set the selected object."""
        self._selected_object = object_name
        # Update via JavaScript
        script = f"window.pythonBridge.selectObject('{object_name}');"
        self.web_view.page().runJavaScript(script)
        
    def getSelectedObject(self) -> str:
        """Get the currently selected object."""
        return self._selected_object
        
    def setSearchQuery(self, query: str):
        """Set the search query."""
        self._search_query = query
        # Update via JavaScript
        script = f"window.pythonBridge.setSearchQuery('{query}');"
        self.web_view.page().runJavaScript(script)
        
    def getSearchQuery(self) -> str:
        """Get the current search query."""
        return self._search_query


class InspectorWebView(QWidget):
    """
    Inspector Web View - EXACTLY matching React component.
    
    Uses QWebEngineView to embed the React component directly,
    ensuring pixel-perfect reproduction.
    """
    
    # Signals
    transform_changed = pyqtSignal(dict)  # position, rotation, scale
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._selected_object = "Player"
        
        # Setup UI
        self._setup_ui()
        self._setup_zoom_prevention()
        self._setup_connections()
        
    def _setup_ui(self):
        """Setup the inspector web view interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setObjectName("inspectorWebView")
        
        # Create custom web page
        self.web_page = self._create_custom_web_page()
        self.web_view.setPage(self.web_page)
        
        # Load the React component
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "assets")
        inspector_path = os.path.join(assets_dir, "inspector.html")
        print(f"DEBUG: Loading Inspector from: {inspector_path}")
        print(f"DEBUG: File exists: {os.path.exists(inspector_path)}")
        self.web_view.load(QUrl.fromLocalFile(inspector_path))
        
        # Connect load finished signal
        self.web_view.loadFinished.connect(self._on_web_loaded)
        
        # Add to layout
        main_layout.addWidget(self.web_view)
        
    def _create_custom_web_page(self) -> QWebEnginePage:
        """Create a custom web page with zoom prevention."""
        web_page = QWebEnginePage()
        
        # Get settings
        settings = web_page.settings()
        
        # DISABLE ZOOM FUNCTIONALITY
        try:
            if hasattr(QWebEngineSettings, 'ZoomTextOnly'):
                settings.setAttribute(QWebEngineSettings.ZoomTextOnly, False)
                print("DEBUG: Zoom text only disabled")
        except:
            pass

        try:
            zoom_attributes = [
                'ZoomTextOnly', 'ZoomFactor', 'ZoomLevel', 'DefaultZoomLevel',
                'MinimumZoomLevel', 'MaximumZoomLevel'
            ]
            for attr_name in zoom_attributes:
                if hasattr(QWebEngineSettings, attr_name):
                    try:
                        if attr_name in ['ZoomTextOnly']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), False)
                        elif attr_name in ['DefaultZoomLevel', 'ZoomLevel']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), 1.0)
                        print(f"DEBUG: {attr_name} setting configured")
                    except Exception as e:
                        print(f"DEBUG: Could not configure {attr_name}: {e}")
        except Exception as e:
            print(f"DEBUG: Error configuring zoom settings: {e}")
        
        return web_page
        
    def _setup_zoom_prevention(self):
        """Setup zoom prevention mechanisms."""
        # Install event filter
        self.installEventFilter(self)
        
        # Setup timer for zoom prevention
        self._setup_zoom_prevention_timer()
        
        # Set initial zoom factor
        self.web_view.setZoomFactor(1.0)
        
        # Disable context menu
        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        
    def _setup_zoom_prevention_timer(self):
        """Setup timer to enforce zoom prevention."""
        self._zoom_prevention_timer = QTimer()
        self._zoom_prevention_timer.timeout.connect(self._enforce_zoom_prevention)
        self._zoom_prevention_timer.start(100)
        
    def _enforce_zoom_prevention(self):
        """Enforce zoom prevention by resetting zoom factor."""
        if hasattr(self, 'web_view') and self.web_view:
            current_zoom = self.web_view.zoomFactor()
            if current_zoom != 1.0:
                print(f"DEBUG: Zoom factor was {current_zoom}, resetting to 1.0")
                self.web_view.setZoomFactor(1.0)
                
    def _setup_connections(self):
        """Setup signal connections."""
        pass
        
    def _on_web_loaded(self):
        """Handle web page load completion."""
        print("DEBUG: Inspector web page loaded")
        self._inject_zoom_prevention_script()
        self._inject_python_bridge()
        
    def _inject_zoom_prevention_script(self):
        """Inject JavaScript to prevent zooming."""
        zoom_prevention_script = """
        // Disable zoom through JavaScript
        (function() {
            'use strict';
            
            // Prevent keyboard shortcuts
            document.addEventListener('keydown', function(e) {
                if ((e.ctrlKey || e.metaKey) && 
                    (e.key === '+' || e.key === '-' || e.key === '=' || e.key === '0')) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('DEBUG: Zoom shortcut prevented');
                    return false;
                }
            }, true);
            
            // Prevent wheel zoom
            document.addEventListener('wheel', function(e) {
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('DEBUG: Ctrl+wheel zoom prevented');
                    return false;
                }
            }, { passive: false });
            
            // Prevent touch zoom
            document.addEventListener('gesturestart', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('DEBUG: Touch zoom prevented');
                return false;
            }, { passive: false });
            
            // Prevent double-tap zoom
            document.addEventListener('touchend', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('DEBUG: Double-tap zoom prevented');
                return false;
            }, false);
            
            // Set viewport meta tag
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) {
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
            } else {
                const meta = document.createElement('meta');
                meta.name = 'viewport';
                meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                document.head.appendChild(meta);
            }
            
            console.log('DEBUG: Zoom prevention JavaScript injected successfully');
        })();
        """
        
        self.web_view.page().runJavaScript(zoom_prevention_script)
        
    def _inject_python_bridge(self):
        """Inject Python bridge for communication."""
        bridge_script = """
        // Python bridge for inspector
        window.pythonBridge = {
            // Update selected object
            updateSelectedObject: function(objectName) {
                console.log('DEBUG: Selected object updated:', objectName);
                // Update the header title
                const titleElement = document.querySelector('.text-sm.font-medium.text-foreground');
                if (titleElement) {
                    titleElement.textContent = `Inspector - ${objectName}`;
                }
            },
            
            // Update transform values
            updateTransform: function(position, rotation, scale) {
                console.log('DEBUG: Transform updated:', { position, rotation, scale });
                // TODO: Update input values
            },
            
            // Get transform values
            getTransform: function() {
                const inputs = document.querySelectorAll('input[type="text"]');
                const values = Array.from(inputs).map(input => input.value);
                return {
                    position: values.slice(0, 3),
                    rotation: values.slice(3, 6),
                    scale: values.slice(6, 9)
                };
            }
        };
        
        console.log('DEBUG: Python bridge injected successfully');
        """
        
        self.web_view.page().runJavaScript(bridge_script)
        
    def eventFilter(self, obj, event):
        """Event filter to prevent zoom events."""
        if event.type() == QEvent.Type.Wheel:
            wheel_event = QWheelEvent(event)
            if wheel_event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                print("DEBUG: Ctrl+wheel zoom prevented")
                return True
        elif event.type() == QEvent.Type.KeyPress:
            if hasattr(event, 'key') and hasattr(event, 'modifiers'):
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal, Qt.Key.Key_0]:
                        print("DEBUG: Ctrl+Plus/Minus/0 zoom prevented")
                        return True
        return super().eventFilter(obj, event)
        
    def wheelEvent(self, event):
        """Handle wheel events to prevent zoom."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            print("DEBUG: Ctrl+wheel zoom prevented in wheelEvent")
            event.accept()
            return
        super().wheelEvent(event)
        
    def keyPressEvent(self, event):
        """Handle key press events to prevent zoom."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal, Qt.Key.Key_0]:
                print("DEBUG: Ctrl+Plus/Minus/0 zoom prevented in keyPressEvent")
                event.accept()
                return
        super().keyPressEvent(event)
        
    # Public API methods
    def setSelectedObject(self, object_name: str):
        """Set the selected object."""
        self._selected_object = object_name
        # Update via JavaScript
        script = f"window.pythonBridge.updateSelectedObject('{object_name}');"
        self.web_view.page().runJavaScript(script)
        
    def getSelectedObject(self) -> str:
        """Get the currently selected object."""
        return self._selected_object
        
    def updateTransform(self, position, rotation, scale):
        """Update transform values."""
        # Update via JavaScript
        script = f"window.pythonBridge.updateTransform({position}, {rotation}, {scale});"
        self.web_view.page().runJavaScript(script)
        
    def getTransform(self):
        """Get current transform values."""
        # Get via JavaScript
        script = "window.pythonBridge.getTransform();"
        self.web_view.page().runJavaScript(script)


class IDELeftPanel(QWidget):
    """
    Left panel containing scene hierarchy and inspector.
    
    Features:
    - Scene hierarchy with search and object selection
    - Inspector with transform controls
    - Both components use QWebEngineView for pixel-perfect reproduction
    """
    
    # Signals
    object_selected = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Setup UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the left panel user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scene Hierarchy (web-based)
        self.scene_hierarchy = SceneHierarchyWebView()
        self.scene_hierarchy.object_selected.connect(self._on_object_selected)
        main_layout.addWidget(self.scene_hierarchy)
        
        # Inspector (web-based)
        self.inspector = InspectorWebView()
        main_layout.addWidget(self.inspector)
        
    def _on_object_selected(self, object_name: str):
        """Handle object selection from scene hierarchy."""
        self.object_selected.emit(object_name)
        print(f"DEBUG: Object selected in left panel: {object_name}")
        
        # Update inspector with selected object
        self.inspector.setSelectedObject(object_name)
        
    # Public API methods
    def setSelectedObject(self, object_name: str):
        """Set the selected object."""
        self.scene_hierarchy.setSelectedObject(object_name)
        self.inspector.setSelectedObject(object_name)
        
    def getSelectedObject(self) -> str:
        """Get the currently selected object."""
        return self.scene_hierarchy.getSelectedObject()
        
    def setSearchQuery(self, query: str):
        """Set the search query."""
        self.scene_hierarchy.setSearchQuery(query)
        
    def getSearchQuery(self) -> str:
        """Get the current search query."""
        return self.scene_hierarchy.getSearchQuery()
