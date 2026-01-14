"""
OpenSecondDisplay - Receiver GUI
Role: Receiver Engineer

Description:
    Tkinter-based GUI for starting the Receiver.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import sys
import os
import config

import socket

# Global state
running_process = None

def get_ip():
    try:
        # Connect to an external server (doesn't send data) to get the preferred interface IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def start_listening():
    global running_process
    
    # 1. Update Config based on UI inputs
    port = port_entry.get()
    fullscreen = fullscreen_var.get()
    
    # Pass via monkey-patching since we import receiver
    import receiver
    receiver.config.PORT = port
    receiver.config.FULLSCREEN = fullscreen
    
    # UI Update
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)
    status_label.config(text=f"Status: Listening on Port {port}...", fg="green")
    
    def run():
        # Receiver main loop blocks usually, but we need to control it.
        # We will assume receiver.py is refactored similar to sender.py
        try:
            receiver.main()
        except:
            pass
        
        # Finished
        try:
            start_btn.config(state=tk.NORMAL)
            stop_btn.config(state=tk.DISABLED)
            status_label.config(text="Status: Stopped", fg="black")
        except:
            pass

    t = threading.Thread(target=run, daemon=True)
    t.start()

def stop_listening():
    import receiver
    receiver.stop_receiver_signal()
    status_label.config(text="Status: Stopping...", fg="orange")

# --- UI Setup ---
root = tk.Tk()
root.title("OpenSecondDisplay Receiver")
root.geometry("300x250")
root.resizable(False, False)

header = tk.Label(root, text="📺 Receiver", font=("Arial", 16, "bold"))
header.pack(pady=(10, 5))

ip_label = tk.Label(root, text=f"IP: {get_ip()}", font=("Arial", 12), fg="blue")
ip_label.pack(pady=(0, 10))

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Port:").grid(row=0, column=0, sticky="e", pady=5)
port_entry = tk.Entry(form_frame)
port_entry.insert(0, str(config.PORT))
port_entry.grid(row=0, column=1, pady=5)

fullscreen_var = tk.BooleanVar(value=config.FULLSCREEN)
fs_check = tk.Checkbutton(form_frame, text="Fullscreen", variable=fullscreen_var)
fs_check.grid(row=1, column=1, pady=5, sticky="w")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

start_btn = tk.Button(btn_frame, text="Start Listening", bg="green", fg="white", command=start_listening)
start_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(btn_frame, text="Stop", bg="red", fg="white", state=tk.DISABLED, command=stop_listening)
stop_btn.pack(side=tk.RIGHT, padx=5)

status_label = tk.Label(root, text="Status: Idle", font=("Arial", 10))
status_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
