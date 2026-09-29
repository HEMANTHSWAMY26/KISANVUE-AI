from app.schemas import DashboardStatsResponse, TopCropRisk, RegionalHotspot

def get_dashboard_telemetry() -> DashboardStatsResponse:
    """
    Returns aggregated agricultural risk telemetry for regional districts across India.
    Clearly marked as DEMO DATA for hackathon demonstration.
    """
    top_crops = [
        TopCropRisk(
            crop="Chilli (మిరప / मिर्च)",
            icon="🌶️",
            risk_level="HIGH",
            affected_percentage="34%",
            common_pathology="Chilli Leaf Curl Virus (Whitefly vector)"
        ),
        TopCropRisk(
            crop="Tomato (టమోటా / टमाटर)",
            icon="🍅",
            risk_level="MEDIUM",
            affected_percentage="22%",
            common_pathology="Early Blight (Alternaria solani)"
        ),
        TopCropRisk(
            crop="Paddy / Rice (వరి / धान)",
            icon="🌾",
            risk_level="LOW",
            affected_percentage="14%",
            common_pathology="Blast & Sheath Blight Alert"
        ),
        TopCropRisk(
            crop="Cotton (పత్తి / कपास)",
            icon="🌱",
            risk_level="HIGH",
            affected_percentage="28%",
            common_pathology="Pink Bollworm & Whitefly"
        ),
    ]

    hotspots = [
        RegionalHotspot(
            district="Guntur",
            state="Andhra Pradesh",
            crop="Chilli",
            risk_level="HIGH",
            active_cases=312,
            advisory_status="Active Vector Containment Protocol"
        ),
        RegionalHotspot(
            district="Warangal",
            state="Telangana",
            crop="Cotton",
            risk_level="HIGH",
            active_cases=245,
            advisory_status="Pink Bollworm Pheromone Trapping Alert"
        ),
        RegionalHotspot(
            district="Nashik",
            state="Maharashtra",
            crop="Tomato",
            risk_level="MEDIUM",
            active_cases=189,
            advisory_status="Fungal Humidity Precaution"
        ),
        RegionalHotspot(
            district="Ludhiana",
            state="Punjab",
            crop="Paddy",
            risk_level="LOW",
            active_cases=92,
            advisory_status="Standard Surveillance"
        ),
        RegionalHotspot(
            district="Mandya",
            state="Karnataka",
            crop="Sugarcane / Paddy",
            risk_level="LOW",
            active_cases=64,
            advisory_status="Optimal Growth Stage"
        )
    ]

    return DashboardStatsResponse(
        total_scans=1284,
        high_risk_alerts=37,
        active_advisories=214,
        recovered_verifications=89,
        top_risk_crops=top_crops,
        regional_hotspots=hotspots,
        is_demo_data=True,
        notice="DEMO DATA — Simulated agricultural intelligence telemetry for prototype demonstration."
    )
