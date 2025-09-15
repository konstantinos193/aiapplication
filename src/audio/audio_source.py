"""
Audio Source for Nexlify Engine.

This module provides audio source functionality including
3D spatial audio, volume control, and audio effects.
"""

import logging
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from ..utils.logger import get_logger


@dataclass
class AudioClip:
    """Audio clip data."""
    data: np.ndarray
    sample_rate: int
    channels: int
    duration: float
    name: str


class AudioSource:
    """Audio source for 3D spatial audio."""
    
    def __init__(self, source_id: int, audio_data: np.ndarray = None, 
                 position: List[float] = None, is_3d: bool = True):
        self.source_id = source_id
        self.logger = get_logger(__name__)
        
        # Audio data
        self.audio_clip: Optional[AudioClip] = None
        if audio_data is not None:
            self.audio_clip = AudioClip(
                data=audio_data,
                sample_rate=44100,  # Default sample rate
                channels=1 if len(audio_data.shape) == 1 else audio_data.shape[1],
                duration=len(audio_data) / 44100.0,
                name=f"source_{source_id}"
            )
        
        # 3D positioning
        self.position: List[float] = position or [0.0, 0.0, 0.0]
        self.velocity: List[float] = [0.0, 0.0, 0.0]
        self.is_3d: bool = is_3d
        
        # Audio properties
        self.volume: float = 1.0
        self.pitch: float = 1.0
        self.pan: float = 0.0  # -1.0 to 1.0
        self.loop: bool = False
        
        # Playback state
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.play_position: float = 0.0  # Current playback position in seconds
        
        # 3D audio properties
        self.min_distance: float = 1.0
        self.max_distance: float = 500.0
        self.rolloff_factor: float = 1.0
        self.cone_inner_angle: float = 360.0
        self.cone_outer_angle: float = 360.0
        self.cone_outer_gain: float = 0.0
        
        # Audio effects
        self.reverb_enabled: bool = False
        self.reverb_mix: float = 0.0
        self.lowpass_enabled: bool = False
        self.lowpass_cutoff: float = 20000.0
        
    def set_audio_clip(self, audio_clip: AudioClip):
        """Set the audio clip for this source.
        
        Args:
            audio_clip: Audio clip to set
        """
        self.audio_clip = audio_clip
        self.play_position = 0.0
        self.logger.debug(f"Set audio clip: {audio_clip.name}")
    
    def get_audio_clip(self) -> Optional[AudioClip]:
        """Get the current audio clip.
        
        Returns:
            Audio clip or None if not set
        """
        return self.audio_clip
    
    def set_position(self, position: List[float]):
        """Set the 3D position of the audio source.
        
        Args:
            position: 3D position [x, y, z]
        """
        self.position = position.copy()
        self.logger.debug(f"Set position: {position}")
    
    def get_position(self) -> List[float]:
        """Get the 3D position of the audio source.
        
        Returns:
            3D position [x, y, z]
        """
        return self.position.copy()
    
    def set_velocity(self, velocity: List[float]):
        """Set the velocity of the audio source.
        
        Args:
            velocity: Velocity vector [x, y, z]
        """
        self.velocity = velocity.copy()
        self.logger.debug(f"Set velocity: {velocity}")
    
    def get_velocity(self) -> List[float]:
        """Get the velocity of the audio source.
        
        Returns:
            Velocity vector [x, y, z]
        """
        return self.velocity.copy()
    
    def set_volume(self, volume: float):
        """Set the volume of the audio source.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        self.logger.debug(f"Set volume: {self.volume}")
    
    def get_volume(self) -> float:
        """Get the volume of the audio source.
        
        Returns:
            Volume level
        """
        return self.volume
    
    def set_pitch(self, pitch: float):
        """Set the pitch of the audio source.
        
        Args:
            pitch: Pitch multiplier (0.5 to 2.0)
        """
        self.pitch = max(0.5, min(2.0, pitch))
        self.logger.debug(f"Set pitch: {self.pitch}")
    
    def get_pitch(self) -> float:
        """Get the pitch of the audio source.
        
        Returns:
            Pitch multiplier
        """
        return self.pitch
    
    def set_pan(self, pan: float):
        """Set the pan of the audio source.
        
        Args:
            pan: Pan value (-1.0 to 1.0, -1.0 = left, 1.0 = right)
        """
        self.pan = max(-1.0, min(1.0, pan))
        self.logger.debug(f"Set pan: {self.pan}")
    
    def get_pan(self) -> float:
        """Get the pan of the audio source.
        
        Returns:
            Pan value
        """
        return self.pan
    
    def set_loop(self, loop: bool):
        """Set whether the audio should loop.
        
        Args:
            loop: Whether to loop the audio
        """
        self.loop = loop
        self.logger.debug(f"Set loop: {loop}")
    
    def is_looping(self) -> bool:
        """Check if the audio is set to loop.
        
        Returns:
            True if looping, False otherwise
        """
        return self.loop
    
    def play(self):
        """Start playing the audio source."""
        if self.audio_clip is None:
            self.logger.warning("No audio clip set")
            return
        
        self.is_playing = True
        self.is_paused = False
        self.play_position = 0.0
        self.logger.debug("Started playing audio source")
    
    def pause(self):
        """Pause the audio source."""
        if self.is_playing:
            self.is_paused = True
            self.logger.debug("Paused audio source")
    
    def resume(self):
        """Resume the audio source."""
        if self.is_paused:
            self.is_paused = False
            self.logger.debug("Resumed audio source")
    
    def stop(self):
        """Stop the audio source."""
        self.is_playing = False
        self.is_paused = False
        self.play_position = 0.0
        self.logger.debug("Stopped audio source")
    
    def is_playing(self) -> bool:
        """Check if the audio source is playing.
        
        Returns:
            True if playing, False otherwise
        """
        return self.is_playing and not self.is_paused
    
    def is_paused(self) -> bool:
        """Check if the audio source is paused.
        
        Returns:
            True if paused, False otherwise
        """
        return self.is_paused
    
    def set_3d(self, is_3d: bool):
        """Set whether this is a 3D audio source.
        
        Args:
            is_3d: Whether this is a 3D audio source
        """
        self.is_3d = is_3d
        self.logger.debug(f"Set 3D: {is_3d}")
    
    def is_3d(self) -> bool:
        """Check if this is a 3D audio source.
        
        Returns:
            True if 3D, False otherwise
        """
        return self.is_3d
    
    def set_min_distance(self, distance: float):
        """Set the minimum distance for 3D audio.
        
        Args:
            distance: Minimum distance
        """
        self.min_distance = max(0.0, distance)
        self.logger.debug(f"Set min distance: {self.min_distance}")
    
    def get_min_distance(self) -> float:
        """Get the minimum distance for 3D audio.
        
        Returns:
            Minimum distance
        """
        return self.min_distance
    
    def set_max_distance(self, distance: float):
        """Set the maximum distance for 3D audio.
        
        Args:
            distance: Maximum distance
        """
        self.max_distance = max(0.0, distance)
        self.logger.debug(f"Set max distance: {self.max_distance}")
    
    def get_max_distance(self) -> float:
        """Get the maximum distance for 3D audio.
        
        Returns:
            Maximum distance
        """
        return self.max_distance
    
    def set_rolloff_factor(self, factor: float):
        """Set the rolloff factor for 3D audio.
        
        Args:
            factor: Rolloff factor
        """
        self.rolloff_factor = max(0.0, factor)
        self.logger.debug(f"Set rolloff factor: {self.rolloff_factor}")
    
    def get_rolloff_factor(self) -> float:
        """Get the rolloff factor for 3D audio.
        
        Returns:
            Rolloff factor
        """
        return self.rolloff_factor
    
    def set_cone_angles(self, inner_angle: float, outer_angle: float):
        """Set the cone angles for directional audio.
        
        Args:
            inner_angle: Inner cone angle in degrees
            outer_angle: Outer cone angle in degrees
        """
        self.cone_inner_angle = max(0.0, min(360.0, inner_angle))
        self.cone_outer_angle = max(self.cone_inner_angle, min(360.0, outer_angle))
        self.logger.debug(f"Set cone angles: {self.cone_inner_angle}, {self.cone_outer_angle}")
    
    def get_cone_angles(self) -> Tuple[float, float]:
        """Get the cone angles for directional audio.
        
        Returns:
            Tuple of (inner_angle, outer_angle)
        """
        return (self.cone_inner_angle, self.cone_outer_angle)
    
    def set_cone_outer_gain(self, gain: float):
        """Set the outer cone gain.
        
        Args:
            gain: Outer cone gain (0.0 to 1.0)
        """
        self.cone_outer_gain = max(0.0, min(1.0, gain))
        self.logger.debug(f"Set cone outer gain: {self.cone_outer_gain}")
    
    def get_cone_outer_gain(self) -> float:
        """Get the outer cone gain.
        
        Returns:
            Outer cone gain
        """
        return self.cone_outer_gain
    
    def set_reverb(self, enabled: bool, mix: float = 0.0):
        """Set reverb effect.
        
        Args:
            enabled: Whether reverb is enabled
            mix: Reverb mix level (0.0 to 1.0)
        """
        self.reverb_enabled = enabled
        self.reverb_mix = max(0.0, min(1.0, mix))
        self.logger.debug(f"Set reverb: {enabled}, mix: {self.reverb_mix}")
    
    def is_reverb_enabled(self) -> bool:
        """Check if reverb is enabled.
        
        Returns:
            True if reverb enabled, False otherwise
        """
        return self.reverb_enabled
    
    def get_reverb_mix(self) -> float:
        """Get the reverb mix level.
        
        Returns:
            Reverb mix level
        """
        return self.reverb_mix
    
    def set_lowpass(self, enabled: bool, cutoff: float = 20000.0):
        """Set lowpass filter.
        
        Args:
            enabled: Whether lowpass is enabled
            cutoff: Cutoff frequency in Hz
        """
        self.lowpass_enabled = enabled
        self.lowpass_cutoff = max(20.0, min(20000.0, cutoff))
        self.logger.debug(f"Set lowpass: {enabled}, cutoff: {self.lowpass_cutoff}")
    
    def is_lowpass_enabled(self) -> bool:
        """Check if lowpass filter is enabled.
        
        Returns:
            True if lowpass enabled, False otherwise
        """
        return self.lowpass_enabled
    
    def get_lowpass_cutoff(self) -> float:
        """Get the lowpass cutoff frequency.
        
        Returns:
            Cutoff frequency in Hz
        """
        return self.lowpass_cutoff
    
    def get_audio_data(self, buffer_size: int) -> Optional[np.ndarray]:
        """Get audio data for the specified buffer size.
        
        Args:
            buffer_size: Number of samples to get
            
        Returns:
            Audio data or None if not playing
        """
        if not self.is_playing() or self.audio_clip is None:
            return None
        
        try:
            # Calculate start and end positions
            start_sample = int(self.play_position * self.audio_clip.sample_rate)
            end_sample = start_sample + buffer_size
            
            # Get audio data
            if end_sample <= len(self.audio_clip.data):
                audio_data = self.audio_clip.data[start_sample:end_sample]
            else:
                # Handle end of clip
                if self.loop:
                    # Loop the audio
                    remaining_samples = len(self.audio_clip.data) - start_sample
                    audio_data = np.concatenate([
                        self.audio_clip.data[start_sample:],
                        self.audio_clip.data[:buffer_size - remaining_samples]
                    ])
                    self.play_position = (buffer_size - remaining_samples) / self.audio_clip.sample_rate
                else:
                    # End of clip
                    audio_data = self.audio_clip.data[start_sample:]
                    self.stop()
                    return None
            
            # Update play position
            self.play_position += buffer_size / self.audio_clip.sample_rate
            
            # Apply volume
            audio_data = audio_data * self.volume
            
            # Apply pitch (simple time stretching)
            if self.pitch != 1.0:
                # This is a simplified pitch implementation
                # In a real audio engine, this would use proper pitch shifting
                audio_data = audio_data * self.pitch
            
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Error getting audio data: {e}")
            return None
    
    def get_distance_to_listener(self, listener_position: List[float] = None) -> float:
        """Get the distance to the listener.
        
        Args:
            listener_position: Listener position (optional, defaults to origin)
            
        Returns:
            Distance to listener
        """
        if listener_position is None:
            listener_position = [0.0, 0.0, 0.0]
        
        distance = 0.0
        for i in range(3):
            diff = self.position[i] - listener_position[i]
            distance += diff * diff
        
        return np.sqrt(distance)
    
    def get_3d_volume(self, listener_position: List[float] = None) -> float:
        """Get the 3D volume based on distance.
        
        Args:
            listener_position: Listener position (optional, defaults to origin)
            
        Returns:
            3D volume multiplier
        """
        if not self.is_3d or listener_position is None:
            return 1.0
        
        distance = self.get_distance_to_listener(listener_position)
        
        if distance <= self.min_distance:
            return 1.0
        
        if distance >= self.max_distance:
            return 0.0
        
        # Inverse square law with rolloff factor
        volume = self.min_distance / (self.min_distance + self.rolloff_factor * (distance - self.min_distance))
        return max(0.0, min(1.0, volume))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get audio source statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "source_id": self.source_id,
            "is_playing": self.is_playing(),
            "is_paused": self.is_paused(),
            "play_position": self.play_position,
            "volume": self.volume,
            "pitch": self.pitch,
            "pan": self.pan,
            "is_3d": self.is_3d,
            "position": self.position,
            "has_audio_clip": self.audio_clip is not None
        }
