#!/usr/bin/env python3
"""
Build script for creating a single executable file of the Tradelink Intercom System.
This script uses PyInstaller to package all dependencies into one .exe file.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed, install if not."""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False

def clean_build_dirs():
    """Clean up previous build directories."""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"Removed {spec_file}")

def build_executable():
    """Build the executable using PyInstaller."""
    print("\n🚀 Building Tradelink Intercom System executable...")
    
    # Try method 1: Direct import (recommended)
    try:
        print("Method 1: Using PyInstaller direct import...")
        from PyInstaller.__main__ import run
        
        # PyInstaller arguments
        args = [
            "--onefile",                    # Single executable file
            "--windowed",                   # No console window (GUI only)
            "--name=TradelinkIntercom",     # Executable name
            "--add-data=config.py;.",       # Include config file
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui", 
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=pyaudio",
            "--hidden-import=numpy",
            "--hidden-import=win32api",
            "--hidden-import=win32con",
            "--hidden-import=win32gui",
            "--hidden-import=keyboard",
            "--hidden-import=psutil",
            "--collect-all=PyQt6",
            "--collect-all=pyaudio",
            "--collect-all=numpy",
            "--collect-all=win32",
            "--collect-all=keyboard",
            "--collect-all=psutil",
            "main.py"
        ]
        
        # Add icon if it exists
        if os.path.exists("icon.ico"):
            args.insert(1, "--icon=icon.ico")
        
        print("Running PyInstaller...")
        print(" ".join(args))
        
        # Run PyInstaller directly
        run(args)
        
        print("✓ Build completed successfully!")
        return True
        
    except ImportError as e:
        print(f"Method 1 failed: {e}")
        print("Trying method 2: Python module execution...")
        
        # Try method 2: Python module execution
        try:
            import PyInstaller
            
            # Define args for method 2
            args2 = [
                "--onefile",                    # Single executable file
                "--windowed",                   # No console window (GUI only)
                "--name=TradelinkIntercom",     # Executable name
                "--add-data=config.py;.",       # Include config file
                "--hidden-import=PyQt6.QtCore",
                "--hidden-import=PyQt6.QtGui", 
                "--hidden-import=PyQt6.QtWidgets",
                "--hidden-import=pyaudio",
                "--hidden-import=numpy",
                "--hidden-import=win32api",
                "--hidden-import=win32con",
                "--hidden-import=win32gui",
                "--hidden-import=keyboard",
                "--hidden-import=psutil",
                "--collect-all=PyQt6",
                "--collect-all=pyaudio",
                "--collect-all=numpy",
                "--collect-all=win32",
                "--collect-all=keyboard",
                "--collect-all=psutil",
                "main.py"
            ]
            
            # Add icon if it exists
            if os.path.exists("icon.ico"):
                args2.insert(1, "--icon=icon.ico")
            
            cmd = [sys.executable, "-m", "PyInstaller"] + args2
            
            print("Running PyInstaller via Python module...")
            print(" ".join(cmd))
            
            subprocess.check_call(cmd)
            print("✓ Build completed successfully!")
            return True
            
        except Exception as e2:
            print(f"Method 2 failed: {e2}")
            print("Trying method 3: Command line fallback...")
            
            # Try method 3: Command line fallback
            try:
                # Define args for method 3
                args3 = [
                    "--onefile",                    # Single executable file
                    "--windowed",                   # No console window (GUI only)
                    "--name=TradelinkIntercom",     # Executable name
                    "--add-data=config.py;.",       # Include config file
                    "--hidden-import=PyQt6.QtCore",
                    "--hidden-import=PyQt6.QtGui", 
                    "--hidden-import=PyQt6.QtWidgets",
                    "--hidden-import=pyaudio",
                    "--hidden-import=numpy",
                    "--hidden-import=win32api",
                    "--hidden-import=win32con",
                    "--hidden-import=win32gui",
                    "--hidden-import=keyboard",
                    "--hidden-import=psutil",
                    "--collect-all=PyQt6",
                    "--collect-all=pyaudio",
                    "--collect-all=numpy",
                    "--collect-all=win32",
                    "--collect-all=keyboard",
                    "--collect-all=psutil",
                    "main.py"
                ]
                
                # Add icon if it exists
                if os.path.exists("icon.ico"):
                    args3.insert(1, "--icon=icon.ico")
                
                cmd = ["pyinstaller"] + args3
                
                print("Running PyInstaller via command line...")
                print(" ".join(cmd))
                
                subprocess.check_call(cmd)
                print("✓ Build completed successfully!")
                return True
                
            except Exception as e3:
                print(f"All methods failed:")
                print(f"  Method 1 (direct import): {e}")
                print(f"  Method 2 (Python module): {e2}")
                print(f"  Method 3 (command line): {e3}")
                return False

