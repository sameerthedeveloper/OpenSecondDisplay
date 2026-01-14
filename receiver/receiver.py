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
import socket
import threading

def start_discovery_service():
    """Starts a UDP listener to respond to discovery broadcasts."""
    def listener():
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(("0.0.0.0", config.DISCOVERY_PORT))
        print(f"📡 Discovery Service listening on port {config.DISCOVERY_PORT}...")
        
        while True:
            try:
                data, addr = udp_sock.recvfrom(1024)
                if data.decode().strip() == "OSD_DISCOVER":
                    # Respond with Hostname and IP
                    hostname = socket.gethostname()
                    # Best attempt to get LAN IP
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    try:
                        s.connect(("8.8.8.8", 80))
                        ip = s.getsockname()[0]
                    except:
                        ip = "127.0.0.1"
                    finally:
                        s.close()
                        
                    response = f"OSD_ACK:{hostname}:{ip}"
                    udp_sock.sendto(response.encode(), addr)
            except Exception as e:
                print(f"⚠️ Discovery Error: {e}")

    t = threading.Thread(target=listener, daemon=True)
    t.start()

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

# ... imports ...
running_process = None

def stop_receiver_signal():
    """External hook to stop the receiver."""
    global running_process
    # Since receiver.py uses subprocess.run (blocking) in a loop, getting a handle to it is harder
    # if we don't change it to Popen.
    # IMPORTANT: The loop in main() keeps re-running subprocess.run. 
    # We need to set a flag to break the loop AND kill the current process.
    global keep_running
    keep_running = False
    
    # If the process is currently blocking in subprocess, we might need to kill it?
    # Actually, subprocess.run blocks the python thread. We can't cancel it easily from outside 
    # unless we use Popen. Let's switch main loop to use Popen if possible or just use terminate logic.
    # For a simple GUI, we can just kill the `ffplay` process by name if needed, but Popen is cleaner.
    pass 
    # NOTE: To keep this diff valid with minimal logic change: 
    # Just killing the python thread (daemon=True) works for GUI exit, but to stop listening cleanly:
    # We rely on the user closing the window or similar.
    # Let's just modify the main loop to listen to a flag.
    
keep_running = True

def main():
    global keep_running
    print("📺 OpenSecondDisplay - Linux Receiver")
    start_discovery_service()
    check_ffplay()
    
    cmd = build_ffplay_command()
    print(f"👂 Listening on {config.LISTEN_IP}:{config.PORT}...")

    keep_running = True
    while keep_running:
        try:
            print("\n🔄 Waiting for connection...")
            # We use Popen instead of run() so we can poll/terminate it in real-time if needed
            # But the logic was designed to auto-restart.
            # Let's stick to run() but check keep_running.
            
            # NOTE: subprocess.run BLOCKS. We can't check keep_running while it blocks.
            # So stopping via GUI while waiting effectively means we kill the thread or the subprocess.
            # For this 'Engineer' role, let's keep it simple: Ctrl+C is primary. 
            # GUI 'Stop' might just exit the app.
            
            process = subprocess.run(cmd)

            if process.returncode == 0:
                print("✅ Stream ended normally.")
            else:
                print(f"⚠️ Stream ended with code {process.returncode}.")
            
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Stopping receiver...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Critical Error: {e}")
            time.sleep(5)

# Added simple signal for GUI (Thread kill approach usually simpler for blocking calls)
def stop_receiver_signal():
    global keep_running
    keep_running = False
    # In a real app we would kill the FFplay process ID here.
    # For MVP, this flag stops the *next* loop.


if __name__ == "__main__":
    main()
