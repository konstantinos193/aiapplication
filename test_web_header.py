#!/usr/bin/env python3
"""
Test the web-embedded header.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer
    from gui.ide_header_web_working import IDEHeader
    
    print("✅ All imports successful!")
    
    # Create app
    app = QApplication(sys.argv)
    print("✅ QApplication created!")
    
    # Create header
    header = IDEHeader()
    print("✅ Header created!")
    
    # Show header
    header.show()
    print("✅ Header shown!")
    
    # Set up timer to close after 5 seconds
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(5000)
    
    print("✅ Starting app (will close in 5 seconds)...")
    sys.exit(app.exec())
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
