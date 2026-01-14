"""
OpenSecondDisplay - macOS Sender Configuration
Role: macOS Sender Engineer
"""

# Network Configuration
# The IP address of the Linux Receiver
RECEIVER_IP = "192.168.1.100"  # CHANGE THIS to your receiver's IP
RECEIVER_PORT = 12345
DISCOVERY_PORT = 5001

# Video Configuration
# Target resolution for scaling (width:height). 
# Set to None to use native capture resolution (high bandwidth).
# Examples: "1920:1080", "1280:720"
SCALING_RESOLUTION = "1280:720"

# Target Framerate
FPS = 30

# FFmpeg Capture Settings
# Input device index for AVFoundation. "0" is usually the first screen.
# Run 'ffmpeg -f avfoundation -list_devices true -i ""' to see indices.
SCREEN_INDEX = "1"  # "0" typically webcam on some macs, "1" is often main screen if webcam is present.
AUDIO_INDEX = "none" # Audio not supported in MVP

# Encoding Settings
# "ultrafast" gives lowest latency but higher bitrate.
PRESET = "ultrafast"
# "zerolatency" tunes the encoder for real-time streaming.
TUNE = "zerolatency"
# Bitrate control (optional). "2000k" = 2Mbps.
BITRATE = "5000k"
# GME (Group of Pictures) size. Lower = lower latency recovery, higher overhead.
GOP_SIZE = 30 
