#!/usr/bin/env python3
"""
Error Detection and Reporting System for Editor Usability Tools.

This module provides real-time error checking, linting, and detailed
error reporting for multiple programming languages.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple, Union, Any
import logging
import re
import ast
import json
from threading import Lock
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    ERROR = "error"        # Critical errors that prevent execution
    WARNING = "warning"    # Issues that may cause problems
    INFO = "info"          # Informational messages
    HINT = "hint"          # Suggestions for improvement


class ErrorCategory(Enum):
    """Categories of errors."""
    SYNTAX = "syntax"           # Syntax errors
    SEMANTIC = "semantic"       # Semantic errors
    STYLE = "style"             # Code style issues
    PERFORMANCE = "performance" # Performance warnings
    SECURITY = "security"       # Security vulnerabilities
    ACCESSIBILITY = "accessibility" # Accessibility issues
    LINTING = "linting"         # Linting violations


class Language(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    GLSL = "glsl"
    HLSL = "hlsl"
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    MARKDOWN = "markdown"
    CPP = "cpp"
    RUST = "rust"


@dataclass(frozen=True)
class CodeError:
    """Represents a code error or warning."""
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    line_number: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    file_path: str = ""
    language: Language = Language.PYTHON
    code: str = ""
    suggestion: str = ""
    documentation: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class ErrorContext:
    """Context information for error detection."""
    file_path: str
    language: Language
    code: str
    line_number: int
    column: int
    scope: str = "global"
    in_string: bool = False
    in_comment: bool = False
    in_function: bool = False
    in_class: bool = False


@dataclass(frozen=True)
class LintingRule:
    """Represents a linting rule."""
    name: str
    description: str
    severity: ErrorSeverity
    category: ErrorCategory
    pattern: str
    message: str
    suggestion: str = ""
    enabled: bool = True


class ErrorDetectionSystem:
    """
    Comprehensive error detection and reporting system.
    
    This class provides real-time error checking, linting, and detailed
    error reporting for multiple programming languages.
    """
    
    def __init__(self):
        self._linting_rules: Dict[Language, List[LintingRule]] = {}
        self._error_patterns: Dict[Language, Dict[str, str]] = {}
        self._custom_rules: Dict[Language, List[LintingRule]] = {}
        self._lock = Lock()
        self._logger = logging.getLogger(f"{__name__}.ErrorDetectionSystem")
        
        # Initialize language-specific error detection
        self._setup_languages()
        self._logger.info("ErrorDetectionSystem initialized")
    
    def _setup_languages(self):
        """Setup language-specific error detection rules."""
        # Python language setup
        self._setup_python_error_detection()
        
        # GLSL language setup
        self._setup_glsl_error_detection()
        
        # JSON language setup
        self._setup_json_error_detection()
    
    def _setup_python_error_detection(self):
        """Setup Python-specific error detection."""
        python = Language.PYTHON
        
        # Python linting rules
        python_rules = [
            LintingRule(
                name="unused_import",
                description="Unused import statement",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.STYLE,
                pattern=r'^import\s+(\w+)(?:\s+as\s+\w+)?$',
                message="Unused import: {match}",
                suggestion="Remove unused import or use it in your code"
            ),
            LintingRule(
                name="unused_variable",
                description="Unused variable",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.STYLE,
                pattern=r'^\s*(\w+)\s*=\s*[^#\n]+$',
                message="Unused variable: {match}",
                suggestion="Use the variable or prefix with underscore (_)"
            ),
            LintingRule(
                name="missing_docstring",
                description="Missing function/class docstring",
                severity=ErrorSeverity.INFO,
                category=ErrorCategory.STYLE,
                pattern=r'^(?:def|class)\s+(\w+)',
                message="Missing docstring for: {match}",
                suggestion="Add a docstring describing the purpose"
            ),
            LintingRule(
                name="line_too_long",
                description="Line exceeds maximum length",
                severity=ErrorSeverity.INFO,
                category=ErrorCategory.STYLE,
                pattern=r'^.{79,}$',
                message="Line too long ({length} characters)",
                suggestion="Break long lines or use line continuation"
            ),
            LintingRule(
                name="trailing_whitespace",
                description="Trailing whitespace",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.STYLE,
                pattern=r'[ \t]+$',
                message="Trailing whitespace detected",
                suggestion="Remove trailing whitespace"
            )
        ]
        
        self._linting_rules[python] = python_rules
        
        # Python error patterns
        self._error_patterns[python] = {
            'syntax_error': r'(SyntaxError|IndentationError|TabError)',
            'name_error': r'(NameError|UnboundLocalError)',
            'type_error': r'(TypeError|AttributeError)',
            'value_error': r'(ValueError|KeyError|IndexError)',
            'import_error': r'(ImportError|ModuleNotFoundError)',
            'runtime_error': r'(RuntimeError|RecursionError)'
        }
    
    def _setup_glsl_error_detection(self):
        """Setup GLSL-specific error detection."""
        glsl = Language.GLSL
        
        # GLSL linting rules
        glsl_rules = [
            LintingRule(
                name="unused_uniform",
                description="Unused uniform variable",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.STYLE,
                pattern=r'uniform\s+\w+\s+(\w+)',
                message="Unused uniform: {match}",
                suggestion="Use the uniform or remove it"
            ),
            LintingRule(
                name="missing_precision",
                description="Missing precision qualifier",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.STYLE,
                pattern=r'^(?!precision).*float\s+\w+',
                message="Missing precision qualifier",
                suggestion="Add precision qualifier (lowp, mediump, highp)"
            ),
            LintingRule(
                name="unused_varying",
                description="Unused varying variable",
                severity=ErrorSeverity.WARNING,
                category=ErrorCategory.STYLE,
                pattern=r'varying\s+\w+\s+(\w+)',
                message="Unused varying: {match}",
                suggestion="Use the varying or remove it"
            )
        ]
        
        self._linting_rules[glsl] = glsl_rules
        
        # GLSL error patterns
        self._error_patterns[glsl] = {
            'syntax_error': r'(syntax error|unexpected token)',
            'type_error': r'(type mismatch|incompatible types)',
            'variable_error': r'(undefined variable|undeclared identifier)',
            'function_error': r'(undefined function|function not found)'
        }
    
    def _setup_json_error_detection(self):
        """Setup JSON-specific error detection."""
        json = Language.JSON
        
        # JSON linting rules
        json_rules = [
            LintingRule(
                name="trailing_comma",
                description="Trailing comma in JSON",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.SYNTAX,
                pattern=r',\s*}',
                message="Trailing comma not allowed in JSON",
                suggestion="Remove trailing comma"
            ),
            LintingRule(
                name="missing_quotes",
                description="Missing quotes around property names",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.SYNTAX,
                pattern=r'(\w+):',
                message="Property names must be quoted in JSON",
                suggestion="Add quotes around property names"
            )
        ]
        
        self._linting_rules[json] = json_rules
        
        # JSON error patterns
        self._error_patterns[json] = {
            'syntax_error': r'(JSONDecodeError|Invalid JSON)',
            'parse_error': r'(parse error|unexpected token)'
        }
    
    def detect_errors(self, code: str, language: Language) -> List[CodeError]:
        """
        Detect errors in the given code.
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            List of detected errors
        """
        try:
            with self._lock:
                # Create error context
                context = ErrorContext(
                    code=code,
                    language=language,
                    file_path="",
                    line_number=1,
                    column_number=1
                )
                
                errors = []
                
                # Language-specific syntax validation
                if language == Language.PYTHON:
                    errors.extend(self._validate_python_syntax(context))
                elif language == Language.JSON:
                    errors.extend(self._validate_json_syntax(context))
                elif language == Language.GLSL:
                    errors.extend(self._validate_glsl_syntax(context))
                
                # Apply linting rules
                errors.extend(self._apply_linting_rules(context))
                
                # Sort errors by severity and line number
                errors.sort(key=lambda e: (
                    e.severity.value == ErrorSeverity.ERROR.value,
                    e.line_number,
                    e.column
                ), reverse=True)
                
                return errors
                
        except Exception as e:
            self._logger.error(f"Failed to detect errors: {e}")
            return []
    
    def _validate_python_syntax(self, context: ErrorContext) -> List[CodeError]:
        """Validate Python syntax using ast module."""
        errors = []
        
        try:
            # Parse the code to check for syntax errors
            ast.parse(context.code)
        except SyntaxError as e:
            error = CodeError(
                message=f"Syntax Error: {str(e)}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.SYNTAX,
                line_number=e.lineno or context.line_number,
                column=e.offset or context.column,
                file_path=context.file_path,
                language=context.language,
                code=context.code,
                suggestion="Fix the syntax error and try again"
            )
            errors.append(error)
        except Exception as e:
            # Other parsing errors
            error = CodeError(
                message=f"Parsing Error: {str(e)}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.SYNTAX,
                line_number=context.line_number,
                column=context.column,
                file_path=context.file_path,
                language=context.language,
                code=context.code,
                suggestion="Check the code structure and syntax"
            )
            errors.append(error)
        
        return errors
    
    def _validate_json_syntax(self, context: ErrorContext) -> List[CodeError]:
        """Validate JSON syntax."""
        errors = []
        
        try:
            json.loads(context.code)
        except json.JSONDecodeError as e:
            error = CodeError(
                message=f"JSON Error: {str(e)}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.SYNTAX,
                line_number=context.line_number,
                column=context.column,
                file_path=context.file_path,
                language=context.language,
                code=context.code,
                suggestion="Fix the JSON syntax error"
            )
            errors.append(error)
        
        return errors
    
    def _validate_glsl_syntax(self, context: ErrorContext) -> List[CodeError]:
        """Validate GLSL syntax (basic validation)."""
        errors = []
        
        # Basic GLSL validation patterns
        glsl_patterns = {
            'missing_main': r'(?<!void\s+)main\s*\([^)]*\)',
            'invalid_precision': r'precision\s+(?!lowp|mediump|highp)\w+',
            'invalid_type': r'\b(?!float|int|bool|vec[234]|mat[234]|sampler2D)\w+\s+\w+'
        }
        
        for pattern_name, pattern in glsl_patterns.items():
            matches = re.finditer(pattern, context.code, re.IGNORECASE)
            for match in matches:
                line_num = context.code[:match.start()].count('\n') + 1
                error = CodeError(
                    message=f"GLSL {pattern_name.replace('_', ' ').title()}: {match.group()}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.STYLE,
                    line_number=line_num,
                    column=match.start() - context.code.rfind('\n', 0, match.start()) - 1,
                    file_path=context.file_path,
                    language=context.language,
                    code=context.code,
                    suggestion="Check GLSL syntax and type declarations"
                )
                errors.append(error)
        
        return errors
    
    def _apply_linting_rules(self, context: ErrorContext) -> List[CodeError]:
        """Apply linting rules to the code."""
        errors = []
        
        if context.language not in self._linting_rules:
            return errors
        
        rules = self._linting_rules[context.language]
        
        for line_num, line in enumerate(context.code.split('\n'), 1):
            for rule in rules:
                if not rule.enabled:
                    continue
                
                matches = re.finditer(rule.pattern, line, re.IGNORECASE)
                for match in matches:
                    # Check if we're in a comment or string
                    if self._is_in_comment_or_string(line, match.start()):
                        continue
                    
                    error = CodeError(
                        message=rule.message.format(match=match.group()),
                        severity=rule.severity,
                        category=rule.category,
                        line_number=line_num,
                        column=match.start(),
                        end_line=line_num,
                        end_column=match.end(),
                        file_path=context.file_path,
                        language=context.language,
                        code=line,
                        suggestion=rule.suggestion
                    )
                    errors.append(error)
        
        return errors
    
    def _is_in_comment_or_string(self, line: str, position: int) -> bool:
        """Check if a position is inside a comment or string."""
        # Simple check for Python comments
        comment_pos = line.find('#')
        if comment_pos != -1 and position > comment_pos:
            return True
        
        # Check for string literals (simplified)
        in_string = False
        quote_char = None
        
        for i, char in enumerate(line[:position]):
            if char in '"\'':
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char:
                    in_string = False
                    quote_char = None
        
        return in_string
    
    def add_custom_linting_rule(self, language: Language, rule: LintingRule) -> bool:
        """
        Add a custom linting rule.
        
        Args:
            language: Programming language
            rule: Linting rule to add
            
        Returns:
            True if rule was added successfully, False otherwise
        """
        try:
            with self._lock:
                if language not in self._custom_rules:
                    self._custom_rules[language] = []
                
                self._custom_rules[language].append(rule)
                
                # Also add to main linting rules
                if language not in self._linting_rules:
                    self._linting_rules[language] = []
                
                self._linting_rules[language].append(rule)
                
                self._logger.debug(f"Added custom linting rule for {language.value}: {rule.name}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to add custom linting rule: {e}")
            return False
    
    def get_error_summary(self, errors: List[CodeError]) -> Dict[str, Any]:
        """
        Get a summary of detected errors.
        
        Args:
            errors: List of detected errors
            
        Returns:
            Error summary dictionary
        """
        if not errors:
            return {"total_errors": 0, "has_errors": False}
        
        summary = {
            "total_errors": len(errors),
            "has_errors": True,
            "errors_by_severity": {},
            "errors_by_category": {},
            "errors_by_language": {},
            "most_common_errors": [],
            "file_paths": list(set(e.file_path for e in errors if e.file_path))
        }
        
        # Count by severity
        for error in errors:
            severity = error.severity.value
            summary["errors_by_severity"][severity] = summary["errors_by_severity"].get(severity, 0) + 1
        
        # Count by category
        for error in errors:
            category = error.category.value
            summary["errors_by_category"][category] = summary["errors_by_category"].get(category, 0) + 1
        
        # Count by language
        for error in errors:
            language = error.language.value
            summary["errors_by_language"][language] = summary["errors_by_language"].get(language, 0) + 1
        
        # Most common error messages
        error_messages = [e.message for e in errors]
        message_counts = {}
        for msg in error_messages:
            message_counts[msg] = message_counts.get(msg, 0) + 1
        
        summary["most_common_errors"] = sorted(
            message_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return summary
    
    def get_linting_rules_summary(self) -> Dict[str, Any]:
        """Get a summary of all linting rules."""
        return {
            "total_languages": len(self._linting_rules),
            "languages": list(lang.value for lang in self._linting_rules.keys()),
            "rules_by_language": {
                lang.value: len(rules) for lang, rules in self._linting_rules.items()
            },
            "total_custom_rules": sum(len(rules) for rules in self._custom_rules.values()),
            "custom_rules_by_language": {
                lang.value: len(rules) for lang, rules in self._custom_rules.items()
            }
        }
    
    def validate_linting_rules(self) -> Dict[str, Any]:
        """Validate linting rules for consistency issues."""
        issues = []
        warnings = []
        
        for language, rules in self._linting_rules.items():
            # Check for duplicate rule names
            rule_names = [rule.name for rule in rules]
            duplicates = set([name for name in rule_names if rule_names.count(name) > 1])
            
            if duplicates:
                warnings.append(f"Duplicate rule names in {language.value}: {list(duplicates)}")
            
            # Check for invalid regex patterns
            for rule in rules:
                try:
                    re.compile(rule.pattern)
                except re.error as e:
                    issues.append(f"Invalid regex pattern in {language.value} rule '{rule.name}': {e}")
            
            # Check for empty messages
            empty_messages = [rule.name for rule in rules if not rule.message]
            if empty_messages:
                warnings.append(f"Rules without messages in {language.value}: {empty_messages}")
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues,
            "warnings": warnings,
            "total_languages": len(self._linting_rules),
            "total_rules": sum(len(rules) for rules in self._linting_rules.values())
        }
