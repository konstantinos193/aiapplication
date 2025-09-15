"""
Main application class for Nexlify.

This class manages the application lifecycle, initialization,
and coordination between different engine systems.
"""

import sys
import logging
import time
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from .engine import GameEngine
from ..gui.game_design_ide import GameDesignIDE
from ..ai.ai_manager import AIManager
from ..physics.physics_engine import PhysicsEngine
from ..audio.audio_engine import AudioEngine
from ..scripting.scripting_engine import ScriptingEngine
from ..asset.asset_pipeline import AssetPipeline
from ..utils.logger import get_logger


class NexlifyApplication:
    """Main application class for Nexlify."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the Nexlify application.
        
        Args:
            config: Application configuration dictionary
        """
        self.config = config
        self.logger = get_logger(__name__)
        self.qt_app: Optional[QApplication] = None
        self.main_window: Optional[GameDesignIDE] = None
        self.game_engine: Optional[GameEngine] = None
        
        # Engine subsystems
        self.ai_manager: Optional[AIManager] = None
        self.physics_engine: Optional[PhysicsEngine] = None
        self.audio_engine: Optional[AudioEngine] = None
        self.scripting_engine: Optional[ScriptingEngine] = None
        self.asset_pipeline: Optional[AssetPipeline] = None
        
        self.is_running = False
        
        self.logger.info("Initializing Nexlify Application")
    
    def initialize(self) -> bool:
        """Initialize all application components.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Initialize Qt application
            if not self._init_qt():
                return False
            
            # Initialize engine subsystems
            if not self._init_engine_subsystems():
                return False
            
            # Initialize game engine
            if not self._init_game_engine():
                return False
            
            # Initialize main window
            if not self._init_main_window():
                return False
            
            # Update timer is now setup in _init_main_window after window is shown
            
            self.logger.info("Application initialization completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}", exc_info=True)
            return False
    
    def _global_exception_handler(self, exc_type, exc_value, exc_traceback):
        """Global exception handler to catch unhandled crashes."""
        self.logger.error("=== UNHANDLED CRASH DETECTED ===", exc_info=(exc_type, exc_value, exc_traceback))
        self.logger.error(f"Exception type: {exc_type}")
        self.logger.error(f"Exception value: {exc_value}")
        
        # Try to show error in GUI if possible
        try:
            if self.main_window:
                self.main_window.show_error_dialog(f"CRASH: {exc_type.__name__}: {exc_value}")
        except:
            pass
        
        # Don't exit - let the application try to recover
        self.logger.error("Application will attempt to continue...")
    
    def _init_qt(self) -> bool:
        """Initialize Qt application.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.qt_app = QApplication(sys.argv)
            self.qt_app.setApplicationName("Nexlify")
            self.qt_app.setApplicationVersion("1.0.0")
            self.qt_app.setOrganizationName("Nexlify")
            
            # Set application style
            self.qt_app.setStyle('Fusion')
            
            # Set up global exception handler
            sys.excepthook = self._global_exception_handler
            
            self.logger.info("Qt application initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Qt: {e}")
            return False
    
    def _init_engine_subsystems(self) -> bool:
        """Initialize engine subsystems.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize AI Manager
            self.ai_manager = AIManager(self.config.get('ai', {}))
            if not self.ai_manager.initialize(self.config.get('ai', {})):
                self.logger.error("Failed to initialize AI manager")
                return False
            
            # Initialize Physics Engine
            from ..physics.physics_engine import PhysicsConfig
            physics_config = PhysicsConfig()
            self.physics_engine = PhysicsEngine(physics_config)
            if not self.physics_engine.initialize():
                self.logger.error("Failed to initialize physics engine")
                return False
            
            # Initialize Audio Engine
            from ..audio.audio_engine import AudioConfig
            audio_config = AudioConfig()
            self.audio_engine = AudioEngine(audio_config)
            if not self.audio_engine.initialize():
                self.logger.error("Failed to initialize audio engine")
                return False
            
            # Initialize Scripting Engine
            from ..scripting.scripting_engine import ScriptingConfig
            scripting_config = ScriptingConfig()
            self.scripting_engine = ScriptingEngine(scripting_config)
            if not self.scripting_engine.initialize():
                self.logger.error("Failed to initialize scripting engine")
                return False
            
            # Initialize Asset Pipeline
            self.asset_pipeline = AssetPipeline(self.ai_manager)
            if not self.asset_pipeline.initialize():
                self.logger.error("Failed to initialize asset pipeline")
                return False
            
            self.logger.info("Engine subsystems initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize engine subsystems: {e}")
            return False
    
    def _init_game_engine(self) -> bool:
        """Initialize the game engine.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.game_engine = GameEngine(self.config)
            if not self.game_engine.initialize():
                return False
            
            self.logger.info("Game engine initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize game engine: {e}")
            return False
    
    def _init_main_window(self) -> bool:
        """Initialize the main window.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.main_window = GameDesignIDE(self.game_engine)
            self.main_window.show()
            
            # Setup update timer after main window is shown
            self._setup_update_timer()
            
            self.logger.info("Main window initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize main window: {e}")
            return False
    
    def _setup_update_timer(self):
        """Setup the update timer for the game loop."""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update)
        
        # Set update rate (60 FPS)
        update_interval = int(1000 / 60)  # milliseconds
        self.update_timer.start(update_interval)
        
        self.logger.info(f"Update timer started at {60} FPS")
    
    def _update(self):
        """Update game logic and rendering."""
        if self.game_engine and self.is_running:
            try:
                # Calculate delta time since last update
                current_time = time.time()
                if not hasattr(self, '_last_update_time'):
                    self._last_update_time = current_time
                
                delta_time = current_time - self._last_update_time
                self._last_update_time = current_time
                
                # Update game engine with delta time
                self.game_engine.update(delta_time)
                
                # Update engine subsystems
                if self.physics_engine:
                    self.physics_engine.step(delta_time)
                
                if self.audio_engine:
                    # Audio engine updates in its own thread
                    pass
                
                if self.scripting_engine:
                    self.scripting_engine.update_scripts(delta_time)
            except Exception as e:
                self.logger.error(f"Error in game update: {e}")
    
    def run(self) -> int:
        """Run the application main loop.
        
        Returns:
            Exit code
        """
        if not self.initialize():
            self.logger.error("Failed to initialize application")
            return 1
        
        self.is_running = True
        self.logger.info("Starting application main loop")
        
        try:
            # Start Qt event loop
            exit_code = self.qt_app.exec()
            self.logger.info("Application main loop finished")
            return exit_code
            
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}", exc_info=True)
            return 1
        
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the application and cleanup resources."""
        self.logger.info("Shutting down application")
        
        self.is_running = False
        
        if self.update_timer:
            self.update_timer.stop()
        
        # Shutdown engine subsystems
        if self.asset_pipeline:
            self.asset_pipeline.shutdown()
        
        if self.scripting_engine:
            self.scripting_engine.shutdown()
        
        if self.audio_engine:
            self.audio_engine.shutdown()
        
        if self.physics_engine:
            self.physics_engine.shutdown()
        
        if self.ai_manager:
            self.ai_manager.shutdown()
        
        if self.game_engine:
            self.game_engine.shutdown()
        
        if self.main_window:
            self.main_window.close()
        
        self.logger.info("Application shutdown completed")
