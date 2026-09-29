# Third-Party Code & Architecture Attribution

KisanVue AI was architected for the Google Cloud "Build with AI: Code for Communities" Hackathon. It builds upon and adapts concepts, UI patterns, and backend structures from the following open-source projects:

---

## 1. VERIFYX
* **Source:** Local reference (`VERIFYX-main`)
* **License:** MIT / Open Source
* **Reused / Adapted Components:**
  - **Camera & Evidence Capture Workflow:** Adapted image ingestion, progressive validation pipeline, and visual inspection design.
  - **Verify-Again / Re-Scan Concept:** The signature closed-loop verification architecture (`Rescan` / `spatialRuleEngine` concepts adapted for foliar recovery tracking).
  - **Inspection Reporting Patterns:** Clean, high-contrast, structured cards displaying severity, confidence, and actionable instructions.

---

## 2. Agrova-AI
* **Source:** Local reference (`Agrova-Ai-main`)
* **License:** MIT
* **Reused / Adapted Components:**
  - **Google Gemini Multimodal Crop Pathology:** Adapted agricultural system prompts and structured diagnostic response schemas.
  - **FastAPI Backend Architecture:** Asynchronous endpoint design and CORS middleware.
  - **Open-Meteo Integration:** Real-time agro-meteorological fetching (temperature, humidity, precipitation probability) combined with disease risk correlation.

---

## 3. AgroBot
* **Source:** Local reference (`AgroBot-main`)
* **License:** MIT
* **Reused / Adapted Components:**
  - **Multilingual Support:** Indian language localization focusing on Telugu (`te`), Hindi (`hi`), and English (`en`).
  - **Conversational Agricultural Extension:** Plainspoken, farmer-friendly oral phrasing for digital advisory.
  - **Speech / Audio Advisory:** Integration of Web Speech API speech-to-text and speech synthesis for low-literacy accessibility.

---

## 4. KrishiMitra AI & Smart Agriculture AI System
* **Source:** Local reference (`krishimitra-ai-main`, `smart-agriculture-ai-system-main`)
* **Usage:** Architectural reference for regional agricultural hotspot monitoring and district risk indicators.
