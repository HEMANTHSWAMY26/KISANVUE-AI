"""
KisanVue AI — Satellite Intelligence Service
=============================================
Provides Sentinel-2 satellite vegetation intelligence, including:
- NDVI (Normalized Difference Vegetation Index)
- NDWI (Normalized Difference Water Index / Moisture-context)
- Explainable Vegetation Status (HEALTHY, MODERATE, STRESSED, CRITICAL)
- Multi-temporal Vegetation Trend (IMPROVING, STABLE, DECLINING, INCONCLUSIVE)
- Field-level contextual interpretation

Provider Architecture:
    SatelliteProvider (Base)
       ├── SentinelHubProvider (Real Sentinel-2 via Sentinel Hub API)
       └── DemoSatelliteProvider (Calibrated fallback with clear DEMO labeling)
"""

import math
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import httpx

from app.config import (
    SENTINELHUB_CLIENT_ID,
    SENTINELHUB_CLIENT_SECRET,
    SENTINELHUB_INSTANCE_ID,
    DEFAULT_LAT,
    DEFAULT_LON
)

logger = logging.getLogger("kisanvue.satellite")

# ==============================================================================
# SCIENTIFIC THRESHOLDS & EXPLAINABLE INTERPRETATION GUIDELINES
# ==============================================================================
# Application-level heuristic interpretation rules for agricultural context.
# NOTE: These indices are environmental context indicators and do NOT represent
# a definitive clinical plant pathology diagnosis or direct soil moisture gauge.
#
# NDVI (Normalized Difference Vegetation Index):
#   - Measures relative chlorophyll absorbance in Red (B04) vs reflectance in NIR (B08)
#   - NDVI >= 0.60: HEALTHY  (Relatively strong vegetation signal, dense photosynthetically active canopy)
#   - 0.40 <= NDVI < 0.60: MODERATE (Moderate vegetative vigour, typical of growing vegetative canopy)
#   - 0.20 <= NDVI < 0.40: STRESSED (Lower vegetation signal, indicative of sparse canopy, foliar stress or senescence)
#   - NDVI < 0.20: CRITICAL (Very low vegetation signal, bare soil, severe canopy thinning, or post-harvest)
#
# NDWI (Normalized Difference Water Index):
#   - Measures water-related canopy reflectance contrast (Green B03 vs NIR B08 or NIR B08 vs SWIR B11)
#   - Serves as a water-related vegetation context and moisture-stress indicator.
#   - Caution: Does not directly measure subsurface root moisture or specific irrigation volumes.
#
# Vegetation Trend:
#   - IMPROVING: Multi-observation delta > +0.05
#   - DECLINING: Multi-observation delta < -0.05
#   - STABLE: Multi-observation delta within [-0.05, +0.05]
#   - INCONCLUSIVE: When historical satellite passes are unavailable or obscured by cloud cover.
# ==============================================================================

def classify_vegetation_status(ndvi: Optional[float]) -> str:
    """Classifies NDVI into explainable categories without claiming universal diagnosis."""
    if ndvi is None:
        return "MODERATE"
    if ndvi >= 0.60:
        return "HEALTHY"
    elif ndvi >= 0.40:
        return "MODERATE"
    elif ndvi >= 0.20:
        return "STRESSED"
    else:
        return "CRITICAL"


def compute_vegetation_trend(historical_ndvi: Optional[List[float]]) -> str:
    """
    Computes vegetation trend across multi-temporal satellite observations.
    Returns: IMPROVING, STABLE, DECLINING, or INCONCLUSIVE.
    If historical data is unavailable, explicitly returns INCONCLUSIVE (no fabrication).
    """
    if not historical_ndvi or len(historical_ndvi) < 2:
        return "INCONCLUSIVE"
    delta = historical_ndvi[-1] - historical_ndvi[0]
    if delta > 0.05:
        return "IMPROVING"
    elif delta < -0.05:
        return "DECLINING"
    else:
        return "STABLE"


