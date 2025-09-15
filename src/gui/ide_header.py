#!/usr/bin/env python3
"""
IDE Header Panel - Contains play controls, transform tools, and main title.

This replicates the React header exactly with:
- Play/Pause/Stop/Reset controls
- Transform tools (Move, Rotate, Scale)
- Main title with logo
- Performance metrics
- Theme toggle
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame,
    QPushButton, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap

from .components.react_style_button import ReactStyleButton
from .components.react_style_toolbar_button import ReactStyleToolbarButton
from .components.react_style_panel import ReactStylePanel
from .design_system.react_theme_system import react_theme
from .utils.svg_loader import load_svg_icon


class IDEHeader(QWidget):
    """
    IDE Header with play controls, transform tools, and main title.
    
    Features:
    - Play controls with active state
    - Transform tools (Move, Rotate, Scale)
    - Main title with logo and version
    - Performance metrics (FPS, Memory, Online status)
    - Theme toggle and settings
    """
    
    # Signals
    play_state_changed = pyqtSignal(bool)
    transform_tool_changed = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._is_playing = False
        self._active_transform_tool = "move"
        self._fps = 60
        self._memory_usage = 245
        
        # Setup UI
        self._setup_ui()
        self._setup_connections()
        self._setup_theme()
        self._setup_timer()
        
        # Set fixed height
        self.setFixedHeight(64)  # h-16 = 64px
        
    def _setup_ui(self):
        """Setup the header user interface."""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 0, 24, 0)  # px-6 = 24px
        main_layout.setSpacing(24)  # gap-6 = 24px
        
        # Left section: Play controls and tools
        left_section = self._create_left_section()
        main_layout.addWidget(left_section)
        
        # Center section: Main title and breadcrumb
        center_section = self._create_center_section()
        main_layout.addWidget(center_section)
        
        # Right section: Performance and settings
        right_section = self._create_right_section()
        main_layout.addWidget(right_section)
        
        # Apply glass effect styling
        self._apply_glass_effect()
        
    def _create_left_section(self) -> QWidget:
        """Create the left section with play controls and transform tools."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)  # gap-6 = 24px
        
        # Play controls group
        play_controls = self._create_play_controls()
        layout.addWidget(play_controls)
        
        # Transform tools group
        transform_tools = self._create_transform_tools()
        layout.addWidget(transform_tools)
        
        # Separator
        separator = self._create_separator()
        layout.addWidget(separator)
        
        # Project breadcrumb
        breadcrumb = self._create_breadcrumb()
        layout.addWidget(breadcrumb)
        
        layout.addStretch()
        
        return container
        
    def _create_play_controls(self) -> QWidget:
        """Create play controls group - EXACTLY matching React."""
        container = QFrame()
        container.setObjectName("playControls")
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)  # p-1 = 4px
        layout.setSpacing(4)  # gap-1 = 4px
        
        # Play/Pause button with proper icons - EXACTLY matching React
        self.play_button = ReactStyleToolbarButton(
            text="▶",  # Will be replaced with proper icon
            active=self._is_playing,
            tooltip="Play" if not self._is_playing else "Pause"
        )
        self.play_button.setToggleable(True)
        self.play_button.active_changed.connect(self._on_play_state_changed)
        self.play_button.setObjectName("playButton")  # For animate-glow styling
        layout.addWidget(self.play_button)
        
        # Stop button - EXACTLY matching React (h-3 w-3 = 12x12px)
        self.stop_button = ReactStyleToolbarButton(
            text="■",  # Will be replaced with proper icon
            tooltip="Stop"
        )
        self.stop_button.setObjectName("stopButton")  # For smaller icon styling
        layout.addWidget(self.stop_button)
        
        # Reset button - EXACTLY matching React (h-4 w-4 = 16x16px)
        self.reset_button = ReactStyleToolbarButton(
            text="↻",  # Will be replaced with proper icon
            tooltip="Reset"
        )
        layout.addWidget(self.reset_button)
        
        # Initialize play button icon
        self._update_play_button_icon()
        
        # Apply professional gradient styling
        self._apply_professional_gradient(container)
        
        # Setup glow animation for play button (EXACTLY matching React animate-glow)
        # Only animate when playing (matching React className="animate-glow" behavior)
        self._setup_glow_animation()
        
        return container
        
        
    def _create_transform_tools(self) -> QWidget:
        """Create transform tools group - EXACTLY matching React."""
        container = QFrame()
        container.setObjectName("transformTools")
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)  # p-1 = 4px
        layout.setSpacing(4)  # gap-1 = 4px
        
        # Move tool
        self.move_tool = ReactStyleToolbarButton(
            text="↔",  # Will be replaced with proper icon
            tooltip="Move Tool",
            active=True
        )
        self.move_tool.setToggleable(True)
        self.move_tool.active_changed.connect(lambda active: self._on_transform_tool_changed("move"))
        layout.addWidget(self.move_tool)
        
        # Rotate tool
        self.rotate_tool = ReactStyleToolbarButton(
            text="⟲",  # Will be replaced with proper icon
            tooltip="Rotate Tool"
        )
        self.rotate_tool.setToggleable(True)
        self.rotate_tool.active_changed.connect(lambda active: self._on_transform_tool_changed("rotate"))
        layout.addWidget(self.rotate_tool)
        
        # Scale tool
        self.scale_tool = ReactStyleToolbarButton(
            text="⤧",  # Will be replaced with proper icon
            tooltip="Scale Tool"
        )
        self.scale_tool.setToggleable(True)
        self.scale_tool.active_changed.connect(lambda active: self._on_transform_tool_changed("scale"))
        layout.addWidget(self.scale_tool)
        
        # Apply professional gradient styling
        self._apply_professional_gradient(container)
        
        return container
        
    def _create_separator(self) -> QWidget:
        """Create vertical separator."""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setObjectName("separator")
        
        # Apply gradient styling
        separator.setStyleSheet("""
            QFrame#separator {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 transparent,
                    stop:0.5 rgba(255, 255, 255, 0.1),
                    stop:1 transparent);
                max-width: 1px;
            }
        """)
        
        return separator
        
    def _create_breadcrumb(self) -> QWidget:
        """Create project breadcrumb navigation - EXACTLY matching React."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)  # gap-2 = 8px
        
        # Project label
        project_label = QLabel("Project")
        project_label.setObjectName("breadcrumbLabel")
        layout.addWidget(project_label)
        
        # Chevron
        chevron1 = QLabel(">")
        chevron1.setObjectName("breadcrumbChevron")
        layout.addWidget(chevron1)
        
        # Scenes label
        scenes_label = QLabel("Scenes")
        scenes_label.setObjectName("breadcrumbLabel")
        layout.addWidget(scenes_label)
        
        # Chevron
        chevron2 = QLabel(">")
        chevron2.setObjectName("breadcrumbChevron")
        layout.addWidget(chevron2)
        
        # Active tab
        self.active_tab_label = QLabel("MainScene")
        self.active_tab_label.setObjectName("activeTabLabel")
        layout.addWidget(self.active_tab_label)
        
        return container
        
    def _create_center_section(self) -> QWidget:
        """Create the center section with main title and logo."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)  # gap-4 = 16px
        
        # Logo container
        logo_container = self._create_logo_container()
        layout.addWidget(logo_container)
        
        # Title and version
        title_container = self._create_title_container()
        layout.addWidget(title_container)
        
        layout.addStretch()
        
        return container
        
    def _create_logo_container(self) -> QWidget:
        """Create the logo container - EXACTLY matching React."""
        container = QFrame()
        container.setObjectName("logoContainer")
        container.setFixedSize(40, 40)  # w-10 h-10 = 40x40px
        
        # Apply gradient background with shimmer effect
        container.setStyleSheet("""
            QFrame#logoContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff6b35,
                    stop:1 #ff8c42);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                position: relative;
            }
        """)
        
        # Logo icon (LayersIcon equivalent)
        logo_label = QLabel("📚", container)  # Layers icon equivalent
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 20px; color: white;")
        
        return container
        
    def _create_title_container(self) -> QWidget:
        """Create the title and version container - EXACTLY matching React."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)  # gap-1 = 4px
        
        # Main title with gradient text
        title_label = QLabel("Game Design IDE")
        title_label.setObjectName("mainTitle")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Version info
        version_container = QWidget()
        version_layout = QHBoxLayout(version_container)
        version_layout.setContentsMargins(0, 0, 0, 0)
        version_layout.setSpacing(8)  # gap-2 = 8px
        
        # Pro badge with gradient border
        pro_badge = QLabel("Pro")
        pro_badge.setObjectName("proBadge")
        pro_badge.setFixedSize(32, 20)  # w-8 h-5
        pro_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_layout.addWidget(pro_badge)
        
        # Version number
        version_label = QLabel("v2.1.0")
        version_label.setObjectName("versionLabel")
        version_layout.addWidget(version_label)
        
        layout.addWidget(version_container)
        
        return container
        
    def _create_right_section(self) -> QWidget:
        """Create the right section with performance metrics and settings."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)  # gap-3 = 12px
        
        # Performance metrics
        performance_container = self._create_performance_container()
        layout.addWidget(performance_container)
        
        # Theme toggle (placeholder)
        self.theme_toggle = QPushButton("🌙")
        self.theme_toggle.setObjectName("themeToggle")
        self.theme_toggle.setFixedSize(32, 32)
        self.theme_toggle.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_toggle)
        
        # Settings button
        settings_button = ReactStyleButton(
            text="Settings",
            variant="outline",
            size="sm"
        )
        layout.addWidget(settings_button)
        
        return container
        
    def _create_performance_container(self) -> QWidget:
        """Create performance metrics container - EXACTLY matching React."""
        container = QFrame()
        container.setObjectName("performanceContainer")
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 4, 12, 4)  # px-3 py-1
        layout.setSpacing(16)  # gap-4 = 16px
        
        # FPS with ActivityIcon
        fps_container = QWidget()
        fps_layout = QHBoxLayout(fps_container)
        fps_layout.setContentsMargins(0, 0, 0, 0)
        fps_layout.setSpacing(4)  # gap-1 = 4px
        
        fps_icon = QLabel("⚡")  # ActivityIcon equivalent
        fps_icon.setObjectName("fpsIcon")
        fps_layout.addWidget(fps_icon)
        
        self.fps_label = QLabel(f"{self._fps} FPS")
        self.fps_label.setObjectName("fpsLabel")
        fps_layout.addWidget(self.fps_label)
        
        layout.addWidget(fps_container)
        
        # Memory with MemoryStickIcon
        memory_container = QWidget()
        memory_layout = QHBoxLayout(memory_container)
        memory_layout.setContentsMargins(0, 0, 0, 0)
        memory_layout.setSpacing(4)  # gap-1 = 4px
        
        memory_icon = QLabel("💾")  # MemoryStickIcon equivalent
        memory_icon.setObjectName("memoryIcon")
        memory_layout.addWidget(memory_icon)
        
        self.memory_label = QLabel(f"{self._memory_usage}MB")
        self.memory_label.setObjectName("memoryLabel")
        memory_layout.addWidget(self.memory_label)
        
        layout.addWidget(memory_container)
        
        # Online status with WifiIcon
        online_container = QWidget()
        online_layout = QHBoxLayout(online_container)
        online_layout.setContentsMargins(0, 0, 0, 0)
        online_layout.setSpacing(4)  # gap-1 = 4px
        
        online_icon = QLabel("📶")  # WifiIcon equivalent
        online_icon.setObjectName("onlineIcon")
        online_layout.addWidget(online_icon)
        
        online_label = QLabel("Online")
        online_label.setObjectName("onlineLabel")
        online_layout.addWidget(online_label)
        
        layout.addWidget(online_container)
        
        # Apply glass effect styling
        self._apply_glass_effect(container)
        
        return container
        
    def _apply_professional_gradient(self, container: QWidget):
        """Apply professional gradient styling - EXACTLY matching React."""
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.1);  /* border-border/50 */
                border-radius: 8px;  /* rounded-lg */
            }
        """)
        
    def _apply_glass_effect(self, container: Optional[QWidget] = None):
        """Apply glass effect styling - EXACTLY matching React."""
        target = container or self
        
        target.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);  /* glass-effect */
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QLabel#breadcrumbLabel, QLabel#breadcrumbChevron {
                color: rgba(255, 255, 255, 0.6);  /* text-muted-foreground */
                font-size: 12px;  /* text-sm */
            }
            
            QLabel#activeTabLabel {
                color: white;  /* text-foreground */
                font-weight: bold;  /* font-medium */
                font-size: 12px;  /* text-sm */
            }
            
            QLabel#mainTitle {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff6b35,
                    stop:1 #ff8c42);
                color: #ff6b35;  /* text-gradient */
                font-size: 18px;  /* text-lg */
                font-weight: bold;  /* font-bold */
            }
            
            QLabel#proBadge {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff6b35,
                    stop:1 #ff8c42);
                color: white;
                border-radius: 10px;  /* rounded-full */
                font-size: 10px;  /* text-xs */
                font-weight: bold;  /* font-medium */
                padding: 2px 8px;  /* px-2 py-0.5 */
            }
            
            QLabel#versionLabel {
                color: rgba(255, 255, 255, 0.6);  /* text-muted-foreground */
                font-size: 10px;  /* text-xs */
            }
            
            QLabel#fpsIcon, QLabel#memoryIcon, QLabel#onlineIcon {
                font-size: 12px;  /* h-3 w-3 */
            }
            
            QLabel#fpsLabel, QLabel#memoryLabel, QLabel#onlineLabel {
                color: rgba(255, 255, 255, 0.8);  /* text-muted-foreground */
                font-size: 10px;  /* text-xs */
                font-family: monospace;  /* font-mono */
            }
            
            QPushButton#themeToggle {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: white;
                font-size: 16px;
            }
            
            QPushButton#themeToggle:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            /* EXACTLY matching React - smaller icon for stop button (h-3 w-3) */
            QPushButton#stopButton {
                font-size: 10px;  /* Smaller text for h-3 w-3 equivalent */
            }
        """)
        
    def _setup_connections(self):
        """Setup signal connections."""
        # Play button connections
        self.play_button.clicked.connect(self._on_play_clicked)
        
        # Transform tool connections
        self.move_tool.clicked.connect(lambda: self._on_transform_tool_changed("move"))
        self.rotate_tool.clicked.connect(lambda: self._on_transform_tool_changed("rotate"))
        self.scale_tool.clicked.connect(lambda: self._on_transform_tool_changed("scale"))
        
    def _setup_theme(self):
        """Setup theme - EXACTLY matching React."""
        # Apply header styling to match React exactly
        self.setStyleSheet(f"""
            QWidget {{
                background: rgba(255, 255, 255, 0.05);  /* glass-effect */
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);  /* border-border/50 */
                color: {react_theme.get_color("foreground")};
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            
            QLabel {{
                color: {react_theme.get_color("foreground")};
                font-weight: 500;
            }}
            
            QPushButton {{
                background: {react_theme.get_color("secondary")};
                border: 1px solid {react_theme.get_color("border")};
                border-radius: 8px;
                padding: 8px 16px;
                color: {react_theme.get_color("foreground")};
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
        """)
        
    def _setup_timer(self):
        """Setup timer for performance updates."""
        self._performance_timer = QTimer()
        self._performance_timer.timeout.connect(self._update_performance)
        self._performance_timer.start(1000)  # Update every second
        
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
        
    def _on_play_clicked(self):
        """Handle play button click - EXACTLY matching React onClick behavior."""
        self._is_playing = not self._is_playing
        self.play_button.setActive(self._is_playing)
        
        # Update icon based on state
        self._update_play_button_icon()
        
        # Update tooltip
        tooltip = "Pause" if self._is_playing else "Play"
        self.play_button.setTooltip(tooltip)
        
        # EXACTLY matching React className="animate-glow" behavior
        if self._is_playing:
            # Start glow animation when playing
            self._glow_animation.start()
        else:
            # Stop glow animation when paused
            self._glow_animation.stop()
            # Reset glow intensity to 0
            self.play_button.setProperty("glow_intensity", 0.0)
            self.play_button.update()
        
        # Emit signal
        self.play_state_changed.emit(self._is_playing)
        
    def _on_play_state_changed(self, is_playing: bool):
        """Handle play state changes from button."""
        self._is_playing = is_playing
        
    def _update_play_button_icon(self):
        """Update the play button icon based on current state."""
        if self._is_playing:
            self.play_button.setText("⏸")  # Pause symbol
        else:
            self.play_button.setText("▶")  # Play symbol
        
    def _on_transform_tool_changed(self, tool: str):
        """Handle transform tool changes."""
        self._active_transform_tool = tool
        
        # Update active states
        self.move_tool.setActive(tool == "move")
        self.rotate_tool.setActive(tool == "rotate")
        self.scale_tool.setActive(tool == "scale")
        
        # Emit signal
        self.transform_tool_changed.emit(tool)
        
    def _update_performance(self):
        """Update performance metrics."""
        # Simulate performance updates
        import random
        self._fps = random.randint(55, 65)
        self._memory_usage = random.randint(240, 250)
        
        # Update labels
        self.fps_label.setText(f"{self._fps} FPS")
        self.memory_label.setText(f"{self._memory_usage}MB")
        
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        # Toggle theme
        react_theme.toggle_theme()
        
        # Update button icon
        if react_theme.get_current_mode() == react_theme.ThemeMode.DARK:
            self.theme_toggle.setText("🌙")
            self.theme_toggle.setToolTip("Switch to Light theme")
        else:
            self.theme_toggle.setText("☀️")
            self.theme_toggle.setToolTip("Switch to Dark theme")
            
        # Update all panel themes
        self._update_panel_themes()
        
    def _update_panel_themes(self):
        """Update themes for all panels."""
        # Find the main IDE window and update all panels
        main_window = self.window()
        if hasattr(main_window, 'left_panel'):
            main_window.left_panel._setup_theme()
        if hasattr(main_window, 'center_panel'):
            main_window.center_panel._setup_theme()
        if hasattr(main_window, 'right_panel'):
            main_window.right_panel._setup_theme()
        if hasattr(main_window, 'status_bar'):
            main_window.status_bar._setup_theme()
        # Don't call main window theme setup to avoid recursion
        # main_window._setup_theme()
        
    def _setup_glow_animation(self):
        """Setup glow animation for play button - EXACTLY matching React animate-glow."""
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        
        # Create glow animation - EXACTLY matching React className="animate-glow"
        self._glow_animation = QPropertyAnimation(self.play_button, b"glow_intensity")
        self._glow_animation.setDuration(2000)  # 2 seconds
        self._glow_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._glow_animation.setLoopCount(-1)  # Infinite loop
        self._glow_animation.setStartValue(0.0)
        self._glow_animation.setEndValue(1.0)
        
        # Don't start animation yet - only when playing (matching React behavior)
        # self._glow_animation.start()
        
    # Public API methods
    def setPlayState(self, is_playing: bool):
        """Set the play state - EXACTLY matching React behavior."""
        self._is_playing = is_playing
        self.play_button.setActive(is_playing)
        
        # Update icon based on state
        self._update_play_button_icon()
        
        # Update tooltip
        tooltip = "Pause" if is_playing else "Play"
        self.play_button.setTooltip(tooltip)
        
        # EXACTLY matching React className="animate-glow" behavior
        if is_playing:
            # Start glow animation when playing
            self._glow_animation.start()
        else:
            # Stop glow animation when paused
            self._glow_animation.stop()
            # Reset glow intensity to 0
            self.play_button.setProperty("glow_intensity", 0.0)
            self.play_button.update()
        
    def getPlayState(self) -> bool:
        """Get the current play state."""
        return self._is_playing
        
    def setActiveTransformTool(self, tool: str):
        """Set the active transform tool."""
        self._on_transform_tool_changed(tool)
        
    def getActiveTransformTool(self) -> str:
        """Get the currently active transform tool."""
        return self._active_transform_tool
        
    def setActiveTab(self, tab_name: str):
        """Set the active tab in breadcrumb."""
        self.active_tab_label.setText(tab_name)
