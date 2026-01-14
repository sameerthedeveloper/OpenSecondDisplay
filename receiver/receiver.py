"""
OpenSecondDisplay - Linux Receiver
Role: Linux Receiver Engineer

Description:
    Listens for an incoming TCP stream and plays it back using FFplay.
    Designed for Linux (X11/Wayland) with auto-recovery.

Usage:
    python3 receiver.py

Dependencies:
    - python3
    - ffmpeg (includes ffplay)
"""

import subprocess
import sys
import time
import config

def check_ffplay():
    """Verifies that FFplay is installed."""
    try:
        subprocess.run(["ffplay", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ FFplay found.")
    except FileNotFoundError:
        print("❌ Error: FFplay not found. Please install ffmpeg package.")
        sys.exit(1)

def build_ffplay_command():
    """Constructs the FFplay command for low-latency playback."""
    
    # Input URL: Listen mode
    input_url = f"tcp://{config.LISTEN_IP}:{config.PORT}?listen"

    cmd = [
        "ffplay",
        "-window_title", config.WINDOW_TITLE,
        "-fflags", config.FFLAGS,
        "-flags", "low_delay",
        "-strict", "experimental",
        
        # Optimization for fast start
        "-probesize", config.PROBESIZE,
        "-analyzeduration", config.ANALYZEDURATION,
        
        # Video Logic
        "-vf", "setpts=0",  # Remove timestamps to play frames immediately as they arrive
        
        # Protocol
        "-f", "mpegts",
        input_url
    ]

    if config.FULLSCREEN:
        cmd.insert(1, "-fs")

    # Hide cursor over window if possible (ffplay doesn't natively hide always, but fullscreen helps)
    
    return cmd

def main():
    print("📺 OpenSecondDisplay - Linux Receiver")
    check_ffplay()
    
    cmd = build_ffplay_command()
    print(f"👂 Listening on {config.LISTEN_IP}:{config.PORT}...")
    # print("DEBUG Command:", " ".join(cmd))

    while True:
        try:
            print("\n🔄 Waiting for connection...")
            # Run FFplay. It will block until connection, then run until stream ends.
            # If sender disconnects, FFplay usually exits.
            process = subprocess.run(cmd)

            if process.returncode == 0:
                print("✅ Stream ended normally.")
            else:
                print(f"⚠️ Stream ended with code {process.returncode}.")
            
            # Small delay to prevent tight loop in case of immediate crash
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Stopping receiver...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Critical Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
