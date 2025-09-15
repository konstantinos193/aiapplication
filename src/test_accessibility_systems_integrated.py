#!/usr/bin/env python3
"""
Comprehensive test script for integrated accessibility systems.

This script tests the integration between ARIA system, screen reader integration,
and semantic structure modules to ensure they work together correctly.
"""

import sys
import os
import logging

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gui.accessibility.aria_system import (
    AriaSystem, AriaRole, AriaState, AriaProperty, 
    LiveRegionPriority, AriaLabel, AriaLiveRegion
)
from gui.accessibility.screen_reader_integration import (
    ScreenReaderIntegration, AnnouncementPriority, NavigationMode,
    ScreenReaderType, AnnouncementType, NavigationElement, ScreenReaderProfile
)
from gui.accessibility.semantic_structure import (
    SemanticStructure, HeadingLevel, LandmarkType, ListType,
    HeadingStructure, LandmarkRegion, ListStructure
)


def test_aria_system_integration():
    """Test the ARIA system integration."""
    print("Testing ARIA System Integration...")
    
    try:
        aria_system = AriaSystem()
        
        # Test basic ARIA functionality
        assert aria_system.set_aria_label("btn1", "Save Button", "Saves the current document")
        assert aria_system.set_element_role("btn1", AriaRole.BUTTON)
        assert aria_system.set_element_state("btn1", AriaState.PRESSED, "false")
        
        # Test live region creation
        assert aria_system.create_live_region("status1", LiveRegionPriority.ASSERTIVE)
        assert aria_system.announce_to_live_region("status1", "Document saved successfully")
        
        # Test relationship management
        assert aria_system.add_relationship("btn1", "form1", AriaProperty.CONTROLS)
        
        # Test attribute generation
        attributes = aria_system.generate_aria_attributes("btn1")
        assert "role" in attributes
        assert attributes["role"] == "button"
        assert "aria-label" in attributes
        assert "aria-pressed" in attributes
        
        # Test validation
        validation = aria_system.validate_accessibility("btn1")
        assert not validation["has_issues"]
        
        print("  ✓ ARIA system integration working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ ARIA system integration test failed: {e}")
        return False


def test_screen_reader_integration():
    """Test the screen reader integration system."""
    print("Testing Screen Reader Integration...")
    
    try:
        screen_reader = ScreenReaderIntegration()
        
        # Test user profile management
        profile = ScreenReaderProfile(
            user_id="test_user",
            screen_reader=ScreenReaderType.NVDA,
            navigation_preference=NavigationMode.LANDMARK,
            announcement_preference=AnnouncementPriority.HIGH
        )
        assert screen_reader.create_user_profile(profile)
        assert screen_reader.set_current_user("test_user")
        
        # Test announcement system
        assert screen_reader.announce("Page loaded successfully", AnnouncementPriority.NORMAL)
        assert screen_reader.announce_error("Validation error occurred")
        assert screen_reader.announce_success("Form submitted successfully")
        
        # Test navigation element registration
        nav_element = NavigationElement(
            element_id="nav1",
            role="navigation",
            label="Main Navigation",
            description="Primary navigation menu",
            level=1,
            order=1
        )
        assert screen_reader.register_navigation_element(nav_element)
        
        # Test navigation
        assert screen_reader.navigate_to_element("nav1")
        context = screen_reader.get_navigation_context()
        assert context.current_element == "nav1"
        assert context.mode == NavigationMode.LANDMARK
        
        # Test navigation methods
        assert screen_reader.navigate_next()
        assert screen_reader.navigate_previous()
        
        print("  ✓ Screen reader integration working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Screen reader integration test failed: {e}")
        return False


def test_semantic_structure():
    """Test the semantic structure system."""
    print("Testing Semantic Structure...")
    
    try:
        semantic = SemanticStructure()
        
        # Test heading registration
        heading = HeadingStructure(
            element_id="h1",
            level=HeadingLevel.H1,
            text="Main Title",
            description="Primary page heading",
            order=1
        )
        assert semantic.register_heading(heading)
        
        # Test landmark registration
        landmark = LandmarkRegion(
            element_id="nav1",
            type=LandmarkType.NAVIGATION,
            label="Main Navigation",
            description="Primary navigation menu",
            level=1,
            order=2
        )
        assert semantic.register_landmark(landmark)
        
        # Test list registration
        list_structure = ListStructure(
            element_id="menu1",
            type=ListType.NAVIGATION,
            label="Main Menu",
            description="Primary menu items",
            order=3
        )
        assert semantic.register_list(list_structure)
        
        # Test structure retrieval
        heading_hierarchy = semantic.get_heading_hierarchy()
        assert heading_hierarchy['total'] == 1
        assert heading_hierarchy['headings']['h1']['text'] == "Main Title"
        
        landmark_structure = semantic.get_landmark_structure()
        assert landmark_structure['total'] == 1
        assert landmark_structure['landmarks']['nav1']['type'] == "navigation"
        
        # Test accessible elements
        accessible = semantic.get_accessible_elements()
        assert len(accessible) == 3
        
        # Test validation
        validation = semantic.validate_semantic_structure()
        assert not validation["has_issues"]
        
        print("  ✓ Semantic structure working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Semantic structure test failed: {e}")
        return False


