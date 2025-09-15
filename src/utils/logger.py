"""
Logging system for Nexlify.

This module provides a centralized logging system with:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- File and console output
- Timestamp formatting
- Thread safety
- Log rotation
"""

import logging
import logging.handlers
import sys
import os
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """Setup the logging system.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup log files to keep
    """
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
            print(f"Logging to file: {log_file}")
            
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
    
    # Set specific logger levels
    logging.getLogger('PyQt6').setLevel(logging.WARNING)
    logging.getLogger('OpenGL').setLevel(logging.WARNING)
    
    print(f"Logging initialized at level: {log_level}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for console."""
    
    # Color codes for different log levels
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_colored_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None
) -> None:
    """Setup logging with colored console output.
    
    Args:
        log_level: Logging level
        log_file: Optional log file path
    """
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create colored formatter for console
    colored_formatter = ColoredFormatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Create standard formatter for file
    file_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
            
            print(f"Logging to file: {log_file}")
            
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
    
    # Set specific logger levels
    logging.getLogger('PyQt6').setLevel(logging.WARNING)
    logging.getLogger('OpenGL').setLevel(logging.WARNING)
    
    print(f"Colored logging initialized at level: {log_level}")


# Convenience function for quick logging setup
def quick_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Quick setup for a logger with basic configuration.
    
    Args:
        name: Logger name
        level: Log level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Add console handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt='%(levelname)-8s | %(name)-20s | %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
