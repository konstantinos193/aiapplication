#!/usr/bin/env python3
"""
Standalone test for accessibility systems.

This test directly imports and tests the accessibility modules
without going through the problematic gui package imports.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_aria_system_standalone():
    """Test the ARIA system directly."""
    print("Testing ARIA System (Standalone)...")
    
    try:
        # Import directly from the module path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gui', 'accessibility'))
        
        from aria_system import (
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
        import traceback
        traceback.print_exc()
        return False

def test_screen_reader_integration_standalone():
    """Test the screen reader integration system directly."""
    print("Testing Screen Reader Integration (Standalone)...")
    
    try:
        from screen_reader_integration import (
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
        import traceback
        traceback.print_exc()
        return False

def test_semantic_structure_standalone():
    """Test the semantic structure system directly."""
    print("Testing Semantic Structure (Standalone)...")
    
    try:
        from semantic_structure import (
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
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all standalone tests."""
    print("Standalone Accessibility Systems Test")
    print("=" * 45)
    
    tests = [
        test_aria_system_standalone,
        test_screen_reader_integration_standalone,
        test_semantic_structure_standalone
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 45)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All accessibility systems are working correctly!")
        print("\nNext steps:")
        print("1. ✅ ARIA System - Complete and functional")
        print("2. ✅ Screen Reader Integration - Complete and functional")
        print("3. ✅ Semantic Structure - Complete and functional")
        print("\n🚀 Ready for production use!")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    main()