def generate_cautious_summary(ndvi: float, ndwi: float, status: str, trend: str, is_demo: bool) -> str:
    """Generates an honest, cautious agronomic interpretation without false diagnostic claims."""
    # NDVI interpretation
    if ndvi >= 0.65:
        veg_text = "Vegetation signal appears relatively strong across the monitored field sector."
    elif ndvi >= 0.45:
        veg_text = "Vegetation signal indicates moderate vegetative vigour and partial canopy closure."
    elif ndvi >= 0.25:
        veg_text = "Vegetation signal reflects potentially weaker or stressed vegetation cover."
    else:
        veg_text = "Vegetation signal is low, suggesting sparse foliage, severe stress, or bare patch."

    # NDWI interpretation
    if ndwi >= 0.25:
        water_text = "Water-related vegetation context shows adequate canopy hydration reflectance."
    elif ndwi >= 0.10:
        water_text = "Moisture-context indicator shows moderate canopy water content."
    else:
        water_text = "Water-related vegetation indicator shows low moisture signal, suggesting potential drying."

    # Trend text
    if trend == "IMPROVING":
        trend_text = "Multi-temporal trajectory shows positive vegetative recovery."
    elif trend == "DECLINING":
        trend_text = "Multi-temporal trajectory shows recent decline in vegetation reflectance."
    elif trend == "STABLE":
        trend_text = "Vegetative reflectance has remained stable across recent observations."
    else:
        trend_text = "Historical comparison is inconclusive due to single observation."

    prefix = "Simulated satellite context: " if is_demo else "Sentinel-2 observation: "
    return f"{prefix}{veg_text} {water_text} {trend_text}"


# ==============================================================================
# PROVIDER ABSTRACTION
# ==============================================================================

