# Touchless Brightness Control Using Hand Gestures 🖐️✨☀️

[![CI/CD Pipeline](https://github.com/santhoshiodiganti007-spec/Real-time-brightness-controlling-using-hand-gestures-with-open-cv-and-mediapipe/actions/workflows/ci.yml/badge.svg)](https://github.com/santhoshiodiganti007-spec/Real-time-brightness-controlling-using-hand-gestures-with-open-cv-and-mediapipe/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React Vite](https://img.shields.io/badge/React-18%2B-cyan.svg)](https://vitejs.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade, real-time computer vision system that enables users to control their physical monitor screen brightness without touching physical controls. 

Using **MediaPipe Hand Landmarker** and **OpenCV**, the application detects hand landmarks, calculates the 2D Euclidean distance between the user's **Thumb Tip** and **Index Finger Tip**, normalizes the gesture distance, applies **Exponential Moving Average (EMA)** noise smoothing, and updates local operating system display hardware in real time.

---

## 🌟 Key Features

* **Touchless Hardware Control:** Directly adjusts local screen hardware brightness on Windows/Linux/macOS via `screen-brightness-control`.
* **Real-Time MediaPipe Hand Tracking:** Tracks 21 3D hand landmarks with visual distance lines and landmark overlays at 30+ FPS.
* **Noise Reduction & Smoothing:** Implements Exponential Moving Average ($\alpha = 0.2$) signal smoothing and thresholding to eliminate brightness flicker.
* **Guided Adaptive Calibration:** Guided step-by-step wizard to calibrate minimum pinch and maximum spread distances tailored to any user's hand size.
* **Real-Time Telemetry & WebSocket:** Low-latency WebSocket streaming (`/ws/brightness`) feeds live telemetry to a React Vite dashboard without HTTP polling.
* **SQLite Persistence:** SQLAlchemy ORM records runtime sessions, statistics, and historical brightness adjustment events.
* **Modern React Dashboard:** Dark, responsive glassmorphic UI built with React, Vite, Tailwind CSS, Lucide Icons, and Recharts.
* **Hardware & Demo Mode Fallback:** Graceful fallback to simulated demo mode when camera hardware or display APIs are unssupported or inside Docker.

---

## 📐 System Architecture

```text
               ┌─────────────────────────────────────────┐
               │           Webcam Video Feed             │
               └────────────────────┬────────────────────┘
                                    │
                                  OpenCV
                                    │
               ┌────────────────────▼────────────────────┐
               │      MediaPipe Hand Landmarker          │
               └────────────────────┬────────────────────┘
                                    │
                        Thumb & Index Landmarks
                                    │
               ┌────────────────────▼────────────────────┐
               │      2D Euclidean Distance Metric       │
               └────────────────────┬────────────────────┘
                                    │
               ┌────────────────────▼────────────────────┐
               │      Normalization & Calibration        │
               └────────────────────┬────────────────────┘
                                    │
               ┌────────────────────▼────────────────────┐
               │  Exponential Moving Average Smoothing   │
               └────────────────────┬────────────────────┘
                                    │
               ┌────────────────────▼────────────────────┐
               │     Local OS Brightness Controller      │
               └────────────────────┬────────────────────┘
                                    │
               ┌────────────────────▼────────────────────┐
               │       Physical Display Hardware         │
               └─────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

* **Computer Vision & AI:** Python 3.11, OpenCV, MediaPipe Tasks Vision, NumPy
* **OS Hardware API:** `screen-brightness-control`
* **Backend:** FastAPI, Pydantic v2, Uvicorn, SQLAlchemy, SQLite
* **Frontend:** React 18, Vite, Tailwind CSS, Axios, Recharts, Lucide Icons
* **Testing:** pytest, FastAPI TestClient
* **DevOps & Packaging:** Docker, Docker Compose, PyInstaller, PowerShell, GitHub Actions

---

## ⚡ Quick Start (Windows)

### 1. Clone & Setup

```powershell
git clone https://github.com/santhoshiodiganti007-spec/Real-time-brightness-controlling-using-hand-gestures-with-open-cv-and-mediapipe.git
cd Real-time-brightness-controlling-using-hand-gestures-with-open-cv-and-mediapipe

# Run automated Windows setup script
.\scripts\setup_windows.ps1
```

### 2. Launch Application

```powershell
# One-command startup script
.\scripts\start_application.ps1
```

* **React Dashboard:** [http://127.0.0.1:3000](http://127.0.0.1:3000)
* **FastAPI Backend:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🖐️ Gesture Instructions

| Gesture | Action |
| :--- | :--- |
| **Thumb + Index Pinch (Fingers Close)** | Lower screen brightness (e.g. 10% - 30%) |
| **Thumb + Index Spread (Fingers Apart)** | Increase screen brightness (e.g. 70% - 100%) |
| **Open Hand (All 5 Fingers Raised)** | Pause gesture brightness control |

---

## 🧪 Running Unit Tests

Run the backend test suite:

```powershell
py -3.11 -m pytest backend/tests
```

Build the frontend bundle:

```powershell
cd frontend
npm run build
```

---

## 📦 Standalone Windows Executable (.exe)

Generate `TouchlessBrightnessControl.exe` without requiring Python installation:

```powershell
py -3.11 scripts/build_executable.py
```

The compiled output will be generated in `dist/TouchlessBrightnessControl/`.

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

*Note: Containerized/cloud environments run in **DEMO MODE** simulating monitor output, because cloud containers cannot directly modify local physical display hardware.*

---

## 📑 Documentation

* 📐 [Architecture Documentation](docs/architecture.md)
* 📡 [API Documentation](docs/api.md)
* ⚙️ [Installation Guide](docs/installation.md)
* 🎯 [Calibration Guide](docs/calibration.md)
* 🔧 [Troubleshooting Guide](docs/troubleshooting.md)
* 🚀 [Deployment Guide](docs/deployment.md)
* 🎓 [Viva Questions & Answers](docs/viva_questions.md)
* 💼 [Interview Questions & Answers](docs/interview_questions.md)

---

## 🔒 Privacy Notice

Webcam video frames are processed **100% locally in computer memory**. Raw video frames or personal data are never recorded to disk or transmitted to any external server.

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
