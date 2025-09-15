#!/usr/bin/env python3
"""
IDE Right Panel - Contains AI Chat Assistant.

This replicates the React right panel exactly with:
- AI chat interface
- Message history
- Input field with send button
"""

from typing import Optional, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from .components.react_style_panel import ReactStylePanel
from .components.react_style_input import ReactStyleInput
from .components.react_style_button import ReactStyleButton
from .design_system.react_theme_system import react_theme


class IDERightPanel(QWidget):
    """
    Right panel containing AI chat assistant.
    
    Features:
    - AI chat interface with message history
    - Input field with send button
    - Professional styling and gradients
    """
    
    # Signals
    message_sent = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._chat_message = ""
        self._messages = [
            {
                "type": "ai",
                "content": "Hello! I'm your AI assistant. I can help you with game development, scripting, design patterns, and optimization techniques."
            },
            {
                "type": "user",
                "content": "How can I create a smooth player movement script with physics?"
            },
            {
                "type": "ai",
                "content": "I can help you create a physics-based movement script! Here's a comprehensive approach using Rigidbody components..."
            }
        ]
        
        # Setup UI
        self._setup_ui()
        self._setup_connections()
        self._setup_theme()
        
    def _setup_ui(self):
        """Setup the right panel user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # AI Chat panel
        self.chat_panel = self._create_chat_panel()
        main_layout.addWidget(self.chat_panel)
        
    def _create_chat_panel(self) -> ReactStylePanel:
        """Create the AI chat panel."""
        panel = ReactStylePanel(
            title="AI Assistant",
            icon="💬",  # Placeholder icon
            gradient=True
        )
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)  # p-4 = 16px
        content_layout.setSpacing(16)  # mb-4 = 16px
        
        # Chat messages area
        messages_container = self._create_messages_container()
        content_layout.addWidget(messages_container)
        
        # Input area
        input_container = self._create_input_container()
        content_layout.addWidget(input_container)
        
        # Set the content
        panel.setContent(content_widget)
        
        return panel
        
    def _create_messages_container(self) -> QWidget:
        """Create the chat messages container."""
        container = QFrame()
        container.setObjectName("messagesContainer")
        container.setMinimumHeight(300)
        
        # Apply gradient background
        container.setStyleSheet("""
            QFrame#messagesContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 0, 0, 0.8),
                    stop:0.5 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.5));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)  # p-4 = 16px
        layout.setSpacing(16)  # space-y-4 = 16px
        
        # Create messages
        for i, message in enumerate(self._messages):
            message_widget = self._create_message_widget(message, i)
            layout.addWidget(message_widget)
            
        layout.addStretch()
        
        return container
        
    def _create_message_widget(self, message: dict, index: int) -> QWidget:
        """Create a message widget."""
        container = QFrame()
        container.setObjectName("messageWidget")
        
        # Apply styling based on message type
        if message["type"] == "ai":
            container.setStyleSheet("""
                QFrame#messageWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(255, 107, 53, 0.15),
                        stop:0.5 rgba(255, 107, 53, 0.1),
                        stop:1 rgba(255, 107, 53, 0.05));
                    border: 1px solid rgba(255, 107, 53, 0.2);
                    border-radius: 12px;
                }
            """)
        else:
            container.setStyleSheet("""
                QFrame#messageWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(255, 255, 255, 0.1),
                        stop:0.5 rgba(255, 255, 255, 0.09),
                        stop:1 rgba(255, 255, 255, 0.08));
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    margin-left: 32px;
                }
            """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)  # p-4 = 16px
        layout.setSpacing(0)
        
        # Message content
        content_label = QLabel(message["content"])
        content_label.setObjectName("messageContent")
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            font-size: 14px;
            line-height: 1.5;
            color: rgba(255, 255, 255, 0.9);
        """)
        layout.addWidget(content_label)
        
        return container
        
    def _create_input_container(self) -> QWidget:
        """Create the input container."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)  # gap-3 = 12px
        
        # Chat input
        self.chat_input = ReactStyleInput(
            placeholder="Ask me anything about game development...",
            text=self._chat_message
        )
        self.chat_input.text_changed.connect(self._on_chat_input_changed)
        layout.addWidget(self.chat_input)
        
        # Send button
        send_button = ReactStyleButton(
            text="",
            size="sm"
        )
        send_button.setIcon("📤")
        send_button.clicked.connect(self._on_send_clicked)
        layout.addWidget(send_button)
        
        return container
        
    def _setup_connections(self):
        """Setup signal connections."""
        # Chat input
        if hasattr(self, 'chat_input'):
            self.chat_input.text_changed.connect(self._on_chat_input_changed)
            
    def _setup_theme(self):
        """Setup enhanced theme with sophisticated styling."""
        # Apply sophisticated right panel styling
        self.setStyleSheet(f"""
            QWidget {{
                background: {react_theme.get_color("sidebar")};
                color: {react_theme.get_color("sidebar_foreground")};
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            
            QLabel {{
                color: {react_theme.get_color("sidebar_foreground")};
            }}
            
            QPushButton {{
                background: {react_theme.get_sidebar_secondary_color().name()};
                border: 1px solid {react_theme.get_color("sidebar_border")};
                border-radius: 8px;
                padding: 8px 16px;
                color: {react_theme.get_color("sidebar_foreground")};
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background: {react_theme.get_color("sidebar_accent")};
                color: {react_theme.get_color("sidebar_accent_foreground")};
                border-color: {react_theme.get_color("sidebar_ring")};
            }}
            
            QPushButton:pressed {{
                background: {react_theme.get_color("sidebar_primary")};
            }}
            
            QTextEdit {{
                background: {react_theme.get_color("sidebar")};
                border: 1px solid {react_theme.get_color("sidebar_border")};
                border-radius: 8px;
                color: {react_theme.get_color("sidebar_foreground")};
                font-size: 13px;
                padding: 8px;
            }}
            
            QTextEdit:focus {{
                border-color: {react_theme.get_color("sidebar_ring")};
                outline: none;
            }}
            
            QScrollBar:vertical {{
                background: {react_theme.get_sidebar_muted_color().name()};
                width: 8px;
                border-radius: 4px;
            }}
            
            QScrollBar::handle:vertical {{
                background: {react_theme.get_color("sidebar_border")};
                border-radius: 4px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: {react_theme.get_color("sidebar_accent")};
            }}
        """)
        
    def _apply_theme(self):
        """Apply current theme."""
        colors = react_theme.get_current_colors()
        
        # Update styling based on theme
        if react_theme.get_current_mode() == "dark":
            self._apply_dark_theme()
        else:
            self._apply_light_theme()
            
    def _apply_dark_theme(self):
        """Apply dark theme styling."""
        # Dark theme is already applied by default
        pass
        
    def _apply_light_theme(self):
        """Apply light theme styling."""
        # Light theme adjustments
        pass
        
    def _on_theme_changed(self):
        """Handle theme changes."""
        self._apply_theme()
        
    def _on_chat_input_changed(self, text: str):
        """Handle chat input changes."""
        self._chat_message = text
        
    def _on_send_clicked(self):
        """Handle send button click."""
        if self._chat_message.strip():
            # Add user message
            self._add_message("user", self._chat_message)
            
            # Emit signal
            self.message_sent.emit(self._chat_message)
            
            # Clear input
            self._chat_input.setText("")
            self._chat_message = ""
            
            # Simulate AI response (you can replace with real AI)
            self._simulate_ai_response()
            
    def _add_message(self, message_type: str, content: str):
        """Add a new message to the chat."""
        message = {
            "type": message_type,
            "content": content
        }
        self._messages.append(message)
        
        # Create and add message widget
        message_widget = self._create_message_widget(message, len(self._messages) - 1)
        
        # Find the messages container and add the new message
        messages_container = self.chat_panel.findChild(QFrame, "messagesContainer")
        if messages_container:
            # Remove the stretch item
            layout = messages_container.layout()
            if layout.count() > 0:
                stretch_item = layout.takeAt(layout.count() - 1)
                if stretch_item:
                    stretch_item.widget().deleteLater()
            
            # Add the new message
            layout.addWidget(message_widget)
            
            # Add stretch back
            layout.addStretch()
            
    def _simulate_ai_response(self):
        """Simulate an AI response."""
        # Simulate typing delay
        import time
        time.sleep(0.5)
        
        # Add AI response
        response = "I understand your question! Let me help you with that. This is a simulated response - in the real implementation, this would come from your AI service."
        self._add_message("ai", response)
        
    # Public API methods
    def addMessage(self, message_type: str, content: str):
        """Add a message programmatically."""
        self._add_message(message_type, content)
        
    def getMessages(self) -> List[dict]:
        """Get all chat messages."""
        return self._messages.copy()
        
    def clearMessages(self):
        """Clear all chat messages."""
        self._messages.clear()
        
        # Clear the messages container
        messages_container = self.chat_panel.findChild(QFrame, "messagesContainer")
        if messages_container:
            layout = messages_container.layout()
            while layout.count() > 1:  # Keep the stretch item
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                    
        # Add initial messages back
        self._setup_ui()
