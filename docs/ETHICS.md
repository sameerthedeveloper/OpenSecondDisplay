# Ethics, Security & Compliance
**Role:** Open-Source & Ethics Reviewer

## 1. Open Source Compatibility
- **Tools Used:** Python 3 (PSF License), FFmpeg (LGPL/GPL).
- **Compliance:** This project uses FFmpeg as a command-line subprocess (`subprocess` in Python), which complies with LGPL requirements by dynamic linking (runtime execution). We do not statically link FFmpeg.
- **License Recommended:** MIT. This allows maximum freedom for users to modify specific flags for their hardware without restriction.

## 2. Ethical Compliance Checklist
- [x] **No DRM Bypass:** The tool captures the *user's own desktop*. It does not decrypt HDCP or protected content streams.
- [x] **User Consent:** The tool runs visibly in a terminal. It requires explicit user action to start.
- [x] **No Hidden Data Collection:** No telemetry, no "phone home", no analytics. The code is 100% auditable Python.
- [x] **OS Integrity:** The tool uses standard OS APIs (AVFoundation) and does not require disabling SIP (System Integrity Protection) on macOS.

## 3. Security Considerations
> [!WARNING]
> **This protocol is Unencrypted.**

- **Risk:** The TCP stream contains raw/compressed video data of your screen. Anyone on the same LAN segment could potentially capture packets and reconstruct the video.
- **Mitigation:**
    -   **Use on Trusted LANs Only:** Do not use on Public WiFi (cafes, airports).
    -   **Future Work:** Implementation of `SRT` with encryption or tunneling over SSH (`ssh -L`).

## 4. Privacy Statement
**OpenSecondDisplay collects NO data.**
- All processing happens locally on your device.
- No data is sent to the cloud.
- No third-party API calls are made.
