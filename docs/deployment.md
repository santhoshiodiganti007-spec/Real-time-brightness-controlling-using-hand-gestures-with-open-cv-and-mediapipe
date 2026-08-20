# Deployment Strategy & Distinction

## Local Desktop Mode vs Cloud Dashboard Mode

### Local Desktop Mode (Full Capabilities)
- **Architecture:** Runs locally on the user's host machine.
- **Webcam:** Accesses host webcam via OpenCV.
- **Screen Control:** Controls physical display monitor brightness using `screen_brightness_control`.
- **Packaging:** Can be compiled into standalone Windows executable `TouchlessBrightnessControl.exe`.

### Cloud / Docker Dashboard Mode (Monitoring & Telemetry)
- **Architecture:** Deployed to Vercel/Render/Docker containers.
- **Webcam:** Uses synthetic video feed or browser WebRTC camera input.
- **Screen Control:** Operates in **DEMO MODE**.
- **Important Technical Distinction:** Cloud servers cannot directly modify physical display hardware connected to a remote end-user's workstation. Cloud deployment serves for monitoring, analytics, settings sync, and demonstration purposes.
