#!/usr/bin/env python3
"""
IDE Center Panel - 3D Viewport Component.

This replicates the React Center Panel component exactly using QWebEngineView
for pixel-perfect reproduction, just like the header and left panel.
"""

from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QKeyEvent, QWheelEvent
from PyQt6.QtCore import QEvent


class IDECenterPanel(QWidget):
    """
    Center Panel - 3D Viewport with tabs.
    
    Uses QWebEngineView to embed the React component directly,
    ensuring pixel-perfect reproduction.
    """
    
    # Signals
    tab_changed = pyqtSignal(str)
    tab_added = pyqtSignal(str)
    tab_closed = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._current_tab = "Main Scene"
        self._tabs = ["Main Scene", "Game Logic", "Materials"]
        
        # Setup UI
        self._setup_ui()
        self._setup_zoom_prevention()
        self._setup_connections()
        
    def _setup_ui(self):
        """Setup the center panel web view interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create splitter for viewport and asset browser
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(self.splitter)
        
        # Create web view for center panel (3D viewport)
        self.web_view = QWebEngineView()
        self.web_view.setObjectName("centerPanelWebView")
        
        # Create custom web page
        self.web_page = self._create_custom_web_page()
        self.web_view.setPage(self.web_page)
        
        # Load the React component
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "assets")
        center_panel_path = os.path.join(assets_dir, "center_panel.html")
        print(f"DEBUG: Loading Center Panel from: {center_panel_path}")
        print(f"DEBUG: File exists: {os.path.exists(center_panel_path)}")
        self.web_view.load(QUrl.fromLocalFile(center_panel_path))
        
        # Connect load finished signal
        self.web_view.loadFinished.connect(self._on_web_loaded)
        
        # Add viewport to splitter
        self.splitter.addWidget(self.web_view)
        
        # Ensure the web view has proper size policy
        self.web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Create asset browser
        from .ide_asset_browser import IDEAssetBrowser
        from ..asset.asset_manager import AssetManager
        
        # Create a temporary asset manager for now
        temp_asset_manager = AssetManager()
        self.asset_browser = IDEAssetBrowser(temp_asset_manager, self)
        
        # Ensure the asset browser has proper size policy
        self.asset_browser.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Add asset browser to splitter
        self.splitter.addWidget(self.asset_browser)
        
        # Set splitter sizes (viewport gets more space, asset browser gets less)
        self.splitter.setSizes([700, 200])
        
        # Make the splitter handle visible and styled
        self.splitter.setHandleWidth(4)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 2px;
            }
            QSplitter::handle:hover {
                background: rgba(255, 140, 66, 0.3);
            }
        """)
        
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
        print("DEBUG: Center Panel web page loaded")
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
        bridge_script = f"""
        // Python bridge for center panel
        window.pythonBridge = {{
            // Tab management
            switchTab: function(tabName) {{
                console.log('DEBUG: Switching to tab:', tabName);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'tab_changed',
                    data: tabName
                }}));
            }},
            
            // Add new tab
            addTab: function(tabName) {{
                console.log('DEBUG: Adding new tab:', tabName);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'tab_added',
                    data: tabName
                }}));
            }},
            
            // Close tab
            closeTab: function(tabName) {{
                console.log('DEBUG: Closing tab:', tabName);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'tab_closed',
                    data: tabName
                }}));
            }},
            
            // Viewport controls
            setViewportMode: function(mode) {{
                console.log('DEBUG: Setting viewport mode:', mode);
                // TODO: Implement viewport mode switching
            }},
            
            // Minimap interaction
            updateMinimap: function(data) {{
                console.log('DEBUG: Updating minimap:', data);
                // TODO: Implement minimap updates
            }}
        }};
        
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
    def setCurrentTab(self, tab_name: str):
        """Set the current active tab."""
        self._current_tab = tab_name
        # Update via JavaScript
        script = f"window.pythonBridge.switchTab('{tab_name}');"
        self.web_view.page().runJavaScript(script)
        
    def getCurrentTab(self) -> str:
        """Get the currently active tab."""
        return self._current_tab
        
    def addTab(self, tab_name: str):
        """Add a new tab."""
        if tab_name not in self._tabs:
            self._tabs.append(tab_name)
            # Update via JavaScript
            script = f"window.pythonBridge.addTab('{tab_name}');"
            self.web_view.page().runJavaScript(script)
            
    def closeTab(self, tab_name: str):
        """Close a tab."""
        if tab_name in self._tabs and len(self._tabs) > 1:
            self._tabs.remove(tab_name)
            # Update via JavaScript
            script = f"window.pythonBridge.closeTab('{tab_name}');"
            self.web_view.page().runJavaScript(script)
            
    def getTabs(self) -> list:
        """Get all available tabs."""
        return self._tabs.copy()
        
    def setViewportMode(self, mode: str):
        """Set the viewport mode (e.g., '3D', '2D', 'Wireframe')."""
        # Update via JavaScript
        script = f"window.pythonBridge.setViewportMode('{mode}');"
        self.web_view.page().runJavaScript(script)
        
    def updateMinimap(self, data: dict):
        """Update the minimap with new data."""
        # Update via JavaScript
        import json
        script = f"window.pythonBridge.updateMinimap({json.dumps(data)});"
        self.web_view.page().runJavaScript(script)
        
    # Asset Browser integration methods
    def getAssetBrowser(self):
        """Get the asset browser component."""
        return self.asset_browser
        
    def setAssetCategory(self, category: str):
        """Set the asset browser category."""
        if hasattr(self, 'asset_browser'):
            self.asset_browser.setCategory(category)
            
    def selectAsset(self, asset_name: str, asset_type: str):
        """Select an asset in the asset browser."""
        if hasattr(self, 'asset_browser'):
            self.asset_browser.selectAsset(asset_name, asset_type)
            
    def searchAssets(self, search_term: str):
        """Search for assets in the asset browser."""
        if hasattr(self, 'asset_browser'):
            self.asset_browser.searchAssets(search_term)
            
    def refreshAssets(self):
        """Refresh the asset browser."""
        if hasattr(self, 'asset_browser'):
            self.asset_browser.refreshAssets()
