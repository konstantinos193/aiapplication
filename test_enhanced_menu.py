#!/usr/bin/env python3
"""
Test script for the enhanced menu system and AI panels.

This script tests the new features:
- Enhanced menu system with AI menu
- AI Tools panel
- Asset Generator panel
- Enhanced toolbar
- Menu shortcuts
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from gui.main_window import MainWindow
from core.engine import GameEngine


def test_enhanced_menu():
    """Test the enhanced menu system."""
    app = QApplication(sys.argv)
    
    # Create a mock game engine
    engine = GameEngine()
    
    # Create main window
    config = {
        "window_title": "Nexlify - Enhanced Menu Test",
        "theme": "dark",
        "ai_enabled": True
    }
    
    window = MainWindow(engine, config)
    window.show()
    
    # Test the enhanced features
    print("✅ Enhanced Menu System Test")
    print("📋 Available features:")
    print("   - AI Menu with shortcuts")
    print("   - Enhanced Toolbar with icons")
    print("   - AI Tools Panel (Ctrl+Shift+A)")
    print("   - Asset Generator Panel (Ctrl+Shift+G)")
    print("   - Scene Tools in Tools menu")
    print("   - AI Generation shortcuts")
    
    # Auto-test: Open AI Tools after 2 seconds
    def open_ai_tools():
        print("🤖 Opening AI Tools panel...")
        window._show_ai_tools()
    
    # Auto-test: Open Asset Generator after 4 seconds
    def open_asset_generator():
        print("🎨 Opening Asset Generator panel...")
        window._show_asset_generator()
    
    # Auto-test: Test AI generation after 6 seconds
    def test_ai_generation():
        print("🚀 Testing AI generation...")
        window._generate_code_ai()
    
    # Schedule tests
    QTimer.singleShot(2000, open_ai_tools)
    QTimer.singleShot(4000, open_asset_generator)
    QTimer.singleShot(6000, test_ai_generation)
    
    print("\n🎯 Test sequence will run automatically:")
    print("   2s: Open AI Tools")
    print("   4s: Open Asset Generator")
    print("   6s: Test AI Code Generation")
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    test_enhanced_menu()
