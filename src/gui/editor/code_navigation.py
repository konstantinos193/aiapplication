#!/usr/bin/env python3
"""
Code Navigation and Search Tools for Editor Usability Tools.

This module provides intelligent code navigation, search, and symbol
resolution capabilities for multiple programming languages.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple, Union, Any, Set
import logging
import re
import ast
import json
from threading import Lock
from pathlib import Path
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class SymbolType(Enum):
    """Types of code symbols."""
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    CONSTANT = "constant"
    IMPORT = "import"
    MODULE = "module"
    PACKAGE = "package"
    PROPERTY = "property"
    ENUM = "enum"
    STRUCT = "struct"
    INTERFACE = "interface"
    NAMESPACE = "namespace"
    MACRO = "macro"
    COMMENT = "comment"
    STRING = "string"
    NUMBER = "number"


class SearchScope(Enum):
    """Search scope options."""
    CURRENT_FILE = "current_file"
    CURRENT_DIRECTORY = "current_directory"
    PROJECT = "project"
    WORKSPACE = "workspace"
    ALL_FILES = "all_files"


class NavigationDirection(Enum):
    """Navigation direction options."""
    FORWARD = "forward"
    BACKWARD = "backward"
    UP = "up"
    DOWN = "down"
    NEXT = "next"
    PREVIOUS = "previous"


@dataclass(frozen=True)
class CodeSymbol:
    """Represents a code symbol."""
    name: str
    symbol_type: SymbolType
    line_number: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    file_path: str = ""
    language: str = ""
    scope: str = ""
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class SearchResult:
    """Result of a code search operation."""
    query: str
    results: List[CodeSymbol]
    total_count: int
    search_time: float
    scope: SearchScope
    language_filter: Optional[str] = None
    symbol_type_filter: Optional[SymbolType] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class NavigationContext:
    """Context for code navigation operations."""
    current_file: str
    current_line: int
    current_column: int
    cursor_position: Tuple[int, int]
    symbol_stack: List[CodeSymbol] = field(default_factory=list)
    navigation_history: List[Tuple[str, int, int]] = field(default_factory=list)
    bookmarks: List[Tuple[str, int, int]] = field(default_factory=list)
    recent_files: List[str] = field(default_factory=list)


class CodeNavigationEngine:
    """
    Advanced code navigation and search engine.
    
    This class provides intelligent code navigation, search, and symbol
    resolution capabilities for multiple programming languages.
    """
    
    def __init__(self):
        self._symbol_index: Dict[str, Dict[str, CodeSymbol]] = defaultdict(dict)
        self._file_symbols: Dict[str, List[CodeSymbol]] = {}
        self._symbol_references: Dict[str, List[Tuple[str, int, int]]] = defaultdict(list)
        self._navigation_contexts: Dict[str, NavigationContext] = {}
        self._search_cache: Dict[str, SearchResult] = {}
        self._lock = Lock()
        self._logger = logging.getLogger(f"{__name__}.CodeNavigationEngine")
        
        # Initialize language-specific parsers
        self._setup_language_parsers()
        self._logger.info("CodeNavigationEngine initialized")
    
    def _setup_language_parsers(self):
        """Setup language-specific symbol parsers."""
        self._parsers = {
            'python': self._parse_python_symbols,
            'glsl': self._parse_glsl_symbols,
            'hlsl': self._parse_hlsl_symbols,
            'json': self._parse_json_symbols,
            'cpp': self._parse_cpp_symbols,
            'rust': self._parse_rust_symbols
        }
    
    def index_file(self, file_path: str, content: str, language: str) -> bool:
        """
        Index a file for symbol resolution.
        
        Args:
            file_path: Path to the file
            content: File content
            language: Programming language
            
        Returns:
            True if indexing was successful, False otherwise
        """
        try:
            with self._lock:
                # Clear existing symbols for this file
                if file_path in self._file_symbols:
                    old_symbols = self._file_symbols[file_path]
                    for symbol in old_symbols:
                        if symbol.name in self._symbol_index[file_path]:
                            del self._symbol_index[file_path][symbol.name]
                
                # Parse symbols based on language
                if language in self._parsers:
                    symbols = self._parsers[language](content, file_path)
                else:
                    symbols = self._parse_generic_symbols(content, file_path, language)
                
                # Index symbols
                self._file_symbols[file_path] = symbols
                for symbol in symbols:
                    self._symbol_index[file_path][symbol.name] = symbol
                
                # Build reference index
                self._build_reference_index(file_path, content, symbols)
                
                self._logger.debug(f"Indexed {len(symbols)} symbols in {file_path}")
                return True
                
        except Exception as e:
            self._logger.error(f"Failed to index file {file_path}: {e}")
            return False
    
    def _parse_python_symbols(self, content: str, file_path: str) -> List[CodeSymbol]:
        """Parse Python symbols from AST."""
        symbols = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    symbol = CodeSymbol(
                        name=node.name,
                        symbol_type=SymbolType.CLASS,
                        line_number=getattr(node, 'lineno', 1),
                        column=getattr(node, 'col_offset', 0),
                        end_line=getattr(node, 'end_lineno', None),
                        end_column=getattr(node, 'end_col_offset', None),
                        file_path=file_path,
                        language='python',
                        metadata={
                            'bases': [base.id for base in node.bases if hasattr(base, 'id')],
                            'decorators': [d.id for d in node.decorator_list if hasattr(d, 'id')]
                        }
                    )
                    symbols.append(symbol)
                
                elif isinstance(node, ast.FunctionDef):
                    symbol = CodeSymbol(
                        name=node.name,
                        symbol_type=SymbolType.FUNCTION,
                        line_number=getattr(node, 'lineno', 1),
                        column=getattr(node, 'col_offset', 0),
                        end_line=getattr(node, 'end_lineno', None),
                        end_column=getattr(node, 'end_col_offset', None),
                        file_path=file_path,
                        language='python',
                        parent=self._get_parent_name(node),
                        metadata={
                            'args': [arg.arg for arg in node.args.args],
                            'decorators': [d.id for d in node.decorator_list if hasattr(d, 'id')]
                        }
                    )
                    symbols.append(symbol)
                
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            symbol = CodeSymbol(
                                name=target.id,
                                symbol_type=SymbolType.VARIABLE,
                                line_number=getattr(node, 'lineno', 1),
                                column=getattr(node, 'col_offset', 0),
                                file_path=file_path,
                                language='python',
                                parent=self._get_parent_name(node)
                            )
                            symbols.append(symbol)
                
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        symbol = CodeSymbol(
                            name=alias.name,
                            symbol_type=SymbolType.IMPORT,
                            line_number=getattr(node, 'lineno', 1),
                            column=getattr(node, 'col_offset', 0),
                            file_path=file_path,
                            language='python',
                            metadata={'alias': alias.asname}
                        )
                        symbols.append(symbol)
                
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        symbol = CodeSymbol(
                            name=alias.name,
                            symbol_type=SymbolType.IMPORT,
                            line_number=getattr(node, 'lineno', 1),
                            column=getattr(node, 'col_offset', 0),
                            file_path=file_path,
                            language='python',
                            metadata={'module': node.module, 'alias': alias.asname}
                        )
                        symbols.append(symbol)
        
        except SyntaxError:
            # File has syntax errors, parse as generic
            pass
        
        return symbols
    
    def _parse_glsl_symbols(self, content: str, file_path: str) -> List[CodeSymbol]:
        """Parse GLSL symbols using regex patterns."""
        symbols = []
        
        # Function definitions
        function_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'
        for match in re.finditer(function_pattern, content):
            symbol = CodeSymbol(
                name=match.group(2),
                symbol_type=SymbolType.FUNCTION,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language='glsl',
                metadata={'return_type': match.group(1)}
            )
            symbols.append(symbol)
        
        # Uniform declarations
        uniform_pattern = r'uniform\s+(\w+)\s+(\w+);'
        for match in re.finditer(uniform_pattern, content):
            symbol = CodeSymbol(
                name=match.group(2),
                symbol_type=SymbolType.VARIABLE,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language='glsl',
                metadata={'uniform_type': match.group(1)}
            )
            symbols.append(symbol)
        
        # Variable declarations
        variable_pattern = r'(\w+)\s+(\w+)\s*[=;]'
        for match in re.finditer(variable_pattern, content):
            if match.group(1) not in ['uniform', 'attribute', 'varying', 'in', 'out']:
                symbol = CodeSymbol(
                    name=match.group(2),
                    symbol_type=SymbolType.VARIABLE,
                    line_number=content[:match.start()].count('\n') + 1,
                    column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                    file_path=file_path,
                    language='glsl',
                    metadata={'var_type': match.group(1)}
                )
                symbols.append(symbol)
        
        return symbols
    
    def _parse_hlsl_symbols(self, content: str, file_path: str) -> List[CodeSymbol]:
        """Parse HLSL symbols using regex patterns."""
        symbols = []
        
        # Function definitions
        function_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'
        for match in re.finditer(function_pattern, content):
            symbol = CodeSymbol(
                name=match.group(2),
                symbol_type=SymbolType.FUNCTION,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language='hlsl',
                metadata={'return_type': match.group(1)}
            )
            symbols.append(symbol)
        
        # Variable declarations
        variable_pattern = r'(\w+)\s+(\w+)\s*[=;]'
        for match in re.finditer(variable_pattern, content):
            if match.group(1) not in ['uniform', 'attribute', 'varying', 'in', 'out']:
                symbol = CodeSymbol(
                    name=match.group(2),
                    symbol_type=SymbolType.VARIABLE,
                    line_number=content[:match.start()].count('\n') + 1,
                    column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                    file_path=file_path,
                    language='hlsl',
                    metadata={'var_type': match.group(1)}
                )
                symbols.append(symbol)
        
        return symbols
    
    def _parse_json_symbols(self, content: str, file_path: str) -> List[CodeSymbol]:
        """Parse JSON symbols (properties and values)."""
        symbols = []
        
        try:
            data = json.loads(content)
            self._parse_json_object(data, symbols, file_path, 1, 0)
        except json.JSONDecodeError:
            # Invalid JSON, parse as generic
            pass
        
        return symbols
    
    def _parse_json_object(self, obj: Any, symbols: List[CodeSymbol], file_path: str, 
                          line: int, depth: int):
        """Recursively parse JSON object for symbols."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                symbol = CodeSymbol(
                    name=str(key),
                    symbol_type=SymbolType.PROPERTY,
                    line_number=line,
                    column=depth * 2,
                    file_path=file_path,
                    language='json',
                    metadata={'value_type': type(value).__name__}
                )
                symbols.append(symbol)
                
                if isinstance(value, (dict, list)):
                    self._parse_json_object(value, symbols, file_path, line + 1, depth + 1)
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    self._parse_json_object(item, symbols, file_path, line + i, depth + 1)
    
    def _parse_cpp_symbols(self, content: str, file_path: str) -> List[CodeSymbol]:
        """Parse C++ symbols using regex patterns."""
        symbols = []
        
        # Class definitions
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, content):
            symbol = CodeSymbol(
                name=match.group(1),
                symbol_type=SymbolType.CLASS,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language='cpp'
            )
            symbols.append(symbol)
        
        # Function definitions
        function_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'
        for match in re.finditer(function_pattern, content):
            symbol = CodeSymbol(
                name=match.group(2),
                symbol_type=SymbolType.FUNCTION,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language='cpp',
                metadata={'return_type': match.group(1)}
            )
            symbols.append(symbol)
        
        return symbols
    
    def _parse_rust_symbols(self, content: str, file_path: str) -> List[CodeSymbol]:
        """Parse Rust symbols using regex patterns."""
        symbols = []
        
        # Function definitions
        function_pattern = r'fn\s+(\w+)\s*\([^)]*\)'
        for match in re.finditer(function_pattern, content):
            symbol = CodeSymbol(
                name=match.group(1),
                symbol_type=SymbolType.FUNCTION,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language='rust'
            )
            symbols.append(symbol)
        
        # Struct definitions
        struct_pattern = r'struct\s+(\w+)'
        for match in re.finditer(struct_pattern, content):
            symbol = CodeSymbol(
                name=match.group(1),
                symbol_type=SymbolType.STRUCT,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language='rust'
            )
            symbols.append(symbol)
        
        return symbols
    
    def _parse_generic_symbols(self, content: str, file_path: str, language: str) -> List[CodeSymbol]:
        """Parse symbols using generic patterns for unsupported languages."""
        symbols = []
        
        # Look for function-like patterns
        function_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)'
        for match in re.finditer(function_pattern, content):
            symbol = CodeSymbol(
                name=match.group(2),
                symbol_type=SymbolType.FUNCTION,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language=language,
                metadata={'return_type': match.group(1)}
            )
            symbols.append(symbol)
        
        # Look for variable-like patterns
        variable_pattern = r'(\w+)\s+(\w+)\s*[=;]'
        for match in re.finditer(variable_pattern, content):
            symbol = CodeSymbol(
                name=match.group(2),
                symbol_type=SymbolType.VARIABLE,
                line_number=content[:match.start()].count('\n') + 1,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1,
                file_path=file_path,
                language=language,
                metadata={'var_type': match.group(1)}
            )
            symbols.append(symbol)
        
        return symbols
    
    def _get_parent_name(self, node: ast.AST) -> Optional[str]:
        """Get the parent name for a node."""
        try:
            for parent in ast.walk(node):
                for child in ast.iter_child_nodes(parent):
                    if child is node:
                        if isinstance(parent, ast.ClassDef):
                            return parent.name
                        elif isinstance(parent, ast.FunctionDef):
                            return parent.name
                        break
        except:
            pass
        return None
    
    def _build_reference_index(self, file_path: str, content: str, symbols: List[CodeSymbol]):
        """Build an index of symbol references."""
        for symbol in symbols:
            # Find all references to this symbol in the file
            references = []
            symbol_name = re.escape(symbol.name)
            
            # Look for references (excluding the definition)
            pattern = rf'\b{symbol_name}\b'
            for match in re.finditer(pattern, content):
                line_num = content[:match.start()].count('\n') + 1
                col_num = match.start() - content.rfind('\n', 0, match.start()) - 1
                
                # Skip if this is the definition
                if (line_num == symbol.line_number and 
                    abs(col_num - symbol.column) < len(symbol.name)):
                    continue
                
                references.append((file_path, line_num, col_num))
            
            self._symbol_references[symbol.name].extend(references)
    
    def search_symbols(self, query: str, scope: SearchScope = SearchScope.PROJECT,
                      language_filter: Optional[str] = None,
                      symbol_type_filter: Optional[SymbolType] = None) -> SearchResult:
        """
        Search for symbols matching the query.
        
        Args:
            query: Search query string
            scope: Search scope
            language_filter: Optional language filter
            symbol_type_filter: Optional symbol type filter
            
        Returns:
            Search result with matching symbols
        """
        try:
            start_time = datetime.now()
            
            with self._lock:
                results = []
                cache_key = f"{query}:{scope.value}:{language_filter}:{symbol_type_filter}"
                
                # Check cache first
                if cache_key in self._search_cache:
                    return self._search_cache[cache_key]
                
                # Determine search files based on scope
                search_files = self._get_search_files(scope)
                
                # Search in each file
                for file_path in search_files:
                    if file_path in self._file_symbols:
                        file_symbols = self._file_symbols[file_path]
                        
                        for symbol in file_symbols:
                            if self._matches_search_criteria(symbol, query, language_filter, symbol_type_filter):
                                results.append(symbol)
                
                # Sort results by relevance
                results.sort(key=lambda s: self._calculate_relevance(s, query))
                
                search_time = (datetime.now() - start_time).total_seconds()
                
                result = SearchResult(
                    query=query,
                    results=results,
                    total_count=len(results),
                    search_time=search_time,
                    scope=scope,
                    language_filter=language_filter,
                    symbol_type_filter=symbol_type_filter
                )
                
                # Cache the result
                self._search_cache[cache_key] = result
                
                return result
                
        except Exception as e:
            self._logger.error(f"Search failed: {e}")
            return SearchResult(
                query=query,
                results=[],
                total_count=0,
                search_time=0.0,
                scope=scope,
                language_filter=language_filter,
                symbol_type_filter=symbol_type_filter,
                errors=[f"Search failed: {e}"]
            )
    
    def _get_search_files(self, scope: SearchScope) -> List[str]:
        """Get list of files to search based on scope."""
        if scope == SearchScope.ALL_FILES:
            return list(self._file_symbols.keys())
        elif scope == SearchScope.PROJECT:
            # For now, return all files. In a real implementation,
            # this would filter based on project structure
            return list(self._file_symbols.keys())
        else:
            # Other scopes would need additional context
            return list(self._file_symbols.keys())
    
    def _matches_search_criteria(self, symbol: CodeSymbol, query: str,
                               language_filter: Optional[str],
                               symbol_type_filter: Optional[SymbolType]) -> bool:
        """Check if symbol matches search criteria."""
        # Check language filter
        if language_filter and symbol.language != language_filter:
            return False
        
        # Check symbol type filter
        if symbol_type_filter and symbol.symbol_type != symbol_type_filter:
            return False
        
        # Check if query matches symbol name
        query_lower = query.lower()
        symbol_lower = symbol.name.lower()
        
        # Exact match
        if query_lower == symbol_lower:
            return True
        
        # Contains query
        if query_lower in symbol_lower:
            return True
        
        # Query contains symbol (partial match)
        if symbol_lower in query_lower:
            return True
        
        # Fuzzy match (simple implementation)
        if self._fuzzy_match(query_lower, symbol_lower):
            return True
        
        return False
    
    def _fuzzy_match(self, query: str, target: str) -> bool:
        """Simple fuzzy matching implementation."""
        if len(query) < 2:
            return False
        
        # Check if query characters appear in order in target
        query_idx = 0
        for char in target:
            if query_idx < len(query) and char == query[query_idx]:
                query_idx += 1
                if query_idx == len(query):
                    return True
        
        return False
    
    def _calculate_relevance(self, symbol: CodeSymbol, query: str) -> float:
        """Calculate relevance score for search result."""
        score = 0.0
        
        # Exact match gets highest score
        if symbol.name.lower() == query.lower():
            score += 100.0
        
        # Starts with query
        elif symbol.name.lower().startswith(query.lower()):
            score += 50.0
        
        # Contains query
        elif query.lower() in symbol.name.lower():
            score += 25.0
        
        # Fuzzy match
        elif self._fuzzy_match(query.lower(), symbol.name.lower()):
            score += 10.0
        
        # Prefer functions and classes
        if symbol.symbol_type in [SymbolType.FUNCTION, SymbolType.CLASS]:
            score += 5.0
        
        # Prefer symbols in current file (if we have context)
        # This would need to be implemented with navigation context
        
        return score
    
    def go_to_definition(self, symbol_name: str, current_file: str,
                        current_line: int) -> Optional[CodeSymbol]:
        """
        Go to the definition of a symbol.
        
        Args:
            symbol_name: Name of the symbol to find
            current_file: Current file path
            current_line: Current line number
            
        Returns:
            Symbol definition if found, None otherwise
        """
        try:
            with self._lock:
                # First check in current file
                if current_file in self._symbol_index:
                    if symbol_name in self._symbol_index[current_file]:
                        return self._symbol_index[current_file][symbol_name]
                
                # Search in all files
                for file_path, symbols in self._symbol_index.items():
                    if symbol_name in symbols:
                        return symbols[symbol_name]
                
                return None
                
        except Exception as e:
            self._logger.error(f"Failed to go to definition: {e}")
            return None
    
    def find_references(self, symbol_name: str, current_file: str) -> List[Tuple[str, int, int]]:
        """
        Find all references to a symbol.
        
        Args:
            symbol_name: Name of the symbol
            current_file: Current file path
            
        Returns:
            List of reference locations
        """
        try:
            with self._lock:
                references = self._symbol_references.get(symbol_name, [])
                
                # Filter out the definition
                filtered_references = []
                for file_path, line, col in references:
                    if file_path == current_file:
                        # Check if this is the definition
                        if file_path in self._symbol_index:
                            if symbol_name in self._symbol_index[file_path]:
                                symbol = self._symbol_index[file_path][symbol_name]
                                if line == symbol.line_number and col == symbol.column:
                                    continue
                    
                    filtered_references.append((file_path, line, col))
                
                return filtered_references
                
        except Exception as e:
            self._logger.error(f"Failed to find references: {e}")
            return []
    
    def get_symbol_info(self, symbol_name: str, current_file: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a symbol.
        
        Args:
            symbol_name: Name of the symbol
            current_file: Current file path
            
        Returns:
            Symbol information dictionary if found, None otherwise
        """
        try:
            with self._lock:
                # Find symbol definition
                symbol = self.go_to_definition(symbol_name, current_file, 1)
                if not symbol:
                    return None
                
                # Get references
                references = self.find_references(symbol_name, current_file)
                
                # Build info dictionary
                info = {
                    'name': symbol.name,
                    'type': symbol.symbol_type.value,
                    'file': symbol.file_path,
                    'line': symbol.line_number,
                    'column': symbol.column,
                    'language': symbol.language,
                    'scope': symbol.scope,
                    'parent': symbol.parent,
                    'metadata': symbol.metadata,
                    'references_count': len(references),
                    'references': references[:10],  # Limit to first 10 references
                    'children_count': len(symbol.children)
                }
                
                return info
                
        except Exception as e:
            self._logger.error(f"Failed to get symbol info: {e}")
            return None
    
    def get_navigation_context(self, file_path: str) -> NavigationContext:
        """
        Get or create navigation context for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Navigation context
        """
        if file_path not in self._navigation_contexts:
            self._navigation_contexts[file_path] = NavigationContext(
                current_file=file_path,
                current_line=1,
                current_column=1,
                cursor_position=(1, 1)
            )
        
        return self._navigation_contexts[file_path]
    
    def update_navigation_context(self, file_path: str, line: int, column: int):
        """
        Update navigation context with current position.
        
        Args:
            file_path: Path to the file
            line: Current line number
            column: Current column number
        """
        context = self.get_navigation_context(file_path)
        
        # Add current position to history
        if (file_path, line, column) != context.navigation_history[-1] if context.navigation_history else None:
            context.navigation_history.append((file_path, line, column))
            
            # Limit history size
            if len(context.navigation_history) > 100:
                context.navigation_history = context.navigation_history[-100:]
        
        # Update current position
        context.current_line = line
        context.current_column = column
        context.cursor_position = (line, column)
        
        # Update recent files
        if file_path in context.recent_files:
            context.recent_files.remove(file_path)
        context.recent_files.insert(0, file_path)
        
        # Limit recent files
        if len(context.recent_files) > 20:
            context.recent_files = context.recent_files[:20]
    
    def add_bookmark(self, file_path: str, line: int, column: int, description: str = ""):
        """
        Add a bookmark at the specified location.
        
        Args:
            file_path: Path to the file
            line: Line number
            column: Column number
            description: Optional bookmark description
        """
        context = self.get_navigation_context(file_path)
        
        bookmark = (file_path, line, column)
        if bookmark not in context.bookmarks:
            context.bookmarks.append(bookmark)
    
    def remove_bookmark(self, file_path: str, line: int, column: int):
        """
        Remove a bookmark at the specified location.
        
        Args:
            file_path: Path to the file
            line: Line number
            column: Column number
        """
        context = self.get_navigation_context(file_path)
        
        bookmark = (file_path, line, column)
        if bookmark in context.bookmarks:
            context.bookmarks.remove(bookmark)
    
    def get_navigation_summary(self) -> Dict[str, Any]:
        """Get a summary of navigation state."""
        return {
            "total_files_indexed": len(self._file_symbols),
            "total_symbols": sum(len(symbols) for symbols in self._file_symbols.values()),
            "total_references": sum(len(refs) for refs in self._symbol_references.values()),
            "navigation_contexts": len(self._navigation_contexts),
            "search_cache_size": len(self._search_cache),
            "supported_languages": list(self._parsers.keys())
        }
