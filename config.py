"""
Configuration file for Tradelink Intercom System
Modify these settings as needed for your environment
"""

# Network Configuration
NETWORK_CONFIG = {
    'discovery_port': 5002,      # Port for user discovery
    'audio_port': 5003,          # Port for audio transmission
    'broadcast_port': 5001,      # Port for broadcast messages
    'timeout': 1.0,              # Network timeout in seconds
    'max_audio_packet_size': 65536,  # Maximum audio packet size
}

# Audio Configuration
AUDIO_CONFIG = {
    'sample_rate': 44100,        # Audio sample rate (Hz)
    'chunk_size': 1024,          # Audio chunk size for processing
    'channels': 1,               # Number of audio channels (1 = mono)
    'format': 'int16',           # Audio format
    'noise_gate_threshold': 500, # Noise gate threshold
    'buffer_size': 4096,         # Audio buffer size
}

# Hotkey Configuration
HOTKEY_CONFIG = {
    'primary_key': 'f5',         # Primary key for push-to-talk
    'modifier': 'fn',            # Modifier key (if applicable)
    'fallback_keys': ['f5', 'ctrl+f5', 'alt+f5'],  # Fallback key combinations
    'suppress_key': True,        # Suppress key from other applications
}

# UI Configuration
UI_CONFIG = {
    'window_width': 600,         # Main window width
    'window_height': 500,        # Main window height
    'minimize_to_tray': True,    # Minimize to system tray on close
    'show_notifications': True,  # Show system notifications
    'notification_duration': 3000,  # Notification display time (ms)
}

# System Configuration
SYSTEM_CONFIG = {
    'auto_start': False,         # Auto-start with Windows
    'run_as_admin': False,       # Run as administrator (for global hotkeys)
    'log_level': 'INFO',         # Logging level
    'log_file': 'intercom.log',  # Log file path
    'backup_settings': True,     # Backup settings on changes
}

# Shop Configuration
SHOP_CONFIG = {
    'default_shops': [
        'Shop A',
        'Shop B', 
        'Shop C',
        'Shop D',
        'Warehouse',
        'Office'
    ],
    'max_users_per_shop': 10,    # Maximum users per shop
    'user_timeout': 300,         # User timeout in seconds
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'audio_update_interval': 100,    # Audio level update interval (ms)
    'network_scan_interval': 1000,   # Network scan interval (ms)
    'user_list_update_interval': 2000,  # User list update interval (ms)
    'max_audio_queue_size': 100,     # Maximum audio packets in queue
}

# Security Configuration
SECURITY_CONFIG = {
    'encrypt_audio': False,      # Encrypt audio data (not implemented in MVP)
    'require_authentication': False,  # Require user authentication
    'allowed_networks': [],      # List of allowed network ranges
    'block_external_access': True,    # Block external network access
}

def get_config(section: str, key: str, default=None):
    """Get configuration value with fallback to default."""
    configs = {
        'network': NETWORK_CONFIG,
        'audio': AUDIO_CONFIG,
        'hotkey': HOTKEY_CONFIG,
        'ui': UI_CONFIG,
        'system': SYSTEM_CONFIG,
        'shop': SHOP_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'security': SECURITY_CONFIG,
    }
    
    return configs.get(section, {}).get(key, default)

def update_config(section: str, key: str, value):
    """Update configuration value."""
    configs = {
        'network': NETWORK_CONFIG,
        'audio': AUDIO_CONFIG,
        'hotkey': HOTKEY_CONFIG,
        'ui': UI_CONFIG,
        'system': SYSTEM_CONFIG,
        'shop': SHOP_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'security': SECURITY_CONFIG,
    }
    
    if section in configs and key in configs[section]:
        configs[section][key] = value
        return True
    return False

def get_all_config():
    """Get all configuration as a dictionary."""
    return {
        'network': NETWORK_CONFIG,
        'audio': AUDIO_CONFIG,
        'hotkey': HOTKEY_CONFIG,
        'ui': UI_CONFIG,
        'system': SYSTEM_CONFIG,
        'shop': SHOP_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'security': SECURITY_CONFIG,
    }
