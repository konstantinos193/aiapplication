# Nexlify Assets Directory

This directory contains assets for the Nexlify Engine application.

## Icons

### `nexlify_icon.svg` (256x256)
- **Full-featured icon** with text labels and animations
- Best for: Documentation, websites, high-resolution displays
- Features: 3D cube, AI neural network, animated particles, text labels

### `nexlify_icon_simple.svg` (128x128)
- **Simplified icon** optimized for application use
- Best for: Window icons, taskbar, file associations
- Features: Clean 3D cube, AI neural network, subtle animations

## Usage as Window Icon

### For GLFW Applications
```cpp
// In your editor_application.cpp
#include <GLFW/glfw3.h>

// Set window icon
GLFWimage icon;
icon.pixels = loadIconPixels("assets/nexlify_icon_simple.svg");
icon.width = 128;
icon.height = 128;
glfwSetWindowIcon(window_, 1, &icon);
```

### For Windows Applications
```cpp
// Set window icon using Windows API
HICON hIcon = LoadIcon(hInstance, "assets/nexlify_icon_simple.ico");
SetClassLongPtr(hwnd, GCLP_HICON, (LONG_PTR)hIcon);
```

## Converting SVG to ICO

To convert the SVG to ICO format for Windows:

1. **Online converter**: Use tools like convertio.co or cloudconvert.com
2. **Command line**: Use ImageMagick:
   ```bash
   magick convert nexlify_icon_simple.svg -define icon:auto-resize=16,32,48,64,128,256 nexlify_icon.ico
   ```
3. **GIMP/Photoshop**: Import SVG and export as ICO

## Icon Design Elements

- **3D Cube**: Represents the 3D game engine capabilities
- **Neural Network**: Symbolizes AI-powered features
- **Blue Gradient**: Modern, tech-focused color scheme
- **Rounded Corners**: Contemporary, friendly appearance
- **Subtle Animations**: Dynamic, engaging feel

## Recommended Sizes

- **16x16**: Taskbar icons
- **32x32**: File explorer, small displays
- **48x48**: Desktop shortcuts
- **128x128**: High-DPI displays
- **256x256**: Retina displays, documentation
