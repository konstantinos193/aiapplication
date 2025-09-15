"""
3D Viewport Panel for Nexlify Engine.

This module provides a 3D viewport interface similar to Unity's Scene view,
allowing users to view and manipulate 3D scenes with camera controls and gizmos.
"""

from typing import Optional, Tuple, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QPushButton, QComboBox, QSlider, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPointF, QRectF, QPoint
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QWheelEvent, QMouseEvent, QKeyEvent, QPolygonF
import math
import time

from ..utils.logger import get_logger
from ..core.game_object import GameObject
from .design_system.spacing_system import spacing
from .design_system.typography_system import typography


class Camera:
    """Simple camera class for viewport navigation."""
    
    def __init__(self):
        self.position = [0.0, 5.0, 10.0]  # x, y, z
        self.target = [0.0, 0.0, 0.0]     # Look at point
        self.up = [0.0, 1.0, 0.0]         # Up vector
        self.fov = 60.0                    # Field of view
        self.near_plane = 0.1
        self.far_plane = 1000.0
        
        # Camera controls
        self.orbit_distance = 10.0
        self.orbit_angles = [0.0, 0.0]     # [horizontal, vertical]
        self.pan_offset = [0.0, 0.0]      # [x, z] pan offset
    
    def orbit(self, horizontal: float, vertical: float):
        """Orbit the camera around the target."""
        self.orbit_angles[0] += horizontal
        self.orbit_angles[1] += vertical
        
        # Clamp vertical angle to prevent flipping
        self.orbit_angles[1] = max(-89.0, min(89.0, self.orbit_angles[1]))
        
        # Calculate new position
        import math
        rad_h = math.radians(self.orbit_angles[0])
        rad_v = math.radians(self.orbit_angles[1])
        
        self.position[0] = self.target[0] + self.orbit_distance * math.cos(rad_v) * math.sin(rad_h)
        self.position[1] = self.target[1] + self.orbit_distance * math.sin(rad_v)
        self.position[2] = self.target[2] + self.orbit_distance * math.cos(rad_v) * math.cos(rad_h)
    
    def pan(self, delta_x: float, delta_y: float):
        """Pan the camera and target."""
        # Calculate right vector
        import math
        forward = self._normalize([self.target[0] - self.position[0], 
                                 self.target[1] - self.position[1], 
                                 self.target[2] - self.position[2]])
        right = self._cross(forward, self.up)
        
        # Pan amount based on distance
        pan_speed = self.orbit_distance * 0.01
        
        # Update target
        self.target[0] += right[0] * delta_x * pan_speed
        self.target[2] += right[2] * delta_x * pan_speed
        self.target[1] -= delta_y * pan_speed
        
        # Update position to maintain distance
        self.orbit(0, 0)
    
    def zoom(self, factor: float):
        """Zoom the camera in/out."""
        self.orbit_distance = max(1.0, self.orbit_distance * factor)
        self.orbit(0, 0)
    
    def focus_on_object(self, game_object: GameObject):
        """Focus camera on a specific GameObject."""
        if game_object and hasattr(game_object, 'transform'):
            # Set target to object position
            self.target = game_object.transform.position.copy()
            # Adjust distance based on object scale
            max_scale = max(game_object.transform.scale)
            self.orbit_distance = max(5.0, max_scale * 3.0)
            self.orbit(0, 0)
    
    def _normalize(self, vector):
        """Normalize a vector."""
        import math
        length = math.sqrt(sum(x*x for x in vector))
        if length > 0:
            return [x/length for x in vector]
        return vector
    
    def _cross(self, a, b):
        """Cross product of two vectors."""
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]
        ]


