import sys
import asyncio
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from app.services.weather_service import get_current_weather
from app.services.gemini_service import analyze_crop_image, chat_agronomist_advisor
from app.services.verify_engine import evaluate_crop_verification
from app.services.dashboard_service import get_dashboard_telemetry

async def run_tests():
    print("--- 1. Testing Weather Service ---")
    weather = await get_current_weather()
    print("Weather:", weather.location, weather.temperature, weather.humidity, weather.rain_chance)
    print("Agro impact:", weather.agro_impact[:80], "...")

    print("\n--- 2. Testing Crop Analysis (Telugu & Chilli) ---")
    dummy_bytes = b"fake-chilli-image-data"
    result_te = await analyze_crop_image(
        image_bytes=dummy_bytes,
        mime_type="image/jpeg",
        language="te",
        filename_hint="chilli_leaf_curl.jpg",
        weather_context=weather.model_dump()
    )
    print("Crop:", result_te.crop)
    print("Condition:", result_te.condition)
    print("Risk:", result_te.risk_level, "Confidence:", result_te.confidence)
    print("Telugu Advisory Summary:", result_te.multilingual.get("summary"))
    print("Telugu Actions Count:", len(result_te.multilingual.get("immediate_actions", [])))

    print("\n--- 3. Testing Crop Analysis (Hindi & Tomato) ---")
    result_hi = await analyze_crop_image(
        image_bytes=dummy_bytes,
        mime_type="image/jpeg",
        language="hi",
        filename_hint="tomato_early_blight.jpg",
        weather_context=weather.model_dump()
    )
    print("Crop:", result_hi.crop)
    print("Condition:", result_hi.condition)
    print("Risk:", result_hi.risk_level)
    print("Hindi Advisory Summary:", result_hi.multilingual.get("summary"))

    print("\n--- 4. Testing Verify-Again Workflow (Initial HIGH -> Follow-up Recovery) ---")
    verify_res = evaluate_crop_verification(
        previous_condition="Chilli Leaf Curl Virus",
        previous_risk="HIGH",
        followup_filename_hint="chilli_recovered.jpg",
        days_elapsed=5,
        language="te"
    )
    print("Previous Risk:", verify_res.previous_risk_level)
    print("Current Risk:", verify_res.current_risk_level)
    print("Recovery Status:", verify_res.recovery_status, "Score:", verify_res.recovery_score)
    print("Telugu Recovery Summary:", verify_res.multilingual.get("summary"))

    print("\n--- 5. Testing Conversational Agronomist (Telugu Voice/Text Query) ---")
    chat_te = await chat_agronomist_advisor(
        question="నా మిరప ఆకులు ముడుచుకుపోతున్నాయి, ఏ మందు పిచికారీ చేయాలి?",
        language="te",
        crop_context="Chilli",
        condition_context="Leaf curl"
    )
    print("Telugu Agronomist Response:", chat_te.response)

    print("\n--- 6. Testing Intelligence Dashboard ---")
    dash = get_dashboard_telemetry()
    print("Total Scans:", dash.total_scans, "Alerts:", dash.high_risk_alerts, "Top Crops:", len(dash.top_risk_crops))
    print("Is Demo Data:", dash.is_demo_data)

    print("\n--- 7. Testing Satellite Intelligence Service (Sentinel-2 / Demo) ---")
    from app.satellite_service import get_satellite_intelligence
    sat_guntur = await get_satellite_intelligence(latitude=16.3067, longitude=80.4365)
    print("Guntur Satellite Mode:", sat_guntur["mode"], "Source:", sat_guntur["source"])
    print("Observation Date:", sat_guntur["observation_date"])
    print("NDVI:", sat_guntur["ndvi"], "NDWI:", sat_guntur["ndwi"])
    print("Vegetation Status:", sat_guntur["vegetation_status"], "Trend:", sat_guntur["vegetation_trend"])
    print("Summary:", sat_guntur["crop_health_summary"])
    assert sat_guntur["available"] is True
    assert sat_guntur["ndvi"] is not None
    assert sat_guntur["ndwi"] is not None
    assert sat_guntur["vegetation_status"] in ["HEALTHY", "MODERATE", "STRESSED", "CRITICAL"]
    assert sat_guntur["vegetation_trend"] in ["IMPROVING", "STABLE", "DECLINING", "INCONCLUSIVE"]

    print("\n--- 8. Testing Soil Intelligence Service (SoilGrids / Demo) ---")
    from app.soil_service import get_soil_intelligence
    soil_guntur = await get_soil_intelligence(latitude=16.3067, longitude=80.4365)
    print("Soil Mode:", soil_guntur["mode"], "Source:", soil_guntur["source"])
    print("SOC:", soil_guntur["organic_carbon"], "Clay%:", soil_guntur["clay_percent"], "Texture:", soil_guntur["soil_texture_class"])
    print("Soil Context:", soil_guntur["soil_context"])
    assert soil_guntur["available"] is True
    assert soil_guntur["clay_percent"] is not None
    assert soil_guntur["sand_percent"] is not None
    assert soil_guntur["organic_carbon"] is not None

    print("\n--- 9. Testing Crop Recommendation Engine & Regenerative Options ---")
    from app.crop_recommendation_service import generate_crop_recommendations
    recs = await generate_crop_recommendations(
        current_crop="Chilli",
        soil_context=soil_guntur,
        weather_context=weather.model_dump(),
        satellite_context=sat_guntur,
        language="en"
    )
    print("Recs Provider:", recs["ai_provider"], "Season:", recs["season"])
    print("Recommended Crops:", len(recs["recommended_crops"]))
    for c in recs["recommended_crops"]:
        print("  *", c["crop"], "| Risk:", c["risk"])
    print("Regenerative Options:", len(recs["regenerative_options"]))
    for ro in recs["regenerative_options"]:
        print("  ->", ro["practice"], "| Benefit:", ro["benefit"][:50])
    assert len(recs["recommended_crops"]) >= 2
    assert len(recs["regenerative_options"]) >= 2

    print("\n--- 10. Testing Unified Farm Intelligence Orchestrator ---")
    from app.farm_intelligence_service import get_unified_farm_intelligence
    farm_res = await get_unified_farm_intelligence(latitude=16.3067, longitude=80.4365, crop_hint="Chilli")
    print("Farm Status:", farm_res["status"], "Location:", farm_res["location_name"])
    print("Weather Layer:", farm_res["weather"]["temperature"])
    print("Satellite Layer:", farm_res["satellite"]["source"], farm_res["satellite"].get("ndvi"))
    print("Soil Layer:", farm_res["soil"]["source"], farm_res["soil"].get("soil_texture_class"))
    print("Recommendations Layer:", len(farm_res["recommendations"].get("recommended_crops", [])))
    assert farm_res["status"] == "success"
    assert "transparency_flags" in farm_res

    print("\nALL BACKEND UNIT TESTS (WEATHER, GEMINI, SATELLITE, SOIL, RECOMMENDATIONS) PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())
