"""
Spacing validation system for ensuring consistent spacing across the UI.

This module provides tools to:
- Validate spacing consistency across panels
- Measure actual spacing values
- Generate spacing reports
- Create visual alignment guides
"""

from typing import Dict, List, Tuple, Optional, Any
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import logging

from ..responsive import responsive_spacing_manager, Breakpoint
from ..design_system.spacing_system import spacing, SpacingUnit

logger = logging.getLogger(__name__)


class SpacingValidator:
    """Validates spacing consistency across UI components."""
    
    def __init__(self):
        self.validation_results: Dict[str, Dict[str, Any]] = {}
        self.spacing_measurements: Dict[str, Dict[str, int]] = {}
        self.alignment_issues: List[Dict[str, Any]] = []
        
    def validate_panel_spacing(self, panel: QWidget, panel_name: str) -> Dict[str, Any]:
        """Validate spacing for a specific panel.
        
        Args:
            panel: The panel widget to validate
            panel_name: Name of the panel for reporting
            
        Returns:
            Validation results dictionary
        """
        try:
            results = {
                'panel_name': panel_name,
                'total_issues': 0,
                'spacing_issues': [],
                'alignment_issues': [],
                'responsive_issues': [],
                'overall_score': 100
            }
            
            # Validate panel margins
            margin_issues = self._validate_panel_margins(panel, panel_name)
            results['spacing_issues'].extend(margin_issues)
            
            # Validate internal spacing
            internal_issues = self._validate_internal_spacing(panel, panel_name)
            results['spacing_issues'].extend(internal_issues)
            
            # Validate responsive spacing
            responsive_issues = self._validate_responsive_spacing(panel, panel_name)
            results['responsive_issues'].extend(responsive_issues)
            
            # Calculate overall score
            total_issues = len(results['spacing_issues']) + len(results['alignment_issues']) + len(results['responsive_issues'])
            results['total_issues'] = total_issues
            results['overall_score'] = max(0, 100 - (total_issues * 10))
            
            self.validation_results[panel_name] = results
            logger.info(f"Validated {panel_name}: Score {results['overall_score']}/100, {total_issues} issues")
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to validate panel {panel_name}: {e}")
            return {
                'panel_name': panel_name,
                'total_issues': 1,
                'error': str(e),
                'overall_score': 0
            }
    
    def _validate_panel_margins(self, panel: QWidget, panel_name: str) -> List[Dict[str, Any]]:
        """Validate panel margin consistency.
        
        Args:
            panel: Panel widget to validate
            panel_name: Name of the panel
            
        Returns:
            List of margin validation issues
        """
        issues = []
        
        try:
            # Get expected margins based on design system
            expected_margin = spacing.md  # 16px
            expected_padding = spacing.sm  # 12px
            
            # Get actual layout margins
            layout = panel.layout()
            if layout:
                margins = layout.contentsMargins()
                actual_margin = margins.left()  # Assuming symmetric margins
                
                # Check if margins match expected values
                if abs(actual_margin - expected_margin) > 2:  # Allow 2px tolerance
                    issues.append({
                        'type': 'margin_mismatch',
                        'expected': expected_margin,
                        'actual': actual_margin,
                        'tolerance': 2,
                        'severity': 'medium'
                    })
                
                # Check if margins are consistent (left = right = top = bottom)
                if not (margins.left() == margins.right() == margins.top() == margins.bottom()):
                    issues.append({
                        'type': 'inconsistent_margins',
                        'left': margins.left(),
                        'right': margins.right(),
                        'top': margins.top(),
                        'bottom': margins.bottom(),
                        'severity': 'high'
                    })
            
        except Exception as e:
            logger.error(f"Failed to validate margins for {panel_name}: {e}")
            issues.append({
                'type': 'validation_error',
                'error': str(e),
                'severity': 'critical'
            })
        
        return issues
    
    def _validate_internal_spacing(self, panel: QWidget, panel_name: str) -> List[Dict[str, Any]]:
        """Validate internal spacing between elements.
        
        Args:
            panel: Panel widget to validate
            panel_name: Name of the panel
            
        Returns:
            List of internal spacing validation issues
        """
        issues = []
        
        try:
            layout = panel.layout()
            if layout:
                # Check layout spacing
                actual_spacing = layout.spacing()
                expected_spacing = spacing.sm  # 12px
                
                if abs(actual_spacing - expected_spacing) > 2:
                    issues.append({
                        'type': 'spacing_mismatch',
                        'expected': expected_spacing,
                        'actual': actual_spacing,
                        'tolerance': 2,
                        'severity': 'medium'
                    })
                
                # Check child widget spacing (basic check)
                child_count = layout.count()
                if child_count > 1:
                    # This is a simplified check - in a real implementation,
                    # you'd traverse the widget hierarchy more thoroughly
                    pass
                    
        except Exception as e:
            logger.error(f"Failed to validate internal spacing for {panel_name}: {e}")
            issues.append({
                'type': 'validation_error',
                'error': str(e),
                'severity': 'critical'
            })
        
        return issues
    
    def _validate_responsive_spacing(self, panel: QWidget, panel_name: str) -> List[Dict[str, Any]]:
        """Validate responsive spacing implementation.
        
        Args:
            panel: Panel widget to validate
            panel_name: Name of the panel
            
        Returns:
            List of responsive spacing validation issues
        """
        issues = []
        
        try:
            # Check if panel has responsive spacing methods
            if not hasattr(panel, 'get_responsive_spacing'):
                issues.append({
                    'type': 'missing_responsive_methods',
                    'missing_methods': ['get_responsive_spacing'],
                    'severity': 'high'
                })
            
            if not hasattr(panel, 'get_current_breakpoint'):
                issues.append({
                    'type': 'missing_responsive_methods',
                    'missing_methods': ['get_current_breakpoint'],
                    'severity': 'high'
                })
            
            # Check if panel is connected to responsive spacing manager
            # This would require more sophisticated reflection in a real implementation
            
        except Exception as e:
            logger.error(f"Failed to validate responsive spacing for {panel_name}: {e}")
            issues.append({
                'type': 'validation_error',
                'error': str(e),
                'severity': 'critical'
            })
        
        return issues
    
    def validate_all_panels(self, main_window) -> Dict[str, Any]:
        """Validate spacing across all panels in the main window.
        
        Args:
            main_window: Main window containing all panels
            
        Returns:
            Overall validation results
        """
        try:
            overall_results = {
                'total_panels': 0,
                'validated_panels': 0,
                'overall_score': 0,
                'total_issues': 0,
                'panel_results': {},
                'recommendations': []
            }
            
            # Find all panels in the main window
            panels = self._find_all_panels(main_window)
            overall_results['total_panels'] = len(panels)
            
            total_score = 0
            total_issues = 0
            
            for panel_name, panel in panels.items():
                if panel:
                    result = self.validate_panel_spacing(panel, panel_name)
                    overall_results['panel_results'][panel_name] = result
                    overall_results['validated_panels'] += 1
                    
                    total_score += result['overall_score']
                    total_issues += result['total_issues']
            
            # Calculate overall metrics
            if overall_results['validated_panels'] > 0:
                overall_results['overall_score'] = total_score // overall_results['validated_panels']
                overall_results['total_issues'] = total_issues
            
            # Generate recommendations
            overall_results['recommendations'] = self._generate_recommendations(overall_results)
            
            self.validation_results = overall_results
            logger.info(f"Validation complete: {overall_results['validated_panels']} panels, "
                       f"Score: {overall_results['overall_score']}/100, "
                       f"Issues: {overall_results['total_issues']}")
            
            return overall_results
            
        except Exception as e:
            logger.error(f"Failed to validate all panels: {e}")
            return {
                'error': str(e),
                'overall_score': 0
            }
    
    def _find_all_panels(self, main_window) -> Dict[str, QWidget]:
        """Find all panel widgets in the main window.
        
        Args:
            main_window: Main window to search
            
        Returns:
            Dictionary of panel names to panel widgets
        """
        panels = {}
        
        try:
            # Common panel names to look for
            panel_attributes = [
                'scene_panel', 'inspector_panel', 'properties_panel',
                'viewport_panel', 'assets_panel', 'console_panel',
                'ai_chat_panel'
            ]
            
            for attr_name in panel_attributes:
                if hasattr(main_window, attr_name):
                    panel = getattr(main_window, attr_name)
                    if panel and isinstance(panel, QWidget):
                        panels[attr_name] = panel
            
            # Also look for panels in layout children
            if hasattr(main_window, 'centralWidget'):
                central = main_window.centralWidget()
                if central and hasattr(central, 'layout'):
                    self._find_panels_in_layout(central.layout(), panels)
                    
        except Exception as e:
            logger.error(f"Failed to find panels: {e}")
        
        return panels
    
    def _find_panels_in_layout(self, layout, panels: Dict[str, QWidget]):
        """Recursively find panels in a layout hierarchy.
        
        Args:
            layout: Layout to search
            panels: Dictionary to populate with found panels
        """
        if not layout:
            return
        
        try:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget():
                    widget = item.widget()
                    widget_name = widget.objectName()
                    
                    # Check if this looks like a panel
                    if (widget_name and 'panel' in widget_name.lower()) or \
                       (hasattr(widget, 'get_responsive_spacing')):
                        panels[widget_name or f"panel_{len(panels)}"] = widget
                
                # Recursively check sub-layouts
                if item.layout():
                    self._find_panels_in_layout(item.layout(), panels)
                    
        except Exception as e:
            logger.error(f"Failed to search layout: {e}")
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results.
        
        Args:
            results: Validation results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        try:
            if results['overall_score'] < 80:
                recommendations.append("Overall spacing consistency needs improvement. Focus on standardizing margins and padding.")
            
            if results['total_issues'] > 5:
                recommendations.append("High number of spacing issues detected. Consider systematic review of design system implementation.")
            
            # Analyze specific panel issues
            for panel_name, panel_result in results.get('panel_results', {}).items():
                if panel_result['overall_score'] < 70:
                    recommendations.append(f"Panel '{panel_name}' has significant spacing issues. Priority review recommended.")
                
                # Check for specific issue types
                spacing_issues = panel_result.get('spacing_issues', [])
                margin_issues = [i for i in spacing_issues if i['type'] == 'margin_mismatch']
                if margin_issues:
                    recommendations.append(f"Panel '{panel_name}' has margin inconsistencies. Verify design system compliance.")
                
                responsive_issues = panel_result.get('responsive_issues', [])
                missing_methods = [i for i in responsive_issues if i['type'] == 'missing_responsive_methods']
                if missing_methods:
                    recommendations.append(f"Panel '{panel_name}' missing responsive spacing methods. Implement responsive spacing integration.")
            
            if not recommendations:
                recommendations.append("Spacing system is working well! Continue monitoring for consistency.")
                
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            recommendations.append("Error generating recommendations. Check logs for details.")
        
        return recommendations
    
    def generate_report(self) -> str:
        """Generate a human-readable validation report.
        
        Returns:
            Formatted report string
        """
        try:
            if not self.validation_results:
                return "No validation results available. Run validation first."
            
            report = []
            report.append("=" * 60)
            report.append("SPACING VALIDATION REPORT")
            report.append("=" * 60)
            report.append("")
            
            # Overall summary
            overall = self.validation_results
            report.append(f"OVERALL SCORE: {overall.get('overall_score', 0)}/100")
            report.append(f"PANELS VALIDATED: {overall.get('validated_panels', 0)}/{overall.get('total_panels', 0)}")
            report.append(f"TOTAL ISSUES: {overall.get('total_issues', 0)}")
            report.append("")
            
            # Panel details
            report.append("PANEL DETAILS:")
            report.append("-" * 40)
            
            for panel_name, panel_result in overall.get('panel_results', {}).items():
                report.append(f"📋 {panel_name.upper()}")
                report.append(f"   Score: {panel_result.get('overall_score', 0)}/100")
                report.append(f"   Issues: {panel_result.get('total_issues', 0)}")
                
                # Show specific issues
                spacing_issues = panel_result.get('spacing_issues', [])
                if spacing_issues:
                    report.append("   Spacing Issues:")
                    for issue in spacing_issues[:3]:  # Show first 3 issues
                        report.append(f"     • {issue.get('type', 'Unknown')}: {issue.get('severity', 'Unknown')}")
                
                report.append("")
            
            # Recommendations
            recommendations = overall.get('recommendations', [])
            if recommendations:
                report.append("RECOMMENDATIONS:")
                report.append("-" * 40)
                for rec in recommendations:
                    report.append(f"💡 {rec}")
                report.append("")
            
            report.append("=" * 60)
            report.append("Report generated by SpacingValidator")
            report.append("=" * 60)
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return f"Error generating report: {e}"


# Global validator instance
spacing_validator = SpacingValidator()
