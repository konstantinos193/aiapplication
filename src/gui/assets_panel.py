"""
Assets Panel for Nexlify Engine.

This module provides an asset exploration and management interface
similar to Unity's Project window, with collapsible functionality.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QLineEdit, QComboBox, QSplitter, QFrame,
    QHeaderView, QMenu, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPixmap, QAction

from ..utils.logger import get_logger


class AssetsPanel(QWidget):
    """Collapsible panel for exploring and managing project assets."""
    
    # Signals
    asset_selected = pyqtSignal(str)  # Emits asset path when selected
    asset_double_clicked = pyqtSignal(str)  # Emits asset path when double-clicked
    
    def __init__(self, main_window):
        """Initialize the assets panel.
        
        Args:
            main_window: Reference to the main window
        """
        super().__init__()
        self.main_window = main_window
        self.game_engine = main_window.game_engine
        self.logger = get_logger(__name__)
        
        self.is_collapsed = False
        self._init_ui()
        self.logger.info("Assets panel initialized")
    
    def _init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Header with collapse button
        header_layout = QHBoxLayout()
        
        # Collapse button
        self.collapse_btn = QPushButton("▼")
        self.collapse_btn.setToolTip("Collapse/Expand Assets Panel")
        self.collapse_btn.setMaximumWidth(20)
        self.collapse_btn.clicked.connect(self._toggle_collapse)
        self.collapse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 3px;
                padding: 2px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """)
        header_layout.addWidget(self.collapse_btn)
        
        # Title
        title_label = QLabel("Assets")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search assets...")
        self.search_box.setMaximumWidth(200)
        self.search_box.textChanged.connect(self._filter_assets)
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #fafafa;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border-color: #ff6b35;
                background-color: #262626;
            }
            QLineEdit:hover {
                border-color: #ff8c42;
                background-color: #262626;
            }
            QLineEdit::placeholder {
                color: #a3a3a3;
            }
        """)
        header_layout.addWidget(self.search_box)
        
        # View mode selector
        self.view_mode_combo = QComboBox()
        self.view_mode_combo.addItems(["List", "Grid", "Details"])
        self.view_mode_combo.setMaximumWidth(80)
        self.view_mode_combo.currentTextChanged.connect(self._change_view_mode)
        self.view_mode_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 3px;
                font-size: 11px;
            }
        """)
        header_layout.addWidget(self.view_mode_combo)
        
        main_layout.addLayout(header_layout)
        
        # Assets tree widget
        self.assets_tree = QTreeWidget()
        self.assets_tree.setHeaderLabels(["Name", "Type", "Size", "Modified"])
        self.assets_tree.setAlternatingRowColors(True)
        self.assets_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.assets_tree.customContextMenuRequested.connect(self._show_context_menu)
        self.assets_tree.itemDoubleClicked.connect(self._on_asset_double_clicked)
        self.assets_tree.itemSelectionChanged.connect(self._on_asset_selected)
        
        # Style the tree widget
        self.assets_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2d2d30;
                color: #ffffff;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                font-size: 11px;
            }
            QTreeWidget::item {
                padding: 2px;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
            }
            QTreeWidget::item:hover {
                background-color: #3e3e42;
            }
            QHeaderView::section {
                background-color: #3e3e42;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #5a5a5a;
                font-weight: bold;
            }
        """)
        
        # Set column widths
        header = self.assets_tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Name column
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Size
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Modified
        
        main_layout.addWidget(self.assets_tree)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.asset_count_label = QLabel("Assets: 0")
        self.asset_count_label.setStyleSheet("color: #cccccc; font-size: 10px;")
        status_layout.addWidget(self.asset_count_label)
        
        status_layout.addStretch()
        
        self.current_path_label = QLabel("Path: /")
        self.current_path_label.setStyleSheet("color: #cccccc; font-size: 10px;")
        status_layout.addWidget(self.current_path_label)
        
        main_layout.addLayout(status_layout)
        
        # Populate with sample assets
        self._populate_sample_assets()
    
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
        self.assets_tree.hide()
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.logger.info("Assets panel collapsed")
    
    def expand(self):
        """Expand the panel to show all content."""
        self.is_collapsed = False
        self.collapse_btn.setText("▼")
        self.assets_tree.show()
        self.setMaximumHeight(200)
        self.setMinimumHeight(100)
        self.logger.info("Assets panel expanded")
    
    def _populate_sample_assets(self):
        """Populate the assets tree with sample assets for demonstration."""
        # Clear existing items
        self.assets_tree.clear()
        
        # Create root items for different asset types
        models_item = QTreeWidgetItem(self.assets_tree, ["3D Models", "Folder", "", ""])
        models_item.setIcon(0, self._get_folder_icon())
        
        textures_item = QTreeWidgetItem(self.assets_tree, ["Textures", "Folder", "", ""])
        textures_item.setIcon(0, self._get_folder_icon())
        
        materials_item = QTreeWidgetItem(self.assets_tree, ["Materials", "Folder", "", ""])
        materials_item.setIcon(0, self._get_folder_icon())
        
        scripts_item = QTreeWidgetItem(self.assets_tree, ["Scripts", "Folder", "", ""])
        scripts_item.setIcon(0, self._get_folder_icon())
        
        audio_item = QTreeWidgetItem(self.assets_tree, ["Audio", "Folder", "", ""])
        audio_item.setIcon(0, self._get_folder_icon())
        
        # Add sample assets to 3D Models
        cube_item = QTreeWidgetItem(models_item, ["Cube.obj", "3D Model", "2.3 KB", "2025-08-30"])
        cube_item.setIcon(0, self._get_model_icon())
        
        sphere_item = QTreeWidgetItem(models_item, ["Sphere.obj", "3D Model", "1.8 KB", "2025-08-30"])
        sphere_item.setIcon(0, self._get_model_icon())
        
        # Add sample assets to Textures
        grass_tex = QTreeWidgetItem(textures_item, ["grass_diffuse.png", "Texture", "512 KB", "2025-08-30"])
        grass_tex.setIcon(0, self._get_texture_icon())
        
        stone_tex = QTreeWidgetItem(textures_item, ["stone_normal.png", "Texture", "256 KB", "2025-08-30"])
        stone_tex.setIcon(0, self._get_texture_icon())
        
        # Add sample assets to Materials
        grass_mat = QTreeWidgetItem(materials_item, ["GrassMaterial.mat", "Material", "1.2 KB", "2025-08-30"])
        grass_mat.setIcon(0, self._get_material_icon())
        
        stone_mat = QTreeWidgetItem(materials_item, ["StoneMaterial.mat", "Material", "1.1 KB", "2025-08-30"])
        stone_mat.setIcon(0, self._get_material_icon())
        
        # Add sample assets to Scripts
        player_script = QTreeWidgetItem(scripts_item, ["PlayerController.py", "Script", "3.4 KB", "2025-08-30"])
        player_script.setIcon(0, self._get_script_icon())
        
        game_manager = QTreeWidgetItem(scripts_item, ["GameManager.py", "Script", "2.1 KB", "2025-08-30"])
        game_manager.setIcon(0, self._get_script_icon())
        
        # Expand all items
        self.assets_tree.expandAll()
        
        # Update asset count
        self._update_asset_count()
    
    def _get_folder_icon(self):
        """Get a folder icon for tree items."""
        # In a real implementation, you'd load actual icons
        # For now, return an empty pixmap
        return QIcon()
    
    def _get_model_icon(self):
        """Get a 3D model icon for tree items."""
        return QIcon()
    
    def _get_texture_icon(self):
        """Get a texture icon for tree items."""
        return QIcon()
    
    def _get_material_icon(self):
        """Get a material icon for tree items."""
        return QIcon()
    
    def _get_script_icon(self):
        """Get a script icon for tree items."""
        return QIcon()
    
    def _filter_assets(self, search_text):
        """Filter assets based on search text."""
        # In a real implementation, this would filter the tree items
        self.logger.info(f"Filtering assets with: {search_text}")
    
    def _change_view_mode(self, mode):
        """Change the view mode of the assets panel."""
        self.logger.info(f"Changed view mode to: {mode}")
        # In a real implementation, this would change the display format
    
    def _show_context_menu(self, position):
        """Show the context menu for assets."""
        item = self.assets_tree.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        # Add context menu actions
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self._open_asset(item))
        menu.addAction(open_action)
        
        if item.text(1) == "Folder":
            new_asset_action = QAction("Create New Asset", self)
            new_asset_action.triggered.connect(lambda: self._create_new_asset(item))
            menu.addAction(new_asset_action)
        
        menu.addSeparator()
        
        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self._rename_asset(item))
        menu.addAction(rename_action)
        
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._delete_asset(item))
        menu.addAction(delete_action)
        
        menu.exec(self.assets_tree.mapToGlobal(position))
    
    def _open_asset(self, item):
        """Open the selected asset."""
        asset_name = item.text(0)
        asset_type = item.text(1)
        self.logger.info(f"Opening asset: {asset_name} ({asset_type})")
        self.asset_double_clicked.emit(asset_name)
    
    def _create_new_asset(self, folder_item):
        """Create a new asset in the selected folder."""
        folder_name = folder_item.text(0)
        self.logger.info(f"Creating new asset in folder: {folder_name}")
        # In a real implementation, this would show a dialog to create new assets
    
    def _rename_asset(self, item):
        """Rename the selected asset."""
        asset_name = item.text(0)
        self.logger.info(f"Renaming asset: {asset_name}")
        # In a real implementation, this would allow inline editing
    
    def _delete_asset(self, item):
        """Delete the selected asset."""
        asset_name = item.text(0)
        reply = QMessageBox.question(
            self, "Delete Asset",
            f"Are you sure you want to delete '{asset_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logger.info(f"Deleting asset: {asset_name}")
            # In a real implementation, this would remove the item and delete the file
    
    def _on_asset_selected(self):
        """Handle when an asset is selected."""
        current_item = self.assets_tree.currentItem()
        if current_item:
            asset_name = current_item.text(0)
            self.asset_selected.emit(asset_name)
            self.current_path_label.setText(f"Path: /{asset_name}")
    
    def _on_asset_double_clicked(self, item, column):
        """Handle when an asset is double-clicked."""
        asset_name = item.text(0)
        self.asset_double_clicked.emit(asset_name)
        self.logger.info(f"Asset double-clicked: {asset_name}")
    
    def _update_asset_count(self):
        """Update the asset count display."""
        # Count all items (excluding folders)
        count = 0
        for i in range(self.assets_tree.topLevelItemCount()):
            top_item = self.assets_tree.topLevelItem(i)
            count += self._count_assets_recursive(top_item)
        
        self.asset_count_label.setText(f"Assets: {count}")
    
    def _count_assets_recursive(self, item):
        """Recursively count assets in a tree item."""
        count = 0
        if item.text(1) != "Folder":
            count += 1
        
        for i in range(item.childCount()):
            count += self._count_assets_recursive(item.child(i))
        
        return count
    
    def refresh(self):
        """Refresh the assets panel."""
        self._populate_sample_assets()
        self.logger.info("Assets panel refreshed")
