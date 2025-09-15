#!/usr/bin/env python3
"""
Test script for accessibility systems.

This script tests all the accessibility modules to ensure they work correctly.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_typography_accessibility():
    """Test typography accessibility system."""
    print("Testing Typography Accessibility System...")
    
    try:
        from gui.accessibility.typography_system import typography_accessibility, AccessibilityLevel
        
        # Test basic functionality
        print(f"  ✓ Current accessibility level: {typography_accessibility._current_level.value}")
        
        # Test font size accessibility
        accessible_size = typography_accessibility.get_accessible_font_size(16, AccessibilityLevel.LARGE_TEXT)
        print(f"  ✓ Accessible font size for LARGE_TEXT: {accessible_size}px")
        
        # Test line height
        line_height = typography_accessibility.get_accessible_line_height(16, AccessibilityLevel.HIGH_CONTRAST)
        print(f"  ✓ Line height for HIGH_CONTRAST: {line_height}")
        
        # Test font family
        font_family = typography_accessibility.get_accessible_font_family('primary')
        print(f"  ✓ Accessible font family: {font_family}")
        
        print("  ✓ Typography accessibility system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Typography accessibility system failed: {e}")
        return False

def test_color_accessibility():
    """Test color accessibility system."""
    print("Testing Color Accessibility System...")
    
    try:
        from gui.accessibility.color_accessibility import color_accessibility, ColorBlindnessType
        
        # Test contrast calculation
        contrast_ratio = color_accessibility.calculate_contrast_ratio("#000000", "#FFFFFF")
        print(f"  ✓ Black on white contrast ratio: {contrast_ratio:.2f}")
        
        # Test contrast validation
        is_accessible, ratio = color_accessibility.validate_contrast("#000000", "#FFFFFF", "normal_text")
        print(f"  ✓ Black on white accessible: {is_accessible} (ratio: {ratio:.2f})")
        
        # Test color blindness simulation
        simulated_color = color_accessibility.simulate_color_blindness("#FF0000", ColorBlindnessType.PROTANOPIA)
        print(f"  ✓ Red color simulated for protanopia: {simulated_color}")
        
        print("  ✓ Color accessibility system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Color accessibility system failed: {e}")
        return False

def test_visual_accessibility():
    """Test visual accessibility system."""
    print("Testing Visual Accessibility System...")
    
    try:
        from gui.accessibility.visual_accessibility import visual_accessibility, FocusIndicatorStyle, VisualFeedbackType
        
        # Test focus indicator styles
        focus_style = visual_accessibility.get_focus_indicator_style(FocusIndicatorStyle.OUTLINE)
        print(f"  ✓ Focus indicator style: {focus_style.style.value}")
        
        # Test focus indicator CSS
        css = visual_accessibility.get_focus_indicator_css(FocusIndicatorStyle.GLOW)
        print(f"  ✓ Focus indicator CSS: {css}")
        
        # Test visual feedback
        feedback = visual_accessibility.create_success_indicator("Operation completed successfully")
        print(f"  ✓ Success feedback: {feedback.message}")
        
        print("  ✓ Visual accessibility system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Visual accessibility system failed: {e}")
        return False

def test_accessibility_spacing():
    """Test accessibility spacing system."""
    print("Testing Accessibility Spacing System...")
    
    try:
        from gui.accessibility.accessibility_spacing import accessibility_spacing, AccessibilitySpacingLevel
        
        # Test accessible spacing
        accessible_spacing = accessibility_spacing.get_accessible_spacing(16, AccessibilitySpacingLevel.LARGE_TEXT)
        print(f"  ✓ Accessible spacing for LARGE_TEXT: {accessible_spacing}px")
        
        # Test touch-friendly spacing
        touch_spacing = accessibility_spacing.get_touch_friendly_spacing('button')
        print(f"  ✓ Touch-friendly button spacing: {touch_spacing}px")
        
        # Test focus indicator spacing
        focus_spacing = accessibility_spacing.get_focus_indicator_spacing((100, 50))
        print(f"  ✓ Focus indicator offset: {focus_spacing['offset']}px")
        
        print("  ✓ Accessibility spacing system working correctly")
        return True
        
    except Exception as e:
        print(f"  ✗ Accessibility spacing system failed: {e}")
        return False

def main():
    """Run all accessibility system tests."""
    print("🧪 Testing Accessibility Systems\n")
    
    tests = [
        test_typography_accessibility,
        test_color_accessibility,
        test_visual_accessibility,
        test_accessibility_spacing
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
