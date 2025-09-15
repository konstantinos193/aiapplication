#!/usr/bin/env python3
"""
Test script to verify text-based icons are working properly.
"""

import sys
import os
sys.path.append('.')

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from src.gui.ide_header import IDEHeader


def test_text_icons():
    """Test the text-based icons in the header."""
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Text Icons Test")
    window.setGeometry(100, 100, 800, 200)
    
    # Create central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Create layout
    layout = QVBoxLayout(central_widget)
    
    # Create header
    header = IDEHeader()
    layout.addWidget(header)
    
    # Show window
    window.show()
    
    print("Text Icons Test Window opened successfully!")
    print("Check if the play (▶), stop (■), and reset (↻) icons are visible and properly sized.")
    print("Click the play button to see it switch between play (▶) and pause (⏸) icons.")
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    test_text_icons()
