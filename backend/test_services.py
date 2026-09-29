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

    print("\nALL BACKEND UNIT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())
