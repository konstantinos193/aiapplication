#!/usr/bin/env python3
"""
Demo for React-Style Professional Button Component.

This demo showcases all button variants, sizes, and features
to demonstrate the 100% visual fidelity with the React version.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .react_style_button import ReactStyleButton


class ReactButtonDemo(QMainWindow):
    """Demo window showcasing React-style buttons."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("React-Style Button Demo - Nexlify Engine")
        self.setGeometry(100, 100, 800, 600)
        
        # Setup UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the demo user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("React-Style Button Component Demo")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setWeight(700)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        subtitle = QLabel("100% Visual Fidelity with React ProfessionalButton")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_font.setWeight(400)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #64748b;")
        main_layout.addWidget(subtitle)
        
        # Variants section
        self._create_variants_section(main_layout)
        
        # Sizes section
        self._create_sizes_section(main_layout)
        
        # Features section
        self._create_features_section(main_layout)
        
        # Interactive section
        self._create_interactive_section(main_layout)
        
        main_layout.addStretch()
        
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
        
    def _create_features_section(self, parent_layout):
        """Create section showing button features."""
        # Section header
        section_header = self._create_section_header("Button Features")
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
        self.counter_label.setStyleSheet("color: #f8fafc; font-size: 14px;")
        
        counter_btn = ReactStyleButton("Click Me!", variant="secondary", size="lg")
        counter_btn.clicked.connect(self._increment_counter)
        
        interactive_layout.addWidget(counter_btn)
        interactive_layout.addWidget(self.counter_label)
        interactive_layout.addStretch()
        
        parent_layout.addLayout(interactive_layout)
        
    def _create_section_header(self, text: str) -> QLabel:
        """Create a section header label."""
        header = QLabel(text)
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setWeight(600)
        header.setFont(header_font)
        header.setStyleSheet("color: #f8fafc; margin-top: 20px; margin-bottom: 10px;")
        return header
        
    def _show_click_message(self, message: str):
        """Show a message when a button is clicked."""
        print(f"🎯 {message}")
        
    def _increment_counter(self):
        """Increment the click counter."""
        self.counter += 1
        self.counter_label.setText(f"Clicks: {self.counter}")


def main():
    """Main function to run the demo."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show demo window
    demo = ReactButtonDemo()
    demo.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
