#!/usr/bin/env python3
"""
Basic structure test for accessibility modules.
"""

import os
import sys

print("Starting basic structure test...")

# Check if files exist
accessibility_dir = os.path.join("src", "gui", "accessibility")
print(f"Checking accessibility directory: {accessibility_dir}")

if os.path.exists(accessibility_dir):
    print("✓ Accessibility directory exists")
    
    files = os.listdir(accessibility_dir)
    print(f"Files in directory: {files}")
    
    # Check each file
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(accessibility_dir, file)
            print(f"Checking file: {file}")
            
            # Try to read the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    print(f"  First line: {first_line}")
                    
                    # Count lines
                    f.seek(0)
                    line_count = len(f.readlines())
                    print(f"  Total lines: {line_count}")
                    
            except Exception as e:
                print(f"  Error reading file: {e}")
else:
    print("✗ Accessibility directory not found")

print("Basic structure test completed.")
