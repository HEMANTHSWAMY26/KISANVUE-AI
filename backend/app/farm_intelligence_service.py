"""
KisanVue AI — Farm Intelligence Orchestrator Service
=====================================================
Unified intelligence pipeline for smallholder agriculture:
LOCATION
  ↓
WEATHER (Open-Meteo)
  ↓
SATELLITE (Sentinel-2 NDVI / NDWI)
  ↓
SOIL (SoilGrids Organic Carbon & Texture)
  ↓
CROP & REGENERATIVE RECOMMENDATIONS (Google Gemini Multimodal Reasoning)
  ↓
LOCALIZED AGRO-ADVISORY
"""

import asyncio
import logging
from typing import Optional, Dict, Any

from app.config import DEFAULT_LAT, DEFAULT_LON, DEFAULT_LOCATION_NAME
from app.services.weather_service import get_current_weather
from app.satellite_service import get_satellite_intelligence
from app.soil_service import get_soil_intelligence
from app.crop_recommendation_service import generate_crop_recommendations

logger = logging.getLogger("kisanvue.farm_intelligence")

async def get_unified_farm_intelligence(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    crop_hint: Optional[str] = "Chilli",
    language: str = "en",
    farmer_objective: str = "sustainable_yield"
) -> Dict[str, Any]:
    """
    Orchestrates live/demo environmental telemetry layers into one cohesive farm intelligence model.
    Fail-safe: A failure in any single provider does NOT crash the pipeline.
    """
    lat = latitude if latitude is not None else DEFAULT_LAT
    lon = longitude if longitude is not None else DEFAULT_LON

    # 1. Fetch Environmental Telemetry Concurrently
    weather_task = get_current_weather(lat=lat, lon=lon)
    satellite_task = get_satellite_intelligence(latitude=lat, longitude=lon)
    soil_task = get_soil_intelligence(latitude=lat, longitude=lon)

    weather_res, sat_res, soil_res = await asyncio.gather(
        weather_task, satellite_task, soil_task, return_exceptions=True
    )

    # Weather Handling
    if isinstance(weather_res, Exception):
        logger.warning(f"Weather query exception: {weather_res}")
        weather_dict = {
            "temperature": "30°C", "humidity": "75%", "rain_chance": "30%",
            "weather_description": "Partly Cloudy", "location": DEFAULT_LOCATION_NAME,
            "agro_impact": "Favorable growing conditions with moderate humidity."
        }
    else:
        weather_dict = weather_res.model_dump()

    # Satellite Handling
    if isinstance(sat_res, Exception):
        logger.warning(f"Satellite query exception: {sat_res}")
        sat_dict = {"available": False, "mode": "unavailable", "source": "Sentinel-2"}
    else:
        sat_dict = sat_res

    # Soil Handling
    if isinstance(soil_res, Exception):
        logger.warning(f"Soil query exception: {soil_res}")
        soil_dict = {"available": False, "mode": "unavailable", "source": "SoilGrids"}
    else:
        soil_dict = soil_res

    # 2. Generate Explainable Crop & Regenerative Recommendations via Gemini
    try:
        rec_res = await generate_crop_recommendations(
            current_crop=crop_hint,
            soil_context=soil_dict,
            weather_context=weather_dict,
            satellite_context=sat_dict,
            farmer_objective=farmer_objective,
            language=language
        )
    except Exception as e:
        logger.error(f"Crop recommendation exception: {e}")
        rec_res = {
            "status": "partial",
            "recommended_crops": [],
            "regenerative_options": [],
            "agronomic_summary": "Recommendations temporarily unavailable."
        }

    return {
        "status": "success",
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "location_name": weather_dict.get("location", DEFAULT_LOCATION_NAME),
        "weather": weather_dict,
        "satellite": sat_dict,
        "soil": soil_dict,
        "recommendations": rec_res,
        "transparency_flags": {
            "weather_live": weather_dict.get("is_live", True),
            "satellite_mode": sat_dict.get("mode", "demo"),
            "soil_mode": soil_dict.get("mode", "demo"),
            "ai_reasoning_provider": rec_res.get("ai_provider", "gemini")
        }
    }