class ThreeDViewportWidget(QWidget):
    """Professional 3D viewport widget with advanced rendering."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_viewport = parent
        self.logger = get_logger(__name__)
        
        # FPS tracking
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
        
        # Setup timer for rendering
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self._update_fps)
        self.render_timer.start(1000)  # Update FPS every second
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_animation)
        self.animation_timer.start(16)  # 60 FPS for smooth animation
        
        # Animation state
        self.animation_time = 0.0
        
        # Crash protection
        self.crash_count = 0
        self.max_crashes = 3
        
    def _update_fps(self):
        """Update FPS counter."""
        current_time = time.time()
        if self.last_fps_time > 0:
            self.current_fps = self.frame_count / (current_time - self.last_fps_time)
        self.frame_count = 0
        self.last_fps_time = current_time
    
    def _update_animation(self):
        """Update animation state."""
        self.animation_time += 0.016  # 16ms = 60 FPS
        if self.animation_time > 360:  # Reset after full rotation
            self.animation_time = 0
        self.update()
    
    def paintEvent(self, event):
        """Paint the 3D viewport."""
        try:
            self.frame_count += 1
            
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Set up the viewport
            painter.setViewport(0, 0, self.width(), self.height())
            
            # Clear background with gradient
            self._draw_background(painter)
            
            # Draw 3D grid
            self._draw_3d_grid(painter)
            
            # Draw 3D objects
            self._draw_3d_objects(painter)
            
            # Draw coordinate axes
            self._draw_coordinate_axes(painter)
            
            # Draw UI overlays
            self._draw_ui_overlays(painter)
            
            # Draw FPS counter (bottom right)
            self._draw_fps_counter(painter)
            
        except Exception as e:
            self.crash_count += 1
            self.logger.error(f"CRASH #{self.crash_count} in paintEvent: {e}", exc_info=True)
            
            # Stop rendering if too many crashes
            if self.crash_count >= self.max_crashes:
                self.logger.error("Too many crashes, stopping rendering")
                self.animation_timer.stop()
                self.render_timer.stop()
                return
            
            # Draw error message on screen
            try:
                painter = QPainter(self)
                painter.fillRect(self.rect(), QColor(255, 0, 0, 100))
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"CRASH #{self.crash_count}: {str(e)}")
            except:
                pass
    
    def _draw_background(self, painter):
        """Draw professional gradient background."""
        # Create a more appealing dark background
        background_color = QColor(20, 22, 25)  # Slightly bluish dark
        painter.fillRect(self.rect(), background_color)
        
        # Add subtle grid pattern overlay for depth
        painter.setPen(QPen(QColor(30, 32, 35), 1))
        for x in range(0, self.width(), 30):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 30):
            painter.drawLine(0, y, self.width(), y)
    
    def _draw_3d_grid(self, painter):
        """Draw the 3D grid."""
        # Always show grid for now (can be made configurable later)
        
        # Professional grid with better visibility
        grid_size = 15  # Reduced for better performance
        grid_spacing = 2.0  # Increased spacing for better visibility
        
        # Create depth effect with multiple grid layers
        for layer in range(2):  # Reduced layers for better performance
            alpha = 60 - layer * 20  # Increased alpha for better visibility
            if alpha < 20:
                alpha = 20
                
            # Grid line colors with better contrast
            minor_pen = QPen(QColor(80, 80, 100, alpha), 1)
            major_pen = QPen(QColor(120, 120, 140, alpha), 2)
            
            for i in range(-grid_size, grid_size + 1):
                # Vertical lines (X-axis)
                pen = major_pen if i == 0 else minor_pen
                painter.setPen(pen)
                
                # Add depth offset for 3D effect
                depth_offset = layer * 1.0
                x1, y1 = self._world_to_screen(i * grid_spacing, depth_offset, -grid_size * grid_spacing)
                x2, y2 = self._world_to_screen(i * grid_spacing, depth_offset, grid_size * grid_spacing)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
                
                # Horizontal lines (Z-axis)
                x1, y1 = self._world_to_screen(-grid_size * grid_spacing, depth_offset, i * grid_spacing)
                x2, y2 = self._world_to_screen(grid_size * grid_spacing, depth_offset, i * grid_spacing)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    
    def _draw_3d_objects(self, painter):
        """Draw 3D objects in the scene."""
        try:
            if not self.parent_viewport.game_engine:
                self.logger.debug("No game engine available")
                return
            
            # Get scene objects
            scene = self.parent_viewport.game_engine.get_current_scene()
            if not scene:
                self.logger.debug("No current scene available")
                return
            
            self.logger.debug(f"Drawing scene: {scene.name}")
            game_objects = scene.get_all_objects()
            self.logger.debug(f"Found {len(game_objects)} game objects")
            
            for game_object in game_objects:
                try:
                    if hasattr(game_object, 'transform'):
                        pos = game_object.transform.position
                        self.logger.debug(f"Drawing {game_object.name} at position {pos}")
                        self._draw_game_object(painter, game_object, pos)
                    else:
                        self.logger.debug(f"GameObject {game_object.name} has no transform")
                except Exception as e:
                    self.logger.error(f"Error drawing GameObject {game_object.name}: {e}", exc_info=True)
                    
        except Exception as e:
            self.logger.error(f"CRASH in _draw_3d_objects: {e}", exc_info=True)
            raise
    
    def _draw_game_object(self, painter, game_object, position):
        """Draw a single GameObject with professional styling."""
        try:
            self.logger.debug(f"Drawing GameObject: {game_object.name}")
            
            # Convert 3D position to 2D screen position
            screen_x, screen_y = self._world_to_screen(position[0], position[1], position[2])
            self.logger.debug(f"3D position {position} -> 2D screen position ({screen_x}, {screen_y})")
            
            if game_object.name == "Main Camera":
                # Professional camera representation - more visible
                camera_size = 15  # Larger for better visibility
                
                # Camera shadow
                painter.setPen(QPen(QColor(0, 0, 0, 0), 0))
                painter.setBrush(QBrush(QColor(0, 0, 0, 60)))  # Darker shadow
                painter.drawEllipse(int(screen_x - camera_size - 3), int(screen_y - camera_size - 3), 
                                  (camera_size + 3) * 2, (camera_size + 3) * 2)
                
                # Camera body (blue with glow) - brighter
                painter.setPen(QPen(QColor(0, 150, 255), 3))  # Brighter blue, thicker line
                painter.setBrush(QBrush(QColor(0, 150, 255, 180)))  # More opaque
                painter.drawEllipse(int(screen_x - camera_size), int(screen_y - camera_size), 
                                  camera_size * 2, camera_size * 2)
                
                # Camera lens (white with highlight) - more visible
                lens_size = camera_size * 0.7  # Larger lens
                painter.setPen(QPen(QColor(255, 255, 255), 2))  # Thicker line
                painter.setBrush(QBrush(QColor(255, 255, 255, 220)))  # More opaque
                painter.drawEllipse(int(screen_x - lens_size), int(screen_y - lens_size),
                                  int(lens_size * 2), int(lens_size * 2))
                
                # Camera label with background - more visible
                self._draw_label_with_background(painter, "Camera", screen_x, screen_y + camera_size + 20, 
                                               QColor(0, 150, 255), QColor(0, 150, 255, 120))
                
            elif game_object.name == "Directional Light":
                # Professional light representation - more visible
                light_size = 12  # Larger for better visibility
                
                # Light glow effect - more visible
                for glow_size in [light_size + 6, light_size + 3, light_size]:
                    alpha = 50 - (glow_size - light_size) * 15  # Higher alpha values
                    if alpha < 15:
                        alpha = 15
                    painter.setPen(QPen(QColor(255, 180, 0, alpha), 2))  # Brighter orange, thicker
                    painter.setBrush(QBrush(QColor(255, 180, 0, alpha)))
                    painter.drawEllipse(int(screen_x - glow_size), int(screen_y - glow_size), 
                                      glow_size * 2, glow_size * 2)
                
                # Light source - brighter
                painter.setPen(QPen(QColor(255, 180, 0), 3))  # Thicker line
                painter.setBrush(QBrush(QColor(255, 180, 0, 240)))  # More opaque
                painter.drawEllipse(int(screen_x - light_size), int(screen_y - light_size), 
                                  light_size * 2, light_size * 2)
                
                # Animated light rays - more visible
                ray_length = light_size * 2.0  # Longer rays
                for i, angle in enumerate([0, 45, 90, 135, 180, 225, 270, 315]):
                    rad = math.radians(angle + self.animation_time * 20)  # Animate rotation
                    end_x = screen_x + math.cos(rad) * ray_length
                    end_y = screen_y + math.sin(rad) * ray_length
                    
                    # Vary ray opacity for depth - higher values
                    opacity = 200 - (i * 20)  # Higher base opacity
                    if opacity < 80:
                        opacity = 80
                    painter.setPen(QPen(QColor(255, 180, 0, opacity), 2))  # Thicker rays
                    painter.drawLine(int(screen_x), int(screen_y), int(end_x), int(end_y))
                
                # Light label - more visible
                self._draw_label_with_background(painter, "Light", screen_x, screen_y + light_size + 20,
                                               QColor(255, 180, 0), QColor(255, 180, 0, 120))
                
            elif game_object.name == "Ground":
                # Professional ground representation - more visible
                ground_size = 25  # Larger for better visibility
                
                # Ground shadow - darker
                painter.setPen(QPen(QColor(0, 0, 0, 0), 0))
                painter.setBrush(QBrush(QColor(0, 0, 0, 80)))  # Darker shadow
                painter.drawEllipse(int(screen_x - ground_size), int(screen_y - ground_size),
                                  ground_size * 2, ground_size * 2)
                
                # Ground plane with texture - more visible
                painter.setPen(QPen(QColor(120, 120, 120), 3))  # Thicker border, brighter
                painter.setBrush(QBrush(QColor(80, 80, 80, 200)))  # More opaque
                painter.drawRect(int(screen_x - ground_size), int(screen_y - ground_size),
                               ground_size * 2, ground_size * 2)
                
                # Ground texture lines - more visible
                for i in range(-ground_size + 5, ground_size, 8):  # Wider spacing
                    painter.setPen(QPen(QColor(140, 140, 140, 150), 2))  # Brighter, thicker
                    painter.drawLine(int(screen_x + i), int(screen_y - ground_size),
                                   int(screen_x + i), int(screen_y + ground_size))
                    painter.drawLine(int(screen_x - ground_size), int(screen_y + i),
                                   int(screen_x + ground_size), int(screen_y + i))
                
                # Ground label - more visible
                self._draw_label_with_background(painter, "Ground", screen_x, screen_y + ground_size + 20,
                                               QColor(220, 220, 220), QColor(100, 100, 100, 150))
                
            else:
                # Professional generic object representation - more visible
                obj_size = 10  # Larger for better visibility
                
                # Object shadow - darker
                painter.setPen(QPen(QColor(0, 0, 0, 0), 0))
                painter.setBrush(QBrush(QColor(0, 0, 0, 60)))  # Darker shadow
                painter.drawEllipse(int(screen_x - obj_size), int(screen_y - obj_size),
                                  obj_size * 2, obj_size * 2)
                
                # Object body with glow - brighter
                painter.setPen(QPen(QColor(255, 255, 255), 3))  # Thicker line
                painter.setBrush(QBrush(QColor(255, 255, 255, 200)))  # More opaque
                painter.drawEllipse(int(screen_x - obj_size), int(screen_y - obj_size),
                                  obj_size * 2, obj_size * 2)
                
                # Object label - more visible
                self._draw_label_with_background(painter, game_object.name, screen_x, screen_y + obj_size + 20,
                                               QColor(255, 255, 255), QColor(120, 120, 120, 150))
                
        except Exception as e:
            self.logger.error(f"CRASH in _draw_game_object for {game_object.name}: {e}", exc_info=True)
            raise
    
    def _draw_label_with_background(self, painter, text, x, y, text_color, bg_color):
        """Draw text with a background rectangle."""
        # Draw background
        painter.setPen(QPen(QColor(0, 0, 0, 0), 0))
        painter.setBrush(QBrush(bg_color))
        
        # Calculate text size - larger font for better readability
        font = QFont("Segoe UI", 9, QFont.Weight.Bold)  # Larger, bold font
        painter.setFont(font)
        text_rect = painter.fontMetrics().boundingRect(text)
        
        # Draw background rectangle - larger padding
        bg_rect = QRectF(x - text_rect.width()/2 - 6, y - text_rect.height()/2 - 3,
                         text_rect.width() + 12, text_rect.height() + 6)
        painter.drawRoundedRect(bg_rect, 4, 4)  # Larger radius
        
        # Draw text
        painter.setPen(text_color)
        painter.drawText(int(x - text_rect.width()/2), int(y + text_rect.height()/2), text)
    
    def _draw_coordinate_axes(self, painter):
        """Draw 3D coordinate axes with professional styling."""
        try:
            # Center point
            center_x, center_y = self._world_to_screen(0, 0, 0)
        
            # X-axis (Red) with arrow - more visible
            painter.setPen(QPen(QColor(255, 80, 80), 4))  # Brighter red with thicker line
            x_end, y_end = self._world_to_screen(8, 0, 0)  # Longer axis for better visibility
            painter.drawLine(int(center_x), int(center_y), int(x_end), int(y_end))
            
            # X-axis arrow
            arrow_size = 10  # Larger arrow
            painter.setBrush(QBrush(QColor(255, 80, 80)))
            arrow_points = QPolygonF([
                QPointF(x_end, y_end),
                QPointF(x_end - arrow_size, y_end - arrow_size//2),
                QPointF(x_end - arrow_size, y_end + arrow_size//2)
            ])
            painter.drawPolygon(arrow_points)
            
            # Y-axis (Green) with arrow - more visible
            painter.setPen(QPen(QColor(80, 255, 80), 4))  # Brighter green with thicker line
            y_end, y_end = self._world_to_screen(0, 8, 0)  # Longer axis for better visibility
            painter.drawLine(int(center_x), int(center_y), int(y_end), int(y_end))
            
            # Y-axis arrow
            painter.setBrush(QBrush(QColor(80, 255, 80)))
            arrow_points = QPolygonF([
                QPointF(y_end, y_end),
                QPointF(y_end - arrow_size//2, y_end - arrow_size),
                QPointF(y_end + arrow_size//2, y_end - arrow_size)
            ])
            painter.drawPolygon(arrow_points)
            
            # Z-axis (Blue) with arrow - more visible
            painter.setPen(QPen(QColor(80, 80, 255), 4))  # Brighter blue with thicker line
            z_end, z_end = self._world_to_screen(0, 0, 8)  # Longer axis for better visibility
            painter.drawLine(int(center_x), int(center_y), int(z_end), int(z_end))
            
            # Z-axis arrow
            painter.setBrush(QBrush(QColor(80, 80, 255)))
            arrow_points = QPolygonF([
                QPointF(z_end, z_end),
                QPointF(z_end - arrow_size, z_end - arrow_size//2),
                QPointF(z_end - arrow_size, z_end + arrow_size//2)
            ])
            painter.drawPolygon(arrow_points)
            
            # Axis labels with backgrounds - more visible
            self._draw_label_with_background(painter, "X", x_end + 15, y_end, 
                                           QColor(255, 80, 80), QColor(255, 80, 80, 80))
            self._draw_label_with_background(painter, "Y", y_end, y_end + 20, 
                                           QColor(80, 255, 80), QColor(80, 255, 80, 80))
            self._draw_label_with_background(painter, "Z", z_end + 15, z_end, 
                                           QColor(80, 80, 255), QColor(80, 80, 255, 80))
        
        except Exception as e:
            self.logger.error(f"CRASH in _draw_coordinate_axes: {e}", exc_info=True)
            raise
    
    def _draw_ui_overlays(self, painter):
        """Draw UI overlays on top of 3D scene."""
        # View mode indicator with background
        self._draw_label_with_background(painter, f"View: Perspective", 
                                       10, 20, QColor(255, 255, 255), QColor(0, 0, 0, 80))
        
        # Camera info with background
        scene = self.parent_viewport.game_engine.get_current_scene()
        if scene:
            camera_obj = scene.find_game_object("Main Camera")
            if camera_obj and hasattr(camera_obj, 'transform'):
                camera_pos = camera_obj.transform.position
                camera_text = f"Camera: ({camera_pos[0]:.1f}, {camera_pos[1]:.1f}, {camera_pos[2]:.1f})"
                self._draw_label_with_background(painter, camera_text, 10, 40, 
                                               QColor(255, 255, 255), QColor(0, 0, 0, 80))
    
    def _draw_fps_counter(self, painter):
        """Draw FPS counter in bottom right corner."""
        # FPS background - more visible
        painter.setPen(QPen(QColor(0, 0, 0, 0), 0))
        painter.setBrush(QBrush(QColor(0, 0, 0, 180)))  # More opaque
        
        # FPS text
        fps_text = f"FPS: {self.current_fps:.1f}"
        font = QFont("Segoe UI", 11, QFont.Weight.Bold)  # Larger font
        painter.setFont(font)
        text_rect = painter.fontMetrics().boundingRect(fps_text)
        
        # Position in bottom right
        x = self.width() - text_rect.width() - 25  # More padding
        y = self.height() - 15  # More padding
        
        # Draw background rectangle - larger
        bg_rect = QRectF(x - 10, y - text_rect.height() - 6,
                         text_rect.width() + 20, text_rect.height() + 12)
        painter.drawRoundedRect(bg_rect, 6, 6)  # Larger radius
        
        # Draw FPS text
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(int(x), int(y), fps_text)
        
        # Add subtle border - more visible
        painter.setPen(QPen(QColor(0, 150, 255, 200), 2))  # Thicker, more opaque
        painter.drawRoundedRect(bg_rect, 6, 6)
    
    def _world_to_screen(self, x, y, z):
        """Convert 3D world coordinates to 2D screen coordinates."""
        # Get camera from the current scene
        scene = self.parent_viewport.game_engine.get_current_scene()
        if scene:
            # Find the main camera
            camera_obj = scene.find_game_object("Main Camera")
            if camera_obj and hasattr(camera_obj, 'transform'):
                camera_pos = camera_obj.transform.position
                
                # Calculate relative position from camera
                rel_x = x - camera_pos[0]
                rel_y = y - camera_pos[1]
                rel_z = z - camera_pos[2]
                
                # Simple perspective projection
                distance = math.sqrt(rel_x**2 + rel_y**2 + rel_z**2)
                if distance > 0:
                    # Perspective factor - adjust for better visibility
                    perspective = 100.0 / (distance + 1.0)  # Add 1 to avoid division by zero
                    
                    # Convert to screen coordinates
                    screen_x = self.width() / 2 + rel_x * perspective
                    screen_y = self.height() / 2 + rel_z * perspective  # Use Z for Y screen coordinate
                    
                    return screen_x, screen_y
        
        # Fallback to simple projection with better scaling
        scale = 15.0  # Reduced scale for better visibility
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        screen_x = center_x + x * scale
        screen_y = center_y + z * scale  # Use Z for Y screen coordinate
        
        return screen_x, screen_y
    
    def resizeEvent(self, event):
        """Handle viewport resize."""
        super().resizeEvent(event)
        self.update()


class GizmoHandle(QWidget):
    """Gizmo handle for object manipulation."""
    
    def __init__(self, gizmo_type: str, position: QPointF, size: float = 10.0):
        super().__init__()
        self.gizmo_type = gizmo_type
        self.position = position
        self.size = size
        self.is_selected = False
        
        # Set position and size
        self.setGeometry(int(position.x() - size/2), int(position.y() - size/2), int(size), int(size))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        # Professional color scheme
        if self.gizmo_type == "translate":
            color = QColor(0, 120, 215)      # Blue for translate
            hover_color = QColor(0, 150, 255) # Lighter blue for hover
        elif self.gizmo_type == "rotate":
            color = QColor(255, 140, 0)      # Orange for rotate
            hover_color = QColor(255, 170, 0) # Lighter orange for hover
        elif self.gizmo_type == "scale":
            color = QColor(170, 0, 255)      # Purple for scale
            hover_color = QColor(200, 0, 255) # Lighter purple for hover
        else:
            color = QColor(255, 255, 255)     # White default
            hover_color = QColor(255, 255, 255)
        
        if self.is_selected:
            color = QColor(255, 255, 0)       # Bright yellow when selected
            hover_color = QColor(255, 255, 0)
        
        # Professional gizmo styling
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.gizmo_type == "translate":
            # Professional arrow with gradient effect
            painter.setPen(QPen(color, 3))
            painter.setBrush(QBrush(color))
            
            # Arrow shaft
            painter.drawLine(0, int(self.size/2), 0, int(-self.size/2))
            
            # Arrow head (triangle)
            arrow_points = [
                QPointF(0, int(-self.size/2)),
                QPointF(int(-self.size/3), int(-self.size/2 + 8)),
                QPointF(int(self.size/3), int(-self.size/2 + 8))
            ]
            painter.drawPolygon(QPolygonF(arrow_points))
            
        elif self.gizmo_type == "rotate":
            # Professional circle with rotation indicator
            painter.setPen(QPen(color, 3))
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))  # Transparent fill
            
            # Main circle
            painter.drawEllipse(int(-self.size/2), int(-self.size/2), int(self.size), int(self.size))
            
            # Rotation indicator dots
            dot_size = 3
            for angle in [0, 90, 180, 270]:
                import math
                rad = math.radians(angle)
                dot_x = int(math.cos(rad) * (self.size/2 - 5))
                dot_y = int(math.sin(rad) * (self.size/2 - 5))
                painter.setBrush(QBrush(color))
                painter.drawEllipse(dot_x - dot_size, dot_y - dot_size, dot_size * 2, dot_size * 2)
                
        elif self.gizmo_type == "scale":
            # Professional scale gizmo with corner indicators
            painter.setPen(QPen(color, 3))
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))  # Transparent fill
            
            # Main square
            painter.drawRect(int(-self.size/2), int(-self.size/2), int(self.size), int(self.size))
            
            # Corner scale indicators
            corner_size = 4
            corners = [
                (-self.size/2, -self.size/2), (self.size/2, -self.size/2),
                (self.size/2, self.size/2), (-self.size/2, self.size/2)
            ]
            for corner_x, corner_y in corners:
                painter.setBrush(QBrush(color))
                painter.drawRect(int(corner_x - corner_size), int(corner_y - corner_size), 
                               corner_size * 2, corner_size * 2)
        
        # Add hover effect
        if self.is_selected:
            # Selection glow effect
            glow_color = QColor(255, 255, 0, 100)
            painter.setPen(QPen(glow_color, 6))
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            
            if self.gizmo_type == "translate":
                painter.drawLine(0, int(self.size/2 + 3), 0, int(-self.size/2 - 3))
            elif self.gizmo_type == "rotate":
                painter.drawEllipse(int(-self.size/2 - 3), int(-self.size/2 - 3), 
                                  int(self.size + 6), int(self.size + 6))
            elif self.gizmo_type == "scale":
                painter.drawRect(int(-self.size/2 - 3), int(-self.size/2 - 3), 
                               int(self.size + 6), int(self.size + 6))


class TransformGizmo:
    """Transform gizmo for object manipulation."""
    
    def __init__(self):
        self.handles = []
        self.selected_handle = None
        self.gizmo_mode = "translate"  # translate, rotate, scale
        self.is_visible = True
    
    def create_gizmo(self, position: QPointF, parent_widget=None):
        """Create gizmo handles at the given position."""
        # Clear existing handles
        for handle in self.handles:
            handle.deleteLater()
        self.handles.clear()
        
        # Create handles for each axis
        handle_size = 15.0
        offset = 30.0
        
        # X-axis handle (red)
        x_handle = GizmoHandle(self.gizmo_mode, position + QPointF(offset, 0), handle_size)
        if parent_widget:
            x_handle.setParent(parent_widget)
        self.handles.append(x_handle)
        
        # Y-axis handle (green)
        y_handle = GizmoHandle(self.gizmo_mode, position + QPointF(0, -offset), handle_size)
        if parent_widget:
            y_handle.setParent(parent_widget)
        self.handles.append(y_handle)
        
        # Z-axis handle (blue)
        z_handle = GizmoHandle(self.gizmo_mode, position + QPointF(0, offset), handle_size)
        if parent_widget:
            z_handle.setParent(parent_widget)
        self.handles.append(z_handle)
    
    def set_mode(self, mode: str):
        """Set the gizmo mode."""
        self.gizmo_mode = mode
        for handle in self.handles:
            handle.gizmo_type = mode
    
    def set_position(self, position: QPointF):
        """Update gizmo position."""
        offset = 30.0
        if len(self.handles) >= 3:
            self.handles[0].setGeometry(int(position.x() + offset - self.handles[0].size/2), 
                                       int(position.y() - self.handles[0].size/2), 
                                       int(self.handles[0].size), int(self.handles[0].size))
            self.handles[1].setGeometry(int(position.x() - self.handles[1].size/2), 
                                       int(position.y() - offset - self.handles[1].size/2), 
                                       int(self.handles[1].size), int(self.handles[1].size))
            self.handles[2].setGeometry(int(position.x() - self.handles[2].size/2), 
                                       int(position.y() + offset - self.handles[2].size/2), 
                                       int(self.handles[2].size), int(self.handles[2].size))
    
    def hide(self):
        """Hide the gizmo."""
        self.is_visible = False
        for handle in self.handles:
            handle.setVisible(False)
    
    def show(self):
        """Show the gizmo."""
        self.is_visible = True
        for handle in self.handles:
            handle.setVisible(True)


class ViewportPanel(QWidget):
    """3D viewport panel for viewing and editing 3D scenes."""
    
    # Signals
    view_changed = pyqtSignal(str)  # Emits view mode when changed
    selection_changed = pyqtSignal(object)  # Emits selected GameObject
    
    def __init__(self, main_window):
        """Initialize the viewport panel.
        
        Args:
            main_window: Reference to the main window
        """
        # Initialize logger first
        self.logger = get_logger(__name__)
        
        try:
            self.logger.info("Starting ViewportPanel initialization...")
            super().__init__()
            self.logger.info("QWidget initialized")
            
            self.main_window = main_window
            self.logger.info("Main window reference set")
            
            self.game_engine = main_window.game_engine
            self.logger.info("Game engine reference set")
            
            self.current_view_mode = "Perspective"
            self.show_grid = True
            self.show_gizmos = True
            self.camera_mode = "Scene"
            self.logger.info("Viewport properties initialized")
            
            # Camera and gizmo system
            self.camera = Camera()
            self.transform_gizmo = None  # Will be initialized after scene creation
            self.selected_object = None
            
            # Mouse interaction
            self.last_mouse_pos = None
            self.is_orbiting = False
            self.is_panning = False
            self.is_manipulating = False
            
            # Initialize collections to prevent attribute errors
            self._grid_items = []
            self._3d_objects = []
            self._scene_objects_rendered = False
            
            self._init_ui()
            self.logger.info("UI initialized")
            
            self._setup_styles()
            self.logger.info("Styles set up")
            
            self._setup_timer()
            self.logger.info("Timer set up")
            
            # Render 3D objects once after initialization
            self._render_3d_objects()
            self.logger.info("3D objects rendered")
            
            self.logger.info("Viewport panel initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing ViewportPanel: {e}")
            raise
    
    def _init_ui(self):
        """Initialize the user interface."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Top toolbar
        self._create_toolbar()
        
        # Main viewport area
        self._create_viewport_area()
        
        # Bottom status bar
        self._create_status_bar()
    
    def _create_status_bar(self):
        """Create the viewport status bar."""
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(spacing.sm, spacing.xs, spacing.sm, spacing.xs)  # 8px, 4px, 8px, 4px
        status_layout.setSpacing(spacing.md)  # 16px spacing between elements
        
        # Selection info
        self.selection_info_label = QLabel("Selected: None")
        self.selection_info_label.setStyleSheet(f"color: #e1e1e1; font-size: {typography.sm}px; font-weight: bold; padding: {spacing.xs}px {spacing.sm}px; background: rgba(0, 120, 215, 0.1); border-radius: 3px;")
        self.selection_info_label.setMinimumWidth(150)
        status_layout.addWidget(self.selection_info_label)
        
        # Mouse position
        self.mouse_pos_label = QLabel("Mouse: (0, 0)")
        self.mouse_pos_label.setStyleSheet(f"color: #e1e1e1; font-size: {typography.sm}px; font-weight: bold; padding: {spacing.xs}px {spacing.sm}px; background: rgba(255, 140, 0, 0.1); border-radius: 3px;")
        self.mouse_pos_label.setMinimumWidth(120)
        status_layout.addWidget(self.mouse_pos_label)
        
        # Camera info
        self.camera_info_label = QLabel("Camera: Idle")
        self.camera_info_label.setStyleSheet(f"color: #e1e1e1; font-size: {typography.sm}px; font-weight: bold; padding: {spacing.xs}px {spacing.sm}px; background: rgba(170, 0, 255, 0.1); border-radius: 3px;")
        self.camera_info_label.setMinimumWidth(120)
        status_layout.addWidget(self.camera_info_label)
        
        status_layout.addStretch()
        
        # Transform mode info
        self.transform_mode_label = QLabel("Transform: Translate")
        self.transform_mode_label.setStyleSheet(f"color: #e1e1e1; font-size: {typography.sm}px; font-weight: bold; padding: {spacing.xs}px {spacing.sm}px; background: rgba(0, 255, 0, 0.1); border-radius: 3px;")
        self.transform_mode_label.setMinimumWidth(140)
        status_layout.addWidget(self.transform_mode_label)
        
        self.main_layout.addWidget(status_frame)
    
    def _create_toolbar(self):
        """Create the viewport toolbar."""
        toolbar_frame = QFrame()
        toolbar_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(spacing.sm, spacing.xs, spacing.sm, spacing.xs)  # 8px, 4px, 8px, 4px
        toolbar_layout.setSpacing(spacing.sm)  # 8px spacing between elements
        
        # View mode selector
        view_label = QLabel("View:")
        view_label.setStyleSheet(f"color: #e1e1e1; font-size: {typography.sm}px; font-weight: bold; margin-right: {spacing.sm}px;")
        toolbar_layout.addWidget(view_label)
        
        self.view_mode_combo = QComboBox()
        self.view_mode_combo.addItems(["Perspective", "Orthographic", "Top", "Front", "Side"])
        self.view_mode_combo.setCurrentText(self.current_view_mode)
        self.view_mode_combo.currentTextChanged.connect(self._on_view_mode_changed)
        self.view_mode_combo.setMaximumWidth(130)
        self.view_mode_combo.setMinimumHeight(24)
        toolbar_layout.addWidget(self.view_mode_combo)
        
        toolbar_layout.addSpacing(spacing.lg)  # 20px spacing
        
        # Camera mode selector
        camera_label = QLabel("Camera:")
        camera_label.setStyleSheet(f"color: #e1e1e1; font-size: {typography.sm}px; font-weight: bold; margin-right: {spacing.sm}px;")
        toolbar_layout.addWidget(camera_label)
        
        self.camera_mode_combo = QComboBox()
        self.camera_mode_combo.addItems(["Scene", "Game"])
        self.camera_mode_combo.setCurrentText(self.camera_mode)
        self.camera_mode_combo.currentTextChanged.connect(self._on_camera_mode_changed)
        self.camera_mode_combo.setMaximumWidth(90)
        self.camera_mode_combo.setMinimumHeight(24)
        toolbar_layout.addWidget(self.camera_mode_combo)
        
        toolbar_layout.addSpacing(20)
        
        # Grid toggle
        self.grid_checkbox = QCheckBox("Grid")
        self.grid_checkbox.setChecked(self.show_grid)
        self.grid_checkbox.toggled.connect(self._on_grid_toggled)
        toolbar_layout.addWidget(self.grid_checkbox)
        
        # Gizmos toggle
        self.gizmos_checkbox = QCheckBox("Gizmos")
        self.gizmos_checkbox.setChecked(self.show_gizmos)
        self.gizmos_checkbox.toggled.connect(self._on_gizmos_toggled)
        toolbar_layout.addWidget(self.gizmos_checkbox)
        
        toolbar_layout.addStretch()
        
        # Zoom controls
        zoom_label = QLabel("Zoom:")
        zoom_label.setStyleSheet("color: #e1e1e1; font-size: 11px; font-weight: bold; margin-right: 8px;")
        toolbar_layout.addWidget(zoom_label)
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(10, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setMaximumWidth(120)
        self.zoom_slider.setMinimumHeight(20)
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        toolbar_layout.addWidget(self.zoom_slider)
        
        # Zoom percentage label
        self.zoom_percentage_label = QLabel("100%")
        self.zoom_percentage_label.setStyleSheet("color: #e1e1e1; font-size: 11px; font-weight: bold; margin-left: 8px;")
        self.zoom_percentage_label.setMinimumWidth(45)
        toolbar_layout.addWidget(self.zoom_percentage_label)
        
        self.main_layout.addWidget(toolbar_frame)
    
    def _create_viewport_area(self):
        """Create the main 3D viewport rendering area."""
        # Create a custom 3D viewport widget
        self.viewport_widget = ThreeDViewportWidget(self)
        self.viewport_widget.setFixedSize(500, 400)
        self.viewport_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d30, stop:1 #1e1e1e);
                border: 2px solid #0078d4;
                border-radius: 6px;
            }
        """)
        
        # Setup mouse and wheel events
        self.viewport_widget.installEventFilter(self)
        self.viewport_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Add viewport to layout
        self.main_layout.addWidget(self.viewport_widget)
        
        # Setup gizmo
        self.transform_gizmo = TransformGizmo()
        if not self.show_gizmos:
            self.transform_gizmo.hide()
    
    def _create_grid(self):
        """Create a professional 3D grid for the viewport."""
        # Grid is now handled by the 3D viewport widget
        pass
    
    def _update_grid(self):
        """Update grid visibility."""
        # Grid is now handled by the 3D viewport widget
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
    
    def _update_gizmo(self):
        """Update gizmo visibility and position."""
        # Gizmo is now handled by the 3D viewport widget
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
    
    # Coordinate conversion is now handled by the 3D viewport widget
    
    def _setup_styles(self):
        """Setup the panel styles."""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d30, stop:1 #1e1e1e);
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3e3e42, stop:1 #2d2d30);
                border: 2px solid #3e3e42;
                border-radius: 4px;
                padding: 6px 8px;
                color: #ffffff;
                selection-background-color: #0078d4;
                font-weight: bold;
                min-height: 20px;
            }
            QComboBox:hover {
                border-color: #0078d4;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4e4e52, stop:1 #3e3e42);
            }
            QComboBox:focus {
                border-color: #0078d4;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4e4e52, stop:1 #3e3e42);
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #0078d4;
                margin-right: 8px;
            }
            QSlider::groove:horizontal {
                border: 2px solid #3e3e42;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d30, stop:1 #1e1e1e);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                border: 2px solid #0078d4;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #0078d4);
                border-color: #106ebe;
            }
            QCheckBox {
                color: #e1e1e1;
                font-size: 11px;
                font-weight: bold;
                spacing: 8px;
            }
            QCheckBox:hover {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #3e3e42;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d30, stop:1 #1e1e1e);
            }
            QCheckBox::indicator:unchecked:hover {
                border-color: #0078d4;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #0078d4;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
            }
            QLabel {
                color: #e1e1e1;
                font-weight: bold;
            }
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3e3e42, stop:1 #2d2d30);
                border: 1px solid #3e3e42;
                border-radius: 4px;
            }
        """)
    
    def _setup_timer(self):
        """Setup timer for viewport updates."""
        # DISABLED: Timer was causing infinite resize loops
        # self.update_timer = QTimer()
        # self.update_timer.timeout.connect(self._update_viewport)
        # self.update_timer.start(500)  # 2 FPS - minimal updates to prevent resizing loops
        pass
    
    def _update_viewport(self):
        """Update the viewport display."""
        # Update the 3D viewport widget
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
    
    def _render_3d_objects(self):
        """Render 3D objects in the viewport."""
        # 3D objects are now rendered by the 3D viewport widget
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
        
        self._scene_objects_rendered = True
    
    # Event handlers
    def _on_view_mode_changed(self, view_mode):
        """Handle view mode change."""
        self.current_view_mode = view_mode
        self.view_changed.emit(view_mode)
        self.logger.info(f"View mode changed to: {view_mode}")
    
    def _on_camera_mode_changed(self, camera_mode):
        """Handle camera mode change."""
        self.camera_mode = camera_mode
        self.logger.info(f"Camera mode changed to: {camera_mode}")
    
    def _on_grid_toggled(self, checked):
        """Handle grid toggle."""
        self.show_grid = checked
        self.logger.info(f"Grid visibility: {checked}")
        self._update_grid()
    
    def _on_gizmos_toggled(self, checked):
        """Handle gizmos toggle."""
        self.show_gizmos = checked
        self.logger.info(f"Gizmos visibility: {checked}")
        # Update the 3D viewport widget
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
    
    def _on_zoom_changed(self, value):
        """Handle zoom change."""
        zoom_percentage = value
        self.zoom_percentage_label.setText(f"{zoom_percentage}%")
        self.logger.info(f"Zoom changed to: {zoom_percentage}%")
    
    def set_selection(self, game_object):
        """Set the currently selected GameObject.
        
        Args:
            game_object: The GameObject to select
        """
        self.selected_object = game_object
        # Update the 3D viewport widget
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
        if game_object:
            self.selection_info_label.setText(f"Selected: {game_object.name}")
            self.selection_changed.emit(game_object)
        else:
            self.selection_info_label.setText("Selected: None")
            self.selection_changed.emit(None)
    
    def refresh(self):
        """Refresh the viewport display."""
        # Update the 3D viewport widget
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
        self.logger.info("Viewport refreshed")
    
    def resizeEvent(self, event):
        """Handle viewport resize events."""
        super().resizeEvent(event)
        
        # CRITICAL: Prevent infinite resize loops by blocking excessive resizes
        if hasattr(self, '_last_size') and self._last_size == event.size():
            return
            
        # Log the resize but limit logging to prevent spam
        if not hasattr(self, '_resize_count'):
            self._resize_count = 0
        self._resize_count += 1
        
        if self._resize_count <= 5:  # Only log first 5 resizes
            self.logger.info(f"Viewport resized to: {event.size().width()}x{event.size().height()}")
        
        self._last_size = event.size()
        
        # IMPORTANT: Don't resize the graphics view - this causes the loop!
        # self.view.setFixedSize(event.size())  # This was the problem!
        
        # Update the 3D viewport widget after resize
        if hasattr(self, 'viewport_widget'):
            self.viewport_widget.update()
    
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        # In the future, this will handle 3D object selection
        pos = event.pos()
        self.mouse_pos_label.setText(f"Mouse: ({pos.x()}, {pos.y()})")
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        # In the future, this will handle camera movement and object manipulation
        pos = event.pos()
        self.mouse_pos_label.setText(f"Mouse: ({pos.x()}, {pos.y()})")
        super().mouseMoveEvent(event)

    def eventFilter(self, obj, event):
        """Event filter for viewport interactions."""
        if obj == self.viewport_widget:
            if event.type() == event.Type.MouseButtonPress:
                self._handle_mouse_press(event)
                return True
            elif event.type() == event.Type.MouseButtonRelease:
                self._handle_mouse_release(event)
                return True
            elif event.type() == event.Type.MouseMove:
                self._handle_mouse_move(event)
                return True
            elif event.type() == event.Type.Wheel:
                self._handle_wheel(event)
                return True
        return super().eventFilter(obj, event)
    
    def _handle_mouse_press(self, event):
        """Handle mouse button press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Start camera orbit
            self.is_orbiting = True
            self.last_mouse_pos = event.pos()
                
        elif event.button() == Qt.MouseButton.MiddleButton:
            # Start camera pan
            self.is_panning = True
            self.last_mouse_pos = event.pos()
    
    def _handle_mouse_release(self, event):
        """Handle mouse button release events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_orbiting = False
            self.is_manipulating = False
                
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = False
        
        self.last_mouse_pos = None
    
    def _handle_mouse_move(self, event):
        """Handle mouse move events."""
        if not self.last_mouse_pos:
            return
        
        current_pos = event.pos()
        delta = current_pos - self.last_mouse_pos
        
        if self.is_orbiting:
            # Camera orbit
            sensitivity = 0.5
            self.camera.orbit(delta.x() * sensitivity, delta.y() * sensitivity)
            self._update_camera_info()
            
        elif self.is_panning:
            # Camera pan
            sensitivity = 0.01
            self.camera.pan(delta.x() * sensitivity, delta.y() * sensitivity)
            self._update_camera_info()
            
        elif self.is_manipulating and self.selected_object:
            # Object manipulation
            self._handle_object_manipulation(delta)
        
        # Update mouse position display
        self.mouse_pos_label.setText(f"Mouse: ({current_pos.x()}, {current_pos.y()})")
        
        self.last_mouse_pos = current_pos
    
    def _handle_wheel(self, event):
        """Handle mouse wheel events for zooming."""
        zoom_factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.camera.zoom(zoom_factor)
        self._update_camera_info()
    
    def _handle_object_manipulation(self, delta):
        """Handle object manipulation through gizmo."""
        if not self.transform_gizmo or not self.transform_gizmo.selected_handle or not self.selected_object:
            return
        
        # Get the axis being manipulated
        axis = self.transform_gizmo.selected_handle.data(0)
        sensitivity = 0.1
        
        if self.transform_gizmo.gizmo_mode == "translate":
            if axis == "x":
                self.selected_object.transform.translate(delta.x() * sensitivity, 0, 0)
            elif axis == "y":
                self.selected_object.transform.translate(0, -delta.y() * sensitivity, 0)
            elif axis == "z":
                self.selected_object.transform.translate(0, 0, delta.y() * sensitivity)
                
        elif self.transform_gizmo.gizmo_mode == "rotate":
            if axis == "x":
                self.selected_object.transform.rotate(delta.y() * sensitivity, 0, 0)
            elif axis == "y":
                self.selected_object.transform.rotate(0, delta.x() * sensitivity, 0)
            elif axis == "z":
                self.selected_object.transform.rotate(0, 0, delta.x() * sensitivity)
                
        elif self.transform_gizmo.gizmo_mode == "scale":
            scale_factor = 1.0 + (delta.x() + delta.y()) * sensitivity * 0.01
            if axis == "x":
                self.selected_object.transform.scale_by(scale_factor, 1, 1)
            elif axis == "y":
                self.selected_object.transform.scale_by(1, scale_factor, 1)
            elif axis == "z":
                self.selected_object.transform.scale_by(1, 1, scale_factor)
        
        # Update gizmo position
        self._update_gizmo()
        
        # Emit selection changed signal to update inspector
        self.selection_changed.emit(self.selected_object)
    
    def _update_camera_info(self):
        """Update camera info display."""
        mode = "Orbit" if self.is_orbiting else "Pan" if self.is_panning else "Idle"
        self.camera_info_label.setText(f"Camera: {mode}")
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        if not self.transform_gizmo:
            super().keyPressEvent(event)
            return
            
        if event.key() == Qt.Key.Key_Q:
            # Switch to translate mode
            self.transform_gizmo.set_mode("translate")
            self.camera_info_label.setText("Gizmo: Translate")
        elif event.key() == Qt.Key.Key_W:
            # Switch to rotate mode
            self.transform_gizmo.set_mode("rotate")
            self.camera_info_label.setText("Gizmo: Rotate")
        elif event.key() == Qt.Key.Key_E:
            # Switch to scale mode
            self.transform_gizmo.set_mode("scale")
            self.camera_info_label.setText("Gizmo: Scale")
        elif event.key() == Qt.Key.Key_F:
            # Focus camera on selected object
            if self.selected_object:
                self.camera.focus_on_object(self.selected_object)
                self._update_camera_info()
        elif event.key() == Qt.Key.Key_Space:
            # Toggle gizmo visibility
            self.show_gizmos = not self.show_gizmos
            self.gizmos_checkbox.setChecked(self.show_gizmos)
            if self.show_gizmos:
                self.transform_gizmo.show()
            else:
                self.transform_gizmo.hide()
        
        super().keyPressEvent(event)