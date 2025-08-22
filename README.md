# Tradelink Intercom System

A high-quality, push-to-talk intercom system for shop-to-shop communication over local networks.

## Features

- **Push-to-Talk**: Global Fn+F5 hotkey for instant communication
- **Crystal Clear Audio**: High-quality voice transmission
- **System Tray Operation**: Runs silently in background
- **One-to-One Communication**: Direct user-to-user calls
- **Local Network**: Fast communication over LAN
- **Simple Setup**: Easy installation and configuration

## Quick Start

### Option 1: Python Version (Development)
1. **Install Python 3.8+** if not already installed
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python main.py
   ```

### Option 2: Executable Version (Production - Recommended)
1. **Build the Executable**:
   ```bash
   # Double-click build.bat or run:
   python build_exe.py
   ```
2. **Deploy to Shops**:
   - Copy `dist/TradelinkIntercom.exe` to each computer
   - Or use `install_exe.bat` for system installation
   - Or copy `TradelinkIntercom_Portable/` folder

**Note:** The executable version doesn't require Python installation on shop computers!

## Configuration

1. **First Run**: Enter your username and shop location
2. **Network Setup**: The app automatically detects other users on the same network
3. **Hotkey**: Use Fn+F5 to push-to-talk (works globally)

## System Requirements

- Windows 10/11
- Python 3.8+
- Microphone and Speakers
- Local network connection

## Troubleshooting

- **Audio Issues**: Check microphone permissions in Windows
- **Network Issues**: Ensure both computers are on the same network
- **Hotkey Not Working**: Run as administrator if needed

## Development

This is an MVP version designed for fast deployment and easy expansion.

## 🚀 Executable Deployment

For production deployment to shops, build a single executable file:

```bash
# Quick build
double-click build.bat

# Manual build
python build_exe.py
```

This creates:
- **Single .exe file** - Easy deployment to any Windows computer
- **No Python required** - Runs independently on shop computers
- **Professional installation** - Can install to Program Files
- **Portable version** - Run from USB drives or any folder

See `EXECUTABLE_DEPLOYMENT.md` for complete deployment instructions.
