#!/usr/bin/env python3
"""
Simple Test for React-Style Input Component - Quick Verification.

This script quickly tests the input to verify it looks identical
to the React ProfessionalInput component.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.gui.components.react_style_input import ReactStyleInput
from src.gui.design_system.react_theme_system import react_theme, ThemeMode


class SimpleInputTest(QMainWindow):
    """Simple test window for quick input verification."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Test - Quick Verification")
        self.setGeometry(100, 100, 600, 500)
        
        # Apply initial theme
        self._apply_theme()
        
        # Connect theme changes
        react_theme.theme_changed.connect(self._on_theme_changed)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the simple test user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("React Input Verification")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setWeight(700)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Theme toggle
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_display = QLabel("Light")
        theme_toggle = QLabel("Click to toggle")
        theme_toggle.setStyleSheet("color: blue; text-decoration: underline; cursor: pointer;")
        theme_toggle.mousePressEvent = lambda e: self._toggle_theme()
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_display)
        theme_layout.addWidget(theme_toggle)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        # Test inputs
        # Basic input
        basic_input = ReactStyleInput(
            label="Username",
            placeholder="Enter your username"
        )
        basic_input.text_changed.connect(lambda text: print(f"Basic: {text}"))
        layout.addWidget(basic_input)
        
        # Input with error
        error_input = ReactStyleInput(
            label="Email",
            placeholder="Enter your email",
            error="Please enter a valid email address"
        )
        error_input.text_changed.connect(lambda text: print(f"Error: {text}"))
        layout.addWidget(error_input)
        
        # Input without label
        no_label_input = ReactStyleInput(
            placeholder="Input without label"
        )
        no_label_input.text_changed.connect(lambda text: print(f"No label: {text}"))
        layout.addWidget(no_label_input)
        
        # Instructions
        instructions = QLabel("""
        Verification Checklist:
        ✓ Border radius should be exactly 6px (rounded-md)
        ✓ Focus ring should be 2px with ring-offset-0
        ✓ Focus shadow should be subtle (shadow-md shadow-accent/20)
        ✓ Error state should use destructive colors
        ✓ Label should be text-xs font-medium text-muted-foreground
        ✓ Input should be h-9 (36px height)
        ✓ Padding should be px-3 py-1 (12px horizontal, 4px vertical)
        """)
        instructions.setWordWrap(True)
        instructions.setFont(QFont("Arial", 10))
        layout.addWidget(instructions)
        
        layout.addStretch()
        
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
        """)


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show test window
    window = SimpleInputTest()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
