"""
Audio Listener for Nexlify Engine.

This module provides audio listener functionality for
3D spatial audio including position, orientation, and velocity.
"""

import logging
import math
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from ..utils.logger import get_logger


@dataclass
class AudioListener:
    """Audio listener for 3D spatial audio."""
    
    def __init__(self, listener_id: int, position: List[float] = None, 
                 orientation: List[float] = None):
        self.listener_id = listener_id
        self.logger = get_logger(__name__)
        
        # Position and orientation
        self.position: List[float] = position or [0.0, 0.0, 0.0]
        self.velocity: List[float] = [0.0, 0.0, 0.0]
        self.orientation: List[float] = orientation or [0.0, 0.0, -1.0]  # Forward direction
        self.up_vector: List[float] = [0.0, 1.0, 0.0]  # Up direction
        
        # Audio properties
        self.volume: float = 1.0
        self.mute: bool = False
        
        # 3D audio properties
        self.doppler_factor: float = 1.0
        self.speed_of_sound: float = 343.0  # m/s
        
        # Audio effects
        self.reverb_enabled: bool = False
        self.reverb_room: float = 0.0
        self.reverb_room_hf: float = 0.0
        self.reverb_decay_time: float = 0.0
        self.reverb_decay_hf_ratio: float = 0.0
        self.reverb_reflections: float = 0.0
        self.reverb_reflections_delay: float = 0.0
        self.reverb_reverb: float = 0.0
        self.reverb_reverb_delay: float = 0.0
        self.reverb_hf_reference: float = 5000.0
        self.reverb_lf_reference: float = 250.0
        self.reverb_room_rolloff_factor: float = 0.0
        self.reverb_air_absorption_hf_gain: float = 0.0
        self.reverb_flags: int = 0
    
    def set_position(self, position: List[float]):
        """Set the position of the audio listener.
        
        Args:
            position: 3D position [x, y, z]
        """
        self.position = position.copy()
        self.logger.debug(f"Set listener position: {position}")
    
    def get_position(self) -> List[float]:
        """Get the position of the audio listener.
        
        Returns:
            3D position [x, y, z]
        """
        return self.position.copy()
    
    def set_velocity(self, velocity: List[float]):
        """Set the velocity of the audio listener.
        
        Args:
            velocity: Velocity vector [x, y, z]
        """
        self.velocity = velocity.copy()
        self.logger.debug(f"Set listener velocity: {velocity}")
    
    def get_velocity(self) -> List[float]:
        """Get the velocity of the audio listener.
        
        Returns:
            Velocity vector [x, y, z]
        """
        return self.velocity.copy()
    
    def set_orientation(self, forward: List[float], up: List[float] = None):
        """Set the orientation of the audio listener.
        
        Args:
            forward: Forward direction vector [x, y, z]
            up: Up direction vector [x, y, z] (optional)
        """
        self.orientation = forward.copy()
        if up is not None:
            self.up_vector = up.copy()
        
        self.logger.debug(f"Set listener orientation: forward={forward}, up={self.up_vector}")
    
    def get_orientation(self) -> Tuple[List[float], List[float]]:
        """Get the orientation of the audio listener.
        
        Returns:
            Tuple of (forward_direction, up_direction)
        """
        return (self.orientation.copy(), self.up_vector.copy())
    
    def set_volume(self, volume: float):
        """Set the volume of the audio listener.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        self.logger.debug(f"Set listener volume: {self.volume}")
    
    def get_volume(self) -> float:
        """Get the volume of the audio listener.
        
        Returns:
            Volume level
        """
        return self.volume
    
    def set_mute(self, mute: bool):
        """Set whether the audio listener is muted.
        
        Args:
            mute: Whether to mute the listener
        """
        self.mute = mute
        self.logger.debug(f"Set listener mute: {mute}")
    
    def is_muted(self) -> bool:
        """Check if the audio listener is muted.
        
        Returns:
            True if muted, False otherwise
        """
        return self.mute
    
    def set_doppler_factor(self, factor: float):
        """Set the Doppler effect factor.
        
        Args:
            factor: Doppler factor
        """
        self.doppler_factor = max(0.0, factor)
        self.logger.debug(f"Set Doppler factor: {self.doppler_factor}")
    
    def get_doppler_factor(self) -> float:
        """Get the Doppler effect factor.
        
        Returns:
            Doppler factor
        """
        return self.doppler_factor
    
    def set_speed_of_sound(self, speed: float):
        """Set the speed of sound.
        
        Args:
            speed: Speed of sound in m/s
        """
        self.speed_of_sound = max(1.0, speed)
        self.logger.debug(f"Set speed of sound: {self.speed_of_sound}")
    
    def get_speed_of_sound(self) -> float:
        """Get the speed of sound.
        
        Returns:
            Speed of sound in m/s
        """
        return self.speed_of_sound
    
    def set_reverb_properties(self, room: float = 0.0, room_hf: float = 0.0,
                            decay_time: float = 0.0, decay_hf_ratio: float = 0.0,
                            reflections: float = 0.0, reflections_delay: float = 0.0,
                            reverb: float = 0.0, reverb_delay: float = 0.0,
                            hf_reference: float = 5000.0, lf_reference: float = 250.0,
                            room_rolloff_factor: float = 0.0, air_absorption_hf_gain: float = 0.0,
                            flags: int = 0):
        """Set reverb properties.
        
        Args:
            room: Room effect level
            room_hf: Room high-frequency effect level
            decay_time: Reverb decay time
            decay_hf_ratio: High-frequency decay ratio
            reflections: Early reflections level
            reflections_delay: Early reflections delay
            reverb: Late reverb level
            reverb_delay: Late reverb delay
            hf_reference: High-frequency reference
            lf_reference: Low-frequency reference
            room_rolloff_factor: Room rolloff factor
            air_absorption_hf_gain: Air absorption high-frequency gain
            flags: Reverb flags
        """
        self.reverb_room = room
        self.reverb_room_hf = room_hf
        self.reverb_decay_time = decay_time
        self.reverb_decay_hf_ratio = decay_hf_ratio
        self.reverb_reflections = reflections
        self.reverb_reflections_delay = reflections_delay
        self.reverb_reverb = reverb
        self.reverb_reverb_delay = reverb_delay
        self.reverb_hf_reference = hf_reference
        self.reverb_lf_reference = lf_reference
        self.reverb_room_rolloff_factor = room_rolloff_factor
        self.reverb_air_absorption_hf_gain = air_absorption_hf_gain
        self.reverb_flags = flags
        
        self.logger.debug(f"Set reverb properties: room={room}, decay_time={decay_time}")
    
    def get_reverb_properties(self) -> Dict[str, float]:
        """Get reverb properties.
        
        Returns:
            Dictionary of reverb properties
        """
        return {
            "room": self.reverb_room,
            "room_hf": self.reverb_room_hf,
            "decay_time": self.reverb_decay_time,
            "decay_hf_ratio": self.reverb_decay_hf_ratio,
            "reflections": self.reverb_reflections,
            "reflections_delay": self.reverb_reflections_delay,
            "reverb": self.reverb_reverb,
            "reverb_delay": self.reverb_reverb_delay,
            "hf_reference": self.reverb_hf_reference,
            "lf_reference": self.reverb_lf_reference,
            "room_rolloff_factor": self.reverb_room_rolloff_factor,
            "air_absorption_hf_gain": self.reverb_air_absorption_hf_gain,
            "flags": self.reverb_flags
        }
    
    def set_reverb_enabled(self, enabled: bool):
        """Enable or disable reverb.
        
        Args:
            enabled: Whether reverb is enabled
        """
        self.reverb_enabled = enabled
        self.logger.debug(f"Set reverb enabled: {enabled}")
    
    def is_reverb_enabled(self) -> bool:
        """Check if reverb is enabled.
        
        Returns:
            True if reverb enabled, False otherwise
        """
        return self.reverb_enabled
    
    def get_distance_to_source(self, source_position: List[float]) -> float:
        """Get the distance to an audio source.
        
        Args:
            source_position: Audio source position
            
        Returns:
            Distance to source
        """
        distance = 0.0
        for i in range(3):
            diff = self.position[i] - source_position[i]
            distance += diff * diff
        
        return math.sqrt(distance)
    
    def get_relative_velocity(self, source_velocity: List[float]) -> float:
        """Get the relative velocity between listener and source.
        
        Args:
            source_velocity: Audio source velocity
            
        Returns:
            Relative velocity magnitude
        """
        relative_velocity = 0.0
        for i in range(3):
            diff = self.velocity[i] - source_velocity[i]
            relative_velocity += diff * diff
        
        return math.sqrt(relative_velocity)
    
    def get_doppler_shift(self, source_position: List[float], source_velocity: List[float]) -> float:
        """Calculate Doppler shift for an audio source.
        
        Args:
            source_position: Audio source position
            source_velocity: Audio source velocity
            
        Returns:
            Doppler shift factor
        """
        try:
            # Calculate distance vector
            distance_vector = [source_position[i] - self.position[i] for i in range(3)]
            distance = math.sqrt(sum(d * d for d in distance_vector))
            
            if distance < 1e-6:
                return 1.0
            
            # Normalize distance vector
            distance_vector = [d / distance for d in distance_vector]
            
            # Calculate relative velocity along the line of sight
            relative_velocity = 0.0
            for i in range(3):
                relative_velocity += (source_velocity[i] - self.velocity[i]) * distance_vector[i]
            
            # Calculate Doppler shift
            doppler_shift = 1.0 + (relative_velocity * self.doppler_factor) / self.speed_of_sound
            
            # Clamp to reasonable range
            return max(0.1, min(10.0, doppler_shift))
            
        except Exception as e:
            self.logger.error(f"Error calculating Doppler shift: {e}")
            return 1.0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get audio listener statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "listener_id": self.listener_id,
            "position": self.position,
            "velocity": self.velocity,
            "orientation": self.orientation,
            "up_vector": self.up_vector,
            "volume": self.volume,
            "mute": self.mute,
            "doppler_factor": self.doppler_factor,
            "speed_of_sound": self.speed_of_sound,
            "reverb_enabled": self.reverb_enabled
        }
