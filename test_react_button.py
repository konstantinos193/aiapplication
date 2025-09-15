#!/usr/bin/env python3
"""
Enhanced Test Script for React-Style Button Component.

This script showcases the enhanced button with:
- Exact CSS color scheme matching
- Light/dark theme switching
- All button variants and features
- Professional IDE styling
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.gui.components.react_style_button import ReactStyleButton
from src.gui.design_system.react_theme_system import react_theme, ThemeMode


class EnhancedTestWindow(QMainWindow):
    """Enhanced test window for React-style button with theme switching."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced React Button Test - Nexlify")
        self.setGeometry(100, 100, 800, 600)
        
        # Apply initial theme
        self._apply_theme()
        
        # Connect theme changes
        react_theme.theme_changed.connect(self._on_theme_changed)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the enhanced test user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Enhanced React-Style Button Test")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setWeight(700)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Theme toggle section
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Current Theme:")
        self.theme_display = QLabel("Light")
        theme_toggle = ReactStyleButton("Toggle Theme", variant="outline")
        theme_toggle.clicked.connect(self._toggle_theme)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_display)
        theme_layout.addWidget(theme_toggle)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        # Button variants
        variants_layout = QHBoxLayout()
        variants_layout.setSpacing(16)
        
        primary_btn = ReactStyleButton("Primary", variant="primary")
        primary_btn.clicked.connect(lambda: print("Primary clicked!"))
        variants_layout.addWidget(primary_btn)
        
        secondary_btn = ReactStyleButton("Secondary", variant="secondary")
        secondary_btn.clicked.connect(lambda: print("Secondary clicked!"))
        variants_layout.addWidget(secondary_btn)
        
        outline_btn = ReactStyleButton("Outline", variant="outline")
        outline_btn.clicked.connect(lambda: print("Outline clicked!"))
        variants_layout.addWidget(outline_btn)
        
        ghost_btn = ReactStyleButton("Ghost", variant="ghost")
        ghost_btn.clicked.connect(lambda: print("Ghost clicked!"))
        variants_layout.addWidget(ghost_btn)
        
        destructive_btn = ReactStyleButton("Destructive", variant="destructive")
        destructive_btn.clicked.connect(lambda: print("Destructive clicked!"))
        variants_layout.addWidget(destructive_btn)
        
        variants_layout.addStretch()
        layout.addLayout(variants_layout)
        
        # Button sizes
        sizes_layout = QHBoxLayout()
        sizes_layout.setSpacing(16)
        
        small_btn = ReactStyleButton("Small", size="sm", variant="primary")
        small_btn.clicked.connect(lambda: print("Small clicked!"))
        sizes_layout.addWidget(small_btn)
        
        medium_btn = ReactStyleButton("Medium", size="md", variant="primary")
        medium_btn.clicked.connect(lambda: print("Medium clicked!"))
        sizes_layout.addWidget(medium_btn)
        
        large_btn = ReactStyleButton("Large", size="lg", variant="primary")
        large_btn.clicked.connect(lambda: print("Large clicked!"))
        sizes_layout.addWidget(large_btn)
        
        sizes_layout.addStretch()
        layout.addLayout(sizes_layout)
        
        # Features
        features_layout = QHBoxLayout()
        features_layout.setSpacing(16)
        
        no_gradient_btn = ReactStyleButton("No Gradient", variant="primary", gradient=False)
        no_gradient_btn.clicked.connect(lambda: print("No gradient clicked!"))
        features_layout.addWidget(no_gradient_btn)
        
        no_shadow_btn = ReactStyleButton("No Shadow", variant="primary", shadow=False)
        no_shadow_btn.clicked.connect(lambda: print("No shadow clicked!"))
        features_layout.addWidget(no_shadow_btn)
        
        disabled_btn = ReactStyleButton("Disabled", variant="primary")
        disabled_btn.setEnabled(False)
        features_layout.addWidget(disabled_btn)
        
        features_layout.addStretch()
        layout.addLayout(features_layout)
        
        # Theme info
        theme_info = QLabel("This button uses the exact CSS color scheme from your React design system!")
        theme_info.setWordWrap(True)
        theme_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(theme_info)
        
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
    window = EnhancedTestWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
