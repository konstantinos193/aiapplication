#!/usr/bin/env python3
"""
Minimal test to check basic functionality.
"""

print("Starting minimal test...")

try:
    print("Testing basic imports...")
    
    # Test basic Python functionality
    from enum import Enum
    from dataclasses import dataclass
    print("✓ Basic imports working")
    
    # Test our modules
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    print("✓ Path setup complete")
    
    # Try to import our modules
    try:
        from gui.accessibility.aria_system import AriaSystem
        print("✓ ARIA system import successful")
    except Exception as e:
        print(f"✗ ARIA system import failed: {e}")
    
    try:
        from gui.accessibility.screen_reader_integration import ScreenReaderIntegration
        print("✓ Screen reader integration import successful")
    except Exception as e:
        print(f"✗ Screen reader integration import failed: {e}")
    
    try:
        from gui.accessibility.semantic_structure import SemanticStructure
        print("✓ Semantic structure import successful")
    except Exception as e:
        print(f"✗ Semantic structure import failed: {e}")
    
    print("Minimal test completed.")
    
except Exception as e:
    print(f"Test failed with error: {e}")
    import traceback
    traceback.print_exc()
