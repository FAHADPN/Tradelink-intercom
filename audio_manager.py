import pyaudio
import numpy as np
import threading
import time
from typing import Optional, Callable

class AudioManager:
    """Manages high-quality audio capture and playback for the intercom system."""
    
    def __init__(self, sample_rate: int = 44100, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        
        # Audio streams
        self.input_stream: Optional[pyaudio.Stream] = None
        self.output_stream: Optional[pyaudio.Stream] = None
        
        # Callbacks
        self.on_audio_data: Optional[Callable[[bytes], None]] = None
        self.on_playback_request: Optional[Callable[[bytes], None]] = None
        
        # State
        self.is_recording = False
        self.is_playing = False
        self.recording_thread: Optional[threading.Thread] = None
        
        # Audio quality settings
        self.channels = 1  # Mono for better performance
        self.format = pyaudio.paInt16
        
    def start_recording(self, on_data_callback: Callable[[bytes], None]):
        """Start recording audio from microphone."""
        if self.is_recording:
            return
            
        self.on_audio_data = on_data_callback
        self.is_recording = True
        
        try:
            self.input_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            
            self.input_stream.start_stream()
            print("Audio recording started")
            
        except Exception as e:
            print(f"Error starting audio recording: {e}")
            self.is_recording = False
            
    def stop_recording(self):
        """Stop recording audio."""
        self.is_recording = False
        
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
            self.input_stream = None
            
        print("Audio recording stopped")
        
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio input stream."""
        if self.is_recording and self.on_audio_data:
            # Apply noise reduction and enhance audio quality
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            
            # Simple noise gate (remove very quiet sounds)
            threshold = 500
            audio_data = np.where(np.abs(audio_data) < threshold, 0, audio_data)
            
            # Convert back to bytes
            processed_data = audio_data.tobytes()
            self.on_audio_data(processed_data)
            
        return (in_data, pyaudio.paContinue)
        
    def play_audio(self, audio_data: bytes):
        """Play received audio data."""
        if self.is_playing:
            return
            
        self.is_playing = True
        
        try:
            self.output_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.chunk_size
            )
            
            # Play the audio data
            self.output_stream.write(audio_data)
            self.output_stream.stop_stream()
            self.output_stream.close()
            self.output_stream = None
            
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            self.is_playing = False
            
    def get_available_devices(self):
        """Get list of available audio input and output devices."""
        devices = {
            'input': [],
            'output': []
        }
        
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                devices['input'].append({
                    'index': i,
                    'name': device_info['name'],
                    'channels': device_info['maxInputChannels']
                })
            if device_info['maxOutputChannels'] > 0:
                devices['output'].append({
                    'index': i,
                    'name': device_info['name'],
                    'channels': device_info['maxOutputChannels']
                })
                
        return devices
        
    def set_input_device(self, device_index: int):
        """Set the input device for recording."""
        # Stop current recording if active
        if self.is_recording:
            self.stop_recording()
            
        # Update device index for next recording session
        self.input_device_index = device_index
        
    def set_output_device(self, device_index: int):
        """Set the output device for playback."""
        self.output_device_index = device_index
        
    def cleanup(self):
        """Clean up audio resources."""
        self.stop_recording()
        if self.audio:
            self.audio.terminate()
            
    def get_audio_levels(self) -> float:
        """Get current audio input level for VU meter."""
        if not self.is_recording or not self.input_stream:
            return 0.0
            
        try:
            # Get current audio data
            data = self.input_stream.read(self.chunk_size, exception_on_overflow=False)
            audio_array = np.frombuffer(data, dtype=np.int16)
            
            # Calculate RMS level
            rms = np.sqrt(np.mean(audio_array**2))
            # Normalize to 0-1 range
            level = min(1.0, rms / 32768.0)
            
            return level
        except:
            return 0.0
