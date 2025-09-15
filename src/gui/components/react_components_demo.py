#!/usr/bin/env python3
"""
Comprehensive Demo for React-Style Components - Nexlify Engine.

This demo showcases both React-style components:
- ProfessionalButton (EnhancedReactButton)
- ProfessionalInput (ReactStyleInput)
- Light/dark theme switching
- All variants and features
- Professional IDE styling
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QFrame, QPushButton, QCheckBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .react_style_button import ReactStyleButton
from .react_style_input import ReactStyleInput
from ..design_system.react_theme_system import react_theme, ThemeMode


class ReactComponentsDemo(QMainWindow):
    """Comprehensive demo window showcasing React-style components with theme switching."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("React-Style Components Demo - Nexlify Engine")
        self.setGeometry(100, 100, 1200, 900)
        
        # Setup UI
        self._setup_ui()
        self._apply_theme()
        
        # Connect theme changes
        react_theme.theme_changed.connect(self._on_theme_changed)
        
    def _setup_ui(self):
        """Setup the comprehensive demo user interface."""
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
        
        # Components showcase
        self._create_components_showcase(main_layout)
        
        main_layout.addStretch()
        
    def _create_header_section(self, parent_layout):
        """Create the header section with title and description."""
        # Title
        title = QLabel("React-Style Components Showcase")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setWeight(700)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("100% Visual Fidelity with Exact CSS Color Matching")
        subtitle_font = QFont()
        subtitle_font.setPointSize(18)
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
            size="lg"
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
        
    def _create_components_showcase(self, parent_layout):
        """Create comprehensive components showcase."""
        # Create horizontal layout for components
        components_layout = QHBoxLayout()
        components_layout.setSpacing(20)
        
        # Left side - Buttons showcase
        buttons_showcase = self._create_buttons_showcase()
        components_layout.addWidget(buttons_showcase)
        
        # Right side - Inputs showcase
        inputs_showcase = self._create_inputs_showcase()
        components_layout.addWidget(inputs_showcase)
        
        parent_layout.addLayout(components_layout)
        
    def _create_buttons_showcase(self) -> QGroupBox:
        """Create comprehensive buttons showcase."""
        group_box = QGroupBox("Professional Buttons")
        group_box.setFont(self._get_section_font())
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(16)
        
        # Button variants
        variants_header = QLabel("Button Variants")
        variants_header.setFont(self._get_subsection_font())
        layout.addWidget(variants_header)
        
        variants_layout = QHBoxLayout()
        variants_layout.setSpacing(12)
        
        primary_btn = ReactStyleButton("Primary", variant="primary")
        primary_btn.clicked.connect(lambda: self._show_click_message("Primary button clicked!"))
        variants_layout.addWidget(primary_btn)
        
        secondary_btn = ReactStyleButton("Secondary", variant="secondary")
        secondary_btn.clicked.connect(lambda: self._show_click_message("Secondary button clicked!"))
        variants_layout.addWidget(secondary_btn)
        
        outline_btn = ReactStyleButton("Outline", variant="outline")
        outline_btn.clicked.connect(lambda: self._show_click_message("Outline button clicked!"))
        variants_layout.addWidget(outline_btn)
        
        ghost_btn = ReactStyleButton("Ghost", variant="ghost")
        ghost_btn.clicked.connect(lambda: self._show_click_message("Ghost button clicked!"))
        variants_layout.addWidget(ghost_btn)
        
        destructive_btn = ReactStyleButton("Destructive", variant="destructive")
        destructive_btn.clicked.connect(lambda: self._show_click_message("Destructive button clicked!"))
        variants_layout.addWidget(destructive_btn)
        
        variants_layout.addStretch()
        layout.addLayout(variants_layout)
        
        # Button sizes
        sizes_header = QLabel("Button Sizes")
        sizes_header.setFont(self._get_subsection_font())
        layout.addWidget(sizes_header)
        
        sizes_layout = QHBoxLayout()
        sizes_layout.setSpacing(12)
        
        small_btn = ReactStyleButton("Small", size="sm", variant="primary")
        small_btn.clicked.connect(lambda: self._show_click_message("Small button clicked!"))
        sizes_layout.addWidget(small_btn)
        
        medium_btn = ReactStyleButton("Medium", size="md", variant="primary")
        medium_btn.clicked.connect(lambda: self._show_click_message("Medium button clicked!"))
        sizes_layout.addWidget(medium_btn)
        
        large_btn = ReactStyleButton("Large", size="lg", variant="primary")
        large_btn.clicked.connect(lambda: self._show_click_message("Large button clicked!"))
        sizes_layout.addWidget(large_btn)
        
        sizes_layout.addStretch()
        layout.addLayout(sizes_layout)
        
        # Advanced features
        features_header = QLabel("Advanced Features")
        features_header.setFont(self._get_subsection_font())
        layout.addWidget(features_header)
        
        features_layout = QHBoxLayout()
        features_layout.setSpacing(12)
        
        no_gradient_btn = ReactStyleButton("No Gradient", variant="primary", gradient=False)
        no_gradient_btn.clicked.connect(lambda: self._show_click_message("No gradient button clicked!"))
        features_layout.addWidget(no_gradient_btn)
        
        no_shadow_btn = ReactStyleButton("No Shadow", variant="primary", shadow=False)
        no_shadow_btn.clicked.connect(lambda: self._show_click_message("No shadow button clicked!"))
        features_layout.addWidget(no_shadow_btn)
        
        disabled_btn = ReactStyleButton("Disabled", variant="primary")
        disabled_btn.setEnabled(False)
        features_layout.addWidget(disabled_btn)
        
        features_layout.addStretch()
        layout.addLayout(features_layout)
        
        layout.addStretch()
        return group_box
        
    def _create_inputs_showcase(self) -> QGroupBox:
        """Create comprehensive inputs showcase."""
        group_box = QGroupBox("Professional Inputs")
        group_box.setFont(self._get_section_font())
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(16)
        
        # Basic inputs
        basic_header = QLabel("Basic Inputs")
        basic_header.setFont(self._get_subsection_font())
        layout.addWidget(basic_header)
        
        # Username input
        username_input = ReactStyleInput(
            label="Username",
            placeholder="Enter your username",
            text=""
        )
        username_input.text_changed.connect(lambda text: self._show_input_message(f"Username: {text}"))
        layout.addWidget(username_input)
        
        # Email input with error
        email_input = ReactStyleInput(
            label="Email",
            placeholder="Enter your email",
            error="Please enter a valid email address"
        )
        email_input.text_changed.connect(lambda text: self._show_input_message(f"Email: {text}"))
        layout.addWidget(email_input)
        
        # Password input
        password_input = ReactStyleInput(
            label="Password",
            placeholder="Enter your password",
            text=""
        )
        password_input.text_changed.connect(lambda text: self._show_input_message(f"Password: {text}"))
        layout.addWidget(password_input)
        
        # Advanced inputs
        advanced_header = QLabel("Advanced Inputs")
        advanced_header.setFont(self._get_subsection_font())
        layout.addWidget(advanced_header)
        
        # Gradient input
        gradient_input = ReactStyleInput(
            label="Gradient Input",
            placeholder="This input has a gradient background",
            gradient=True
        )
        gradient_input.text_changed.connect(lambda text: self._show_input_message(f"Gradient: {text}"))
        layout.addWidget(gradient_input)
        
        # Read-only input
        readonly_input = ReactStyleInput(
            label="Read-only Input",
            text="This input is read-only",
            placeholder="Cannot edit this"
        )
        readonly_input.setReadOnly(True)
        layout.addWidget(readonly_input)
        
        # Disabled input
        disabled_input = ReactStyleInput(
            label="Disabled Input",
            text="This input is disabled",
            placeholder="Cannot use this"
        )
        disabled_input.setEnabled(False)
        layout.addWidget(disabled_input)
        
        # Interactive demo
        interactive_header = QLabel("Interactive Demo")
        interactive_header.setFont(self._get_subsection_font())
        layout.addWidget(interactive_header)
        
        # Dynamic error input
        self.dynamic_error_input = ReactStyleInput(
            label="Dynamic Error Input",
            placeholder="Type 'error' to see an error message"
        )
        self.dynamic_error_input.text_changed.connect(self._on_dynamic_input_changed)
        layout.addWidget(self.dynamic_error_input)
        
        # Clear button
        clear_btn = ReactStyleButton("Clear All Inputs", variant="secondary", size="sm")
        clear_btn.clicked.connect(self._clear_all_inputs)
        layout.addWidget(clear_btn)
        
        layout.addStretch()
        return group_box
        
    def _get_section_font(self) -> QFont:
        """Get section header font."""
        font = QFont()
        font.setPointSize(20)
        font.setWeight(600)
        return font
        
    def _get_subsection_font(self) -> QFont:
        """Get subsection header font."""
        font = QFont()
        font.setPointSize(16)
        font.setWeight(500)
        return font
        
    def _create_section_header(self, text: str) -> QLabel:
        """Create a section header label."""
        header = QLabel(text)
        header_font = QFont()
        header_font.setPointSize(24)
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
            QGroupBox {{
                color: {colors.foreground};
                border: 2px solid {colors.border};
                border-radius: {react_theme.get_radius("md")}px;
                margin-top: 1ex;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {colors.foreground};
            }}
        """)
        
    def _show_click_message(self, message: str):
        """Show a message when a button is clicked."""
        print(f"🎯 {message}")
        
    def _show_input_message(self, message: str):
        """Show a message when input text changes."""
        print(f"📝 {message}")
        
    def _on_dynamic_input_changed(self, text: str):
        """Handle dynamic input changes for error demonstration."""
        if text.lower() == "error":
            self.dynamic_error_input.setError("This is a dynamic error message!")
        else:
            self.dynamic_error_input.setError("")
            
    def _clear_all_inputs(self):
        """Clear all input fields."""
        # Find all ReactStyleInput widgets and clear them
        for child in self.findChildren(ReactStyleInput):
            child.clear()
            child.setError("")
        print("🧹 All inputs cleared!")


def main():
    """Main function to run the comprehensive demo."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show demo window
    demo = ReactComponentsDemo()
    demo.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
