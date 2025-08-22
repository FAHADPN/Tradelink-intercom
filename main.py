#!/usr/bin/env python3
"""
Tradelink Intercom System - Main Application

A high-quality, push-to-talk intercom system for shop-to-shop communication.
"""

import sys
import os
import time
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot

# Import our custom modules
from main_window import MainWindow
from audio_manager import AudioManager
from network_manager import NetworkManager, User
from hotkey_manager import HotkeyManager

class IntercomController:
    """Main controller that coordinates all intercom system components."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Tradelink Intercom")
        self.app.setApplicationVersion("1.0.0")
        
        # Initialize components
        self.main_window = MainWindow()
        self.audio_manager = None
        self.network_manager = None
        self.hotkey_manager = None
        
        # State
        self.is_initialized = False
        self.current_target_user = None
        
        # Timers
        self.audio_level_timer = QTimer()
        self.audio_level_timer.timeout.connect(self.update_audio_levels)
        self.audio_level_timer.start(100)  # Update every 100ms
        
        # Connect signals
        self.setup_signal_connections()
        
    def setup_signal_connections(self):
        """Setup signal connections between components."""
        # Main window signals
        self.main_window.audio_level_updated.connect(self.audio_manager.get_audio_levels if self.audio_manager else lambda: 0.0)
        
    def initialize_system(self):
        """Initialize the intercom system components."""
        try:
            print("Initializing Tradelink Intercom System...")
            
            # Initialize audio manager
            self.audio_manager = AudioManager()
            print("Audio manager initialized")
            
            # Initialize network manager
            self.network_manager = NetworkManager(
                username=self.main_window.username,
                shop_location=self.main_window.shop_location
            )
            
            # Set network callbacks
            self.network_manager.on_user_discovered = self.on_user_discovered
            self.network_manager.on_user_offline = self.on_user_offline
            self.network_manager.on_audio_received = self.on_audio_received
            
            print("Network manager initialized")
            
            # Initialize hotkey manager
            self.hotkey_manager = HotkeyManager()
            self.hotkey_manager.set_push_to_talk_callbacks(
                self.on_push_to_talk_start,
                self.on_push_to_talk_stop
            )
            
            print("Hotkey manager initialized")
            
            # Start components
            self.start_components()
            
            self.is_initialized = True
            print("System initialization complete!")
            
        except Exception as e:
            print(f"Error initializing system: {e}")
            self.show_error_dialog("Initialization Error", str(e))
            
    def start_components(self):
        """Start all system components."""
        try:
            # Start network manager
            self.network_manager.start()
            self.main_window.update_status("Connected", True)
            
            # Start hotkey manager
            self.hotkey_manager.start_listening()
            
            # Start audio level monitoring
            self.audio_level_timer.start()
            
            print("All components started successfully")
            
        except Exception as e:
            print(f"Error starting components: {e}")
            self.show_error_dialog("Startup Error", str(e))
            
    def on_user_discovered(self, user: User):
        """Handle new user discovery."""
        print(f"User discovered: {user.username} at {user.shop_location}")
        
        # Update UI on main thread
        self.main_window.update_users_list(self.network_manager.get_online_users())
        
        # Show notification
        self.main_window.show_notification(
            "New User Online",
            f"{user.username} at {user.shop_location} is now available"
        )
        
    def on_user_offline(self, user: User):
        """Handle user going offline."""
        print(f"User offline: {user.username} at {user.shop_location}")
        
        # Update UI on main thread
        self.main_window.update_users_list(self.network_manager.get_online_users())
        
        # Show notification
        self.main_window.show_notification(
            "User Offline",
            f"{user.username} at {user.shop_location} is no longer available"
        )
        
    def on_audio_received(self, audio_packet):
        """Handle received audio data."""
        print(f"Audio received from {audio_packet.sender}")
        
        # Play the audio
        if self.audio_manager:
            self.audio_manager.play_audio(audio_packet.audio_data)
            
        # Show notification
        self.main_window.show_notification(
            "Incoming Call",
            f"Audio from {audio_packet.sender} at {audio_packet.sender_shop}"
        )
        
    def on_push_to_talk_start(self):
        """Handle push-to-talk activation."""
        print("Push-to-Talk activated")
        
        # Update UI
        self.main_window.set_ptt_active(True)
        
        # Start audio recording
        if self.audio_manager and self.current_target_user:
            self.audio_manager.start_recording(self.on_audio_data_ready)
            
    def on_push_to_talk_stop(self):
        """Handle push-to-talk deactivation."""
        print("Push-to-Talk deactivated")
        
        # Update UI
        self.main_window.set_ptt_active(False)
        
        # Stop audio recording
        if self.audio_manager:
            self.audio_manager.stop_recording()
            
    def on_audio_data_ready(self, audio_data: bytes):
        """Handle audio data ready for transmission."""
        if self.current_target_user and self.network_manager:
            # Send audio to target user
            self.network_manager.send_audio(
                target_user=self.current_target_user['username'],
                target_shop=self.current_target_user['shop_location'],
                audio_data=audio_data
            )
            
    def update_audio_levels(self):
        """Update audio level display."""
        if self.audio_manager:
            level = self.audio_manager.get_audio_levels()
            self.main_window.update_audio_level(level)
            
    def set_target_user(self, username: str, shop_location: str):
        """Set the target user for communication."""
        self.current_target_user = {
            'username': username,
            'shop_location': shop_location
        }
        print(f"Target user set to: {username} at {shop_location}")
        
    def show_error_dialog(self, title: str, message: str):
        """Show an error dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(self.main_window, title, message)
        
    def cleanup(self):
        """Clean up system resources."""
        print("Cleaning up system...")
        
        if self.audio_manager:
            self.audio_manager.cleanup()
            
        if self.network_manager:
            self.network_manager.cleanup()
            
        if self.hotkey_manager:
            self.hotkey_manager.cleanup()
            
        print("Cleanup complete")
        
    def run(self):
        """Run the intercom system."""
        try:
            # Show main window
            self.main_window.show()
            
            # Initialize system after window is shown
            QTimer.singleShot(100, self.initialize_system)
            
            # Run the application
            return self.app.exec()
            
        except Exception as e:
            print(f"Error running application: {e}")
            self.show_error_dialog("Runtime Error", str(e))
            return 1
        finally:
            self.cleanup()

def main():
    """Main entry point."""
    try:
        # Create and run the intercom controller
        controller = IntercomController()
        return controller.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