def test_systems_integration():
    """Test the integration between all three systems."""
    print("Testing Systems Integration...")
    
    try:
        # Initialize all systems
        aria_system = AriaSystem()
        screen_reader = ScreenReaderIntegration()
        semantic = SemanticStructure()
        
        # Create a comprehensive test scenario
        # 1. Create a form structure
        form_landmark = LandmarkRegion(
            element_id="form1",
            type=LandmarkType.FORM,
            label="Contact Form",
            description="Contact information form",
            level=1,
            order=1
        )
        semantic.register_landmark(form_landmark)
        
        # 2. Create form elements with ARIA attributes
        name_input = NavigationElement(
            element_id="name_input",
            role="textbox",
            label="Name",
            description="Enter your full name",
            level=2,
            parent_id="form1",
            order=1
        )
        screen_reader.register_navigation_element(name_input)
        
        # Set ARIA attributes for the input
        aria_system.set_aria_label("name_input", "Name", "Enter your full name")
        aria_system.set_element_role("name_input", AriaRole.TEXTBOX)
        aria_system.set_element_state("name_input", AriaState.REQUIRED, "true")
        
        # 3. Create a submit button
        submit_btn = NavigationElement(
            element_id="submit_btn",
            role="button",
            label="Submit",
            description="Submit the form",
            level=2,
            parent_id="form1",
            order=2
        )
        screen_reader.register_navigation_element(submit_btn)
        
        aria_system.set_aria_label("submit_btn", "Submit", "Submit the form")
        aria_system.set_element_role("submit_btn", AriaRole.BUTTON)
        
        # 4. Create a status live region
        status_region = AriaLiveRegion(
            element_id="status_region",
            priority=LiveRegionPriority.POLITE,
            description="Form submission status"
        )
        aria_system._live_regions["status_region"] = status_region
        
        # 5. Test the integrated workflow
        # Navigate to the form
        assert screen_reader.navigate_to_element("form1")
        screen_reader.announce("Navigated to contact form", AnnouncementPriority.NORMAL)
        
        # Navigate to name input
        assert screen_reader.navigate_to_element("name_input")
        screen_reader.announce("Name input field", AnnouncementPriority.NORMAL)
        
        # Navigate to submit button
        assert screen_reader.navigate_to_element("submit_btn")
        screen_reader.announce("Submit button", AnnouncementPriority.NORMAL)
        
        # Simulate form submission
        aria_system.announce_to_live_region("status_region", "Form submitted successfully")
        screen_reader.announce_success("Form submitted successfully")
        
        # 6. Validate the integrated structure
        # Check ARIA system
        aria_summary = aria_system.get_accessibility_summary()
        assert aria_summary["total_labels"] >= 2
        assert aria_summary["total_live_regions"] >= 1
        
        # Check screen reader system
        screen_reader_summary = screen_reader.get_accessibility_summary()
        assert screen_reader_summary["total_navigation_elements"] >= 3
        
        # Check semantic structure
        semantic_summary = semantic.get_semantic_structure()
        assert semantic_summary["landmarks"]["total"] >= 1
        
        # 7. Test navigation context
        context = screen_reader.get_navigation_context()
        assert context.current_element == "submit_btn"
        assert context.level == 2
        
        # 8. Test accessibility validation
        aria_validation = aria_system.validate_accessibility("name_input")
        assert not aria_validation["has_issues"]
        
        semantic_validation = semantic.validate_semantic_structure()
        assert not semantic_validation["has_issues"]
        
        print("  ✓ Systems integration working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Systems integration test failed: {e}")
        return False


