#!/usr/bin/env python3
"""
Professional UI Demo for Nexlify Engine.

This demo showcases the beautiful, custom-designed UI components
with gradients, shadows, and professional aesthetics.
"""

import sys
import os
from pathlib import Path

# Add the src/gui/design_system directory to the path
design_path = Path(__file__).parent / "src" / "gui" / "design_system"
sys.path.insert(0, str(design_path))

import tkinter as tk
from tkinter import ttk
from professional_theme import ProfessionalTheme, ColorScheme, ButtonStyle
from professional_components import (
    ProfessionalButton, ProfessionalPanel, ProfessionalHeader,
    ProfessionalInput, ProfessionalDropdown, ProfessionalToggle
)


class ProfessionalUIDemo:
    """Demo application showcasing professional UI components."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nexlify Engine - Professional UI Demo")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0f172a")
        
        # Initialize theme
        self.theme = ProfessionalTheme(ColorScheme.DARK_PRO)
        self.root.theme = self.theme  # Make theme accessible to components
        
        # Create the demo
        self._create_demo()
        
        # Center the window
        self._center_window()
    
    def _center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_demo(self):
        """Create the demo interface."""
        # Create main header
        header = ProfessionalHeader(
            self.root, 
            title="Nexlify Engine - Professional UI Demo",
            width=1200, 
            height=80
        )
        header.pack(fill="x", pady=(0, 20))
        
        # Create main content frame
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create left panel for controls
        self._create_controls_panel(main_frame)
        
        # Create right panel for component showcase
        self._create_showcase_panel(main_frame)
    
    def _create_controls_panel(self, parent):
        """Create the controls panel."""
        # Left panel
        left_frame = tk.Frame(parent, bg="#0f172a")
        left_frame.pack(side="left", fill="y", padx=(0, 20))
        
        # Theme selector
        theme_label = tk.Label(
            left_frame, 
            text="Theme Selection", 
            font=("Segoe UI", 14, "bold"),
            bg="#0f172a", fg="#f8fafc"
        )
        theme_label.pack(pady=(0, 10))
        
        # Theme buttons
        themes_frame = tk.Frame(left_frame, bg="#0f172a")
        themes_frame.pack(fill="x", pady=(0, 20))
        
        theme_buttons = [
            ("Dark Pro", ColorScheme.DARK_PRO),
            ("Dark Neon", ColorScheme.DARK_NEON),
            ("Gaming", ColorScheme.GAMING)
        ]
        
        for text, scheme in theme_buttons:
            btn = ProfessionalButton(
                themes_frame, 
                text=text,
                command=lambda s=scheme: self._change_theme(s),
                style_type="secondary",
                width=100, height=35
            )
            btn.pack(pady=2)
        
        # Component controls
        controls_label = tk.Label(
            left_frame, 
            text="Component Controls", 
            font=("Segoe UI", 14, "bold"),
            bg="#0f172a", fg="#f8fafc"
        )
        controls_label.pack(pady=(20, 10))
        
        # Input field
        self.input_field = ProfessionalInput(
            left_frame, 
            placeholder="Enter text here...",
            width=200
        )
        self.input_field.pack(pady=(0, 10))
        
        # Dropdown
        self.dropdown = ProfessionalDropdown(
            left_frame,
            options=["Option 1", "Option 2", "Option 3", "Custom Option"],
            default="Select an option",
            width=200
        )
        self.dropdown.pack(pady=(0, 10))
        
        # Toggle
        self.toggle = ProfessionalToggle(
            left_frame,
            text="Enable Feature",
            default=False
        )
        self.toggle.pack(pady=(0, 20))
        
        # Action buttons
        actions_label = tk.Label(
            left_frame, 
            text="Actions", 
            font=("Segoe UI", 14, "bold"),
            bg="#0f172a", fg="#f8fafc"
        )
        actions_label.pack(pady=(20, 10))
        
        # Primary button
        primary_btn = ProfessionalButton(
            left_frame,
            text="Primary Action",
            command=self._primary_action,
            style_type="primary",
            width=200, height=40
        )
        primary_btn.pack(pady=(0, 10))
        
        # Success button
        success_btn = ProfessionalButton(
            left_frame,
            text="Success Action",
            command=self._success_action,
            style_type="success",
            width=200, height=40
        )
        success_btn.pack(pady=(0, 10))
        
        # Danger button
        danger_btn = ProfessionalButton(
            left_frame,
            text="Danger Action",
            command=self._danger_action,
            style_type="danger",
            width=200, height=40
        )
        danger_btn.pack(pady=(0, 10))
    
    def _create_showcase_panel(self, parent):
        """Create the component showcase panel."""
        # Right panel
        right_frame = tk.Frame(parent, bg="#0f172a")
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Showcase title
        showcase_title = tk.Label(
            right_frame,
            text="Component Showcase",
            font=("Segoe UI", 18, "bold"),
            bg="#0f172a", fg="#f8fafc"
        )
        showcase_title.pack(pady=(0, 20))
        
        # Create showcase grid
        self._create_showcase_grid(right_frame)
    
    def _create_showcase_grid(self, parent):
        """Create a grid of component showcases."""
        # Grid frame
        grid_frame = tk.Frame(parent, bg="#0f172a")
        grid_frame.pack(fill="both", expand=True)
        
        # Configure grid weights
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        grid_frame.rowconfigure(1, weight=1)
        
        # Panel 1: Buttons showcase
        buttons_panel = ProfessionalPanel(
            grid_frame,
            title="Professional Buttons",
            width=280, height=200
        )
        buttons_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Add button examples to panel
        self._add_button_examples(buttons_panel)
        
        # Panel 2: Inputs showcase
        inputs_panel = ProfessionalPanel(
            grid_frame,
            title="Professional Inputs",
            width=280, height=200
        )
        inputs_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Add input examples to panel
        self._add_input_examples(inputs_panel)
        
        # Panel 3: Controls showcase
        controls_panel = ProfessionalPanel(
            grid_frame,
            title="Professional Controls",
            width=280, height=200
        )
        controls_panel.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Add control examples to panel
        self._add_control_examples(controls_panel)
        
        # Panel 4: Theme info
        theme_panel = ProfessionalPanel(
            grid_frame,
            title="Theme Information",
            width=280, height=200
        )
        theme_panel.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Add theme info to panel
        self._add_theme_info(theme_panel)
    
    def _add_button_examples(self, panel):
        """Add button examples to the panel."""
        # Create a frame inside the panel for content
        content_frame = tk.Frame(panel, bg="#1e293b")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Small buttons
        small_frame = tk.Frame(content_frame, bg="#1e293b")
        small_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            small_frame, 
            text="Small:", 
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#f8fafc"
        ).pack(side="left")
        
        ProfessionalButton(
            small_frame,
            text="Small",
            style_type="primary",
            width=60, height=25
        ).pack(side="right")
        
        # Medium buttons
        medium_frame = tk.Frame(content_frame, bg="#1e293b")
        medium_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            medium_frame, 
            text="Medium:", 
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#f8fafc"
        ).pack(side="left")
        
        ProfessionalButton(
            medium_frame,
            text="Medium",
            style_type="secondary",
            width=80, height=30
        ).pack(side="right")
        
        # Large buttons
        large_frame = tk.Frame(content_frame, bg="#1e293b")
        large_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            large_frame, 
            text="Large:", 
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#f8fafc"
        ).pack(side="left")
        
        ProfessionalButton(
            large_frame,
            text="Large",
            style_type="primary",
            width=100, height=35
        ).pack(side="right")
    
    def _add_input_examples(self, panel):
        """Add input examples to the panel."""
        # Create a frame inside the panel for content
        content_frame = tk.Frame(panel, bg="#1e293b")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Text input
        tk.Label(
            content_frame, 
            text="Text Input:", 
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#f8fafc"
        ).pack(anchor="w", pady=(0, 5))
        
        ProfessionalInput(
            content_frame,
            placeholder="Enter text...",
            width=200
        ).pack(fill="x", pady=(0, 15))
        
        # Dropdown
        tk.Label(
            content_frame, 
            text="Dropdown:", 
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#f8fafc"
        ).pack(anchor="w", pady=(0, 5))
        
        ProfessionalDropdown(
            content_frame,
            options=["Choice A", "Choice B", "Choice C"],
            default="Make a choice",
            width=200
        ).pack(fill="x", pady=(0, 15))
        
        # Toggle
        tk.Label(
            content_frame, 
            text="Toggle Switch:", 
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#f8fafc"
        ).pack(anchor="w", pady=(0, 5))
        
        ProfessionalToggle(
            content_frame,
            text="Enable Feature",
            default=True
        ).pack(anchor="w")
    
    def _add_control_examples(self, panel):
        """Add control examples to the panel."""
        # Create a frame inside the panel for content
        content_frame = tk.Frame(panel, bg="#1e293b")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Color scheme info
        tk.Label(
            content_frame, 
            text=f"Current Theme: {self.theme.scheme.value.replace('_', ' ').title()}", 
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b", fg="#f8fafc"
        ).pack(anchor="w", pady=(0, 10))
        
        # Primary color
        color_frame = tk.Frame(content_frame, bg="#1e293b")
        color_frame.pack(fill="x", pady=2)
        
        tk.Label(
            color_frame, 
            text="Primary:", 
            font=("Segoe UI", 9),
            bg="#1e293b", fg="#f8fafc"
        ).pack(side="left")
        
        color_box = tk.Frame(
            color_frame, 
            bg=self.theme.color_palette.primary,
            width=20, height=20
        )
        color_box.pack(side="right")
        
        # Accent color
        accent_frame = tk.Frame(content_frame, bg="#1e293b")
        accent_frame.pack(fill="x", pady=2)
        
        tk.Label(
            accent_frame, 
            text="Accent:", 
            font=("Segoe UI", 9),
            bg="#1e293b", fg="#f8fafc"
        ).pack(side="left")
        
        accent_box = tk.Frame(
            accent_frame, 
            bg=self.theme.color_palette.accent,
            width=20, height=20
        )
        accent_box.pack(side="right")
        
        # Background color
        bg_frame = tk.Frame(content_frame, bg="#1e293b")
        bg_frame.pack(fill="x", pady=2)
        
        tk.Label(
            bg_frame, 
            text="Background:", 
            font=("Segoe UI", 9),
            bg="#1e293b", fg="#f8fafc"
        ).pack(side="left")
        
        bg_box = tk.Frame(
            bg_frame, 
            bg=self.theme.color_palette.background,
            width=20, height=20
        )
        bg_box.pack(side="right")
    
    def _add_theme_info(self, panel):
        """Add theme information to the panel."""
        # Create a frame inside the panel for content
        content_frame = tk.Frame(panel, bg="#1e293b")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Theme details
        info_text = f"""
