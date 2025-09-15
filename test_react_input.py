#!/usr/bin/env python3
"""
Comprehensive Test for React-Style Input Component - Nexlify Engine.

This test showcases the ReactStyleInput with:
- Exact CSS color scheme matching
- Light/dark theme switching
- All input states and features
- Professional IDE styling
- 100% visual fidelity with React component
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.gui.components.react_style_input import ReactStyleInput
from src.gui.design_system.react_theme_system import react_theme, ThemeMode


class ReactInputTest(QMainWindow):
    """Comprehensive test window for React-style input with theme switching."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("React-Style Input Test - Nexlify")
        self.setGeometry(100, 100, 1000, 800)
        
        # Apply initial theme
        self._apply_theme()
        
        # Connect theme changes
        react_theme.theme_changed.connect(self._on_theme_changed)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the comprehensive test user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("React-Style Input Component Test")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setWeight(700)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("100% Visual Fidelity with Exact CSS Color Matching")
        subtitle_font = QFont()
        subtitle_font.setPointSize(16)
        subtitle_font.setWeight(400)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Theme toggle section
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Current Theme:")
        self.theme_display = QLabel("Light")
        theme_toggle = QLabel("Toggle Theme (Click here)")
        theme_toggle.setStyleSheet("color: blue; text-decoration: underline; cursor: pointer;")
        theme_toggle.mousePressEvent = lambda e: self._toggle_theme()
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_display)
        theme_layout.addWidget(theme_toggle)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        # Components showcase
        components_layout = QHBoxLayout()
        components_layout.setSpacing(20)
        
        # Left side - Basic inputs
        basic_inputs = self._create_basic_inputs_showcase()
        components_layout.addWidget(basic_inputs)
        
        # Right side - Advanced inputs
        advanced_inputs = self._create_advanced_inputs_showcase()
        components_layout.addWidget(advanced_inputs)
        
        layout.addLayout(components_layout)
        
        # Interactive demo section
        interactive_demo = self._create_interactive_demo()
        layout.addWidget(interactive_demo)
        
        # Theme info
        theme_info = QLabel("This input uses the exact CSS color scheme from your React design system!")
        theme_info.setWordWrap(True)
        theme_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(theme_info)
        
        layout.addStretch()
        
    def _create_basic_inputs_showcase(self) -> QGroupBox:
        """Create basic inputs showcase."""
        group_box = QGroupBox("Basic Inputs")
        group_box.setFont(self._get_section_font())
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(16)
        
        # Username input
        username_input = ReactStyleInput(
            label="Username",
            placeholder="Enter your username"
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
            placeholder="Enter your password"
        )
        password_input.text_changed.connect(lambda text: self._show_input_message(f"Password: {text}"))
        layout.addWidget(password_input)
        
        # No label input
        no_label_input = ReactStyleInput(
            placeholder="Input without label"
        )
        no_label_input.text_changed.connect(lambda text: self._show_input_message(f"No label: {text}"))
        layout.addWidget(no_label_input)
        
        layout.addStretch()
        return group_box
        
    def _create_advanced_inputs_showcase(self) -> QGroupBox:
        """Create advanced inputs showcase."""
        group_box = QGroupBox("Advanced Inputs")
        group_box.setFont(self._get_section_font())
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(16)
        
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
        
        # Input with initial text
        initial_input = ReactStyleInput(
            label="Input with Initial Text",
            text="Hello World!",
            placeholder="This has initial text"
        )
        initial_input.text_changed.connect(lambda text: self._show_input_message(f"Initial: {text}"))
        layout.addWidget(initial_input)
        
        layout.addStretch()
        return group_box
        
    def _create_interactive_demo(self) -> QGroupBox:
        """Create interactive demo section."""
        group_box = QGroupBox("Interactive Demo")
        group_box.setFont(self._get_section_font())
        
        layout = QVBoxLayout(group_box)
        layout.setSpacing(16)
        
        # Dynamic error input
        self.dynamic_error_input = ReactStyleInput(
            label="Dynamic Error Input",
            placeholder="Type 'error' to see an error message"
        )
        self.dynamic_error_input.text_changed.connect(self._on_dynamic_input_changed)
        layout.addWidget(self.dynamic_error_input)
        
        # Dynamic label input
        self.dynamic_label_input = ReactStyleInput(
            label="Dynamic Label Input",
            placeholder="Type 'label' to change the label"
        )
        self.dynamic_label_input.text_changed.connect(self._on_dynamic_label_changed)
        layout.addWidget(self.dynamic_label_input)
        
        # Focus state display
        self.focus_state_label = QLabel("Focus State: None")
        self.focus_state_label.setFont(self._get_subsection_font())
        layout.addWidget(self.focus_state_label)
        
        # Connect focus changes
        self.dynamic_error_input.focus_changed.connect(self._on_focus_changed)
        self.dynamic_label_input.focus_changed.connect(self._on_focus_changed)
        
        # Instructions
        instructions = QLabel("""
        Interactive Features:
        • Type 'error' in the first input to see error styling
        • Type 'label' in the second input to change its label
        • Click on inputs to see focus ring and shadow effects
        • Watch the focus state display update in real-time
        """)
        instructions.setWordWrap(True)
        instructions.setFont(self._get_subsection_font())
        layout.addWidget(instructions)
        
        return group_box
        
    def _get_section_font(self) -> QFont:
        """Get section header font."""
        font = QFont()
        font.setPointSize(18)
        font.setWeight(600)
        return font
        
    def _get_subsection_font(self) -> QFont:
        """Get subsection header font."""
        font = QFont()
        font.setPointSize(14)
        font.setWeight(500)
        return font
        
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
            QGroupBox {{
                color: {colors.foreground};
                border: 2px solid {colors.border};
                border-radius: 8px;
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
        
    def _show_input_message(self, message: str):
        """Show a message when input text changes."""
        print(f"📝 {message}")
        
    def _on_dynamic_input_changed(self, text: str):
        """Handle dynamic input changes for error demonstration."""
        if text.lower() == "error":
            self.dynamic_error_input.setError("This is a dynamic error message!")
        else:
            self.dynamic_error_input.setError("")
            
    def _on_dynamic_label_changed(self, text: str):
        """Handle dynamic input changes for label demonstration."""
        if text.lower() == "label":
            self.dynamic_label_input.setLabel("Label Changed!")
        else:
            self.dynamic_label_input.setLabel("Dynamic Label Input")
            
    def _on_focus_changed(self, focused: bool):
        """Handle focus state changes."""
        if focused:
            self.focus_state_label.setText("Focus State: Focused")
        else:
            self.focus_state_label.setText("Focus State: None")


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show test window
    window = ReactInputTest()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
