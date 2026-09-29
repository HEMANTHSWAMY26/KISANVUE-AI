import os
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    DEFAULT_LAT,
    DEFAULT_LON,
    DEFAULT_LOCATION_NAME,
    PORT,
    HOST,
    BASE_DIR
)
from app.schemas import (
    WeatherResponse,
    CropAnalysisResponse,
    VerifyCropResponse,
    ChatAdvisoryRequest,
    ChatAdvisoryResponse,
    DashboardStatsResponse
)
from app.services.weather_service import get_current_weather
from app.services.gemini_service import (
    analyze_crop_image, 
    chat_agronomist_advisor,
    verify_crop_with_gemini,
    is_gemini_configured,
    test_gemini_direct
)
from app.services.dashboard_service import get_dashboard_telemetry

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("kisanvue.main")

# FastAPI App
app = FastAPI(
    title="KisanVue AI — Agricultural Intelligence API",
    description="Multimodal crop pathology, localized Gemini reasoning, weather telemetry, and verify-again workflows.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample images directory
SAMPLES_DIR = BASE_DIR.parent / "frontend" / "public" / "samples"

# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@app.get("/api/health", tags=["System"])
async def health_check():
    """System health, Gemini readiness status, and active AI provider."""
    ready = is_gemini_configured()
    return {
        "status": "online",
        "service": "KisanVue AI Core",
        "gemini_ready": ready,
        "ai_provider": "gemini" if ready else "simulation",
        "active_model": GEMINI_MODEL,
        "default_hub": DEFAULT_LOCATION_NAME,
        "tagline": "See. Understand. Act. Verify."
    }


@app.get("/api/test-gemini", tags=["System"])
async def test_gemini_endpoint():
    """Direct test of Google Gemini API connectivity."""
    return await test_gemini_direct()


@app.get("/api/weather", response_model=WeatherResponse, tags=["Weather"])
async def weather_endpoint(
    lat: Optional[float] = Query(None, description="Field latitude"),
    lon: Optional[float] = Query(None, description="Field longitude"),
    location_name: Optional[str] = Query(None, description="Location label")
):
    """Fetches real-time agro-meteorological metrics via Open-Meteo."""
    return await get_current_weather(lat=lat, lon=lon, location_name=location_name)


@app.post("/api/analyze-crop", response_model=CropAnalysisResponse, tags=["Analysis"])
async def analyze_crop_endpoint(
    file: UploadFile = File(...),
    language: str = Form("en"),
    crop_hint: str = Form(""),
    lat: Optional[float] = Form(None),
    lon: Optional[float] = Form(None),
):
    """
    Multimodal crop disease detection using Google Gemini & Agricultural Reasoning.
    Accepts crop image (JPEG/PNG/WebP), validates size, retrieves environmental
    weather context, and returns structured diagnosis + localized advisory.
    """
    # 1. Validation
    if not file.content_type or not (file.content_type.startswith("image/") or file.content_type == "application/octet-stream"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format '{file.content_type}'. Please upload a valid crop image (JPG, PNG, WebP)."
        )

    image_bytes = await file.read()
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty. Please capture or select a clear photo of the crop leaf."
        )

    if len(image_bytes) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image size exceeds the 20MB limit. Please provide a lighter image."
        )

    # 2. Get Weather Context
    weather_res = await get_current_weather(lat=lat, lon=lon)
    weather_dict = weather_res.model_dump()

    # 3. Analyze with Gemini Service
    filename = file.filename or crop_hint or "crop.jpg"
    result = await analyze_crop_image(
        image_bytes=image_bytes,
        mime_type=file.content_type or "image/jpeg",
        language=language,
        filename_hint=f"{filename} {crop_hint}",
        weather_context=weather_dict
    )

    return result


