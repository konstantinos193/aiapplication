"""
AI Tools Panel for Nexlify Engine.

This module provides AI-powered tools for:
- Code generation
- Asset creation
- Scene building
- Problem solving
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QComboBox, QSpinBox, 
    QCheckBox, QGroupBox, QScrollArea, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor

from ..utils.logger import get_logger


class AIToolsPanel(QWidget):
    """AI Tools panel with multiple AI-powered features."""
    
    # Signals
    code_generated = pyqtSignal(str, str)  # code, language
    asset_generated = pyqtSignal(str, str)  # asset_type, file_path
    scene_generated = pyqtSignal(str)  # scene_description
    
    def __init__(self, game_engine):
        """Initialize the AI Tools panel.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        self._init_ui()
        self.logger.info("AI Tools panel initialized")
    
    def _init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header
        header = QLabel("AI Tools")
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
        self._create_code_generator_tab()
        self._create_asset_generator_tab()
        self._create_scene_builder_tab()
        self._create_problem_solver_tab()
        
        main_layout.addWidget(self.tab_widget)
    
    def _create_code_generator_tab(self):
        """Create the code generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Language selection
        lang_group = QGroupBox("Code Language")
        lang_layout = QHBoxLayout(lang_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "C++", "C#", "JavaScript", "GLSL"])
        self.language_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
        """)
        lang_layout.addWidget(QLabel("Language:"))
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        layout.addWidget(lang_group)
        
        # Prompt input
        prompt_group = QGroupBox("AI Prompt")
        prompt_layout = QVBoxLayout(prompt_group)
        
        self.code_prompt = QTextEdit()
        self.code_prompt.setPlaceholderText("Describe the code you want me to generate...\n\nExamples:\n- 'Create a player movement script'\n- 'Generate a shader for water effects'\n- 'Write a collision detection system'")
        self.code_prompt.setMaximumHeight(100)
        self.code_prompt.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        prompt_layout.addWidget(self.code_prompt)
        
        layout.addWidget(prompt_group)
        
        # Generate button
        generate_btn = QPushButton("Generate Code")
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
        generate_btn.clicked.connect(self._generate_code)
        layout.addWidget(generate_btn)
        
        # Generated code display
        code_group = QGroupBox("Generated Code")
        code_layout = QVBoxLayout(code_group)
        
        self.generated_code = QTextEdit()
        self.generated_code.setReadOnly(True)
        self.generated_code.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        code_layout.addWidget(self.generated_code)
        
        # Code actions
        code_actions = QHBoxLayout()
        
        copy_btn = QPushButton("📋 Copy")
        copy_btn.setStyleSheet("""
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
        copy_btn.clicked.connect(self._copy_generated_code)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self._save_generated_code)
        
        code_actions.addWidget(copy_btn)
        code_actions.addWidget(save_btn)
        code_actions.addStretch()
        
        code_layout.addLayout(code_actions)
        layout.addWidget(code_group)
        
        self.tab_widget.addTab(tab, "Code Generator")
    
    def _create_asset_generator_tab(self):
        """Create the asset generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Asset type selection
        type_group = QGroupBox("Asset Type")
        type_layout = QHBoxLayout(type_group)
        
        self.asset_type_combo = QComboBox()
        self.asset_type_combo.addItems(["3D Model (.obj)", "Texture (.png)", "Audio (.wav)", "Material", "Animation"])
        self.asset_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 150px;
            }
        """)
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.asset_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Asset parameters
        params_group = QGroupBox("Parameters")
        params_layout = QVBoxLayout(params_group)
        
        # Size parameters
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(16, 4096)
        self.width_spin.setValue(512)
        self.width_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        size_layout.addWidget(self.width_spin)
        
        size_layout.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(16, 4096)
        self.height_spin.setValue(512)
        self.height_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        size_layout.addWidget(self.height_spin)
        size_layout.addStretch()
        
        params_layout.addLayout(size_layout)
        
        # Quality settings
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Low", "Medium", "High", "Ultra"])
        self.quality_combo.setCurrentText("Medium")
        self.quality_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }
        """)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        
        params_layout.addLayout(quality_layout)
        layout.addWidget(params_group)
        
        # Asset description
        desc_group = QGroupBox("Asset Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.asset_description = QTextEdit()
        self.asset_description.setPlaceholderText("Describe the asset you want to generate...\n\nExamples:\n- 'A realistic tree with green leaves'\n- 'A metallic surface with scratches'\n- 'A futuristic weapon model'")
        self.asset_description.setMaximumHeight(80)
        self.asset_description.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        desc_layout.addWidget(self.asset_description)
        
        layout.addWidget(desc_group)
        
        # Generate button
        generate_btn = QPushButton("🎨 Generate Asset")
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
        generate_btn.clicked.connect(self._generate_asset)
        layout.addWidget(generate_btn)
        
        # Progress and status
        self.asset_status = QLabel("Ready to generate assets")
        self.asset_status.setStyleSheet("""
            QLabel {
                color: #4ec9b0;
                font-style: italic;
                padding: 10px;
                background-color: #2d2d30;
                border-radius: 4px;
                border: 1px solid #3e3e42;
            }
        """)
        layout.addWidget(self.asset_status)
        
        self.tab_widget.addTab(tab, "Asset Generator")
    
    def _create_scene_builder_tab(self):
        """Create the scene building tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Scene type
        type_group = QGroupBox("Scene Type")
        type_layout = QHBoxLayout(type_group)
        
        self.scene_type_combo = QComboBox()
        self.scene_type_combo.addItems(["Outdoor Environment", "Indoor Room", "Game Level", "Character Scene", "Vehicle Scene", "Custom"])
        self.scene_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 180px;
            }
        """)
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.scene_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Scene description
        desc_group = QGroupBox("Scene Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.scene_description = QTextEdit()
        self.scene_description.setPlaceholderText("Describe the scene you want to build...\n\nExamples:\n- 'A forest clearing with ancient ruins'\n- 'A sci-fi laboratory with holographic displays'\n- 'A medieval castle courtyard with fountains'")
        self.scene_description.setMaximumHeight(100)
        self.scene_description.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        desc_layout.addWidget(self.scene_description)
        
        layout.addWidget(desc_group)
        
        # Scene options
        options_group = QGroupBox("Scene Options")
        options_layout = QVBoxLayout(options_group)
        
        self.auto_lighting = QCheckBox("Auto-generate lighting")
        self.auto_lighting.setChecked(True)
        self.auto_lighting.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        
        self.auto_materials = QCheckBox("Auto-generate materials")
        self.auto_materials.setChecked(True)
        
        self.optimize_geometry = QCheckBox("Optimize geometry")
        self.optimize_geometry.setChecked(True)
        
        options_layout.addWidget(self.auto_lighting)
        options_layout.addWidget(self.auto_materials)
        options_layout.addWidget(self.optimize_geometry)
        
        layout.addWidget(options_group)
        
        # Build button
        build_btn = QPushButton("Build Scene")
        build_btn.setStyleSheet("""
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
        build_btn.clicked.connect(self._build_scene)
        layout.addWidget(build_btn)
        
        # Scene preview
        preview_group = QGroupBox("Generated Scene")
        preview_layout = QVBoxLayout(preview_group)
        
        self.scene_preview = QTextEdit()
        self.scene_preview.setReadOnly(True)
        self.scene_preview.setMaximumHeight(150)
        self.scene_preview.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        preview_layout.addWidget(self.scene_preview)
        
        layout.addWidget(preview_group)
        
        self.tab_widget.addTab(tab, "🏗️ Scene Builder")
    
    def _create_problem_solver_tab(self):
        """Create the problem solving tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Problem input
        problem_group = QGroupBox("Describe Your Problem")
        problem_layout = QVBoxLayout(problem_group)
        
        self.problem_input = QTextEdit()
        self.problem_input.setPlaceholderText("Describe the coding problem or bug you're experiencing...\n\nExamples:\n- 'My game crashes when loading textures'\n- 'How do I implement smooth camera movement?'\n- 'Performance is slow with many objects'")
        self.problem_input.setMaximumHeight(120)
        self.problem_input.setStyleSheet("""
            QTextEdit {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        problem_layout.addWidget(self.problem_input)
        
        layout.addWidget(problem_group)
        
        # Problem type
        type_group = QGroupBox("Problem Category")
        type_layout = QHBoxLayout(type_group)
        
        self.problem_type_combo = QComboBox()
        self.problem_type_combo.addItems(["Bug Fix", "Performance", "Architecture", "Algorithm", "API Usage", "General"])
        self.problem_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #3e3e42;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
        """)
        type_layout.addWidget(QLabel("Category:"))
        type_layout.addWidget(self.problem_type_combo)
        type_layout.addStretch()
        
        layout.addWidget(type_group)
        
        # Solve button
        solve_btn = QPushButton("🔍 Solve Problem")
        solve_btn.setStyleSheet("""
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
        solve_btn.clicked.connect(self._solve_problem)
        layout.addWidget(solve_btn)
        
        # Solution display
        solution_group = QGroupBox("AI Solution")
        solution_layout = QVBoxLayout(solution_group)
        
        self.solution_display = QTextEdit()
        self.solution_display.setReadOnly(True)
        self.solution_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
            }
        """)
        solution_layout.addWidget(self.solution_display)
        
        layout.addWidget(solution_group)
        
        self.tab_widget.addTab(tab, "🔍 Problem Solver")
    
    def _generate_code(self):
        """Generate code based on the prompt."""
        prompt = self.code_prompt.toPlainText().strip()
        language = self.language_combo.currentText()
        
        if not prompt:
            self.generated_code.setText("Please enter a prompt first.")
            return
        
        # Simulate AI code generation (replace with actual AI call)
        sample_code = self._get_sample_code(language, prompt)
        
        self.generated_code.setText(sample_code)
        self.logger.info(f"Generated {language} code for prompt: {prompt[:50]}...")
        
        # Emit signal
        self.code_generated.emit(sample_code, language)
    
    def _generate_asset(self):
        """Generate an asset based on the description."""
        asset_type = self.asset_type_combo.currentText()
        description = self.asset_description.toPlainText().strip()
        
        if not description:
            self.asset_status.setText("Please enter an asset description first.")
            return
        
        self.asset_status.setText(f"Generating {asset_type}...")
        
        # Simulate asset generation (replace with actual AI call)
        # In real implementation, this would call AI service and save files
        
        self.asset_status.setText(f"Generated {asset_type} successfully!")
        self.logger.info(f"Generated {asset_type} asset: {description[:50]}...")
        
        # Emit signal
        self.asset_generated.emit(asset_type, f"generated_{asset_type.lower()}")
    
    def _build_scene(self):
        """Build a scene based on the description."""
        scene_type = self.scene_type_combo.currentText()
        description = self.scene_description.toPlainText().strip()
        
        if not description:
            self.scene_preview.setText("Please enter a scene description first.")
            return
        
        # Simulate scene building (replace with actual AI call)
        scene_data = self._get_sample_scene(scene_type, description)
        
        self.scene_preview.setText(scene_data)
        self.logger.info(f"Built {scene_type} scene: {description[:50]}...")
        
        # Emit signal
        self.scene_generated.emit(description)
    
    def _solve_problem(self):
        """Solve a coding problem."""
        problem = self.problem_input.toPlainText().strip()
        problem_type = self.problem_type_combo.currentText()
        
        if not problem:
            self.solution_display.setText("Please describe your problem first.")
            return
        
        # Simulate problem solving (replace with actual AI call)
        solution = self._get_sample_solution(problem_type, problem)
        
        self.solution_display.setText(solution)
        self.logger.info(f"Solved {problem_type} problem: {problem[:50]}...")
    
    def _copy_generated_code(self):
        """Copy generated code to clipboard."""
        code = self.generated_code.toPlainText()
        if code:
            clipboard = self.window().windowHandle().clipboard()
            clipboard.setText(code)
            self.logger.info("Copied generated code to clipboard")
    
    def _save_generated_code(self):
        """Save generated code to file."""
        # TODO: Implement file save dialog
        self.logger.info("Save code functionality not implemented yet")
    
    def _get_sample_code(self, language: str, prompt: str) -> str:
        """Get sample code for demonstration."""
        if "player movement" in prompt.lower():
            if language == "Python":
                return '''import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.angle = 0
    
    def move(self, keys):
        if keys[pygame.K_w]:
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed
        if keys[pygame.K_s]:
            self.x -= math.cos(self.angle) * self.speed
            self.y -= math.sin(self.angle) * self.speed
        if keys[pygame.K_a]:
            self.angle -= 0.1
        if keys[pygame.K_d]:
            self.angle += 0.1
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 20)'''
            elif language == "C++":
                return '''#include <SFML/Graphics.hpp>
#include <cmath>

class Player {
private:
    float x, y;
    float speed = 5.0f;
    float angle = 0.0f;
    
public:
    Player(float startX, float startY) : x(startX), y(startY) {}
    
    void move(const sf::Keyboard::Key& key) {
        if (key == sf::Keyboard::W) {
            x += cos(angle) * speed;
            y += sin(angle) * speed;
        }
        if (key == sf::Keyboard::S) {
            x -= cos(angle) * speed;
            y -= sin(angle) * speed;
        }
        if (key == sf::Keyboard::A) angle -= 0.1f;
        if (key == sf::Keyboard::D) angle += 0.1f;
    }
    
    void draw(sf::RenderWindow& window) {
        sf::CircleShape player(20);
        player.setPosition(x, y);
        player.setFillColor(sf::Color::Red);
        window.draw(player);
    }
};'''
        
        # Default sample code
        return f"// Generated {language} code for: {prompt}\n// This is a sample implementation\n// Replace with actual AI-generated code\n\n"
    
    def _get_sample_scene(self, scene_type: str, description: str) -> str:
        """Get sample scene data for demonstration."""
        return f"""Scene: {scene_type}
Description: {description}

Generated Objects:
- Ground plane (100x100 units)
- Lighting: Directional light (sun)
- Camera: Position (0, 10, -20), Target (0, 0, 0)

Objects:
1. Main building (position: 0, 0, 0)
2. Trees (positions: -15, 0, -10; 15, 0, -10)
3. Path (from -20, 0, 0 to 20, 0, 0)

Materials:
- Ground: Grass texture
- Building: Stone material
- Trees: Bark and leaf materials

This scene was generated by AI based on your description.
In the full implementation, this would create actual GameObjects."""
    
    def _get_sample_solution(self, problem_type: str, problem: str) -> str:
        """Get sample solution for demonstration."""
        return f"""Problem: {problem}
Category: {problem_type}

AI Solution:

1. **Root Cause Analysis:**
   The issue appears to be related to resource management and memory allocation.

2. **Recommended Fix:**
   - Implement proper resource cleanup
   - Add error handling for edge cases
   - Use smart pointers for memory management

3. **Code Example:**
   ```cpp
   // Before (problematic)
   Texture* texture = new Texture();
   // ... use texture
   // Missing delete - memory leak!
   
   // After (fixed)
   std::unique_ptr<Texture> texture = std::make_unique<Texture>();
   // ... use texture
   // Automatically cleaned up
   ```

4. **Prevention:**
   - Always use RAII principles
   - Implement unit tests for edge cases
   - Use static analysis tools

This solution was generated by AI analysis of your problem.
In the full implementation, this would provide specific code fixes."""
