# 🎸 AI Guitar Pedal System

A high-performance, fault-tolerant AI Multi-Effects system that combines an intelligent cloud orchestration layer with ultra-low latency hardware DSP processing.

## 🌟 Overview

The AI Guitar Pedal System solves the complex challenge of mapping natural language and dynamic audio features to precise digital signal processing (DSP) parameters. It bridges the gap between high-level AI representations and low-level hardware constraints, making it suitable for both studio environments and rigorous live performance conditions.

### Core Philosophy
- **Deterministic Edge Execution**: Models and inference are optimized to run securely on-device, bypassing network latency when it matters most.
- **Fail-Safe Architecture**: Constant state shadow-copying (`/dev/shm`) and automated daemon restart loops ensure the core C++ audio engine never fully shuts down during a performance.
- **Continuous Learning (RLHF)**: Intelligent backend systems (powered by Gemini) analyze user corrections on physical knobs to continuously fine-tune the parameter mapping mappings.

## 🏗️ System Architecture

The project is structured into three primary domains:

1. **`dsp_engine/` (The Core)**: The C++ / JUCE-based routing matrix. Responsible for rendering real-time audio with strict safeties (anti-zipper smoothing, hard mathematical clamps).
2. **`backend/` (The Brain)**: FastAPI, PostgreSQL/SQLite, and Python ML pipelines. Handles AudioMAE feature extraction, K-Means clustering optimizations, and talks to the Gemini API for natural language translation and RLHF refinement.
3. **`frontend/` (The Control Center)**: A React/Vite-based mobile viewer and premium user interface for adjusting presets, viewing AI metrics, and interacting with the system remotely.

## 🚀 Quick Start & Deployment

### 1. Cloud & Backend Services
Requires Python 3.10+ and Node.js.

```bash
# 1. Install Backend Dependencies
pip install -r backend/requirements.txt
pip install librosa numpy soundfile

# 2. Run the FastAPI Server
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend Control App
```bash
# 1. Install and run the React/Vite UI
cd frontend
npm install
npm run dev
```
Navigate to the provided localhost address (e.g., `http://localhost:5173`) to open the control interface.

### 3. Edge Hardware (e.g., Raspberry Pi)
For physical deployment:
1. Transfer the system package to the target edge device.
2. Run `./start_blue_green.sh` to initialize the auto-updater and fallback image architecture.
3. Run `./systemd_auto_recovery.sh` (Requires `sudo`) to start the state-shadowing and fast-reboot daemon.

## 🧠 Continuous AI Tuning (RLHF)

The system improves itself by analyzing how users physically override AI suggestions. To run a manual feedback loop:

```bash
# Set your Gemini API Key
export GEMINI_API_KEY="your_actual_api_key"  # Linux/Mac
# $env:GEMINI_API_KEY="your_actual_api_key"  # Windows PowerShell

# Run the integration script
python backend/rlhf_gemini_integration.py
```

## 🛡️ Enterprise DSP Safeties

- **Pydantic Validation**: Intercepts AI responses; explicitly blocks mathematically impossible or dangerous parameter boundaries (e.g., Infinite Gain) before they reach the hardware.
- **Linear Smoothing**: Rapid preset changes (`<0.8ms` pull rate) are dynamically faded over `20ms` to eliminate digital artifacts.

---
*Built for the rigors of the road. Intelligent, but fundamentally uncompromising on audio stability.*
