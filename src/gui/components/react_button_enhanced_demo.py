#!/usr/bin/env python3
"""
Enhanced Demo for React-Style Professional Button Component.

This demo showcases the enhanced button with:
- Exact CSS color scheme matching
- Light/dark theme switching
- All button variants and sizes
- Advanced animations and effects
- Professional IDE styling
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QFrame, QPushButton, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .react_style_button import ReactStyleButton
from ..design_system.react_theme_system import react_theme, ThemeMode


class EnhancedReactButtonDemo(QMainWindow):
    """Enhanced demo window showcasing React-style buttons with theme switching."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced React-Style Button Demo - Nexlify Engine")
        self.setGeometry(100, 100, 1000, 800)
        
        # Setup UI
        self._setup_ui()
        self._apply_theme()
        
        # Connect theme changes
        react_theme.theme_changed.connect(self._on_theme_changed)
        
    def _setup_ui(self):
        """Setup the enhanced demo user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        self._create_header_section(main_layout)
        
        # Theme controls section
        self._create_theme_section(main_layout)
        
        # Button variants section
        self._create_variants_section(main_layout)
        
        # Button sizes section
        self._create_sizes_section(main_layout)
        
        # Advanced features section
        self._create_advanced_features_section(main_layout)
        
        # Interactive section
        self._create_interactive_section(main_layout)
        
        main_layout.addStretch()
        
    def _create_header_section(self, parent_layout):
        """Create the header section with title and description."""
        # Title
        title = QLabel("Enhanced React-Style Button Component")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(700)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("100% Visual Fidelity with Exact CSS Color Matching")
        subtitle_font = QFont()
        subtitle_font.setPointSize(16)
        subtitle_font.setWeight(400)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(subtitle)
        
        # Description
        description = QLabel("Professional IDE styling with light/dark theme support, advanced animations, and sophisticated effects")
        description_font = QFont()
        description_font.setPointSize(14)
        description_font.setWeight(400)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(description)
        
    def _create_theme_section(self, parent_layout):
        """Create theme switching controls."""
        # Section header
        section_header = self._create_section_header("Theme Controls")
        parent_layout.addWidget(section_header)
        
        # Theme controls layout
        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(16)
        
        # Theme toggle button
        self.theme_toggle = ReactStyleButton(
            "Toggle Theme", 
            variant="outline", 
            size="md"
        )
        self.theme_toggle.clicked.connect(self._toggle_theme)
        theme_layout.addWidget(self.theme_toggle)
        
        # Current theme label
        self.theme_label = QLabel("Current Theme: Light")
        theme_layout.addWidget(self.theme_label)
        
        # Theme info
        theme_info = QLabel("Switch between light and dark themes to see the exact CSS color matching")
        theme_info.setWordWrap(True)
        theme_layout.addWidget(theme_info)
        
        theme_layout.addStretch()
        parent_layout.addLayout(theme_layout)
        
    def _create_variants_section(self, parent_layout):
        """Create section showing all button variants."""
        # Section header
        section_header = self._create_section_header("Button Variants")
        parent_layout.addWidget(section_header)
        
        # Variants layout
        variants_layout = QHBoxLayout()
        variants_layout.setSpacing(16)
        
        # Primary button
        primary_btn = ReactStyleButton("Primary", variant="primary")
        primary_btn.clicked.connect(lambda: self._show_click_message("Primary button clicked!"))
        variants_layout.addWidget(primary_btn)
        
        # Secondary button
        secondary_btn = ReactStyleButton("Secondary", variant="secondary")
        secondary_btn.clicked.connect(lambda: self._show_click_message("Secondary button clicked!"))
        variants_layout.addWidget(secondary_btn)
        
        # Outline button
        outline_btn = ReactStyleButton("Outline", variant="outline")
        outline_btn.clicked.connect(lambda: self._show_click_message("Outline button clicked!"))
        variants_layout.addWidget(outline_btn)
        
        # Ghost button
        ghost_btn = ReactStyleButton("Ghost", variant="ghost")
        ghost_btn.clicked.connect(lambda: self._show_click_message("Ghost button clicked!"))
        variants_layout.addWidget(ghost_btn)
        
        # Destructive button
        destructive_btn = ReactStyleButton("Destructive", variant="destructive")
        destructive_btn.clicked.connect(lambda: self._show_click_message("Destructive button clicked!"))
        variants_layout.addWidget(destructive_btn)
        
        variants_layout.addStretch()
        parent_layout.addLayout(variants_layout)
        
    def _create_sizes_section(self, parent_layout):
        """Create section showing all button sizes."""
        # Section header
        section_header = self._create_section_header("Button Sizes")
        parent_layout.addWidget(section_header)
        
        # Sizes layout
        sizes_layout = QHBoxLayout()
        sizes_layout.setSpacing(16)
        
        # Small button
        small_btn = ReactStyleButton("Small", size="sm", variant="primary")
        small_btn.clicked.connect(lambda: self._show_click_message("Small button clicked!"))
        sizes_layout.addWidget(small_btn)
        
        # Medium button
        medium_btn = ReactStyleButton("Medium", size="md", variant="primary")
        medium_btn.clicked.connect(lambda: self._show_click_message("Medium button clicked!"))
        sizes_layout.addWidget(medium_btn)
        
        # Large button
        large_btn = ReactStyleButton("Large", size="lg", variant="primary")
        large_btn.clicked.connect(lambda: self._show_click_message("Large button clicked!"))
        sizes_layout.addWidget(large_btn)
        
        sizes_layout.addStretch()
        parent_layout.addLayout(sizes_layout)
        
    def _create_advanced_features_section(self, parent_layout):
        """Create section showing advanced button features."""
        # Section header
        section_header = self._create_section_header("Advanced Features")
        parent_layout.addWidget(section_header)
        
        # Features layout
        features_layout = QHBoxLayout()
        features_layout.setSpacing(16)
        
        # Button with no gradient
        no_gradient_btn = ReactStyleButton("No Gradient", variant="primary", gradient=False)
        no_gradient_btn.clicked.connect(lambda: self._show_click_message("No gradient button clicked!"))
        features_layout.addWidget(no_gradient_btn)
        
        # Button with no shadow
        no_shadow_btn = ReactStyleButton("No Shadow", variant="primary", shadow=False)
        no_shadow_btn.clicked.connect(lambda: self._show_click_message("No shadow button clicked!"))
        features_layout.addWidget(no_shadow_btn)
        
        # Disabled button
        disabled_btn = ReactStyleButton("Disabled", variant="primary")
        disabled_btn.setEnabled(False)
        features_layout.addWidget(disabled_btn)
        
        # Custom properties button
        custom_btn = ReactStyleButton(
            "Custom", 
            variant="secondary", 
            custom_props={"special_effect": True}
        )
        custom_btn.clicked.connect(lambda: self._show_click_message("Custom button clicked!"))
        features_layout.addWidget(custom_btn)
        
        features_layout.addStretch()
        parent_layout.addLayout(features_layout)
        
    def _create_interactive_section(self, parent_layout):
        """Create section for interactive demonstrations."""
        # Section header
        section_header = self._create_section_header("Interactive Demo")
        parent_layout.addWidget(section_header)
        
        # Interactive layout
        interactive_layout = QHBoxLayout()
        interactive_layout.setSpacing(16)
        
        # Counter button
        self.counter = 0
        self.counter_label = QLabel("Clicks: 0")
        
        counter_btn = ReactStyleButton("Click Me!", variant="secondary", size="lg")
        counter_btn.clicked.connect(self._increment_counter)
        
        interactive_layout.addWidget(counter_btn)
        interactive_layout.addWidget(self.counter_label)
        
        # State display
        self.state_label = QLabel("Button State: normal")
        interactive_layout.addWidget(self.state_label)
        
        # Animation progress display
        self.progress_label = QLabel("Animation Progress: 0%")
        interactive_layout.addWidget(self.progress_label)
        
        interactive_layout.addStretch()
        parent_layout.addLayout(interactive_layout)
        
        # Connect button state changes
        counter_btn.state_changed.connect(self._on_button_state_changed)
        
    def _create_section_header(self, text: str) -> QLabel:
        """Create a section header label."""
        header = QLabel(text)
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setWeight(600)
        header.setFont(header_font)
        header.setStyleSheet("margin-top: 20px; margin-bottom: 10px;")
        return header
        
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        react_theme.toggle_theme()
        
    def _on_theme_changed(self, mode: ThemeMode):
        """Handle theme change events."""
        self._apply_theme()
        self.theme_label.setText(f"Current Theme: {mode.value.title()}")
        
    def _apply_theme(self):
        """Apply current theme to the demo window."""
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
                border-radius: {react_theme.get_radius("md")}px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors.accent};
                color: {colors.accent_foreground};
            }}
        """)
        
    def _show_click_message(self, message: str):
        """Show a message when a button is clicked."""
        print(f"🎯 {message}")
        
    def _increment_counter(self):
        """Increment the click counter."""
        self.counter += 1
        self.counter_label.setText(f"Clicks: {self.counter}")
        
    def _on_button_state_changed(self, old_state: str, new_state: str):
        """Handle button state changes."""
        self.state_label.setText(f"Button State: {new_state}")
        
        # Update animation progress display
        if hasattr(self, 'counter_btn'):
            progress = self.counter_btn.get_animation_progress()
            hover_progress = int(progress.get("hover", 0) * 100)
            self.progress_label.setText(f"Animation Progress: {hover_progress}%")


def main():
    """Main function to run the enhanced demo."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show demo window
    demo = EnhancedReactButtonDemo()
    demo.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
