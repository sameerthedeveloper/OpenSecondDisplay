# OpenSecondDisplay Architecture

**Role:** Product Architect (Lead)
**Version:** 1.0

## 1. High-Level Architecture

The system follows a strict **Sender-Receiver** model over TCP/IP LAN.

```mermaid
graph LR
    subgraph macOS_Sender["macOS Sender (Host)"]
        A[Screen Capture<br/>(AVFoundation)] --> B[FFmpeg Encoder]
        B --> C[TCP Sender Socket]
    end

    subgraph Linux_Receiver["Linux Receiver (Client)"]
        D[TCP Listening Socket] --> E[FFplayer / Decoder]
        E --> F[Display Output]
    end

    C -- "MPEG-TS Stream (h.264)" --> D
```

## 2. Module Boundaries

### 2.1 Sender Module (`sender/`)
- **Responsibility:** Capture user-selected screen, encode video, stream over network.
- **Input:** Screen Content, Cursor.
- **Output:** TCP Stream.
- **Constraints:**
  - Must use native `avfoundation` for capture (macOS).
  - Must use hardware acceleration (`h264_videotoolbox`) if available, or software `libx264` (ultrafast) as fallback.
  - **NO** third-party GUI libraries. CLI-based or simple wrapper.

### 2.2 Receiver Module (`receiver/`)
- **Responsibility:** Listen for incoming connection, decode stream, display full screens.
- **Input:** TCP Stream.
- **Output:** Video Render.
- **Constraints:**
  - Must run on X11 (or Wayland via XWayland).
  - Use `ffplay` for zero-code playback implementation where possible, or `cv2` if custom handling needed (but prompt says "FFplay" specifically).
  - Auto-reconnect logic.

### 2.3 Shared Configuration
- **Mechanism:** `config.py` in each module (or shared if feasible, but separated for deployment isolation).
- **Key Parameters:**
  - Host IP / Port
  - Resolution (Sender scaling)
  - Framerate (FPS)
  - Bitrate

## 3. Interaction Flow

1.  **Receiver Start**:
    - Receiver script starts.
    - Opens TCP socket (Server mode) or listens for FFmpeg stream.
    - Status: `WAITING_FOR_CONNECTION`.

2.  **Sender Start**:
    - Sender script starts.
    - Reads `config.py`.
    - Enumerates screens (finds ID).
    - Constructs FFmpeg command.
    - Connects to Receiver IP:Port.
    
3.  **Streaming**:
    - FFmpeg pipes output to TCP.
    - Receiver captures bytes -> decodes -> displays.

4.  **Teardown/Error**:
    - If TCP connection breaks:
        - Sender: Log error, attempt reconnect or exit.
        - Receiver: Clear screen (optional), return to `WAITING_FOR_CONNECTION`.

## 4. Configuration Strategy
Configuration shall be minimal and Python-native (`config.py`).

**Example `config.py` Structure:**
```python
# Network
RECEIVER_IP = "192.168.1.X"
PORT = 12345

# Video
RESOLUTION = "1920x1080"
E_FPS = 30
PRESET = "ultrafast"  # or 'realtime'
```

## 5. Error-Handling Philosophy
- **Fail Fast, recover silently (Receiver)**: Receiver should never crash completely; if stream dies, it loops and waits.
- **Log Clearly (Sender)**: Sender must output FFmpeg logs to stderr/file for debugging latency issues.
- **Graceful Exit**: `Ctrl+C` must kill the underlying FFmpeg process immediately (orphan process prevention).

## 6. Constraints Checklist (Enforced)
- [x] **Python + FFmpeg only**: Core logic in Python `subprocess` calls or `ffmpeg-python`.
- [x] **macOS Sender**: AVFoundation input device.
- [x] **Linux Receiver**: Generic compatibility.
- [x] **Open-source**: No proprietary blobs.
- [x] **LAN-only**: No external signaling servers.
