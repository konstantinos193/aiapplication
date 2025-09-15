#!/usr/bin/env python3
"""
Direct test script for accessibility systems.

This script tests the accessibility modules directly without package imports.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

def test_typography_accessibility_direct():
    """Test typography accessibility system directly."""
    print("Testing Typography Accessibility System (Direct)...")
    
    try:
        # Import the module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "typography_accessibility", 
            "gui/accessibility/typography_system.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test basic functionality
        ta = module.TypographyAccessibility()
        print(f"  ✓ Typography accessibility system created successfully")
        print(f"  ✓ Current level: {ta._current_level.value}")
        
        # Test font size accessibility
        accessible_size = ta.get_accessible_font_size(16, module.AccessibilityLevel.LARGE_TEXT)
        print(f"  ✓ Accessible font size for LARGE_TEXT: {accessible_size}px")
        
        print("  ✓ Typography accessibility system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Typography accessibility system failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_color_accessibility_direct():
    """Test color accessibility system directly."""
    print("Testing Color Accessibility System (Direct)...")
    
    try:
        # Import the module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "color_accessibility", 
            "gui/accessibility/color_accessibility.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test basic functionality
        ca = module.ColorAccessibility()
        print(f"  ✓ Color accessibility system created successfully")
        
        # Test contrast calculation
        contrast_ratio = ca.calculate_contrast_ratio("#000000", "#FFFFFF")
        print(f"  ✓ Black on white contrast ratio: {contrast_ratio:.2f}")
        
        print("  ✓ Color accessibility system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Color accessibility system failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_visual_accessibility_direct():
    """Test visual accessibility system directly."""
    print("Testing Visual Accessibility System (Direct)...")
    
    try:
        # Import the module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "visual_accessibility", 
            "gui/accessibility/visual_accessibility.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test basic functionality
        va = module.VisualAccessibility()
        print(f"  ✓ Visual accessibility system created successfully")
        
        # Test focus indicator styles
        focus_style = va.get_focus_indicator_style(module.FocusIndicatorStyle.OUTLINE)
        print(f"  ✓ Focus indicator style: {focus_style.style.value}")
        
        print("  ✓ Visual accessibility system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Visual accessibility system failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_accessibility_spacing_direct():
    """Test accessibility spacing system directly."""
    print("Testing Accessibility Spacing System (Direct)...")
    
    try:
        # Import the module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "accessibility_spacing", 
            "gui/accessibility/accessibility_spacing.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test basic functionality
        asys = module.AccessibilitySpacing()
        print(f"  ✓ Accessibility spacing system created successfully")
        
        # Test accessible spacing
        accessible_spacing = asys.get_accessible_spacing(16, module.AccessibilitySpacingLevel.LARGE_TEXT)
        print(f"  ✓ Accessible spacing for LARGE_TEXT: {accessible_spacing}px")
        
        print("  ✓ Accessibility spacing system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Accessibility spacing system failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all accessibility system tests."""
    print("🧪 Testing Accessibility Systems (Direct Import)\n")
    
    tests = [
        test_typography_accessibility_direct,
        test_color_accessibility_direct,
        test_visual_accessibility_direct,
        test_accessibility_spacing_direct
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All accessibility systems are working correctly!")
        return 0
    else:
        print("❌ Some accessibility systems have issues that need to be fixed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
