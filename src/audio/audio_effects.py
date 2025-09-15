"""
Audio Effects for Nexlify Engine.

This module provides audio effects processing including
reverb, filters, and other audio processing effects.
"""

import logging
import numpy as np
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from .audio_source import AudioSource
from ..utils.logger import get_logger


@dataclass
class AudioEffect:
    """Audio effect configuration."""
    name: str
    enabled: bool = True
    parameters: Dict[str, Any] = None


class AudioEffects:
    """Audio effects processing system."""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Active effects
        self.active_effects: List[AudioEffect] = []
        
        # Effect parameters
        self.reverb_room_size = 0.5
        self.reverb_damping = 0.5
        self.reverb_wet_mix = 0.3
        self.reverb_dry_mix = 0.7
        
        self.lowpass_cutoff = 20000.0
        self.highpass_cutoff = 20.0
        self.bandpass_center = 1000.0
        self.bandpass_bandwidth = 100.0
        
        self.distortion_gain = 1.0
        self.distortion_threshold = 0.5
        
        self.echo_delay = 0.1
        self.echo_decay = 0.5
        self.echo_feedback = 0.3
        
        # Default sample rate
        self.sample_rate = 44100
        
        # Performance tracking
        self.effects_processed = 0
        self.processing_time = 0.0
        
    def initialize(self) -> bool:
        """Initialize the audio effects system.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing audio effects...")
            
            # Clear active effects
            self.active_effects.clear()
            
            self.is_initialized = True
            self.logger.info("✅ Audio effects initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize audio effects: {e}")
            return False
    
    def process_audio(self, audio_data: np.ndarray, source: AudioSource) -> np.ndarray:
        """Process audio data with effects.
        
        Args:
            audio_data: Input audio data
            source: Audio source
            
        Returns:
            Processed audio data
        """
        if not self.is_initialized or audio_data is None:
            return audio_data
        
        try:
            processed_data = audio_data.copy()
            
            # Apply reverb if enabled
            if source.is_reverb_enabled():
                processed_data = self._apply_reverb(processed_data, source)
            
            # Apply lowpass filter if enabled
            if source.is_lowpass_enabled():
                processed_data = self._apply_lowpass(processed_data, source)
            
            # Apply other effects based on source properties
            processed_data = self._apply_other_effects(processed_data, source)
            
            self.effects_processed += 1
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error processing audio effects: {e}")
            return audio_data
    
    def _apply_reverb(self, audio_data: np.ndarray, source: AudioSource) -> np.ndarray:
        """Apply reverb effect to audio data.
        
        Args:
            audio_data: Input audio data
            source: Audio source
            
        Returns:
            Audio data with reverb applied
        """
        try:
            # Simple reverb implementation using delay lines
            # In a real audio engine, this would use proper reverb algorithms
            
            reverb_mix = source.get_reverb_mix()
            if reverb_mix <= 0:
                return audio_data
            
            # Create reverb buffer
            reverb_buffer = np.zeros_like(audio_data)
            
            # Simple delay-based reverb
            delay_samples = int(0.1 * self.sample_rate)  # 100ms delay
            
            if delay_samples < len(audio_data):
                # Apply delayed signal
                reverb_buffer[delay_samples:] += audio_data[:-delay_samples] * 0.3
                
                # Apply feedback
                reverb_buffer[delay_samples:] += reverb_buffer[:-delay_samples] * 0.2
            
            # Mix reverb with original signal
            wet_signal = reverb_buffer * reverb_mix
            dry_signal = audio_data * (1.0 - reverb_mix)
            
            return wet_signal + dry_signal
            
        except Exception as e:
            self.logger.error(f"Error applying reverb: {e}")
            return audio_data
    
    def _apply_lowpass(self, audio_data: np.ndarray, source: AudioSource) -> np.ndarray:
        """Apply lowpass filter to audio data.
        
        Args:
            audio_data: Input audio data
            source: Audio source
            
        Returns:
            Audio data with lowpass filter applied
        """
        try:
            cutoff = source.get_lowpass_cutoff()
            
            # Simple first-order lowpass filter
            # In a real audio engine, this would use proper filter design
            
            if cutoff >= 20000.0:
                return audio_data  # No filtering needed
            
            # Calculate filter coefficient
            dt = 1.0 / self.sample_rate
            rc = 1.0 / (2.0 * np.pi * cutoff)
            alpha = dt / (rc + dt)
            
            # Apply filter
            filtered_data = np.zeros_like(audio_data)
            if len(filtered_data) > 0:
                filtered_data[0] = audio_data[0]
                for i in range(1, len(filtered_data)):
                    filtered_data[i] = alpha * audio_data[i] + (1 - alpha) * filtered_data[i-1]
            
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Error applying lowpass filter: {e}")
            return audio_data
    
    def _apply_other_effects(self, audio_data: np.ndarray, source: AudioSource) -> np.ndarray:
        """Apply other audio effects.
        
        Args:
            audio_data: Input audio data
            source: Audio source
            
        Returns:
            Audio data with effects applied
        """
        try:
            processed_data = audio_data.copy()
            
            # Apply pitch shifting (simplified)
            if source.get_pitch() != 1.0:
                # This is a very simplified pitch implementation
                # In a real audio engine, this would use proper pitch shifting algorithms
                processed_data = processed_data * source.get_pitch()
            
            # Apply panning
            if source.get_pan() != 0.0:
                pan = source.get_pan()
                if len(processed_data.shape) > 1 and processed_data.shape[1] == 2:
                    # Stereo panning
                    left_gain = 1.0 - max(0, pan)
                    right_gain = 1.0 + min(0, pan)
                    processed_data[:, 0] *= left_gain
                    processed_data[:, 1] *= right_gain
            
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error applying other effects: {e}")
            return audio_data
    
    def add_effect(self, effect: AudioEffect) -> bool:
        """Add an audio effect.
        
        Args:
            effect: Audio effect to add
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            if effect not in self.active_effects:
                self.active_effects.append(effect)
                self.logger.debug(f"Added audio effect: {effect.name}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error adding audio effect: {e}")
            return False
    
    def remove_effect(self, effect_name: str) -> bool:
        """Remove an audio effect.
        
        Args:
            effect_name: Name of the effect to remove
            
        Returns:
            True if removed successfully, False otherwise
        """
        try:
            for i, effect in enumerate(self.active_effects):
                if effect.name == effect_name:
                    del self.active_effects[i]
                    self.logger.debug(f"Removed audio effect: {effect_name}")
                    return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error removing audio effect: {e}")
            return False
    
    def get_active_effects(self) -> List[AudioEffect]:
        """Get list of active effects.
        
        Returns:
            List of active effects
        """
        return self.active_effects.copy()
    
    def set_reverb_parameters(self, room_size: float = None, damping: float = None,
                            wet_mix: float = None, dry_mix: float = None):
        """Set reverb parameters.
        
        Args:
            room_size: Room size (0.0 to 1.0)
            damping: Damping (0.0 to 1.0)
            wet_mix: Wet mix level (0.0 to 1.0)
            dry_mix: Dry mix level (0.0 to 1.0)
        """
        if room_size is not None:
            self.reverb_room_size = max(0.0, min(1.0, room_size))
        if damping is not None:
            self.reverb_damping = max(0.0, min(1.0, damping))
        if wet_mix is not None:
            self.reverb_wet_mix = max(0.0, min(1.0, wet_mix))
        if dry_mix is not None:
            self.reverb_dry_mix = max(0.0, min(1.0, dry_mix))
        
        self.logger.debug(f"Set reverb parameters: room_size={self.reverb_room_size}, damping={self.reverb_damping}")
    
    def set_filter_parameters(self, lowpass_cutoff: float = None, highpass_cutoff: float = None,
                            bandpass_center: float = None, bandpass_bandwidth: float = None):
        """Set filter parameters.
        
        Args:
            lowpass_cutoff: Lowpass cutoff frequency
            highpass_cutoff: Highpass cutoff frequency
            bandpass_center: Bandpass center frequency
            bandpass_bandwidth: Bandpass bandwidth
        """
        if lowpass_cutoff is not None:
            self.lowpass_cutoff = max(20.0, min(20000.0, lowpass_cutoff))
        if highpass_cutoff is not None:
            self.highpass_cutoff = max(20.0, min(20000.0, highpass_cutoff))
        if bandpass_center is not None:
            self.bandpass_center = max(20.0, min(20000.0, bandpass_center))
        if bandpass_bandwidth is not None:
            self.bandpass_bandwidth = max(1.0, min(10000.0, bandpass_bandwidth))
        
        self.logger.debug(f"Set filter parameters: lowpass={self.lowpass_cutoff}, highpass={self.highpass_cutoff}")
    
    def set_distortion_parameters(self, gain: float = None, threshold: float = None):
        """Set distortion parameters.
        
        Args:
            gain: Distortion gain
            threshold: Distortion threshold
        """
        if gain is not None:
            self.distortion_gain = max(0.1, min(10.0, gain))
        if threshold is not None:
            self.distortion_threshold = max(0.0, min(1.0, threshold))
        
        self.logger.debug(f"Set distortion parameters: gain={self.distortion_gain}, threshold={self.distortion_threshold}")
    
    def set_echo_parameters(self, delay: float = None, decay: float = None, feedback: float = None):
        """Set echo parameters.
        
        Args:
            delay: Echo delay in seconds
            decay: Echo decay factor
            feedback: Echo feedback factor
        """
        if delay is not None:
            self.echo_delay = max(0.0, min(1.0, delay))
        if decay is not None:
            self.echo_decay = max(0.0, min(1.0, decay))
        if feedback is not None:
            self.echo_feedback = max(0.0, min(1.0, feedback))
        
        self.logger.debug(f"Set echo parameters: delay={self.echo_delay}, decay={self.echo_decay}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get audio effects statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "active_effects": len(self.active_effects),
            "effects_processed": self.effects_processed,
            "processing_time": self.processing_time,
            "reverb_room_size": self.reverb_room_size,
            "reverb_damping": self.reverb_damping,
            "lowpass_cutoff": self.lowpass_cutoff,
            "highpass_cutoff": self.highpass_cutoff
        }
    
    def shutdown(self):
        """Shutdown the audio effects system."""
        if self.is_initialized:
            self.logger.info("Shutting down audio effects...")
            
            # Clear active effects
            self.active_effects.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Audio effects shutdown complete")
