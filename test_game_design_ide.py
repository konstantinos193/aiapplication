#!/usr/bin/env python3
"""
Test file for the complete Game Design IDE.

This will launch the full IDE with all panels and components
to verify everything works correctly together.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from gui.game_design_ide import GameDesignIDE
from gui.design_system.react_theme_system import react_theme


def main():
    """Main function to launch the Game Design IDE."""
    print("🚀 Launching Game Design IDE...")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Game Design IDE - Nexlify Engine")
    app.setApplicationVersion("2.1.0")
    
    print("✅ Qt application created")
    
    # Create and show the IDE
    print("🎯 Creating Game Design IDE...")
    ide = GameDesignIDE()
    
    print("✅ IDE created successfully")
    
    # Show the IDE
    ide.show()
    print("✅ IDE displayed")
    
    # Print IDE information
    print(f"📊 IDE Size: {ide.width()}x{ide.height()}")
    print(f"🎮 Play State: {ide.getPlayState()}")
    print(f"🎯 Selected Object: {ide.getSelectedObject()}")
    print(f"📁 Active Tab: {ide.getActiveTab()}")
    
    # Test theme switching
    print("🌙 Testing theme system...")
    
    def test_theme_switching():
        """Test theme switching functionality."""
        current_theme = react_theme.get_current_mode()
        print(f"🎨 Current theme: {current_theme}")
        
        # Toggle theme
        react_theme.toggle_theme()
        new_theme = react_theme.get_current_mode()
        print(f"🎨 New theme: {new_theme}")
        
        # Toggle back
        react_theme.toggle_theme()
        final_theme = react_theme.get_current_mode()
        print(f"🎨 Final theme: {final_theme}")
        
        print("✅ Theme switching test completed")
    
    # Schedule theme test after a delay
    QTimer.singleShot(2000, test_theme_switching)
    
    # Test play state
    def test_play_state():
        """Test play state functionality."""
        print("▶️ Testing play state...")
        
        # Set play state
        ide.setPlayState(True)
        play_state = ide.getPlayState()
        print(f"▶️ Play state set to: {play_state}")
        
        # Test object selection
        ide.setSelectedObject("Main Camera")
        selected_object = ide.getSelectedObject()
        print(f"🎯 Selected object: {selected_object}")
        
        # Test tab switching
        ide.setActiveTab("Game Logic")
        active_tab = ide.getActiveTab()
        print(f"📁 Active tab: {active_tab}")
        
        print("✅ Play state test completed")
    
    # Schedule play state test after theme test
    QTimer.singleShot(4000, test_play_state)
    
    print("🚀 Game Design IDE is ready!")
    print("💡 Features available:")
    print("   - Header with play controls and transform tools")
    print("   - Left panel: Scene hierarchy + inspector")
    print("   - Center panel: 3D viewport + tabs + assets browser")
    print("   - Right panel: AI chat assistant")
    print("   - Status bar with system info")
    print("   - Theme switching (🌙 button in header)")
    print("   - Resizable panels")
    print("   - Professional styling with gradients and shadows")
    
    # Run the application
    print("\n🎮 Starting main loop...")
    exit_code = app.exec()
    
    print("👋 Game Design IDE closed")
    return exit_code


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Error launching Game Design IDE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
