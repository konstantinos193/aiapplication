#!/usr/bin/env python3
"""
Code Formatting and Refactoring Tools for Editor Usability Tools.

This module provides automatic code cleanup, formatting, and refactoring
capabilities for multiple programming languages.
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


class FormattingStyle(Enum):
    """Code formatting styles."""
    PEP8 = "pep8"           # Python PEP 8 style
    BLACK = "black"          # Black formatter style
    GOOGLE = "google"        # Google style guide
    CUSTOM = "custom"        # Custom formatting rules


class RefactoringType(Enum):
    """Types of refactoring operations."""
    EXTRACT_METHOD = "extract_method"
    EXTRACT_VARIABLE = "extract_variable"
    RENAME = "rename"
    INLINE = "inline"
    MOVE = "move"
    SPLIT = "split"
    MERGE = "merge"
    REORDER = "reorder"


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
class FormattingRule:
    """Represents a code formatting rule."""
    name: str
    description: str
    pattern: str
    replacement: str
    enabled: bool = True
    priority: int = 0
    language: Language = Language.PYTHON


@dataclass(frozen=True)
class RefactoringOperation:
    """Represents a refactoring operation."""
    operation_type: RefactoringType
    description: str
    old_code: str
    new_code: str
    line_number: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    file_path: str = ""
    language: Language = Language.PYTHON
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class FormattingResult:
    """Result of code formatting operation."""
    formatted_code: str
    changes_made: List[str]
    warnings: List[str]
    errors: List[str]
    original_length: int
    formatted_length: int
    processing_time: float


class CodeFormattingEngine:
    """
    Advanced code formatting and refactoring engine.
    
    This class provides automatic code cleanup, formatting, and refactoring
    capabilities for multiple programming languages.
    """
    
    def __init__(self):
        self._formatting_rules: Dict[Language, List[FormattingRule]] = {}
        self._refactoring_patterns: Dict[Language, Dict[str, str]] = {}
        self._custom_rules: Dict[Language, List[FormattingRule]] = {}
        self._lock = Lock()
        self._logger = logging.getLogger(f"{__name__}.CodeFormattingEngine")
        
        # Initialize language-specific formatting
        self._setup_languages()
        self._logger.info("CodeFormattingEngine initialized")
    
    def _setup_languages(self):
        """Setup language-specific formatting rules."""
        # Python language setup
        self._setup_python_formatting()
        
        # GLSL language setup
        self._setup_glsl_formatting()
        
        # JSON language setup
        self._setup_json_formatting()
    
    def _setup_python_formatting(self):
        """Setup Python-specific formatting rules."""
        python = Language.PYTHON
        
        # Python formatting rules (PEP 8 style)
        python_rules = [
            FormattingRule(
                name="remove_trailing_whitespace",
                description="Remove trailing whitespace",
                pattern=r'[ \t]+$',
                replacement='',
                language=python,
                priority=1
            ),
            FormattingRule(
                name="fix_indentation",
                description="Fix indentation to use 4 spaces",
                pattern=r'^\t+',
                replacement=lambda m: '    ' * len(m.group()),
                language=python,
                priority=2
            ),
            FormattingRule(
                name="fix_line_length",
                description="Break long lines at 79 characters",
                pattern=r'^(.{79,})$',
                replacement=lambda m: self._break_long_line(m.group(1)),
                language=python,
                priority=3
            ),
            FormattingRule(
                name="add_spaces_around_operators",
                description="Add spaces around operators",
                pattern=r'(\w)([+\-*/=<>!&|%])(\w)',
                replacement=r'\1 \2 \3',
                language=python,
                priority=4
            ),
            FormattingRule(
                name="fix_import_spacing",
                description="Add blank lines between import groups",
                pattern=r'(import\s+\w+)\n(import\s+\w+)',
                replacement=r'\1\n\n\2',
                language=python,
                priority=5
            )
        ]
        
        self._formatting_rules[python] = python_rules
        
        # Python refactoring patterns
        self._refactoring_patterns[python] = {
            'extract_method': r'def\s+(\w+)\s*\([^)]*\):\s*\n((?:\s+[^\n]*\n)*)',
            'extract_variable': r'(\w+)\s*=\s*([^#\n]+)',
            'rename_variable': r'\b(\w+)\b',
            'inline_function': r'(\w+)\s*=\s*lambda\s*[^:]*:\s*([^#\n]+)'
        }
    
    def _setup_glsl_formatting(self):
        """Setup GLSL-specific formatting rules."""
        glsl = Language.GLSL
        
        # GLSL formatting rules
        glsl_rules = [
            FormattingRule(
                name="fix_glsl_indentation",
                description="Fix GLSL indentation to use 4 spaces",
                pattern=r'^\t+',
                replacement=lambda m: '    ' * len(m.group()),
                language=glsl,
                priority=1
            ),
            FormattingRule(
                name="add_glsl_spacing",
                description="Add spaces around GLSL operators",
                pattern=r'(\w)([+\-*/=<>!&|%])(\w)',
                replacement=r'\1 \2 \3',
                language=glsl,
                priority=2
            ),
            FormattingRule(
                name="fix_glsl_precision",
                description="Standardize precision qualifiers",
                pattern=r'precision\s+(lowp|mediump|highp)\s+float;',
                replacement=r'precision \1 float;',
                language=glsl,
                priority=3
            )
        ]
        
        self._formatting_rules[glsl] = glsl_rules
        
        # GLSL refactoring patterns
        self._refactoring_patterns[glsl] = {
            'extract_function': r'void\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            'extract_uniform': r'uniform\s+(\w+)\s+(\w+);',
            'rename_variable': r'\b(\w+)\b'
        }
    
    def _setup_json_formatting(self):
        """Setup JSON-specific formatting rules."""
        json = Language.JSON
        
        # JSON formatting rules
        json_rules = [
            FormattingRule(
                name="format_json_indentation",
                description="Format JSON with consistent indentation",
                pattern=r'^(\s*)([^"\s][^:]*):',
                replacement=lambda m: self._format_json_indent(m.group(1), m.group(2)),
                language=json,
                priority=1
            ),
            FormattingRule(
                name="remove_json_trailing_commas",
                description="Remove trailing commas in JSON",
                pattern=r',(\s*[}\]])',
                replacement=r'\1',
                language=json,
                priority=2
            )
        ]
        
        self._formatting_rules[json] = json_rules
        
        # JSON refactoring patterns
        self._refactoring_patterns[json] = {
            'extract_object': r'\{[^}]*\}',
            'rename_property': r'"(\w+)":',
            'add_property': r'(\{[^}]*\})'
        }
    
    def _break_long_line(self, line: str) -> str:
        """Break a long line at appropriate points."""
        if len(line) <= 79:
            return line
        
        # Try to break at operators
        operators = [' + ', ' - ', ' * ', ' / ', ' = ', ' == ', ' != ', ' and ', ' or ']
        for op in operators:
            if op in line:
                parts = line.split(op)
                if len(parts) == 2:
                    if len(parts[0]) <= 79 and len(parts[1]) <= 79:
                        return f"{parts[0]}{op}\n    {parts[1]}"
        
        # Try to break at commas
        if ', ' in line:
            parts = line.split(', ')
            if len(parts) == 2:
                if len(parts[0]) <= 79 and len(parts[1]) <= 79:
                    return f"{parts[0]},\n    {parts[1]}"
        
        # Force break at 79 characters
        return f"{line[:79]}\n    {line[79:]}"
    
    def _format_json_indent(self, current_indent: str, content: str) -> str:
        """Format JSON indentation."""
        # Increase indentation by 2 spaces
        new_indent = current_indent + "  "
        return f"{new_indent}{content}:"
    
    def format_code(self, code: str, language: Language, style: FormattingStyle = FormattingStyle.PEP8) -> FormattingResult:
        """
        Format code according to specified style.
        
        Args:
            code: Source code to format
            language: Programming language
            style: Formatting style to apply
            
        Returns:
            Formatting result with formatted code and metadata
        """
        try:
            start_time = datetime.now()
            
            with self._lock:
                formatted_code = code
                changes_made = []
                warnings = []
                errors = []
                
                if language not in self._formatting_rules:
                    warnings.append(f"No formatting rules found for {language.value}")
                    return FormattingResult(
                        formatted_code=code,
                        changes_made=changes_made,
                        warnings=warnings,
                        errors=errors,
                        original_length=len(code),
                        formatted_length=len(code),
                        processing_time=0.0
                    )
                
                rules = self._formatting_rules[language]
                
                # Apply formatting rules in priority order
                rules.sort(key=lambda r: r.priority)
                
                for rule in rules:
                    if not rule.enabled:
                        continue
                    
                    try:
                        if callable(rule.replacement):
                            # Custom replacement function
                            new_code = re.sub(rule.pattern, rule.replacement, formatted_code, flags=re.MULTILINE)
                        else:
                            # Simple string replacement
                            new_code = re.sub(rule.pattern, rule.replacement, formatted_code, flags=re.MULTILINE)
                        
                        if new_code != formatted_code:
                            formatted_code = new_code
                            changes_made.append(f"Applied {rule.name}: {rule.description}")
                    
                    except Exception as e:
                        warnings.append(f"Failed to apply rule '{rule.name}': {e}")
                
                # Language-specific post-processing
                if language == Language.PYTHON:
                    formatted_code = self._post_process_python(formatted_code)
                elif language == Language.JSON:
                    formatted_code = self._post_process_json(formatted_code)
                elif language == Language.GLSL:
                    formatted_code = self._post_process_glsl(formatted_code)
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                return FormattingResult(
                    formatted_code=formatted_code,
                    changes_made=changes_made,
                    warnings=warnings,
                    errors=errors,
                    original_length=len(code),
                    formatted_length=len(formatted_code),
                    processing_time=processing_time
                )
                
        except Exception as e:
            self._logger.error(f"Failed to format code: {e}")
            return FormattingResult(
                formatted_code=code,
                changes_made=[],
                warnings=[],
                errors=[f"Formatting failed: {e}"],
                original_length=len(code),
                formatted_length=len(code),
                processing_time=0.0
            )
    
    def _post_process_python(self, code: str) -> str:
        """Post-process Python code formatting."""
        lines = code.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            # Ensure consistent indentation
            if line.strip() and not line.startswith('#'):
                # Count leading spaces and convert to 4-space indentation
                leading_spaces = len(line) - len(line.lstrip())
                indent_level = leading_spaces // 4
                formatted_line = '    ' * indent_level + line.strip()
                formatted_lines.append(formatted_line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _post_process_json(self, code: str) -> str:
        """Post-process JSON code formatting."""
        try:
            # Parse and re-format JSON with consistent indentation
            parsed = json.loads(code)
            return json.dumps(parsed, indent=2, separators=(',', ': '))
        except json.JSONDecodeError:
            # If JSON is invalid, return as-is
            return code
    
    def _post_process_glsl(self, code: str) -> str:
        """Post-process GLSL code formatting."""
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():
                # Ensure consistent indentation
                leading_spaces = len(line) - len(line.lstrip())
                indent_level = leading_spaces // 4
                formatted_line = '    ' * indent_level + line.strip()
                formatted_lines.append(formatted_line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def suggest_refactoring(self, code: str, language: Language) -> List[RefactoringOperation]:
        """
        Suggest refactoring opportunities in the code.
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            List of suggested refactoring operations
        """
        try:
            with self._lock:
                suggestions = []
                
                if language not in self._refactoring_patterns:
                    return suggestions
                
                patterns = self._refactoring_patterns[language]
                
                # Analyze code for refactoring opportunities
                if language == Language.PYTHON:
                    suggestions.extend(self._analyze_python_refactoring(code))
                elif language == Language.GLSL:
                    suggestions.extend(self._analyze_glsl_refactoring(code))
                elif language == Language.JSON:
                    suggestions.extend(self._analyze_json_refactoring(code))
                
                return suggestions
                
        except Exception as e:
            self._logger.error(f"Failed to suggest refactoring: {e}")
            return []
    
    def _analyze_python_refactoring(self, code: str) -> List[RefactoringOperation]:
        """Analyze Python code for refactoring opportunities."""
        suggestions = []
        
        try:
            # Parse Python code
            tree = ast.parse(code)
            
            # Look for long functions (extract method opportunity)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(code.split('\n')) > 20:  # Function longer than 20 lines
                        suggestion = RefactoringOperation(
                            operation_type=RefactoringType.EXTRACT_METHOD,
                            description="Function is quite long, consider extracting parts into smaller functions",
                            old_code=code,
                            new_code=code,  # Placeholder
                            line_number=getattr(node, 'lineno', 1),
                            column=getattr(node, 'col_offset', 0),
                            language=Language.PYTHON,
                            confidence=0.8
                        )
                        suggestions.append(suggestion)
            
            # Look for repeated code patterns
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and len(line.strip()) > 50:
                    # Long line - suggest breaking it up
                    suggestion = RefactoringOperation(
                        operation_type=RefactoringType.SPLIT,
                        description="Long line detected, consider breaking it up for readability",
                        old_code=line,
                        new_code=self._break_long_line(line),
                        line_number=i + 1,
                        column=0,
                        language=Language.PYTHON,
                        confidence=0.9
                    )
                    suggestions.append(suggestion)
        
        except SyntaxError:
            # Code has syntax errors, can't analyze for refactoring
            pass
        
        return suggestions
    
    def _analyze_glsl_refactoring(self, code: str) -> List[RefactoringOperation]:
        """Analyze GLSL code for refactoring opportunities."""
        suggestions = []
        
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if 'uniform' in line and ';' in line:
                # Suggest organizing uniforms
                suggestion = RefactoringOperation(
                    operation_type=RefactoringType.REORDER,
                    description="Consider grouping related uniforms together",
                    old_code=line,
                    new_code=line,
                    line_number=i + 1,
                    column=0,
                    language=Language.GLSL,
                    confidence=0.7
                )
                suggestions.append(suggestion)
        
        return suggestions
    
    def _analyze_json_refactoring(self, code: str) -> List[RefactoringOperation]:
        """Analyze JSON code for refactoring opportunities."""
        suggestions = []
        
        try:
            parsed = json.loads(code)
            
            # Suggest organizing properties
            if isinstance(parsed, dict) and len(parsed) > 10:
                suggestion = RefactoringOperation(
                    operation_type=RefactoringType.REORDER,
                    description="Large JSON object detected, consider organizing properties into logical groups",
                    old_code=code,
                    new_code=code,
                    line_number=1,
                    column=0,
                    language=Language.JSON,
                    confidence=0.6
                )
                suggestions.append(suggestion)
        
        except json.JSONDecodeError:
            # Invalid JSON, can't analyze
            pass
        
        return suggestions
    
    def add_custom_formatting_rule(self, language: Language, rule: FormattingRule) -> bool:
        """
        Add a custom formatting rule.
        
        Args:
            language: Programming language
            rule: Formatting rule to add
            
        Returns:
            True if rule was added successfully, False otherwise
        """
        try:
            with self._lock:
                if language not in self._custom_rules:
                    self._custom_rules[language] = []
                
                self._custom_rules[language].append(rule)
                
                # Also add to main formatting rules
                if language not in self._formatting_rules:
                    self._formatting_rules[language] = []
                
                self._formatting_rules[language].append(rule)
                
                self._logger.debug(f"Added custom formatting rule for {language.value}: {rule.name}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to add custom formatting rule: {e}")
            return False
    
    def get_formatting_summary(self) -> Dict[str, Any]:
        """Get a summary of all formatting rules."""
        return {
            "total_languages": len(self._formatting_rules),
            "languages": list(lang.value for lang in self._formatting_rules.keys()),
            "rules_by_language": {
                lang.value: len(rules) for lang, rules in self._formatting_rules.items()
            },
            "total_custom_rules": sum(len(rules) for rules in self._custom_rules.values()),
            "custom_rules_by_language": {
                lang.value: len(rules) for lang, rules in self._custom_rules.items()
            }
        }
    
    def validate_formatting_rules(self) -> Dict[str, Any]:
        """Validate formatting rules for consistency issues."""
        issues = []
        warnings = []
        
        for language, rules in self._formatting_rules.items():
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
            
            # Check for empty descriptions
            empty_descriptions = [rule.name for rule in rules if not rule.description]
            if empty_descriptions:
                warnings.append(f"Rules without descriptions in {language.value}: {empty_descriptions}")
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues,
            "warnings": warnings,
            "total_languages": len(self._formatting_rules),
            "total_rules": sum(len(rules) for rules in self._formatting_rules.values())
        }
