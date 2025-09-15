"""
Configuration management for Nexlify.

This module provides configuration loading, validation, and management
with support for JSON configuration files and default values.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field, asdict

from .logger import get_logger


@dataclass
class RenderingConfig:
    """Rendering configuration settings."""
    window_width: int = 1280
    window_height: int = 720
    fullscreen: bool = False
    vsync: bool = True
    msaa_samples: int = 4
    max_fps: int = 60
    render_scale: float = 1.0


@dataclass
class AIConfig:
    """AI configuration settings."""
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    huggingface_model: str = ""
    local_model_path: str = ""
    max_tokens: int = 2048
    temperature: float = 0.7
    enable_fallback: bool = True


@dataclass
class AssetConfig:
    """Asset generation configuration."""
    output_directory: str = "assets"
    supported_formats: list = field(default_factory=lambda: [".obj", ".png", ".jpg", ".wav"])
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    auto_save: bool = True
    backup_enabled: bool = True


@dataclass
class PhysicsConfig:
    """Physics engine configuration."""
    gravity: list = field(default_factory=lambda: [0.0, -9.81, 0.0])
    time_step: float = 1.0 / 60.0
    max_sub_steps: int = 10
    solver_iterations: int = 10
    enable_debug_draw: bool = False


@dataclass
class AudioConfig:
    """Audio system configuration."""
    sample_rate: int = 44100
    channels: int = 2
    buffer_size: int = 1024
    master_volume: float = 1.0
    enable_3d_audio: bool = True


@dataclass
class InputConfig:
    """Input system configuration."""
    mouse_sensitivity: float = 1.0
    keyboard_repeat_delay: float = 0.5
    keyboard_repeat_rate: float = 0.1
    gamepad_deadzone: float = 0.1
    enable_touch_input: bool = False


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    log_file: str = "logs/nexlify.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_console: bool = True
    enable_file: bool = True


@dataclass
class NexlifyConfig:
    """Main configuration class containing all settings."""
    
    # Application settings
    app_name: str = "Nexlify"
    app_version: str = "1.0.0"
    debug_mode: bool = False
    
    # Core configurations
    rendering: RenderingConfig = field(default_factory=RenderingConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    assets: AssetConfig = field(default_factory=AssetConfig)
    physics: PhysicsConfig = field(default_factory=PhysicsConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    input: InputConfig = field(default_factory=InputConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Custom settings
    custom_settings: Dict[str, Any] = field(default_factory=dict)


class ConfigManager:
    """Manages application configuration loading and saving."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize the configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "nexlify_config.json"
        self.logger = get_logger(__name__)
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Config Manager initialized with directory: {self.config_dir}")
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.
        
        Returns:
            Configuration dictionary
        """
        try:
            if self.config_file.exists():
                self.logger.info(f"Loading configuration from: {self.config_file}")
                config = self._load_from_file()
            else:
                self.logger.info("📝 Creating default configuration")
                config = self._create_default_config()
                self.save_config(config)
            
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.logger.info("🔄 Falling back to default configuration")
            return self._create_default_config()
    
    def _load_from_file(self) -> Dict[str, Any]:
        """Load configuration from JSON file.
        
        Returns:
            Configuration dictionary
        """
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Convert to configuration objects
        config = NexlifyConfig()
        
        # Update with loaded data
        for key, value in config_data.items():
            if hasattr(config, key):
                if isinstance(value, dict) and hasattr(getattr(config, key), '__dataclass_fields__'):
                    # Handle nested dataclass objects
                    nested_obj = getattr(config, key)
                    for nested_key, nested_value in value.items():
                        if hasattr(nested_obj, nested_key):
                            setattr(nested_obj, nested_key, nested_value)
                else:
                    setattr(config, key, value)
        
        return asdict(config)
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration.
        
        Returns:
            Default configuration dictionary
        """
        config = NexlifyConfig()
        return asdict(config)
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup of existing config
            if self.config_file.exists():
                backup_file = self.config_file.with_suffix('.json.backup')
                self.config_file.rename(backup_file)
                self.logger.debug(f"📋 Created backup: {backup_file}")
            
            # Save new configuration
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Configuration saved to: {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration setting by dot-separated path.
        
        Args:
            key_path: Dot-separated path to setting (e.g., "rendering.window_width")
            default: Default value if setting not found
            
        Returns:
            Setting value or default
        """
        try:
            keys = key_path.split('.')
            config = self.load_config()
            
            value = config
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
            
        except Exception as e:
            self.logger.error(f"Failed to get setting {key_path}: {e}")
            return default
    
    def set_setting(self, key_path: str, value: Any) -> bool:
        """Set a configuration setting by dot-separated path.
        
        Args:
            key_path: Dot-separated path to setting
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            keys = key_path.split('.')
            config = self.load_config()
            
            # Navigate to the parent of the target key
            current = config
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[keys[-1]] = value
            
            # Save the updated configuration
            return self.save_config(config)
            
        except Exception as e:
            self.logger.error(f"Failed to set setting {key_path}: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration values.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Basic validation
            if 'rendering' in config:
                rendering = config['rendering']
                if rendering.get('window_width', 0) <= 0:
                    self.logger.error("Invalid window width")
                    return False
                if rendering.get('window_height', 0) <= 0:
                    self.logger.error("Invalid window height")
                    return False
            
            if 'ai' in config:
                ai = config['ai']
                if ai.get('max_tokens', 0) <= 0:
                    self.logger.error("Invalid max tokens")
                    return False
            
            self.logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
    
    def reload_config(self) -> Dict[str, Any]:
        """Reload configuration from file.
        
        Returns:
            Updated configuration dictionary
        """
        self.logger.info("🔄 Reloading configuration")
        return self.load_config()
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to a different location.
        
        Args:
            export_path: Path to export configuration to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            config = self.load_config()
            export_file = Path(export_path)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📤 Configuration exported to: {export_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export configuration: {e}")
            return False
