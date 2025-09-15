"""
Viewport widget for 3D scene rendering.

This module contains the main viewport widget that displays
the 3D scene using OpenGL rendering.
"""

import numpy as np
from typing import Optional, Tuple
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QKeySequence, QShortcut, QMouseEvent, QWheelEvent

from ..rendering.renderer import Renderer
from ..utils.logger import get_logger


class ViewportWidget(QWidget):
    """Main 3D viewport widget."""
    
    # Signals
    viewport_clicked = pyqtSignal(QPoint)
    viewport_resized = pyqtSignal(int, int)
    
    def __init__(self, game_engine):
        """Initialize the viewport widget.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        
        self.game_engine = game_engine
        self.logger = get_logger(__name__)
        
        # Viewport state
        self.is_initialized = False
        self.is_rendering = False
        
        # Camera state
        self.camera_position = np.array([0.0, 5.0, 10.0], dtype=np.float32)
        self.camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        # Mouse state
        self.mouse_pressed = False
        self.last_mouse_pos = QPoint()
        self.mouse_sensitivity = 0.01
        
        # Setup UI
        self._setup_ui()
        self._setup_shortcuts()
        self._setup_timers()
        
        # Initialize OpenGL context
        self._init_opengl()
        
        self.logger.info("✅ Viewport widget initialized")
    
    def _setup_ui(self):
        """Setup the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Viewport info label
        self.info_label = QLabel("Viewport - Press F1 for help")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("background-color: rgba(0,0,0,0.7); color: white; padding: 5px;")
        layout.addWidget(self.info_label)
        
        # Set focus policy for keyboard input
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Help shortcut
        help_shortcut = QShortcut(QKeySequence("F1"), self)
        help_shortcut.activated.connect(self._show_help)
        
        # Camera shortcuts
        reset_camera_shortcut = QShortcut(QKeySequence("R"), self)
        reset_camera_shortcut.activated.connect(self._reset_camera)
        
        # View shortcuts
        front_view_shortcut = QShortcut(QKeySequence("1"), self)
        front_view_shortcut.activated.connect(lambda: self._set_view("front"))
        
        side_view_shortcut = QShortcut(QKeySequence("2"), self)
        side_view_shortcut.activated.connect(lambda: self._set_view("side"))
        
        top_view_shortcut = QShortcut(QKeySequence("3"), self)
        top_view_shortcut.activated.connect(lambda: self._set_view("top"))
        
        perspective_view_shortcut = QShortcut(QKeySequence("4"), self)
        perspective_view_shortcut.activated.connect(lambda: self._set_view("perspective"))
    
    def _setup_timers(self):
        """Setup timers for rendering and updates."""
        # Render timer
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self._render_frame)
        self.render_timer.start(16)  # ~60 FPS
        
        # Info update timer
        self.info_timer = QTimer()
        self.info_timer.timeout.connect(self._update_info)
        self.info_timer.start(1000)  # 1 FPS
    
    def _init_opengl(self):
        """Initialize OpenGL context."""
        try:
            # This will be implemented when we add the actual OpenGL renderer
            # For now, just mark as initialized
            self.is_initialized = True
            self.logger.info("✅ OpenGL context initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize OpenGL: {e}")
            self.is_initialized = False
    
    def _render_frame(self):
        """Render a single frame."""
        if not self.is_initialized or not self.is_rendering:
            return
        
        try:
            # Update camera matrices
            self._update_camera()
            
            # Render the scene
            if self.game_engine and self.game_engine.renderer:
                self.game_engine.renderer.render_scene()
            
            # Update viewport
            self.update()
            
        except Exception as e:
            self.logger.error(f"❌ Error rendering frame: {e}")
    
    def _update_camera(self):
        """Update camera matrices."""
        # This will be implemented with the actual camera system
        pass
    
    def _update_info(self):
        """Update viewport information display."""
        if self.game_engine and self.game_engine.is_initialized:
            stats = self.game_engine.get_stats()
            info_text = f"Viewport - FPS: {stats.fps:.1f} | Entities: {stats.entity_count} | Press F1 for help"
            self.info_label.setText(info_text)
    
    def _show_help(self):
        """Show viewport help information."""
        help_text = """
Viewport Controls:
- Mouse: Rotate camera
- Mouse wheel: Zoom in/out
- WASD: Move camera
- R: Reset camera
- 1: Front view
- 2: Side view  
- 3: Top view
- 4: Perspective view
- F1: Show this help
        """
        self.logger.info("Showing viewport help")
        # TODO: Implement help dialog
        print(help_text)
    
    def _reset_camera(self):
        """Reset camera to default position."""
        self.camera_position = np.array([0.0, 5.0, 10.0], dtype=np.float32)
        self.camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.logger.info("Camera reset to default position")
    
    def _set_view(self, view_type: str):
        """Set camera to a predefined view.
        
        Args:
            view_type: Type of view to set
        """
        if view_type == "front":
            self.camera_position = np.array([0.0, 0.0, 10.0], dtype=np.float32)
            self.camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
            self.camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        elif view_type == "side":
            self.camera_position = np.array([10.0, 0.0, 0.0], dtype=np.float32)
            self.camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
            self.camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        elif view_type == "top":
            self.camera_position = np.array([0.0, 10.0, 0.0], dtype=np.float32)
            self.camera_target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
            self.camera_up = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        elif view_type == "perspective":
            self._reset_camera()
        
        self.logger.info(f"Camera set to {view_type} view")
    
    def start_rendering(self):
        """Start the rendering loop."""
        self.is_rendering = True
        self.logger.info("🎬 Rendering started")
    
    def stop_rendering(self):
        """Stop the rendering loop."""
        self.is_rendering = False
        self.logger.info("⏹️ Rendering stopped")
    
    def resizeEvent(self, event):
        """Handle viewport resize events."""
        super().resizeEvent(event)
        
        width = event.size().width()
        height = event.size().height()
        
        # Update viewport size
        if self.game_engine and self.game_engine.renderer:
            self.game_engine.renderer.resize_viewport(width, height)
        
        # Emit resize signal
        self.viewport_resized.emit(width, height)
        
        self.logger.debug(f"Viewport resized to {width}x{height}")
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            self.last_mouse_pos = event.pos()
            self.setFocus()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
        
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events."""
        if self.mouse_pressed:
            # Calculate mouse delta
            delta = event.pos() - self.last_mouse_pos
            
            # Rotate camera based on mouse movement
            self._rotate_camera(delta.x(), delta.y())
            
            self.last_mouse_pos = event.pos()
        
        super().mouseMoveEvent(event)
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel events."""
        # Zoom camera
        zoom_factor = 0.1
        if event.angleDelta().y() > 0:
            # Zoom in
            self._zoom_camera(1.0 + zoom_factor)
        else:
            # Zoom out
            self._zoom_camera(1.0 - zoom_factor)
        
        super().wheelEvent(event)
    
    def _rotate_camera(self, delta_x: int, delta_y: int):
        """Rotate camera based on mouse movement.
        
        Args:
            delta_x: Horizontal mouse movement
            delta_y: Vertical mouse movement
        """
        # This will be implemented with the actual camera system
        # For now, just log the movement
        self.logger.debug(f"Camera rotation: {delta_x}, {delta_y}")
    
    def _zoom_camera(self, factor: float):
        """Zoom camera in or out.
        
        Args:
            factor: Zoom factor (>1 for zoom in, <1 for zoom out)
        """
        # This will be implemented with the actual camera system
        # For now, just log the zoom
        self.logger.debug(f"Camera zoom: {factor}")
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        key = event.key()
        
        # Camera movement
        if key == Qt.Key.Key_W:
            self._move_camera_forward()
        elif key == Qt.Key.Key_S:
            self._move_camera_backward()
        elif key == Qt.Key.Key_A:
            self._move_camera_left()
        elif key == Qt.Key.Key_D:
            self._move_camera_right()
        elif key == Qt.Key.Key_Q:
            self._move_camera_up()
        elif key == Qt.Key.Key_E:
            self._move_camera_down()
        
        super().keyPressEvent(event)
    
    def _move_camera_forward(self):
        """Move camera forward."""
        # This will be implemented with the actual camera system
        self.logger.debug("Camera moving forward")
    
    def _move_camera_backward(self):
        """Move camera backward."""
        # This will be implemented with the actual camera system
        self.logger.debug("Camera moving backward")
    
    def _move_camera_left(self):
        """Move camera left."""
        # This will be implemented with the actual camera system
        self.logger.debug("Camera moving left")
    
    def _move_camera_right(self):
        """Move camera right."""
        # This will be implemented with the actual camera system
        self.logger.debug("Camera moving right")
    
    def _move_camera_up(self):
        """Move camera up."""
        # This will be implemented with the actual camera system
        self.logger.debug("Camera moving up")
    
    def _move_camera_down(self):
        """Move camera down."""
        # This will be implemented with the actual camera system
        self.logger.debug("Camera moving down")
    
    def setup_shortcuts(self):
        """Setup viewport-specific shortcuts."""
        # This method is called by the main window
        # Shortcuts are already set up in _setup_shortcuts
        pass