Theme: {self.theme.scheme.value.replace('_', ' ').title()}

Colors: {len(self.theme.color_palette.__dict__)} defined
Gradients: {len(self.theme.gradients)} available
Shadows: {len(self.theme.shadows)} styles
Border Radius: {len(self.theme.border_radius)} options
Spacing: {len(self.theme.spacing)} scales
Typography: {len(self.theme.typography)} styles

Animation Timing:
• Fast: {self.theme.get_animation_timing()['fast']}
• Normal: {self.theme.get_animation_timing()['normal']}
• Slow: {self.theme.get_animation_timing()['slow']}
        """
        
        info_label = tk.Label(
            content_frame,
            text=info_text,
            font=("Segoe UI", 9),
            bg="#1e293b", fg="#f8fafc",
            justify="left",
            anchor="nw"
        )
        info_label.pack(fill="both", expand=True)
    
    def _change_theme(self, scheme):
        """Change the current theme."""
        self.theme = ProfessionalTheme(scheme)
        self.root.theme = self.theme
        
        # Update the demo
        self.root.destroy()
        self.__init__()
    
    def _primary_action(self):
        """Handle primary action button click."""
        print("🎯 Primary action triggered!")
        # You could show a notification or update the UI here
    
    def _success_action(self):
        """Handle success action button click."""
        print("✅ Success action triggered!")
        # You could show a success message or update the UI here
    
    def _danger_action(self):
        """Handle danger action button click."""
        print("⚠️ Danger action triggered!")
        # You could show a confirmation dialog or update the UI here
    
    def run(self):
        """Run the demo application."""
        self.root.mainloop()


def main():
    """Main function to run the demo."""
    print("🚀 Starting Professional UI Demo...")
    print("✨ Showcasing beautiful, custom-designed UI components")
    print("🎨 With gradients, shadows, and professional aesthetics")
    print("=" * 60)
    
    try:
        demo = ProfessionalUIDemo()
        demo.run()
    except Exception as e:
        print(f"❌ Demo failed to start: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
