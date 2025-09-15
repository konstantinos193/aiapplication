"""
Graphical User Interface for Nexlify.

This package contains all GUI components including:
- Main window
- Panels and widgets
- Rendering viewport
- Menu system
- Toolbars
"""

# Import new IDE components
from .game_design_ide import GameDesignIDE
from .ide_header_web_working import IDEHeader
from .ide_left_panel import IDELeftPanel
from .ide_center_panel import IDECenterPanel
from .ide_ai_assistant import IDEAIAssistant
from .ide_status_bar import IDEStatusBar

__all__ = [
    'GameDesignIDE',
    'IDEHeader',
    'IDELeftPanel',
    'IDECenterPanel',
    'IDEAIAssistant',
    'IDEStatusBar'
]
