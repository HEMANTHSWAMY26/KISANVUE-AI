"""
KisanVue AI — Crop Recommendation & Regenerative Agriculture Service
====================================================================
Combines:
  CROP + SOIL + WEATHER + SATELLITE + SEASON
  → MULTIMODAL AGRICULTURAL & REGENERATIVE RECOMMENDATIONS

Uses Google Gemini as the core reasoning engine with domain knowledge base fallback.
All recommendations are explainable ("WHY"), risk-rated, and feature actionable
regenerative farming practices.
"""

import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

from app.config import GEMINI_API_KEY, GEMINI_MODEL, FALLBACK_MODELS
from app.services.gemini_service import is_gemini_configured, genai_client

logger = logging.getLogger("kisanvue.crop_recommendation")

# ==============================================================================
# SEASON INFERENCE HELPER
# ==============================================================================
def get_current_season() -> str:
    """Infers current Indian agricultural season based on calendar month."""
    month = datetime.utcnow().month
    if 6 <= month <= 10:
        return "Kharif (Monsoon Season — June to October)"
    elif 11 <= month or month <= 2:
        return "Rabi (Winter / Post-Monsoon Season — November to February)"
    else:
        return "Zaid (Summer Season — March to May)"


# ==============================================================================
# CURATED DOMAIN KNOWLEDGE BASE (Simulation / Offline Fallback)
# ==============================================================================
DOMAIN_RECOMMENDATIONS = {
    "clay_heavy": {
        "recommended_crops": [
            {
                "crop": "Bengal Gram / Chickpea (శనగ / चना)",
                "reason": "Deep taproot penetrates heavy clay vertisol, breaking subsoil compaction while fixing atmospheric nitrogen to replenish depleted soil reserves.",
                "soil_fit": "Thrives in deep black cotton soils (clay > 40%) with high residual moisture retention.",
                "weather_fit": "Well-adapted to post-monsoon ambient temperatures with minimal supplemental irrigation.",
                "water_need": "Low to Moderate (requires 1-2 protective irrigations at pod development).",
                "risk": "LOW"
            },
            {
                "crop": "Maize / Sweet Corn (మొక్కజొన్న / मक्का)",
                "reason": "Fast-growing high-biomass canopy that utilizes residual fertilizer nutrients, suppresses weeds, and yields valuable fodder.",
                "soil_fit": "Clay loam with good organic matter supports high nutrient uptake.",
                "weather_fit": "Tolerant of prevailing regional temperatures and ambient humidity.",
                "water_need": "Moderate (requires consistent soil moisture during tasseling and silking).",
                "risk": "MEDIUM"
            },
            {
                "crop": "Black Gram / Urad Dal (మినుములు / उड़द)",
                "reason": "Short-duration pulse (70-75 days) ideal as a catch-crop; enriches soil microflora and breaks insect vector lifecycles.",
                "soil_fit": "Vertisols and clay loams with neutral to mildly alkaline pH.",
                "weather_fit": "Performs well in warm, moderate conditions with minimal rain disturbance.",
                "water_need": "Low (drought-resilient pulse crop).",
                "risk": "LOW"
            }
        ],
        "regenerative_options": [
            {
                "practice": "Pulse Crop Rotation (Legume-Cereal Cycling)",
                "benefit": "Biological nitrogen fixation (~30–40 kg N/ha) and interruption of host cycles for whiteflies and soil nematodes.",
                "reason": "Rotating Solanaceous cash crops (Chilli/Tomato) with pulses restores natural soil fertility."
            },
            {
                "practice": "In-situ Crop Residue Retention & Mulching",
                "benefit": "Reduces surface evaporation in heavy clay, buffers soil temperatures, and feeds beneficial earthworms and mycorrhizae.",
                "reason": "Prevents soil crusting and deep cracking typical of black soils during dry spells."
            },
            {
                "practice": "Bio-inoculation with Trichoderma & Mycorrhiza",
                "benefit": "Biological barrier against Fusarium wilt and root rot without synthetic chemical load.",
                "reason": "Colonizes the rhizosphere and strengthens natural plant immune defenses."
            }
        ],
        "multilingual": {
            "te": {
                "summary": "మట్టి లక్షణాలు, వాతావరణం మరియు ఉపగ్రహ పచ్చదనం ఆధారంగా శనగ లేదా మినుములు పంట మార్పిడికి అత్యంత అనుకూలం. ఇవి నేల సారాన్ని పెంచి తెగుళ్ల వ్యాప్తిని అరికడతాయి.",
                "regenerative_title": "పునరుత్పాదక వ్యవసాయ పద్ధతులు"
            },
            "hi": {
                "summary": "मृदा बनावट, मौसम और उपग्रह निगरानी के आधार पर चना अथवा उड़द जैसी दलहनी फसलों का फसल चक्र सर्वोत्तम है। इससे मिट्टी की उर्वरा शक्ति बढ़ती है।",
                "regenerative_title": "पुनर्योजी कृषि पद्धतियाँ"
            },
            "en": {
                "summary": "Based on soil texture, current weather, and satellite vegetation context, legume rotation (Chickpea/Blackgram) is strongly indicated to break pest cycles and rebuild soil organic nitrogen.",
                "regenerative_title": "Potential Regenerative Practices"
            }
        }
    },
    "loam_balanced": {
        "recommended_crops": [
            {
                "crop": "Red Gram / Pigeonpea (కందులు / अरहर)",
                "reason": "Deep root system loosens soil profiles and draws nutrients from deeper soil layers, creating resilient crop cover.",
                "soil_fit": "Well-drained sandy loam or loam with balanced aeration.",
                "weather_fit": "High heat tolerance and resilient in varying rainfall patterns.",
                "water_need": "Low (deep root system withstands intermittent moisture stress).",
                "risk": "LOW"
            },
            {
                "crop": "Groundnut / Peanut (వేరుశనగ / मूंगफली)",
                "reason": "Enriches topsoil with nitrogen nodules, prevents surface erosion, and provides high commercial value.",
                "soil_fit": "Light sandy loam facilitates easy peg penetration and pod development.",
                "weather_fit": "Warm sunny days promote vigorous flowering and pegging.",
                "water_need": "Moderate (sensitive during flowering and pod development).",
                "risk": "MEDIUM"
            },
            {
                "crop": "Finger Millet / Ragi (రాగులు / रागी)",
                "reason": "Climate-smart nutraceutical millet requiring minimal synthetic inputs; highly resilient to fluctuating rainfall.",
                "soil_fit": "Adapts to modest fertility and light textured soils.",
                "weather_fit": "Thrives across broad temperature bands.",
                "water_need": "Very Low (exemplary water use efficiency).",
                "risk": "LOW"
            }
        ],
        "regenerative_options": [
            {
                "practice": "Green Manuring with Sunnhemp / Dhaincha",
                "benefit": "Adds 15-20 tonnes/ha of green biomass, improving organic carbon and soil porosity.",
                "reason": "Quickly builds soil structure and replenishes light-textured soils."
            },
            {
                "practice": "Cover Cropping with Cowpea (Lobia)",
                "benefit": "Protects bare topsoil from wind and rain erosion while fixing biological nitrogen.",
                "reason": "Suppresses opportunistic weeds and conserves moisture."
            },
            {
                "practice": "Micro-Irrigation with Fertigation Scheduling",
                "benefit": "Saves 35-45% water compared to flood irrigation, preventing nutrient leaching.",
                "reason": "Directs water and bio-fertilizer precisely to the active root zone."
            }
        ],
        "multilingual": {
            "te": {
                "summary": "తేలికపాటి నేలలకు కందులు, వేరుశనగ లేదా రాగులు సాగు చేయడం ఎంతో లాభదాయకం. పచ్చిరొట్ట ఎరువుల వాడకం వల్ల నేల సారం పెరుగుతుంది.",
                "regenerative_title": "పునరుత్పాదక వ్యవసాయ పద్ధతులు"
            },
            "hi": {
                "summary": "हल्की दोमट मिट्टी के लिए अरहर, मूंगफली या रागी की खेती उपयुक्त है। हरी खाद का उपयोग मिट्टी की गुणवत्ता में सुधार करता है।",
                "regenerative_title": "पुनर्योजी कृषि पद्धतियाँ"
            },
            "en": {
                "summary": "Light to medium loam soils are ideal for Pigeonpea and climate-resilient Millets. Green manuring and cover cropping will enhance moisture retention.",
                "regenerative_title": "Potential Regenerative Practices"
            }
        }
    }
}


