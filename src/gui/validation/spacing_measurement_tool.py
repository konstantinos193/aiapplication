"""
Spacing measurement tool for real-time UI spacing analysis.

This module provides tools to:
- Measure spacing between UI elements
- Calculate actual vs expected spacing
- Generate spacing reports
- Monitor spacing changes
"""

from typing import Dict, List, Optional, Tuple, Any
from PyQt6.QtWidgets import QWidget, QApplication, QToolTip
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QCursor
import logging
import math

from ..responsive import responsive_spacing_manager, Breakpoint
from ..design_system.spacing_system import spacing, SpacingUnit

logger = logging.getLogger(__name__)


class SpacingMeasurementTool:
    """Tool for measuring spacing between UI elements."""
    
    def __init__(self):
        self.measurements: Dict[str, Dict[str, Any]] = {}
        self.active_measurements: List[Dict[str, Any]] = []
        self.measurement_history: List[Dict[str, Any]] = []
        
        # Measurement settings
        self.measurement_tolerance = 2  # pixels
        self.show_measurement_lines = True
        self.show_measurement_labels = True
        
        # Visual settings
        self.measurement_color = QColor(0, 255, 255, 150)  # Cyan
        self.label_color = QColor(255, 255, 255, 255)  # White
        self.error_color = QColor(255, 0, 0, 150)  # Red
        
        logger.info("SpacingMeasurementTool initialized")
    
    def measure_widget_spacing(self, widget1: QWidget, widget2: QWidget, 
                             measurement_name: str = None) -> Dict[str, Any]:
        """Measure spacing between two widgets.
        
        Args:
            widget1: First widget
            widget2: Second widget
            measurement_name: Name for this measurement
            
        Returns:
            Measurement results dictionary
        """
        try:
            if not measurement_name:
                measurement_name = f"{widget1.objectName() or type(widget1).__name__}_to_{widget2.objectName() or type(widget2).__name__}"
            
            # Get widget geometries
            rect1 = widget1.geometry()
            rect2 = widget2.geometry()
            
            # Calculate distances
            distances = self._calculate_widget_distances(rect1, rect2)
            
            # Get expected spacing from design system
            expected_spacing = self._get_expected_spacing(widget1, widget2)
            
            # Calculate measurement results
            measurement = {
                'name': measurement_name,
                'widget1': {
                    'name': widget1.objectName() or type(widget1).__name__,
                    'geometry': rect1,
                    'center': rect1.center()
                },
                'widget2': {
                    'name': widget2.objectName() or type(widget2).__name__,
                    'geometry': rect2,
                    'center': rect2.center()
                },
                'distances': distances,
                'expected_spacing': expected_spacing,
                'spacing_analysis': self._analyze_spacing(distances, expected_spacing),
                'timestamp': QTimer().remainingTime()  # Simple timestamp
            }
            
            # Store measurement
            self.measurements[measurement_name] = measurement
            self.measurement_history.append(measurement)
            
            # Keep only last 100 measurements
            if len(self.measurement_history) > 100:
                self.measurement_history.pop(0)
            
            logger.info(f"Measured spacing: {measurement_name} - {distances['horizontal']}px horizontal, {distances['vertical']}px vertical")
            
            return measurement
            
        except Exception as e:
            logger.error(f"Failed to measure spacing: {e}")
            return {
                'name': measurement_name or 'Unknown',
                'error': str(e)
            }
    
    def _calculate_widget_distances(self, rect1: QRect, rect2: QRect) -> Dict[str, float]:
        """Calculate distances between two rectangles.
        
        Args:
            rect1: First rectangle
            rect2: Second rectangle
            
        Returns:
            Dictionary with horizontal and vertical distances
        """
        try:
            # Calculate horizontal distance
            if rect1.right() < rect2.left():
                # rect1 is to the left of rect2
                horizontal = rect2.left() - rect1.right()
            elif rect2.right() < rect1.left():
                # rect2 is to the left of rect1
                horizontal = rect1.left() - rect2.right()
            else:
                # Rectangles overlap horizontally
                horizontal = 0
            
            # Calculate vertical distance
            if rect1.bottom() < rect2.top():
                # rect1 is above rect2
                vertical = rect2.top() - rect1.bottom()
            elif rect2.bottom() < rect1.top():
                # rect2 is above rect1
                vertical = rect1.top() - rect2.bottom()
            else:
                # Rectangles overlap vertically
                vertical = 0
            
            # Calculate center-to-center distance
            center1 = rect1.center()
            center2 = rect2.center()
            center_distance = math.sqrt((center2.x() - center1.x()) ** 2 + (center2.y() - center1.y()) ** 2)
            
            return {
                'horizontal': horizontal,
                'vertical': vertical,
                'center_to_center': center_distance,
                'overlap': horizontal == 0 and vertical == 0
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate distances: {e}")
            return {
                'horizontal': 0,
                'vertical': 0,
                'center_to_center': 0,
                'overlap': False
            }
    
    def _get_expected_spacing(self, widget1: QWidget, widget2: QWidget) -> Dict[str, Any]:
        """Get expected spacing between widgets based on design system.
        
        Args:
            widget1: First widget
            widget2: Second widget
            
        Returns:
            Expected spacing values
        """
        try:
            expected = {
                'horizontal': spacing.md,  # 16px default
                'vertical': spacing.md,    # 16px default
                'source': 'design_system_default'
            }
            
            # Check if widgets have responsive spacing
            if hasattr(widget1, 'get_responsive_spacing'):
                try:
                    responsive_spacing = widget1.get_responsive_spacing(spacing.md)
                    expected['horizontal'] = responsive_spacing
                    expected['vertical'] = responsive_spacing
                    expected['source'] = 'responsive_spacing'
                except Exception as e:
                    logger.debug(f"Failed to get responsive spacing: {e}")
            
            # Check if widgets are in the same layout
            if hasattr(widget1, 'parent') and widget1.parent():
                parent = widget1.parent()
                if hasattr(parent, 'layout') and parent.layout():
                    layout = parent.layout()
                    layout_spacing = layout.spacing()
                    if layout_spacing > 0:
                        expected['horizontal'] = layout_spacing
                        expected['vertical'] = layout_spacing
                        expected['source'] = 'layout_spacing'
            
            return expected
            
        except Exception as e:
            logger.error(f"Failed to get expected spacing: {e}")
            return {
                'horizontal': spacing.md,
                'vertical': spacing.md,
                'source': 'fallback'
            }
    
    def _analyze_spacing(self, distances: Dict[str, float], expected: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze spacing against expected values.
        
        Args:
            distances: Actual distances
            expected: Expected spacing values
            
        Returns:
            Spacing analysis results
        """
        try:
            analysis = {
                'horizontal_status': 'unknown',
                'vertical_status': 'unknown',
                'overall_status': 'unknown',
                'issues': [],
                'recommendations': []
            }
            
            # Analyze horizontal spacing
            horizontal_diff = abs(distances['horizontal'] - expected['horizontal'])
            if horizontal_diff <= self.measurement_tolerance:
                analysis['horizontal_status'] = 'correct'
            elif distances['horizontal'] < expected['horizontal']:
                analysis['horizontal_status'] = 'too_close'
                analysis['issues'].append(f"Horizontal spacing too close: {distances['horizontal']}px (expected {expected['horizontal']}px)")
            else:
                analysis['horizontal_status'] = 'too_far'
                analysis['issues'].append(f"Horizontal spacing too far: {distances['horizontal']}px (expected {expected['horizontal']}px)")
            
            # Analyze vertical spacing
            vertical_diff = abs(distances['vertical'] - expected['vertical'])
            if vertical_diff <= self.measurement_tolerance:
                analysis['vertical_status'] = 'correct'
            elif distances['vertical'] < expected['vertical']:
                analysis['vertical_status'] = 'too_close'
                analysis['issues'].append(f"Vertical spacing too close: {distances['vertical']}px (expected {expected['vertical']}px)")
            else:
                analysis['vertical_status'] = 'too_far'
                analysis['issues'].append(f"Vertical spacing too far: {distances['vertical']}px (expected {expected['vertical']}px)")
            
            # Determine overall status
            if analysis['horizontal_status'] == 'correct' and analysis['vertical_status'] == 'correct':
                analysis['overall_status'] = 'correct'
            elif analysis['horizontal_status'] == 'correct' or analysis['vertical_status'] == 'correct':
                analysis['overall_status'] = 'partially_correct'
            else:
                analysis['overall_status'] = 'incorrect'
            
            # Generate recommendations
            if analysis['overall_status'] != 'correct':
                if analysis['horizontal_status'] != 'correct':
                    analysis['recommendations'].append(f"Adjust horizontal spacing to {expected['horizontal']}px")
                if analysis['vertical_status'] != 'correct':
                    analysis['recommendations'].append(f"Adjust vertical spacing to {expected['vertical']}px")
                
                analysis['recommendations'].append("Check layout margins and spacing settings")
                analysis['recommendations'].append("Verify responsive spacing implementation")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze spacing: {e}")
            return {
                'horizontal_status': 'error',
                'vertical_status': 'error',
                'overall_status': 'error',
                'issues': [f"Analysis error: {e}"],
                'recommendations': ["Check measurement tool configuration"]
            }
    
    def measure_all_widgets_in_layout(self, layout_widget: QWidget) -> List[Dict[str, Any]]:
        """Measure spacing between all widgets in a layout.
        
        Args:
            layout_widget: Widget containing the layout
            
        Returns:
            List of measurements
        """
        try:
            measurements = []
            
            if not hasattr(layout_widget, 'layout') or not layout_widget.layout():
                logger.warning(f"Widget {layout_widget.objectName()} has no layout")
                return measurements
            
            layout = layout_widget.layout()
            widgets = []
            
            # Collect all widgets in the layout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget():
                    widgets.append(item.widget())
            
            # Measure spacing between adjacent widgets
            for i in range(len(widgets) - 1):
                widget1 = widgets[i]
                widget2 = widgets[i + 1]
                
                measurement = self.measure_widget_spacing(
                    widget1, widget2, 
                    f"layout_{i}_to_{i+1}"
                )
                
                if 'error' not in measurement:
                    measurements.append(measurement)
            
            logger.info(f"Measured spacing for {len(widgets)} widgets in layout, generated {len(measurements)} measurements")
            return measurements
            
        except Exception as e:
            logger.error(f"Failed to measure layout spacing: {e}")
            return []
    
    def get_measurement_summary(self) -> Dict[str, Any]:
        """Get a summary of all measurements.
        
        Returns:
            Measurement summary dictionary
        """
        try:
            if not self.measurements:
                return {
                    'total_measurements': 0,
                    'status': 'no_measurements'
                }
            
            total = len(self.measurements)
            correct = 0
            partially_correct = 0
            incorrect = 0
            errors = 0
            
            for measurement in self.measurements.values():
                if 'error' in measurement:
                    errors += 1
                else:
                    status = measurement.get('spacing_analysis', {}).get('overall_status', 'unknown')
                    if status == 'correct':
                        correct += 1
                    elif status == 'partially_correct':
                        partially_correct += 1
                    else:
                        incorrect += 1
            
            summary = {
                'total_measurements': total,
                'correct': correct,
                'partially_correct': partially_correct,
                'incorrect': incorrect,
                'errors': errors,
                'accuracy_percentage': (correct / total * 100) if total > 0 else 0,
                'status': 'measured'
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate measurement summary: {e}")
            return {
                'total_measurements': 0,
                'status': 'error',
                'error': str(e)
            }
    
    def export_measurements(self, format_type: str = 'json') -> str:
        """Export measurements to various formats.
        
        Args:
            format_type: Export format ('json', 'csv', 'text')
            
        Returns:
            Exported data as string
        """
        try:
            if format_type == 'json':
                import json
                return json.dumps(self.measurements, indent=2, default=str)
            
            elif format_type == 'csv':
                csv_lines = ['Name,Widget1,Widget2,Horizontal,Vertical,Expected,Status,Issues']
                
                for measurement in self.measurements.values():
                    if 'error' not in measurement:
                        name = measurement['name']
                        widget1 = measurement['widget1']['name']
                        widget2 = measurement['widget2']['name']
                        horizontal = measurement['distances']['horizontal']
                        vertical = measurement['distances']['vertical']
                        expected = measurement['expected_spacing']['horizontal']
                        status = measurement['spacing_analysis']['overall_status']
                        issues = '; '.join(measurement['spacing_analysis']['issues'])
                        
                        csv_lines.append(f'{name},{widget1},{widget2},{horizontal},{vertical},{expected},{status},"{issues}"')
                
                return '\n'.join(csv_lines)
            
            elif format_type == 'text':
                text_lines = []
                text_lines.append("SPACING MEASUREMENT REPORT")
                text_lines.append("=" * 50)
                text_lines.append("")
                
                for measurement in self.measurements.values():
                    if 'error' not in measurement:
                        text_lines.append(f"📏 {measurement['name']}")
                        text_lines.append(f"   Widgets: {measurement['widget1']['name']} → {measurement['widget2']['name']}")
                        text_lines.append(f"   Horizontal: {measurement['distances']['horizontal']}px")
                        text_lines.append(f"   Vertical: {measurement['distances']['vertical']}px")
                        text_lines.append(f"   Expected: {measurement['expected_spacing']['horizontal']}px")
                        text_lines.append(f"   Status: {measurement['spacing_analysis']['overall_status']}")
                        
                        if measurement['spacing_analysis']['issues']:
                            text_lines.append("   Issues:")
                            for issue in measurement['spacing_analysis']['issues']:
                                text_lines.append(f"     • {issue}")
                        
                        text_lines.append("")
                
                return '\n'.join(text_lines)
            
            else:
                raise ValueError(f"Unsupported format: {format_type}")
                
        except Exception as e:
            logger.error(f"Failed to export measurements: {e}")
            return f"Export failed: {e}"
    
    def clear_measurements(self):
        """Clear all stored measurements."""
        try:
            self.measurements.clear()
            self.measurement_history.clear()
            logger.info("All measurements cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear measurements: {e}")
    
    def get_measurement_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific measurement by name.
        
        Args:
            name: Measurement name
            
        Returns:
            Measurement dictionary or None if not found
        """
        return self.measurements.get(name)
    
    def get_measurements_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get all measurements with a specific status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of matching measurements
        """
        try:
            matching = []
            
            for measurement in self.measurements.values():
                if 'error' not in measurement:
                    measurement_status = measurement.get('spacing_analysis', {}).get('overall_status', 'unknown')
                    if measurement_status == status:
                        matching.append(measurement)
            
            return matching
            
        except Exception as e:
            logger.error(f"Failed to filter measurements by status: {e}")
            return []


# Global measurement tool instance
spacing_measurement_tool = SpacingMeasurementTool()
