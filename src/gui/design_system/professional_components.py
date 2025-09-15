#!/usr/bin/env python3
"""
Professional UI Components for Nexlify Engine.

This module provides beautiful, custom-designed UI components
with gradients, shadows, and professional aesthetics.
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk
import math


class ComponentType(Enum):
    """Types of professional UI components."""
    BUTTON = "button"
    PANEL = "panel"
    HEADER = "header"
    INPUT = "input"
    DROPDOWN = "dropdown"
    TOGGLE = "toggle"
    SLIDER = "slider"
    PROGRESS = "progress"
    CARD = "card"
    MODAL = "modal"
    TOOLTIP = "tooltip"


@dataclass
class ComponentStyle:
    """Professional component styling configuration."""
    background: str
    foreground: str
    border_color: str
    border_width: int
    border_radius: int
    padding: tuple
    margin: tuple
    shadow: Dict
    gradient: Optional[str] = None
    hover_effects: Optional[Dict] = None
    focus_effects: Optional[Dict] = None


class ProfessionalButton(tk.Canvas):
    """Professional button with gradients, shadows, and hover effects."""
    
    def __init__(self, parent, text="", command=None, style_type="primary", 
                 width=120, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.style_type = style_type
        self.width = width
        self.height = height
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # Create the button
        self._create_button()
    
    def _create_button(self):
        """Create the professional button appearance."""
        # Clear canvas
        self.delete("all")
        
        # Get theme colors
        theme = self.master.master.master.theme if hasattr(self.master.master.master, 'theme') else None
        
        if theme:
            colors = theme.color_palette
            shadows = theme.shadows
        else:
            # Fallback colors
            colors = type('Colors', (), {
                'primary': '#2563eb',
                'primary_light': '#3b82f6',
                'primary_dark': '#1d4ed8',
                'surface': '#1e293b',
                'surface_light': '#334155',
                'surface_dark': '#0f172a',
                'text_primary': '#f8fafc',
                'border': '#334155'
            })()
            shadows = {'button': type('Shadow', (), {'color': '#000000', 'offset_x': 0, 'offset_y': 2, 'blur_radius': 8, 'spread_radius': 0, 'opacity': 0.25})()}
        
        # Create shadow (simplified for Tkinter compatibility)
        shadow_offset = 2
        shadow_color = "#1a1a1a"  # Dark shadow color
        
        # Draw shadow
        self.create_rectangle(
            shadow_offset + 2, shadow_offset + 2,
            self.width - 2, self.height - 2,
            fill=shadow_color, outline="",
            width=0
        )
        
        # Create button background
        if self.style_type == "primary":
            # Primary button with gradient
            self.create_rectangle(
                0, 0, self.width, self.height,
                fill=colors.primary, outline="",
                width=0
            )
            # Add gradient effect
            self._create_gradient_overlay(colors.primary, colors.primary_dark)
        else:
            # Secondary button
            self.create_rectangle(
                0, 0, self.width, self.height,
                fill=colors.surface, outline=colors.border,
                width=1
            )
            # Add subtle gradient
            self._create_gradient_overlay(colors.surface, colors.surface_dark)
        
        # Add text
        text_color = colors.text_primary
        self.create_text(
            self.width // 2, self.height // 2,
            text=self.text, fill=text_color,
            font=("Segoe UI", 12, "bold"),
            anchor="center"
        )
        
        # Add subtle highlight
        self._create_highlight()
    
    def _create_gradient_overlay(self, start_color, end_color):
        """Create a gradient overlay effect."""
        steps = 20
        for i in range(steps):
            ratio = i / steps
            color = self._interpolate_color(start_color, end_color, ratio)
            y = int(self.height * ratio)
            height = int(self.height / steps)
            
            self.create_rectangle(
                0, y, self.width, y + height,
                fill=color, outline="",
                width=0
            )
    
    def _create_highlight(self):
        """Create a subtle highlight effect."""
        highlight_color = "#ffffff"
        self.create_rectangle(
            0, 0, self.width, self.height // 3,
            fill=highlight_color, outline="",
            width=0
        )
    
    def _hex_to_rgba(self, hex_color, alpha):
        """Convert hex color to RGBA string."""
        # Tkinter doesn't support alpha, so use a darker version
        return hex_color
    
    def _interpolate_color(self, color1, color2, ratio):
        """Interpolate between two hex colors."""
        # Simple color interpolation
        if ratio < 0.5:
            return color1
        else:
            return color2
    
    def _on_click(self, event):
        """Handle button click."""
        self._create_button_pressed()
    
    def _on_release(self, event):
        """Handle button release."""
        self._create_button()
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        """Handle mouse enter."""
        self._create_button_hover()
    
    def _on_leave(self, event):
        """Handle mouse leave."""
        self._create_button()
    
    def _create_button_pressed(self):
        """Create pressed button appearance."""
        self.delete("all")
        
        # Get theme colors
        theme = self.master.master.master.theme if hasattr(self.master.master.master, 'theme') else None
        
        if theme:
            colors = theme.color_palette
        else:
            colors = type('Colors', (), {
                'primary': '#1d4ed8',
                'primary_light': '#3b82f6',
                'surface': '#0f172a',
                'surface_light': '#1e293b',
                'text_primary': '#f8fafc'
            })()
        
        # Create pressed button (darker)
        if self.style_type == "primary":
            self.create_rectangle(
                0, 0, self.width, self.height,
                fill=colors.primary_dark, outline="",
                width=0
            )
        else:
            self.create_rectangle(
                0, 0, self.width, self.height,
                fill=colors.surface_dark, outline="",
                width=0
            )
        
        # Add text
        self.create_text(
            self.width // 2, self.height // 2 + 1,  # Slight offset for pressed effect
            text=self.text, fill=colors.text_primary,
            font=("Segoe UI", 12, "bold"),
            anchor="center"
        )
    
    def _create_button_hover(self):
        """Create hover button appearance."""
        self.delete("all")
        
        # Get theme colors
        theme = self.master.master.master.theme if hasattr(self.master.master.master, 'theme') else None
        
        if theme:
            colors = theme.color_palette
        else:
            colors = type('Colors', (), {
                'primary': '#3b82f6',
                'primary_light': '#60a5fa',
                'surface': '#334155',
                'surface_light': '#475569',
                'text_primary': '#f8fafc'
            })()
        
        # Create hover button (lighter)
        if self.style_type == "primary":
            self.create_rectangle(
                0, 0, self.width, self.height,
                fill=colors.primary_light, outline="",
                width=0
            )
        else:
            self.create_rectangle(
                0, 0, self.width, self.height,
                fill=colors.surface_light, outline="",
                width=0
            )
        
        # Add text
        self.create_text(
            self.width // 2, self.height // 2,
            text=self.text, fill=colors.text_primary,
            font=("Segoe UI", 12, "bold"),
            anchor="center"
        )
        
        # Add glow effect
        self._create_glow_effect()
    
    def _create_glow_effect(self):
        """Create a subtle glow effect."""
        glow_color = "#ffffff"
        self.create_rectangle(
            2, 2, self.width - 2, self.height - 2,
            outline=glow_color, width=2
        )


class ProfessionalPanel(tk.Frame):
    """Professional panel with gradients, shadows, and modern design."""
    
    def __init__(self, parent, title="", width=300, height=200, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        
        self.title = title
        self.width = width
        self.height = height
        
        # Configure frame
        self.configure(relief="flat", bd=0)
        
        # Create canvas for custom drawing
        self.canvas = tk.Canvas(
            self, width=width, height=height,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Create the panel
        self._create_panel()
    
    def _create_panel(self):
        """Create the professional panel appearance."""
        # Clear canvas
        self.canvas.delete("all")
        
        # Get theme colors
        theme = self.master.theme if hasattr(self.master, 'theme') else None
        
        if theme:
            colors = theme.color_palette
            shadows = theme.shadows
        else:
            # Fallback colors
            colors = type('Colors', (), {
                'surface': '#1e293b',
                'surface_dark': '#0f172a',
                'border': '#334155',
                'text_primary': '#f8fafc',
                'text_secondary': '#cbd5e1'
            })()
            shadows = {'panel': type('Shadow', (), {'color': '#000000', 'offset_x': 0, 'offset_y': 4, 'blur_radius': 12, 'spread_radius': 0, 'opacity': 0.15})()}
        
        # Create shadow (simplified for Tkinter compatibility)
        shadow_offset = 4
        shadow_color = "#1a1a1a"  # Dark shadow color
        
        # Draw shadow
        self.canvas.create_rectangle(
            shadow_offset, shadow_offset,
            self.width - 2, self.height - 2,
            fill=shadow_color, outline="",
            width=0
        )
        
        # Create panel background with gradient
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill=colors.surface, outline=colors.border,
            width=1
        )
        
        # Add gradient effect
        self._create_panel_gradient(colors.surface, colors.surface_dark)
        
        # Add title if provided
        if self.title:
            self._create_title(colors.text_primary, colors.text_secondary)
        
        # Add subtle highlight
        self._create_panel_highlight()
    
    def _create_panel_gradient(self, start_color, end_color):
        """Create a panel gradient effect."""
        steps = 15
        for i in range(steps):
            ratio = i / steps
            color = self._interpolate_color(start_color, end_color, ratio)
            y = int(self.height * ratio)
            height = int(self.height / steps)
            
            self.canvas.create_rectangle(
                0, y, self.width, y + height,
                fill=color, outline="",
                width=0
            )
    
    def _create_title(self, primary_color, secondary_color):
        """Create panel title."""
        # Title background
        title_height = 30
        self.canvas.create_rectangle(
            0, 0, self.width, title_height,
            fill=primary_color, outline="",
            width=0
        )
        
        # Title text
        self.canvas.create_text(
            15, title_height // 2,
            text=self.title, fill=secondary_color,
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        )
        
        # Title separator
        self.canvas.create_line(
            0, title_height, self.width, title_height,
            fill=secondary_color, width=1
        )
    
    def _create_panel_highlight(self):
        """Create a subtle panel highlight."""
        highlight_color = "#ffffff"
        self.canvas.create_rectangle(
            0, 0, self.width, 2,
            fill=highlight_color, outline="",
            width=0
        )
    
    def _hex_to_rgba(self, hex_color, alpha):
        """Convert hex color to RGBA string."""
        return hex_color + "40"
    
    def _interpolate_color(self, color1, color2, ratio):
        """Interpolate between two hex colors."""
        if ratio < 0.5:
            return color1
        else:
            return color2


class ProfessionalHeader(tk.Frame):
    """Professional header with gradients and modern design."""
    
    def __init__(self, parent, title="Nexlify Engine", width=800, height=60, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        
        self.title = title
        self.width = width
        self.height = height
        
        # Configure frame
        self.configure(relief="flat", bd=0)
        
        # Create canvas for custom drawing
        self.canvas = tk.Canvas(
            self, width=width, height=height,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Create the header
        self._create_header()
    
    def _create_header(self):
        """Create the professional header appearance."""
        # Clear canvas
        self.canvas.delete("all")
        
        # Get theme colors
        theme = self.master.theme if hasattr(self.master, 'theme') else None
        
        if theme:
            colors = theme.color_palette
            shadows = theme.shadows
        else:
            # Fallback colors
            colors = type('Colors', (), {
                'background': '#0f172a',
                'background_light': '#1e293b',
                'border': '#334155',
                'text_primary': '#f8fafc',
                'accent': '#f59e0b'
            })()
            shadows = {'header': type('Shadow', (), {'color': '#000000', 'offset_x': 0, 'offset_y': 2, 'blur_radius': 8, 'spread_radius': 0, 'opacity': 0.2})()}
        
        # Create shadow (simplified for Tkinter compatibility)
        shadow_offset = 2
        shadow_color = "#1a1a1a"  # Dark shadow color
        
        # Draw shadow
        self.canvas.create_rectangle(
            shadow_offset, shadow_offset,
            self.width, self.height,
            fill=shadow_color, outline="",
            width=0
        )
        
        # Create header background with gradient
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill=colors.background, outline="",
            width=0
        )
        
        # Add horizontal gradient effect
        self._create_header_gradient(colors.background, colors.background_light)
        
        # Add title
        self._create_header_title(colors.text_primary, colors.accent)
        
        # Add subtle border
        self.canvas.create_line(
            0, self.height - 1, self.width, self.height - 1,
            fill=colors.border, width=1
        )
    
    def _create_header_gradient(self, start_color, end_color):
        """Create a header gradient effect."""
        steps = 20
        for i in range(steps):
            ratio = i / steps
            color = self._interpolate_color(start_color, end_color, ratio)
            x = int(self.width * ratio)
            width = int(self.width / steps)
            
            self.canvas.create_rectangle(
                x, 0, x + width, self.height,
                fill=color, outline="",
                width=0
            )
    
    def _create_header_title(self, text_color, accent_color):
        """Create header title with accent."""
        # Main title
        self.canvas.create_text(
            20, self.height // 2,
            text=self.title, fill=text_color,
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        )
        
        # Accent line
        accent_width = 60
        accent_x = 20
        accent_y = self.height - 8
        
        self.canvas.create_line(
            accent_x, accent_y, accent_x + accent_width, accent_y,
            fill=accent_color, width=3
        )
    
    def _hex_to_rgba(self, hex_color, alpha):
        """Convert hex color to RGBA string."""
        return hex_color + "40"
    
    def _interpolate_color(self, color1, color2, ratio):
        """Interpolate between two hex colors."""
        if ratio < 0.5:
            return color1
        else:
            return color2


class ProfessionalInput(tk.Entry):
    """Professional input field with modern styling."""
    
    def __init__(self, parent, placeholder="", width=200, **kwargs):
        super().__init__(parent, width=width, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = "#64748b"
        self.focus_color = "#2563eb"
        self.default_border = "#334155"
        
        # Configure styling
        self.configure(
            relief="flat",
            bd=0,
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            selectbackground="#2563eb",
            selectforeground="#ffffff"
        )
        
        # Bind events
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<KeyRelease>", self._on_key_release)
        
        # Set placeholder
        if self.placeholder:
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
            self.placeholder_active = True
        else:
            self.placeholder_active = False
    
    def _on_focus_in(self, event):
        """Handle focus in event."""
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(fg="#f8fafc")
            self.placeholder_active = False
        
        # Change border color
        self.configure(relief="solid", bd=2, highlightbackground=self.focus_color)
    
    def _on_focus_out(self, event):
        """Handle focus out event."""
        # Reset border
        self.configure(relief="flat", bd=0, highlightbackground="")
        
        # Check if empty and restore placeholder
        if not self.get() and self.placeholder:
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
            self.placeholder_active = True
    
    def _on_key_release(self, event):
        """Handle key release event."""
        if self.placeholder_active:
            return
        
        # Remove placeholder if user types
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.placeholder_active = False


class ProfessionalDropdown(tk.Frame):
    """Professional dropdown with modern styling."""
    
    def __init__(self, parent, options=None, default=None, width=150, **kwargs):
        super().__init__(parent, width=width, **kwargs)
        
        self.options = options or []
        self.default = default
        self.width = width
        self.is_open = False
        
        # Configure frame
        self.configure(relief="flat", bd=0)
        
        # Create dropdown button
        self.button = tk.Button(
            self, text=default or "Select...",
            relief="flat", bd=0,
            bg="#1e293b", fg="#f8fafc",
            font=("Segoe UI", 11),
            cursor="hand2"
        )
        self.button.pack(fill="x", padx=1, pady=1)
        
        # Create dropdown list
        self.listbox = tk.Listbox(
            self, relief="flat", bd=0,
            bg="#1e293b", fg="#f8fafc",
            font=("Segoe UI", 11),
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            highlightthickness=0
        )
        
        # Bind events
        self.button.bind("<Button-1>", self._toggle_dropdown)
        self.listbox.bind("<Double-Button-1>", self._select_option)
        
        # Populate options
        self._populate_options()
    
    def _populate_options(self):
        """Populate dropdown with options."""
        for option in self.options:
            self.listbox.insert(tk.END, option)
    
    def _toggle_dropdown(self, event):
        """Toggle dropdown visibility."""
        if self.is_open:
            self.listbox.pack_forget()
            self.is_open = False
        else:
            self.listbox.pack(fill="x", padx=1)
            self.is_open = True
    
    def _select_option(self, event):
        """Handle option selection."""
        selection = self.listbox.curselection()
        if selection:
            selected = self.listbox.get(selection[0])
            self.button.config(text=selected)
            self._toggle_dropdown(None)
    
    def get(self):
        """Get selected value."""
        return self.button.cget("text")
    
    def set(self, value):
        """Set selected value."""
        if value in self.options:
            self.button.config(text=value)


class ProfessionalToggle(tk.Frame):
    """Professional toggle switch with smooth animation."""
    
    def __init__(self, parent, text="", default=False, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.text = text
        self.state = default
        self.width = 50
        self.height = 24
        
        # Configure frame
        self.configure(relief="flat", bd=0)
        
        # Create toggle canvas
        self.canvas = tk.Canvas(
            self, width=self.width, height=self.height,
            highlightthickness=0
        )
        self.canvas.pack(side="left")
        
        # Create label
        if self.text:
            self.label = tk.Label(
                self, text=self.text,
                bg="#0f172a", fg="#f8fafc",
                font=("Segoe UI", 11)
            )
            self.label.pack(side="left", padx=(10, 0))
        
        # Bind events
        self.canvas.bind("<Button-1>", self._toggle)
        
        # Create the toggle
        self._create_toggle()
    
    def _create_toggle(self):
        """Create the toggle switch appearance."""
        # Clear canvas
        self.canvas.delete("all")
        
        # Colors
        bg_color = "#2563eb" if self.state else "#64748b"
        circle_color = "#ffffff"
        
        # Draw background
        self.canvas.create_rounded_rectangle(
            0, 0, self.width, self.height,
            radius=self.height // 2,
            fill=bg_color, outline="",
            width=0
        )
        
        # Draw circle
        circle_x = self.width - self.height // 2 - 2 if self.state else self.height // 2 + 2
        self.canvas.create_oval(
            circle_x - self.height // 2 + 2,
            2,
            circle_x + self.height // 2 - 2,
            self.height - 2,
            fill=circle_color, outline="",
            width=0
        )
    
    def _toggle(self, event):
        """Toggle the switch state."""
        self.state = not self.state
        self._create_toggle()
    
    def get(self):
        """Get toggle state."""
        return self.state
    
    def set(self, state):
        """Set toggle state."""
        self.state = state
        self._create_toggle()


# Add rounded rectangle method to Canvas
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
    """Create a rounded rectangle on the canvas."""
    # Create rounded rectangle path
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    
    return self.create_polygon(points, smooth=True, **kwargs)

# Monkey patch Canvas class
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle
