"""
Standard Button Component for Nexlify GUI

This component provides a standardized button with consistent
spacing, typography, and alignment following the design system.
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.typography_system import typography, FontSize, FontWeight
from ..design_system.alignment_system import alignment, HorizontalAlignment


class StandardButton(QPushButton):
    """Standard button component with consistent design system styling."""
    
    # Signals
    clicked_with_data = pyqtSignal(object)  # Emits custom data when clicked
    
    def __init__(self, text: str = "", parent=None, 
                 size: str = "medium", variant: str = "primary"):
        """Initialize the standard button.
        
        Args:
            text: Button text
            parent: Parent widget
            size: Button size ("small", "medium", "large")
            variant: Button variant ("primary", "secondary", "danger", "success")
        """
        super().__init__(text, parent)
        
        self.size = size
        self.variant = variant
        
        self._setup_styling()
        self._setup_behavior()
        
    def _setup_styling(self):
        """Setup button styling using design system."""
        # Get spacing values
        button_padding_h = spacing.button_spacing
        button_padding_v = spacing.sm  # 8px vertical padding
        
        # Get typography values
        if self.size == "small":
            font_size = typography.sm
            button_height = spacing.button_height - 8  # 24px
        elif self.size == "large":
            font_size = typography.lg
            button_height = spacing.button_height + 8  # 40px
        else:  # medium
            font_size = typography.md
            button_height = spacing.button_height  # 32px
        
        # Set font
        font = QFont()
        font.setPointSize(font_size)
        font.setWeight(typography.medium)
        self.setFont(font)
        
        # Set size
        self.setMinimumHeight(button_height)
        self.setMaximumHeight(button_height)
        
        # Set padding
        self.setContentsMargins(button_padding_h, button_padding_v, 
                               button_padding_h, button_padding_v)
        
        # Apply variant-specific styling
        self._apply_variant_styling()
        
    def _apply_variant_styling(self):
        """Apply styling based on button variant."""
        if self.variant == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
            """)
        elif self.variant == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f3f2f1;
                    color: #323130;
                    border: 1px solid #d2d0ce;
                    border-radius: 4px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #edebe9;
                    border-color: #c7c6c4;
                }
                QPushButton:pressed {
                    background-color: #e1dfdd;
                }
                QPushButton:disabled {
                    background-color: #f3f2f1;
                    color: #a19f9d;
                    border-color: #edebe9;
                }
            """)
        elif self.variant == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #d13438;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #b02a2e;
                }
                QPushButton:pressed {
                    background-color: #8f2428;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
            """)
        elif self.variant == "success":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #107c10;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #0e6b0e;
                }
                QPushButton:pressed {
                    background-color: #0c5a0c;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
            """)
        else:  # default
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #323130;
                    border: 1px solid #d2d0ce;
                    border-radius: 4px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #f3f2f1;
                    border-color: #c7c6c4;
                }
                QPushButton:pressed {
                    background-color: #edebe9;
                }
                QPushButton:disabled {
                    background-color: #f3f2f1;
                    color: #a19f9d;
                    border-color: #edebe9;
                }
            """)
    
    def _setup_behavior(self):
        """Setup button behavior."""
        # Enable focus for keyboard navigation
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Set cursor
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def set_size(self, size: str):
        """Set button size.
        
        Args:
            size: Button size ("small", "medium", "large")
        """
        self.size = size
        self._setup_styling()
        
    def set_variant(self, variant: str):
        """Set button variant.
        
        Args:
            variant: Button variant ("primary", "secondary", "danger", "success")
        """
        self.variant = variant
        self._apply_variant_styling()
        
    def set_custom_data(self, data: object):
        """Set custom data to be emitted when button is clicked.
        
        Args:
            data: Custom data object
        """
        self._custom_data = data
        
    def mousePressEvent(self, event):
        """Handle mouse press event."""
        if hasattr(self, '_custom_data'):
            self.clicked_with_data.emit(self._custom_data)
        super().mousePressEvent(event)
