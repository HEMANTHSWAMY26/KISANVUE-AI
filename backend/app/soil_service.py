"""
KisanVue AI — Soil Intelligence Service
========================================
Provides coordinate-based soil property intelligence, including:
- Soil Organic Carbon (SOC in g/kg or %)
- Soil Texture Context: Clay %, Sand %, Silt %
- Soil Texture Class (e.g., Clay Loam, Sandy Loam, Vertisol profile)
- Cautious agronomic interpretation regarding water retention & tilth

Provider Architecture:
    SoilProvider (Base)
       ├── SoilGridsProvider (Real ISRIC SoilGrids REST API with strict timeout)
       └── DemoSoilProvider (Domain-calibrated regional fallback with clear DEMO labels)
"""

import math
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

import httpx

from app.config import DEFAULT_LAT, DEFAULT_LON

logger = logging.getLogger("kisanvue.soil")

# ==============================================================================
# SCIENTIFIC INTERPRETATION & TEXTURE HELPERS
# ==============================================================================
# Guidelines:
# - Organic carbon: higher organic carbon generally indicates greater organic matter context.
# - Clay / Sand / Silt: soil texture context influencing drainage and aeration.
# - Cautious wording: "soil texture context", "organic-carbon indicator", "may influence water retention".
# ==============================================================================

def classify_soil_texture(clay: float, sand: float, silt: float) -> str:
    """Standard USDA texture triangle approximation."""
    if clay >= 40:
        if silt >= 40:
            return "Silty Clay"
        elif sand >= 45:
            return "Sandy Clay"
        return "Clay"
    elif clay >= 27:
        if sand >= 45:
            return "Sandy Clay Loam"
        elif sand <= 20:
            return "Silty Clay Loam"
        return "Clay Loam"
    elif clay >= 20:
        return "Loam"
    elif silt >= 50:
        return "Silt Loam"
    elif sand >= 70:
        return "Sandy Loam" if clay >= 10 else "Loamy Sand"
    else:
        return "Loam"


def generate_cautious_soil_context(
    texture_class: str,
    organic_carbon: float,
    clay: float,
    sand: float,
    silt: float,
    is_demo: bool
) -> str:
    """Generates an honest, cautious agronomic interpretation without unsubstantiated fertility claims."""
    # Organic carbon interpretation
    if organic_carbon >= 10.0:
        oc_desc = "Organic-carbon indicator reflects favorable organic matter background."
    elif organic_carbon >= 6.0:
        oc_desc = "Organic-carbon indicator suggests moderate organic matter presence."
    else:
        oc_desc = "Organic-carbon indicator indicates relatively low organic matter context."

    # Texture interpretation
    if clay >= 35.0:
        tex_desc = f"{texture_class} profile with significant clay fraction; may offer high moisture retention but requires attention to aeration and drainage."
    elif sand >= 50.0:
        tex_desc = f"{texture_class} profile with high sand proportion; typically well-drained and permeable with lower nutrient and water buffering."
    else:
        tex_desc = f"{texture_class} profile exhibiting balanced particle distribution, generally favorable for root penetration and moisture retention."

    prefix = "Simulated soil profile: " if is_demo else "SoilGrids observation: "
    return f"{prefix}{tex_desc} {oc_desc}"


# ==============================================================================
# SOIL PROVIDER ABSTRACTION
# ==============================================================================

