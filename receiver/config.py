"""
OpenSecondDisplay - Linux Receiver Configuration
Role: Linux Receiver Engineer
"""

# Network Configuration
# 0.0.0.0 listens on all available interfaces
LISTEN_IP = "0.0.0.0"
PORT = 12345
DISCOVERY_PORT = 5001

# Playback Configuration
# "fullscreen" to occupy the entire monitor
FULLSCREEN = True

# Window Title
WINDOW_TITLE = "OpenSecondDisplay Receiver"

# Buffer Management (Latency vs Smoothness)
# Lower is better for latency, higher for smoothness.
# "nobuffer" reduces latency significantly.
FFLAGS = "nobuffer" 

# Probesize/Analyzeduration
# Reduce these to start playback faster, at the risk of misdetecting stream info (rare for mpegts).
PROBESIZE = "32" # Bytes
ANALYZEDURATION = "0" # Microseconds
