"""
Scripting Engine for Nexlify Engine.

This module provides Python-based scripting functionality including:
- Component scripting
- Game logic scripting
- Event handling
- Hot reloading
- Script debugging
"""

import os
import sys
import logging
import importlib
import threading
import time
from typing import Dict, Any, Optional, List, Callable, Type
from dataclasses import dataclass
from pathlib import Path
import inspect

from .script_component import ScriptComponent
from .event_system import EventSystem
from ..core.component import Component
from ..utils.logger import get_logger


@dataclass
class ScriptInfo:
    """Script information."""
    name: str
    file_path: str
    module: Any
    class_type: Type[ScriptComponent]
    last_modified: float
    is_loaded: bool = False


@dataclass
class ScriptingConfig:
    """Scripting engine configuration."""
    script_paths: List[str] = None
    enable_hot_reload: bool = True
    hot_reload_interval: float = 1.0
    enable_debugging: bool = True
    max_script_instances: int = 1000
    auto_reload_on_error: bool = True


class ScriptingEngine:
    """Main scripting engine class."""
    
    def __init__(self, config: ScriptingConfig = None):
        self.config = config or ScriptingConfig()
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Script management
        self.scripts: Dict[str, ScriptInfo] = {}
        self.script_instances: Dict[int, ScriptComponent] = {}
        self.next_instance_id = 1
        
        # Event system
        self.event_system: Optional[EventSystem] = None
        
        # Hot reloading
        self.hot_reload_thread: Optional[threading.Thread] = None
        self.hot_reload_running = False
        self.watched_files: Dict[str, float] = {}
        
        # Performance tracking
        self.script_update_time = 0.0
        self.script_count = 0
        
        # Default script paths
        if self.config.script_paths is None:
            self.config.script_paths = [
                "scripts",
                "assets/scripts",
                "src/scripting/scripts"
            ]
        
    def initialize(self) -> bool:
        """Initialize the scripting engine.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing scripting engine...")
            
            # Initialize event system
            self.event_system = EventSystem()
            if not self.event_system.initialize():
                self.logger.error("Failed to initialize event system")
                return False
            
            # Create script directories
            for script_path in self.config.script_paths:
                Path(script_path).mkdir(parents=True, exist_ok=True)
            
            # Load all scripts
            self._load_all_scripts()
            
            # Start hot reloading if enabled
            if self.config.enable_hot_reload:
                self._start_hot_reload()
            
            self.is_initialized = True
            self.logger.info("✅ Scripting engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize scripting engine: {e}", exc_info=True)
            return False
    
    def _load_all_scripts(self):
        """Load all scripts from script paths."""
        for script_path in self.config.script_paths:
            self._load_scripts_from_path(script_path)
    
    def _load_scripts_from_path(self, script_path: str):
        """Load scripts from a specific path.
        
        Args:
            script_path: Path to load scripts from
        """
        try:
            script_dir = Path(script_path)
            if not script_dir.exists():
                return
            
            # Add to Python path
            if str(script_dir) not in sys.path:
                sys.path.insert(0, str(script_dir))
            
            # Find all Python files
            for py_file in script_dir.glob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                
                self._load_script_file(py_file)
                
        except Exception as e:
            self.logger.error(f"Error loading scripts from {script_path}: {e}")
    
    def _load_script_file(self, file_path: Path):
        """Load a single script file.
        
        Args:
            file_path: Path to script file
        """
        try:
            script_name = file_path.stem
            module_name = f"scripts.{script_name}"
            
            # Check if already loaded
            if script_name in self.scripts:
                return
            
            # Import module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                self.logger.error(f"Could not load spec for {file_path}")
                return
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find script component classes
            script_classes = []
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, ScriptComponent) and 
                    obj != ScriptComponent and 
                    obj.__module__ == module.__name__):
                    script_classes.append(obj)
            
            if not script_classes:
                self.logger.warning(f"No script component classes found in {file_path}")
                return
            
            # Register each script class
            for script_class in script_classes:
                script_info = ScriptInfo(
                    name=script_class.__name__,
                    file_path=str(file_path),
                    module=module,
                    class_type=script_class,
                    last_modified=file_path.stat().st_mtime,
                    is_loaded=True
                )
                
                self.scripts[script_class.__name__] = script_info
                self.watched_files[str(file_path)] = file_path.stat().st_mtime
                
                self.logger.info(f"Loaded script: {script_class.__name__}")
                
        except Exception as e:
            self.logger.error(f"Error loading script file {file_path}: {e}")
    
    def _start_hot_reload(self):
        """Start the hot reload thread."""
        if self.hot_reload_running:
            return
        
        self.hot_reload_running = True
        self.hot_reload_thread = threading.Thread(target=self._hot_reload_loop, daemon=True)
        self.hot_reload_thread.start()
        
        self.logger.info("Hot reload started")
    
    def _stop_hot_reload(self):
        """Stop the hot reload thread."""
        self.hot_reload_running = False
        if self.hot_reload_thread and self.hot_reload_thread.is_alive():
            self.hot_reload_thread.join(timeout=1.0)
        
        self.logger.info("Hot reload stopped")
    
    def _hot_reload_loop(self):
        """Hot reload monitoring loop."""
        while self.hot_reload_running:
            try:
                self._check_for_script_changes()
                time.sleep(self.config.hot_reload_interval)
            except Exception as e:
                self.logger.error(f"Error in hot reload loop: {e}")
    
    def _check_for_script_changes(self):
        """Check for script file changes and reload if necessary."""
        for file_path, last_modified in self.watched_files.items():
            try:
                if os.path.exists(file_path):
                    current_modified = os.path.getmtime(file_path)
                    if current_modified > last_modified:
                        self.logger.info(f"Hot reloading script: {file_path}")
                        self._reload_script_file(Path(file_path))
                        self.watched_files[file_path] = current_modified
            except Exception as e:
                self.logger.error(f"Error checking script changes for {file_path}: {e}")
    
    def _reload_script_file(self, file_path: Path):
        """Reload a script file.
        
        Args:
            file_path: Path to script file
        """
        try:
            script_name = file_path.stem
            
            # Find scripts from this file
            scripts_to_reload = []
            for script_info in self.scripts.values():
                if script_info.file_path == str(file_path):
                    scripts_to_reload.append(script_info)
            
            # Reload each script
            for script_info in scripts_to_reload:
                self._reload_script(script_info)
                
        except Exception as e:
            self.logger.error(f"Error reloading script file {file_path}: {e}")
    
    def _reload_script(self, script_info: ScriptInfo):
        """Reload a specific script.
        
        Args:
            script_info: Script information
        """
        try:
            # Reload the module
            importlib.reload(script_info.module)
            
            # Update script info
            script_info.last_modified = os.path.getmtime(script_info.file_path)
            
            # Notify existing instances
            for instance in self.script_instances.values():
                if instance.__class__.__name__ == script_info.name:
                    instance.on_script_reloaded()
            
            self.logger.info(f"Reloaded script: {script_info.name}")
            
        except Exception as e:
            self.logger.error(f"Error reloading script {script_info.name}: {e}")
    
    def create_script_instance(self, script_name: str, game_object=None) -> Optional[ScriptComponent]:
        """Create a new script instance.
        
        Args:
            script_name: Name of the script class
            game_object: GameObject to attach to (optional)
            
        Returns:
            Script component instance or None if failed
        """
        if script_name not in self.scripts:
            self.logger.error(f"Script not found: {script_name}")
            return None
        
        if len(self.script_instances) >= self.config.max_script_instances:
            self.logger.error("Maximum script instances reached")
            return None
        
        try:
            script_info = self.scripts[script_name]
            instance_id = self.next_instance_id
            self.next_instance_id += 1
            
            # Create script instance
            script_instance = script_info.class_type()
            script_instance.set_instance_id(instance_id)
            script_instance.set_game_object(game_object)
            
            # Initialize script
            script_instance.initialize()
            
            # Store instance
            self.script_instances[instance_id] = script_instance
            
            self.logger.debug(f"Created script instance: {script_name} (ID: {instance_id})")
            return script_instance
            
        except Exception as e:
            self.logger.error(f"Error creating script instance {script_name}: {e}")
            return None
    
    def destroy_script_instance(self, instance_id: int) -> bool:
        """Destroy a script instance.
        
        Args:
            instance_id: Script instance ID
            
        Returns:
            True if instance destroyed successfully, False otherwise
        """
        if instance_id not in self.script_instances:
            return False
        
        try:
            script_instance = self.script_instances[instance_id]
            script_instance.shutdown()
            del self.script_instances[instance_id]
            
            self.logger.debug(f"Destroyed script instance: {instance_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error destroying script instance {instance_id}: {e}")
            return False
    
    def get_script_instance(self, instance_id: int) -> Optional[ScriptComponent]:
        """Get a script instance by ID.
        
        Args:
            instance_id: Script instance ID
            
        Returns:
            Script instance or None if not found
        """
        return self.script_instances.get(instance_id)
    
    def update_scripts(self, delta_time: float):
        """Update all script instances.
        
        Args:
            delta_time: Time since last update
        """
        if not self.is_initialized:
            return
        
        start_time = time.time()
        
        try:
            # Update all script instances
            for script_instance in self.script_instances.values():
                if script_instance.is_enabled():
                    script_instance.update(delta_time)
            
            # Update event system
            if self.event_system:
                self.event_system.update(delta_time)
            
        except Exception as e:
            self.logger.error(f"Error updating scripts: {e}")
        
        # Update performance stats
        self.script_update_time = time.time() - start_time
        self.script_count = len(self.script_instances)
    
    def get_available_scripts(self) -> List[str]:
        """Get list of available script names.
        
        Returns:
            List of script names
        """
        return list(self.scripts.keys())
    
    def get_script_info(self, script_name: str) -> Optional[ScriptInfo]:
        """Get script information.
        
        Args:
            script_name: Name of the script
            
        Returns:
            Script information or None if not found
        """
        return self.scripts.get(script_name)
    
    def get_event_system(self) -> Optional[EventSystem]:
        """Get the event system.
        
        Returns:
            Event system instance
        """
        return self.event_system
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scripting engine statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "script_count": len(self.scripts),
            "instance_count": len(self.script_instances),
            "update_time": self.script_update_time,
            "hot_reload_enabled": self.config.enable_hot_reload,
            "hot_reload_running": self.hot_reload_running
        }
    
    def shutdown(self):
        """Shutdown the scripting engine."""
        if self.is_initialized:
            self.logger.info("Shutting down scripting engine...")
            
            # Stop hot reloading
            self._stop_hot_reload()
            
            # Shutdown all script instances
            for script_instance in self.script_instances.values():
                try:
                    script_instance.shutdown()
                except Exception as e:
                    self.logger.error(f"Error shutting down script instance: {e}")
            
            self.script_instances.clear()
            
            # Shutdown event system
            if self.event_system:
                self.event_system.shutdown()
                self.event_system = None
            
            # Clear scripts
            self.scripts.clear()
            self.watched_files.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Scripting engine shutdown complete")
