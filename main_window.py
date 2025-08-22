import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QTextEdit, QSystemTrayIcon, QMenu, QAction, 
                             QMessageBox, QFrame, QProgressBar, QGroupBox,
                             QLineEdit, QDialog, QDialogButtonBox, QFormLayout)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QIcon, QFont, QPixmap, QPainter, QColor
import json

class SetupDialog(QDialog):
    """Dialog for initial setup of username and shop location."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tradelink Intercom Setup")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        # Setup UI
        layout = QFormLayout()
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your name")
        
        self.shop_combo = QComboBox()
        self.shop_combo.addItems(["Shop A", "Shop B", "Shop C", "Shop D"])
        
        layout.addRow("Username:", self.username_edit)
        layout.addRow("Shop Location:", self.shop_combo)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)
        self.setLayout(layout)
        
    def get_settings(self):
        """Get the entered settings."""
        return {
            'username': self.username_edit.text(),
            'shop_location': self.shop_combo.currentText()
        }

class AudioLevelWidget(QWidget):
    """Custom widget for displaying audio levels."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 30)
        self.level = 0.0
        
    def set_level(self, level: float):
        """Set the audio level (0.0 to 1.0)."""
        self.level = max(0.0, min(1.0, level))
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(40, 40, 40))
        
        # Level bar
        bar_width = int(self.width() * self.level)
        if self.level > 0.7:
            color = QColor(255, 100, 100)  # Red for high levels
        elif self.level > 0.4:
            color = QColor(255, 200, 100)  # Yellow for medium levels
        else:
            color = QColor(100, 255, 100)  # Green for low levels
            
        painter.fillRect(0, 0, bar_width, self.height(), color)
        
        # Border
        painter.setPen(QColor(100, 100, 100))
        painter.drawRect(0, 0, self.width()-1, self.height()-1)

