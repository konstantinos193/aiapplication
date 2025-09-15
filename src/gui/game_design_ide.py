#!/usr/bin/env python3
"""
Game Design IDE - Main Container for Nexlify Engine.

This is the main layout that replaces the old main window,
implementing the complete React IDE design with 100% visual fidelity.
"""

from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QApplication, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

from .design_system.react_theme_system import react_theme
from .ide_header_web_working import IDEHeader
from .ide_left_panel import IDELeftPanel
from .ide_center_panel import IDECenterPanel
from .ide_ai_assistant import IDEAIAssistant
from .ide_status_bar import IDEStatusBar


class GameDesignIDE(QMainWindow):
    """
    Main Game Design IDE window that replicates the React layout exactly.
    
    Features:
    - Header with play controls and transform tools
    - Left panel: Scene hierarchy + inspector
    - Center panel: 3D viewport + tabs
    - Right panel: AI chat assistant
    - Bottom: Assets browser + status bar
    - 100% visual fidelity with React components
    """
    
    # Signals
    scene_changed = pyqtSignal(str)
    object_selected = pyqtSignal(str)
    play_state_changed = pyqtSignal(bool)
    
    def __init__(self, game_engine, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Store game engine reference
        self.game_engine = game_engine
        
        # State
        self._is_playing = False
        self._selected_object = "Player"
        self._active_tab = "MainScene"
        
        # Setup UI
        self._setup_ui()
        self._setup_connections()
        self._setup_theme()
        
        # Set window properties
        self.setWindowTitle("Game Design IDE - Nexlify Engine")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Ensure proper sizing
        self.setMinimumSize(1200, 800)
        
    def resizeEvent(self, event):
        """Handle window resize events to ensure proper layout."""
        super().resizeEvent(event)
        print(f"DEBUG: Main window resized to: {event.size().width()}x{event.size().height()}")
        # Force layout update
        self.centralWidget().updateGeometry()
        
    def _setup_ui(self):
        """Setup the main user interface."""
        # Central widget
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        self.header = IDEHeader(self)
        self.header.setFixedHeight(60)  # Fixed height for header
        main_layout.addWidget(self.header)
        
        # Main content splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter, 1)  # Give stretch factor 1 to the splitter
        
        # Ensure the splitter expands to fill all available space
        main_splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Debug: Print central widget size policy
        print(f"DEBUG: Central widget size policy: {central_widget.sizePolicy().horizontalPolicy()}, {central_widget.sizePolicy().verticalPolicy()}")
        print(f"DEBUG: Main splitter size policy: {main_splitter.sizePolicy().horizontalPolicy()}, {main_splitter.sizePolicy().verticalPolicy()}")
        
        # Left panel (Scene + Inspector)
        self.left_panel = IDELeftPanel(self)
        if hasattr(self.left_panel, 'set_game_engine'):
            self.left_panel.set_game_engine(self.game_engine)
        main_splitter.addWidget(self.left_panel)
        
        # Center panel (Viewport + Assets)
        self.center_panel = IDECenterPanel(self)
        main_splitter.addWidget(self.center_panel)
        
        # Right panel (AI Chat) - Make it extend to bottom
        self.right_panel = IDEAIAssistant(self)
        self.right_panel.setMinimumWidth(350)  # Ensure minimum width
        main_splitter.addWidget(self.right_panel)
        
        # Set splitter sizes - give more space to center panel
        main_splitter.setSizes([300, 900, 400])
        
        # Ensure AI chat panel stretches to fill available vertical space
        # Use setStretchFactor to make the right panel expand more
        main_splitter.setStretchFactor(0, 0)  # Left panel - no stretch
        main_splitter.setStretchFactor(1, 1)  # Center panel - stretch
        main_splitter.setStretchFactor(2, 2)  # Right panel - stretch more
        
        # Debug: Print splitter information
        print(f"DEBUG: Main splitter has {main_splitter.count()} widgets")
        print(f"DEBUG: Splitter sizes: {main_splitter.sizes()}")
        # Note: stretchFactor method may not exist in PyQt6, using sizes instead
        
        # Force layout update
        main_splitter.updateGeometry()
        
        # Style the main splitter
        main_splitter.setHandleWidth(4)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 2px;
            }
            QSplitter::handle:hover {
                background: rgba(255, 140, 66, 0.3);
            }
        """)
        
        # Status bar
        self.status_bar = IDEStatusBar(self)
        self.status_bar.setFixedHeight(30)  # Fixed height for status bar
        main_layout.addWidget(self.status_bar)
        
    def _setup_connections(self):
        """Setup signal connections."""
        # Header connections
        self.header.play_state_changed.connect(self._on_play_state_changed)
        
        # Left panel connections
        self.left_panel.object_selected.connect(self._on_object_selected)
        
        # Center panel connections
        self.center_panel.tab_changed.connect(self._on_tab_changed)
        
        # Asset browser connections
        if hasattr(self.center_panel, 'asset_browser'):
            self.center_panel.asset_browser.asset_selected.connect(self._on_asset_selected)
            self.center_panel.asset_browser.category_changed.connect(self._on_asset_category_changed)
            self.center_panel.asset_browser.import_requested.connect(self._on_asset_import_requested)
        
    def _setup_theme(self):
        """Setup enhanced theme with sophisticated styling."""
        # Set enhanced dark theme by default
        from .design_system.react_theme_system import ThemeMode
        react_theme.switch_theme(ThemeMode.DARK)
        
        # Apply sophisticated main window styling
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 {react_theme.get_color("background")},
                                          stop:1 {react_theme.get_color("card")});
                color: {react_theme.get_color("foreground")};
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            
            QSplitter::handle {{
                background: {react_theme.get_color("border")};
                border-radius: 2px;
                margin: 1px;
            }}
            
            QSplitter::handle:hover {{
                background: {react_theme.get_color("accent")};
            }}
            
            QStatusBar {{
                background: {react_theme.get_color("card")};
                border-top: 1px solid {react_theme.get_color("border")};
                color: {react_theme.get_color("foreground")};
            }}
            
            QMenuBar {{
                background: {react_theme.get_color("card")};
                border-bottom: 1px solid {react_theme.get_color("border")};
                color: {react_theme.get_color("foreground")};
            }}
            
            QMenuBar::item {{
                background: transparent;
                padding: 8px 12px;
                border-radius: 6px;
            }}
            
            QMenuBar::item:selected {{
                background: {react_theme.get_color("muted")};
            }}
            
            QMenu {{
                background: {react_theme.get_color("card")};
                border: 1px solid {react_theme.get_color("border")};
                border-radius: 8px;
                padding: 4px;
                color: {react_theme.get_color("foreground")};
            }}
            
            QMenu::item {{
                padding: 8px 16px;
                border-radius: 4px;
            }}
            
            QMenu::item:selected {{
                background: {react_theme.get_color("muted")};
            }}
        """)
        
    def _on_theme_changed(self):
        """Handle theme changes."""
        self._apply_theme()
        
    def _on_play_state_changed(self, is_playing: bool):
        """Handle play state changes."""
        self._is_playing = is_playing
        self.play_state_changed.emit(is_playing)
        
    def _on_object_selected(self, object_name: str):
        """Handle object selection."""
        self._selected_object = object_name
        self.object_selected.emit(object_name)
        
    def _on_tab_changed(self, tab_name: str):
        """Handle tab changes."""
        self._active_tab = tab_name
        self.scene_changed.emit(tab_name)
        
    def _on_asset_selected(self, asset_name: str, asset_type: str):
        """Handle asset selection."""
        print(f"Asset selected: {asset_name} ({asset_type})")
        # TODO: Implement asset selection logic
        
    def _on_asset_category_changed(self, category_name: str):
        """Handle asset category changes."""
        print(f"Asset category changed to: {category_name}")
        # TODO: Implement category change logic
        
    def _on_asset_import_requested(self):
        """Handle asset import requests."""
        print("Asset import requested")
        # TODO: Implement asset import dialog
        
    # Public API methods
    def setPlayState(self, is_playing: bool):
        """Set the play state."""
        self._is_playing = is_playing
        self.header.setPlayState(is_playing)
        
    def getPlayState(self) -> bool:
        """Get the current play state."""
        return self._is_playing
        
    def setSelectedObject(self, object_name: str):
        """Set the selected object."""
        self._selected_object = object_name
        self.left_panel.setSelectedObject(object_name)
        
    def getSelectedObject(self) -> str:
        """Get the currently selected object."""
        return self._selected_object
        
    def setActiveTab(self, tab_name: str):
        """Set the active tab."""
        self._active_tab = tab_name
        self.center_panel.setActiveTab(tab_name)
        
    def getActiveTab(self) -> str:
        """Get the currently active tab."""
        return self._active_tab
        
    # Asset Browser API methods
    def setAssetCategory(self, category: str):
        """Set the asset browser category."""
        if hasattr(self.center_panel, 'asset_browser'):
            self.center_panel.setAssetCategory(category)
            
    def selectAsset(self, asset_name: str, asset_type: str):
        """Select an asset in the asset browser."""
        if hasattr(self.center_panel, 'asset_browser'):
            self.center_panel.selectAsset(asset_name, asset_type)
            
    def searchAssets(self, search_term: str):
        """Search for assets in the asset browser."""
        if hasattr(self.center_panel, 'searchAssets'):
            self.center_panel.searchAssets(search_term)
            
    def refreshAssets(self):
        """Refresh the asset browser."""
        if hasattr(self.center_panel, 'refreshAssets'):
            self.center_panel.refreshAssets()


# Main entry point for testing
if __name__ == "__main__":
    import sys
    import os
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    
    from PyQt6.QtWidgets import QApplication
    from .design_system.react_theme_system import react_theme
    
    app = QApplication(sys.argv)
    
    # Create and show IDE
    ide = GameDesignIDE()
    ide.show()
    
    # Run app
    sys.exit(app.exec())
