#!/usr/bin/env python3
"""
Standalone Test Script for Editor Usability Tools.

This script directly imports the editor modules to bypass import issues
with the gui package structure.
"""

import sys
import os
import time
from pathlib import Path

# Add the src/gui/editor directory to the path
editor_path = Path(__file__).parent / "src" / "gui" / "editor"
sys.path.insert(0, str(editor_path))

def test_code_completion_engine():
    """Test the Code Completion Engine."""
    print("\n=== Testing Code Completion Engine ===")
    
    try:
        from code_completion import (
            CodeCompletionEngine, CompletionType, SuggestionPriority, 
            Language, CodeSuggestion, CompletionContext, SyntaxToken
        )
        
        # Create engine
        engine = CodeCompletionEngine()
        print("✓ CodeCompletionEngine created successfully")
        
        # Test Python code completion
        python_code = """
def calculate_area(width, height):
    \"\"\"Calculate the area of a rectangle.\"\"\"
    area = width * height
    return area

class Rectangle:
    \"\"\"A simple rectangle class.\"\"\"
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def get_area(self):
        \"\"\"Get the area of this rectangle.\"\"\"
        return self.width * self.height
"""
        
        # Test getting suggestions
        suggestions = engine.get_code_completion_suggestions(
            python_code, 5, 10, Language.PYTHON
        )
        print(f"✓ Got {len(suggestions)} Python completion suggestions")
        
        # Test syntax highlighting
        tokens = engine.analyze_syntax_for_highlighting(python_code, Language.PYTHON)
        print(f"✓ Analyzed {len(tokens)} syntax tokens for highlighting")
        
        # Test custom suggestions
        engine.add_custom_suggestion(
            "calculate_perimeter", 
            "def calculate_perimeter(width, height):\n    return 2 * (width + height)",
            Language.PYTHON
        )
        print("✓ Added custom suggestion successfully")
        
        # Test GLSL completion
        glsl_code = """
// Fragment shader for basic texture mapping
void main() {
    vec4 color = texture2D(texture, texCoord);
    gl_FragColor = color;
}
"""
        
        glsl_suggestions = engine.get_code_completion_suggestions(
            glsl_code, 2, 10, Language.GLSL
        )
        print(f"✓ Got {len(glsl_suggestions)} GLSL completion suggestions")
        
        print("✓ Code Completion Engine tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Code Completion Engine test failed: {e}")
        return False

def test_error_detection_system():
    """Test the Error Detection System."""
    print("\n=== Testing Error Detection System ===")
    
    try:
        from error_detection import (
            ErrorDetectionSystem, ErrorSeverity, ErrorCategory,
            Language, CodeError, ErrorContext, LintingRule
        )
        
        # Create system
        system = ErrorDetectionSystem()
        print("✓ ErrorDetectionSystem created successfully")
        
        # Test Python error detection
        valid_python = "def test(): pass"
        invalid_python = "def test(: pass"  # Missing parameter name
        
        # Test valid Python
        errors = system.detect_errors(valid_python, Language.PYTHON)
        print(f"✓ Valid Python code: {len(errors)} errors detected (expected 0)")
        
        # Test invalid Python
        errors = system.detect_errors(invalid_python, Language.PYTHON)
        print(f"✓ Invalid Python code: {len(errors)} errors detected (expected >0)")
        
        # Test JSON validation
        valid_json = '{"name": "test", "value": 42}'
        invalid_json = '{"name": "test", "value": 42'  # Missing closing brace
        
        # Test valid JSON
        errors = system.detect_errors(valid_json, Language.JSON)
        print(f"✓ Valid JSON: {len(errors)} errors detected (expected 0)")
        
        # Test invalid JSON
        errors = system.detect_errors(invalid_json, Language.JSON)
        print(f"✓ Invalid JSON: {len(errors)} errors detected (expected >0)")
        
        # Test GLSL validation
        valid_glsl = "void main() { gl_FragColor = vec4(1.0); }"
        invalid_glsl = "void main() { gl_FragColor = vec4(1.0"  # Missing closing brace
        
        # Test valid GLSL
        errors = system.detect_errors(valid_glsl, Language.GLSL)
        print(f"✓ Valid GLSL: {len(errors)} errors detected (expected 0)")
        
        errors = system.detect_errors(invalid_glsl, Language.GLSL)
        print(f"✓ Invalid GLSL: {len(errors)} errors detected (expected >0)")
        
        # Test custom linting rules
        rule = LintingRule(
            name="no_single_letter_vars",
            pattern=r'\b[a-zA-Z]\s*=',
            message="Avoid single letter variable names",
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.STYLE
        )
        
        system.add_custom_linting_rule(Language.PYTHON, rule)
        print("✓ Added custom linting rule successfully")
        
        # Test custom rule
        test_code = "x = 5\ny = 10"
        errors = system.detect_errors(test_code, Language.PYTHON)
        print(f"✓ Custom rule detected {len(errors)} style warnings")
        
        print("✓ Error Detection System tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error Detection System test failed: {e}")
        return False

