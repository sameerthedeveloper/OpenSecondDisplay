# 🖥️ OpenSecondDisplay

**Turn your Linux machine into a low-latency secondary display for macOS.**

OpenSecondDisplay is a lightweight, open-source tool that uses **FFmpeg** and **Python** to stream your macOS desktop to a Linux device over a local network (LAN). No proprietary SDKs, no cloud servers, just pure raw TCP streaming.

---

## 🚀 Features

- **Low Latency**: Optimized FFmpeg logic (`ultrafast` preset, `zerolatency` tune).
- **Cross-Platform**: macOS Sender -> Linux Receiver.
- **Wireless/Wired**: Works over any LAN (Ethernet recommended).
- **Zero Bloat**: No Electron, no web servers. just `python3` and `ffmpeg`.

---

## 🛠️ Prerequisites

### macOS (Sender)
1.  **Homebrew**: Required to install dependencies.
2.  **Unblock Security**: You will need to allow Terminal/Python to record the screen.
```bash
brew install ffmpeg python3
```

### Linux (Receiver)
1.  **FFmpeg/FFplay**: Usually available in standard repos.
```bash
sudo apt update && sudo apt install ffmpeg python3
# OR
sudo dnf install ffmpeg python3
```

---

## 📥 Installation

1.  **Clone the Repository** on **BOTH** machines:
    ```bash
    git clone https://github.com/yourusername/duodisplay.git
    cd duodisplay
    ```

---

## ⚡ Usage Guidelines

### Step 1: Start the Receiver (Linux)
The receiver waits for a connection.
1.  Edit `receiver/config.py` if you want to change the port (Default: 12345).
2.  Run:
    ```bash
    python3 receiver/receiver.py
    ```
    *It will say: "Waiting for connection..."*

### Step 2: Start the Sender (macOS)
1.  Edit `sender/config.py`:
    -   **Set `RECEIVER_IP`** to your Linux machine's IP address.
    -   (Optional) Check `SCREEN_INDEX`. Run `ffmpeg -f avfoundation -list_devices true -i ""` to find your screen ID.
2.  Run:
    ```bash
    python3 sender/sender.py
    ```

### Step 3: Enjoy
Your macOS screen should appear on the Linux display in full screen!
- **To Exit**: Press `Ctrl+C` in the terminal on either side.

---

## ⚠️ Known Limitations
- **Audio**: Video only (MVP).
- **Latency**: Dependent on network. WiFi may have jitter. Ethernet is <60ms.
- **Privacy**: The stream is **unencrypted TCP**. Use only on trusted LANs.

## 🗺️ Roadmap
- [ ] Audio Forwarding
- [ ] Easy GUI Wrapper
- [ ] SRT Protocol Support (for lossy Networks)
- [ ] Wayland Native Client (currently uses XWayland via FFplay)

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
