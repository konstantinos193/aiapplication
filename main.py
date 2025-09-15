#!/usr/bin/env python3
"""
Nexlify - AI-Driven Game Engine with Asset Generation
Main Application Entry Point

This is the main entry point for the Nexlify Python application.
It handles initialization, configuration loading, and starts the main GUI.
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.application import NexlifyApplication
from src.utils.logger import setup_logging
from src.utils.config_manager import ConfigManager
from src.utils.error_handler import ErrorHandler


def main():
    """Main application entry point."""
    try:
        # Setup logging first
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Nexlify Application")
        
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Initialize error handler
        error_handler = ErrorHandler()
        
        # Create and run application
        app = NexlifyApplication(config)
        exit_code = app.run()
        
        logger.info(f"Nexlify Application finished with exit code: {exit_code}")
        return exit_code
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
