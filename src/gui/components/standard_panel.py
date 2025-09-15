"""
Standard Panel Component for Nexlify GUI

This component provides a standardized panel with consistent
spacing, typography, and alignment following the design system.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import Union

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.typography_system import typography, FontSize, FontWeight
from ..design_system.alignment_system import alignment, HorizontalAlignment
from ..responsive import responsive_spacing_manager
from ..animations import spacing_animation_manager, EasingType


class StandardPanel(QWidget):
    """Standard panel component with consistent design system styling."""
    
    def __init__(self, title: str = "", parent=None, 
                 variant: str = "default", collapsible: bool = False):
        """Initialize the standard panel.
        
        Args:
            title: Panel title
            parent: Parent widget
            variant: Visual variant (default, primary, secondary, accent)
            collapsible: Whether the panel can be collapsed
        """
        super().__init__(parent)
        
        # Store configuration
        self.title = title
        self.variant = variant
        self.collapsible = collapsible
        self.collapsed = False
        
        # Create layout
        self._create_layout()
        self._apply_styling()
        self._setup_connections()
    
    def _create_layout(self):
        """Create the panel layout."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            spacing.md,  # 16px outer margin
            spacing.md,  # 16px outer margin
            spacing.md,  # 16px outer margin
            spacing.md   # 16px outer margin
        )
        self.main_layout.setSpacing(0)
        
        # Header layout
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(spacing.sm)  # 8px spacing between header elements
        
        # Title label
        if self.title:
            self.title_label = QLabel(self.title)
            self.title_label.setObjectName("panel-title")
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.header_layout.addWidget(self.title_label)
        
        # Add stretch to push any header controls to the right
        self.header_layout.addStretch()
        
        # Add header to main layout
        self.main_layout.addLayout(self.header_layout)
        
        # Content area
        self.content_widget = QWidget()
        self.content_widget.setObjectName("panel-content")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(
            spacing.sm,  # 12px inner padding
            spacing.sm,  # 12px inner padding
            spacing.sm,  # 12px inner padding
            spacing.sm   # 12px inner padding
        )
        self.content_layout.setSpacing(spacing.sm)  # 8px spacing between content items
        
        self.main_layout.addWidget(self.content_widget)
    
    def _apply_styling(self):
        """Apply design system styling."""
        # Get spacing values
        panel_margin = spacing.md  # 16px outer margin
        panel_padding = spacing.sm  # 12px inner padding
        header_spacing = spacing.sm  # 16px from content
        border_radius = 4  # 4px border radius
        
        # Get typography values
        title_font_size = typography.lg  # 18px font size
        title_font_weight = typography.semi_bold  # Semi-bold font weight
        
        # Base styling
        base_style = f"""
            QWidget#panel-content {{
                background-color: #1e1e1e;
                border: 1px solid #555555;
                border-radius: {border_radius}px;
                padding: {panel_padding}px;
            }}
            
            QLabel#panel-title {{
                color: #ffffff;
                font-size: {title_font_size}px;
                font-weight: {title_font_weight};
                padding: {spacing.xs}px 0px;
            }}
        """
        
        # Variant-specific styling
        if self.variant == "primary":
            base_style += f"""
                QWidget#panel-content {{
                    border: 1px solid #0078d4;
                    background-color: #0f1419;
                }}
                
                QLabel#panel-title {{
                    color: #0078d4;
                }}
            """
        elif self.variant == "secondary":
            base_style += f"""
                QWidget#panel-content {{
                    border: 1px solid #6c757d;
                    background-color: #1a1a1a;
                }}
                
                QLabel#panel-title {{
                    color: #6c757d;
                }}
            """
        elif self.variant == "accent":
            base_style += f"""
                QWidget#panel-content {{
                    border: 1px solid #ff6b35;
                    background-color: #1a0f0a;
                }}
                
                QLabel#panel-title {{
                    color: #ff6b35;
                }}
            """
        
        self.setStyleSheet(base_style)
    
    def _setup_connections(self):
        """Setup signal connections."""
        pass  # No signals needed for basic panel
    
    def add_widget(self, widget: QWidget):
        """Add a widget to the panel content area.
        
        Args:
            widget: Widget to add to the panel
        """
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add a layout to the panel content area.
        
        Args:
            layout: Layout to add to the panel
        """
        self.content_layout.addLayout(layout)
    
    def add_stretch(self):
        """Add a stretch to the panel content area."""
        self.content_layout.addStretch()
    
    def set_title(self, title: str):
        """Set the panel title.
        
        Args:
            title: New panel title
        """
        self.title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)
    
    def set_variant(self, variant: str):
        """Set the panel visual variant.
        
        Args:
            variant: Visual variant (default, primary, secondary, accent)
        """
        self.variant = variant
        self._apply_styling()
    
    def get_content_layout(self):
        """Get the content layout for direct manipulation.
        
        Returns:
            QVBoxLayout: The content layout
        """
        return self.content_layout
    
    def clear_content(self):
        """Clear all content from the panel."""
        # Remove all widgets from content layout
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
    
    def set_content_margins(self, left: int, top: int, right: int, bottom: int):
        """Set custom content margins.
        
        Args:
            left: Left margin in pixels
            top: Top margin in pixels
            right: Right margin in pixels
            bottom: Bottom margin in pixels
        """
        self.content_layout.setContentsMargins(left, top, right, bottom)
    
    def set_content_spacing(self, spacing_value: int):
        """Set custom content spacing.
        
        Args:
            spacing_value: Spacing between content items in pixels
        """
        self.content_layout.setSpacing(spacing_value)
    
    def get_responsive_spacing(self, base_spacing: Union[int, SpacingUnit], 
                              touch_friendly: bool = False) -> int:
        """Get responsive spacing value for current breakpoint.
        
        Args:
            base_spacing: Base spacing value
            touch_friendly: Whether to apply touch-friendly adjustments
            
        Returns:
            Responsive spacing value
        """
        return responsive_spacing_manager.get_responsive_spacing(base_spacing, touch_friendly)
    
    def animate_spacing_change(self, start_spacing: int, end_spacing: int, 
                             duration: int = 300, easing: EasingType = EasingType.EASE_IN_OUT):
        """Animate spacing change for the panel.
        
        Args:
            start_spacing: Starting spacing value
            end_spacing: Ending spacing value
            duration: Animation duration in milliseconds
            easing: Easing curve type
        """
        return spacing_animation_manager.animate_spacing_change(
            self, start_spacing, end_spacing, duration, easing
        )
    
    def get_current_breakpoint(self) -> str:
        """Get current breakpoint name.
        
        Returns:
            Current breakpoint name
        """
        return responsive_spacing_manager.get_current_breakpoint().value