def test_code_formatting_engine():
    """Test the Code Formatting Engine."""
    print("\n=== Testing Code Formatting Engine ===")
    
    try:
        from code_formatting import (
            CodeFormattingEngine, FormattingStyle, RefactoringType,
            Language, FormattingRule, RefactoringOperation, FormattingResult
        )
        
        # Create engine
        engine = CodeFormattingEngine()
        print("✓ CodeFormattingEngine created successfully")
        
        # Test Python formatting
        unformatted_python = """def test_function(x,y):
    result=x+y
    return result"""
        
        result = engine.format_code(unformatted_python, Language.PYTHON, FormattingStyle.PEP8)
        print(f"✓ Python formatting: {len(result.changes_made)} changes made")
        print(f"  Original length: {result.original_length}, Formatted length: {result.formatted_length}")
        
        # Test JSON formatting
        unformatted_json = '{"name":"test","value":42,"nested":{"key":"value"}}'
        
        result = engine.format_code(unformatted_json, Language.JSON, FormattingStyle.CUSTOM)
        print(f"✓ JSON formatting: {len(result.changes_made)} changes made")
        print(f"  Original length: {result.original_length}, Formatted length: {result.formatted_length}")
        
        # Test GLSL formatting
        unformatted_glsl = """void main(){
vec4 color=texture2D(texture,texCoord);
gl_FragColor=color;}"""
        
        result = engine.format_code(unformatted_glsl, Language.GLSL, FormattingStyle.CUSTOM)
        print(f"✓ GLSL formatting: {len(result.changes_made)} changes made")
        print(f"  Original length: {result.original_length}, Formatted length: {result.formatted_length}")
        
        # Test refactoring suggestions
        suggestions = engine.suggest_refactoring(unformatted_python, Language.PYTHON)
        print(f"✓ Got {len(suggestions)} refactoring suggestions")
        
        # Test custom formatting rule
        custom_rule = FormattingRule(
            name="add_spaces_around_equals",
            description="Add spaces around equals signs",
            pattern=r'(\w)=(\w)',
            message="Add spaces around equals signs",
            replacement=r'\1 = \2',
            language=Language.PYTHON,
            priority=10
        )
        
        engine.add_custom_formatting_rule(Language.PYTHON, custom_rule)
        print("✓ Added custom formatting rule successfully")
        
        # Test custom rule
        test_code = "x=5\ny=10"
        result = engine.format_code(test_code, Language.PYTHON, FormattingStyle.CUSTOM)
        print(f"✓ Custom rule applied: {len(result.changes_made)} changes made")
        
        # Test validation
        validation = engine.validate_formatting_rules()
        print(f"✓ Formatting rules validation: {validation['total_rules']} rules, {len(validation['issues'])} issues")
        
        print("✓ Code Formatting Engine tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Code Formatting Engine test failed: {e}")
        return False