def create_installer_bat():
    """Create a simple installer batch file for the executable."""
    installer_content = """@echo off
echo ========================================
echo Tradelink Intercom System - Installer
echo ========================================
echo.

echo Copying executable to Program Files...
if not exist "C:\\Program Files\\TradelinkIntercom" mkdir "C:\\Program Files\\TradelinkIntercom"

copy "dist\\TradelinkIntercom.exe" "C:\\Program Files\\TradelinkIntercom\\"

echo.
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Tradelink Intercom.lnk'); $Shortcut.TargetPath = 'C:\\Program Files\\TradelinkIntercom\\TradelinkIntercom.exe'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo The Tradelink Intercom System has been installed to:
echo C:\\Program Files\\TradelinkIntercom\\
echo.
echo A desktop shortcut has been created.
echo.
echo To run the system, double-click the desktop shortcut.
echo.
pause
"""
    
    with open("install_exe.bat", "w") as f:
        f.write(installer_content)
    
    print("✓ Created install_exe.bat")

def create_portable_version():
    """Create a portable version that can run from any folder."""
    if os.path.exists("dist/TradelinkIntercom.exe"):
        portable_dir = "TradelinkIntercom_Portable"
        if os.path.exists(portable_dir):
            shutil.rmtree(portable_dir)
        
        os.makedirs(portable_dir)
        
        # Copy executable
        shutil.copy("dist/TradelinkIntercom.exe", portable_dir)
        
        # Copy config file
        shutil.copy("config.py", portable_dir)
        
        # Create run script
        run_script = """@echo off
echo Starting Tradelink Intercom System...
TradelinkIntercom.exe
pause
"""
        with open(f"{portable_dir}/run.bat", "w") as f:
            f.write(run_script)
        
        # Create README
        readme_content = """# Tradelink Intercom System - Portable Version

This is a portable version of the Tradelink Intercom System.

## Usage

1. Copy this folder to any computer
2. Double-click `run.bat` to start the system
3. No installation required!

## Files

- `TradelinkIntercom.exe` - Main application
- `config.py` - Configuration file (can be modified)
- `run.bat` - Launcher script

## Notes

- This version runs from any folder
- No system-wide installation
- Perfect for USB drives or temporary deployment
- Settings are saved in the same folder

## Support

See the main README.md for troubleshooting and configuration help.
"""
        with open(f"{portable_dir}/README.txt", "w") as f:
            f.write(readme_content)
        
        print(f"✓ Created portable version in {portable_dir}/")
        return True
    return False

def main():
    """Main build process."""
    print("🏗️  Tradelink Intercom System - Executable Builder")
    print("=" * 50)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("Cannot continue without PyInstaller")
        return 1
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if not build_executable():
        return 1
    
    # Create installer
    create_installer_bat()
    
    # Create portable version
    create_portable_version()
    
    print("\n🎉 Build completed successfully!")
    print("\n📁 Output files:")
    print("  - dist/TradelinkIntercom.exe (Main executable)")
    print("  - install_exe.bat (System installer)")
    print("  - TradelinkIntercom_Portable/ (Portable version)")
    
    print("\n🚀 Next steps:")
    print("  1. Test the executable: dist/TradelinkIntercom.exe")
    print("  2. Use install_exe.bat for system-wide installation")
    print("  3. Copy TradelinkIntercom_Portable/ for portable use")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
