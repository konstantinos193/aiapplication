#!/usr/bin/env python3
"""
Test creating accessibility classes step by step.
"""

import sys
import os

# Disable logging
import logging
logging.disable(logging.CRITICAL)

# Add the accessibility directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gui', 'accessibility'))

def test_aria_class_creation():
    """Test creating ARIA class step by step."""
    print("Testing ARIA Class Creation...")
    
    try:
        # Import enums first
        from aria_system import AriaRole, AriaState, AriaProperty
        print("  ✓ Enums imported")
        
        # Import dataclasses
        from aria_system import AriaLabel, AriaLiveRegion, AriaRelationship
        print("  ✓ Dataclasses imported")
        
        # Import main class
        from aria_system import AriaSystem
        print("  ✓ AriaSystem class imported")
        
        # Create instance
        aria = AriaSystem()
        print("  ✓ AriaSystem instance created")
        
        # Test basic operation
        result = aria.set_aria_label("test1", "Test Label")
        print(f"  ✓ Set label result: {result}")
        
        print("  ✓ ARIA class creation successful")
        return True
        
    except Exception as e:
        print(f"  ✗ ARIA class creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_screen_reader_class_creation():
    """Test creating screen reader class step by step."""
    print("Testing Screen Reader Class Creation...")
    
    try:
        # Import enums first
        from screen_reader_integration import (
            AnnouncementPriority, NavigationMode, ScreenReaderType
        )
        print("  ✓ Enums imported")
        
        # Import dataclasses
        from screen_reader_integration import (
            ScreenReaderAnnouncement, NavigationElement, ScreenReaderProfile
        )
        print("  ✓ Dataclasses imported")
        
        # Import main class
        from screen_reader_integration import ScreenReaderIntegration
        print("  ✓ ScreenReaderIntegration class imported")
        
        # Create instance
        screen_reader = ScreenReaderIntegration()
        print("  ✓ ScreenReaderIntegration instance created")
        
        # Test basic operation
        profile = ScreenReaderProfile(
            user_id="test",
            screen_reader=ScreenReaderType.GENERIC
        )
        result = screen_reader.create_user_profile(profile)
        print(f"  ✓ Create profile result: {result}")
        
        print("  ✓ Screen reader class creation successful")
        return True
        
    except Exception as e:
        print(f"  ✗ Screen reader class creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_semantic_class_creation():
    """Test creating semantic class step by step."""
    print("Testing Semantic Class Creation...")
    
    try:
        # Import enums first
        from semantic_structure import HeadingLevel, LandmarkType, ListType
        print("  ✓ Enums imported")
        
        # Import dataclasses
        from semantic_structure import (
            HeadingStructure, LandmarkRegion, ListStructure
        )
        print("  ✓ Dataclasses imported")
        
        # Import main class
        from semantic_structure import SemanticStructure
        print("  ✓ SemanticStructure class imported")
        
        # Create instance
        semantic = SemanticStructure()
        print("  ✓ SemanticStructure instance created")
        
        # Test basic operation
        heading = HeadingStructure(
            element_id="h1",
            level=HeadingLevel.H1,
            text="Test Heading",
            order=1
        )
        result = semantic.register_heading(heading)
        print(f"  ✓ Register heading result: {result}")
        
        print("  ✓ Semantic class creation successful")
        return True
        
    except Exception as e:
        print(f"  ✗ Semantic class creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run class creation tests."""
    print("Accessibility Class Creation Test")
    print("=" * 40)
    
    tests = [
        test_aria_class_creation,
        test_screen_reader_class_creation,
        test_semantic_class_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All classes created successfully!")
        return True
    else:
        print("❌ Some class creation failed.")
        return False

if __name__ == "__main__":
    main()