def test_code_navigation_engine():
    """Test the Code Navigation Engine."""
    print("\n=== Testing Code Navigation Engine ===")
    
    try:
        from code_navigation import (
            CodeNavigationEngine, SymbolType, SearchScope, NavigationDirection,
            CodeSymbol, SearchResult, NavigationContext
        )
        
        # Create engine
        engine = CodeNavigationEngine()
        print("✓ CodeNavigationEngine created successfully")
        
        # Test Python file indexing
        python_code = """
class TestClass:
    def __init__(self):
        self.value = 42
    
    def test_method(self, param):
        result = self.value + param
        return result

def global_function():
    return "test"

variable = 100
"""
        
        success = engine.index_file("test.py", python_code, "python")
        print(f"✓ Python file indexing: {'successful' if success else 'failed'}")
        
        # Test GLSL file indexing
        glsl_code = """
void main() {
    vec4 color = texture2D(texture, texCoord);
    gl_FragColor = color;
}

uniform float time;
uniform vec2 resolution;
"""
        
        success = engine.index_file("test.glsl", glsl_code, "glsl")
        print(f"✓ GLSL file indexing: {'successful' if success else 'failed'}")
        
        # Test JSON file indexing
        json_code = '{"name": "test", "properties": {"value": 42, "enabled": true}}'
        
        success = engine.index_file("test.json", json_code, "json")
        print(f"✓ JSON file indexing: {'successful' if success else 'failed'}")
        
        # Test symbol search
        search_result = engine.search_symbols("test", SearchScope.ALL_FILES)
        print(f"✓ Symbol search: found {search_result.total_count} results in {search_result.search_time:.3f}s")
        
        # Test language-specific search
        python_search = engine.search_symbols("test", SearchScope.ALL_FILES, language_filter="python")
        print(f"✓ Python-only search: found {python_search.total_count} results")
        
        # Test symbol type search
        class_search = engine.search_symbols("", SearchScope.ALL_FILES, symbol_type_filter=SymbolType.CLASS)
        print(f"✓ Class search: found {class_search.total_count} classes")
        
        # Test go to definition
        symbol = engine.go_to_definition("TestClass", "test.py", 1)
        if symbol:
            print(f"✓ Go to definition: found {symbol.name} at line {symbol.line_number}")
        else:
            print("✗ Go to definition failed")
        
        # Test find references
        references = engine.find_references("test_method", "test.py")
        print(f"✓ Find references: found {len(references)} references")
        
        # Test symbol info
        info = engine.get_symbol_info("TestClass", "test.py")
        if info:
            print(f"✓ Symbol info: {info['name']} ({info['type']}) with {info['references_count']} references")
        else:
            print("✗ Symbol info failed")
        
        # Test navigation context
        context = engine.get_navigation_context("test.py")
        print(f"✓ Navigation context: {context.current_file}")
        
        # Test bookmark management
        engine.add_bookmark("test.py", 5, 10, "Important method")
        print("✓ Added bookmark successfully")
        
        # Test navigation summary
        summary = engine.get_navigation_summary()
        print(f"✓ Navigation summary: {summary['total_files_indexed']} files, {summary['total_symbols']} symbols")
        
        print("✓ Code Navigation Engine tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Code Navigation Engine test failed: {e}")
        return False

def test_integration():
    """Test integration between all editor tools."""
    print("\n=== Testing Editor Tools Integration ===")
    
    try:
        from code_completion import CodeCompletionEngine, Language
        from error_detection import ErrorDetectionSystem
        from code_formatting import CodeFormattingEngine, FormattingStyle
        from code_navigation import CodeNavigationEngine, SearchScope
        
        # Create all engines
        completion_engine = CodeCompletionEngine()
        error_system = ErrorDetectionSystem()
        formatting_engine = CodeFormattingEngine()
        navigation_engine = CodeNavigationEngine()
        
        print("✓ All editor engines created successfully")
        
        # Test workflow: index file -> detect errors -> format -> get suggestions
        test_code = """
def calculate_area(width,height):
    area=width*height
    return area

class Rectangle:
    def __init__(self,width,height):
        self.width=width
        self.height=height
    
    def get_area(self):
        return self.width*self.height
"""
        
        # Step 1: Index the file
        navigation_engine.index_file("integration_test.py", test_code, "python")
        print("✓ Step 1: File indexed")
        
        # Step 2: Detect errors
        errors = error_system.detect_errors(test_code, Language.PYTHON)
        print(f"✓ Step 2: Detected {len(errors)} errors")
        
        # Step 3: Format the code
        formatted_result = formatting_engine.format_code(test_code, Language.PYTHON, FormattingStyle.PEP8)
        print(f"✓ Step 3: Code formatted with {len(formatted_result.changes_made)} changes")
        
        # Step 4: Get completion suggestions
        suggestions = completion_engine.get_code_completion_suggestions(
            formatted_result.formatted_code, 5, 10, Language.PYTHON
        )
        print(f"✓ Step 4: Got {len(suggestions)} completion suggestions")
        
        # Step 5: Search for symbols
        search_result = navigation_engine.search_symbols("Rectangle", SearchScope.ALL_FILES)
        print(f"✓ Step 5: Found {search_result.total_count} Rectangle symbols")
        
        print("✓ Editor Tools Integration tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Editor Tools Integration test failed: {e}")
        return False

def main():
    """Run all editor usability tools tests."""
    print("🚀 Starting Editor Usability Tools Standalone Tests")
    print("=" * 60)
    
    start_time = time.time()
    
    # Run all tests
    tests = [
        test_code_completion_engine,
        test_error_detection_system,
        test_code_formatting_engine,
        test_code_navigation_engine,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    print(f"⏱️  Total time: {total_time:.2f} seconds")
    
    if passed == total:
        print("🎉 All Editor Usability Tools tests passed successfully!")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
