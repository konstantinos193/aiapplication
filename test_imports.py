#!/usr/bin/env python3
"""
Test Imports.

This script tests if all the necessary imports work correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all necessary imports."""
    try:
        print("Testing imports...")
        
        # Test PyQt6 imports
        from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QSizePolicy
        print("✅ PyQt6 imports successful")
        
        # Test our custom imports
        from gui.game_design_ide import GameDesignIDE
        print("✅ GameDesignIDE import successful")
        
        from gui.ide_ai_assistant import IDEAIAssistant
        print("✅ IDEAIAssistant import successful")
        
        from gui.ide_center_panel import IDECenterPanel
        print("✅ IDECenterPanel import successful")
        
        from asset.asset_manager import AssetManager
        print("✅ AssetManager import successful")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
