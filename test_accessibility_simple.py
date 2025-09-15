#!/usr/bin/env python3
"""
Simple test script for accessibility systems.

This script tests the accessibility modules without complex imports.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_aria_system():
    """Test the ARIA system."""
    print("Testing ARIA System...")
    
    try:
        from gui.accessibility.aria_system import (
            AriaSystem, AriaRole, AriaState, LiveRegionPriority
        )
        
        aria_system = AriaSystem()
        
        # Test basic functionality
        assert aria_system.set_aria_label("btn1", "Save Button", "Saves the current document")
        assert aria_system.set_element_role("btn1", AriaRole.BUTTON)
        assert aria_system.set_element_state("btn1", AriaState.PRESSED, "false")
        
        # Test live region
        assert aria_system.create_live_region("status1", LiveRegionPriority.ASSERTIVE)
        assert aria_system.announce_to_live_region("status1", "Document saved successfully")
        
        # Test attribute generation
        attributes = aria_system.generate_aria_attributes("btn1")
        assert "role" in attributes
        assert attributes["role"] == "button"
        
        print("  ✓ ARIA system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ ARIA system test failed: {e}")
        return False

def test_screen_reader_integration():
    """Test the screen reader integration system."""
    print("Testing Screen Reader Integration...")
    
    try:
        from gui.accessibility.screen_reader_integration import (
            ScreenReaderIntegration, AnnouncementPriority, NavigationMode,
            ScreenReaderType, NavigationElement, ScreenReaderProfile
        )
        
        screen_reader = ScreenReaderIntegration()
        
        # Test user profile
        profile = ScreenReaderProfile(
            user_id="test_user",
            screen_reader=ScreenReaderType.NVDA,
            navigation_preference=NavigationMode.LANDMARK
        )
        assert screen_reader.create_user_profile(profile)
        assert screen_reader.set_current_user("test_user")
        
        # Test announcements
        assert screen_reader.announce("Page loaded successfully")
        assert screen_reader.announce_error("Validation error occurred")
        
        # Test navigation
        nav_element = NavigationElement(
            element_id="nav1",
            role="navigation",
            label="Main Navigation",
            level=1,
            order=1
        )
        assert screen_reader.register_navigation_element(nav_element)
        assert screen_reader.navigate_to_element("nav1")
        
        print("  ✓ Screen reader integration working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Screen reader integration test failed: {e}")
        return False

def test_semantic_structure():
    """Test the semantic structure system."""
    print("Testing Semantic Structure...")
    
    try:
        from gui.accessibility.semantic_structure import (
            SemanticStructure, HeadingLevel, LandmarkType, 
            HeadingStructure, LandmarkRegion
        )
        
        semantic = SemanticStructure()
        
        # Test heading
        heading = HeadingStructure(
            element_id="h1",
            level=HeadingLevel.H1,
            text="Main Title",
            order=1
        )
        assert semantic.register_heading(heading)
        
        # Test landmark
        landmark = LandmarkRegion(
            element_id="nav1",
            type=LandmarkType.NAVIGATION,
            label="Main Navigation",
            level=1,
            order=2
        )
        assert semantic.register_landmark(landmark)
        
        # Test structure retrieval
        heading_hierarchy = semantic.get_heading_hierarchy()
        assert heading_hierarchy['total'] == 1
        
        landmark_structure = semantic.get_landmark_structure()
        assert landmark_structure['total'] == 1
        
        print("  ✓ Semantic structure working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Semantic structure test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Simple Accessibility Systems Test")
    print("=" * 40)
    
    tests = [
        test_aria_system,
        test_screen_reader_integration,
        test_semantic_structure
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
        print("🎉 All accessibility systems are working correctly!")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    main()
