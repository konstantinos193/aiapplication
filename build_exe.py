#!/usr/bin/env python3
"""
Build script for creating Nexlify executable
"""
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def build_executable():
    """Build the Nexlify application executable"""
    print("🚀 Building Nexlify Executable...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyInstaller"], check=True)
    
    # Create build directory
    build_dir = Path("build_exe")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    print("📦 Running PyInstaller...")
    
    try:
        # Import PyInstaller and run it as a module
        import PyInstaller.__main__ as pyinstaller_main
        
        # PyInstaller arguments - EXCLUDING unnecessary heavy packages
        args = [
            "--onefile",                    # Single executable file
            "--windowed",                   # No console window (for GUI apps)
            "--name=Nexlify",               # Executable name
            "--icon=assets/nexlify_icon_simple.ico",  # Application icon
            "--add-data=assets;assets",     # Include assets folder
            "--add-data=config;config",     # Include config folder
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtWidgets", 
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=OpenGL",
            "--hidden-import=numpy",
            "--hidden-import=PIL",
            "--hidden-import=yaml",
            "--hidden-import=pydantic",
            # EXCLUDE heavy packages we don't need
            "--exclude-module=torch",
            "--exclude-module=matplotlib",
            "--exclude-module=scipy",
            "--exclude-module=pytest",
            "--exclude-module=click",
            "--exclude-module=rich",
            "--exclude-module=tqdm",
            "--exclude-module=auto-py-to-exe",
            "--exclude-module=Eel",
            "--exclude-module=bottle",
            "--exclude-module=gevent",
            "--exclude-module=lxml",
            "--exclude-module=jinja2",
            "--exclude-module=dateutil",
            "--exclude-module=certifi",
            "--exclude-module=charset-normalizer",
            "--exclude-module=idna",
            "--exclude-module=urllib3",
            "--exclude-module=requests",
            "--exclude-module=setuptools",
            "--exclude-module=wheel",
            "--exclude-module=pkg_resources",
            "--exclude-module=platformdirs",
            "--exclude-module=pycparser",
            "--exclude-module=cffi",
            "--exclude-module=greenlet",
            "--exclude-module=zope.event",
            "--exclude-module=zope.interface",
            "--exclude-module=pygments",
            "--exclude-module=markdown-it-py",
            "--exclude-module=mdurl",
            "--exclude-module=iniconfig",
            "--exclude-module=pluggy",
            "--exclude-module=packaging",
            "--exclude-module=pyparsing",
            "--exclude-module=importlib_resources",
            "--exclude-module=importlib_metadata",
            "--exclude-module=zipp",
            "--exclude-module=jaraco.functools",
            "--exclude-module=jaraco.text",
            "--exclude-module=jaraco.context",
            "--exclude-module=backports.tarfile",
            "--exclude-module=backports",
            "--exclude-module=typing_extensions",
            "--exclude-module=typing_inspection",
            "--exclude-module=annotated_types",
            "--exclude-module=pydantic_core",
            "--exclude-module=colorama",
            "--exclude-module=six",
            "--exclude-module=zoneinfo",
            "--exclude-module=OpenGL_accelerate",
            "main.py"
        ]
        
        print("🔧 Excluding unnecessary packages for faster build...")
        print("📋 Build configuration ready")
        
        # Start build with progress tracking
        start_time = time.time()
        print("⏳ Starting build process...")
        
        # Run PyInstaller
        pyinstaller_main.run(args)
        
        build_time = time.time() - start_time
        print(f"✅ Build completed in {build_time:.1f} seconds!")
        
        # Move executable to build directory
        exe_path = Path("dist/Nexlify.exe")
        if exe_path.exists():
            target_path = build_dir / "Nexlify.exe"
            shutil.move(str(exe_path), str(target_path))
            print(f"🎯 Executable created: {target_path}")
            
            # Copy assets and config
            if Path("assets").exists():
                shutil.copytree("assets", build_dir / "assets")
            if Path("config").exists():
                shutil.copytree("config", build_dir / "config")
            
            print(f"📁 Build package ready in: {build_dir}")
            
            # Show file size
            exe_size = target_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 Executable size: {exe_size:.1f} MB")
            
        else:
            print("❌ Executable not found in dist folder")
            
    except Exception as e:
        print(f"❌ Build failed with error: {e}")
        print("Trying alternative approach...")
        
        # Fallback: try using python -m PyInstaller with exclusions
        try:
            cmd = [sys.executable, "-m", "PyInstaller"] + [
                "--onefile",
                "--windowed",
                "--name=Nexlify",
                "--icon=assets/nexlify_icon_simple.ico",
                "--add-data=assets;assets",
                "--add-data=config;config",
                "--hidden-import=PyQt6.QtCore",
                "--hidden-import=PyQt6.QtWidgets",
                "--hidden-import=PyQt6.QtGui",
                "--hidden-import=OpenGL",
                "--hidden-import=numpy",
                "--hidden-import=PIL",
                "--hidden-import=yaml",
                "--hidden-import=pydantic",
                "--exclude-module=torch",
                "--exclude-module=matplotlib",
                "--exclude-module=scipy",
                "--exclude-module=pytest",
                "main.py"
            ]
            
            print("🔄 Using fallback build method...")
            start_time = time.time()
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            build_time = time.time() - start_time
            
            print(f"✅ Fallback build completed in {build_time:.1f} seconds!")
            
            # Move executable to build directory
            exe_path = Path("dist/Nexlify.exe")
            if exe_path.exists():
                target_path = build_dir / "Nexlify.exe"
                shutil.move(str(exe_path), str(target_path))
                print(f"🎯 Executable created: {target_path}")
                
                # Copy assets and config
                if Path("assets").exists():
                    shutil.copytree("assets", build_dir / "assets")
                if Path("config").exists():
                    shutil.copytree("config", build_dir / "config")
                
                print(f"📁 Build package ready in: {build_dir}")
                
                # Show file size
                exe_size = target_path.stat().st_size / (1024 * 1024)  # MB
                print(f"📊 Executable size: {exe_size:.1f} MB")
                
            else:
                print("❌ Executable not found in dist folder")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Fallback build also failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    return True

def build_debug():
    """Build with debug information"""
    print("🐛 Building Debug Version...")
    
    try:
        import PyInstaller.__main__ as pyinstaller_main
        
        args = [
            "--onefile",
            "--console",                    # Show console for debug
            "--name=Nexlify_Debug",
            "--icon=assets/nexlify_icon_simple.ico",
            "--add-data=assets;assets",
            "--add-data=config;config",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=OpenGL",
            "--hidden-import=numpy",
            "--hidden-import=PIL",
            "--hidden-import=yaml",
            "--hidden-import=pydantic",
            "--exclude-module=torch",
            "--exclude-module=matplotlib",
            "--exclude-module=scipy",
            "--exclude-module=pytest",
            "main.py"
        ]
        
        print("🔧 Building debug version with exclusions...")
        start_time = time.time()
        pyinstaller_main.run(args)
        build_time = time.time() - start_time
        
        print(f"✅ Debug build completed in {build_time:.1f} seconds!")
        return True
        
    except Exception as e:
        print(f"❌ Debug build failed: {e}")
        return False

def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"Removed: {dir_name}")
    
    # Clean .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"Removed: {spec_file}")
    
    print("✅ Cleanup completed!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Nexlify executable")
    parser.add_argument("--debug", action="store_true", help="Build debug version")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    
    args = parser.parse_args()
    
    if args.clean:
        clean_build()
    elif args.debug:
        build_debug()
    else:
        build_executable()