class SoilProvider(ABC):
    @abstractmethod
    async def get_soil_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Retrieve soil property intelligence. Returns None if provider fails."""
        pass


class SoilGridsProvider(SoilProvider):
    """
    Live SoilGrids 2.0 REST API Provider (ISRIC World Soil Information).
    Retrieves global gridded surface soil properties (0-5cm / 0-30cm).
    """

    BASE_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"

    async def get_soil_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        params = {
            "lon": lon,
            "lat": lat,
            "property": ["soc", "clay", "sand", "silt"],
            "depth": "0-5cm",
            "value": "mean"
        }

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.get(self.BASE_URL, params=params)
                if res.status_code != 200:
                    logger.info(f"SoilGrids live query returned status {res.status_code}")
                    return None

                data = res.json()
                layers = data.get("properties", {}).get("layers", [])
                extracted = {}

                for layer in layers:
                    name = layer.get("name")
                    depths = layer.get("depths", [])
                    if depths:
                        val = depths[0].get("values", {}).get("mean")
                        if val is not None:
                            extracted[name] = float(val)

                # Check if all 4 key properties exist
                if not all(k in extracted for k in ["clay", "sand", "silt", "soc"]):
                    logger.info("SoilGrids returned incomplete property layers.")
                    return None

                # Convert SoilGrids raw units (dg/kg -> g/kg, divide by 10 for %)
                # clay, sand, silt raw are in g/kg (out of 1000) -> / 10 = %
                clay_pct = round(extracted["clay"] / 10.0, 1)
                sand_pct = round(extracted["sand"] / 10.0, 1)
                silt_pct = round(extracted["silt"] / 10.0, 1)
                soc_g_kg = round(extracted["soc"] / 10.0, 1)  # dg/kg / 10 = g/kg

                texture_class = classify_soil_texture(clay_pct, sand_pct, silt_pct)
                context = generate_cautious_soil_context(
                    texture_class, soc_g_kg, clay_pct, sand_pct, silt_pct, is_demo=False
                )

                return {
                    "available": True,
                    "mode": "real",
                    "source": "SoilGrids",
                    "latitude": round(lat, 4),
                    "longitude": round(lon, 4),
                    "organic_carbon": soc_g_kg,
                    "organic_carbon_unit": "g/kg",
                    "clay_percent": clay_pct,
                    "sand_percent": sand_pct,
                    "silt_percent": silt_pct,
                    "soil_texture_class": texture_class,
                    "soil_context": context,
                    "confidence": "HIGH",
                    "is_demo": False,
                    "message": "Live SoilGrids 250m global soil property query successful.",
                    "disclaimer": "SoilGrids predictions represent 250m resolution regional estimates and do not replace physical laboratory soil testing."
                }

        except Exception as e:
            logger.info(f"Live SoilGrids query failed or timed out: {e}")
            return None


class DemoSoilProvider(SoilProvider):
    """
    Calibrated domain fallback for Indian agro-climatic zones.
    Provides transparent simulated soil profiles when live SoilGrids API is unreachable.
    Always visibly tags outputs as DEMO / SIMULATED.
    """

    REGIONAL_PROFILES = {
        "guntur": {
            "name": "Guntur District, Andhra Pradesh (Krishna-Godavari Zone)",
            "lat": 16.3067,
            "lon": 80.4365,
            "organic_carbon": 8.4,
            "clay": 44.5,
            "sand": 28.2,
            "silt": 27.3,
            "texture": "Clay (Deep Black Cotton / Vertisol)"
        },
        "warangal": {
            "name": "Warangal District, Telangana (Central Telangana Zone)",
            "lat": 17.9784,
            "lon": 79.5941,
            "organic_carbon": 6.8,
            "clay": 22.0,
            "sand": 54.0,
            "silt": 24.0,
            "texture": "Sandy Loam (Red Alfisol / Chalkas)"
        },
        "nashik": {
            "name": "Nashik District, Maharashtra (Western Maharashtra Zone)",
            "lat": 19.9975,
            "lon": 73.7898,
            "organic_carbon": 9.6,
            "clay": 32.5,
            "sand": 38.0,
            "silt": 29.5,
            "texture": "Clay Loam (Medium Black Inceptisol)"
        }
    }

    async def get_soil_data(self, lat: float, lon: float) -> Dict[str, Any]:
        matched = None
        min_dist = float("inf")

        for key, p in self.REGIONAL_PROFILES.items():
            dist = math.sqrt((lat - p["lat"]) ** 2 + (lon - p["lon"]) ** 2)
            if dist < min_dist:
                min_dist = dist
                matched = p

        if min_dist < 1.5 and matched:
            clay = matched["clay"]
            sand = matched["sand"]
            silt = matched["silt"]
            soc = matched["organic_carbon"]
            texture_class = matched["texture"]
            zone_desc = matched["name"]
        else:
            # Deterministic coordinate hash for arbitrary locations
            factor = abs(math.sin(lat * 31.415 + lon * 92.653))
            clay = round(20.0 + (factor * 30.0), 1)  # 20% to 50%
            sand = round(25.0 + ((1.0 - factor) * 35.0), 1)  # 25% to 60%
            silt = round(max(5.0, 100.0 - (clay + sand)), 1)
            soc = round(4.5 + (factor * 6.5), 1)
            texture_class = classify_soil_texture(clay, sand, silt)
            zone_desc = f"Simulated Profile ({round(lat, 3)}°N, {round(lon, 3)}°E)"

        context = generate_cautious_soil_context(
            texture_class, soc, clay, sand, silt, is_demo=True
        )

        return {
            "available": True,
            "mode": "demo",
            "source": "SoilGrids (Simulated)",
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "organic_carbon": soc,
            "organic_carbon_unit": "g/kg",
            "clay_percent": clay,
            "sand_percent": sand,
            "silt_percent": silt,
            "soil_texture_class": texture_class,
            "soil_context": context,
            "confidence": "MEDIUM",
            "is_demo": True,
            "zone_reference": zone_desc,
            "message": "Demo Soil Intelligence — Simulated soil profile for prototype demonstration.",
            "disclaimer": "Simulated regional soil context. Does not replace physical field soil sample lab testing."
        }


# ==============================================================================
# MAIN SERVICE FACADE
# ==============================================================================

async def get_soil_intelligence(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
) -> Dict[str, Any]:
    """
    Clean interface to retrieve soil properties.
    Attempts real SoilGrids 2.0 query; falls back automatically to domain-calibrated DemoSoilProvider.
    Never crashes on failure.
    """
    lat = latitude if latitude is not None else DEFAULT_LAT
    lon = longitude if longitude is not None else DEFAULT_LON

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        lat, lon = DEFAULT_LAT, DEFAULT_LON

    try:
        # 1. Attempt live SoilGrids query
        real_provider = SoilGridsProvider()
        real_data = await real_provider.get_soil_data(lat, lon)
        if real_data and real_data.get("available"):
            return real_data

        # 2. Fall back to domain-calibrated Demo provider
        demo_provider = DemoSoilProvider()
        return await demo_provider.get_soil_data(lat, lon)

    except Exception as err:
        logger.error(f"Unexpected error in get_soil_intelligence: {err}")
        return {
            "available": False,
            "mode": "unavailable",
            "source": "SoilGrids",
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "message": "Soil property data temporarily unavailable"
        }
