"""
Spacing documentation generator for automatic documentation creation.

This module provides tools to:
- Generate spacing system documentation
- Create spacing guidelines
- Generate code examples
- Create visual spacing charts
- Export documentation in various formats
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import os
import logging

from ..responsive import responsive_spacing_manager, Breakpoint
from ..design_system.spacing_system import spacing, SpacingUnit
from ..design_system.typography_system import typography, FontSize, FontWeight
from ..design_system.alignment_system import alignment, HorizontalAlignment

logger = logging.getLogger(__name__)


class SpacingDocumentationGenerator:
    """Generates comprehensive documentation for the spacing system."""
    
    def __init__(self):
        self.documentation_data: Dict[str, Any] = {}
        self.generated_files: List[str] = []
        
        # Documentation settings
        self.include_code_examples = True
        self.include_visual_charts = True
        self.include_responsive_examples = True
        self.include_best_practices = True
        
        logger.info("SpacingDocumentationGenerator initialized")
    
    def generate_complete_documentation(self, output_dir: str = "docs/spacing") -> Dict[str, Any]:
        """Generate complete spacing system documentation.
        
        Args:
            output_dir: Directory to output documentation files
            
        Returns:
            Dictionary containing generation results
        """
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Collect all documentation data
            self._collect_documentation_data()
            
            # Generate different documentation formats
            results = {
                'markdown': self._generate_markdown_documentation(output_dir),
                'html': self._generate_html_documentation(output_dir),
                'json': self._generate_json_documentation(output_dir),
                'pdf': self._generate_pdf_documentation(output_dir)
            }
            
            # Generate summary
            summary = self._generate_documentation_summary(results)
            
            logger.info(f"Generated complete documentation in {output_dir}")
            return {
                'output_directory': output_dir,
                'files_generated': self.generated_files,
                'formats': results,
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate complete documentation: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _collect_documentation_data(self):
        """Collect all data needed for documentation generation."""
        try:
            # Spacing system data
            self.documentation_data['spacing_system'] = {
                'base_units': {
                    'xs': spacing.xs,
                    'sm': spacing.sm,
                    'md': spacing.md,
                    'lg': spacing.lg,
                    'xl': spacing.xl,
                    'xxl': spacing.xxl
                },
                'special_units': {
                    'button_height': spacing.button_height,
                    'tree_indent': spacing.tree_indent,
                    'selection_padding': spacing.selection_padding
                },
                'utility_functions': [
                    'get_panel_spacing()',
                    'get_section_spacing()',
                    'get_item_spacing()',
                    'get_margin()',
                    'get_padding()'
                ]
            }
            
            # Typography system data
            self.documentation_data['typography_system'] = {
                'font_sizes': {
                    'xs': typography.xs,
                    'sm': typography.sm,
                    'md': typography.md,
                    'lg': typography.lg,
                    'xl': typography.xl,
                    'xxl': typography.xxl
                },
                'font_weights': {
                    'light': typography.light,
                    'normal': typography.normal,
                    'medium': typography.medium,
                    'bold': typography.bold
                },
                'line_heights': {
                    'tight': typography.line_height_tight,
                    'normal': typography.line_height_normal,
                    'relaxed': typography.line_height_relaxed
                }
            }
            
            # Alignment system data
            self.documentation_data['alignment_system'] = {
                'horizontal_alignments': [
                    'LEFT', 'CENTER', 'RIGHT', 'JUSTIFY'
                ],
                'vertical_alignments': [
                    'TOP', 'MIDDLE', 'BOTTOM', 'BASELINE'
                ],
                'utility_functions': [
                    'get_alignment_class()',
                    'apply_alignment()',
                    'get_text_alignment()'
                ]
            }
            
            # Responsive system data
            self.documentation_data['responsive_system'] = {
                'breakpoints': [
                    {'name': 'Mobile', 'width': 480, 'multiplier': 0.75},
                    {'name': 'Tablet', 'width': 768, 'multiplier': 0.875},
                    {'name': 'Desktop', 'width': 1024, 'multiplier': 1.0},
                    {'name': 'Widescreen', 'width': 1440, 'multiplier': 1.125}
                ],
                'features': [
                    'Breakpoint detection',
                    'Responsive spacing calculation',
                    'Touch-friendly adjustments',
                    'High-DPI scaling'
                ]
            }
            
            # Animation system data
            self.documentation_data['animation_system'] = {
                'animation_types': [
                    'SPACING_CHANGE',
                    'MARGIN_CHANGE',
                    'PADDING_CHANGE',
                    'LAYOUT_CHANGE'
                ],
                'easing_types': [
                    'LINEAR',
                    'EASE_IN',
                    'EASE_OUT',
                    'EASE_IN_OUT',
                    'BOUNCE',
                    'ELASTIC'
                ],
                'features': [
                    'Smooth transitions',
                    'Keyframe animations',
                    'Animation groups',
                    'Performance optimization'
                ]
            }
            
            # Best practices
            self.documentation_data['best_practices'] = [
                'Use consistent spacing units throughout the application',
                'Apply responsive spacing for different screen sizes',
                'Maintain visual hierarchy with proper spacing',
                'Use animation sparingly to avoid distraction',
                'Test spacing on different devices and resolutions',
                'Follow the 8px grid system for consistency',
                'Use semantic spacing names (sm, md, lg) rather than pixel values',
                'Implement touch-friendly spacing for mobile devices'
            ]
            
            # Code examples
            self.documentation_data['code_examples'] = {
                'basic_spacing': self._generate_basic_spacing_example(),
                'responsive_spacing': self._generate_responsive_spacing_example(),
                'animation_example': self._generate_animation_example(),
                'panel_integration': self._generate_panel_integration_example()
            }
            
            logger.info("Collected comprehensive documentation data")
            
        except Exception as e:
            logger.error(f"Failed to collect documentation data: {e}")
    
    def _generate_markdown_documentation(self, output_dir: str) -> str:
        """Generate Markdown documentation.
        
        Args:
            output_dir: Output directory
            
        Returns:
            Path to generated markdown file
        """
        try:
            markdown_content = []
            
            # Title and overview
            markdown_content.extend([
                "# UI Spacing & Alignment System Documentation",
                "",
                f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
                "",
                "## Table of Contents",
                "",
                "1. [Overview](#overview)",
                "2. [Spacing System](#spacing-system)",
                "3. [Typography System](#typography-system)",
                "4. [Alignment System](#alignment-system)",
                "5. [Responsive System](#responsive-system)",
                "6. [Animation System](#animation-system)",
                "7. [Best Practices](#best-practices)",
                "8. [Code Examples](#code-examples)",
                "9. [Integration Guide](#integration-guide)",
                "",
                "---",
                ""
            ])
            
            # Overview
            markdown_content.extend([
                "## Overview",
                "",
                "The UI Spacing & Alignment System provides a comprehensive framework for maintaining consistent visual hierarchy and professional appearance across all UI components in the Nexlify application.",
                "",
                "### Key Features",
                "",
                "- **Consistent Spacing**: Standardized spacing units and utilities",
                "- **Responsive Design**: Automatic spacing adjustments for different screen sizes",
                "- **Animation Support**: Smooth transitions and spacing animations",
                "- **Professional Appearance**: Industry-standard spacing practices",
                "- **Developer Friendly**: Easy-to-use API and comprehensive documentation",
                "",
                "---",
                ""
            ])
            
            # Spacing System
            markdown_content.extend([
                "## Spacing System",
                "",
                "### Base Spacing Units",
                "",
                "| Unit | Size | Use Case |",
                "|------|------|----------|"
            ])
            
            for unit, size in self.documentation_data['spacing_system']['base_units'].items():
                markdown_content.append(f"| {unit.upper()} | {size}px | {self._get_spacing_use_case(unit)} |")
            
            markdown_content.extend([
                "",
                "### Special Spacing Units",
                "",
                "| Unit | Size | Description |",
                "|------|------|-------------|"
            ])
            
            for unit, size in self.documentation_data['spacing_system']['special_units'].items():
                markdown_content.append(f"| {unit.replace('_', ' ').title()} | {size}px | {self._get_special_spacing_description(unit)} |")
            
            markdown_content.extend([
                "",
                "### Utility Functions",
                "",
                "```python",
                "from src.gui.design_system.spacing_system import spacing",
                "",
                "# Get panel spacing (margin, padding)",
                "margin, padding = spacing.get_panel_spacing()",
                "",
                "# Get section spacing",
                "section_spacing = spacing.get_section_spacing()",
                "",
                "# Get item spacing",
                "item_spacing = spacing.get_item_spacing()",
                "```",
                "",
                "---",
                ""
            ])
            
            # Typography System
            markdown_content.extend([
                "## Typography System",
                "",
                "### Font Sizes",
                "",
                "| Size | Pixels | Use Case |",
                "|------|--------|----------|"
            ])
            
            for size, pixels in self.documentation_data['typography_system']['font_sizes'].items():
                markdown_content.append(f"| {size.upper()} | {pixels}px | {self._get_font_size_use_case(size)} |")
            
            markdown_content.extend([
                "",
                "### Font Weights",
                "",
                "| Weight | Value | Use Case |",
                "|--------|-------|----------|"
            ])
            
            for weight, value in self.documentation_data['typography_system']['font_weights'].items():
                markdown_content.append(f"| {weight.title()} | {value} | {self._get_font_weight_use_case(weight)} |")
            
            markdown_content.extend([
                "",
                "---",
                ""
            ])
            
            # Responsive System
            markdown_content.extend([
                "## Responsive System",
                "",
                "### Breakpoints",
                "",
                "| Breakpoint | Width | Multiplier | Description |",
                "|------------|-------|------------|-------------|"
            ])
            
            for bp in self.documentation_data['responsive_system']['breakpoints']:
                markdown_content.append(f"| {bp['name']} | {bp['width']}px | {bp['multiplier']}x | {self._get_breakpoint_description(bp)} |")
            
            markdown_content.extend([
                "",
                "### Usage Example",
                "",
                "```python",
                "from src.gui.responsive import responsive_spacing_manager",
                "",
                "# Get responsive spacing for current breakpoint",
                "responsive_spacing = responsive_spacing_manager.get_responsive_spacing(spacing.md)",
                "",
                "# Check current breakpoint",
                "current_breakpoint = responsive_spacing_manager.get_current_breakpoint()",
                "print(f'Current breakpoint: {current_breakpoint.value}')",
                "```",
                "",
                "---",
                ""
            ])
            
            # Best Practices
            markdown_content.extend([
                "## Best Practices",
                "",
                "### Spacing Guidelines",
                ""
            ])
            
            for i, practice in enumerate(self.documentation_data['best_practices'], 1):
                markdown_content.append(f"{i}. {practice}")
            
            markdown_content.extend([
                "",
                "---",
                ""
            ])
            
            # Code Examples
            markdown_content.extend([
                "## Code Examples",
                "",
                "### Basic Spacing Usage",
                "",
                "```python",
                self.documentation_data['code_examples']['basic_spacing'],
                "```",
                "",
                "### Responsive Spacing Integration",
                "",
                "```python",
                self.documentation_data['code_examples']['responsive_spacing'],
                "```",
                "",
                "### Animation Integration",
                "",
                "```python",
                self.documentation_data['code_examples']['animation_example'],
                "```",
                "",
                "---",
                ""
            ])
            
            # Integration Guide
            markdown_content.extend([
                "## Integration Guide",
                "",
                "### Adding to Existing Panels",
                "",
                "1. Import responsive spacing manager",
                "2. Connect to breakpoint changes",
                "3. Implement responsive spacing methods",
                "4. Test on different screen sizes",
                "",
                "### Testing Your Implementation",
                "",
                "1. Use the spacing validator to check consistency",
                "2. Test responsive behavior by resizing the window",
                "3. Verify spacing matches design system specifications",
                "4. Check for visual alignment issues",
                "",
                "---",
                "",
                "*This documentation was automatically generated by the SpacingDocumentationGenerator.*"
            ])
            
            # Write to file
            markdown_file = os.path.join(output_dir, "spacing_system_documentation.md")
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(markdown_content))
            
            self.generated_files.append(markdown_file)
            logger.info(f"Generated Markdown documentation: {markdown_file}")
            
            return markdown_file
            
        except Exception as e:
            logger.error(f"Failed to generate Markdown documentation: {e}")
            return ""
    
    def _generate_html_documentation(self, output_dir: str) -> str:
        """Generate HTML documentation.
        
        Args:
            output_dir: Output directory
            
        Returns:
            Path to generated HTML file
        """
        try:
            # For now, we'll create a simple HTML version
            # In a full implementation, you'd use a proper HTML template engine
            
            html_content = [
                "<!DOCTYPE html>",
                "<html lang='en'>",
                "<head>",
                "    <meta charset='UTF-8'>",
                "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
                "    <title>UI Spacing System Documentation</title>",
                "    <style>",
                "        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }",
                "        .container { max-width: 1200px; margin: 0 auto; }",
                "        table { border-collapse: collapse; width: 100%; margin: 20px 0; }",
                "        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }",
                "        th { background-color: #f2f2f2; }",
                "        code { background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }",
                "        pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }",
                "        .section { margin: 40px 0; }",
                "        h1 { color: #333; border-bottom: 3px solid #0078d4; padding-bottom: 10px; }",
                "        h2 { color: #555; border-bottom: 2px solid #ddd; padding-bottom: 8px; }",
                "        h3 { color: #666; }",
                "    </style>",
                "</head>",
                "<body>",
                "    <div class='container'>",
                f"        <h1>UI Spacing System Documentation</h1>",
                f"        <p><em>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>",
                "",
                "        <div class='section'>",
                "            <h2>Overview</h2>",
                "            <p>The UI Spacing & Alignment System provides a comprehensive framework for maintaining consistent visual hierarchy and professional appearance across all UI components.</p>",
                "        </div>",
                "",
                "        <div class='section'>",
                "            <h2>Spacing Units</h2>",
                "            <table>",
                "                <tr><th>Unit</th><th>Size</th><th>Use Case</th></tr>"
            ]
            
            # Add spacing units table
            for unit, size in self.documentation_data['spacing_system']['base_units'].items():
                html_content.append(f"                <tr><td><code>{unit.upper()}</code></td><td>{size}px</td><td>{self._get_spacing_use_case(unit)}</td></tr>")
            
            html_content.extend([
                "            </table>",
                "        </div>",
                "",
                "        <div class='section'>",
                "            <h2>Code Examples</h2>",
                "            <h3>Basic Usage</h3>",
                "            <pre><code>",
                self.documentation_data['code_examples']['basic_spacing'].replace('<', '&lt;').replace('>', '&gt;'),
                "            </code></pre>",
                "        </div>",
                "",
                "        <div class='section'>",
                "            <h2>Best Practices</h2>",
                "            <ul>"
            ])
            
            for practice in self.documentation_data['best_practices']:
                html_content.append(f"                <li>{practice}</li>")
            
            html_content.extend([
                "            </ul>",
                "        </div>",
                "    </div>",
                "</body>",
                "</html>"
            ])
            
            # Write to file
            html_file = os.path.join(output_dir, "spacing_system_documentation.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(html_content))
            
            self.generated_files.append(html_file)
            logger.info(f"Generated HTML documentation: {html_file}")
            
            return html_file
            
        except Exception as e:
            logger.error(f"Failed to generate HTML documentation: {e}")
            return ""
    
    def _generate_json_documentation(self, output_dir: str) -> str:
        """Generate JSON documentation.
        
        Args:
            output_dir: Output directory
            
        Returns:
            Path to generated JSON file
        """
        try:
            json_file = os.path.join(output_dir, "spacing_system_documentation.json")
            
            # Add metadata
            documentation_with_metadata = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'version': '1.0.0',
                    'generator': 'SpacingDocumentationGenerator'
                },
                'content': self.documentation_data
            }
            
            import json
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(documentation_with_metadata, f, indent=2, default=str)
            
            self.generated_files.append(json_file)
            logger.info(f"Generated JSON documentation: {json_file}")
            
            return json_file
            
        except Exception as e:
            logger.error(f"Failed to generate JSON documentation: {e}")
            return ""
    
    def _generate_pdf_documentation(self, output_dir: str) -> str:
        """Generate PDF documentation.
        
        Args:
            output_dir: Output directory
            
        Returns:
            Path to generated PDF file
        """
        try:
            # For now, we'll just note that PDF generation would be implemented
            # In a full implementation, you'd use a library like reportlab or weasyprint
            
            pdf_file = os.path.join(output_dir, "spacing_system_documentation.pdf")
            
            # Create a placeholder note
            note_file = os.path.join(output_dir, "pdf_generation_note.txt")
            with open(note_file, 'w', encoding='utf-8') as f:
                f.write("PDF generation would be implemented here using a library like reportlab or weasyprint.\n")
                f.write("The markdown and HTML versions provide the same content in different formats.\n")
            
            logger.info("PDF generation note created (PDF generation not yet implemented)")
            
            return pdf_file
            
        except Exception as e:
            logger.error(f"Failed to generate PDF documentation: {e}")
            return ""
    
    def _generate_documentation_summary(self, results: Dict[str, str]) -> Dict[str, Any]:
        """Generate a summary of documentation generation results.
        
        Args:
            results: Results from documentation generation
            
        Returns:
            Summary dictionary
        """
        try:
            summary = {
                'total_files': len(self.generated_files),
                'formats_generated': len([r for r in results.values() if r]),
                'success_rate': len([r for r in results.values() if r]) / len(results) * 100,
                'file_types': list(set([os.path.splitext(f)[1] for f in self.generated_files])),
                'total_size': sum([os.path.getsize(f) for f in self.generated_files if os.path.exists(f)]),
                'generation_time': datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate documentation summary: {e}")
            return {'error': str(e)}
    
    def _get_spacing_use_case(self, unit: str) -> str:
        """Get use case description for a spacing unit.
        
        Args:
            unit: Spacing unit name
            
        Returns:
            Use case description
        """
        use_cases = {
            'xs': 'Very small gaps, fine details',
            'sm': 'Small gaps, tight layouts',
            'md': 'Standard spacing, general use',
            'lg': 'Large gaps, breathing room',
            'xl': 'Extra large gaps, major sections',
            'xxl': 'Maximum gaps, page-level spacing'
        }
        return use_cases.get(unit, 'General use')
    
    def _get_special_spacing_description(self, unit: str) -> str:
        """Get description for special spacing units.
        
        Args:
            unit: Special spacing unit name
            
        Returns:
            Description
        """
        descriptions = {
            'button_height': 'Standard height for buttons',
            'tree_indent': 'Indentation for tree view items',
            'selection_padding': 'Padding for selected items'
        }
        return descriptions.get(unit, 'Specialized spacing unit')
    
    def _get_font_size_use_case(self, size: str) -> str:
        """Get use case for font sizes.
        
        Args:
            size: Font size name
            
        Returns:
            Use case description
        """
        use_cases = {
            'xs': 'Captions, fine print',
            'sm': 'Small text, secondary information',
            'md': 'Body text, general content',
            'lg': 'Subheadings, emphasis',
            'xl': 'Headings, titles',
            'xxl': 'Main titles, hero text'
        }
        return use_cases.get(size, 'General text')
    
    def _get_font_weight_use_case(self, weight: str) -> str:
        """Get use case for font weights.
        
        Args:
            weight: Font weight name
            
        Returns:
            Use case description
        """
        use_cases = {
            'light': 'Subtle text, secondary information',
            'normal': 'Body text, general content',
            'medium': 'Emphasis, subheadings',
            'bold': 'Headings, important text'
        }
        return use_cases.get(weight, 'General text')
    
    def _get_breakpoint_description(self, breakpoint: Dict[str, Any]) -> str:
        """Get description for a breakpoint.
        
        Args:
            breakpoint: Breakpoint data
            
        Returns:
            Description
        """
        descriptions = {
            'Mobile': 'Small screens, touch-friendly spacing',
            'Tablet': 'Medium screens, balanced spacing',
            'Desktop': 'Standard screens, normal spacing',
            'Widescreen': 'Large screens, generous spacing'
        }
        return descriptions.get(breakpoint['name'], 'Standard spacing')
    
    def _generate_basic_spacing_example(self) -> str:
        """Generate basic spacing usage example.
        
        Returns:
            Code example string
        """
        return '''from src.gui.design_system.spacing_system import spacing

# Apply spacing to a layout
layout = QVBoxLayout()
layout.setContentsMargins(spacing.md, spacing.md, spacing.md, spacing.md)
layout.setSpacing(spacing.sm)

# Use spacing in styling
widget.setStyleSheet(f"""
    QWidget {{
        padding: {spacing.sm}px;
        margin: {spacing.xs}px;
    }}
