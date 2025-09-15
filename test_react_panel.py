#!/usr/bin/env python3
"""
Test for React-Style Panel Component - Visual Fidelity Verification.

This script tests the ReactStylePanel to verify it looks identical
to the React ProfessionalPanel component.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.gui.components.react_style_panel import ReactStylePanel
from src.gui.components.react_style_button import ReactStyleButton
from src.gui.components.react_style_input import ReactStyleInput
from src.gui.design_system.react_theme_system import react_theme, ThemeMode


class ReactPanelTest(QMainWindow):
    """Test window for React-style panel verification."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("React Panel Test - Visual Fidelity")
        self.setGeometry(100, 100, 1200, 800)

        # Apply initial theme
        self._apply_theme()

        # Connect theme changes
        react_theme.theme_changed.connect(self._on_theme_changed)

        self._setup_ui()

    def _setup_ui(self):
        """Setup the test user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("React Panel Visual Fidelity Test")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setWeight(700)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Theme toggle
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_display = QLabel("Light")
        theme_toggle = QPushButton("Toggle Theme")
        theme_toggle.clicked.connect(self._toggle_theme)

        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_display)
        theme_layout.addWidget(theme_toggle)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # Panels showcase
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(20)

        # Left side - Basic panels
        basic_panels = self._create_basic_panels_showcase()
        panels_layout.addWidget(basic_panels)

        # Right side - Advanced panels
        advanced_panels = self._create_advanced_panels_showcase()
        panels_layout.addWidget(advanced_panels)

        layout.addLayout(panels_layout)

        # Interactive demo
        interactive_demo = self._create_interactive_demo()
        layout.addWidget(interactive_demo)

        layout.addStretch()

    def _create_basic_panels_showcase(self) -> QWidget:
        """Create basic panels showcase."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)

        # Panel without title
        no_title_panel = ReactStylePanel()
        no_title_panel.addWidget(QLabel("Panel without title"))
        no_title_panel.addWidget(ReactStyleButton("Button inside panel"))
        layout.addWidget(no_title_panel)

        # Panel with title only
        title_panel = ReactStylePanel(title="Panel with Title")
        title_panel.addWidget(QLabel("This panel has a title but no icon"))
        title_panel.addWidget(ReactStyleInput(placeholder="Input inside panel"))
        layout.addWidget(title_panel)

        # Panel with title and icon
        icon_panel = ReactStylePanel(title="Settings Panel", icon="⚙️")
        icon_panel.addWidget(QLabel("This panel has both title and icon"))
        icon_panel.addWidget(ReactStyleButton("Save Settings", variant="primary"))
        layout.addWidget(icon_panel)

        return container

    def _create_advanced_panels_showcase(self) -> QWidget:
        """Create advanced panels showcase."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)

        # Panel with gradient
        gradient_panel = ReactStylePanel(title="Gradient Panel", gradient=True)
        gradient_panel.addWidget(QLabel("This panel has a gradient background"))
        gradient_panel.addWidget(ReactStyleButton("Gradient Button", variant="secondary"))
        layout.addWidget(gradient_panel)

        # Panel without shadow
        no_shadow_panel = ReactStylePanel(title="No Shadow Panel", shadow=False)
        no_shadow_panel.addWidget(QLabel("This panel has no shadow"))
        no_shadow_panel.addWidget(ReactStyleInput(label="No shadow input"))
        layout.addWidget(no_shadow_panel)

        # Panel with all features
        full_panel = ReactStylePanel(title="Full Featured Panel", icon="🚀", gradient=True, shadow=True)
        full_panel.addWidget(QLabel("This panel has everything:"))
        full_panel.addWidget(QLabel("• Title with icon"))
        full_panel.addWidget(QLabel("• Gradient background"))
        full_panel.addWidget(QLabel("• Professional shadows"))
        full_panel.addWidget(ReactStyleButton("Full Feature Button", variant="primary"))
        layout.addWidget(full_panel)

        return container

    def _create_interactive_demo(self) -> QWidget:
        """Create interactive demo section."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)

        # Title
        demo_title = QLabel("Interactive Demo")
        demo_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(demo_title)

        # Dynamic panel
        self.dynamic_panel = ReactStylePanel(title="Dynamic Panel")
        self.dynamic_panel.addWidget(QLabel("This panel can be modified in real-time"))
        
        # Controls
        controls_layout = QHBoxLayout()
        
        # Title control
        title_input = ReactStyleInput(placeholder="Enter new title")
        title_input.textChanged.connect(self._update_panel_title)
        controls_layout.addWidget(title_input)
        
        # Icon control
        icon_input = ReactStyleInput(placeholder="Enter icon (emoji)")
        icon_input.textChanged.connect(self._update_panel_icon)
        controls_layout.addWidget(icon_input)
        
        # Toggle buttons
        gradient_toggle = QPushButton("Toggle Gradient")
        gradient_toggle.clicked.connect(self._toggle_gradient)
        controls_layout.addWidget(gradient_toggle)
        
        shadow_toggle = QPushButton("Toggle Shadow")
        shadow_toggle.clicked.connect(self._toggle_shadow)
        controls_layout.addWidget(shadow_toggle)
        
        self.dynamic_panel.addLayout(controls_layout)
        layout.addWidget(self.dynamic_panel)

        # Instructions
        instructions = QLabel("""
        Interactive Features:
        • Type in the title input to change the panel title
        • Type an emoji in the icon input to change the icon
        • Click buttons to toggle gradient and shadow effects
        • Hover over panels to see subtle animations
        """)
        instructions.setWordWrap(True)
        instructions.setFont(QFont("Arial", 10))
        layout.addWidget(instructions)

        return container

    def _update_panel_title(self, title: str):
        """Update dynamic panel title."""
        if title:
            self.dynamic_panel.setTitle(title)

    def _update_panel_icon(self, icon: str):
        """Update dynamic panel icon."""
        if icon:
            self.dynamic_panel.setIcon(icon)

    def _toggle_gradient(self):
        """Toggle gradient on dynamic panel."""
        current = self.dynamic_panel.gradient_enabled
        self.dynamic_panel.setGradient(not current)

    def _toggle_shadow(self):
        """Toggle shadow on dynamic panel."""
        current = self.dynamic_panel.shadow_enabled
        self.dynamic_panel.setShadow(not current)

    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        react_theme.toggle_theme()

    def _on_theme_changed(self, mode: ThemeMode):
        """Handle theme change events."""
        self._apply_theme()
        self.theme_display.setText(mode.value.title())

    def _apply_theme(self):
        """Apply current theme to the test window."""
        colors = react_theme.get_current_colors()

        # Apply theme colors
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {colors.background};
                color: {colors.foreground};
            }}
            QLabel {{
                color: {colors.foreground};
            }}
            QPushButton {{
                background-color: {colors.secondary};
                color: {colors.secondary_foreground};
                border: 1px solid {colors.border};
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors.accent};
                color: {colors.accent_foreground};
            }}
        """)


def main():
    """Main function."""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show test window
    window = ReactPanelTest()
    window.show()

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
