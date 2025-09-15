#!/usr/bin/env python3
"""
Comprehensive test for accessibility systems.

This test demonstrates all the accessibility functionality working together.
"""

import sys
import os

# Disable logging to avoid import issues
import logging
logging.disable(logging.CRITICAL)

# Add the accessibility directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gui', 'accessibility'))

def test_comprehensive_aria():
    """Test comprehensive ARIA functionality."""
    print("Testing Comprehensive ARIA System...")
    
    try:
        from aria_system import (
            AriaSystem, AriaRole, AriaState, AriaProperty, LiveRegionPriority
        )
        
        aria = AriaSystem()
        
        # Test comprehensive ARIA setup
        # 1. Button with full ARIA attributes
        aria.set_aria_label("save_btn", "Save Document", "Saves the current document to disk")
        aria.set_element_role("save_btn", AriaRole.BUTTON)
        aria.set_element_state("save_btn", AriaState.PRESSED, "false")
        aria.set_element_state("save_btn", AriaState.DISABLED, "false")
        
        # 2. Form input with validation
        aria.set_aria_label("email_input", "Email Address", "Enter your email address")
        aria.set_element_role("email_input", AriaRole.TEXTBOX)
        aria.set_element_state("email_input", AriaState.REQUIRED, "true")
        aria.set_element_state("email_input", AriaState.INVALID, "false")
        
        # 3. Live region for status updates
        aria.create_live_region("status_region", LiveRegionPriority.POLITE, True, "Status updates")
        
        # 4. Relationships
        aria.add_relationship("save_btn", "document_form", AriaProperty.CONTROLS)
        aria.add_relationship("email_input", "email_help", AriaProperty.DESCRIBEDBY)
        
        # Test attribute generation
        button_attrs = aria.generate_aria_attributes("save_btn")
        input_attrs = aria.generate_aria_attributes("email_input")
        
        assert "role" in button_attrs
        assert button_attrs["role"] == "button"
        assert "aria-label" in button_attrs
        assert "aria-pressed" in button_attrs
        
        assert "role" in input_attrs
        assert input_attrs["role"] == "textbox"
        assert "aria-required" in input_attrs
        
        # Test validation
        button_validation = aria.validate_accessibility("save_btn")
        input_validation = aria.validate_accessibility("email_input")
        
        assert not button_validation["has_issues"]
        assert not input_validation["has_issues"]
        
        # Test live region
        assert aria.announce_to_live_region("status_region", "Document saved successfully")
        
        print("  ✓ Comprehensive ARIA functionality working")
        return True
        
    except Exception as e:
        print(f"  ✗ Comprehensive ARIA test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_comprehensive_screen_reader():
    """Test comprehensive screen reader functionality."""
    print("Testing Comprehensive Screen Reader Integration...")
    
    try:
        from screen_reader_integration import (
            ScreenReaderIntegration, AnnouncementPriority, NavigationMode,
            ScreenReaderType, AnnouncementType, NavigationElement, ScreenReaderProfile
        )
        
        screen_reader = ScreenReaderIntegration()
        
        # 1. Create user profiles
        nvda_profile = ScreenReaderProfile(
            user_id="nvda_user",
            screen_reader=ScreenReaderType.NVDA,
            navigation_preference=NavigationMode.LANDMARK,
            announcement_preference=AnnouncementPriority.HIGH
        )
        
        jaws_profile = ScreenReaderProfile(
            user_id="jaws_user",
            screen_reader=ScreenReaderType.JAWS,
            navigation_preference=NavigationMode.LINEAR,
            announcement_preference=AnnouncementPriority.NORMAL
        )
        
        screen_reader.create_user_profile(nvda_profile)
        screen_reader.create_user_profile(jaws_profile)
        
        # 2. Switch between users
        screen_reader.set_current_user("nvda_user")
        assert screen_reader.get_current_user() == "nvda_user"
        
        # 3. Create navigation structure
        main_nav = NavigationElement(
            element_id="main_nav",
            role="navigation",
            label="Main Navigation",
            description="Primary site navigation",
            level=1,
            order=1
        )
        
        nav_items = []
        for i, item in enumerate(["Home", "About", "Services", "Contact"]):
            nav_item = NavigationElement(
                element_id=f"nav_{item.lower()}",
                role="link",
                label=item,
                description=f"Navigate to {item} page",
                level=2,
                parent_id="main_nav",
                order=i + 1
            )
            nav_items.append(nav_item)
            screen_reader.register_navigation_element(nav_item)
        
        screen_reader.register_navigation_element(main_nav)
        
        # 4. Test navigation
        screen_reader.navigate_to_element("main_nav")
        context = screen_reader.get_navigation_context()
        assert context.current_element == "main_nav"
        
        # Navigate through items
        for item in nav_items:
            screen_reader.navigate_to_element(item.element_id)
            screen_reader.announce(f"Navigated to {item.label}")
        
        # 5. Test announcements
        screen_reader.announce_status("Page loaded successfully")
        screen_reader.announce_error("Form validation failed")
        screen_reader.announce_success("Data saved successfully")
        screen_reader.announce_warning("Session will expire soon")
        
        # 6. Switch to different user
        screen_reader.set_current_user("jaws_user")
        assert screen_reader.get_current_user() == "jaws_user"
        
        # 7. Test different navigation mode
        screen_reader.navigate_to_element("main_nav")
        context = screen_reader.get_navigation_context()
        assert context.mode == NavigationMode.LINEAR
        
        print("  ✓ Comprehensive screen reader functionality working")
        return True
        
    except Exception as e:
        print(f"  ✗ Comprehensive screen reader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_comprehensive_semantic():
    """Test comprehensive semantic structure functionality."""
    print("Testing Comprehensive Semantic Structure...")
    
    try:
        from semantic_structure import (
            SemanticStructure, HeadingLevel, LandmarkType, ListType,
            HeadingStructure, LandmarkRegion, ListStructure
        )
        
        semantic = SemanticStructure()
        
        # 1. Create comprehensive document structure
        # Main heading
        main_heading = HeadingStructure(
            element_id="h1_main",
            level=HeadingLevel.H1,
            text="Welcome to Our Website",
            description="Primary page heading",
            order=1
        )
        semantic.register_heading(main_heading)
        
        # Sub headings
        about_heading = HeadingStructure(
            element_id="h2_about",
            level=HeadingLevel.H2,
            text="About Us",
            description="About section heading",
            parent_id="h1_main",
            order=2
        )
        semantic.register_heading(about_heading)
        
        services_heading = HeadingStructure(
            element_id="h2_services",
            level=HeadingLevel.H2,
            text="Our Services",
            description="Services section heading",
            parent_id="h1_main",
            order=3
        )
        semantic.register_heading(services_heading)
        
        # 2. Create landmark regions
        header_landmark = LandmarkRegion(
            element_id="header",
            type=LandmarkType.BANNER,
            label="Page Header",
            description="Site header with logo and navigation",
            level=1,
            order=1
        )
        semantic.register_landmark(header_landmark)
        
        nav_landmark = LandmarkRegion(
            element_id="nav",
            type=LandmarkType.NAVIGATION,
            label="Main Navigation",
            description="Primary site navigation",
            level=1,
            order=2
        )
        semantic.register_landmark(nav_landmark)
        
        main_landmark = LandmarkRegion(
            element_id="main",
            type=LandmarkType.MAIN,
            label="Main Content",
            description="Primary page content",
            level=1,
            order=3
        )
        semantic.register_landmark(main_landmark)
        
        # 3. Create list structures
        nav_list = ListStructure(
            element_id="nav_list",
            type=ListType.NAVIGATION,
            label="Navigation Menu",
            description="Site navigation menu items",
            order=1
        )
        semantic.register_list(nav_list)
        
        # 4. Test structure retrieval
        heading_hierarchy = semantic.get_heading_hierarchy()
        landmark_structure = semantic.get_landmark_structure()
        
        assert heading_hierarchy['total'] == 3
        assert landmark_structure['total'] == 3
        
        # 5. Test accessible elements
        accessible = semantic.get_accessible_elements()
        assert len(accessible) >= 6  # 3 headings + 3 landmarks
        
        # 6. Test validation
        validation = semantic.validate_semantic_structure()
        assert not validation["has_issues"]
        
        # 7. Test navigation path
        path = semantic.get_navigation_path("h2_about")
        assert "h1_main" in path
        assert "h2_about" in path
        
        print("  ✓ Comprehensive semantic structure functionality working")
        return True
        
    except Exception as e:
        print(f"  ✗ Comprehensive semantic structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_systems_integration():
    """Test all systems working together."""
    print("Testing Systems Integration...")
    
    try:
        # Import all systems
        from aria_system import AriaSystem, AriaRole, AriaState
        from screen_reader_integration import (
            ScreenReaderIntegration, NavigationElement, ScreenReaderProfile, ScreenReaderType
        )
        from semantic_structure import (
            SemanticStructure, HeadingStructure, HeadingLevel, LandmarkRegion, LandmarkType
        )
        
        # Initialize all systems
        aria = AriaSystem()
        screen_reader = ScreenReaderIntegration()
        semantic = SemanticStructure()
        
        # Create a comprehensive web page structure
        
        # 1. Page structure
        page_heading = HeadingStructure(
            element_id="page_title",
            level=HeadingLevel.H1,
            text="Accessibility Demo Page",
            order=1
        )
        semantic.register_heading(page_heading)
        
        # 2. Navigation landmark
        nav_landmark = LandmarkRegion(
            element_id="page_nav",
            type=LandmarkType.NAVIGATION,
            label="Page Navigation",
            order=2
        )
        semantic.register_landmark(nav_landmark)
        
        # 3. Navigation elements
        nav_elements = []
        for i, item in enumerate(["Home", "Demo", "About"]):
            nav_element = NavigationElement(
                element_id=f"nav_{item.lower()}",
                role="link",
                label=item,
                level=1,
                parent_id="page_nav",
                order=i + 1
            )
            nav_elements.append(nav_element)
            screen_reader.register_navigation_element(nav_element)
            
            # Set ARIA attributes
            aria.set_aria_label(f"nav_{item.lower()}", item, f"Navigate to {item}")
            aria.set_element_role(f"nav_{item.lower()}", AriaRole.LINK)
        
        # 4. Main content
        main_landmark = LandmarkRegion(
            element_id="page_main",
            type=LandmarkType.MAIN,
            label="Main Content",
            order=3
        )
        semantic.register_landmark(main_landmark)
        
        # 5. Form elements
        form_heading = HeadingStructure(
            element_id="form_title",
            level=HeadingLevel.H2,
            text="Contact Form",
            parent_id="page_title",
            order=4
        )
        semantic.register_heading(form_heading)
        
        # Form inputs
        name_input = NavigationElement(
            element_id="name_input",
            role="textbox",
            label="Name",
            level=2,
            parent_id="page_main",
            order=5
        )
        screen_reader.register_navigation_element(name_input)
        
        aria.set_aria_label("name_input", "Name", "Enter your full name")
        aria.set_element_role("name_input", AriaRole.TEXTBOX)
        aria.set_element_state("name_input", AriaState.REQUIRED, "true")
        
        # 6. Test integrated workflow
        # Navigate to navigation
        screen_reader.navigate_to_element("page_nav")
        screen_reader.announce("Entered navigation menu")
        
        # Navigate through nav items
        for nav_element in nav_elements:
            screen_reader.navigate_to_element(nav_element.element_id)
            screen_reader.announce(f"Navigation item: {nav_element.label}")
        
        # Navigate to main content
        screen_reader.navigate_to_element("page_main")
        screen_reader.announce("Entered main content area")
        
        # Navigate to form
        screen_reader.navigate_to_element("name_input")
        screen_reader.announce("Name input field")
        
        # 7. Validate all systems
        aria_summary = aria.get_accessibility_summary()
        screen_reader_summary = screen_reader.get_accessibility_summary()
        semantic_summary = semantic.get_semantic_structure()
        
        assert aria_summary["total_labels"] >= 4
        assert screen_reader_summary["total_navigation_elements"] >= 4
        assert semantic_summary["headings"]["total"] >= 2
        assert semantic_summary["landmarks"]["total"] >= 2
        
        print("  ✓ Systems integration working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Systems integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive accessibility tests."""
    print("Comprehensive Accessibility Systems Test")
    print("=" * 55)
    
    tests = [
        test_comprehensive_aria,
        test_comprehensive_screen_reader,
        test_comprehensive_semantic,
        test_systems_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 55)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All accessibility systems are working correctly and integrated!")
        print("\n✅ What's Working:")
        print("1. ARIA System - Complete ARIA role, state, and property management")
        print("2. Screen Reader Integration - User profiles, navigation, announcements")
        print("3. Semantic Structure - Document structure, landmarks, headings")
        print("4. Systems Integration - All modules working together seamlessly")
        print("\n🚀 Ready for production use!")
        print("\nNext steps:")
        print("- Integrate with your GUI system")
        print("- Add real screen reader callbacks")
        print("- Implement accessibility testing tools")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    main()
