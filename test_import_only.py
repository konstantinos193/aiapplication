#!/usr/bin/env python3
"""
Test importing only the enums from accessibility modules.
"""

import sys
import os

# Disable logging
import logging
logging.disable(logging.CRITICAL)

# Add the accessibility directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gui', 'accessibility'))

def test_aria_enums():
    """Test importing ARIA enums only."""
    print("Testing ARIA Enums Import...")
    
    try:
        from aria_system import AriaRole, AriaState, AriaProperty
        print("  ✓ ARIA enums imported successfully")
        
        # Test enum values
        assert AriaRole.BUTTON.value == "button"
        assert AriaState.PRESSED.value == "aria-pressed"
        assert AriaProperty.LABEL.value == "aria-label"
        
        print("  ✓ ARIA enum values correct")
        return True
        
    except Exception as e:
        print(f"  ✗ ARIA enums import failed: {e}")
        return False

def test_screen_reader_enums():
    """Test importing screen reader enums only."""
    print("Testing Screen Reader Enums Import...")
    
    try:
        from screen_reader_integration import (
            AnnouncementPriority, NavigationMode, ScreenReaderType
        )
        print("  ✓ Screen reader enums imported successfully")
        
        # Test enum values
        assert AnnouncementPriority.NORMAL.value == "normal"
        assert NavigationMode.LINEAR.value == "linear"
        assert ScreenReaderType.NVDA.value == "nvda"
        
        print("  ✓ Screen reader enum values correct")
        return True
        
    except Exception as e:
        print(f"  ✗ Screen reader enums import failed: {e}")
        return False

def test_semantic_enums():
    """Test importing semantic enums only."""
    print("Testing Semantic Enums Import...")
    
    try:
        from semantic_structure import HeadingLevel, LandmarkType, ListType
        print("  ✓ Semantic enums imported successfully")
        
        # Test enum values
        assert HeadingLevel.H1.value == 1
        assert LandmarkType.NAVIGATION.value == "navigation"
        assert ListType.UNORDERED.value == "unordered"
        
        print("  ✓ Semantic enum values correct")
        return True
        
    except Exception as e:
        print(f"  ✗ Semantic enums import failed: {e}")
        return False

def main():
    """Run enum import tests."""
    print("Accessibility Enums Import Test")
    print("=" * 35)
    
    tests = [
        test_aria_enums,
        test_screen_reader_enums,
        test_semantic_enums
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 35)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enums imported successfully!")
        return True
    else:
        print("❌ Some enum imports failed.")
        return False

if __name__ == "__main__":
    main()
