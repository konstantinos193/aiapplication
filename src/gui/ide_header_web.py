#!/usr/bin/env python3
"""
IDE Header Panel with Web-Embedded React Component for Pixel-Perfect Matching.

This header embeds the actual React component inside PyQt6 using QWebEngineView,
providing 100% pixel-perfect visual matching with full functionality.
"""

import os
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QIcon, QKeyEvent, QWheelEvent
from PyQt6.QtCore import QEvent

from .design_system.react_theme_system import react_theme


class WebEmbeddedIDEHeader(QWidget):
    """
    IDE Header with web-embedded React component for pixel-perfect matching.
    
    Features:
    - 100% pixel-perfect React appearance
    - Full React functionality and animations
    - Bidirectional communication between React and PyQt6
    - Real-time performance updates
    - Theme integration
    """
    
    # Signals
    play_state_changed = pyqtSignal(bool)
    transform_tool_changed = pyqtSignal(str)
    theme_toggled = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # State
        self._is_playing = False
        self._active_transform_tool = "move"
        self._fps = 60
        self._memory_usage = 245
        
        # Setup UI
        self._setup_ui()
        self._setup_web_communication()
        self._setup_timer()
        
        # Set fixed height to match React
        self.setFixedHeight(64)  # h-16 = 64px
        
        # Install event filter to prevent zoom shortcuts
        self.installEventFilter(self)
        
        # Setup zoom prevention timer
        self._setup_zoom_prevention_timer()
        
    def _setup_zoom_prevention_timer(self):
        """Setup timer to ensure zoom factor stays at 1.0."""
        self._zoom_prevention_timer = QTimer()
        self._zoom_prevention_timer.timeout.connect(self._enforce_zoom_prevention)
        self._zoom_prevention_timer.start(100)  # Check every 100ms
        
    def _enforce_zoom_prevention(self):
        """Enforce zoom prevention by resetting zoom factor to 1.0."""
        if hasattr(self, 'web_view') and self.web_view:
            current_zoom = self.web_view.zoomFactor()
            if current_zoom != 1.0:
                print(f"DEBUG: Zoom factor was {current_zoom}, resetting to 1.0")
                self.web_view.setZoomFactor(1.0)
        
    def _setup_ui(self):
        """Setup the web-embedded header interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create web view for React component
        self.web_view = QWebEngineView()
        
        # Get the absolute path to the React HTML file
        # Go from src/gui/ to project root, then to assets
        current_dir = os.path.dirname(os.path.abspath(__file__))  # src/gui/
        project_root = os.path.dirname(os.path.dirname(current_dir))  # project root
        
        # Use the React HTML file
        html_path = os.path.join(project_root, 'assets', 'react_header.html')
        print(f"DEBUG: Using React HTML: {html_path}")
        print(f"DEBUG: React HTML exists: {os.path.exists(html_path)}")
        
        # Convert to file URL
        html_url = QUrl.fromLocalFile(html_path)
        
        # Set web view properties
        self.web_view.setMinimumHeight(64)
        self.web_view.setMaximumHeight(64)
        
        # DISABLE ZOOM - Set zoom factor to 1.0 and prevent changes
        self.web_view.setZoomFactor(1.0)
        
        # Disable context menu to prevent zoom options
        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        
        # Add web view to layout
        main_layout.addWidget(self.web_view)
        
        # Connect web view signals
        self.web_view.loadFinished.connect(self._on_web_loaded)
        self.web_view.loadStarted.connect(self._on_web_load_started)
        self.web_view.loadProgress.connect(self._on_web_load_progress)
        
        # Force a resize to ensure proper sizing
        self.web_view.resize(800, 64)  # Give it a reasonable width
        
        # Ensure the web view is properly configured for rendering
        self.web_view.setMinimumSize(800, 64)
        self.web_view.setMaximumSize(8000, 64)  # Allow horizontal expansion
        
        # Load the React component after a short delay to ensure proper initialization
        print("DEBUG: Scheduling HTML load...")
        QTimer.singleShot(100, lambda: self._load_html_content(html_url))
        
    def eventFilter(self, obj, event):
        """Event filter to prevent zoom shortcuts and wheel zooming."""
        if event.type() == QEvent.Type.Wheel:
            # Prevent mouse wheel zooming
            wheel_event = QWheelEvent(event)
            if wheel_event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Ctrl+wheel detected - prevent zoom
                print("DEBUG: Ctrl+wheel zoom prevented")
                return True  # Event handled, don't propagate
                
        elif event.type() == QEvent.Type.KeyPress:
            # Prevent keyboard zoom shortcuts
            if hasattr(event, 'key') and hasattr(event, 'modifiers'):
                # Event is already a QKeyEvent, use it directly
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal]:
                        # Ctrl+Plus, Ctrl+Minus, Ctrl+Equal detected - prevent zoom
                        print("DEBUG: Ctrl+Plus/Minus zoom prevented")
                        return True  # Event handled, don't propagate
                    elif event.key() == Qt.Key.Key_0:
                        # Ctrl+0 detected - prevent zoom reset
                        print("DEBUG: Ctrl+0 zoom reset prevented")
                        return True  # Event handled, don't propagate
                    
        # Let other events pass through
        return super().eventFilter(obj, event)
        
    def wheelEvent(self, event):
        """Override wheel event to prevent zooming."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Ctrl+wheel detected - prevent zoom
            print("DEBUG: Ctrl+wheel zoom prevented in wheelEvent")
            event.accept()  # Accept but don't process
            return
        super().wheelEvent(event)
        
    def keyPressEvent(self, event):
        """Override key press event to prevent zoom shortcuts."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Minus, Qt.Key.Key_Equal, Qt.Key.Key_0]:
                # Ctrl+Plus, Ctrl+Minus, Ctrl+Equal, Ctrl+0 detected - prevent zoom
                print("DEBUG: Ctrl+Plus/Minus/0 zoom prevented in keyPressEvent")
                event.accept()  # Accept but don't process
                return
        super().keyPressEvent(event)
        
    def _load_html_content(self, html_url):
        """Load HTML content with proper debugging."""
        print(f"DEBUG: Loading HTML content from: {html_url.toString()}")
        print(f"DEBUG: Web view is visible: {self.web_view.isVisible()}")
        print(f"DEBUG: Web view size: {self.web_view.size()}")
        
        # Set the URL
        self.web_view.setUrl(html_url)
        print(f"DEBUG: URL set successfully")
        
        # Check if it was set properly
        print(f"DEBUG: Web view page: {self.web_view.page()}")
        print(f"DEBUG: Web view page URL: {self.web_view.page().url().toString() if self.web_view.page() else 'No page'}")
        
    def _setup_web_communication(self):
        """Setup communication between React and PyQt6."""
        # Create a custom web page for communication
        self.web_page = CustomWebPage(self)
        
        # Enable JavaScript and remove security restrictions
        
        # Enable JavaScript and other necessary settings
        settings = self.web_page.settings()
        
        # DISABLE ZOOM FUNCTIONALITY
        try:
            # Disable zoom text sizing
            if hasattr(QWebEngineSettings, 'ZoomTextOnly'):
                settings.setAttribute(QWebEngineSettings.ZoomTextOnly, False)
                print("DEBUG: Zoom text only disabled")
        except:
            pass
            
        # Additional zoom prevention settings
        try:
            # Disable any zoom-related settings that might exist
            zoom_attributes = [
                'ZoomTextOnly', 'ZoomFactor', 'ZoomLevel', 'DefaultZoomLevel',
                'MinimumZoomLevel', 'MaximumZoomLevel'
            ]
            for attr_name in zoom_attributes:
                if hasattr(QWebEngineSettings, attr_name):
                    try:
                        # Try to disable or set to neutral values
                        if attr_name in ['ZoomTextOnly']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), False)
                        elif attr_name in ['DefaultZoomLevel', 'ZoomLevel']:
                            settings.setAttribute(getattr(QWebEngineSettings, attr_name), 1.0)
                        print(f"DEBUG: {attr_name} setting configured")
                    except Exception as e:
                        print(f"DEBUG: Could not configure {attr_name}: {e}")
        except Exception as e:
            print(f"DEBUG: Error configuring zoom settings: {e}")
        
        # Try different attribute names that might exist
        js_attributes = [
            'JavascriptEnabled',
            'JavascriptCanOpenWindows', 
            'JavascriptCanAccessClipboard',
            'LocalContentCanAccessRemoteUrls',
            'AllowRunningInsecureContent',
            'AllowGeolocationOnInsecureOrigins'
        ]
        
        for attr_name in js_attributes:
            try:
                if hasattr(QWebEngineSettings, attr_name):
                    attr_value = getattr(QWebEngineSettings, attr_name)
                    settings.setAttribute(attr_value, True)
                    print(f"DEBUG: Enabled {attr_name}")
            except Exception as e:
                print(f"DEBUG: Could not enable {attr_name}: {e}")
        
        # Set additional settings that might help
        try:
            settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
            print("DEBUG: Local content can access remote URLs")
        except:
            pass
            
        try:
            settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
            print("DEBUG: Allow running insecure content")
        except:
            pass
        
        self.web_view.setPage(self.web_page)
        
        # Connect signals from web page
        self.web_page.play_state_changed.connect(self._on_play_state_changed)
        self.web_page.transform_tool_changed.connect(self._on_transform_tool_changed)
        self.web_page.theme_toggled.connect(self._on_theme_toggled)
        
    def _setup_timer(self):
        """Setup timer for performance updates."""
        self._performance_timer = QTimer()
        self._performance_timer.timeout.connect(self._update_performance)
        self._performance_timer.start(1000)  # Update every second
        
    def _on_web_load_started(self):
        """Handle web content load started."""
        print("DEBUG: React header load started...")
        
    def _on_web_load_progress(self, progress: int):
        """Handle web content load progress."""
        print(f"DEBUG: React header load progress: {progress}%")
        
    def _on_web_loaded(self, success: bool):
        """Handle web page load completion."""
        print(f"DEBUG: React header load finished, success: {success}")
        if success:
            print("DEBUG: React header loaded successfully!")
            
            # Force the web view to update and render
            self.web_view.update()
            self.web_view.repaint()
            
            # Inject zoom prevention JavaScript
            self._inject_zoom_prevention_script()
            
            # Check if React component is mounted and catch any errors
            self.web_view.page().runJavaScript("""
                try {
                    console.log('Checking React component...');
                    if (document.getElementById('root')) {
                        console.log('Root element found');
                        if (document.getElementById('root').children.length > 0) {
                            console.log('React component mounted');
                        } else {
                            console.log('Root element is empty');
                        }
                    } else {
                        console.log('Root element not found');
                    }
                    
                    // Check if our test element is visible
                    const testElement = document.querySelector('[style*="background: linear-gradient(135deg, #ff0000, #00ff00)"]');
                    if (testElement) {
                        console.log('Test element found and should be visible');
                        testElement.style.zIndex = '9999';
                        testElement.style.position = 'fixed';
                    } else {
                        console.log('Test element not found');
                    }
                    
                } catch (error) {
                    console.error('Error checking React component:', error);
                }
            """)
            
                    # Also check the web view content directly
            self._check_web_view_content()
            
            # Force a final update to ensure rendering
            QTimer.singleShot(500, self._force_web_view_update)
            
            # Inject initial state
            self._inject_initial_state()
        else:
            print("DEBUG: React header failed to load!")
            
    def _inject_zoom_prevention_script(self):
        """Inject JavaScript to prevent zooming on the HTML side."""
        zoom_prevention_script = """
        // Disable zoom through JavaScript
        (function() {
            'use strict';
            
            // Prevent zoom shortcuts
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey && (e.key === '+' || e.key === '-' || e.key === '0' || e.key === '=')) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Zoom shortcut prevented:', e.key);
                    return false;
                }
            }, true);
            
            // Prevent wheel zoom
            document.addEventListener('wheel', function(e) {
                if (e.ctrlKey) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Ctrl+wheel zoom prevented');
                    return false;
                }
            }, { passive: false });
            
            // Prevent touch zoom
            document.addEventListener('gesturestart', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Touch zoom gesture prevented');
                return false;
            }, { passive: false });
            
            // Prevent double-tap zoom
            let lastTouchEnd = 0;
            document.addEventListener('touchend', function(e) {
                const now = (new Date()).getTime();
                if (now - lastTouchEnd <= 300) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Double-tap zoom prevented');
                    return false;
                }
                lastTouchEnd = now;
            }, false);
            
            // Set viewport to prevent zoom
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) {
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
            } else {
                const newViewport = document.createElement('meta');
                newViewport.name = 'viewport';
                newViewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                document.head.appendChild(newViewport);
            }
            
            console.log('Zoom prevention JavaScript injected successfully');
        })();
        """
        
        try:
            self.web_view.page().runJavaScript(zoom_prevention_script)
            print("DEBUG: Zoom prevention JavaScript injected")
        except Exception as e:
            print(f"DEBUG: Failed to inject zoom prevention JavaScript: {e}")
            
    def _check_web_view_content(self):
        """Check what content is actually in the web view."""
        print("DEBUG: Checking web view content...")
        print(f"DEBUG: Web view size: {self.web_view.size()}")
        print(f"DEBUG: Web view is visible: {self.web_view.isVisible()}")
        print(f"DEBUG: Web view has focus: {self.web_view.hasFocus()}")
        
        # Try to get the page title
        self.web_view.page().runJavaScript("document.title", self._on_title_received)
        
        # Try to get the HTML content
        self.web_view.page().runJavaScript("document.documentElement.outerHTML", self._on_html_received)
        
        # Check if our test element exists
        self.web_view.page().runJavaScript("""
            const testElement = document.querySelector('[style*=\"background: linear-gradient(135deg, #ff0000, #00ff00)\"]');
            if (testElement) {
                console.log('Test element found in HTML');
                testElement.style.border = '3px solid yellow';
                testElement.style.zIndex = '9999';
                'FOUND';
            } else {
                console.log('Test element NOT found in HTML');
                'NOT_FOUND';
            }
        """, self._on_test_element_check)
        
    def _on_title_received(self, title):
        """Handle title received from web view."""
        print(f"DEBUG: Web page title: {title}")
        
    def _on_html_received(self, html):
        """Handle HTML content received from web view."""
        print(f"DEBUG: HTML content length: {len(html) if html else 0}")
        if html and len(html) > 100:
            print(f"DEBUG: HTML preview: {html[:100]}...")
        
    def _on_test_element_check(self, result):
        """Handle test element check result."""
        print(f"DEBUG: Test element check result: {result}")
        
    def _force_web_view_update(self):
        """Force the web view to update and render its content."""
        print("DEBUG: Forcing web view update...")
        self.web_view.update()
        self.web_view.repaint()
        
        # Force a resize to trigger rendering
        current_size = self.web_view.size()
        self.web_view.resize(current_size.width() + 1, current_size.height())
        self.web_view.resize(current_size.width(), current_size.height())
        
        print("DEBUG: Web view update forced")
        
    def _inject_initial_state(self):
        """Inject initial state into React component."""
        # Set initial play state
        self._inject_play_state()
        
        # Set initial transform tool
        self._inject_transform_tool()
        
        # Set initial performance data
        self._inject_performance_data()
        
    def _inject_play_state(self):
        """Inject play state into React component."""
        script = f"window.setPlayState && window.setPlayState({str(self._is_playing).lower()});"
        self.web_view.page().runJavaScript(script)
        
    def _inject_transform_tool(self):
        """Inject transform tool state into React component."""
        script = f"window.setTransformTool && window.setTransformTool('{self._active_transform_tool}');"
        self.web_view.page().runJavaScript(script)
        
    def _inject_performance_data(self):
        """Inject performance data into React component."""
        script = f"""
        if (window.setPerformanceData) {{
            window.setPerformanceData({{
                fps: {self._fps},
                memoryUsage: {self._memory_usage}
            }});
        }}
        """
        self.web_view.page().runJavaScript(script)
        
    def _update_performance(self):
        """Update performance metrics and inject into React."""
        import random
        
        # Simulate performance updates
        self._fps = random.randint(55, 65)
        self._memory_usage = random.randint(240, 250)
        
        # Inject updated data into React
        self._inject_performance_data()
        
    def _on_play_state_changed(self, is_playing: bool):
        """Handle play state changes from React."""
        self._is_playing = is_playing
        self.play_state_changed.emit(is_playing)
        
    def _on_transform_tool_changed(self, tool: str):
        """Handle transform tool changes from React."""
        self._active_transform_tool = tool
        self.transform_tool_changed.emit(tool)
        
    def _on_theme_toggled(self):
        """Handle theme toggle from React."""
        self.theme_toggled.emit()
        
    # Public API methods
    def setPlayState(self, is_playing: bool):
        """Set the play state - synchronized with React."""
        self._is_playing = is_playing
        self._inject_play_state()
        
    def getPlayState(self) -> bool:
        """Get the current play state."""
        return self._is_playing
        
    def setActiveTransformTool(self, tool: str):
        """Set the active transform tool - synchronized with React."""
        self._active_transform_tool = tool
        self._inject_transform_tool()
        
    def getActiveTransformTool(self) -> str:
        """Get the currently active transform tool."""
        return self._active_transform_tool
        
    def setActiveTab(self, tab_name: str):
        """Set the active tab in breadcrumb - synchronized with React."""
        script = f"window.setActiveTab && window.setActiveTab('{tab_name}');"
        self.web_view.page().runJavaScript(script)
        
    def setPerformanceData(self, fps: int, memory_usage: int):
        """Set performance data - synchronized with React."""
        self._fps = fps
        self._memory_usage = memory_usage
        self._inject_performance_data()
        
    def refresh(self):
        """Refresh the React component."""
        self.web_view.reload()


class CustomWebPage(QWebEnginePage):
    """
    Custom web page for handling communication between React and PyQt6.
    """
    
    # Signals for communication
    play_state_changed = pyqtSignal(bool)
    transform_tool_changed = pyqtSignal(str)
    theme_toggled = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Connect JavaScript console messages
        try:
            # Connect to the javaScriptConsoleMessage signal
            self.javaScriptConsoleMessage.connect(self._on_console_message)
            print("Connected to javaScriptConsoleMessage signal successfully!")
        except Exception as e:
            print(f"Error connecting to javaScriptConsoleMessage: {e}")
            print("Communication between React and PyQt6 may be limited")
        
    def _on_console_message(self, level, message, line_number, source_id):
        """Handle JavaScript console messages for communication."""
        try:
            # Parse communication messages
            if message.startswith('PYQT6_EVENT:'):
                self._parse_event_message(message)
        except Exception as e:
            print(f"Error parsing console message: {e}")
            
    def _parse_event_message(self, message: str):
        """Parse event messages from React."""
        try:
            # Extract event data
            event_data = message.replace('PYQT6_EVENT:', '').strip()
            
            # Parse JSON event data
            import json
            event = json.loads(event_data)
            
            # Handle different event types
            event_type = event.get('type')
            event_data = event.get('data')
            
            if event_type == 'playStateChanged':
                self.play_state_changed.emit(event_data)
            elif event_type == 'transformToolChanged':
                self.transform_tool_changed.emit(event_data)
            elif event_type == 'themeToggled':
                self.theme_toggled.emit()
                
        except Exception as e:
            print(f"Error parsing event message: {e}")


# Alias for backward compatibility
IDEHeader = WebEmbeddedIDEHeader
