# Networking & Performance Tuning
**Role:** Networking & Performance Engineer

## 1. Transmission Protocol: TCP vs UDP
We selected **TCP** (MPEG-TS) for the MVP for the following reasons:
- **Reliability:** No artifacts from dropped packets (video glitching).
- **Simplicity:** FFmpeg/FFplay native support via `tcp://`.
- **Trade-off:** Slightly higher latency than UDP/RTP, but easier to traverse NAT/Firewalls within LAN.

*Future Optimization: Switch to SRT (Secure Reliable Transport) or RTP for unstable networks.*

## 2. Low-Latency FFmpeg Flags (Implemented)

### Sender (`sender.py`)
| Flag | Value | Effect |
|------|-------|--------|
| `-preset` | `ultrafast` | Minimizes encoding CPU usage and delay. |
| `-tune` | `zerolatency` | Disables frame reordering (B-frames), pushing frames immediately. |
| `-g` | `30` | Keyframe every 30 frames (1 sec @ 30fps). Fast recovery from corruption. |
| `-vf scale` | `1280:720` | Downscaling significantly improves encoding speed and reduces bandwidth. |

### Receiver (`receiver.py`)
| Flag | Value | Effect |
|------|-------|--------|
| `-fflags` | `nobuffer` | Tells decoder to output frames as soon as they arrive. |
| `-flags` | `low_delay` | Signal codec to minimize delay. |
| `-probesize` | `32` | Reduce analysis buffer to ~0 bytes to start immediately. |
| `-vf setpts` | `0` | Discard timestamps and play frames ASAP. |

## 3. Network Tuning Guide

### 3.1 Use Ethernet
**WiFi is the enemy of low latency.** 
- **Ethernet:** Consistent <1ms ping.
- **WiFi:** Jitter varies from 2ms to 100ms+, causing stutter.

### 3.2 Reduce Buffer Bloat
If you experience a delay that "grows" over time:
1.  Check `config.py` in `receiver` and ensure `FFLAGS = "nobuffer"`.
2.  Reduce `sender` Resolution.

### 3.3 Latency Benchmarking
To measure end-to-end latency:
1.  Start Sender and Receiver.
2.  Open a stopwatch/timer window on the Sender screen.
3.  Take a photo (or high-speed video) capturing both screens.
4.  **Latency = Receiver Time - Sender Time**.

**Targets:**
- **Excellent:** < 60ms
- **Good:** < 100ms
- **usable:** < 200ms

## 4. Failure Scenarios

### "Connection Refused"
- **Cause:** Receiver is not running or Firewall blocking port 12345.
- **Fix:** Start `receiver.py` first. Allow port 12345 (TCP) on Linux firewall (`sudo ufw allow 12345/tcp`).

### "Green Artifacts / Smearing"
- **Cause:** Network Packet Loss or CPU overload.
- **Fix:** Lower `BITRATE` in `sender/config.py` (try "2000k").
