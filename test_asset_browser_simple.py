#!/usr/bin/env python3
"""
Simple Asset Browser Test.

This script tests the basic asset browser integration.
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
    print("Starting Asset Browser Test...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create asset manager
    asset_manager = AssetManager()
    
    # Create and show IDE
    ide = GameDesignIDE(asset_manager)
    ide.show()
    
    print("✅ IDE loaded with asset browser!")
    print("📁 Asset browser should be visible below the 3D viewport")
    print("🔍 Try clicking on different asset categories")
    print("🔍 Try searching for assets")
    
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
