import socket
import threading
import json
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict

@dataclass
class User:
    """Represents a user in the intercom system."""
    username: str
    shop_location: str
    ip_address: str
    port: int
    last_seen: float
    is_online: bool = True

@dataclass
class AudioPacket:
    """Represents an audio packet for transmission."""
    sender: str
    sender_shop: str
    timestamp: float
    audio_data: bytes
    sequence_number: int

class NetworkManager:
    """Manages network communication between shops."""
    
    def __init__(self, username: str, shop_location: str, port: int = 5000):
        self.username = username
        self.shop_location = shop_location
        self.port = port
        
        # Network settings
        self.broadcast_port = 5001
        self.discovery_port = 5002
        self.audio_port = 5003
        
        # Sockets
        self.udp_socket: Optional[socket.socket] = None
        self.discovery_socket: Optional[socket.socket] = None
        self.audio_socket: Optional[socket.socket] = None
        
        # User management
        self.users: Dict[str, User] = {}
        self.local_ip = self._get_local_ip()
        
        # Callbacks
        self.on_user_discovered: Optional[Callable[[User], None]] = None
        self.on_user_offline: Optional[Callable[[User], None]] = None
        self.on_audio_received: Optional[Callable[[AudioPacket], None]] = None
        
        # Threads
        self.discovery_thread: Optional[threading.Thread] = None
        self.audio_thread: Optional[threading.Thread] = None
        self.running = False
        
        # Audio sequence tracking
        self.audio_sequence = 0
        
    def start(self):
        """Start the network manager."""
        if self.running:
            return
            
        self.running = True
        
        try:
            # Create UDP socket for general communication
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.udp_socket.bind(('', self.port))
            
            # Create discovery socket
            self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.discovery_socket.bind(('', self.discovery_port))
            
            # Create audio socket
            self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.audio_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.audio_socket.bind(('', self.audio_port))
            
            # Start discovery thread
            self.discovery_thread = threading.Thread(target=self._discovery_worker, daemon=True)
            self.discovery_thread.start()
            
            # Start audio thread
            self.audio_thread = threading.Thread(target=self._audio_worker, daemon=True)
            self.audio_thread.start()
            
            # Broadcast presence
            self._broadcast_presence()
            
            print(f"Network manager started on port {self.port}")
            
        except Exception as e:
            print(f"Error starting network manager: {e}")
            self.running = False
            
    def stop(self):
        """Stop the network manager."""
        self.running = False
        
        if self.udp_socket:
            self.udp_socket.close()
        if self.discovery_socket:
            self.discovery_socket.close()
        if self.audio_socket:
            self.audio_socket.close()
            
        print("Network manager stopped")
        
    def _get_local_ip(self) -> str:
        """Get the local IP address."""
        try:
            # Create a socket to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
            
    def _broadcast_presence(self):
        """Broadcast presence to other users on the network."""
        if not self.running:
            return
            
        try:
            presence_data = {
                'type': 'presence',
                'username': self.username,
                'shop_location': self.shop_location,
                'ip_address': self.local_ip,
                'port': self.port,
                'timestamp': time.time()
            }
            
            # Broadcast to discovery port
            message = json.dumps(presence_data).encode()
            self.discovery_socket.sendto(message, ('<broadcast>', self.discovery_port))
            
        except Exception as e:
            print(f"Error broadcasting presence: {e}")
            
    def _discovery_worker(self):
        """Worker thread for discovering other users."""
        while self.running:
            try:
                self.discovery_socket.settimeout(1.0)
                data, addr = self.discovery_socket.recvfrom(1024)
                
                if data:
                    message = json.loads(data.decode())
                    
                    if message['type'] == 'presence':
                        self._handle_presence(message, addr[0])
                    elif message['type'] == 'offline':
                        self._handle_offline(message)
                        
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Discovery error: {e}")
                
        print("Discovery worker stopped")
        
    def _audio_worker(self):
        """Worker thread for receiving audio data."""
        while self.running:
            try:
                self.audio_socket.settimeout(1.0)
                data, addr = self.audio_socket.recvfrom(65536)  # Large buffer for audio
                
                if data:
                    # Parse audio packet
                    try:
                        packet_data = json.loads(data.decode())
                        audio_packet = AudioPacket(
                            sender=packet_data['sender'],
                            sender_shop=packet_data['sender_shop'],
                            timestamp=packet_data['timestamp'],
                            audio_data=bytes.fromhex(packet_data['audio_data']),
                            sequence_number=packet_data['sequence_number']
                        )
                        
                        if self.on_audio_received:
                            self.on_audio_received(audio_packet)
                            
                    except Exception as e:
                        print(f"Error parsing audio packet: {e}")
                        
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Audio worker error: {e}")
                
        print("Audio worker stopped")
        
    def _handle_presence(self, message: dict, ip_address: str):
        """Handle presence message from another user."""
        user_key = f"{message['username']}@{message['shop_location']}"
        
        if user_key not in self.users:
            # New user discovered
            user = User(
                username=message['username'],
                shop_location=message['shop_location'],
                ip_address=ip_address,
                port=message['port'],
                last_seen=time.time()
            )
            
            self.users[user_key] = user
            
            if self.on_user_discovered:
                self.on_user_discovered(user)
                
            print(f"User discovered: {user.username} at {user.shop_location}")
        else:
            # Update existing user
            self.users[user_key].last_seen = time.time()
            self.users[user_key].is_online = True
            
    def _handle_offline(self, message: dict):
        """Handle offline message from another user."""
        user_key = f"{message['username']}@{message['shop_location']}"
        
        if user_key in self.users:
            self.users[user_key].is_online = False
            
            if self.on_user_offline:
                self.on_user_offline(self.users[user_key])
                
            print(f"User went offline: {self.users[user_key].username}")
            
    def send_audio(self, target_user: str, target_shop: str, audio_data: bytes):
        """Send audio data to a specific user."""
        if not self.running:
            return
            
        try:
            user_key = f"{target_user}@{target_shop}"
            
            if user_key not in self.users:
                print(f"User {user_key} not found")
                return
                
            user = self.users[user_key]
            
            # Create audio packet
            packet = AudioPacket(
                sender=self.username,
                sender_shop=self.shop_location,
                timestamp=time.time(),
                audio_data=audio_data,
                sequence_number=self.audio_sequence
            )
            
            # Convert to JSON and send
            packet_data = {
                'sender': packet.sender,
                'sender_shop': packet.sender_shop,
                'timestamp': packet.timestamp,
                'audio_data': packet.audio_data.hex(),
                'sequence_number': packet.sequence_number
            }
            
            message = json.dumps(packet_data).encode()
            self.audio_socket.sendto(message, (user.ip_address, self.audio_port))
            
            self.audio_sequence += 1
            
        except Exception as e:
            print(f"Error sending audio: {e}")
            
    def get_online_users(self) -> List[User]:
        """Get list of online users."""
        return [user for user in self.users.values() if user.is_online]
        
    def send_offline_notification(self):
        """Send offline notification to other users."""
        if not self.running:
            return
            
        try:
            offline_data = {
                'type': 'offline',
                'username': self.username,
                'shop_location': self.shop_location,
                'timestamp': time.time()
            }
            
            message = json.dumps(offline_data).encode()
            self.discovery_socket.sendto(message, ('<broadcast>', self.discovery_port))
            
        except Exception as e:
            print(f"Error sending offline notification: {e}")
            
    def cleanup(self):
        """Clean up network resources."""
        self.send_offline_notification()
        self.stop()
