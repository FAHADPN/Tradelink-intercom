# Tradelink Intercom System - Executable Deployment Guide

## 🚀 Building the Executable

### Prerequisites
- Python 3.8+ installed
- All dependencies installed (`pip install -r requirements.txt`)
- Windows 10/11 (for building)

### Quick Build
```bash
# Option 1: Use the batch file (recommended)
double-click build.bat

# Option 2: Run manually
python build_exe.py
```

### What Gets Created
After building, you'll have:
- `dist/TradelinkIntercom.exe` - Single executable file
- `install_exe.bat` - System installer
- `TradelinkIntercom_Portable/` - Portable version folder

## 📦 Deployment Options

### Option 1: Single Executable (Recommended for Shops)
**File:** `dist/TradelinkIntercom.exe`

**Pros:**
- Single file deployment
- No installation required
- Can run from USB drive
- Easy to copy between computers

**Usage:**
1. Copy `TradelinkIntercom.exe` to any computer
2. Double-click to run
3. First run will ask for username/shop setup

### Option 2: System Installation
**File:** `install_exe.bat`

**Pros:**
- Installs to Program Files
- Creates desktop shortcut
- Professional installation
- Easy for end users

**Usage:**
1. Run `install_exe.bat` as administrator
2. System installs to `C:\Program Files\TradelinkIntercom\`
3. Desktop shortcut created automatically

### Option 3: Portable Package
**Folder:** `TradelinkIntercom_Portable/`

**Pros:**
- Complete package in one folder
- Includes configuration file
- Easy launcher script
- Perfect for USB deployment

**Usage:**
1. Copy entire folder to any computer
2. Run `run.bat` to start
3. All files stay together

## 🔧 Building Process Details

### PyInstaller Configuration
The build script uses these PyInstaller options:

```bash
--onefile          # Single executable
--windowed         # No console window
--name=TradelinkIntercom  # Executable name
--add-data=config.py;.    # Include config file
--hidden-import=...       # Include all dependencies
--collect-all=...         # Collect all package data
```

### Dependencies Included
- PyQt6 (GUI framework)
- PyAudio (audio handling)
- NumPy (audio processing)
- pywin32 (Windows API)
- keyboard (hotkey support)
- psutil (system utilities)

### Build Output
```
dist/
└── TradelinkIntercom.exe  # ~50-100 MB executable

TradelinkIntercom_Portable/
├── TradelinkIntercom.exe
├── config.py
├── run.bat
└── README.txt
```

## 🚀 Deployment to Shops

### Step 1: Build the Executable
```bash
python build_exe.py
```

### Step 2: Test Locally
```bash
# Test the executable
dist/TradelinkIntercom.exe

# Test portable version
TradelinkIntercom_Portable/run.bat
```

### Step 3: Deploy to Shops
**For each shop computer:**

1. **Copy executable:**
   ```bash
   # Option A: Single file
   copy TradelinkIntercom.exe C:\Users\Public\Desktop\
   
   # Option B: Portable folder
   xcopy TradelinkIntercom_Portable C:\Users\Public\Desktop\ /E /I
   
   # Option C: System install
   run install_exe.bat as administrator
   ```

2. **Create shortcut:**
   - Right-click executable → Send to → Desktop
   - Or use the installer for automatic shortcut creation

### Step 4: First Run Setup
Each computer will need:
- Username (e.g., "John", "Sarah")
- Shop location (e.g., "Shop A", "Shop B")
- Microphone permissions enabled
- Network access allowed

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Build executable successfully
- [ ] Test on development machine
- [ ] Verify audio input/output works
- [ ] Test network discovery
- [ ] Test push-to-talk functionality

### Shop Setup
- [ ] Copy executable to each computer
- [ ] Create desktop shortcuts
- [ ] Enable microphone permissions
- [ ] Configure Windows Firewall
- [ ] Test network connectivity
- [ ] Verify user discovery
- [ ] Test audio communication

### Post-Deployment
- [ ] Document any custom configurations
- [ ] Create backup of working setup
- [ ] Train shop staff on usage
- [ ] Test with multiple users
- [ ] Monitor for any issues

## 🔍 Troubleshooting Executable Issues

### Common Problems

#### 1. Executable Won't Start
**Symptoms:**
- Double-click does nothing
- Error message about missing DLLs
- Application crashes immediately

**Solutions:**
- Run from command line to see errors
- Check Windows Defender/antivirus blocking
- Verify all dependencies were included
- Try running as administrator

#### 2. Missing Audio
**Symptoms:**
- No microphone input
- No audio output
- Audio device errors

**Solutions:**
- Check microphone permissions
- Verify audio drivers are working
- Test with Windows Sound Recorder
- Run as administrator

#### 3. Network Issues
**Symptoms:**
- Users not discovered
- Connection errors
- Firewall blocking

**Solutions:**
- Check Windows Firewall settings
- Verify network connectivity
- Test with ping between computers
- Check antivirus network blocking

### Debug Mode
To see error messages, modify the build script:
```python
# Change --windowed to --console in build_exe.py
"--console",  # Instead of "--windowed"
```

## 📱 Advanced Deployment

### Silent Installation
Create a silent installer using:
```batch
@echo off
TradelinkIntercom.exe /SILENT /NORESTART
```

### Auto-Start
Add to Windows startup:
```batch
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "TradelinkIntercom" /t REG_SZ /d "C:\\Program Files\\TradelinkIntercom\\TradelinkIntercom.exe" /f
```

### Network Deployment
For multiple shops:
1. Build executable once
2. Use network share or USB drives
3. Create deployment script for each shop
4. Use Group Policy for enterprise deployment

## 🎯 Best Practices

### Performance
- Keep executable size under 100MB
- Use --onefile for single deployment
- Test on target hardware before deployment

### Security
- Sign executable with code signing certificate
- Use Windows Defender exclusions if needed
- Monitor for false positive antivirus alerts

### Maintenance
- Keep build environment consistent
- Document any dependency changes
- Test on multiple Windows versions
- Create backup of working builds

## 📞 Support

### Build Issues
- Check PyInstaller version compatibility
- Verify all dependencies are installed
- Check Python version compatibility

### Runtime Issues
- Use console mode for debugging
- Check Windows Event Viewer
- Test with minimal configuration

### Deployment Issues
- Verify target system requirements
- Check network and firewall settings
- Test on clean Windows installation

## 🎉 Success Metrics

Your deployment is successful when:
- [ ] Executable runs on all target computers
- [ ] Audio input/output works correctly
- [ ] Network discovery finds other users
- [ ] Push-to-talk functions properly
- [ ] Users can communicate between shops
- [ ] System runs reliably in background
- [ ] No Python installation required on target machines

The executable version eliminates the need for Python installation on shop computers, making deployment much simpler and more professional!
