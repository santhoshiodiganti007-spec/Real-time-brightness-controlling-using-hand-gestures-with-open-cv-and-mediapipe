# Troubleshooting & Diagnostic Guide

## Common Issues & Solutions

### 1. Webcam Stream Not Loading
- **Cause:** Another app (Zoom, Teams, Skype) is locking camera index 0.
- **Fix:** Close competing camera applications or select camera index `1` in Settings.

### 2. Physical Brightness Does Not Change
- **Cause:** External desktop monitor connected via HDMI/DisplayPort without DDC/CI protocol enabled.
- **Fix:** Ensure DDC/CI is enabled in physical monitor OSD settings, or verify `screen_brightness_control` permissions. The app automatically enters **DEMO MODE** if physical hardware is unssupported to prevent crashes.

### 3. Rapid Brightness Flickering
- **Cause:** Low smoothing factor $\alpha$.
- **Fix:** Increase Exponential Moving Average smoothing or raise Update Threshold ($\ge 2\%$) in Settings.
