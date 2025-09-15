@echo off
echo 🚀 Building Nexlify Executable...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

REM Install requirements if needed
echo 📦 Installing requirements...
pip install -r requirements.txt

REM Build executable
echo.
echo 🔨 Building executable...
python build_exe.py

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo 🎯 Executable is in the build_exe folder
echo.
pause
