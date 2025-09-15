"""
Visual alignment guide for UI development and debugging.

This module provides visual overlays that show:
- Spacing measurements
- Alignment guides
- Grid lines
- Margin and padding indicators
"""

from typing import Dict, List, Optional, Tuple, Any
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath
import logging

from ..responsive import responsive_spacing_manager, Breakpoint
from ..design_system.spacing_system import spacing, SpacingUnit

logger = logging.getLogger(__name__)


class VisualAlignmentGuide(QWidget):
    """Visual overlay widget that shows spacing and alignment guides."""
    
    # Signals
    guide_clicked = pyqtSignal(str, int, int)  # guide_type, x, y
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Guide settings
        self.show_spacing_guides = True
        self.show_alignment_guides = True
        self.show_grid_guides = False
        self.show_margin_guides = True
        self.show_padding_guides = True
        
        # Visual settings
        self.guide_color = QColor(0, 255, 0, 100)  # Semi-transparent green
        self.text_color = QColor(255, 255, 255, 200)  # Semi-transparent white
        self.grid_color = QColor(100, 100, 255, 50)  # Semi-transparent blue
        
        # Guide data
        self.spacing_guides: List[Dict[str, Any]] = []
        self.alignment_guides: List[Dict[str, Any]] = []
        self.margin_guides: List[Dict[str, Any]] = []
        self.padding_guides: List[Dict[str, Any]] = []
        
        # Update timer for responsive updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_guides)
        self.update_timer.start(1000)  # Update every second
        
        logger.info("VisualAlignmentGuide initialized")
    
    def set_show_spacing_guides(self, show: bool):
        """Set whether to show spacing guides.
        
        Args:
            show: Whether to show spacing guides
        """
        self.show_spacing_guides = show
        self.update()
    
    def set_show_alignment_guides(self, show: bool):
        """Set whether to show alignment guides.
        
        Args:
            show: Whether to show alignment guides
        """
        self.show_alignment_guides = show
        self.update()
    
    def set_show_grid_guides(self, show: bool):
        """Set whether to show grid guides.
        
        Args:
            show: Whether to show grid guides
        """
        self.show_grid_guides = show
        self.update()
    
    def set_show_margin_guides(self, show: bool):
        """Set whether to show margin guides.
        
        Args:
            show: Whether to show margin guides
        """
        self.show_margin_guides = show
        self.update()
    
    def set_show_padding_guides(self, show: bool):
        """Set whether to show padding guides.
        
        Args:
            show: Whether to show padding guides
        """
        self.show_padding_guides = show
        self.update()
    
    def analyze_widget_spacing(self, widget: QWidget) -> Dict[str, Any]:
        """Analyze spacing for a specific widget.
        
        Args:
            widget: Widget to analyze
            
        Returns:
            Dictionary containing spacing analysis
        """
        try:
            analysis = {
                'widget_name': widget.objectName() or type(widget).__name__,
                'geometry': widget.geometry(),
                'margins': None,
                'padding': None,
                'spacing': None,
                'children': []
            }
            
            # Analyze layout if available
            if hasattr(widget, 'layout') and widget.layout():
                layout = widget.layout()
                analysis['margins'] = layout.contentsMargins()
                analysis['spacing'] = layout.spacing()
                
                # Analyze child widgets
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item.widget():
                        child_analysis = self.analyze_widget_spacing(item.widget())
                        analysis['children'].append(child_analysis)
            
            # Analyze responsive spacing if available
            if hasattr(widget, 'get_responsive_spacing'):
                try:
                    responsive_margin = widget.get_responsive_spacing(spacing.md)
                    responsive_padding = widget.get_responsive_spacing(spacing.sm)
                    analysis['responsive'] = {
                        'margin': responsive_margin,
                        'padding': responsive_padding
                    }
                except Exception as e:
                    logger.warning(f"Failed to get responsive spacing for {analysis['widget_name']}: {e}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze widget spacing: {e}")
            return {
                'widget_name': 'Unknown',
                'error': str(e)
            }
    
    def generate_spacing_guides(self, widget: QWidget):
        """Generate spacing guides for a widget.
        
        Args:
            widget: Widget to generate guides for
        """
        try:
            self.spacing_guides.clear()
            
            # Analyze the widget
            analysis = self.analyze_widget_spacing(widget)
            
            # Generate margin guides
            if analysis.get('margins'):
                margins = analysis['margins']
                widget_rect = widget.geometry()
                
                # Left margin guide
                if margins.left() > 0:
                    self.spacing_guides.append({
                        'type': 'margin_left',
                        'rect': QRect(widget_rect.left(), widget_rect.top(), 
                                     margins.left(), widget_rect.height()),
                        'label': f'Left Margin: {margins.left()}px',
                        'color': QColor(255, 100, 100, 80)  # Red for margins
                    })
                
                # Right margin guide
                if margins.right() > 0:
                    self.spacing_guides.append({
                        'type': 'margin_right',
                        'rect': QRect(widget_rect.right() - margins.right(), widget_rect.top(),
                                     margins.right(), widget_rect.height()),
                        'label': f'Right Margin: {margins.right()}px',
                        'color': QColor(255, 100, 100, 80)
                    })
                
                # Top margin guide
                if margins.top() > 0:
                    self.spacing_guides.append({
                        'type': 'margin_top',
                        'rect': QRect(widget_rect.left(), widget_rect.top(),
                                     widget_rect.width(), margins.top()),
                        'label': f'Top Margin: {margins.top()}px',
                        'color': QColor(255, 100, 100, 80)
                    })
                
                # Bottom margin guide
                if margins.bottom() > 0:
                    self.spacing_guides.append({
                        'type': 'margin_bottom',
                        'rect': QRect(widget_rect.left(), widget_rect.bottom() - margins.bottom(),
                                     widget_rect.width(), margins.bottom()),
                        'label': f'Bottom Margin: {margins.bottom()}px',
                        'color': QColor(255, 100, 100, 80)
                    })
            
            # Generate spacing guides for children
            if analysis.get('children'):
                for child_analysis in analysis['children']:
                    if child_analysis.get('geometry'):
                        child_rect = child_analysis['geometry']
                        
                        # Add spacing indicator between children
                        if len(self.spacing_guides) > 0:
                            last_guide = self.spacing_guides[-1]
                            if last_guide['type'].startswith('margin'):
                                # Calculate spacing between margin and child
                                spacing_value = abs(child_rect.left() - last_guide['rect'].right())
                                if spacing_value > 0:
                                    self.spacing_guides.append({
                                        'type': 'spacing',
                                        'rect': QRect(last_guide['rect'].right(), child_rect.top(),
                                                     spacing_value, child_rect.height()),
                                        'label': f'Spacing: {spacing_value}px',
                                        'color': QColor(100, 255, 100, 80)  # Green for spacing
                                    })
            
            logger.info(f"Generated {len(self.spacing_guides)} spacing guides")
            
        except Exception as e:
            logger.error(f"Failed to generate spacing guides: {e}")
    
    def generate_alignment_guides(self, widget: QWidget):
        """Generate alignment guides for a widget.
        
        Args:
            widget: Widget to generate guides for
        """
        try:
            self.alignment_guides.clear()
            
            # Get widget geometry
            widget_rect = widget.geometry()
            
            # Center line guides
            center_x = widget_rect.center().x()
            center_y = widget_rect.center().y()
            
            # Vertical center line
            self.alignment_guides.append({
                'type': 'center_vertical',
                'start': QPoint(center_x, widget_rect.top()),
                'end': QPoint(center_x, widget_rect.bottom()),
                'label': 'Center Line (Vertical)',
                'color': QColor(255, 255, 0, 120)  # Yellow for center lines
            })
            
            # Horizontal center line
            self.alignment_guides.append({
                'type': 'center_horizontal',
                'start': QPoint(widget_rect.left(), center_y),
                'end': QPoint(widget_rect.right(), center_y),
                'label': 'Center Line (Horizontal)',
                'color': QColor(255, 255, 0, 120)
            })
            
            # Quarter guides
            quarter_x = widget_rect.width() // 4
            quarter_y = widget_rect.height() // 4
            
            # Left quarter line
            self.alignment_guides.append({
                'type': 'quarter_left',
                'start': QPoint(widget_rect.left() + quarter_x, widget_rect.top()),
                'end': QPoint(widget_rect.left() + quarter_x, widget_rect.bottom()),
                'label': 'Left Quarter',
                'color': QColor(255, 255, 0, 60)  # Lighter yellow for quarter lines
            })
            
            # Right quarter line
            self.alignment_guides.append({
                'type': 'quarter_right',
                'start': QPoint(widget_rect.left() + 3 * quarter_x, widget_rect.top()),
                'end': QPoint(widget_rect.left() + 3 * quarter_x, widget_rect.bottom()),
                'label': 'Right Quarter',
                'color': QColor(255, 255, 0, 60)
            })
            
            logger.info(f"Generated {len(self.alignment_guides)} alignment guides")
            
        except Exception as e:
            logger.error(f"Failed to generate alignment guides: {e}")
    
    def generate_grid_guides(self, widget: QWidget, grid_size: int = 16):
        """Generate grid guides for a widget.
        
        Args:
            widget: Widget to generate guides for
            grid_size: Size of grid cells in pixels
        """
        try:
            # Grid guides would be implemented here
            # For now, we'll just log that it's not implemented
            logger.debug("Grid guides not yet implemented")
            
        except Exception as e:
            logger.error(f"Failed to generate grid guides: {e}")
    
    def _update_guides(self):
        """Update guides based on current responsive breakpoint."""
        try:
            if self.parent():
                # Regenerate guides if parent widget exists
                self.generate_spacing_guides(self.parent())
                self.generate_alignment_guides(self.parent())
                self.update()
                
        except Exception as e:
            logger.error(f"Failed to update guides: {e}")
    
    def paintEvent(self, event):
        """Paint the visual guides."""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            
            # Draw spacing guides
            if self.show_spacing_guides:
                self._draw_spacing_guides(painter)
            
            # Draw alignment guides
            if self.show_alignment_guides:
                self._draw_alignment_guides(painter)
            
            # Draw grid guides
            if self.show_grid_guides:
                self._draw_grid_guides(painter)
            
        except Exception as e:
            logger.error(f"Failed to paint guides: {e}")
    
    def _draw_spacing_guides(self, painter: QPainter):
        """Draw spacing guides.
        
        Args:
            painter: QPainter instance
        """
        try:
            for guide in self.spacing_guides:
                # Set pen and brush
                pen = QPen(guide['color'])
                pen.setWidth(2)
                painter.setPen(pen)
                
                # Draw guide rectangle
                painter.fillRect(guide['rect'], guide['color'])
                
                # Draw label
                self._draw_guide_label(painter, guide)
                
        except Exception as e:
            logger.error(f"Failed to draw spacing guides: {e}")
    
    def _draw_alignment_guides(self, painter: QPainter):
        """Draw alignment guides.
        
        Args:
            painter: QPainter instance
        """
        try:
            for guide in self.alignment_guides:
                # Set pen
                pen = QPen(guide['color'])
                pen.setWidth(2)
                pen.setStyle(Qt.PenStyle.DashLine)
                painter.setPen(pen)
                
                # Draw guide line
                painter.drawLine(guide['start'], guide['end'])
                
                # Draw label
                self._draw_guide_label(painter, guide)
                
        except Exception as e:
            logger.error(f"Failed to draw alignment guides: {e}")
    
    def _draw_grid_guides(self, painter: QPainter):
        """Draw grid guides.
        
        Args:
            painter: QPainter instance
        """
        try:
            # Grid guides would be drawn here
            pass
            
        except Exception as e:
            logger.error(f"Failed to draw grid guides: {e}")
    
    def _draw_guide_label(self, painter: QPainter, guide: Dict[str, Any]):
        """Draw a label for a guide.
        
        Args:
            painter: QPainter instance
            guide: Guide data dictionary
        """
        try:
            # Set font
            font = QFont()
            font.setPointSize(8)
            font.setBold(True)
            painter.setFont(font)
            
            # Set text color
            painter.setPen(QPen(self.text_color))
            
            # Get label position
            if guide['type'].startswith('margin'):
                # For margin guides, show label in the center
                rect = guide['rect']
                label_pos = rect.center()
            elif guide['type'].startswith('center'):
                # For center guides, show label near the line
                start = guide['start']
                label_pos = QPoint(start.x() + 10, start.y() + 20)
            else:
                # For other guides, use a default position
                rect = guide.get('rect', QRect())
                if rect.isValid():
                    label_pos = rect.center()
                else:
                    start = guide.get('start', QPoint())
                    label_pos = QPoint(start.x() + 10, start.y() + 20)
            
            # Draw label
            label = guide.get('label', 'Unknown')
            painter.drawText(label_pos, label)
            
        except Exception as e:
            logger.error(f"Failed to draw guide label: {e}")
    
    def mousePressEvent(self, event):
        """Handle mouse press events for guide interaction.
        
        Args:
            event: Mouse press event
        """
        try:
            pos = event.pos()
            
            # Check if clicked on a guide
            for guide in self.spacing_guides + self.alignment_guides:
                if 'rect' in guide and guide['rect'].contains(pos):
                    self.guide_clicked.emit(guide['type'], pos.x(), pos.y())
                    break
                elif 'start' in guide and 'end' in guide:
                    # For line guides, check if click is near the line
                    if self._is_point_near_line(pos, guide['start'], guide['end'], 5):
                        self.guide_clicked.emit(guide['type'], pos.x(), pos.y())
                        break
            
            super().mousePressEvent(event)
            
        except Exception as e:
            logger.error(f"Failed to handle mouse press: {e}")
    
    def _is_point_near_line(self, point: QPoint, start: QPoint, end: QPoint, tolerance: int) -> bool:
        """Check if a point is near a line within tolerance.
        
        Args:
            point: Point to check
            start: Start of line
            end: End of line
            tolerance: Distance tolerance in pixels
            
        Returns:
            True if point is near line
        """
        try:
            # Calculate distance from point to line
            # This is a simplified calculation - in a real implementation,
            # you'd use proper point-to-line distance formula
            
            # For now, just check if point is within tolerance of either endpoint
            dist_to_start = ((point.x() - start.x()) ** 2 + (point.y() - start.y()) ** 2) ** 0.5
            dist_to_end = ((point.x() - end.x()) ** 2 + (point.y() - end.y()) ** 2) ** 0.5
            
            return dist_to_start <= tolerance or dist_to_end <= tolerance
            
        except Exception as e:
            logger.error(f"Failed to check point near line: {e}")
            return False


# Global visual guide instance
visual_alignment_guide = VisualAlignmentGuide()
