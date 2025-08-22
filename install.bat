@echo off
echo ========================================
echo Tradelink Intercom System - Installer
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the intercom system:
echo 1. Double-click main.py
echo 2. Or run: python main.py
echo.
echo The system will start and ask for your setup
echo (username and shop location)
echo.
echo Press any key to exit...
pause >nul
