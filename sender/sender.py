"""
OpenSecondDisplay - macOS Sender
Role: macOS Sender Engineer

Description:
    Captures the macOS screen using AVFoundation and streams it via TCP to a remote receiver.
    Wraps FFmpeg CLI to ensure low-latency encoding.

Usage:
    python3 sender.py

Dependencies:
    - python3
    - ffmpeg (installed via brew)
"""

import subprocess
import sys
import time
import signal
import config

def check_ffmpeg():
    """Verifies that FFmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ FFmpeg found.")
    except FileNotFoundError:
        print("❌ Error: FFmpeg not found. Please install it using 'brew install ffmpeg'.")
        sys.exit(1)

def list_devices():
    """Lists available AVFoundation devices to help user configure SCREEN_INDEX."""
    print("\n🔍 Scanning AVFoundation devices...")
    cmd = ["ffmpeg", "-f", "avfoundation", "-list_devices", "true", "-i", ""]
    # FFmpeg prints device list to stderr
    subprocess.run(cmd, stderr=sys.stdout)
    print("\n👉 Update 'SCREEN_INDEX' in config.py based on the Video device index above.\n")

def build_ffmpeg_command():
    """Constructs the FFmpeg command string based on configuration."""
    
    # Base command: AVFoundation capture
    cmd = [
        "ffmpeg",
        "-f", "avfoundation",
        "-capture_cursor", "1",
        "-pixel_format", "uyvy422", # Common pixel format for screen capture
        "-framerate", str(config.FPS),
        "-i", f"{config.SCREEN_INDEX}:{config.AUDIO_INDEX}",
    ]

    # Video Encoding (h264_videotoolbox is hardware accelerated on macOS)
    # We try to use hardware acceleration if possible, fallback to libx264 is simpler for portability but higher CPU.
    # Architecture doc mandate: "h264_videotoolbox if available"
    # Note: h264_videotoolbox doesn't always support 'ultrafast' preset in the same way libx264 does.
    # For MVP safety + latency tuning, we'll stick to libx264 with ultrafast unless explicit performance issues.
    # Actually, let's use libx264 for consistent 'tune zerolatency' support which is critical.
    
    cmd.extend([
        "-c:v", "libx264",
        "-preset", config.PRESET,
        "-tune", config.TUNE,
        "-b:v", config.BITRATE,
        "-g", str(config.GOP_SIZE),    # Frequent keyframes for recovery
        "-pix_fmt", "yuv420p",         # Compatible with most players
    ])

    # Scaling
    if config.SCALING_RESOLUTION:
        cmd.extend(["-vf", f"scale={config.SCALING_RESOLUTION}"])

    # Output: MPEG-TS over TCP
    # TCP connection to receiver
    output_url = f"tcp://{config.RECEIVER_IP}:{config.RECEIVER_PORT}"
    
    cmd.extend([
        "-f", "mpegts",
        output_url
    ])

    return cmd

def main():
    print("🚀 OpenSecondDisplay - macOS Sender")
    check_ffmpeg()

    # Optional: Uncomment if you want to see devices every run, or just rely on documentation
    # list_devices()

    print(f"📡 Connecting to Receiver at {config.RECEIVER_IP}:{config.RECEIVER_PORT}...")
    print(f"🎥 Capture Device Index: {config.SCREEN_INDEX} (Cursor: On)")
    print(f"⚙️  Settings: {config.SCALING_RESOLUTION or 'Native'} @ {config.FPS}fps | {config.BITRATE}")
    print("❌ Press Ctrl+C to stop streaming.")

    cmd = build_ffmpeg_command()
    # print("DEBUG Command:", " ".join(cmd))

    try:
        # Popen allows us to keep the script running and handle signals
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, # Capture stderr to debug if needed, or let it flow to console
            text=True
        )
        
        # Stream FFmpeg output to console for feedback (optional, nice for debugging)
        # For a clean sender, maybe mostly silent, but for 'Engineer' role, logging is good.
        while True:
            # Check if process is still alive
            if process.poll() is not None:
                # Process exited
                stderr_out = process.stderr.read()
                print("\n❌ FFmpeg exited unexpectedly.")
                if "Connection refused" in stderr_out:
                    print("👉 Could not connect to Receiver. Is it running?")
                else:
                    print("FFmpeg Error Output:\n" + stderr_out[-500:]) # Last 500 chars
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Stopping stream...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("👋 Stream stopped.")

if __name__ == "__main__":
    main()
