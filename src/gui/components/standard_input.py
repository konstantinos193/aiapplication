"""
Standard Input Components for Nexlify GUI

This module provides standardized input components with consistent
spacing, typography, and alignment following the design system.
"""

from PyQt6.QtWidgets import (
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, 
    QTextEdit, QLabel, QWidget, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.typography_system import typography, FontSize, FontWeight
from ..design_system.alignment_system import alignment, HorizontalAlignment


class StandardTextInput(QWidget):
    """Standard text input component with consistent design system styling."""
    
    # Signals
    text_changed = pyqtSignal(str)
    text_submitted = pyqtSignal(str)
    
    def __init__(self, label: str = "", placeholder: str = "", parent=None,
                 size: str = "medium", variant: str = "default"):
        """Initialize the standard text input.
        
        Args:
            label: Input label text
            placeholder: Placeholder text
            parent: Parent widget
            size: Size variant (small, medium, large)
            variant: Visual variant (default, primary, secondary)
        """
        super().__init__(parent)
        
        # Store configuration
        self.label = label
        self.placeholder = placeholder
        self.size = size
        self.variant = variant
        
        # Create layout
        self._create_layout()
        self._apply_styling()
        self._setup_connections()
        self._set_size()
    
    def _create_layout(self):
        """Create the input layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing.xs)  # 4px spacing between elements
        
        # Label
        if self.label:
            self.label_widget = QLabel(self.label)
            self.label_widget.setObjectName("input-label")
            layout.addWidget(self.label_widget)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(self.placeholder)
        self.input_field.setObjectName("text-input")
        layout.addWidget(self.input_field)
    
    def _apply_styling(self):
        """Apply design system styling."""
        # Get spacing values
        input_height = 32  # 32px input height
        input_padding_h = spacing.sm  # 8px horizontal padding
        input_padding_v = spacing.xs  # 6px vertical padding
        label_margin = spacing.xs  # 8px above inputs
        
        # Get typography values
        label_font_size = typography.sm  # 12px font size
        input_font_size = typography.md  # 14px font size
        
        # Base styling
        base_style = f"""
            QLabel#input-label {{
                color: #cccccc;
                font-size: {label_font_size}px;
                font-weight: {typography.medium};
                margin-bottom: {label_margin}px;
            }}
            
            QLineEdit#text-input {{
                height: {input_height}px;
                padding: {input_padding_v}px {input_padding_h}px;
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: {input_font_size}px;
                selection-background-color: #0078d4;
            }}
            
            QLineEdit#text-input:focus {{
                border: 2px solid #0078d4;
                outline: none;
            }}
            
            QLineEdit#text-input:hover {{
                border: 1px solid #0078d4;
                background-color: #2d2d30;
            }}
            
            QLineEdit#text-input:disabled {{
                background-color: #3e3e42;
                color: #888888;
                border: 1px solid #555555;
            }}
        """
        
        # Variant-specific styling
        if self.variant == "primary":
            base_style += """
                QLineEdit#text-input:focus {
                    border: 2px solid #0078d4;
                }
            """
        elif self.variant == "secondary":
            base_style += """
                QLineEdit#text-input:focus {
                    border: 2px solid #6c757d;
                }
            """
        
        self.setStyleSheet(base_style)
    
    def _set_size(self):
        """Set the input size based on size variant."""
        if self.size == "small":
            self.input_field.setFixedHeight(28)
        elif self.size == "medium":
            self.input_field.setFixedHeight(32)
        elif self.size == "large":
            self.input_field.setFixedHeight(40)
    
    def _setup_connections(self):
        """Setup signal connections."""
        self.input_field.textChanged.connect(self.text_changed.emit)
        self.input_field.returnPressed.connect(
            lambda: self.text_submitted.emit(self.input_field.text())
        )
    
    def get_text(self) -> str:
        """Get the current input text."""
        return self.input_field.text()
    
    def set_text(self, text: str):
        """Set the input text."""
        self.input_field.setText(text)
    
    def clear(self):
        """Clear the input text."""
        self.input_field.clear()


class StandardNumberInput(QWidget):
    """Standard number input component with consistent design system styling."""
    
    # Signals
    value_changed = pyqtSignal(int)
    
    def __init__(self, label: str = "", min_value: int = 0, max_value: int = 100,
                 default_value: int = 0, parent=None, size: str = "medium"):
        """Initialize the standard number input.
        
        Args:
            label: Input label text
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            default_value: Default value
            parent: Parent widget
            size: Size variant (small, medium, large)
        """
        super().__init__(parent)
        
        # Store configuration
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.size = size
        
        # Create layout
        self._create_layout()
        self._apply_styling()
        self._setup_connections()
        self._set_size()
        
        # Set initial value
        self.spin_box.setValue(default_value)
    
    def _create_layout(self):
        """Create the input layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing.xs)  # 4px spacing between elements
        
        # Label
        if self.label:
            self.label_widget = QLabel(self.label)
            self.label_widget.setObjectName("input-label")
            layout.addWidget(self.label_widget)
        
        # Input field
        self.spin_box = QSpinBox()
        self.spin_box.setRange(self.min_value, self.max_value)
        self.spin_box.setObjectName("number-input")
        layout.addWidget(self.spin_box)
    
    def _apply_styling(self):
        """Apply design system styling."""
        # Get spacing values
        input_height = 32  # 32px input height
        input_padding_h = spacing.sm  # 8px horizontal padding
        input_padding_v = spacing.xs  # 6px vertical padding
        label_margin = spacing.xs  # 8px above inputs
        
        # Get typography values
        label_font_size = typography.sm  # 12px font size
        input_font_size = typography.md  # 14px font size
        
        # Base styling
        base_style = f"""
            QLabel#input-label {{
                color: #cccccc;
                font-size: {label_font_size}px;
                font-weight: {typography.medium};
                margin-bottom: {label_margin}px;
            }}
            
            QSpinBox#number-input {{
                height: {input_height}px;
                padding: {input_padding_v}px {input_padding_h}px;
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: {input_font_size}px;
                selection-background-color: #0078d4;
            }}
            
            QSpinBox#number-input:focus {{
                border: 2px solid #0078d4;
                outline: none;
            }}
            
            QSpinBox#number-input:hover {{
                border: 1px solid #0078d4;
                background-color: #2d2d30;
            }}
            
            QSpinBox#number-input::up-button, QSpinBox#number-input::down-button {{
                width: 20px;
                border: none;
                background-color: #2d2d30;
                border-radius: 2px;
            }}
            
            QSpinBox#number-input::up-button:hover, QSpinBox#number-input::down-button:hover {{
                background-color: #0078d4;
            }}
        """
        
        self.setStyleSheet(base_style)
    
    def _set_size(self):
        """Set the input size based on size variant."""
        if self.size == "small":
            self.spin_box.setFixedHeight(28)
        elif self.size == "medium":
            self.spin_box.setFixedHeight(32)
        elif self.size == "large":
            self.spin_box.setFixedHeight(40)
    
    def _setup_connections(self):
        """Setup signal connections."""
        self.spin_box.valueChanged.connect(self.value_changed.emit)
    
    def get_value(self) -> int:
        """Get the current input value."""
        return self.spin_box.value()
    
    def set_value(self, value: int):
        """Set the input value."""
        self.spin_box.setValue(value)


