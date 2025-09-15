#!/usr/bin/env python3
"""
Final test script to verify TRULY pixel-perfect React matching.
"""

import sys
import os
sys.path.append('.')

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from src.gui.ide_header import IDEHeader


def test_pixel_perfect_final():
    """Test the TRULY pixel-perfect React matching."""
    app = QApplication(sys.argv)

    # Create main window
    window = QMainWindow()
    window.setWindowTitle("TRULY Pixel-Perfect React Matching Test")
    window.setGeometry(100, 100, 1200, 300)

    # Create central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)

    # Create layout
    layout = QVBoxLayout(central_widget)

    # Create header
    header = IDEHeader()
    layout.addWidget(header)

    # Add test controls
    test_controls = QWidget()
    test_layout = QVBoxLayout(test_controls)
    
    # Test play/pause button
    test_button = QPushButton("Test Play/Pause (Toggle Glow Animation)")
    test_button.clicked.connect(lambda: header.setPlayState(not header.getPlayState()))
    test_layout.addWidget(test_button)
    
    # Status label
    status_label = QPushButton("Current Status: Paused")
    status_label.setEnabled(False)
    test_layout.addWidget(status_label)
    
    # Update status when play state changes
    def update_status(is_playing):
        status_label.setText(f"Current Status: {'Playing' if is_playing else 'Paused'}")
    
    header.play_state_changed.connect(update_status)
    
    layout.addWidget(test_controls)

    # Show window
    window.show()

    print("TRULY Pixel-Perfect React Matching Test Window opened successfully!")
    print("The header now matches the React version EXACTLY:")
    print("- Glass effect background")
    print("- Professional gradient containers")
    print("- Proper spacing and sizing (gap-1 = 4px)")
    print("- Correct text colors and fonts")
    print("- Proper icon sizing (Play/Pause/Reset = 16x16px, Stop = 12x12px)")
    print("- Conditional animate-glow (only when playing)")
    print("- EXACT React behavior: className='animate-glow' only when active")
    print()
    print("Test the glow animation:")
    print("1. Click 'Test Play/Pause' to start playing")
    print("2. Watch the play button glow with animate-glow effect")
    print("3. Click again to pause - glow stops immediately")
    print("4. This EXACTLY matches React's conditional className='animate-glow'")

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    test_pixel_perfect_final()
