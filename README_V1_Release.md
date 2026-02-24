# 🎸 AI Guitar Pedal - Enterprise V1.0 Release

Welcome to the AI Guitar Pedal project. This repository contains the complete, production-ready source code for an intelligent, offline-survivable, hardware-safe AI Multi-Effects system.

## 🚀 Quick Start (Deployment)

1. **Deploy the Cloud/Mobile Heavy Lifter**
   - The App handles AudioMAE feature extraction and Demucs source separation.
   - Run `docker-compose up -d postgres-db ai-pedal-backend` on your server for the cloud sync hub.

2. **Deploy the Raspberry Pi (Edge Hardware)**
   - Copy this packaged zip to your Raspberry Pi 4/5.
   - Run `./start_blue_green.sh`
     *This activates the Watchtower auto-updater with an instant fallback in case a faulty Docker image is pulled.*
   - Run `./systemd_auto_recovery.sh` (Requires sudo)
     *This installs the Linux daemon that constantly shadows your parameters to `/dev/shm` (RAM Disk) and reboots the JUCE C++ engine within 1 second if a crash occurs.*

## 🛡️ Enterprise DSP Safeties

Do not disable these features unless you understand the physical consequences:

*   **Pydantic Anti-Hallucination (`pydantic_llm_validator.py`):** Intercepts Gemini API responses. If an AI hallucinates bounds (e.g. Gain = 999.0), it drops the packet to prevent speaker blowout.
*   **JUCE Audio Smoother (`JuceAudioSmoother.h`):** Because our SQLite cache swaps presets in `<0.8ms`, parameters fade linearly over `20ms` to prevent digital zipper/popping noises.
*   **OSC Hard Clamps (`OscSafetyValidator.h`):** The final C++ wall preventing mathematical Infinity/NaN errors in the DSP filter loops.

## 💾 Core Technologies
*   **AudioMAE / CLAP:** Extracts phase-accurate, non-linear distortion features that traditional MFCCs lose.
*   **Deterministic MLP Mapping (`audiomae_mlp_mapping_head.py`):** Bypasses LLM prompt guessing and maps 768-D vectors instantly to physical float values.
*   **K-Means API Optimizer:** Prevents LLM scaling costs by mathematically discarding poisoned/troll audio scraping data.

---
*Built with fault-tolerance first. Ready for stadium stages.*