class StandardDropdown(QWidget):
    """Standard dropdown component with consistent design system styling."""
    
    # Signals
    selection_changed = pyqtSignal(str)
    
    def __init__(self, label: str = "", options: list = None, parent=None,
                 size: str = "medium", variant: str = "default"):
        """Initialize the standard dropdown.
        
        Args:
            label: Dropdown label text
            options: List of dropdown options
            parent: Parent widget
            size: Size variant (small, medium, large)
            variant: Visual variant (default, primary, secondary)
        """
        super().__init__(parent)
        
        # Store configuration
        self.label = label
        self.options = options or []
        self.size = size
        self.variant = variant
        
        # Create layout
        self._create_layout()
        self._apply_styling()
        self._setup_connections()
        self._set_size()
        
        # Add options
        self._populate_options()
    
    def _create_layout(self):
        """Create the dropdown layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing.xs)  # 4px spacing between elements
        
        # Label
        if self.label:
            self.label_widget = QLabel(self.label)
            self.label_widget.setObjectName("input-label")
            layout.addWidget(self.label_widget)
        
        # Dropdown field
        self.combo_box = QComboBox()
        self.combo_box.setObjectName("dropdown-input")
        layout.addWidget(self.combo_box)
    
    def _populate_options(self):
        """Populate the dropdown with options."""
        self.combo_box.addItems(self.options)
    
    def _apply_styling(self):
        """Apply design system styling."""
        # Get spacing values
        input_height = 32  # 32px input height
        input_padding_h = spacing.sm  # 8px horizontal padding
        input_padding_v = spacing.xs  # 6px vertical padding
        label_margin = spacing.xs  # 8px above inputs
        
        # Get typography values
        label_font_size = typography.sm  # 12px font size
        input_font_size = typography.md  # 14px font size
        
        # Base styling
        base_style = f"""
            QLabel#input-label {{
                color: #cccccc;
                font-size: {label_font_size}px;
                font-weight: {typography.medium};
                margin-bottom: {label_margin}px;
            }}
            
            QComboBox#dropdown-input {{
                height: {input_height}px;
                padding: {input_padding_v}px {input_padding_h}px;
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: {input_font_size}px;
                selection-background-color: #0078d4;
            }}
            
            QComboBox#dropdown-input:focus {{
                border: 2px solid #0078d4;
                outline: none;
            }}
            
            QComboBox#dropdown-input:hover {{
                border: 1px solid #0078d4;
                background-color: #2d2d30;
            }}
            
            QComboBox#dropdown-input::drop-down {{
                border: none;
                width: 20px;
            }}
            
            QComboBox#dropdown-input::down-arrow {{
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIgNEw2IDhMMTAgNCIgc3Ryb2tlPSIjY2NjY2NjIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
                width: 12px;
                height: 12px;
            }}
            
            QComboBox#dropdown-input QAbstractItemView {{
                background-color: #1e1e1e;
                border: 1px solid #555555;
                selection-background-color: #0078d4;
                color: #ffffff;
            }}
        """
        
        self.setStyleSheet(base_style)
    
    def _set_size(self):
        """Set the dropdown size based on size variant."""
        if self.size == "small":
            self.combo_box.setFixedHeight(28)
        elif self.size == "medium":
            self.combo_box.setFixedHeight(32)
        elif self.size == "large":
            self.combo_box.setFixedHeight(40)
    
    def _setup_connections(self):
        """Setup signal connections."""
        self.combo_box.currentTextChanged.connect(self.selection_changed.emit)
    
    def get_selection(self) -> str:
        """Get the current selection."""
        return self.combo_box.currentText()
    
    def set_selection(self, text: str):
        """Set the current selection."""
        index = self.combo_box.findText(text)
        if index >= 0:
            self.combo_box.setCurrentIndex(index)
    
    def add_option(self, option: str):
        """Add a new option to the dropdown."""
        self.combo_box.addItem(option)
    
    def clear_options(self):
        """Clear all options from the dropdown."""
        self.combo_box.clear() 