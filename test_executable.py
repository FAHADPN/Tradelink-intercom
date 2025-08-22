#!/usr/bin/env python3
"""
Test script for the Tradelink Intercom System executable.
Run this after building to verify everything works correctly.
"""

import os
import sys
import subprocess
import time
import signal

def test_executable_exists():
    """Test if the executable was created."""
    exe_path = "dist/TradelinkIntercom.exe"
    if os.path.exists(exe_path):
        print(f"✓ Executable found: {exe_path}")
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"  Size: {file_size:.1f} MB")
        return exe_path
    else:
        print(f"✗ Executable not found: {exe_path}")
        return None

def test_portable_version():
    """Test if portable version was created."""
    portable_dir = "TradelinkIntercom_Portable"
    if os.path.exists(portable_dir):
        print(f"✓ Portable version found: {portable_dir}/")
        files = os.listdir(portable_dir)
        for file in files:
            print(f"  - {file}")
        return True
    else:
        print(f"✗ Portable version not found: {portable_dir}/")
        return False

def test_installer():
    """Test if installer was created."""
    installer_path = "install_exe.bat"
    if os.path.exists(installer_path):
        print(f"✓ Installer found: {installer_path}")
        return True
    else:
        print(f"✗ Installer not found: {installer_path}")
        return False

def test_executable_launch(exe_path):
    """Test if the executable can launch (basic test)."""
    print(f"\n🧪 Testing executable launch...")
    
    try:
        # Try to launch the executable
        process = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Wait a bit for it to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Executable launched successfully")
            
            # Terminate the process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
            return True
        else:
            # Process exited, check for errors
            stdout, stderr = process.communicate()
            if stderr:
                print(f"✗ Executable failed with error: {stderr.decode()}")
            else:
                print(f"✗ Executable exited unexpectedly")
            return False
            
    except Exception as e:
        print(f"✗ Failed to launch executable: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available."""
    print(f"\n🔍 Testing dependencies...")
    
    required_modules = [
        'PyQt6',
        'pyaudio', 
        'numpy',
        'win32api',
        'keyboard',
        'psutil'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - Missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {', '.join(missing_modules)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    else:
        print("✓ All dependencies available")
        return True

def run_basic_tests():
    """Run basic functionality tests."""
    print(f"\n🧪 Running basic tests...")
    
    # Test audio manager
    try:
        from audio_manager import AudioManager
        audio = AudioManager()
        print("✓ AudioManager created successfully")
        audio.cleanup()
    except Exception as e:
        print(f"✗ AudioManager test failed: {e}")
    
    # Test network manager
    try:
        from network_manager import NetworkManager
        network = NetworkManager("test", "test")
        print("✓ NetworkManager created successfully")
        network.cleanup()
    except Exception as e:
        print(f"✗ NetworkManager test failed: {e}")
    
    # Test hotkey manager
    try:
        from hotkey_manager import HotkeyManager
        hotkey = HotkeyManager()
        print("✓ HotkeyManager created successfully")
        hotkey.cleanup()
    except Exception as e:
        print(f"✗ HotkeyManager test failed: {e}")

def main():
    """Main test function."""
    print("🧪 Tradelink Intercom System - Executable Test")
    print("=" * 50)
    
    # Test dependencies first
    deps_ok = test_dependencies()
    
    # Test executable creation
    exe_path = test_executable_exists()
    portable_ok = test_portable_version()
    installer_ok = test_installer()
    
    # Test executable launch if it exists
    launch_ok = False
    if exe_path:
        launch_ok = test_executable_launch(exe_path)
    
    # Run basic functionality tests
    if deps_ok:
        run_basic_tests()
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 30)
    print(f"Dependencies: {'✓' if deps_ok else '✗'}")
    print(f"Executable: {'✓' if exe_path else '✗'}")
    print(f"Portable: {'✓' if portable_ok else '✗'}")
    print(f"Installer: {'✓' if installer_ok else '✗'}")
    print(f"Launch: {'✓' if launch_ok else '✗'}")
    
    if all([deps_ok, exe_path, portable_ok, installer_ok, launch_ok]):
        print(f"\n🎉 All tests passed! Your executable is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