class SatelliteProvider(ABC):
    @abstractmethod
    async def get_data(
        self,
        lat: float,
        lon: float,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Retrieve satellite intelligence object. Returns None if provider cannot fulfill."""
        pass


class SentinelHubProvider(SatelliteProvider):
    """
    Real Sentinel-2 data provider using Sentinel Hub Statistical / Process API.
    Operates when SENTINELHUB_CLIENT_ID and SENTINELHUB_CLIENT_SECRET are configured.
    """

    OAUTH_URL = "https://services.sentinel-hub.com/oauth/token"
    STATS_URL = "https://services.sentinel-hub.com/api/v1/statistics"

    def __init__(self, client_id: str, client_secret: str, instance_id: str = ""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.instance_id = instance_id

    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret)

    async def _get_auth_token(self, client: httpx.AsyncClient) -> Optional[str]:
        try:
            res = await client.post(
                self.OAUTH_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=8.0
            )
            if res.status_code == 200:
                data = res.json()
                return data.get("access_token")
            logger.warning(f"Sentinel Hub authentication failed: HTTP {res.status_code}")
            return None
        except Exception as e:
            logger.warning(f"Sentinel Hub token request exception: {e}")
            return None

    async def get_data(
        self,
        lat: float,
        lon: float,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        if not self.is_configured():
            return None

        # Build date range: default to last 30 days
        now = datetime.utcnow()
        if not end_date:
            end_date = now.strftime("%Y-%m-%dT23:59:59Z")
        elif "T" not in end_date:
            end_date = f"{end_date}T23:59:59Z"

        if not start_date:
            start_date = (now - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")
        elif "T" not in start_date:
            start_date = f"{start_date}T00:00:00Z"

        # Bounding box ~ 200m around target field point
        delta_deg = 0.002
        bbox = [lon - delta_deg, lat - delta_deg, lon + delta_deg, lat + delta_deg]

        evalscript = """
        //VERSION=3
        function setup() {
          return {
            input: [{
              bands: ["B03", "B04", "B08", "dataMask"]
            }],
            output: [
              { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
              { id: "ndwi", bands: 1, sampleType: "FLOAT32" },
              { id: "dataMask", bands: 1, sampleType: "UINT8" }
            ]
          };
        }
        function evaluatePixel(samples) {
          let b3 = samples.B03;
          let b4 = samples.B04;
          let b8 = samples.B08;
          let ndvi = (b8 + b4 !== 0) ? (b8 - b4) / (b8 + b4) : 0;
          let ndwi = (b3 + b8 !== 0) ? (b3 - b8) / (b3 + b8) : 0;
          return {
            ndvi: [ndvi],
            ndwi: [ndwi],
            dataMask: [samples.dataMask]
          };
        }
        """

        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox,
                    "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {"from": start_date, "to": end_date},
                        "maxCloudCoverage": 30
                    }
                }]
            },
            "aggregation": {
                "timeRange": {"from": start_date, "to": end_date},
                "aggregationInterval": {"of": "P5D"},
                "evalscript": evalscript
            }
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                token = await self._get_auth_token(client)
                if not token:
                    return None

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }

                res = await client.post(self.STATS_URL, json=payload, headers=headers)
                if res.status_code != 200:
                    logger.warning(f"Sentinel Hub stats API returned HTTP {res.status_code}: {res.text[:200]}")
                    return None

                data = res.json()
                data_items = data.get("data", [])
                if not data_items:
                    logger.info("Sentinel Hub returned no valid scenes for specified window/cloud filter.")
                    return None

                # Extract valid observations sorted by date
                observations = []
                for item in data_items:
                    outputs = item.get("outputs", {})
                    ndvi_stat = outputs.get("ndvi", {}).get("bands", {}).get("B0", {}).get("stats", {})
                    ndwi_stat = outputs.get("ndwi", {}).get("bands", {}).get("B0", {}).get("stats", {})
                    mean_ndvi = ndvi_stat.get("mean")
                    mean_ndwi = ndwi_stat.get("mean")
                    from_time = item.get("interval", {}).get("from", "")
                    if mean_ndvi is not None:
                        obs_date = from_time[:10] if len(from_time) >= 10 else now.strftime("%Y-%m-%d")
                        observations.append({
                            "date": obs_date,
                            "ndvi": round(float(mean_ndvi), 3),
                            "ndwi": round(float(mean_ndwi), 3) if mean_ndwi is not None else 0.20
                        })

                if not observations:
                    return None

                latest = observations[-1]
                latest_ndvi = latest["ndvi"]
                latest_ndwi = latest["ndwi"]
                obs_date = latest["date"]

                historical_ndvi = [o["ndvi"] for o in observations]
                trend = compute_vegetation_trend(historical_ndvi)
                status = classify_vegetation_status(latest_ndvi)
                summary = generate_cautious_summary(latest_ndvi, latest_ndwi, status, trend, is_demo=False)

                return {
                    "available": True,
                    "mode": "real",
                    "source": "Sentinel-2",
                    "latitude": round(lat, 4),
                    "longitude": round(lon, 4),
                    "observation_date": obs_date,
                    "ndvi": latest_ndvi,
                    "ndwi": latest_ndwi,
                    "vegetation_status": status,
                    "vegetation_trend": trend,
                    "crop_health_summary": summary,
                    "confidence": "HIGH" if len(observations) >= 3 else "MEDIUM",
                    "is_demo": False,
                    "message": "Live Sentinel-2 multi-spectral observation retrieved.",
                    "historical_observations": observations[-4:],
                    "interpretation_notes": {
                        "ndvi_context": "Higher vegetation signal indicates stronger relative canopy activity.",
                        "ndwi_context": "Water-related vegetation context indicator."
                    }
                }

        except Exception as e:
            logger.warning(f"Error executing Sentinel Hub API query: {e}")
            return None


class DemoSatelliteProvider(SatelliteProvider):
    """
    Robust, domain-calibrated Demo Satellite Provider.
    Engages transparently when real Sentinel Hub credentials are not provided or API fails.
    Explicitly tags all outputs as DEMO / SIMULATED.
    """

    # Calibrated real-world regional agricultural zones across India
    REGIONAL_SCENARIOS = {
        "guntur": {
            "name": "Guntur District, Andhra Pradesh (Chilli & Cotton Belt)",
            "lat": 16.3067,
            "lon": 80.4365,
            "ndvi": 0.72,
            "ndwi": 0.31,
            "history": [0.68, 0.70, 0.72],
            "trend": "STABLE",
            "status": "HEALTHY",
            "summary_detail": "Chilli and commercial crop zone shows active vegetative canopy with consistent photosynthetic reflectance."
        },
        "warangal": {
            "name": "Warangal District, Telangana (Cotton & Red Gram Zone)",
            "lat": 17.9784,
            "lon": 79.5941,
            "ndvi": 0.58,
            "ndwi": 0.22,
            "history": [0.57, 0.59, 0.58],
            "trend": "STABLE",
            "status": "MODERATE",
            "summary_detail": "Rainfed cotton and pulses zone reflects moderate canopy density with mild seasonal moisture variation."
        },
        "nashik": {
            "name": "Nashik District, Maharashtra (Onion & Tomato Tracts)",
            "lat": 19.9975,
            "lon": 73.7898,
            "ndvi": 0.68,
            "ndwi": 0.34,
            "history": [0.60, 0.64, 0.68],
            "trend": "IMPROVING",
            "status": "HEALTHY",
            "summary_detail": "Irrigated horticultural parcels exhibit improving vegetative vigour across early vegetative stages."
        }
    }

    async def get_data(
        self,
        lat: float,
        lon: float,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        # Identify closest regional hub or construct deterministic coordinate-based simulation
        matched_scenario = None
        min_dist = float("inf")

        for key, sc in self.REGIONAL_SCENARIOS.items():
            dist = math.sqrt((lat - sc["lat"]) ** 2 + (lon - sc["lon"]) ** 2)
            if dist < min_dist:
                min_dist = dist
                matched_scenario = sc

        # Use recent observation date (e.g. 2-5 days ago from current system time)
        obs_date = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")

        if min_dist < 1.5 and matched_scenario:
            # Match within regional radius (~150km)
            ndvi = matched_scenario["ndvi"]
            ndwi = matched_scenario["ndwi"]
            history = matched_scenario["history"]
            trend = matched_scenario["trend"]
            status = matched_scenario["status"]
            desc_zone = matched_scenario["name"]
            historical_obs = [
                {"date": (datetime.utcnow() - timedelta(days=12)).strftime("%Y-%m-%d"), "ndvi": history[0]},
                {"date": (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d"), "ndvi": history[1]},
                {"date": obs_date, "ndvi": history[2]}
            ]
        else:
            # Deterministic geographic hash calculation for arbitrary coordinates
            # Produces stable, sensible agricultural index numbers without wild fluctuations
            coord_factor = abs(math.sin(lat * 12.345 + lon * 67.890))
            ndvi = round(0.48 + (coord_factor * 0.28), 2)  # Between 0.48 and 0.76
            ndwi = round(0.18 + (coord_factor * 0.16), 2)  # Between 0.18 and 0.34
            # Since historical data is unavailable for arbitrary uncalibrated coords, return INCONCLUSIVE!
            trend = "INCONCLUSIVE"
            status = classify_vegetation_status(ndvi)
            desc_zone = f"Coordinates ({round(lat, 3)}°N, {round(lon, 3)}°E)"
            historical_obs = None

        summary = generate_cautious_summary(ndvi, ndwi, status, trend, is_demo=True)

        return {
            "available": True,
            "mode": "demo",
            "source": "Sentinel-2 (Simulated)",
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "observation_date": obs_date,
            "ndvi": ndvi,
            "ndwi": ndwi,
            "vegetation_status": status,
            "vegetation_trend": trend,
            "crop_health_summary": summary,
            "confidence": "MEDIUM",
            "is_demo": True,
            "message": "Demo Satellite Intelligence — Simulated satellite context for prototype evaluation.",
            "zone_reference": desc_zone,
            "historical_observations": historical_obs,
            "interpretation_notes": {
                "ndvi_context": "Vegetation signal reflects relative canopy greenness and density. Not a disease diagnosis.",
                "ndwi_context": "Water-related vegetation context indicator."
            },
            "limitations": "Simulated satellite metrics for prototype demonstration. Fallback engaged automatically when live Sentinel Hub credentials are not provided."
        }


# ==============================================================================
# MAIN SERVICE FACADE
# ==============================================================================

async def get_satellite_intelligence(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Clean interface to retrieve satellite vegetation intelligence.
    Attempts real Sentinel Hub data if credentials configured;
    falls back automatically to domain-calibrated Demo Satellite Intelligence.
    Never crashes on failure.
    """
    lat = latitude if latitude is not None else DEFAULT_LAT
    lon = longitude if longitude is not None else DEFAULT_LON

    # Basic coordinate boundary validation
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        lat, lon = DEFAULT_LAT, DEFAULT_LON

    try:
        # 1. Attempt Real Sentinel Hub Provider if credentials configured
        if SENTINELHUB_CLIENT_ID and SENTINELHUB_CLIENT_SECRET:
            try:
                real_provider = SentinelHubProvider(
                    client_id=SENTINELHUB_CLIENT_ID,
                    client_secret=SENTINELHUB_CLIENT_SECRET,
                    instance_id=SENTINELHUB_INSTANCE_ID
                )
                real_data = await real_provider.get_data(
                    lat=lat,
                    lon=lon,
                    start_date=start_date,
                    end_date=end_date
                )
                if real_data and real_data.get("available"):
                    logger.info("Real Sentinel-2 data retrieved successfully.")
                    return real_data
            except Exception as ex:
                logger.warning(f"Real SentinelHubProvider failed, falling back to Demo provider: {ex}")

        # 2. Fall back to Demo Satellite Provider
        demo_provider = DemoSatelliteProvider()
        return await demo_provider.get_data(
            lat=lat,
            lon=lon,
            start_date=start_date,
            end_date=end_date
        )

    except Exception as general_err:
        logger.error(f"Unexpected error in get_satellite_intelligence: {general_err}")
        return {
            "available": False,
            "mode": "unavailable",
            "source": "Sentinel-2",
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "message": "Satellite data temporarily unavailable"
        }
