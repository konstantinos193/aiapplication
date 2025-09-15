"""
Event System for Nexlify Engine.

This module provides a decoupled event system for communication
between different engine systems and game objects.
"""

import logging
from typing import Dict, Any, List, Callable, Set
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import get_logger


class EventPriority(Enum):
    """Event priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Event:
    """Event data structure."""
    name: str
    data: Dict[str, Any]
    timestamp: float
    source: str = ""
    priority: EventPriority = EventPriority.NORMAL


class EventSystem:
    """Event system for decoupled communication."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.is_initialized = False
        
        # Event listeners
        self.listeners: Dict[str, List[Callable]] = {}
        self.priority_listeners: Dict[str, Dict[EventPriority, List[Callable]]] = {}
        
        # Event queue
        self.event_queue: List[Event] = []
        self.max_queue_size = 1000
        
        # Statistics
        self.events_processed = 0
        self.events_dropped = 0
        
    def initialize(self) -> bool:
        """Initialize the event system.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self.logger.info("Initializing event system...")
            
            # Clear any existing data
            self.listeners.clear()
            self.priority_listeners.clear()
            self.event_queue.clear()
            
            self.is_initialized = True
            self.logger.info("✅ Event system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize event system: {e}")
            return False
    
    def subscribe(self, event_name: str, callback: Callable, priority: EventPriority = EventPriority.NORMAL):
        """Subscribe to an event.
        
        Args:
            event_name: Name of the event to subscribe to
            callback: Function to call when event is fired
            priority: Priority level for the callback
        """
        if not self.is_initialized:
            self.logger.error("Event system not initialized")
            return
        
        try:
            # Add to priority listeners
            if event_name not in self.priority_listeners:
                self.priority_listeners[event_name] = {}
            
            if priority not in self.priority_listeners[event_name]:
                self.priority_listeners[event_name][priority] = []
            
            if callback not in self.priority_listeners[event_name][priority]:
                self.priority_listeners[event_name][priority].append(callback)
            
            # Also add to regular listeners for backward compatibility
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            
            if callback not in self.listeners[event_name]:
                self.listeners[event_name].append(callback)
            
            self.logger.debug(f"Subscribed to event: {event_name}")
            
        except Exception as e:
            self.logger.error(f"Error subscribing to event {event_name}: {e}")
    
    def unsubscribe(self, event_name: str, callback: Callable):
        """Unsubscribe from an event.
        
        Args:
            event_name: Name of the event to unsubscribe from
            callback: Function to remove
        """
        if not self.is_initialized:
            return
        
        try:
            # Remove from priority listeners
            if event_name in self.priority_listeners:
                for priority_list in self.priority_listeners[event_name].values():
                    if callback in priority_list:
                        priority_list.remove(callback)
            
            # Remove from regular listeners
            if event_name in self.listeners:
                if callback in self.listeners[event_name]:
                    self.listeners[event_name].remove(callback)
            
            self.logger.debug(f"Unsubscribed from event: {event_name}")
            
        except Exception as e:
            self.logger.error(f"Error unsubscribing from event {event_name}: {e}")
    
    def fire_event(self, event_name: str, data: Dict[str, Any] = None, 
                   source: str = "", priority: EventPriority = EventPriority.NORMAL):
        """Fire an event immediately.
        
        Args:
            event_name: Name of the event to fire
            data: Event data
            source: Source of the event
            priority: Event priority
        """
        if not self.is_initialized:
            return
        
        try:
            import time
            event = Event(
                name=event_name,
                data=data or {},
                timestamp=time.time(),
                source=source,
                priority=priority
            )
            
            self._process_event(event)
            
        except Exception as e:
            self.logger.error(f"Error firing event {event_name}: {e}")
    
    def queue_event(self, event_name: str, data: Dict[str, Any] = None,
                    source: str = "", priority: EventPriority = EventPriority.NORMAL):
        """Queue an event for later processing.
        
        Args:
            event_name: Name of the event to queue
            data: Event data
            source: Source of the event
            priority: Event priority
        """
        if not self.is_initialized:
            return
        
        try:
            import time
            event = Event(
                name=event_name,
                data=data or {},
                timestamp=time.time(),
                source=source,
                priority=priority
            )
            
            # Check queue size
            if len(self.event_queue) >= self.max_queue_size:
                self.events_dropped += 1
                self.logger.warning(f"Event queue full, dropping event: {event_name}")
                return
            
            self.event_queue.append(event)
            
        except Exception as e:
            self.logger.error(f"Error queuing event {event_name}: {e}")
    
    def update(self, delta_time: float):
        """Update the event system and process queued events.
        
        Args:
            delta_time: Time since last update
        """
        if not self.is_initialized:
            return
        
        try:
            # Process all queued events
            while self.event_queue:
                event = self.event_queue.pop(0)
                self._process_event(event)
            
        except Exception as e:
            self.logger.error(f"Error updating event system: {e}")
    
    def _process_event(self, event: Event):
        """Process a single event.
        
        Args:
            event: Event to process
        """
        try:
            # Process priority listeners first
            if event.name in self.priority_listeners:
                for priority in [EventPriority.CRITICAL, EventPriority.HIGH, 
                               EventPriority.NORMAL, EventPriority.LOW]:
                    if priority in self.priority_listeners[event.name]:
                        for callback in self.priority_listeners[event.name][priority]:
                            try:
                                callback(event)
                            except Exception as e:
                                self.logger.error(f"Error in event callback for {event.name}: {e}")
            
            # Process regular listeners
            if event.name in self.listeners:
                for callback in self.listeners[event.name]:
                    try:
                        callback(event)
                    except Exception as e:
                        self.logger.error(f"Error in event callback for {event.name}: {e}")
            
            self.events_processed += 1
            
        except Exception as e:
            self.logger.error(f"Error processing event {event.name}: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get event system statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "events_processed": self.events_processed,
            "events_dropped": self.events_dropped,
            "queued_events": len(self.event_queue),
            "total_listeners": sum(len(listeners) for listeners in self.listeners.values()),
            "event_types": len(self.listeners)
        }
    
    def clear_queue(self):
        """Clear all queued events."""
        self.event_queue.clear()
        self.logger.info("Event queue cleared")
    
    def shutdown(self):
        """Shutdown the event system."""
        if self.is_initialized:
            self.logger.info("Shutting down event system...")
            
            # Clear all data
            self.listeners.clear()
            self.priority_listeners.clear()
            self.event_queue.clear()
            
            self.is_initialized = False
            self.logger.info("✅ Event system shutdown complete")
