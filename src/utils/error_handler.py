"""
Error handling system for Nexlify.

This module provides centralized error handling with:
- Error capture and logging
- User-friendly error messages
- Error recovery strategies
- Error reporting and analytics
"""

import sys
import traceback
import logging
from typing import Optional, Callable, Dict, Any, List
from datetime import datetime
from pathlib import Path

from .logger import get_logger


class ErrorInfo:
    """Information about an error."""
    
    def __init__(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Initialize error information.
        
        Args:
            error: The exception that occurred
            context: Additional context information
        """
        self.error = error
        self.error_type = type(error).__name__
        self.error_message = str(error)
        self.timestamp = datetime.now()
        self.traceback = traceback.format_exc()
        self.context = context or {}
        
        # Extract file and line information
        tb = traceback.extract_tb(error.__traceback__)
        if tb:
            self.file = tb[-1].filename
            self.line = tb[-1].lineno
            self.function = tb[-1].name
        else:
            self.file = "unknown"
            self.line = 0
            self.function = "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error info to dictionary.
        
        Returns:
            Dictionary representation of error info
        """
        return {
            'error_type': self.error_type,
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat(),
            'file': self.file,
            'line': self.line,
            'function': self.function,
            'traceback': self.traceback,
            'context': self.context
        }
    
    def __str__(self) -> str:
        """String representation of error info."""
        return f"{self.error_type}: {self.error_message} at {self.file}:{self.line}"


class ErrorHandler:
    """Centralized error handling system."""
    
    def __init__(self, log_errors: bool = True, save_errors: bool = True):
        """Initialize the error handler.
        
        Args:
            log_errors: Whether to log errors
            save_errors: Whether to save errors to file
        """
        self.log_errors = log_errors
        self.save_errors = save_errors
        self.logger = get_logger(__name__)
        
        # Error storage
        self.errors: List[ErrorInfo] = []
        self.max_errors = 1000
        
        # Error callbacks
        self.error_callbacks: List[Callable[[ErrorInfo], None]] = []
        
        # Setup error file
        if self.save_errors:
            self.error_file = Path("logs/errors.log")
            self.error_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Error Handler initialized")
    
    def handle_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> ErrorInfo:
        """Handle an error and return error information.
        
        Args:
            error: The exception that occurred
            context: Additional context information
            
        Returns:
            Error information object
        """
        error_info = ErrorInfo(error, context)
        
        # Store error
        self.errors.append(error_info)
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)  # Remove oldest error
        
        # Log error
        if self.log_errors:
            self._log_error(error_info)
        
        # Save error to file
        if self.save_errors:
            self._save_error(error_info)
        
        # Call error callbacks
        self._call_error_callbacks(error_info)
        
        return error_info
    
    def _log_error(self, error_info: ErrorInfo):
        """Log an error.
        
        Args:
            error_info: Error information to log
        """
        self.logger.error(
            f"{error_info.error_type}: {error_info.error_message}",
            extra={
                'file': error_info.file,
                'line': error_info.line,
                'function': error_info.function,
                'context': error_info.context
            }
        )
        
        # Log traceback at debug level
        self.logger.debug(f"Traceback:\n{error_info.traceback}")
    
    def _save_error(self, error_info: ErrorInfo):
        """Save error to file.
        
        Args:
            error_info: Error information to save
        """
        try:
            with open(self.error_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"Timestamp: {error_info.timestamp}\n")
                f.write(f"Error Type: {error_info.error_type}\n")
                f.write(f"Error Message: {error_info.error_message}\n")
                f.write(f"File: {error_info.file}:{error_info.line}\n")
                f.write(f"Function: {error_info.function}\n")
                f.write(f"Context: {error_info.context}\n")
                f.write(f"Traceback:\n{error_info.traceback}\n")
                f.write(f"{'='*80}\n")
                
        except Exception as e:
            self.logger.error(f"Failed to save error to file: {e}")
    
    def _call_error_callbacks(self, error_info: ErrorInfo):
        """Call registered error callbacks.
        
        Args:
            error_info: Error information to pass to callbacks
        """
        for callback in self.error_callbacks:
            try:
                callback(error_info)
            except Exception as e:
                self.logger.error(f"Error in error callback: {e}")
    
    def add_error_callback(self, callback: Callable[[ErrorInfo], None]):
        """Add an error callback function.
        
        Args:
            callback: Function to call when errors occur
        """
        self.error_callbacks.append(callback)
        self.logger.debug(f"Added error callback: {callback.__name__}")
    
    def remove_error_callback(self, callback: Callable[[ErrorInfo], None]):
        """Remove an error callback function.
        
        Args:
            callback: Function to remove
        """
        if callback in self.error_callbacks:
            self.error_callbacks.remove(callback)
            self.logger.debug(f"Removed error callback: {callback.__name__}")
    
    def get_recent_errors(self, count: int = 10) -> List[ErrorInfo]:
        """Get recent errors.
        
        Args:
            count: Number of recent errors to return
            
        Returns:
            List of recent errors
        """
        return self.errors[-count:]
    
    def get_errors_by_type(self, error_type: str) -> List[ErrorInfo]:
        """Get errors by type.
        
        Args:
            error_type: Type of error to filter by
            
        Returns:
            List of errors of the specified type
        """
        return [error for error in self.errors if error.error_type == error_type]
    
    def clear_errors(self):
        """Clear all stored errors."""
        self.errors.clear()
        self.logger.info("Cleared all stored errors")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of all errors.
        
        Returns:
            Error summary dictionary
        """
        if not self.errors:
            return {
                'total_errors': 0,
                'error_types': {},
                'recent_errors': []
            }
        
        # Count error types
        error_types = {}
        for error in self.errors:
            error_types[error.error_type] = error_types.get(error.error_type, 0) + 1
        
        return {
            'total_errors': len(self.errors),
            'error_types': error_types,
            'recent_errors': [error.to_dict() for error in self.errors[-5:]]
        }
    
    def setup_global_exception_handler(self):
        """Setup global exception handler for uncaught exceptions."""
        def global_exception_handler(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                # Don't handle keyboard interrupts
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            # Create error info
            error_info = ErrorInfo(exc_value, {
                'uncaught': True,
                'exc_type': exc_type.__name__
            })
            
            # Handle the error
            self.handle_error(exc_value, {
                'uncaught': True,
                'exc_type': exc_type.__name__
            })
        
        sys.excepthook = global_exception_handler
        self.logger.info("Global exception handler installed")


class ErrorRecovery:
    """Error recovery strategies."""
    
    @staticmethod
    def retry_operation(operation: Callable, max_retries: int = 3, 
                       delay: float = 1.0, backoff: float = 2.0):
        """Retry an operation with exponential backoff.
        
        Args:
            operation: Function to retry
            max_retries: Maximum number of retries
            delay: Initial delay between retries
            backoff: Multiplier for delay after each retry
            
        Returns:
            Result of operation if successful
            
        Raises:
            Exception: Last exception if all retries fail
        """
        import time
        
        last_exception = None
        current_delay = delay
        
        for attempt in range(max_retries + 1):
            try:
                return operation()
            except Exception as e:
                last_exception = e
                
                if attempt < max_retries:
                    time.sleep(current_delay)
                    current_delay *= backoff
                else:
                    break
        
        raise last_exception
    
    @staticmethod
    def fallback_operation(primary_operation: Callable, fallback_operation: Callable):
        """Try primary operation, fall back to secondary if it fails.
        
        Args:
            primary_operation: Primary function to try
            fallback_operation: Fallback function if primary fails
            
        Returns:
            Result of primary or fallback operation
        """
        try:
            return primary_operation()
        except Exception:
            return fallback_operation()


# Global error handler instance
_global_error_handler: Optional[ErrorHandler] = None


def get_global_error_handler() -> ErrorHandler:
    """Get the global error handler instance.
    
    Returns:
        Global error handler
    """
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
        _global_error_handler.setup_global_exception_handler()
    return _global_error_handler


def handle_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> ErrorInfo:
    """Handle an error using the global error handler.
    
    Args:
        error: The exception that occurred
        context: Additional context information
        
    Returns:
        Error information object
    """
    return get_global_error_handler().handle_error(error, context)
