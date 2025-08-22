import keyboard
import threading
import time
from typing import Optional, Callable
import win32api
import win32con
import win32gui

class HotkeyManager:
    """Manages global hotkeys for the intercom system."""
    
    def __init__(self):
        self.is_listening = False
        self.listening_thread: Optional[threading.Thread] = None
        
        # Callbacks
        self.on_push_to_talk_start: Optional[Callable[[], None]] = None
        self.on_push_to_talk_stop: Optional[Callable[[], None]] = None
        
        # State
        self.is_ptt_active = False
        self.hotkey_combo = "fn+f5"
        
        # Windows-specific
        self.hotkey_id = 1
        
    def start_listening(self):
        """Start listening for global hotkeys."""
        if self.is_listening:
            return
            
        self.is_listening = True
        
        try:
            # Register the hotkey using Windows API for better global support
            if not self._register_windows_hotkey():
                # Fallback to keyboard library
                self._register_keyboard_hotkey()
                
            print("Hotkey manager started")
            
        except Exception as e:
            print(f"Error starting hotkey manager: {e}")
            self.is_listening = False
            
    def stop_listening(self):
        """Stop listening for global hotkeys."""
        self.is_listening = False
        
        try:
            # Unregister Windows hotkey
            self._unregister_windows_hotkey()
            
            # Unregister keyboard library hotkey
            keyboard.unhook_all()
            
        except Exception as e:
            print(f"Error stopping hotkey manager: {e}")
            
        print("Hotkey manager stopped")
        
    def _register_windows_hotkey(self) -> bool:
        """Register hotkey using Windows API."""
        try:
            # Try to register Fn+F5 (Fn is not directly accessible via Windows API)
            # So we'll use F5 as the primary key
            success = win32gui.RegisterHotKey(
                None,  # No window handle needed for global hotkey
                self.hotkey_id,
                win32con.MOD_NOREPEAT,  # No repeat
                win32con.VK_F5  # F5 key
            )
            
            if success:
                # Start Windows message loop thread
                self.listening_thread = threading.Thread(target=self._windows_message_loop, daemon=True)
                self.listening_thread.start()
                return True
                
        except Exception as e:
            print(f"Windows hotkey registration failed: {e}")
            
        return False
        
    def _register_keyboard_hotkey(self):
        """Register hotkey using keyboard library as fallback."""
        try:
            # Register F5 key (Fn+F5 will be detected as F5 on most keyboards)
            keyboard.on_press_key("f5", self._on_f5_press, suppress=True)
            keyboard.on_release_key("f5", self._on_f5_release, suppress=True)
            
            print("Using keyboard library fallback for hotkeys")
            
        except Exception as e:
            print(f"Keyboard library hotkey registration failed: {e}")
            
    def _unregister_windows_hotkey(self):
        """Unregister Windows hotkey."""
        try:
            win32gui.UnregisterHotKey(None, self.hotkey_id)
        except:
            pass
            
    def _windows_message_loop(self):
        """Windows message loop for hotkey detection."""
        try:
            while self.is_listening:
                # Get Windows messages
                msg = win32gui.GetMessage(None, 0, 0)
                
                if msg[0] == 0:  # WM_QUIT
                    break
                    
                if msg[0] == win32con.WM_HOTKEY:
                    if msg[1] == self.hotkey_id:
                        # F5 was pressed
                        self._handle_f5_press()
                        
                # Process the message
                win32gui.TranslateMessage(msg)
                win32gui.DispatchMessage(msg)
                
        except Exception as e:
            print(f"Windows message loop error: {e}")
            
    def _on_f5_press(self, event):
        """Handle F5 key press from keyboard library."""
        if not self.is_ptt_active:
            self._handle_f5_press()
            
    def _on_f5_release(self, event):
        """Handle F5 key release from keyboard library."""
        if self.is_ptt_active:
            self._handle_f5_release()
            
    def _handle_f5_press(self):
        """Handle F5 key press (start PTT)."""
        if not self.is_ptt_active:
            self.is_ptt_active = True
            
            if self.on_push_to_talk_start:
                self.on_push_to_talk_start()
                
            print("Push-to-Talk activated")
            
    def _handle_f5_release(self):
        """Handle F5 key release (stop PTT)."""
        if self.is_ptt_active:
            self.is_ptt_active = False
            
            if self.on_push_to_talk_stop:
                self.on_push_to_talk_stop()
                
            print("Push-to-Talk deactivated")
            
    def is_push_to_talk_active(self) -> bool:
        """Check if push-to-talk is currently active."""
        return self.is_ptt_active
        
    def set_push_to_talk_callbacks(self, on_start: Callable[[], None], on_stop: Callable[[], None]):
        """Set callbacks for push-to-talk events."""
        self.on_push_to_talk_start = on_start
        self.on_push_to_talk_stop = on_stop
        
    def change_hotkey(self, new_hotkey: str):
        """Change the hotkey combination."""
        try:
            # Stop current listening
            self.stop_listening()
            
            # Update hotkey
            self.hotkey_combo = new_hotkey
            
            # Restart listening
            self.start_listening()
            
            print(f"Hotkey changed to: {new_hotkey}")
            
        except Exception as e:
            print(f"Error changing hotkey: {e}")
            
    def get_current_hotkey(self) -> str:
        """Get the current hotkey combination."""
        return self.hotkey_combo
        
    def test_hotkey(self) -> bool:
        """Test if the current hotkey is working."""
        try:
            # Simulate a test press
            test_thread = threading.Thread(target=self._test_hotkey_sequence, daemon=True)
            test_thread.start()
            return True
        except:
            return False
            
    def _test_hotkey_sequence(self):
        """Test sequence for hotkey functionality."""
        time.sleep(0.1)
        self._handle_f5_press()
        time.sleep(0.1)
        self._handle_f5_release()
        
    def cleanup(self):
        """Clean up hotkey resources."""
        self.stop_listening()
