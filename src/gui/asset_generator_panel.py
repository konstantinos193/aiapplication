"""
Asset Generator Panel for Nexlify Engine.

This module provides AI-powered asset generation for:
- 3D models (.obj files)
- Textures (.png files)
- Materials and shaders
- Audio files
- Procedural generation
"""

import os
import json
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QComboBox, QSpinBox, 
    QCheckBox, QGroupBox, QScrollArea, QSplitter, QFrame,
    QProgressBar, QFileDialog, QMessageBox, QListWidget,
    QListWidgetItem, QSlider, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPainter, QColor

from ..utils.logger import get_logger


class AssetGeneratorPanel(QWidget):
    """Asset Generator panel with AI-powered asset creation."""
    
    # Signals
    asset_created = pyqtSignal(str, str)  # asset_type, file_path
    generation_progress = pyqtSignal(int)  # progress percentage
    generation_complete = pyqtSignal(str, str)  # asset_type, file_path
    
    def __init__(self, game_engine):
        """Initialize the Asset Generator panel.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        # Asset generation state
        self.generating = False
        self.current_asset_type = ""
        self.generated_assets = []
        
        self._init_ui()
        self.logger.info("✅ Asset Generator panel initialized")
    
    def _init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header
        header = QLabel("Asset Generator")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d30, stop:1 #1e1e1e);
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #3e3e42;
            }
        """)
        main_layout.addWidget(header)
        
        # Create tabbed interface
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3e3e42;
                border-radius: 8px;
                background-color: #2d2d30;
            }
            QTabBar::tab {
                background-color: #3e3e42;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
            QTabBar::tab:hover {
                background-color: #5a5a5a;
            }
        """)
        
        # Add tabs
        self._create_3d_model_tab()
        self._create_texture_tab()
        self._create_material_tab()
        self._create_audio_tab()
        self._create_procedural_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3e3e42;
                border-radius: 4px;
                text-align: center;
                background-color: #2d2d30;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                border-radius: 3px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Status and actions
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready to generate assets")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #4ec9b0;
                font-style: italic;
                padding: 8px;
                background-color: #2d2d30;
                border-radius: 4px;
                border: 1px solid #3e3e42;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        # View generated assets button
        view_assets_btn = QPushButton("📁 View Assets")
        view_assets_btn.setStyleSheet("""
            QPushButton {
                background-color: #5a5a5a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
        """)
        view_assets_btn.clicked.connect(self._view_generated_assets)
        status_layout.addWidget(view_assets_btn)
        
        status_layout.addStretch()
        main_layout.addLayout(status_layout)
    
    def _create_3d_model_tab(self):
        """Create the 3D model generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Model type selection
        type_group = QGroupBox("Model Type")
        type_layout = QHBoxLayout(type_group)
        
        self.model_type_combo = QComboBox()
        self.model_type_combo.addItems([
            "Character", "Vehicle", "Building", "Prop", "Environment", "Weapon", "Custom"
        ])
        self.model_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
        """)
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.model_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Model parameters
        params_group = QGroupBox("Model Parameters")
        params_layout = QVBoxLayout(params_group)
        
        # Complexity and detail
        detail_layout = QHBoxLayout()
        detail_layout.addWidget(QLabel("Detail Level:"))
        self.detail_slider = QSlider(Qt.Orientation.Horizontal)
        self.detail_slider.setRange(1, 10)
        self.detail_slider.setValue(5)
        self.detail_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #5a5a5a;
                height: 8px;
                background: #3e3e42;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #0078d4;
                border: 1px solid #0078d4;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        detail_layout.addWidget(self.detail_slider)
        
        self.detail_label = QLabel("5")
        self.detail_label.setStyleSheet("color: #ffffff; min-width: 30px;")
        self.detail_slider.valueChanged.connect(lambda v: self.detail_label.setText(str(v)))
        detail_layout.addWidget(self.detail_label)
        detail_layout.addStretch()
        
        params_layout.addLayout(detail_layout)
        
        # Polygon count
        poly_layout = QHBoxLayout()
        poly_layout.addWidget(QLabel("Max Polygons:"))
        self.poly_spin = QSpinBox()
        self.poly_spin.setRange(100, 100000)
        self.poly_spin.setValue(5000)
        self.poly_spin.setSuffix("k")
        self.poly_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        poly_layout.addWidget(self.poly_spin)
        poly_layout.addStretch()
        
        params_layout.addLayout(poly_layout)
        
        # Export format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems([".obj", ".fbx", ".dae", ".3ds"])
        self.format_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        
        params_layout.addLayout(format_layout)
        layout.addWidget(params_group)
        
        # Model description
        desc_group = QGroupBox("Model Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.model_description = QTextEdit()
        self.model_description.setPlaceholderText("Describe the 3D model you want to generate...\n\nExamples:\n- 'A futuristic robot with glowing blue eyes'\n- 'A medieval sword with ornate handle'\n- 'A realistic tree with autumn leaves'")
        self.model_description.setMaximumHeight(100)
        self.model_description.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        desc_layout.addWidget(self.model_description)
        
        layout.addWidget(desc_group)
        
        # Generate button
        generate_btn = QPushButton("Generate 3D Model")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
        """)
        generate_btn.clicked.connect(lambda: self._generate_asset("3d_model"))
        layout.addWidget(generate_btn)
        
        self.tab_widget.addTab(tab, "🗿 3D Models")
    
    def _create_texture_tab(self):
        """Create the texture generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Texture type
        type_group = QGroupBox("Texture Type")
        type_layout = QHBoxLayout(type_group)
        
        self.texture_type_combo = QComboBox()
        self.texture_type_combo.addItems([
            "Diffuse", "Normal", "Specular", "Roughness", "Metallic", "Height", "Custom"
        ])
        self.texture_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
        """)
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.texture_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Texture parameters
        params_group = QGroupBox("Texture Parameters")
        params_layout = QVBoxLayout(params_group)
        
        # Size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.texture_width = QSpinBox()
        self.texture_width.setRange(16, 4096)
        self.texture_width.setValue(1024)
        self.texture_width.setSuffix("x")
        self.texture_width.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        size_layout.addWidget(self.texture_width)
        
        self.texture_height = QSpinBox()
        self.texture_height.setRange(16, 4096)
        self.texture_height.setValue(1024)
        self.texture_height.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        size_layout.addWidget(self.texture_height)
        size_layout.addStretch()
        
        params_layout.addLayout(size_layout)
        
        # Quality and style
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Quality:"))
        self.texture_quality = QComboBox()
        self.texture_quality.addItems(["Low", "Medium", "High", "Ultra"])
        self.texture_quality.setCurrentText("High")
        self.texture_quality.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }
        """)
        quality_layout.addWidget(self.texture_quality)
        quality_layout.addStretch()
        
        params_layout.addLayout(quality_layout)
        layout.addWidget(params_group)
        
        # Texture description
        desc_group = QGroupBox("Texture Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.texture_description = QTextEdit()
        self.texture_description.setPlaceholderText("Describe the texture you want to generate...\n\nExamples:\n- 'Rusty metal surface with scratches'\n- 'Smooth marble with subtle veins'\n- 'Rough concrete with cracks'")
        self.texture_description.setMaximumHeight(100)
        self.texture_description.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        desc_layout.addWidget(self.texture_description)
        
        layout.addWidget(desc_group)
        
        # Generate button
        generate_btn = QPushButton("Generate Texture")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
        """)
        generate_btn.clicked.connect(lambda: self._generate_asset("texture"))
        layout.addWidget(generate_btn)
        
        self.tab_widget.addTab(tab, "🖼️ Textures")
    
    def _create_material_tab(self):
        """Create the material generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Material type
        type_group = QGroupBox("Material Type")
        type_layout = QHBoxLayout(type_group)
        
        self.material_type_combo = QComboBox()
        self.material_type_combo.addItems([
            "PBR", "Unlit", "Transparent", "Emissive", "Custom Shader"
        ])
        self.material_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
        """)
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.material_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Material properties
        props_group = QGroupBox("Material Properties")
        props_layout = QVBoxLayout(props_group)
        
        # Base color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Base Color:"))
        self.base_color_btn = QPushButton("Select Color")
        self.base_color_btn.setStyleSheet("""
            QPushButton {
                background-color: #5a5a5a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
        """)
        color_layout.addWidget(self.base_color_btn)
        color_layout.addStretch()
        
        props_layout.addLayout(color_layout)
        
        # Metallic and roughness
        mr_layout = QHBoxLayout()
        mr_layout.addWidget(QLabel("Metallic:"))
        self.metallic_spin = QDoubleSpinBox()
        self.metallic_spin.setRange(0.0, 1.0)
        self.metallic_spin.setValue(0.0)
        self.metallic_spin.setSingleStep(0.1)
        self.metallic_spin.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        mr_layout.addWidget(self.metallic_spin)
        
        mr_layout.addWidget(QLabel("Roughness:"))
        self.roughness_spin = QDoubleSpinBox()
        self.roughness_spin.setRange(0.0, 1.0)
        self.roughness_spin.setValue(0.5)
        self.roughness_spin.setSingleStep(0.1)
        self.roughness_spin.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        mr_layout.addWidget(self.roughness_spin)
        mr_layout.addStretch()
        
        props_layout.addLayout(mr_layout)
        layout.addWidget(props_group)
        
        # Material description
        desc_group = QGroupBox("Material Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.material_description = QTextEdit()
        self.material_description.setPlaceholderText("Describe the material you want to generate...\n\nExamples:\n- 'Shiny chrome metal surface'\n- 'Rough stone with moss'\n- 'Translucent glass with refraction'")
        self.material_description.setMaximumHeight(100)
        self.material_description.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        desc_layout.addWidget(self.material_description)
        
        layout.addWidget(desc_group)
        
        # Generate button
        generate_btn = QPushButton("✨ Generate Material")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
        """)
        generate_btn.clicked.connect(lambda: self._generate_asset("material"))
        layout.addWidget(generate_btn)
        
        self.tab_widget.addTab(tab, "✨ Materials")
    
    def _create_audio_tab(self):
        """Create the audio generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Audio type
        type_group = QGroupBox("Audio Type")
        type_layout = QHBoxLayout(type_group)
        
        self.audio_type_combo = QComboBox()
        self.audio_type_combo.addItems([
            "Music", "Sound Effect", "Ambient", "Voice", "Custom"
        ])
        self.audio_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
        """)
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.audio_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Audio parameters
        params_group = QGroupBox("Audio Parameters")
        params_layout = QVBoxLayout(params_group)
        
        # Duration and format
        audio_layout = QHBoxLayout()
        audio_layout.addWidget(QLabel("Duration:"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 300)
        self.duration_spin.setValue(10)
        self.duration_spin.setSuffix("s")
        self.duration_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        audio_layout.addWidget(self.duration_spin)
        
        audio_layout.addWidget(QLabel("Format:"))
        self.audio_format = QComboBox()
        self.audio_format.addItems([".wav", ".mp3", ".ogg"])
        self.audio_format.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        audio_layout.addWidget(self.audio_format)
        audio_layout.addStretch()
        
        params_layout.addLayout(audio_layout)
        layout.addWidget(params_group)
        
        # Audio description
        desc_group = QGroupBox("Audio Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.audio_description = QTextEdit()
        self.audio_description.setPlaceholderText("Describe the audio you want to generate...\n\nExamples:\n- 'Epic orchestral battle music'\n- 'Footsteps on wooden floor'\n- 'Wind through trees with bird sounds'")
        self.audio_description.setMaximumHeight(100)
        self.audio_description.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        desc_layout.addWidget(self.audio_description)
        
        layout.addWidget(desc_group)
        
        # Generate button
        generate_btn = QPushButton("Generate Audio")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
        """)
        generate_btn.clicked.connect(lambda: self._generate_asset("audio"))
        layout.addWidget(generate_btn)
        
        self.tab_widget.addTab(tab, "Audio")
    
    def _create_procedural_tab(self):
        """Create the procedural generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Procedural type
        type_group = QGroupBox("Procedural Type")
        type_layout = QHBoxLayout(type_group)
        
        self.procedural_type_combo = QComboBox()
        self.procedural_type_combo.addItems([
            "Terrain", "Vegetation", "Buildings", "Roads", "Particles", "Custom"
        ])
        self.procedural_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
        """)
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.procedural_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Procedural parameters
        params_group = QGroupBox("Generation Parameters")
        params_layout = QVBoxLayout(params_group)
        
        # Size and complexity
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.procedural_size = QSpinBox()
        self.procedural_size.setRange(100, 10000)
        self.procedural_size.setValue(1000)
        self.procedural_size.setSuffix("x")
        self.procedural_size.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        size_layout.addWidget(self.procedural_size)
        
        self.procedural_size_y = QSpinBox()
        self.procedural_size_y.setRange(100, 10000)
        self.procedural_size_y.setValue(1000)
        self.procedural_size_y.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        size_layout.addWidget(self.procedural_size_y)
        size_layout.addStretch()
        
        params_layout.addLayout(size_layout)
        
        # Seed and variation
        seed_layout = QHBoxLayout()
        seed_layout.addWidget(QLabel("Seed:"))
        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(0, 999999)
        self.seed_spin.setValue(12345)
        self.seed_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        seed_layout.addWidget(self.seed_spin)
        
        seed_layout.addWidget(QLabel("Variation:"))
        self.variation_spin = QDoubleSpinBox()
        self.variation_spin.setRange(0.0, 1.0)
        self.variation_spin.setValue(0.5)
        self.variation_spin.setSingleStep(0.1)
        self.variation_spin.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        seed_layout.addWidget(self.variation_spin)
        seed_layout.addStretch()
        
        params_layout.addLayout(seed_layout)
        layout.addWidget(params_group)
        
        # Procedural description
        desc_group = QGroupBox("Generation Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.procedural_description = QTextEdit()
        self.procedural_description.setPlaceholderText("Describe the procedural content you want to generate...\n\nExamples:\n- 'Mountainous terrain with rivers and forests'\n- 'City grid with skyscrapers and parks'\n- 'Organic cave system with stalactites'")
        self.procedural_description.setMaximumHeight(100)
        self.procedural_description.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        desc_layout.addWidget(self.procedural_description)
        
        layout.addWidget(desc_group)
        
        # Generate button
        generate_btn = QPushButton("🌍 Generate Procedural")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
        """)
        generate_btn.clicked.connect(lambda: self._generate_asset("procedural"))
        layout.addWidget(generate_btn)
        
        self.tab_widget.addTab(tab, "🌍 Procedural")
    
    def _generate_asset(self, asset_type: str):
        """Generate an asset of the specified type."""
        if self.generating:
            QMessageBox.warning(self, "Generation in Progress", 
                              "Please wait for the current generation to complete.")
            return
        
        # Get parameters based on asset type
        params = self._get_generation_params(asset_type)
        if not params:
            return
        
        self.generating = True
        self.current_asset_type = asset_type
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start generation simulation
        self._simulate_generation(asset_type, params)
    
    def _get_generation_params(self, asset_type: str) -> Optional[Dict[str, Any]]:
        """Get generation parameters for the specified asset type."""
        try:
            if asset_type == "3d_model":
                return {
                    "type": self.model_type_combo.currentText(),
                    "detail": self.detail_slider.value(),
                    "max_polygons": self.poly_spin.value() * 1000,
                    "format": self.format_combo.currentText(),
                    "description": self.model_description.toPlainText().strip()
                }
            elif asset_type == "texture":
                return {
                    "type": self.texture_type_combo.currentText(),
                    "width": self.texture_width.value(),
                    "height": self.texture_height.value(),
                    "quality": self.texture_quality.currentText(),
                    "description": self.texture_description.toPlainText().strip()
                }
            elif asset_type == "material":
                return {
                    "type": self.material_type_combo.currentText(),
                    "metallic": self.metallic_spin.value(),
                    "roughness": self.roughness_spin.value(),
                    "description": self.material_description.toPlainText().strip()
                }
            elif asset_type == "audio":
                return {
                    "type": self.audio_type_combo.currentText(),
                    "duration": self.duration_spin.value(),
                    "format": self.audio_format.currentText(),
                    "description": self.audio_description.toPlainText().strip()
                }
            elif asset_type == "procedural":
                return {
                    "type": self.procedural_type_combo.currentText(),
                    "size_x": self.procedural_size.value(),
                    "size_y": self.procedural_size_y.value(),
                    "seed": self.seed_spin.value(),
                    "variation": self.variation_spin.value(),
                    "description": self.procedural_description.toPlainText().strip()
                }
        except Exception as e:
            self.logger.error(f"Error getting parameters for {asset_type}: {e}")
            QMessageBox.critical(self, "Error", f"Failed to get parameters: {e}")
            return None
        
        return None
    
    def _simulate_generation(self, asset_type: str, params: Dict[str, Any]):
        """Simulate asset generation with progress updates."""
        self.status_label.setText(f"Generating {asset_type}...")
        
        # Simulate generation steps
        steps = ["Analyzing parameters", "Generating content", "Optimizing", "Exporting", "Finalizing"]
        current_step = 0
        
        def update_progress():
            nonlocal current_step
            if current_step < len(steps):
                progress = int((current_step / len(steps)) * 100)
                self.progress_bar.setValue(progress)
                self.status_label.setText(f"Generating {asset_type}: {steps[current_step]}")
                current_step += 1
                
                if current_step < len(steps):
                    QTimer.singleShot(800, update_progress)
                else:
                    self._generation_complete(asset_type, params)
        
        QTimer.singleShot(500, update_progress)
    
    def _generation_complete(self, asset_type: str, params: Dict[str, Any]):
        """Handle generation completion."""
        self.generating = False
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        
        # Generate file path
        file_path = self._generate_file_path(asset_type, params)
        
        # Update status
        self.status_label.setText(f"✅ Generated {asset_type} successfully!")
        
        # Add to generated assets list
        asset_info = {
            "type": asset_type,
            "file_path": file_path,
            "params": params,
            "timestamp": "now"  # In real app, use actual timestamp
        }
        self.generated_assets.append(asset_info)
        
        # Emit signals
        self.asset_created.emit(asset_type, file_path)
        self.generation_complete.emit(asset_type, file_path)
        
        self.logger.info(f"Generated {asset_type} asset: {file_path}")
    
    def _generate_file_path(self, asset_type: str, params: Dict[str, Any]) -> str:
        """Generate a file path for the created asset."""
        # In real app, this would create actual files
        base_path = "generated_assets"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        # Generate filename based on type and description
        description = params.get("description", "asset")
        safe_name = "".join(c for c in description if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')[:30]
        
        if asset_type == "3d_model":
            ext = params.get("format", ".obj")
            filename = f"{safe_name}_model{ext}"
        elif asset_type == "texture":
            filename = f"{safe_name}_texture.png"
        elif asset_type == "material":
            filename = f"{safe_name}_material.mat"
        elif asset_type == "audio":
            ext = params.get("format", ".wav")
            filename = f"{safe_name}_audio{ext}"
        elif asset_type == "procedural":
            filename = f"{safe_name}_procedural.asset"
        else:
            filename = f"{safe_name}_{asset_type}.asset"
        
        return os.path.join(base_path, filename)
    
    def _view_generated_assets(self):
        """Show a dialog with all generated assets."""
        if not self.generated_assets:
            QMessageBox.information(self, "No Assets", "No assets have been generated yet.")
            return
        
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Generated Assets")
        dialog.setIcon(QMessageBox.Icon.Information)
        
        asset_list = "\n".join([
            f"• {asset['type']}: {asset['file_path']}"
            for asset in self.generated_assets
        ])
        
        dialog.setText(f"Generated Assets:\n\n{asset_list}")
        dialog.exec()