# ==============================================================================
# MAIN CROP RECOMMENDATION ENGINE
# ==============================================================================
async def generate_crop_recommendations(
    current_crop: Optional[str] = None,
    soil_context: Optional[Dict[str, Any]] = None,
    weather_context: Optional[Dict[str, Any]] = None,
    satellite_context: Optional[Dict[str, Any]] = None,
    season: Optional[str] = None,
    farmer_objective: str = "sustainable_yield",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Multimodal crop and regenerative recommendation engine.
    Orchestrates soil properties + weather telemetry + satellite indices + season + current crop
    through Google Gemini multimodal reasoning, with resilient domain fallback.
    """
    lang_key = language.lower() if language in ["en", "te", "hi"] else "en"
    active_season = season or get_current_season()
    cur_crop = current_crop or "Chilli / General Field Crop"

    # Extract soil facts
    clay_pct = 35.0
    soc = 8.0
    soil_tex = "Clay Loam"
    soil_source = "SoilGrids (Simulated)"
    soil_mode = "demo"

    if soil_context and soil_context.get("available"):
        clay_pct = float(soil_context.get("clay_percent", 35.0))
        soc = float(soil_context.get("organic_carbon", 8.0))
        soil_tex = str(soil_context.get("soil_texture_class", "Clay Loam"))
        soil_source = str(soil_context.get("source", "SoilGrids"))
        soil_mode = str(soil_context.get("mode", "demo"))

    # Extract weather facts
    weather_desc = "29°C, 75% RH, Partly Cloudy"
    if weather_context:
        weather_desc = (
            f"Temperature: {weather_context.get('temperature', '30°C')}, "
            f"Humidity: {weather_context.get('humidity', '75%')}, "
            f"Rain Chance: {weather_context.get('rain_chance', '30%')}"
        )

    # Extract satellite facts
    sat_summary = "NDVI 0.72 (Healthy vegetative signal), Trend: STABLE"
    if satellite_context and satellite_context.get("available"):
        sat_summary = (
            f"NDVI: {satellite_context.get('ndvi', 0.70)}, "
            f"NDWI: {satellite_context.get('ndwi', 0.28)}, "
            f"Status: {satellite_context.get('vegetation_status', 'HEALTHY')}, "
            f"Trend: {satellite_context.get('vegetation_trend', 'STABLE')}, "
            f"Source: {satellite_context.get('source', 'Sentinel-2')} [{satellite_context.get('mode', 'demo')}]"
        )

    # 1. LIVE GEMINI REASONING
    if is_gemini_configured():
        prompt = (
            "You are KisanVue AI's Agricultural Strategist & Agronomist specializing in Indian agriculture, "
            "sustainable crop rotation, soil health, and regenerative farming practices.\n\n"
            "Analyze these EXACT environmental facts:\n"
            f"- Current Crop Context: {cur_crop}\n"
            f"- Agricultural Season: {active_season}\n"
            f"- Weather Conditions: {weather_desc}\n"
            f"- Soil Profile ({soil_source} [{soil_mode}]): Texture: {soil_tex}, Clay: {clay_pct}%, Organic Carbon: {soc} g/kg\n"
            f"- Satellite Vegetation Context: {sat_summary}\n"
            f"- Farmer Objective: {farmer_objective}\n\n"
            "CONSTRAINTS:\n"
            "1. Do NOT invent missing soil or satellite numbers. Refer strictly to the given facts.\n"
            "2. Recommend 2 to 3 crops with explicit reasoning explaining WHY each crop fits the soil texture, weather, and season.\n"
            "3. Provide 2 to 3 practical, accessible Regenerative Agriculture options (e.g. crop rotation, residue mulching, bio-fertilizer, green manuring).\n"
            "4. Frame regenerative practices cautiously as 'Potential regenerative practice' with realistic benefits.\n"
            f"5. Output valid JSON in the requested language ({lang_key}). "
            f"If 'te', provide explanations in Telugu script. If 'hi', in Hindi Devanagari script. If 'en', in English.\n\n"
            "RESPONSE FORMAT (JSON):\n"
            "{\n"
            '  "recommended_crops": [\n'
            '    {\n'
            '      "crop": "Crop Name (Local Script / English)",\n'
            '      "reason": "Detailed 1-2 sentence explanation of why this crop is recommended",\n'
            '      "soil_fit": "Why this crop fits the given soil texture and organic carbon",\n'
            '      "weather_fit": "Why this crop suits the current temperature and moisture profile",\n'
            '      "water_need": "Low | Moderate | High",\n'
            '      "risk": "LOW" | "MEDIUM" | "HIGH"\n'
            '    }\n'
            '  ],\n'
            '  "regenerative_options": [\n'
            '    {\n'
            '      "practice": "Name of practice",\n'
            '      "benefit": "Practical regenerative benefit",\n'
            '      "reason": "Why this practice aids this specific field context"\n'
            '    }\n'
            '  ],\n'
            '  "agronomic_summary": "2 sentence synthesis of the farm strategy in requested language script"\n'
            "}"
        )

        for model_name in FALLBACK_MODELS:
            try:
                from google.genai import types
                logger.info(f"Submitting crop recommendation reasoning to Gemini model '{model_name}'...")
                response = genai_client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )

                if response and response.text:
                    clean_text = response.text.strip()
                    if clean_text.startswith("```"):
                        lines = clean_text.splitlines()
                        if lines[0].startswith("```"):
                            lines = lines[1:]
                        if lines and lines[-1].startswith("```"):
                            lines = lines[:-1]
                        clean_text = "\n".join(lines).strip()

                    parsed = json.loads(clean_text)
                    if "recommended_crops" in parsed and "regenerative_options" in parsed:
                        logger.info("Successfully received crop recommendations from Google Gemini!")
                        return {
                            "status": "success",
                            "ai_provider": "gemini",
                            "season": active_season,
                            "farmer_objective": farmer_objective,
                            "recommended_crops": parsed.get("recommended_crops", []),
                            "regenerative_options": parsed.get("regenerative_options", []),
                            "agronomic_summary": parsed.get("agronomic_summary", ""),
                            "environmental_inputs": {
                                "current_crop": cur_crop,
                                "soil_texture": soil_tex,
                                "clay_percent": clay_pct,
                                "organic_carbon": soc,
                                "weather_summary": weather_desc,
                                "satellite_summary": sat_summary
                            }
                        }
            except Exception as e:
                logger.warning(f"Gemini crop recommendation failed with model '{model_name}': {e}")

    # 2. RESILIENT DOMAIN KNOWLEDGE BASE FALLBACK
    logger.info("Engaging domain knowledge base for crop recommendations (ai_provider='simulation')...")
    key = "clay_heavy" if clay_pct >= 30.0 else "loam_balanced"
    kb = DOMAIN_RECOMMENDATIONS[key]
    ml = kb["multilingual"].get(lang_key, kb["multilingual"]["en"])

    return {
        "status": "success",
        "ai_provider": "simulation",
        "season": active_season,
        "farmer_objective": farmer_objective,
        "recommended_crops": kb["recommended_crops"],
        "regenerative_options": kb["regenerative_options"],
        "agronomic_summary": ml.get("summary", ""),
        "environmental_inputs": {
            "current_crop": cur_crop,
            "soil_texture": soil_tex,
            "clay_percent": clay_pct,
            "organic_carbon": soc,
            "weather_summary": weather_desc,
            "satellite_summary": sat_summary
        }
    }
