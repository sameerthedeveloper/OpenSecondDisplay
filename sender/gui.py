"""
OpenSecondDisplay - macOS Sender GUI
Role: macOS Sender Engineer

Description:
    Tkinter-based GUI for starting the Sender.
    Allows user to configure IP, Port, and Resolution before starting.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import sys
import os
import config
import socket
import time

# Global process handle
process = None

def get_sender_script_path():
    """Returns the path to sender.py or the internal executable path."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return os.path.join(sys._MEIPASS, "sender.py")
    else:
        # Running as script
        return os.path.join(os.path.dirname(__file__), "sender.py")

def start_stream():
    global process
    
    # 1. Update Config based on UI inputs
    ip = ip_entry.get()
    port = port_entry.get()
    resolution = resolution_var.get()
    
    if not ip:
        messagebox.showerror("Error", "Please enter Receiver IP")
        return

    # Update global config (in memory, usually scripts read from file but we pass args or env)
    # Since we are wrapping sender.py (which reads config.py), we need a way to pass these.
    # The current sender.py reads config.py directly. 
    # For this GUI to work effectively with the existing logic, we can pass Env Vars
    # or modify sender.py to accept arguments.
    # Architecture decision: Pass via Environment Variables for minimal code change.
    
    env = os.environ.copy()
    env["OSD_RECEIVER_IP"] = ip
    env["OSD_RECEIVER_PORT"] = port
    env["OSD_SCALING_RESOLUTION"] = resolution if resolution != "Native" else ""
    
    # Disable UI
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)
    status_label.config(text="Status: Streaming...", fg="green")

    # Run sender.py in a thread
    def run_sender():
        global process
        cmd = [sys.executable, get_sender_script_path()] if not getattr(sys, 'frozen', False) else [sys.executable]
        # Important: If it's a onefile exe, sys.executable is the exe itself. But sender logic is inside main.
        # Wait, if we package GUI as the entry point, we need to import main from sender.
        
        # BETTER APPROACH: Import 'main' from sender.py and run it in a thread.
        # But sender.py has a blocking loop. We need to handle it.
        # Let's stick to subprocess because sender.py uses subprocess.run/Popen for ffmpeg anyway.
        # If we package as onefile, we can bundle ffmpeg or rely on system ffmpeg.
        
        # Real-world fix for "frozen" app invoking internal logic:
        # If we just import sender, we can call its main(). But we need the config override.
        # Let's Modify sender.py to look for Env Vars! (Will do next).
        
        # In this implementation, I will assume sender.py will be modified to support ENV vars.
        
        # If "frozen", we are the executable. We can't subprocess "sender.py" easily if it's not external.
        # So we should import sender.
        pass

    # Threading logic to keep GUI responsive
    t = threading.Thread(target=run_process, args=(env,))
    t.start()

def run_process(env):
    global process
    # Just calling the ffmpeg command construction logic would be cleaner, 
    # but re-using sender.py via subprocess ensures strict isolation.
    # However, for PyInstaller single-file, subprocess is tricky. 
    # Let's use the IMPORT method.
    
    try:
        import sender
        # Monkey patch config
        sender.config.RECEIVER_IP = env["OSD_RECEIVER_IP"]
        sender.config.RECEIVER_PORT = env["OSD_RECEIVER_PORT"]
        res = env["OSD_SCALING_RESOLUTION"]
        sender.config.SCALING_RESOLUTION = res if res else None
        
        # Sender main loop is blocking. We run it here.
        # We need a way to kill it. sender.py uses Popen. 
        # We will modify sender.py to return the process handle or expose it.
        
        # For now, let's assume sender.py has a global or class we can instantiate.
        # To avoid complex refactoring now, let's just use subprocess for the FFMPEG call inside sender.
        # We will modify sender.py to be more import-friendly.
        
        sender.main() 
        
    except Exception as e:
        print(e)
        
    # When sender finishes
    try:
        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)
        status_label.config(text="Status: Stopped", fg="black")
    except:
        pass

