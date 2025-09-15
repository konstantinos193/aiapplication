#!/usr/bin/env python3
"""
IDE Asset Browser Component.

This component provides the asset browser functionality for the IDE,
integrating with the asset manager and providing a web-based interface.
"""

from typing import Optional, Dict, Any, List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QKeyEvent, QWheelEvent
from PyQt6.QtCore import QEvent

from ..asset.asset_manager import AssetManager


class IDEAssetBrowser(QWidget):
    """
    Asset Browser component for the IDE.
    
    Provides a web-based interface for browsing, searching, and managing
    game assets with full integration to the asset manager.
    """
    
    # Signals
    asset_selected = pyqtSignal(str, str)  # asset_name, asset_type
    category_changed = pyqtSignal(str)     # category_name
    import_requested = pyqtSignal()        # import dialog requested
    
    def __init__(self, asset_manager: AssetManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Store asset manager reference
        self.asset_manager = asset_manager
        
        # State
        self._current_category = "scripts"
        self._selected_asset = None
        self._search_term = ""
        
        # Setup UI
        self._setup_ui()
        self._setup_zoom_prevention()
        self._setup_connections()
        
    def _setup_ui(self):
        """Setup the asset browser web view interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setObjectName("assetBrowserWebView")
        
        # Create custom web page
        self.web_page = self._create_custom_web_page()
        self.web_view.setPage(self.web_page)
        
        # Load the asset browser component
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "assets")
        asset_browser_path = os.path.join(assets_dir, "asset_browser.html")
        
        print(f"DEBUG: Loading Asset Browser from: {asset_browser_path}")
        print(f"DEBUG: File exists: {os.path.exists(asset_browser_path)}")
        
        self.web_view.load(QUrl.fromLocalFile(asset_browser_path))
        
        # Connect load finished signal
        self.web_view.loadFinished.connect(self._on_web_loaded)
        
        # Add to layout
        main_layout.addWidget(self.web_view)
        
    def _create_custom_web_page(self) -> QWebEnginePage:
        """Create a custom web page with zoom prevention."""
        web_page = QWebEnginePage()
        
        # Get settings
        settings = web_page.settings()
        
        # Disable zoom functionality
        try:
            if hasattr(QWebEngineSettings, 'ZoomTextOnly'):
                settings.setAttribute(QWebEngineSettings.ZoomTextOnly, False)
            if hasattr(QWebEngineSettings, 'DefaultZoomLevel'):
                settings.setAttribute(QWebEngineSettings.DefaultZoomLevel, 1.0)
        except:
            pass
        
        return web_page
        
    def _setup_zoom_prevention(self):
        """Setup zoom prevention mechanisms."""
        # Install event filter
        self.installEventFilter(self)
        
        # Set initial zoom factor
        self.web_view.setZoomFactor(1.0)
        
        # Disable context menu
        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        
    def _setup_connections(self):
        """Setup signal connections."""
        pass
        
    def _on_web_loaded(self):
        """Handle web page load completion."""
        print("DEBUG: Asset Browser web page loaded")
        self._inject_python_bridge()
        self._populate_assets()
        
    def _inject_python_bridge(self):
        """Inject Python bridge for communication."""
        bridge_script = f"""
        // Python bridge for asset browser
        window.pythonBridge = {{
            // Asset selection
            assetSelected: function(assetName, assetType) {{
                console.log('DEBUG: Asset selected:', assetName, 'Type:', assetType);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'asset_selected',
                    data: {{ name: assetName, type: assetType }}
                }}));
            }},
            
            // Category change
            categoryChanged: function(categoryName) {{
                console.log('DEBUG: Category changed to:', categoryName);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'category_changed',
                    data: categoryName
                }}));
            }},
            
            // Import request
            importAsset: function() {{
                console.log('DEBUG: Import asset requested');
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'import_requested',
                    data: null
                }}));
            }}
        }};
        
        console.log('DEBUG: Python bridge injected successfully');
        """
        
        self.web_view.page().runJavaScript(bridge_script)
        
    def _populate_assets(self):
        """Populate the asset browser with assets from the asset manager."""
        # Get assets from asset manager
        assets = self._get_assets_from_manager()
        
        # Update the web interface
        script = f"""
        if (window.assetBrowser) {{
            // Update asset data
            window.assetBrowser.assets = {assets};
            window.assetBrowser.refreshAssets();
            console.log('DEBUG: Assets populated from Python');
        }}
        """
        
        self.web_view.page().runJavaScript(script)
        
    def _get_assets_from_manager(self) -> str:
        """Get assets from asset manager and format for JavaScript."""
        # This is a placeholder - in a real implementation, you'd get actual assets
        # from the asset manager
        import json
        
        sample_assets = {
            "scripts": [
                {"name": "PlayerController.cs", "icon": "code", "type": "script"},
                {"name": "GameManager.cs", "icon": "code", "type": "script"},
                {"name": "UIController.cs", "icon": "code", "type": "script"},
                {"name": "AudioManager.cs", "icon": "code", "type": "script"}
            ],
            "textures": [
                {"name": "player_diffuse.png", "icon": "image", "type": "texture"},
                {"name": "ground_texture.jpg", "icon": "image", "type": "texture"},
                {"name": "ui_background.png", "icon": "image", "type": "texture"},
                {"name": "particle_glow.png", "icon": "image", "type": "texture"}
            ],
            "audio": [
                {"name": "background_music.mp3", "icon": "audio", "type": "audio"},
                {"name": "jump_sound.wav", "icon": "audio", "type": "audio"},
                {"name": "collect_item.wav", "icon": "audio", "type": "audio"},
                {"name": "menu_click.wav", "icon": "audio", "type": "audio"}
            ],
            "models": [
                {"name": "player_model.fbx", "icon": "model", "type": "model"},
                {"name": "environment_props.fbx", "icon": "model", "type": "model"},
                {"name": "weapon_sword.obj", "icon": "model", "type": "model"},
                {"name": "building_house.fbx", "icon": "model", "type": "model"}
            ],
            "prefabs": [
                {"name": "Player.prefab", "icon": "prefab", "type": "prefab"},
                {"name": "Enemy.prefab", "icon": "prefab", "type": "prefab"},
                {"name": "Collectible.prefab", "icon": "prefab", "type": "prefab"},
                {"name": "UI_Panel.prefab", "icon": "prefab", "type": "prefab"}
            ]
        }
        
        return json.dumps(sample_assets)
        
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
    def setCategory(self, category_name: str):
        """Set the current asset category."""
        self._current_category = category_name
        self.category_changed.emit(category_name)
        
        # Update web interface
        script = f"if (window.assetBrowser) {{ window.assetBrowser.setCategory('{category_name}'); }}"
        self.web_view.page().runJavaScript(script)
        
    def getCurrentCategory(self) -> str:
        """Get the currently active category."""
        return self._current_category
        
    def selectAsset(self, asset_name: str, asset_type: str):
        """Select an asset."""
        self._selected_asset = asset_name
        self.asset_selected.emit(asset_name, asset_type)
        
    def getSelectedAsset(self) -> Optional[str]:
        """Get the currently selected asset."""
        return self._selected_asset
        
    def searchAssets(self, search_term: str):
        """Search for assets."""
        self._search_term = search_term
        
        # Update web interface
        script = f"""
        if (window.assetBrowser) {{
            const searchInput = document.querySelector('.search-input');
            if (searchInput) {{
                searchInput.value = '{search_term}';
                searchInput.dispatchEvent(new Event('input'));
            }}
        }}
        """
        
        self.web_view.page().runJavaScript(script)
        
    def refreshAssets(self):
        """Refresh the asset browser."""
        self._populate_assets()
        
    def addAsset(self, category: str, asset_data: Dict[str, Any]):
        """Add a new asset to the browser."""
        # Update web interface
        script = f"""
        if (window.assetBrowser) {{
            window.assetBrowser.addAsset('{category}', {asset_data});
        }}
        """
        
        self.web_view.page().runJavaScript(script)
        
    def removeAsset(self, category: str, asset_name: str):
        """Remove an asset from the browser."""
        # Update web interface
        script = f"""
        if (window.assetBrowser) {{
            window.assetBrowser.removeAsset('{category}', '{asset_name}');
        }}
        """
        
        self.web_view.page().runJavaScript(script)
