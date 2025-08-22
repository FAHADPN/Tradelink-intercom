# Tradelink Intercom System - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies
```bash
# Double-click install.bat
# OR run manually:
pip install -r requirements.txt
```

### Step 2: Run the System
```bash
# Double-click run.bat
# OR run manually:
python main.py
```

### Step 3: First-Time Setup
1. Enter your **Username** (e.g., "John")
2. Select your **Shop Location** (e.g., "Shop A")
3. Click **OK**

### Step 4: Start Communicating
1. **Select a user** from the dropdown
2. **Press Fn+F5** to talk (or just F5)
3. **Release Fn+F5** to stop talking

## 🎯 Key Features

- **Push-to-Talk**: Fn+F5 hotkey works globally
- **System Tray**: Minimizes to background
- **Auto-Discovery**: Finds other users automatically
- **Crystal Clear Audio**: High-quality voice transmission
- **One-to-One Calls**: Direct communication

## 🔧 Quick Configuration

### Change Shop Names
Edit `config.py`:
```python
SHOP_CONFIG = {
    'default_shops': [
        'Front Desk',
        'Back Office', 
        'Warehouse',
        'Sales Floor'
    ],
}
```

### Change Hotkey
Edit `config.py`:
```python
HOTKEY_CONFIG = {
    'primary_key': 'f6',  # Change from f5 to f6
}
```

### Adjust Audio Quality
Edit `config.py`:
```python
AUDIO_CONFIG = {
    'sample_rate': 22050,  # Lower for better performance
    'chunk_size': 512,     # Smaller for lower latency
}
```

## 📱 System Tray Usage

- **Right-click tray icon** → Show (restore window)
- **Right-click tray icon** → Quit (close app)
- **Double-click tray icon** → Restore window

## 🌐 Network Setup

### Automatic (Recommended)
- Both computers on same network
- App discovers users automatically
- No manual configuration needed

### Manual (If Issues)
- Check Windows Firewall allows Python
- Ensure ports 5000-5003 are open
- Verify network discovery is enabled

## 🎵 Audio Setup

### Microphone
- Windows Settings → Privacy → Microphone
- Allow apps to access microphone
- Test with Windows Sound Recorder

### Speakers
- Check Windows audio output
- Test with Windows Media Player
- Adjust volume levels

## 🚨 Troubleshooting

### App Won't Start
```bash
python main.py  # Run from command line to see errors
```

### No Audio
- Check microphone permissions
- Test audio devices in Windows
- Run as administrator

### Users Not Appearing
- Check network connection
- Restart application
- Verify firewall settings

### Hotkey Not Working
- Run as administrator
- Try just F5 instead of Fn+F5
- Check console for "Hotkey manager started"

## 📋 Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Both computers on same network
- [ ] Windows Firewall configured
- [ ] Microphone permissions enabled
- [ ] Test audio input/output
- [ ] Run application on both computers
- [ ] Verify user discovery
- [ ] Test push-to-talk functionality

## 🔄 Daily Usage

1. **Start Application**: Double-click `run.bat`
2. **Minimize to Tray**: Click "Minimize to Tray"
3. **Select Target User**: Choose from dropdown
4. **Press Fn+F5**: Hold to talk, release to stop
5. **Close to Tray**: App stays running in background

## 📞 Support

- **Console Output**: Check for error messages
- **Troubleshooting Guide**: See `TROUBLESHOOTING.md`
- **Configuration**: Modify `config.py` for customization
- **Logs**: Check console for detailed information

## 🎉 You're Ready!

The intercom system is now running and ready for shop-to-shop communication. Users will automatically discover each other and can start talking immediately using the Fn+F5 push-to-talk functionality.
