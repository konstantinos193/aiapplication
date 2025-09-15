#!/usr/bin/env python3
"""
Simple accessibility test focusing on basic functionality.
"""

import sys
import os

# Add the accessibility directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gui', 'accessibility'))

def test_aria_basic():
    """Test basic ARIA functionality."""
    print("Testing ARIA Basic...")
    
    try:
        from aria_system import AriaSystem, AriaRole, AriaState
        
        aria = AriaSystem()
        
        # Test basic operations
        aria.set_aria_label("test1", "Test Label")
        aria.set_element_role("test1", AriaRole.BUTTON)
        
        label = aria.get_aria_label("test1")
        assert label.label == "Test Label"
        
        role = aria.get_element_role("test1")
        assert role == AriaRole.BUTTON
        
        print("  ✓ ARIA basic functionality working")
        return True
        
    except Exception as e:
        print(f"  ✗ ARIA basic test failed: {e}")
        return False

def test_screen_reader_basic():
    """Test basic screen reader functionality."""
    print("Testing Screen Reader Basic...")
    
    try:
        from screen_reader_integration import (
            ScreenReaderIntegration, ScreenReaderType, NavigationMode
        )
        
        # Create without complex initialization
        screen_reader = ScreenReaderIntegration()
        
        # Test basic profile creation
        from screen_reader_integration import ScreenReaderProfile
        profile = ScreenReaderProfile(
            user_id="test",
            screen_reader=ScreenReaderType.GENERIC
        )
        
        result = screen_reader.create_user_profile(profile)
        assert result == True
        
        print("  ✓ Screen reader basic functionality working")
        return True
        
    except Exception as e:
        print(f"  ✗ Screen reader basic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_semantic_basic():
    """Test basic semantic structure functionality."""
    print("Testing Semantic Basic...")
    
    try:
        from semantic_structure import SemanticStructure, HeadingLevel
        
        semantic = SemanticStructure()
        
        # Test basic heading
        from semantic_structure import HeadingStructure
        heading = HeadingStructure(
            element_id="h1",
            level=HeadingLevel.H1,
            text="Test Heading",
            order=1
        )
        
        result = semantic.register_heading(heading)
        assert result == True
        
        # Test retrieval
        retrieved = semantic.get_heading("h1")
        assert retrieved.text == "Test Heading"
        
        print("  ✓ Semantic basic functionality working")
        return True
        
    except Exception as e:
        print(f"  ✗ Semantic basic test failed: {e}")
        return False

def main():
    """Run basic tests."""
    print("Simple Accessibility Basic Test")
    print("=" * 35)
    
    tests = [
        test_aria_basic,
        test_screen_reader_basic,
        test_semantic_basic
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
        print("🎉 Basic accessibility functionality working!")
        return True
    else:
        print("❌ Some basic tests failed.")
        return False

if __name__ == "__main__":
    main()
