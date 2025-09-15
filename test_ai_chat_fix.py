#!/usr/bin/env python3
"""
Test AI Chat Panel Fix.

This script tests if the AI chat panel now properly extends to the bottom.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from gui.game_design_ide import GameDesignIDE
from asset.asset_manager import AssetManager


def main():
    """Main test function."""
    print("Starting AI Chat Panel Fix Test...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create asset manager
    asset_manager = AssetManager()
    
    # Create and show IDE
    ide = GameDesignIDE(asset_manager)
    ide.show()
    
    print("✅ IDE loaded!")
    print("🔍 Check if AI chat panel now extends to the bottom")
    print("🔍 Look for debug messages about sizing")
    print("🔍 Try resizing the window to see if layout updates properly")
    
    # Run app
    return app.exec()


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