""")'''
    
    def _generate_responsive_spacing_example(self) -> str:
        """Generate responsive spacing example.
        
        Returns:
            Code example string
        """
        return '''from src.gui.responsive import responsive_spacing_manager

class MyPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Connect to responsive spacing changes
        responsive_spacing_manager.connect_breakpoint_changed(self.on_breakpoint_changed)
    
    def on_breakpoint_changed(self, breakpoint_name):
        # Update spacing based on new breakpoint
        responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.md)
        self.layout().setContentsMargins(responsive_margin, responsive_margin, 
                                       responsive_margin, responsive_margin)'''
    
    def _generate_animation_example(self) -> str:
        """Generate animation example.
        
        Returns:
            Code example string
        """
        return '''from src.gui.animations import spacing_animation_manager, EasingType

# Animate spacing change
animation = spacing_animation_manager.animate_spacing_change(
    widget=my_widget,
    start_spacing=8,
    end_spacing=16,
    duration=300,
    easing=EasingType.EASE_IN_OUT
)

# Animate margin change
margin_animation = spacing_animation_manager.animate_margin_change(
    widget=my_widget,
    start_margins=(8, 8, 8, 8),
    end_margins=(16, 16, 16, 16),
    duration=500,
    easing=EasingType.EASE_OUT
)'''
    
    def _generate_panel_integration_example(self) -> str:
        """Generate panel integration example.
        
        Returns:
            Code example string
        """
        return '''class MyPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_responsive_spacing()
    
    def setup_responsive_spacing(self):
        # Connect to responsive spacing manager
        responsive_spacing_manager.connect_breakpoint_changed(self.on_breakpoint_changed)
    
    def on_breakpoint_changed(self, breakpoint_name):
        self.update_responsive_spacing()
    
    def update_responsive_spacing(self):
        # Get responsive spacing values
        responsive_margin = responsive_spacing_manager.get_responsive_spacing(spacing.md)
        responsive_padding = responsive_spacing_manager.get_responsive_spacing(spacing.sm)
        
        # Update layout
        layout = self.layout()
        if layout:
            layout.setContentsMargins(responsive_margin, responsive_margin, 
                                   responsive_margin, responsive_margin)
            layout.setSpacing(responsive_padding)
        
        # Update styling
        self.apply_responsive_styling()
    
    def get_responsive_spacing(self, base_spacing, touch_friendly=False):
        return responsive_spacing_manager.get_responsive_spacing(base_spacing, touch_friendly)'''


# Global documentation generator instance
spacing_documentation_generator = SpacingDocumentationGenerator()
