#!/usr/bin/env python3
"""
Test accessibility modules without logging.
"""

import sys
import os

# Disable logging
import logging
logging.disable(logging.CRITICAL)

# Add the accessibility directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gui', 'accessibility'))

def test_aria_no_logging():
    """Test ARIA without logging."""
    print("Testing ARIA (No Logging)...")
    
    try:
        # Import and test basic functionality
        from aria_system import AriaSystem, AriaRole
        
        print("  Import successful")
        
        # Create instance
        aria = AriaSystem()
        print("  Instance created")
        
        # Test basic operation
        result = aria.set_aria_label("test1", "Test Label")
        print(f"  Set label result: {result}")
        
        print("  ✓ ARIA working without logging")
        return True
        
    except Exception as e:
        print(f"  ✗ ARIA test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run test without logging."""
    print("Accessibility Test (No Logging)")
    print("=" * 30)
    
    test_aria_no_logging()
    
    print("Test completed.")

if __name__ == "__main__":
    main()
