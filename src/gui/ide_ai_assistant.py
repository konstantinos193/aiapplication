#!/usr/bin/env python3
"""
IDE AI Assistant - AI Chat Component.

This replicates the React AI Assistant component exactly using QWebEngineView
for pixel-perfect reproduction, just like the header, left panel, and center panel.
"""

from typing import Optional, List, Dict, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QKeyEvent, QWheelEvent
from PyQt6.QtCore import QEvent


class IDEAIAssistant(QWidget):
    """
    AI Assistant - AI Chat Interface.
    
    Uses QWebEngineView to embed the React component directly,
    ensuring pixel-perfect reproduction.
    """
    
    # Signals
    message_sent = pyqtSignal(str)
    message_received = pyqtSignal(str)
    chat_cleared = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._messages: List[Dict[str, Any]] = [
            {
                "id": 1,
                "text": "Hello! I'm your AI assistant. I can help you with game development, scripting, design patterns, and optimization techniques.",
                "is_user": False,
                "timestamp": "2025-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "text": "How can I create a smooth player movement script with physics?",
                "is_user": True,
                "timestamp": "2025-01-01T00:01:00Z"
            },
            {
                "id": 3,
                "text": "I can help you create a physics-based movement script! Here's a comprehensive approach using Rigidbody components...",
                "is_user": False,
                "timestamp": "2025-01-01T00:02:00Z"
            }
        ]
        self._is_typing = False
        
        # Setup UI
        self._setup_ui()
        self._setup_zoom_prevention()
        self._setup_connections()
        
    def _setup_ui(self):
        """Setup the AI assistant web view interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Set size policy to expand vertically - make it expand as much as possible
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setObjectName("aiAssistantWebView")
        
        # Ensure web view expands to fill available space - make it expand maximally
        self.web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Set minimum height to ensure it takes up space
        self.setMinimumHeight(400)
        
        # Override size hint to make it expand more
        self.setSizeIncrement(1, 1)
        
        # Override size hint to make it expand more aggressively
        self.setMinimumHeight(600)  # Increase minimum height
        
        # Override size hint to make it expand more
        self.setSizeIncrement(1, 1)
        
        # Create custom web page
        self.web_page = self._create_custom_web_page()
        self.web_view.setPage(self.web_page)
        
        # Load the React component
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "assets")
        ai_assistant_path = os.path.join(assets_dir, "ai_assistant.html")
        print(f"DEBUG: Loading AI Assistant from: {ai_assistant_path}")
        print(f"DEBUG: File exists: {os.path.exists(ai_assistant_path)}")
        self.web_view.load(QUrl.fromLocalFile(ai_assistant_path))
        
        # Connect load finished signal
        self.web_view.loadFinished.connect(self._on_web_loaded)
        
        # Add to layout
        main_layout.addWidget(self.web_view)
        
        # Debug: Print size policies
        print(f"DEBUG: AI Assistant size policy: {self.sizePolicy().horizontalPolicy()}, {self.sizePolicy().verticalPolicy()}")
        print(f"DEBUG: Web view size policy: {self.web_view.sizePolicy().horizontalPolicy()}, {self.web_view.sizePolicy().verticalPolicy()}")
        
        # Force the widget to update its geometry
        self.updateGeometry()
        
    def resizeEvent(self, event):
        """Handle resize events to ensure proper sizing."""
        super().resizeEvent(event)
        print(f"DEBUG: AI Assistant resized to: {event.size().width()}x{event.size().height()}")
        if hasattr(self, 'web_view') and self.web_view:
            print(f"DEBUG: Web view size: {self.web_view.size().width()}x{self.web_view.size().height()}")
        
        # Force web view to resize
        if hasattr(self, 'web_view') and self.web_view:
            self.web_view.resize(event.size())
            self.web_view.updateGeometry()
    
    def sizeHint(self):
        """Override size hint to make the widget expand more."""
        hint = super().sizeHint()
        # Make it expand more aggressively
        hint.setHeight(max(hint.height(), 800))
        return hint
        
    def _create_custom_web_page(self) -> QWebEnginePage:
        """Create a custom web page with zoom prevention."""
        web_page = QWebEnginePage()
        
        # Get settings
        settings = web_page.settings()
        
        # DISABLE ZOOM FUNCTIONALITY
        try:
            if hasattr(QWebEngineSettings, 'ZoomTextOnly'):
                settings.setAttribute(QWebEngineSettings.ZoomTextOnly, False)
                print("DEBUG: Zoom text only disabled")
        except:
            pass

        try:
            zoom_attributes = [
                'ZoomTextOnly', 'ZoomFactor', 'ZoomLevel', 'DefaultZoomLevel',
                'MinimumZoomLevel', 'MaximumZoomLevel'
            ]
            for attr_name in zoom_attributes:
                if hasattr(QWebEngineSettings, attr_name):
                    try:
                        if attr_name in ['ZoomTextOnly']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), False)
                        elif attr_name in ['DefaultZoomLevel', 'ZoomLevel']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), 1.0)
                        print(f"DEBUG: {attr_name} setting configured")
                    except Exception as e:
                        print(f"DEBUG: Could not configure {attr_name}: {e}")
        except Exception as e:
            print(f"DEBUG: Error configuring zoom settings: {e}")
        
        return web_page
        
    def _setup_zoom_prevention(self):
        """Setup zoom prevention mechanisms."""
        # Install event filter
        self.installEventFilter(self)
        
        # Don't start timer immediately - wait for web view to load
        # self._setup_zoom_prevention_timer()
        
        # Set initial zoom factor
        if hasattr(self, 'web_view') and self.web_view:
            self.web_view.setZoomFactor(1.0)
        
        # Disable context menu
        if hasattr(self, 'web_view') and self.web_view:
            self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        
    def _setup_zoom_prevention_timer(self):
        """Setup timer to enforce zoom prevention."""
        self._zoom_prevention_timer = QTimer()
        self._zoom_prevention_timer.timeout.connect(self._enforce_zoom_prevention)
        self._zoom_prevention_timer.start(100)
        
    def _enforce_zoom_prevention(self):
        """Enforce zoom prevention by resetting zoom factor."""
        if hasattr(self, 'web_view') and self.web_view:
            current_zoom = self.web_view.zoomFactor()
            if current_zoom != 1.0:
                print(f"DEBUG: Zoom factor was {current_zoom}, resetting to 1.0")
                self.web_view.setZoomFactor(1.0)
                
    def _setup_connections(self):
        """Setup signal connections."""
        pass
        
    def _on_web_loaded(self):
        """Handle web page load completion."""
        print("DEBUG: AI Assistant web page loaded")
        self._inject_zoom_prevention_script()
        self._inject_python_bridge()
        self._load_messages()
        
        # Now that web view is loaded, setup zoom prevention timer
        self._setup_zoom_prevention_timer()
        
    def _inject_zoom_prevention_script(self):
        """Inject JavaScript to prevent zooming."""
        zoom_prevention_script = """
        // Disable zoom through JavaScript
        (function() {
            'use strict';
            
            // Prevent keyboard shortcuts
            document.addEventListener('keydown', function(e) {
                if ((e.ctrlKey || e.metaKey) && 
                    (e.key === '+' || e.key === '-' || e.key === '=' || e.key === '0')) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('DEBUG: Zoom shortcut prevented');
                    return false;
                }
            }, true);
            
            // Prevent wheel zoom
            document.addEventListener('wheel', function(e) {
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('DEBUG: Ctrl+wheel zoom prevented');
                    return false;
                }
            }, { passive: false });
            
            // Prevent touch zoom
            document.addEventListener('gesturestart', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('DEBUG: Touch zoom prevented');
                return false;
            }, { passive: false });
            
            // Prevent double-tap zoom
            document.addEventListener('touchend', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('DEBUG: Double-tap zoom prevented');
                return false;
            }, false);
            
            // Set viewport meta tag
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) {
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
            } else {
                const meta = document.createElement('meta');
                meta.name = 'viewport';
                meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                document.head.appendChild(meta);
            }
            
            console.log('DEBUG: Zoom prevention JavaScript injected successfully');
        })();
        """
        
        self.web_view.page().runJavaScript(zoom_prevention_script)
        
    def _inject_python_bridge(self):
        """Inject Python bridge for communication."""
        bridge_script = f"""
        // Python bridge for AI assistant
        window.pythonBridge = {{
            // Send message
            sendMessage: function(message) {{
                console.log('DEBUG: Sending message:', message);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'message_sent',
                    data: message
                }}));
            }},
            
            // Add message to chat
            addMessage: function(message, isUser) {{
                console.log('DEBUG: Adding message:', message, 'isUser:', isUser);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'message_added',
                    data: {{ message: message, isUser: isUser }}
                }}));
            }},
            
            // Clear chat
            clearChat: function() {{
                console.log('DEBUG: Clearing chat');
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'chat_cleared',
                    data: null
                }}));
            }},
            
            // Set typing indicator
            setTyping: function(isTyping) {{
                console.log('DEBUG: Setting typing indicator:', isTyping);
                // Emit signal to Python
                window.qt.webChannelTransport.send(JSON.stringify({{
                    type: 'typing_changed',
                    data: isTyping
                }}));
            }}
        }};
        
        console.log('DEBUG: Python bridge injected successfully');
        """
        
        self.web_view.page().runJavaScript(bridge_script)
        
    def _load_messages(self):
        """Load existing messages into the chat."""
        import json
        script = f"window.pythonBridge.loadMessages({json.dumps(self._messages)});"
        self.web_view.page().runJavaScript(script)
        
    def eventFilter(self, obj, event):
        """Event filter to prevent zoom events."""
        if event.type() == QEvent.Type.Wheel:
            wheel_event = QWheelEvent(event)
            if wheel_event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                print("DEBUG: Ctrl+wheel zoom prevented")
                return True
        elif event.type() == QEvent.Type.KeyPress:
            if hasattr(event, 'key') and hasattr(event, 'modifiers'):
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal, Qt.Key.Key_0]:
                        print("DEBUG: Ctrl+Plus/Minus/0 zoom prevented")
                        return True
        return super().eventFilter(obj, event)
        
    def wheelEvent(self, event):
        """Handle wheel events to prevent zoom."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            print("DEBUG: Ctrl+wheel zoom prevented in wheelEvent")
            event.accept()
            return
        super().wheelEvent(event)
        
    def keyPressEvent(self, event):
        """Handle key press events to prevent zoom."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal, Qt.Key.Key_0]:
                print("DEBUG: Ctrl+Plus/Minus/0 zoom prevented in keyPressEvent")
                event.accept()
                return
        super().keyPressEvent(event)
        
    # Public API methods
    def sendMessage(self, message: str):
        """Send a message to the AI assistant."""
        if not message.strip():
            return
            
        # Add user message
        user_message = {
            "id": len(self._messages) + 1,
            "text": message,
            "is_user": True,
            "timestamp": "2025-01-01T00:00:00Z"  # TODO: Use real timestamp
        }
        self._messages.append(user_message)
        
        # Emit signal
        self.message_sent.emit(message)
        
        # Update via JavaScript
        script = f"window.pythonBridge.addMessage('{message}', true);"
        self.web_view.page().runJavaScript(script)
        
        # Simulate AI response (in real app, this would call AI service)
        self._simulate_ai_response(message)
        
    def _simulate_ai_response(self, user_message: str):
        """Simulate AI response (placeholder for real AI integration)."""
        # TODO: Replace with actual AI service call
        ai_response = f"I received your message: '{user_message}'. This is a placeholder response. In the real application, this would be generated by an AI service."
        
        # Add AI message
        ai_message = {
            "id": len(self._messages) + 1,
            "text": ai_response,
            "is_user": False,
            "timestamp": "2025-01-01T00:00:00Z"  # TODO: Use real timestamp
        }
        self._messages.append(ai_message)
        
        # Emit signal
        self.message_received.emit(ai_response)
        
        # Update via JavaScript
        script = f"window.pythonBridge.addMessage('{ai_response}', false);"
        self.web_view.page().runJavaScript(script)
        
    def addMessage(self, message: str, is_user: bool = False):
        """Add a message to the chat."""
        new_message = {
            "id": len(self._messages) + 1,
            "text": message,
            "is_user": is_user,
            "timestamp": "2025-01-01T00:00:00Z"  # TODO: Use real timestamp
        }
        self._messages.append(new_message)
        
        # Update via JavaScript
        script = f"window.pythonBridge.addMessage('{message}', {str(is_user).lower()});"
        self.web_view.page().runJavaScript(script)
        
    def clearChat(self):
        """Clear all messages from the chat."""
        self._messages.clear()
        
        # Emit signal
        self.chat_cleared.emit()
        
        # Update via JavaScript
        script = "window.pythonBridge.clearChat();"
        self.web_view.page().runJavaScript(script)
        
    def setTyping(self, is_typing: bool):
        """Set the typing indicator."""
        self._is_typing = is_typing
        
        # Update via JavaScript
        script = f"window.pythonBridge.setTyping({str(is_typing).lower()});"
        self.web_view.page().runJavaScript(script)
        
    def getMessages(self) -> List[Dict[str, Any]]:
        """Get all messages in the chat."""
        return self._messages.copy()
        
    def getMessageCount(self) -> int:
        """Get the total number of messages."""
        return len(self._messages)
