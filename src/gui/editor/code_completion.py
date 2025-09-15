#!/usr/bin/env python3
"""
Code Completion Engine for Editor Usability Tools.

This module provides IntelliSense functionality with syntax highlighting,
intelligent code suggestions, and context-aware completions.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple, Union, Any, Set
import logging
import re
from threading import Lock
from pathlib import Path

logger = logging.getLogger(__name__)


class CompletionType(Enum):
    """Types of code completions available."""
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    MODULE = "module"
    KEYWORD = "keyword"
    SNIPPET = "snippet"
    IMPORT = "import"
    ATTRIBUTE = "attribute"
    METHOD = "method"
    PROPERTY = "property"


class SuggestionPriority(Enum):
    """Priority levels for code suggestions."""
    HIGH = "high"      # Exact matches, frequently used
    MEDIUM = "medium"  # Partial matches, common patterns
    LOW = "low"        # Fuzzy matches, less common


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
class CodeSuggestion:
    """Represents a code completion suggestion."""
    text: str
    display_text: str
    completion_type: CompletionType
    priority: SuggestionPriority
    description: str = ""
    documentation: str = ""
    language: Language = Language.PYTHON
    snippet: Optional[str] = None
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None


@dataclass(frozen=True)
class CompletionContext:
    """Context information for code completion."""
    line_number: int
    column: int
    current_word: str
    line_text: str
    file_path: str
    language: Language
    scope: str = "global"
    in_string: bool = False
    in_comment: bool = False
    in_function: bool = False
    in_class: bool = False


@dataclass(frozen=True)
class SyntaxToken:
    """Represents a syntax token for highlighting."""
    text: str
    token_type: str
    start_pos: int
    end_pos: int
    line_number: int
    style: Dict[str, str] = field(default_factory=dict)


class CodeCompletionEngine:
    """
    Advanced code completion engine with IntelliSense capabilities.
    
    This class provides intelligent code suggestions, syntax highlighting,
    and context-aware completions for multiple programming languages.
    """
    
    def __init__(self):
        self._suggestions: Dict[Language, Dict[str, CodeSuggestion]] = {}
        self._snippets: Dict[Language, Dict[str, str]] = {}
        self._keywords: Dict[Language, Set[str]] = {}
        self._syntax_patterns: Dict[Language, Dict[str, str]] = {}
        self._lock = Lock()
        self._logger = logging.getLogger(f"{__name__}.CodeCompletionEngine")
        
        # Initialize language-specific data
        self._setup_languages()
        self._logger.info("CodeCompletionEngine initialized")
    
    def _setup_languages(self):
        """Setup language-specific completions and syntax patterns."""
        # Python language setup
        self._setup_python_language()
        
        # GLSL language setup
        self._setup_glsl_language()
        
        # JSON language setup
        self._setup_json_language()
    
    def _setup_python_language(self):
        """Setup Python-specific language data."""
        python = Language.PYTHON
        
        # Python keywords
        self._keywords[python] = {
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del',
            'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
            'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
            'raise', 'return', 'try', 'while', 'with', 'yield', 'True', 'False',
            'None', 'self', 'super'
        }
        
        # Python built-in functions
        builtin_functions = [
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray',
            'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr',
            'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float',
            'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
            'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len',
            'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object',
            'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr',
            'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
            'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
        ]
        
        for func in builtin_functions:
            suggestion = CodeSuggestion(
                text=func,
                display_text=f"{func}()",
                completion_type=CompletionType.FUNCTION,
                priority=SuggestionPriority.HIGH,
                description=f"Built-in Python function: {func}",
                language=python
            )
            self._add_suggestion(python, func, suggestion)
        
        # Python syntax patterns
        self._syntax_patterns[python] = {
            'keyword': r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|True|False|None|self|super)\b',
            'string': r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"]*"|\'[^\']*\')',
            'comment': r'(#.*$)',
            'function_def': r'\bdef\s+(\w+)\s*\(',
            'class_def': r'\bclass\s+(\w+)',
            'import': r'\b(import|from)\s+(\w+)',
            'number': r'\b\d+\.?\d*\b',
            'operator': r'[\+\-\*/=<>!&\|%]',
            'identifier': r'\b[a-zA-Z_]\w*\b'
        }
    
    def _setup_glsl_language(self):
        """Setup GLSL-specific language data."""
        glsl = Language.GLSL
        
        # GLSL keywords
        self._keywords[glsl] = {
            'attribute', 'const', 'uniform', 'varying', 'centroid', 'flat',
            'smooth', 'noperspective', 'patch', 'sample', 'break', 'continue',
            'do', 'for', 'while', 'switch', 'case', 'default', 'if', 'else',
            'subroutine', 'in', 'out', 'inout', 'invariant', 'precise', 'return',
            'discard', 'mat2', 'mat3', 'mat4', 'mat2x2', 'mat2x3', 'mat2x4',
            'mat3x2', 'mat3x3', 'mat3x4', 'mat4x2', 'mat4x3', 'mat4x4',
            'vec2', 'vec3', 'vec4', 'ivec2', 'ivec3', 'ivec4', 'bvec2',
            'bvec3', 'bvec4', 'dvec2', 'dvec3', 'dvec4', 'float', 'double',
            'int', 'void', 'bool', 'true', 'false'
        }
        
        # GLSL built-in functions
        glsl_functions = [
            'abs', 'acos', 'asin', 'atan', 'ceil', 'clamp', 'cos', 'cross',
            'degrees', 'distance', 'dot', 'exp', 'exp2', 'floor', 'fract',
            'length', 'log', 'log2', 'max', 'min', 'mix', 'mod', 'normalize',
            'pow', 'radians', 'reflect', 'refract', 'round', 'sign', 'sin',
            'smoothstep', 'sqrt', 'step', 'tan', 'texture', 'texture2D'
        ]
        
        for func in glsl_functions:
            suggestion = CodeSuggestion(
                text=func,
                display_text=f"{func}()",
                completion_type=CompletionType.FUNCTION,
                priority=SuggestionPriority.HIGH,
                description=f"GLSL built-in function: {func}",
                language=glsl
            )
            self._add_suggestion(glsl, func, suggestion)
        
        # GLSL syntax patterns
        self._syntax_patterns[glsl] = {
            'keyword': r'\b(attribute|const|uniform|varying|centroid|flat|smooth|noperspective|patch|sample|break|continue|do|for|while|switch|case|default|if|else|subroutine|in|out|inout|invariant|precise|return|discard|mat2|mat3|mat4|vec2|vec3|vec4|float|int|void|bool|true|false)\b',
            'string': r'(".*?")',
            'comment': r'(//.*$|/\*[\s\S]*?\*/)',
            'function_def': r'\b\w+\s+(\w+)\s*\(',
            'number': r'\b\d+\.?\d*\b',
            'operator': r'[\+\-\*/=<>!&\|%]',
            'identifier': r'\b[a-zA-Z_]\w*\b'
        }
    
    def _setup_json_language(self):
        """Setup JSON-specific language data."""
        json = Language.JSON
        
        # JSON keywords
        self._keywords[json] = {'true', 'false', 'null'}
        
        # JSON syntax patterns
        self._syntax_patterns[json] = {
            'keyword': r'\b(true|false|null)\b',
            'string': r'(".*?")',
            'number': r'\b\d+\.?\d*\b',
            'operator': r'[{}[\],:]',
            'whitespace': r'\s+'
        }
    
    def _add_suggestion(self, language: Language, key: str, suggestion: CodeSuggestion):
        """Add a suggestion to the language-specific suggestions."""
        if language not in self._suggestions:
            self._suggestions[language] = {}
        self._suggestions[language][key] = suggestion
    
    def get_completions(self, context: CompletionContext) -> List[CodeSuggestion]:
        """
        Get code completion suggestions based on context.
        
        Args:
            context: Completion context information
            
        Returns:
            List of relevant code suggestions
        """
        try:
            with self._lock:
                suggestions = []
                
                if context.language not in self._suggestions:
                    return suggestions
                
                current_word = context.current_word.lower()
                language_suggestions = self._suggestions[context.language]
                
                # Get suggestions based on current word
                for key, suggestion in language_suggestions.items():
                    if current_word in key.lower() or key.lower().startswith(current_word):
                        suggestions.append(suggestion)
                
                # Add keyword suggestions
                if context.language in self._keywords:
                    for keyword in self._keywords[context.language]:
                        if current_word in keyword.lower() or keyword.lower().startswith(current_word):
                            keyword_suggestion = CodeSuggestion(
                                text=keyword,
                                display_text=keyword,
                                completion_type=CompletionType.KEYWORD,
                                priority=SuggestionPriority.MEDIUM,
                                description=f"{context.language.value.title()} keyword: {keyword}",
                                language=context.language
                            )
                            suggestions.append(keyword_suggestion)
                
                # Sort suggestions by priority and relevance
                suggestions.sort(key=lambda s: (
                    s.priority.value == SuggestionPriority.HIGH.value,
                    s.text.lower().startswith(current_word),
                    len(s.text)
                ), reverse=True)
                
                return suggestions[:20]  # Limit to top 20 suggestions
                
        except Exception as e:
            self._logger.error(f"Failed to get completions: {e}")
            return []
    
    def get_code_completion_suggestions(self, code: str, line: int, column: int, language: Language) -> List[CodeSuggestion]:
        """
        Get code completion suggestions for a specific position in code.
        
        Args:
            code: Source code
            line: Current line number (1-indexed)
            column: Current column number (1-indexed)
            language: Programming language
            
        Returns:
            List of relevant code suggestions
        """
        try:
            # Extract current word at cursor position
            lines = code.split('\n')
            if line <= 0 or line > len(lines):
                return []
            
            current_line = lines[line - 1]
            if column <= 0 or column > len(current_line):
                return []
            
            # Find the start of the current word
            word_start = column - 1
            while word_start > 0 and current_line[word_start - 1].isalnum() or current_line[word_start - 1] == '_':
                word_start -= 1
            
            current_word = current_line[word_start:column]
            
            # Create completion context
            context = CompletionContext(
                current_word=current_word,
                line_number=line,
                column_number=column,
                language=language,
                surrounding_code=current_line,
                file_path=""
            )
            
            return self.get_completions(context)
            
        except Exception as e:
            self._logger.error(f"Failed to get code completion suggestions: {e}")
            return []
    
    def analyze_syntax(self, code: str, language: Language) -> List[SyntaxToken]:
        """
        Analyze code syntax and return tokens for highlighting.
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            List of syntax tokens
        """
        try:
            if language not in self._syntax_patterns:
                return []
            
            tokens = []
            patterns = self._syntax_patterns[language]
            
            for line_num, line in enumerate(code.split('\n'), 1):
                for token_type, pattern in patterns.items():
                    for match in re.finditer(pattern, line, re.IGNORECASE):
                        token = SyntaxToken(
                            text=match.group(),
                            token_type=token_type,
                            start_pos=match.start(),
                            end_pos=match.end(),
                            line_number=line_num,
                            style=self._get_token_style(token_type, language)
                        )
                        tokens.append(token)
            
            return tokens
            
        except Exception as e:
            self._logger.error(f"Failed to analyze syntax: {e}")
            return []
    
    def _get_token_style(self, token_type: str, language: Language) -> Dict[str, str]:
        """Get CSS style for a token type."""
        base_styles = {
            'keyword': {'color': '#569cd6', 'font-weight': 'bold'},
            'string': {'color': '#ce9178'},
            'comment': {'color': '#6a9955', 'font-style': 'italic'},
            'function_def': {'color': '#dcdcaa'},
            'class_def': {'color': '#4ec9b0'},
            'import': {'color': '#c586c0'},
            'number': {'color': '#b5cea8'},
            'operator': {'color': '#d4d4d4'},
            'identifier': {'color': '#9cdcfe'}
        }
        
        return base_styles.get(token_type, {'color': '#d4d4d4'})
    
    def add_custom_suggestion(self, name: str, snippet: str, language: Language) -> bool:
        """
        Add a custom code suggestion.
        
        Args:
            name: Suggestion name/text
            snippet: Code snippet content
            language: Programming language
            
        Returns:
            True if suggestion was added successfully, False otherwise
        """
        try:
            with self._lock:
                suggestion = CodeSuggestion(
                    text=name,
                    display_text=name,
                    completion_type=CompletionType.SNIPPET,
                    priority=SuggestionPriority.MEDIUM,
                    description=f"Custom suggestion: {name}",
                    language=language,
                    snippet=snippet
                )
                self._add_suggestion(language, name, suggestion)
                self._logger.debug(f"Added custom suggestion for {language.value}: {name}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to add custom suggestion: {e}")
            return False
    
    def add_snippet(self, language: Language, name: str, snippet: str) -> bool:
        """
        Add a code snippet.
        
        Args:
            language: Programming language
            name: Snippet name
            snippet: Code snippet content
            
        Returns:
            True if snippet was added successfully, False otherwise
        """
        try:
            with self._lock:
                if language not in self._snippets:
                    self._snippets[language] = {}
                
                self._snippets[language][name] = snippet
                
                # Create suggestion for the snippet
                snippet_suggestion = CodeSuggestion(
                    text=name,
                    display_text=f"{name} (snippet)",
                    completion_type=CompletionType.SNIPPET,
                    priority=SuggestionPriority.MEDIUM,
                    description=f"Code snippet: {name}",
                    language=language,
                    snippet=snippet
                )
                
                self._add_suggestion(language, name, snippet_suggestion)
                
                self._logger.debug(f"Added snippet for {language.value}: {name}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to add snippet: {e}")
            return False
    
    def get_snippet(self, language: Language, name: str) -> Optional[str]:
        """Get a code snippet by name."""
        return self._snippets.get(language, {}).get(name)
    
    def get_suggestions_summary(self) -> Dict[str, Any]:
        """Get a summary of all suggestions and snippets."""
        return {
            "total_languages": len(self._suggestions),
            "languages": list(lang.value for lang in self._suggestions.keys()),
            "total_suggestions": sum(len(suggestions) for suggestions in self._suggestions.values()),
            "total_snippets": sum(len(snippets) for snippets in self._snippets.values()),
            "suggestions_by_language": {lang.value: len(suggestions) for lang, suggestions in self._suggestions.items()},
            "snippets_by_language": {lang.value: len(snippets) for lang, snippets in self._snippets.items()}
        }
    
    def validate_suggestions(self) -> Dict[str, Any]:
        """Validate suggestions for consistency issues."""
        issues = []
        warnings = []
        
        for language, suggestions in self._suggestions.items():
            # Check for duplicate suggestions
            suggestion_texts = [s.text for s in suggestions.values()]
            duplicates = set([text for text in suggestion_texts if suggestion_texts.count(text) > 1])
            
            if duplicates:
                warnings.append(f"Duplicate suggestions in {language.value}: {list(duplicates)}")
            
            # Check for empty descriptions
            empty_descriptions = [s.text for s in suggestions.values() if not s.description]
            if empty_descriptions:
                warnings.append(f"Suggestions without descriptions in {language.value}: {empty_descriptions}")
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues,
            "warnings": warnings,
            "total_languages": len(self._suggestions),
            "total_suggestions": sum(len(suggestions) for suggestions in self._suggestions.values())
        }
    
    def analyze_syntax_for_highlighting(self, code: str, language: Language) -> List[SyntaxToken]:
        """
        Analyze code syntax for highlighting (alias for analyze_syntax).
        
        Args:
            code: Source code to analyze
            language: Language enum value
            
        Returns:
            List of syntax tokens for highlighting
        """
        return self.analyze_syntax(code, language)
