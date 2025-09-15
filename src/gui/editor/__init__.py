#!/usr/bin/env python3
"""
Editor Usability Tools Package.

This package provides comprehensive code editing capabilities including:
- Code completion and suggestions
- Error detection and reporting
- Code formatting and refactoring
- Code navigation and search
"""

from .code_completion import (
    CodeCompletionEngine,
    CompletionType,
    SuggestionPriority,
    Language as CompletionLanguage,
    CodeSuggestion,
    CompletionContext,
    SyntaxToken
)

from .error_detection import (
    ErrorDetectionSystem,
    ErrorSeverity,
    ErrorCategory,
    Language as ErrorLanguage,
    CodeError,
    ErrorContext,
    LintingRule
)

from .code_formatting import (
    CodeFormattingEngine,
    FormattingStyle,
    RefactoringType,
    Language as FormattingLanguage,
    FormattingRule,
    RefactoringOperation,
    FormattingResult
)

from .code_navigation import (
    CodeNavigationEngine,
    SymbolType,
    SearchScope,
    NavigationDirection,
    CodeSymbol,
    SearchResult,
    NavigationContext
)

# Re-export common enums and types
__all__ = [
    # Code Completion
    'CodeCompletionEngine',
    'CompletionType',
    'SuggestionPriority',
    'CodeSuggestion',
    'CompletionContext',
    'SyntaxToken',
    
    # Error Detection
    'ErrorDetectionSystem',
    'ErrorSeverity',
    'ErrorCategory',
    'CodeError',
    'ErrorContext',
    'LintingRule',
    
    # Code Formatting
    'CodeFormattingEngine',
    'FormattingStyle',
    'RefactoringType',
    'FormattingRule',
    'RefactoringOperation',
    'FormattingResult',
    
    # Code Navigation
    'CodeNavigationEngine',
    'SymbolType',
    'SearchScope',
    'NavigationDirection',
    'CodeSymbol',
    'SearchResult',
    'NavigationContext',
    
    # Language enums (aliased to avoid conflicts)
    'CompletionLanguage',
    'ErrorLanguage',
    'FormattingLanguage'
]

# Version information
__version__ = "1.0.0"
__author__ = "Nexlify Engine Team"
__description__ = "Advanced code editing and development tools for the Nexlify engine"
