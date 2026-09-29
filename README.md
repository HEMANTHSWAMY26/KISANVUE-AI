# KisanVue AI

### Tagline
**See. Understand. Act. Verify.**

---

## Overview

**KisanVue AI** is an advanced agricultural intelligence platform designed for smallholder and marginal farmers, built for the Google Cloud **"Build with AI: Code for Communities"** Hackathon. 

Traditional crop health tools stop at a single diagnosis. KisanVue AI delivers an end-to-end closed-loop experience:
1. **See:** High-resolution field photography or camera scanning of crop foliage and pests.
2. **Understand:** Multimodal pathology reasoning with **Google Gemini**, integrated with real-time agro-meteorological context (temperature, humidity, rain probability) via Open-Meteo.
3. **Act:** Clear, responsible Integrated Pest Management (IPM) advisories delivered in native Indian languages (**Telugu**, **Hindi**, **English**) with oral voice readout.
4. **Verify:** The signature **"Verify Again"** engine compares baseline vs. follow-up scans over a 3-to-7-day period to measure plant recovery, calculate recovery scores, and validate treatment efficacy.

---

## Core Capabilities

- **AI-Powered Crop Pathology:** Rapid identification of disease conditions (e.g., Chilli Leaf Curl Virus, Tomato Early Blight, Paddy Blast).
- **Google Gemini Multimodal Reasoning:** Zero-shot agricultural image understanding and structured pathology reports.
- **Micro-Climate Correlation:** Live Open-Meteo weather integration analyzing ambient risk (fungal spore germination windows, vector proliferation spikes).
- **Multilingual Support:** Complete UI, diagnosis, and speech advisories in **English**, **Telugu (తెలుగు)**, and **Hindi (हिंदी)**.
- **Voice Interaction:** Native Web Speech API speech-to-text recognition and text-to-speech audio synthesis with real-time waveform visualizer.
- **Verify-Again Engine:** Side-by-side visual and quantitative recovery tracking (e.g., HIGH Risk ➔ MEDIUM Risk, 82% recovery score).
- **National Telemetry Dashboard:** Aggregated regional hotspot monitoring across Indian agricultural belts (Guntur, Warangal, Nashik, Ludhiana, Mandya) with clearly labeled demo telemetry.
- **Safety & Trust Notice:** Responsible agronomy disclaimers and KVK escalation triggers for rapidly spreading pathogens.

---

## India-Scale Architecture

```text
Farmer (Mobile Camera / Voice / GPS)
  ↓
KisanVue Edge Web Application
  ↓
Google Gemini 2.5 Flash Multimodal Reasoning
  ↓
Agro-Meteorology Layer (Open-Meteo / Humidity / Vectors)
  ↓
Closed-Loop "Verify Again" Efficacy Engine
  ↓
District / Regional Agricultural Intelligence Telemetry
```

---

## Local Setup & Quickstart

### Prerequisites
- Windows PowerShell
- Python 3.10+ (tested on Python 3.14)
- Node.js v18+ & npm

### 1. Backend Setup
```powershell
# Navigate to backend
cd C:\Users\heman\OneDrive\Desktop\KISAN\KISANVUE-AI\backend

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# (Optional) Set your Google Gemini API Key in .env
# If empty, KisanVue runs its resilient local agricultural reasoning engine
notepad .env

# Start the FastAPI server
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Backend runs on: `http://127.0.0.1:8000`  
Interactive Swagger docs: `http://127.0.0.1:8000/docs`

### 2. Frontend Setup
```powershell
# Open a second PowerShell terminal
cd C:\Users\heman\OneDrive\Desktop\KISAN\KISANVUE-AI\frontend

# Install dependencies (already installed)
npm install

# Start Vite dev server
npm run dev
```
Frontend runs on: `http://localhost:5173`

---

## Environment Variables

Defined in `backend/.env.example` and `backend/.env`:

| Variable | Description | Default |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API Key (from Google AI Studio). If omitted, backend uses the built-in domain reasoning engine so the demo never fails. | *Optional* |
| `GEMINI_MODEL` | Target Gemini Model | `gemini-2.5-flash` |
| `HOST` | Server Host IP | `0.0.0.0` |
| `PORT` | Server Port | `8000` |
| `DEFAULT_LAT` | Monitoring Latitude (Guntur, AP) | `16.3067` |
| `DEFAULT_LON` | Monitoring Longitude (Guntur, AP) | `80.4365` |

---

## 1-Click Demo Testing Walkthrough

1. Open `http://localhost:5173` in your browser.
2. Under **Quick Test Crop Samples**, click **"🌶️ Chilli Leaf Curl (Guntur, AP)"**.
3. Click **"Diagnose with Gemini"**. Watch the 5-stage progressive validation pipeline complete.
4. Review the structured report (Severity, Symptoms, Immediate IPM Actions, Weather Impact).
5. Click **"Listen to Advisory"** to hear oral audio guidance in English.
6. Switch the top-right language selector to **"తెలుగు (Telugu)"** or **"हिंदी (Hindi)"** to see instant localization of the entire diagnostic report.
7. Click **"Verify Again"** at the bottom of the result.
8. The comparison screen loads the baseline scan on the left. Click **"Recovered Chilli (5-Day Post Advisory)"** and click **"Analyze Recovery Progress"**.
9. Observe the quantitative recovery score (82/100) and risk level drop (**HIGH ➔ MEDIUM**).
10. Click the **"Voice Agronomist"** tab to chat with the digital extension officer or test the **"National Telemetry"** dashboard.

---

## Attribution & License

Please see [THIRD_PARTY.md](THIRD_PARTY.md) for full licensing details and attribution to **VERIFYX**, **Agrova-AI**, and **AgroBot**.
