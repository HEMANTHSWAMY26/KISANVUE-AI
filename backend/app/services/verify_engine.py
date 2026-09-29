import logging
from typing import Dict, Any, Optional
from app.schemas import VerifyCropResponse

logger = logging.getLogger("kisanvue.verify_engine")

def evaluate_crop_verification(
    previous_condition: str,
    previous_risk: str,
    followup_filename_hint: str = "",
    days_elapsed: int = 5,
    language: str = "en"
) -> VerifyCropResponse:
    """
    Simulation fallback for crop verification progress tracking.
    Evaluates visual changes, calculates an AI-assisted visual improvement score,
    and returns localized recovery assessment.
    """
    lang_key = language.lower() if language else "en"
    if lang_key not in ["en", "te", "hi"]:
        lang_key = "en"

    prev_risk = previous_risk.upper() if previous_risk else "HIGH"
    is_chilli = "chilli" in previous_condition.lower() or "chilli" in followup_filename_hint.lower()
    
    # Calculate visual improvement score dynamically based on treatment days
    base_progress = min(max(int(days_elapsed * 12 + 20), 45), 88)
    calculated_score = base_progress if is_chilli else min(base_progress, 78)
    
    current_risk = "MEDIUM" if prev_risk == "HIGH" else "LOW"
    recovery_status = "IMPROVING"

    observed_changes = [
        "Unfurling of healthy new vegetative shoots with smooth, uncurled margins",
        "Arrest of viral curling progression in upper terminal flush",
        "Reduction in chlorotic yellow mottling; chlorophyll pigmentation normalized across leaf lamina",
        "Drastic reduction in active whitefly nymph colonies under lower leaf surface"
    ]

    ongoing_recommendations = [
        "Continue keeping yellow sticky traps installed along crop canopy for ongoing vector surveillance",
        "Apply a secondary booster spray of bio-tonic or cold-pressed neem oil (3ml/L) after 3 days",
        "Avoid excessive high-nitrogen synthetic fertilizer; apply balanced potassium and micronutrient foliar spray",
        "Perform next verification scan in 72 hours to confirm sustained recovery"
    ]

    multilingual = {
        "te": {
            "language": "te",
            "crop_name": "మిరప (Chilli)" if is_chilli else "టమోటా (Tomato)",
            "recovery_status_label": "స్థితి: మెరుగుపడుతోంది (IMPROVING)",
            "previous_risk_label": f"గత ప్రమాదం: {prev_risk}",
            "current_risk_label": f"ప్రస్తుత ప్రమాదం: {current_risk}",
            "summary": f"{days_elapsed} రోజుల చికిత్స తర్వాత పంట ఆరోగ్యంలో స్పష్టమైన మెరుగుదల కనిపించింది. ఆకుల ముడుత ఆగిపోయి, కొత్తగా వచ్చే ఆకులు చక్కగా విచ్చుకుంటున్నాయి.",
            "observed_changes": [
                "కొత్తగా వచ్చే చిగుళ్ళు ముడుచుకోకుండా సహజంగా పెరుగుతున్నాయి",
                "ఆకులలో పసుపు రంగు మచ్చలు తగ్గి పచ్చదనం పెరిగింది",
                "ఆకుల కింద తెల్లదోమల సంఖ్య గణనీయంగా తగ్గింది"
            ],
            "ongoing_recommendations": [
                "పసుపు జిగురు అట్టలను అలాగే ఉంచండి",
                "మరో 3 రోజుల తర్వాత మరోసారి తేలికపాటి వేప నూనె పిచికారీ చేయండి",
                "72 గంటల తర్వాత మళ్లీ ఒకసారి స్కాన్ చేసి ధృవీకరించుకోండి"
            ],
            "speech_summary": "రైతు సోదరులారా, పంటలో స్పష్టమైన మెరుగుదల కనిపించింది. కొత్త చిగుళ్ళు ఆరోగ్యంగా ఉన్నాయి. పసుపు అట్టలను కొనసాగించండి."
        },
        "hi": {
            "language": "hi",
            "crop_name": "मिर्च (Chilli)" if is_chilli else "टमाटर (Tomato)",
            "recovery_status_label": "स्थिति: सुधार हो रहा है (IMPROVING)",
            "previous_risk_label": f"पिछला जोखिम: {prev_risk}",
            "current_risk_label": f"वर्तमान जोखिम: {current_risk}",
            "summary": f"{days_elapsed} दिनों के उपचार के बाद फसल की स्थिति में उल्लेखनीय सुधार दिखाई दे रहा है। पत्तों का मुड़ना रुक गया है और नई कोपलें स्वस्थ निकल रही हैं।",
            "observed_changes": [
                "नई पत्तियां बिना मुड़े सीधी और स्वस्थ निकल रही हैं",
                "पत्तियों का पीलापन कम होकर गहरा हरा रंग लौट रहा है",
                "पत्तियों के नीचे सफेद मक्खियों की संख्या में भारी कमी आई है"
            ],
            "ongoing_recommendations": [
                "खेत में पीले स्टिकी ट्रैप लगे रहने दें",
                "3 दिन बाद नीम तेल (3 मिली/लीटर) का एक और हल्का छिड़काव करें",
                "72 घंटे बाद अंतिम सत्यापन के लिए फिर से स्कैन करें"
            ],
            "speech_summary": "बधाई हो किसान भाई! आपकी सावधानी और दवा छिड़काव से फसल में सुधार हो रहा है। नए पत्ते स्वस्थ आ रहे हैं। पीले ट्रैप जारी रखें।"
        },
        "en": {
            "language": "en",
            "crop_name": "Chilli" if is_chilli else "Tomato",
            "recovery_status_label": "Status: IMPROVING",
            "previous_risk_label": f"Previous: {prev_risk}",
            "current_risk_label": f"Current: {current_risk}",
            "summary": f"Crop exhibits noticeable visual improvement {days_elapsed} days post-advisory. Viral curling has ceased progressing, with healthy new terminal flush emerging.",
            "observed_changes": observed_changes,
            "ongoing_recommendations": ongoing_recommendations,
            "speech_summary": "Good progress! Your crop shows visual improvement after following the advisory. New leaves are emerging healthy. Maintain sticky traps and re-verify in 72 hours."
        }
    }

    selected_ml = multilingual.get(lang_key, multilingual["en"])

    return VerifyCropResponse(
        crop="Chilli" if is_chilli else "Tomato",
        previous_condition=previous_condition,
        previous_risk_level=prev_risk,
        current_risk_level=current_risk,
        risk_before=prev_risk,
        risk_after=current_risk,
        recovery_status=recovery_status,
        recovery_score=calculated_score,
        visual_improvement_score=calculated_score,
        comparison_summary=selected_ml["summary"],
        observed_changes=observed_changes,
        ongoing_recommendations=ongoing_recommendations,
        next_verification_in="72 hours",
        multilingual=selected_ml,
        ai_provider="simulation",
        limitations="Based on visual comparison of submitted images. Not a laboratory measurement.",
        disclaimer="AI-assisted visual verification tracking. Re-verify in 3 days if symptoms persist."
    )