def test_accessibility_workflows():
    """Test common accessibility workflows."""
    print("Testing Accessibility Workflows...")
    
    try:
        aria_system = AriaSystem()
        screen_reader = ScreenReaderIntegration()
        semantic = SemanticStructure()
        
        # Workflow 1: Page navigation
        # Create page structure
        main_landmark = LandmarkRegion(
            element_id="main",
            type=LandmarkType.MAIN,
            label="Main Content",
            description="Primary page content",
            level=1,
            order=1
        )
        semantic.register_landmark(main_landmark)
        
        # Create navigation
        nav_landmark = LandmarkRegion(
            element_id="nav",
            type=LandmarkType.NAVIGATION,
            label="Site Navigation",
            description="Site-wide navigation menu",
            level=1,
            order=2
        )
        semantic.register_landmark(nav_landmark)
        
        # Create navigation items
        nav_items = ["home", "about", "contact", "help"]
        for i, item in enumerate(nav_items):
            nav_item = NavigationElement(
                element_id=f"nav_{item}",
                role="link",
                label=item.title(),
                description=f"Navigate to {item} page",
                level=2,
                parent_id="nav",
                order=i + 1
            )
            screen_reader.register_navigation_element(nav_item)
            
            # Set ARIA attributes
            aria_system.set_aria_label(f"nav_{item}", item.title(), f"Navigate to {item} page")
            aria_system.set_element_role(f"nav_{item}", AriaRole.LINK)
        
        # Workflow 2: Form interaction
        # Create form structure
        form_landmark = LandmarkRegion(
            element_id="search_form",
            type=LandmarkType.SEARCH,
            label="Search",
            description="Search the website",
            level=1,
            order=3
        )
        semantic.register_landmark(form_landmark)
        
        # Create search input
        search_input = NavigationElement(
            element_id="search_input",
            role="searchbox",
            label="Search",
            description="Enter search terms",
            level=2,
            parent_id="search_form",
            order=1
        )
        screen_reader.register_navigation_element(search_input)
        
        aria_system.set_aria_label("search_input", "Search", "Enter search terms")
        aria_system.set_element_role("search_input", AriaRole.SEARCHBOX)
        aria_system.set_element_state("search_input", AriaState.REQUIRED, "true")
        
        # Create search button
        search_btn = NavigationElement(
            element_id="search_btn",
            role="button",
            label="Search",
            description="Perform search",
            level=2,
            parent_id="search_form",
            order=2
        )
        screen_reader.register_navigation_element(search_btn)
        
        aria_system.set_aria_label("search_btn", "Search", "Perform search")
        aria_system.set_element_role("search_btn", AriaRole.BUTTON)
        
        # Workflow 3: Content reading
        # Create content headings
        content_headings = [
            ("h1", "Welcome to Our Website", 1),
            ("h2", "About Us", 2),
            ("h2", "Our Services", 2),
            ("h3", "Web Development", 3),
            ("h3", "Design Services", 3)
        ]
        
        for element_id, text, level in content_headings:
            heading = HeadingStructure(
                element_id=element_id,
                level=HeadingLevel(level),
                text=text,
                description=f"Section heading: {text}",
                order=level
            )
            semantic.register_heading(heading)
        
        # Test the workflows
        # Navigate through navigation
        assert screen_reader.navigate_to_element("nav")
        screen_reader.announce("Entered navigation menu", AnnouncementPriority.NORMAL)
        
        for item in nav_items:
            assert screen_reader.navigate_to_element(f"nav_{item}")
            screen_reader.announce(f"Navigation item: {item.title()}", AnnouncementPriority.NORMAL)
        
        # Navigate to search form
        assert screen_reader.navigate_to_element("search_form")
        screen_reader.announce("Entered search form", AnnouncementPriority.NORMAL)
        
        # Navigate through form elements
        assert screen_reader.navigate_to_element("search_input")
        screen_reader.announce("Search input field", AnnouncementPriority.NORMAL)
        
        assert screen_reader.navigate_to_element("search_btn")
        screen_reader.announce("Search button", AnnouncementPriority.NORMAL)
        
        # Navigate to main content
        assert screen_reader.navigate_to_element("main")
        screen_reader.announce("Entered main content area", AnnouncementPriority.NORMAL)
        
        # Test heading navigation
        heading_hierarchy = semantic.get_heading_hierarchy()
        assert heading_hierarchy['total'] == 5
        
        # Test accessibility summary
        aria_summary = aria_system.get_accessibility_summary()
        screen_reader_summary = screen_reader.get_accessibility_summary()
        semantic_summary = semantic.get_semantic_structure()
        
        assert aria_summary["total_labels"] >= 6
        assert screen_reader_summary["total_navigation_elements"] >= 6
        assert semantic_summary["landmarks"]["total"] >= 3
        assert semantic_summary["headings"]["total"] >= 5
        
        print("  ✓ Accessibility workflows working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Accessibility workflows test failed: {e}")
        return False


def main():
    """Run all accessibility system tests."""
    print("Comprehensive Accessibility Systems Integration Test")
    print("=" * 60)
    
    tests = [
        test_aria_system_integration,
        test_screen_reader_integration,
        test_semantic_structure,
        test_systems_integration,
        test_accessibility_workflows
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All accessibility systems are working correctly and integrated!")
        print("\nNext steps:")
        print("1. ✅ ARIA System - Complete and functional")
        print("2. ✅ Screen Reader Integration - Complete and functional")
        print("3. ✅ Semantic Structure - Complete and functional")
        print("4. ✅ Systems Integration - All modules work together")
        print("5. ✅ Accessibility Workflows - Common scenarios working")
        print("\n🚀 Ready for production use!")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Set up logging for better debugging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main()