class MainWindow(QMainWindow):
    """Main application window for the intercom system."""
    
    # Signals
    audio_level_updated = pyqtSignal(float)
    user_list_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tradelink Intercom System")
        self.setFixedSize(600, 500)
        
        # Setup UI
        self.setup_ui()
        self.setup_system_tray()
        
        # State
        self.is_minimized = False
        self.current_target_user = None
        
        # Load settings
        self.load_settings()
        
    def setup_ui(self):
        """Setup the main user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("Tradelink Intercom System")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(header)
        
        # Status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        # Connection status
        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        # Audio level
        audio_layout = QHBoxLayout()
        audio_layout.addWidget(QLabel("Audio Level:"))
        self.audio_level_widget = AudioLevelWidget()
        audio_layout.addWidget(self.audio_level_widget)
        audio_layout.addStretch()
        status_layout.addLayout(audio_layout)
        
        layout.addWidget(status_group)
        
        # Users section
        users_group = QGroupBox("Online Users")
        users_layout = QVBoxLayout(users_group)
        
        self.users_combo = QComboBox()
        self.users_combo.addItem("Select a user to call...")
        users_layout.addWidget(self.users_combo)
        
        # User list
        self.users_text = QTextEdit()
        self.users_text.setMaximumHeight(100)
        self.users_text.setReadOnly(True)
        users_layout.addWidget(self.users_text)
        
        layout.addWidget(users_group)
        
        # Communication section
        comm_group = QGroupBox("Communication")
        comm_layout = QVBoxLayout(comm_group)
        
        # Target user display
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Calling:"))
        self.target_label = QLabel("No one selected")
        self.target_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        target_layout.addWidget(self.target_label)
        target_layout.addStretch()
        comm_layout.addLayout(target_layout)
        
        # Push-to-talk button
        self.ptt_button = QPushButton("Push to Talk (Fn+F5)")
        self.ptt_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.ptt_button.clicked.connect(self.toggle_ptt)
        comm_layout.addWidget(self.ptt_button)
        
        # PTT status
        self.ptt_status = QLabel("Press Fn+F5 to talk")
        self.ptt_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ptt_status.setStyleSheet("color: #7f8c8d; font-style: italic;")
        comm_layout.addWidget(self.ptt_status)
        
        layout.addWidget(comm_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.minimize_button = QPushButton("Minimize to Tray")
        self.minimize_button.clicked.connect(self.minimize_to_tray)
        button_layout.addWidget(self.minimize_button)
        
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings)
        button_layout.addWidget(self.settings_button)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.users_combo.currentTextChanged.connect(self.on_user_selected)
        
    def setup_system_tray(self):
        """Setup the system tray icon and menu."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("Tradelink Intercom")
        
        # Set icon (you can add a custom icon file later)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        
    def load_settings(self):
        """Load application settings."""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.username = settings.get('username', '')
                    self.shop_location = settings.get('shop_location', '')
            else:
                # Show setup dialog
                self.show_setup_dialog()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.show_setup_dialog()
            
    def show_setup_dialog(self):
        """Show the initial setup dialog."""
        dialog = SetupDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            self.username = settings['username']
            self.shop_location = settings['shop_location']
            self.save_settings()
        else:
            # User cancelled setup
            QMessageBox.critical(self, "Setup Required", 
                               "Setup is required to use the intercom system.")
            sys.exit(0)
            
    def save_settings(self):
        """Save application settings."""
        try:
            settings = {
                'username': self.username,
                'shop_location': self.shop_location
            }
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def update_status(self, status: str, is_connected: bool = False):
        """Update the connection status."""
        self.status_label.setText(status)
        if is_connected:
            self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            
    def update_audio_level(self, level: float):
        """Update the audio level display."""
        self.audio_level_widget.set_level(level)
        
    def update_users_list(self, users: list):
        """Update the list of online users."""
        self.users_combo.clear()
        self.users_combo.addItem("Select a user to call...")
        
        self.users_text.clear()
        
        for user in users:
            self.users_combo.addItem(f"{user.username} ({user.shop_location})")
            self.users_text.append(f"• {user.username} at {user.shop_location}")
            
    def on_user_selected(self, text: str):
        """Handle user selection from combo box."""
        if text == "Select a user to call...":
            self.current_target_user = None
            self.target_label.setText("No one selected")
            self.ptt_button.setEnabled(False)
        else:
            # Parse user info from combo text
            parts = text.split(" (")
            if len(parts) == 2:
                username = parts[0]
                shop_location = parts[1].rstrip(")")
                self.current_target_user = {'username': username, 'shop_location': shop_location}
                self.target_label.setText(f"{username} at {shop_location}")
                self.ptt_status.setText("Press Fn+F5 to talk")
                self.ptt_button.setEnabled(True)
                
    def toggle_ptt(self):
        """Toggle push-to-talk manually (for testing)."""
        # This will be connected to the hotkey manager
        pass
        
    def set_ptt_active(self, active: bool):
        """Set push-to-talk active state."""
        if active:
            self.ptt_button.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                }
            """)
            self.ptt_button.setText("TALKING...")
            self.ptt_status.setText("TALKING - Release Fn+F5 to stop")
        else:
            self.ptt_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                }
            """)
            self.ptt_button.setText("Push to Talk (Fn+F5)")
            self.ptt_status.setText("Press Fn+F5 to talk")
            
    def minimize_to_tray(self):
        """Minimize the application to system tray."""
        self.hide()
        self.tray_icon.show()
        self.is_minimized = True
        
    def show_settings(self):
        """Show the settings dialog."""
        # For now, just show setup dialog again
        self.show_setup_dialog()
        
    def quit_application(self):
        """Quit the application."""
        QApplication.quit()
        
    def closeEvent(self, event):
        """Handle window close event."""
        if self.is_minimized:
            event.ignore()
            self.minimize_to_tray()
        else:
            event.accept()
            
    def show_notification(self, title: str, message: str):
        """Show a system tray notification."""
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 3000)
