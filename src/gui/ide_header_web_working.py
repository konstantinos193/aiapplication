#!/usr/bin/env python3
"""
IDE Header Panel with Working Web-Embedded React Component.

This header properly embeds the React component from react_header.html
with correct web view configuration and security settings.
"""

import os
import sys
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QIcon, QKeyEvent, QWheelEvent
from PyQt6.QtCore import QEvent


class WorkingWebEmbeddedIDEHeader(QWidget):
    """
    IDE Header with working web-embedded React component.
    
    Features:
    - 100% pixel-perfect React appearance
    - Full React functionality and animations
    - Proper web view configuration
    - Working JavaScript execution
    - ZOOM DISABLED - No Ctrl+wheel or Ctrl+/- zooming
    """
    
    # Signals
    play_state_changed = pyqtSignal(bool)
    transform_tool_changed = pyqtSignal(str)
    theme_toggled = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Setup UI
        self._setup_ui()
        
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
        
        # Create custom web page with proper settings
        self.web_page = self._create_custom_web_page()
        self.web_view.setPage(self.web_page)
        
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
        
        # Get the absolute path to the React HTML file
        current_dir = os.path.dirname(os.path.abspath(__file__))  # src/gui/
        project_root = os.path.dirname(os.path.dirname(current_dir))  # project root
        html_path = os.path.join(project_root, 'assets', 'react_header_simple.html')
        
        print(f"DEBUG: Loading React HTML from: {html_path}")
        print(f"DEBUG: File exists: {os.path.exists(html_path)}")
        
        # Convert to file URL
        html_url = QUrl.fromLocalFile(html_path)
        
        # Load the React component
        self.web_view.setUrl(html_url)
        
    def _create_custom_web_page(self):
        """Create a custom web page with proper settings."""
        web_page = QWebEnginePage(self)
        
        # Get settings and enable everything needed
        settings = web_page.settings()
        
        # DISABLE ZOOM FUNCTIONALITY
        try:
            # Disable zoom text sizing
            if hasattr(QWebEngineSettings, 'ZoomTextOnly'):
                settings.setAttribute(QWebEngineSettings.ZoomTextOnly, False)
                print("DEBUG: Zoom text only disabled")
        except:
            pass
            
        try:
            # Disable automatic zoom
            if hasattr(QWebEngineSettings, 'AutoLoadImages'):
                # This is a workaround - we'll handle zoom prevention in event filters
                pass
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
        
        # Enable JavaScript and all necessary features
        # Note: PyQt6 has different attribute names than PySide6
        try:
            # Try to enable JavaScript (this is the main one we need)
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            print("DEBUG: JavaScript enabled successfully")
        except AttributeError:
            print("DEBUG: JavascriptEnabled attribute not found, trying alternatives...")
            # Try alternative attribute names that might exist
            try:
                # Some versions use different names
                if hasattr(QWebEngineSettings, 'JavascriptEnabled'):
                    settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                    print("DEBUG: JavaScript enabled via alternative method")
                elif hasattr(QWebEngineSettings, 'JavascriptCanOpenWindows'):
                    settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
                    print("DEBUG: JavaScript windows enabled")
                else:
                    print("DEBUG: No JavaScript attributes found, web view may not work properly")
            except Exception as e:
                print(f"DEBUG: Could not enable JavaScript: {e}")
        
        # Try to enable other settings that might exist
        try:
            if hasattr(QWebEngineSettings, 'LocalContentCanAccessRemoteUrls'):
                settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
                print("DEBUG: Local content can access remote URLs")
        except:
            pass
            
        try:
            if hasattr(QWebEngineSettings, 'AllowRunningInsecureContent'):
                settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
                print("DEBUG: Allow running insecure content")
        except:
            pass
            
        try:
            if hasattr(QWebEngineSettings, 'LocalContentCanAccessFileUrls'):
                settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
                print("DEBUG: Local content can access file URLs")
        except:
            pass
        
        print("DEBUG: Web page settings configured")
        
        return web_page
        
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
        
    def _on_web_load_started(self):
        """Handle web content load started."""
        print("DEBUG: React header load started...")
        
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
            
            # Check if React component is working
            self._check_react_component()
            
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
        
    def _check_react_component(self):
        """Check if React component is working properly."""
        print("DEBUG: Checking React component...")
        
        # Check if the test element is visible
        self.web_view.page().runJavaScript("""
            const testElement = document.querySelector('[style*="background: linear-gradient(135deg, #ff0000, #00ff00)"]');
            if (testElement) {
                console.log('Test element found - HTML is working!');
                testElement.style.border = '3px solid yellow';
                testElement.style.zIndex = '9999';
                'HTML_WORKING';
            } else {
                console.log('Test element not found');
                'HTML_NOT_WORKING';
            }
        """, self._on_test_element_check)
        
        # Check if React component rendered
        self.web_view.page().runJavaScript("""
            const rootElement = document.getElementById('root');
            if (rootElement && rootElement.children.length > 0) {
                console.log('Root element has children - React may be working');
                'REACT_MAYBE_WORKING';
            } else {
                console.log('Root element is empty');
                'REACT_NOT_WORKING';
            }
        """, self._on_react_check)
        
    def _on_test_element_check(self, result):
        """Handle test element check result."""
        print(f"DEBUG: Test element check result: {result}")
        
    def _on_react_check(self, result):
        """Handle React component check result."""
        print(f"DEBUG: React component check result: {result}")
        
    # Public API methods
    def setPlayState(self, is_playing: bool):
        """Set the play state - synchronized with React."""
        script = f"window.setPlayState && window.setPlayState({str(is_playing).lower()});"
        self.web_view.page().runJavaScript(script)
        
    def getPlayState(self) -> bool:
        """Get the current play state."""
        # TODO: Get from React component
        return False
        
    def setActiveTransformTool(self, tool: str):
        """Set the active transform tool - synchronized with React."""
        script = f"window.setTransformTool && window.setTransformTool('{tool}');"
        self.web_view.page().runJavaScript(script)
        
    def getActiveTransformTool(self) -> str:
        """Get the currently active transform tool."""
        # TODO: Get from React component
        return "move"
        
    def setActiveTab(self, tab_name: str):
        """Set the active tab in breadcrumb - synchronized with React."""
        script = f"window.setActiveTab && window.setActiveTab('{tab_name}');"
        self.web_view.page().runJavaScript(script)
        
    def setPerformanceData(self, fps: int, memory_usage: int):
        """Set performance data - synchronized with React."""
        script = f"""
        if (window.setPerformanceData) {{
            window.setPerformanceData({{
                fps: {fps},
                memoryUsage: {memory_usage}
            }});
        }}
        """
        self.web_view.page().runJavaScript(script)
        
    def refresh(self):
        """Refresh the React component."""
        self.web_view.reload()


# Alias for backward compatibility
IDEHeader = WorkingWebEmbeddedIDEHeader
