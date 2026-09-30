from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class WeatherResponse(BaseModel):
    temperature: str = Field(..., example="31°C")
    humidity: str = Field(..., example="78%")
    rain_chance: str = Field(..., example="40%")
    wind_speed: str = Field(..., example="14 km/h")
    weather_description: str = Field(..., example="Partly Cloudy")
    location: str = Field(..., example="Guntur, Andhra Pradesh, India")
    is_live: bool = Field(default=True, description="True if retrieved from live Open-Meteo API, False if simulated fallback")
    agro_impact: str = Field(
        ...,
        example="High relative humidity (>75%) coupled with warm temperatures increases fungal sporulation risk and whitefly activity."
    )

class CropAnalysisResponse(BaseModel):
    crop: str = Field(..., example="Chilli")
    condition: str = Field(..., example="Chilli Leaf Curl Virus (Begomovirus)")
    risk_level: str = Field(..., example="HIGH") # HIGH, MEDIUM, LOW, HEALTHY
    confidence: float = Field(..., example=0.91)
    visual_symptoms: List[str] = Field(default_factory=list)
    observations: List[str] = Field(default_factory=list)
    possible_causes: List[str] = Field(default_factory=list)
    immediate_actions: List[str] = Field(default_factory=list)
    preventive_actions: List[str] = Field(default_factory=list)
    monitoring_period: str = Field(default="48 hours", example="48 hours")
    escalation_required: bool = Field(default=False)
    weather_context: Optional[Dict[str, Any]] = None
    satellite_context: Optional[Dict[str, Any]] = None
    multilingual: Dict[str, Any] = Field(default_factory=dict)
    ai_provider: str = Field(default="simulation", description="'gemini' or 'simulation'")
    limitations: str = Field(
        default="Based on visual inspection of submitted photo. Not a laboratory or culture-plate diagnosis."
    )
    disclaimer: str = Field(
        default="AI-assisted agricultural advisory. For severe or rapidly spreading crop problems, consult a qualified agricultural officer or KVK scientist."
    )

class SatelliteResponse(BaseModel):
    available: bool = Field(..., description="Whether satellite intelligence is available")
    mode: str = Field(..., description="'real', 'demo', or 'unavailable'")
    source: str = Field(default="Sentinel-2", description="Data source name e.g. Sentinel-2")
    latitude: float
    longitude: float
    observation_date: Optional[str] = None
    ndvi: Optional[float] = None
    ndwi: Optional[float] = None
    vegetation_status: Optional[str] = None # HEALTHY, MODERATE, STRESSED, CRITICAL
    vegetation_trend: Optional[str] = None # IMPROVING, STABLE, DECLINING, INCONCLUSIVE
    crop_health_summary: Optional[str] = None
    confidence: Optional[str] = None # HIGH, MEDIUM, LOW
    is_demo: bool = Field(default=False)
    message: Optional[str] = None
    zone_reference: Optional[str] = None
    historical_observations: Optional[List[Dict[str, Any]]] = None
    interpretation_notes: Optional[Dict[str, str]] = None
    limitations: Optional[str] = None

class VerifyCropResponse(BaseModel):
    crop: str = Field(..., example="Chilli")
    previous_condition: str = Field(..., example="Chilli Leaf Curl Virus")
    previous_risk_level: str = Field(..., example="HIGH")
    current_risk_level: str = Field(..., example="MEDIUM")
    risk_before: str = Field(default="HIGH")
    risk_after: str = Field(default="MEDIUM")
    recovery_status: str = Field(..., example="IMPROVING") # IMPROVING, STABLE, WORSENING, INCONCLUSIVE
    recovery_score: int = Field(..., example=78) # 0 to 100 (AI-assisted visual improvement score)
    visual_improvement_score: int = Field(default=78)
    comparison_summary: str = Field(...)
    observed_changes: List[str] = Field(default_factory=list)
    ongoing_recommendations: List[str] = Field(default_factory=list)
    next_verification_in: str = Field(default="72 hours")
    multilingual: Dict[str, Any] = Field(default_factory=dict)
    ai_provider: str = Field(default="simulation", description="'gemini' or 'simulation'")
    limitations: str = Field(
        default="Based on visual comparison of submitted images. Not a laboratory measurement."
    )
    disclaimer: str = Field(
        default="AI-assisted visual verification tracking. Re-verify in 3 days if symptoms persist."
    )

class ChatAdvisoryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(default="en") # 'en', 'te', 'hi'
    crop_context: Optional[str] = None
    condition_context: Optional[str] = None

class ChatAdvisoryResponse(BaseModel):
    response: str
    speech_text: str
    language: str
    ai_provider: str = Field(default="simulation", description="'gemini' or 'simulation'")
    suggested_questions: List[str] = Field(default_factory=list)

class TopCropRisk(BaseModel):
    crop: str
    icon: str
    risk_level: str
    affected_percentage: str
    common_pathology: str

class RegionalHotspot(BaseModel):
    district: str
    state: str
    crop: str
    risk_level: str
    active_cases: int
    advisory_status: str

class DashboardStatsResponse(BaseModel):
    total_scans: int = 1284
    high_risk_alerts: int = 37
    active_advisories: int = 214
    recovered_verifications: int = 89
    top_risk_crops: List[TopCropRisk]
    regional_hotspots: List[RegionalHotspot]
    is_demo_data: bool = True
    notice: str = "DEMO DATA — Simulated agricultural intelligence telemetry for prototype demonstration."
