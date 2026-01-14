# 🖥️ OpenSecondDisplay

**Turn your Linux machine into a low-latency secondary display for macOS.**

OpenSecondDisplay is a lightweight, open-source tool that uses **FFmpeg** and **Python** to stream your macOS desktop to a Linux device over a local network (LAN). No proprietary SDKs, no cloud servers, just pure raw TCP streaming.

---

## 🚀 Features

- **Low Latency**: Optimized FFmpeg logic (`ultrafast` preset, `zerolatency` tune).
- **Cross-Platform**: macOS Sender -> Linux/Windows Receiver.
- **GUI Launchers**: Easy-to-use interface (no terminal required).
- **Zero Bloat**: No Electron, no web servers. just `python3` and `ffmpeg`.

---

## 📥 Installation & Usage

### 🍏 macOS (Sender)
1.  **Download**: Go to [Releases](https://github.com/sameerthedeveloper/OpenSecondDisplay/releases) and download `OpenSecondDisplay-Sender.dmg`.
2.  **Install**: Open the DMG and drag the app to your Applications folder.
3.  **Run**: Open "OpenSecondDisplay Sender". You may need to "Right Click > Open" the first time if not notarized.
4.  **Connect**: Enter the Receiver's IP and click **Start Stream**.

### 🐧 Linux (Receiver)
1.  **Download**: Go to [Releases](https://github.com/sameerthedeveloper/OpenSecondDisplay/releases) and download `openseconddisplay-receiver_1.1.3_amd64.deb`.
2.  **Install**:
    ```bash
    sudo dpkg -i openseconddisplay-receiver_1.1.3_amd64.deb
    sudo apt-get install -f  # Fix dependencies if needed
    ```
3.  **Run**:
    -   **Via Terminal**: Run `openseconddisplay-receiver`.
    -   **Via Menu**: Search for "OpenSecondDisplay" in your app drawer.

### 🪟 Windows (Receiver)
1.  **Download**: Download `OpenSecondDisplay-Receiver.exe`.
2.  **Run**: Double-click to start.
3.  **Firewall**: Allow the app through Windows Firewall if prompted.

---

## 🛠️ Manual Setup (For Developers)

### Linux (Receiver)
1.  **FFmpeg/FFplay**: Usually available in standard repos.
```bash
sudo apt update && sudo apt install ffmpeg python3 python3-tk
```
2.  **Clone**: `git clone https://github.com/sameerthedeveloper/OpenSecondDisplay.git`
3.  **Run**: `python3 receiver/gui.py`

### macOS (Sender)
1.  **Homebrew**: `brew install ffmpeg python3 python-tk`
2.  **Clone**: `git clone ...`
3.  **Run**: `python3 sender/gui.py`

---

## ⚠️ Known Limitations
- **Audio**: Video only (MVP).
- **Latency**: Dependent on network. WiFi may have jitter. Ethernet is <60ms.
- **Privacy**: The stream is **unencrypted TCP**. Use only on trusted LANs.

## 🗺️ Roadmap
- [ ] Audio Forwarding
- [ ] SRT Protocol Support (for lossy Networks)
- [ ] Wayland Native Client (currently uses XWayland via FFplay)

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
