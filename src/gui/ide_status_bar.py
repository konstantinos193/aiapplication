#!/usr/bin/env python3
"""
IDE Status Bar - Shows system information and console toggle.

This replicates the React status bar exactly with:
- Ready status
- Object count, triangles, draw calls
- Console toggle
- Time and disk space
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame,
    QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from .design_system.react_theme_system import react_theme


class IDEStatusBar(QWidget):
    """
    IDE Status bar with system information and controls.
    
    Features:
    - Ready status and object counts
    - Console toggle
    - Time and disk space display
    - Professional styling
    """
    
    # Signals
    console_toggled = pyqtSignal(bool)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._show_console = True
        self._object_count = 127
        self._triangle_count = 45200
        self._draw_calls = 23
        self._disk_free = "2.1GB"
        
        # Setup UI
        self._setup_ui()
        self._setup_connections()
        self._setup_theme()
        self._setup_timer()
        
        # Set fixed height
        self.setFixedHeight(32)  # h-8 = 32px
        
    def _setup_ui(self):
        """Setup the status bar user interface."""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 0, 16, 0)  # px-4 = 16px
        main_layout.setSpacing(16)  # gap-4 = 16px
        
        # Left section: Status and counts
        left_section = self._create_left_section()
        main_layout.addWidget(left_section)
        
        # Right section: Console and system info
        right_section = self._create_right_section()
        main_layout.addWidget(right_section)
        
        # Apply glass effect styling
        self._apply_glass_effect()
        
    def _create_left_section(self) -> QWidget:
        """Create the left section with status and counts."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)  # gap-4 = 16px
        
        # Ready status
        ready_label = QLabel("Ready")
        ready_label.setObjectName("readyStatus")
        ready_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 12px;")
        layout.addWidget(ready_label)
        
        # Separator
        separator1 = self._create_separator()
        layout.addWidget(separator1)
        
        # Object count
        objects_label = QLabel(f"Objects: {self._object_count}")
        objects_label.setObjectName("objectsCount")
        objects_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
        layout.addWidget(objects_label)
        
        # Triangle count
        triangles_label = QLabel(f"Triangles: {self._format_number(self._triangle_count)}")
        triangles_label.setObjectName("trianglesCount")
        triangles_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
        layout.addWidget(triangles_label)
        
        # Draw calls
        draw_calls_label = QLabel(f"Draw calls: {self._draw_calls}")
        draw_calls_label.setObjectName("drawCallsCount")
        draw_calls_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
        layout.addWidget(draw_calls_label)
        
        return container
        
    def _create_right_section(self) -> QWidget:
        """Create the right section with console and system info."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)  # gap-4 = 16px
        
        # Console toggle
        console_button = self._create_console_button()
        layout.addWidget(console_button)
        
        # Time display
        time_container = self._create_time_display()
        layout.addWidget(time_container)
        
        # Disk space
        disk_container = self._create_disk_display()
        layout.addWidget(disk_container)
        
        return container
        
    def _create_separator(self) -> QWidget:
        """Create a vertical separator."""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setObjectName("separator")
        separator.setFixedHeight(16)  # h-4 = 16px
        
        # Apply styling
        separator.setStyleSheet("""
            QFrame#separator {
                background: rgba(255, 255, 255, 0.2);
                max-width: 1px;
            }
        """)
        
        return separator
        
    def _create_console_button(self) -> QPushButton:
        """Create the console toggle button."""
        button = QPushButton()
        button.setObjectName("consoleButton")
        button.setFixedHeight(24)  # h-6 = 24px
        
        # Create button content
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(8, 4, 8, 4)  # px-2 py-1 = 8px 4px
        content_layout.setSpacing(4)  # gap-1 = 4px
        
        # Terminal icon
        icon_label = QLabel("💻")
        icon_label.setObjectName("consoleIcon")
        icon_label.setStyleSheet("font-size: 12px;")  # h-3 w-3 = 12px
        content_layout.addWidget(icon_label)
        
        # Text
        text_label = QLabel("Console")
        text_label.setObjectName("consoleText")
        text_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.6);")
        content_layout.addWidget(text_label)
        
        button.setLayout(content_layout)
        
        # Apply styling
        button.setStyleSheet("""
            QPushButton#consoleButton {
                background: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton#consoleButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Connect click event
        button.clicked.connect(self._on_console_clicked)
        
        return button
        
    def _create_time_display(self) -> QWidget:
        """Create the time display."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)  # gap-1 = 4px
        
        # Clock icon
        icon_label = QLabel("🕐")
        icon_label.setObjectName("timeIcon")
        icon_label.setStyleSheet("font-size: 12px;")  # h-3 w-3 = 12px
        layout.addWidget(icon_label)
        
        # Time label
        self.time_label = QLabel("14:32:45")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.6);")
        layout.addWidget(self.time_label)
        
        return container
        
    def _create_disk_display(self) -> QWidget:
        """Create the disk space display."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)  # gap-1 = 4px
        
        # Disk icon
        icon_label = QLabel("💾")
        icon_label.setObjectName("diskIcon")
        icon_label.setStyleSheet("font-size: 12px;")  # h-3 w-3 = 12px
        layout.addWidget(icon_label)
        
        # Disk space label
        disk_label = QLabel(f"{self._disk_free} free")
        disk_label.setObjectName("diskLabel")
        disk_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.6);")
        layout.addWidget(disk_label)
        
        return container
        
    def _apply_glass_effect(self):
        """Apply glass effect styling."""
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            }
        """)
        
    def _setup_connections(self):
        """Setup signal connections."""
        # No specific connections needed for status bar
        
    def _setup_theme(self):
        """Setup enhanced theme with sophisticated styling."""
        # Apply sophisticated status bar styling
        self.setStyleSheet(f"""
            QWidget {{
                background: {react_theme.get_color("card")};
                color: {react_theme.get_color("foreground")};
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                border-top: 1px solid {react_theme.get_color("border")};
            }}
            
            QLabel {{
                color: {react_theme.get_color("foreground")};
                font-size: 12px;
                font-weight: 500;
            }}
            
            QPushButton {{
                background: {react_theme.get_color("secondary")};
                border: 1px solid {react_theme.get_color("border")};
                border-radius: 6px;
                padding: 4px 8px;
                color: {react_theme.get_color("foreground")};
                font-size: 11px;
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background: {react_theme.get_color("muted")};
                border-color: {react_theme.get_color("accent")};
            }}
            
            QPushButton:pressed {{
                background: {react_theme.get_color("primary")};
                color: {react_theme.get_color("primary_foreground")};
            }}
            
            QProgressBar {{
                border: 1px solid {react_theme.get_color("border")};
                border-radius: 4px;
                background: {react_theme.get_color("muted")};
                text-align: center;
                font-size: 10px;
                font-weight: 500;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 {react_theme.get_color("primary")},
                                          stop:1 {react_theme.get_color("accent")});
                border-radius: 3px;
            }}
        """)
        
    def _setup_timer(self):
        """Setup timer for time updates."""
        self._time_timer = QTimer()
        self._time_timer.timeout.connect(self._update_time)
        self._time_timer.start(1000)  # Update every second
        
        # Initialize time
        self._update_time()
        
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
        
    def _on_console_clicked(self):
        """Handle console button click."""
        self._show_console = not self._show_console
        self.console_toggled.emit(self._show_console)
        
        # Update button styling
        self._update_console_button()
        
    def _update_console_button(self):
        """Update console button styling based on state."""
        console_button = self.findChild(QPushButton, "consoleButton")
        if console_button:
            if self._show_console:
                # Console is visible
                console_button.setStyleSheet("""
                    QPushButton#consoleButton {
                        background: rgba(255, 107, 53, 0.2);
                        border: 1px solid rgba(255, 107, 53, 0.3);
                        border-radius: 4px;
                    }
                    QPushButton#consoleButton:hover {
                        background: rgba(255, 107, 53, 0.3);
                    }
                """)
            else:
                # Console is hidden
                console_button.setStyleSheet("""
                    QPushButton#consoleButton {
                        background: transparent;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton#consoleButton:hover {
                        background: rgba(255, 255, 255, 0.1);
                    }
                """)
                
    def _update_time(self):
        """Update the time display."""
        import datetime
        
        current_time = datetime.datetime.now()
        time_string = current_time.strftime("%H:%M:%S")
        
        if hasattr(self, 'time_label'):
            self.time_label.setText(time_string)
            
    def _format_number(self, number: int) -> str:
        """Format large numbers with K, M, B suffixes."""
        if number >= 1000000000:
            return f"{number / 1000000000:.1f}B"
        elif number >= 1000000:
            return f"{number / 1000000:.1f}M"
        elif number >= 1000:
            return f"{number / 1000:.1f}K"
        else:
            return str(number)
            
    # Public API methods
    def setObjectCount(self, count: int):
        """Set the object count."""
        self._object_count = count
        self._update_object_count()
        
    def getObjectCount(self) -> int:
        """Get the current object count."""
        return self._object_count
        
    def setTriangleCount(self, count: int):
        """Set the triangle count."""
        self._triangle_count = count
        self._update_triangle_count()
        
    def getTriangleCount(self) -> int:
        """Get the current triangle count."""
        return self._triangle_count
        
    def setDrawCalls(self, count: int):
        """Set the draw calls count."""
        self._draw_calls = count
        self._update_draw_calls()
        
    def getDrawCalls(self) -> int:
        """Get the current draw calls count."""
        return self._draw_calls
        
    def setDiskFree(self, free_space: str):
        """Set the disk free space."""
        self._disk_free = free_space
        self._update_disk_space()
        
    def getDiskFree(self) -> str:
        """Get the current disk free space."""
        return self._disk_free
        
    def setConsoleVisible(self, visible: bool):
        """Set the console visibility."""
        self._show_console = visible
        self._update_console_button()
        
    def isConsoleVisible(self) -> bool:
        """Get the console visibility state."""
        return self._show_console
        
    def _update_object_count(self):
        """Update the object count display."""
        objects_label = self.findChild(QLabel, "objectsCount")
        if objects_label:
            objects_label.setText(f"Objects: {self._object_count}")
            
    def _update_triangle_count(self):
        """Update the triangle count display."""
        triangles_label = self.findChild(QLabel, "trianglesCount")
        if triangles_label:
            triangles_label.setText(f"Triangles: {self._format_number(self._triangle_count)}")
            
    def _update_draw_calls(self):
        """Update the draw calls display."""
        draw_calls_label = self.findChild(QLabel, "drawCallsCount")
        if draw_calls_label:
            draw_calls_label.setText(f"Draw calls: {self._draw_calls}")
            
    def _update_disk_space(self):
        """Update the disk space display."""
        disk_label = self.findChild(QLabel, "diskLabel")
        if disk_label:
            disk_label.setText(f"{self._disk_free} free")
