"""
Audio Engine for Nexlify Engine.

This module provides the main audio engine that handles:
- 3D spatial audio processing
- Real-time audio effects
- Audio streaming and compression
- Audio asset management
"""

import logging
import threading
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np

from .audio_source import AudioSource
from .audio_listener import AudioListener
from .audio_effects import AudioEffects
from ..utils.logger import get_logger


class AudioFormat(Enum):
    """Audio format types."""
    MONO_8 = "mono_8"
    MONO_16 = "mono_16"
    STEREO_8 = "stereo_8"
    STEREO_16 = "stereo_16"
    MONO_FLOAT = "mono_float"
    STEREO_FLOAT = "stereo_float"


@dataclass
class AudioConfig:
    """Audio engine configuration."""
    sample_rate: int = 44100
    buffer_size: int = 1024
    channels: int = 2
    format: AudioFormat = AudioFormat.STEREO_FLOAT
    enable_3d: bool = True
    enable_effects: bool = True
    max_sources: int = 256
    max_effects: int = 64
    doppler_factor: float = 1.0
    speed_of_sound: float = 343.0


@dataclass
class AudioStats:
    """Audio engine statistics."""
    fps: float = 0.0
    update_time: float = 0.0
    active_sources: int = 0
    total_sources: int = 0
    active_effects: int = 0
    memory_used: int = 0
    cpu_usage: float = 0.0