def stop_stream():
    # We need a way to stop the sender.main() loop or the ffmpeg process it spawned.
    # This requires sender.py to expose a stop function.
    import sender
    # We will implement a stop signal in sender.py
    sender.stop_stream_signal()
    
    status_label.config(text="Status: Stopping...", fg="orange")

# --- UI Setup ---
root = tk.Tk()
root.title("OpenSecondDisplay Sender")
root.geometry("400x350")
root.resizable(False, False)

# Logo/Header
header = tk.Label(root, text="🖥️ Sender (macOS)", font=("Arial", 16, "bold"))
header.pack(pady=10)

# Form
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Receiver IP:").grid(row=0, column=0, sticky="e", pady=5)
ip_entry = tk.Entry(form_frame)
ip_entry.insert(0, config.RECEIVER_IP)
ip_entry.grid(row=0, column=1, pady=5)

def scan_receivers():
    try:
        status_label.config(text="Status: Scanning...", fg="orange")
        root.update()
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1.0)
        
        message = b"OSD_DISCOVER"
        sock.sendto(message, ('255.255.255.255', config.DISCOVERY_PORT))
        
        found = []
        start_time = time.time()
        while time.time() - start_time < 1.0:
            try:
                data, addr = sock.recvfrom(1024)
                text = data.decode()
                if text.startswith("OSD_ACK:"):
                    parts = text.split(":")
                    if len(parts) >= 3:
                        hostname = parts[1]
                        ip = parts[2]
                        found.append((hostname, ip))
            except socket.timeout:
                break
            except:
                pass
                
        sock.close()
        
        if not found:
            messagebox.showinfo("Scan Result", "No receivers found.")
            status_label.config(text="Status: Ready", fg="black")
        elif len(found) == 1:
            hostname, ip = found[0]
            ip_entry.delete(0, tk.END)
            ip_entry.insert(0, ip)
            status_label.config(text=f"Found: {hostname} ({ip})", fg="green")
            messagebox.showinfo("Scan Result", f"Found: {hostname}\nIP: {ip}\n(Auto-filled)")
        else:
            # Multiple found - naive Approach: pick first or list all
            # For MVP: autofill first and show count
            hostname, ip = found[0]
            ip_entry.delete(0, tk.END)
            ip_entry.insert(0, ip)
            msg = "Found Receivers:\n" + "\n".join([f"{h} ({i})" for h, i in found])
            messagebox.showinfo("Scan Result", msg)
            status_label.config(text=f"Found {len(found)} - Selected {hostname}", fg="green")
            
    except Exception as e:
        messagebox.showerror("Error", f"Scan failed: {e}")
        status_label.config(text="Status: Error", fg="red")

scan_btn = tk.Button(form_frame, text="Scan", command=scan_receivers)
scan_btn.grid(row=0, column=2, padx=5)

tk.Label(form_frame, text="Port:").grid(row=1, column=0, sticky="e", pady=5)
port_entry = tk.Entry(form_frame)
port_entry.insert(0, str(config.RECEIVER_PORT))
port_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Resolution:").grid(row=2, column=0, sticky="e", pady=5)
resolution_var = tk.StringVar(value="1280:720")
res_dropdown = tk.OptionMenu(form_frame, resolution_var, "Native", "1920:1080", "1280:720", "1024:768")
res_dropdown.grid(row=2, column=1, pady=5)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

start_btn = tk.Button(btn_frame, text="Start Stream", bg="green", fg="white", command=start_stream)
start_btn.pack(side=tk.LEFT, padx=10)

stop_btn = tk.Button(btn_frame, text="Stop Stream", bg="red", fg="white", state=tk.DISABLED, command=stop_stream)
stop_btn.pack(side=tk.RIGHT, padx=10)

# Status
status_label = tk.Label(root, text="Status: Ready", font=("Arial", 10))
status_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
