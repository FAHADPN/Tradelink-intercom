# Tradelink Intercom System - Troubleshooting Guide

## Common Issues and Solutions

### 1. Application Won't Start

**Symptoms:**
- Double-clicking main.py does nothing
- Error message about Python not found
- Application crashes immediately

**Solutions:**
1. **Check Python Installation:**
   ```bash
   python --version
   ```
   If not found, install Python 3.8+ from https://python.org

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run from Command Line:**
   ```bash
   python main.py
   ```
   This will show error messages if any

### 2. Audio Issues

**Symptoms:**
- No sound when receiving calls
- Microphone not working
- Audio quality is poor

**Solutions:**
1. **Check Windows Audio Settings:**
   - Right-click speaker icon → Sound settings
   - Ensure correct input/output devices are selected
   - Check microphone permissions

2. **Test Audio Devices:**
   - Use Windows Sound Recorder to test microphone
   - Use Windows Media Player to test speakers

3. **Check Application Permissions:**
   - Windows Settings → Privacy → Microphone
   - Ensure "Allow apps to access your microphone" is ON

4. **Audio Device Selection:**
   - The app automatically detects available devices
   - If issues persist, try different USB audio devices

### 3. Network Connection Issues

**Symptoms:**
- Users not appearing in the list
- "Disconnected" status
- Cannot send/receive audio

**Solutions:**
1. **Check Network Connection:**
   - Ensure both computers are on the same network
   - Try pinging between computers
   - Check Windows Firewall settings

2. **Firewall Configuration:**
   - Windows Defender Firewall → Allow an app through firewall
   - Add Python and the intercom application
   - Allow on both Private and Public networks

3. **Port Conflicts:**
   - Check if ports 5000-5003 are available
   - Modify config.py if needed

4. **Network Discovery:**
   - Enable Network Discovery in Windows
   - Turn on file and printer sharing

### 4. Push-to-Talk Hotkey Not Working

**Symptoms:**
- Fn+F5 does nothing
- Hotkey works only when app is focused
- Error message about hotkey registration

**Solutions:**
1. **Run as Administrator:**
   - Right-click main.py → Run as administrator
   - This is required for global hotkeys on Windows

2. **Check Hotkey Registration:**
   - Look for "Hotkey manager started" in console output
   - Try alternative keys (F5, Ctrl+F5, Alt+F5)

3. **Keyboard Compatibility:**
   - Some keyboards handle Fn keys differently
   - Try pressing just F5 instead of Fn+F5

4. **Test Hotkey:**
   - Use the "Test Hotkey" button in settings
   - Check if the button changes color when pressed

### 5. System Tray Issues

**Symptoms:**
- App doesn't minimize to tray
- Tray icon not visible
- Cannot restore from tray

**Solutions:**
1. **Check Tray Visibility:**
   - Click the arrow in system tray
   - Look for "Tradelink Intercom" icon

2. **Tray Icon Settings:**
   - Windows Settings → System → Notifications & actions
   - Ensure "Show app notifications" is ON

3. **Restore from Tray:**
   - Right-click tray icon → Show
   - Or double-click the tray icon

### 6. Performance Issues

**Symptoms:**
- Audio lag or stuttering
- High CPU usage
- Slow response times

**Solutions:**
1. **Adjust Audio Settings:**
   - Modify config.py audio settings
   - Reduce sample rate or chunk size if needed

2. **Close Other Applications:**
   - Close unnecessary background apps
   - Ensure sufficient RAM is available

3. **Network Optimization:**
   - Use wired Ethernet instead of WiFi
   - Check network bandwidth usage

### 7. User Discovery Issues

**Symptoms:**
- Other users don't appear
- Users appear and disappear randomly
- Cannot select target users

**Solutions:**
1. **Check Network Discovery:**
   - Ensure both computers are on same subnet
   - Check router settings for client isolation

2. **Restart Application:**
   - Close and reopen the application
   - This forces a new network discovery

3. **Check User Status:**
   - Look for "User discovered" messages in console
   - Verify usernames and shop locations are different

### 8. Settings and Configuration

**Symptoms:**
- Settings not saved
- App asks for setup every time
- Configuration changes don't apply

**Solutions:**
1. **Check File Permissions:**
   - Ensure the app can write to its directory
   - Run as administrator if needed

2. **Settings File Location:**
   - Look for settings.json in the app directory
   - Check if file is read-only

3. **Reset Configuration:**
   - Delete settings.json and restart
   - This will show setup dialog again

## Advanced Troubleshooting

### Network Diagnostics
```bash
# Check network connectivity
ping [other_computer_ip]

# Check open ports
netstat -an | findstr :500

# Check Windows Firewall
netsh advfirewall firewall show rule name=all
```

### Audio Diagnostics
```python
# Test audio devices in Python
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
```

### Log Analysis
- Check console output for error messages
- Look for specific error codes or messages
- Verify all components are initializing properly

## Getting Help

If you continue to experience issues:

1. **Check Console Output:**
   - Run from command line to see error messages
   - Note any specific error codes

2. **System Information:**
   - Windows version
   - Python version
   - Network configuration

3. **Reproduction Steps:**
   - Document exact steps to reproduce the issue
   - Note when the issue started occurring

4. **Contact Support:**
   - Provide detailed error information
   - Include system specifications
   - Describe the expected vs. actual behavior

## Prevention Tips

1. **Regular Maintenance:**
   - Keep Windows updated
   - Update Python and dependencies
   - Check for audio driver updates

2. **Network Health:**
   - Use quality network equipment
   - Monitor network performance
   - Regular network testing

3. **Backup Configuration:**
   - Keep copies of working settings
   - Document any custom configurations
   - Test changes in a safe environment