class AudioEngine:
    """Main audio engine class."""
    
    def __init__(self, config: AudioConfig = None):
        self.config = config or AudioConfig()
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Audio sources and listeners
        self.audio_sources: Dict[int, AudioSource] = {}
        self.audio_listeners: Dict[int, AudioListener] = {}
        self.next_source_id = 1
        self.next_listener_id = 1
        
        # Audio effects
        self.audio_effects: Optional[AudioEffects] = None
        
        # Performance tracking
        self.stats = AudioStats()
        self.last_update_time = time.time()
        self.update_count = 0
        
        # Threading
        self.audio_thread: Optional[threading.Thread] = None
        self.is_running = False
        self.shutdown_event = threading.Event()
        
        # Audio processing
        self.audio_buffer = np.zeros((self.config.buffer_size, self.config.channels), dtype=np.float32)
        
    def initialize(self) -> bool:
        """Initialize the audio engine.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing audio engine...")
            
            # Initialize audio effects
            self.audio_effects = AudioEffects(self.config)
            if not self.audio_effects.initialize():
                self.logger.error("Failed to initialize audio effects")
                return False
            
            # TODO: Initialize audio backend
            # This would involve:
            # - Setting up audio device
            # - Creating audio context
            # - Configuring audio format
            
            self.is_initialized = True
            self.logger.info("✅ Audio engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize audio engine: {e}", exc_info=True)
            return False
    
    def start(self):
        """Start the audio engine."""
        if not self.is_initialized:
            self.logger.error("Audio engine not initialized")
            return
        
        self.is_running = True
        self.shutdown_event.clear()
        
        # Start audio processing thread
        self.audio_thread = threading.Thread(target=self._audio_thread_func, daemon=True)
        self.audio_thread.start()
        
        self.logger.info("Audio engine started")
    
    def stop(self):
        """Stop the audio engine."""
        self.is_running = False
        self.shutdown_event.set()
        
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join(timeout=1.0)
        
        self.logger.info("Audio engine stopped")
    
    def _audio_thread_func(self):
        """Audio processing thread function."""
        while self.is_running and not self.shutdown_event.is_set():
            try:
                start_time = time.time()
                
                # Process audio
                self._process_audio()
                
                # Update statistics
                self._update_stats()
                
                # Sleep to maintain target frame rate
                elapsed = time.time() - start_time
                target_time = 1.0 / 60.0  # 60 FPS
                sleep_time = max(0, target_time - elapsed)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
            except Exception as e:
                self.logger.error(f"Error in audio thread: {e}", exc_info=True)
    
    def _process_audio(self):
        """Process audio for one frame."""
        # Clear audio buffer
        self.audio_buffer.fill(0.0)
        
        # Process all active audio sources
        for source in self.audio_sources.values():
            if source.is_playing():
                # Get audio data from source
                audio_data = source.get_audio_data(self.config.buffer_size)
                
                if audio_data is not None:
                    # Apply 3D spatial processing
                    if self.config.enable_3d:
                        audio_data = self._apply_3d_processing(source, audio_data)
                    
                    # Apply audio effects
                    if self.config.enable_effects and self.audio_effects:
                        audio_data = self.audio_effects.process_audio(audio_data, source)
                    
                    # Mix into main buffer
                    self._mix_audio(audio_data)
        
        # Output audio buffer
        self._output_audio()
    
    def _apply_3d_processing(self, source: AudioSource, audio_data: np.ndarray) -> np.ndarray:
        """Apply 3D spatial audio processing.
        
        Args:
            source: Audio source
            audio_data: Input audio data
            
        Returns:
            Processed audio data
        """
        # TODO: Implement 3D spatial audio processing
        # This would involve:
        # - Distance attenuation
        # - Doppler effect
        # - HRTF (Head-Related Transfer Function)
        # - Reverb based on environment
        
        # For now, apply simple distance attenuation
        if source.is_3d():
            distance = source.get_distance_to_listener()
            if distance > 0:
                # Simple inverse square law
                attenuation = 1.0 / (1.0 + distance * 0.1)
                audio_data *= attenuation
        
        return audio_data
    
    def _mix_audio(self, audio_data: np.ndarray):
        """Mix audio data into the main buffer.
        
        Args:
            audio_data: Audio data to mix
        """
        # Ensure audio data has correct shape
        if audio_data.shape[1] != self.config.channels:
            # Convert mono to stereo if needed
            if audio_data.shape[1] == 1 and self.config.channels == 2:
                audio_data = np.repeat(audio_data, 2, axis=1)
        
        # Mix audio data
        self.audio_buffer += audio_data
        
        # Clamp to prevent clipping
        self.audio_buffer = np.clip(self.audio_buffer, -1.0, 1.0)
    
    def _output_audio(self):
        """Output the audio buffer to the audio device."""
        # TODO: Implement actual audio output
        # This would involve:
        # - Converting to device format
        # - Sending to audio device
        # - Handling underruns/overruns
        
        pass
    
    def _update_stats(self):
        """Update audio engine statistics."""
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        
        if delta_time > 0:
            self.stats.fps = 1.0 / delta_time
        
        self.stats.update_time = delta_time * 1000.0  # Convert to milliseconds
        self.stats.active_sources = sum(1 for source in self.audio_sources.values() if source.is_playing())
        self.stats.total_sources = len(self.audio_sources)
        self.stats.active_effects = len(self.audio_effects.get_active_effects()) if self.audio_effects else 0
        
        self.last_update_time = current_time
        self.update_count += 1
    
    def create_audio_source(self, audio_data: np.ndarray = None, 
                           position: List[float] = None, is_3d: bool = True) -> int:
        """Create a new audio source.
        
        Args:
            audio_data: Audio data (optional)
            position: 3D position [x, y, z] (optional)
            is_3d: Whether this is a 3D audio source
            
        Returns:
            Audio source ID
        """
        source_id = self.next_source_id
        self.next_source_id += 1
        
        source = AudioSource(source_id, audio_data, position, is_3d)
        self.audio_sources[source_id] = source
        
        self.logger.debug(f"Created audio source: {source_id}")
        return source_id
    
    def destroy_audio_source(self, source_id: int) -> bool:
        """Destroy an audio source.
        
        Args:
            source_id: Audio source ID
            
        Returns:
            True if source destroyed successfully, False otherwise
        """
        if source_id in self.audio_sources:
            source = self.audio_sources[source_id]
            source.stop()
            del self.audio_sources[source_id]
            
            self.logger.debug(f"Destroyed audio source: {source_id}")
            return True
        
        return False
    
    def get_audio_source(self, source_id: int) -> Optional[AudioSource]:
        """Get an audio source by ID.
        
        Args:
            source_id: Audio source ID
            
        Returns:
            Audio source or None if not found
        """
        return self.audio_sources.get(source_id)
    
    def create_audio_listener(self, position: List[float] = None, 
                             orientation: List[float] = None) -> int:
        """Create a new audio listener.
        
        Args:
            position: 3D position [x, y, z] (optional)
            orientation: 3D orientation [x, y, z] (optional)
            
        Returns:
            Audio listener ID
        """
        listener_id = self.next_listener_id
        self.next_listener_id += 1
        
        listener = AudioListener(listener_id, position, orientation)
        self.audio_listeners[listener_id] = listener
        
        self.logger.debug(f"Created audio listener: {listener_id}")
        return listener_id
    
    def destroy_audio_listener(self, listener_id: int) -> bool:
        """Destroy an audio listener.
        
        Args:
            listener_id: Audio listener ID
            
        Returns:
            True if listener destroyed successfully, False otherwise
        """
        if listener_id in self.audio_listeners:
            del self.audio_listeners[listener_id]
            
            self.logger.debug(f"Destroyed audio listener: {listener_id}")
            return True
        
        return False
    
    def get_audio_listener(self, listener_id: int) -> Optional[AudioListener]:
        """Get an audio listener by ID.
        
        Args:
            listener_id: Audio listener ID
            
        Returns:
            Audio listener or None if not found
        """
        return self.audio_listeners.get(listener_id)
    
    def set_global_volume(self, volume: float):
        """Set the global audio volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        
        # Apply to all audio sources
        for source in self.audio_sources.values():
            source.set_volume(volume)
        
        self.logger.debug(f"Set global volume: {volume}")
    
    def set_doppler_factor(self, factor: float):
        """Set the Doppler effect factor.
        
        Args:
            factor: Doppler factor
        """
        self.config.doppler_factor = factor
        self.logger.debug(f"Set Doppler factor: {factor}")
    
    def set_speed_of_sound(self, speed: float):
        """Set the speed of sound.
        
        Args:
            speed: Speed of sound in m/s
        """
        self.config.speed_of_sound = speed
        self.logger.debug(f"Set speed of sound: {speed}")
    
    def get_stats(self) -> AudioStats:
        """Get audio engine statistics.
        
        Returns:
            Current audio statistics
        """
        return self.stats
    
    def get_config(self) -> AudioConfig:
        """Get audio engine configuration.
        
        Returns:
            Current audio configuration
        """
        return self.config
    
    def set_config(self, config: AudioConfig):
        """Set audio engine configuration.
        
        Args:
            config: New audio configuration
        """
        self.config = config
        
        # Recreate audio buffer with new size
        self.audio_buffer = np.zeros((self.config.buffer_size, self.config.channels), dtype=np.float32)
        
        self.logger.info("Audio engine configuration updated")
    
    def shutdown(self):
        """Shutdown the audio engine."""
        if self.is_initialized:
            self.logger.info("Shutting down audio engine...")
            
            # Stop audio engine
            self.stop()
            
            # Clear all audio sources and listeners
            self.audio_sources.clear()
            self.audio_listeners.clear()
            
            # Shutdown audio effects
            if self.audio_effects:
                self.audio_effects.shutdown()
                self.audio_effects = None
            
            self.is_initialized = False
            self.logger.info("✅ Audio engine shutdown complete")
