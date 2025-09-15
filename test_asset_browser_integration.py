#!/usr/bin/env python3
"""
Test Asset Browser Integration.

This script tests the integration of the asset browser into the main IDE.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from gui.game_design_ide import GameDesignIDE
from asset.asset_manager import AssetManager


def test_asset_browser():
    """Test the asset browser integration."""
    print("Testing Asset Browser Integration...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create asset manager
    asset_manager = AssetManager()
    
    # Create and show IDE
    ide = GameDesignIDE(asset_manager)
    ide.show()
    
    # Test asset browser functionality after a short delay
    def test_functionality():
        print("\n=== Testing Asset Browser Functionality ===")
        
        # Test setting category
        print("1. Testing category selection...")
        ide.setAssetCategory("textures")
        
        # Test asset selection
        print("2. Testing asset selection...")
        ide.selectAsset("player_diffuse.png", "texture")
        
        # Test search
        print("3. Testing asset search...")
        ide.searchAssets("player")
        
        # Test refresh
        print("4. Testing asset refresh...")
        ide.refreshAssets()
        
        print("✅ All asset browser tests completed!")
        
        # Close after testing
        QTimer.singleShot(2000, app.quit)
    
    # Run tests after UI is loaded
    QTimer.singleShot(1000, test_functionality)
    
    # Run app
    return app.exec()


if __name__ == "__main__":
    try:
        exit_code = test_asset_browser()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Error testing asset browser: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