@app.post("/api/verify-crop", response_model=VerifyCropResponse, tags=["Verification"])
async def verify_crop_endpoint(
    file: UploadFile = File(...),
    baseline_file: Optional[UploadFile] = File(None),
    baseline_sample_path: Optional[str] = Form(None),
    previous_condition: str = Form("Chilli Leaf Curl Virus"),
    previous_risk: str = Form("HIGH"),
    days_elapsed: int = Form(5),
    language: str = Form("en")
):
    """
    Verify-Again workflow: Multimodal comparative analysis of Baseline Image vs Follow-up Image.
    Sends BOTH images to Google Gemini to assess visual symptom progression,
    calculate AI-assisted improvement score, and determine ongoing recovery guidance.
    """
    if not file.content_type or not (file.content_type.startswith("image/") or file.content_type == "application/octet-stream"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload a valid follow-up image to verify crop recovery."
        )

    followup_bytes = await file.read()
    followup_mime = file.content_type or "image/jpeg"

    # Read baseline image bytes if available
    baseline_bytes = None
    baseline_mime = "image/jpeg"

    if baseline_file:
        baseline_bytes = await baseline_file.read()
        baseline_mime = baseline_file.content_type or "image/jpeg"
    elif baseline_sample_path:
        # Check if local sample file exists
        clean_name = os.path.basename(baseline_sample_path)
        sample_file = SAMPLES_DIR / clean_name
        if sample_file.exists():
            baseline_bytes = sample_file.read_bytes()
    else:
        # Default fallback to chilli_leaf_curl.jpg baseline sample
        default_baseline = SAMPLES_DIR / "chilli_leaf_curl.jpg"
        if default_baseline.exists():
            baseline_bytes = default_baseline.read_bytes()

    return await verify_crop_with_gemini(
        baseline_bytes=baseline_bytes,
        baseline_mime=baseline_mime,
        followup_bytes=followup_bytes,
        followup_mime=followup_mime,
        previous_condition=previous_condition,
        previous_risk=previous_risk,
        days_elapsed=days_elapsed,
        language=language
    )


@app.post("/api/chat-advisory", response_model=ChatAdvisoryResponse, tags=["Advisory"])
async def chat_advisory_endpoint(payload: ChatAdvisoryRequest):
    """Conversational digital agronomist for voice and text farmer queries."""
    if not payload.question or not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    return await chat_agronomist_advisor(
        question=payload.question.strip(),
        language=payload.language,
        crop_context=payload.crop_context,
        condition_context=payload.condition_context
    )


@app.get("/api/dashboard/stats", response_model=DashboardStatsResponse, tags=["Dashboard"])
async def dashboard_stats_endpoint():
    """Aggregated agricultural risk telemetry across Indian agro-climatic zones."""
    return get_dashboard_telemetry()


@app.get("/api/sample-images", tags=["System"])
async def get_sample_images():
    """Returns curated demo crop images for 1-click test execution."""
    return [
        {
            "id": "chilli_curl",
            "name": "Chilli Leaf Curl (మిరప / मिर्च)",
            "file": "chilli_leaf_curl.jpg",
            "path": "/samples/chilli_leaf_curl.jpg",
            "crop": "Chilli",
            "expected_risk": "HIGH",
            "description": "Upward curling and vein thickening caused by whitefly vector."
        },
        {
            "id": "chilli_recovery",
            "name": "Chilli 5-Day Post Advisory (Verify Again)",
            "file": "chilli_recovered.jpg",
            "path": "/samples/chilli_recovered.jpg",
            "crop": "Chilli",
            "expected_risk": "MEDIUM",
            "description": "Healthy new terminal flush emerging after neem bio-spray treatment."
        },
        {
            "id": "tomato_blight",
            "name": "Tomato Early Blight (టమోటా / टमाटर)",
            "file": "tomato_early_blight.jpg",
            "path": "/samples/tomato_early_blight.jpg",
            "crop": "Tomato",
            "expected_risk": "MEDIUM",
            "description": "Concentric target-board rings on lower foliage."
        },
        {
            "id": "healthy_crop",
            "name": "Healthy Paddy / Field Crop (ఆరోగ్యకరమైన / स्वस्थ)",
            "file": "leaf_healthy.jpg",
            "path": "/samples/leaf_healthy.jpg",
            "crop": "Paddy / Foliage",
            "expected_risk": "HEALTHY",
            "description": "Vibrant emerald green leaf without fungal or viral lesions."
        }
    ]


# -----------------------------------------------------------------------------
# Static Files & SPA Routing
# -----------------------------------------------------------------------------
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}", tags=["Frontend"])
    async def serve_spa(full_path: str):
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({"status": "Frontend not yet built. Run npm run build inside frontend."}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
