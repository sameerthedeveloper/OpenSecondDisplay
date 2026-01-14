# 🔧 Troubleshooting Guide

## ❌ "Connection Refused"
**Symptoms:** Sender script exits immediately with a connection error.
**Fixes:**
1.  **Start Receiver First**: The receiver acts as the Server (Listener). It must be running before the sender connects.
2.  **Check IP**: Verify `RECEIVER_IP` in `sender/config.py` matches the Linux machine's actual IP (`ip a` or `ifconfig`).
3.  **Firewall**: Ensure the Linux machine allows incoming TCP traffic on port 12345.
    ```bash
    sudo ufw allow 12345/tcp
    ```

## 🐢 High Latency / Lag
**Symptoms:** Cursor movement feels slow or delayed.
**Fixes:**
1.  **Use Ethernet**: WiFi jitter is the #1 cause.
2.  **Lower Resolution**: In `sender/config.py`, change `SCALING_RESOLUTION` to `"1280:720"`.
3.  **Check Buffer**: In `receiver/config.py`, ensure `FFLAGS = "nobuffer"`.

## 📺 "AvFoundation: Capture Input Error" (macOS)
**Symptoms:** Sender crashes with "Input/output error" or "Permission denied".
**Fixes:**
1.  **Permissions**: Go to **System Settings > Privacy & Security > Screen Recording**. Allow "Terminal" (or your IDE, e.g., VSCode/iTerm).
2.  **Wrong Index**: Your screen ID might not be "1". Run the device list command:
    ```bash
    ffmpeg -f avfoundation -list_devices true -i ""
    ```
    Update `SCREEN_INDEX` in `sender/config.py`.

## 🟩 Green Screen / Artifacts
**Symptoms:** Video is smeared or green blocks appear.
**Fixes:**
1.  **Packet Loss**: Your network can't handle the bitrate.
    -   In `sender/config.py`, reduce `BITRATE` to `"2000k"` (2 Mbps).
    -   Increase `GOP_SIZE` slightly (e.g., 60) to reduce bandwidth overhead, though this hurts recovery time.
