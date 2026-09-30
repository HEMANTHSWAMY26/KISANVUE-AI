// KisanVue AI Frontend API Client

// Production & Environment Configuration
// Dynamically resolves API base URL from VITE_API_BASE_URL environment variable,
// falling back to the public Render backend in production and relative proxy in development.
const getBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_BASE_URL;
  if (envUrl && typeof envUrl === 'string' && envUrl.trim()) {
    let clean = envUrl.trim().replace(/\/+$/, '');
    if (clean.endsWith('/api')) {
      clean = clean.slice(0, -4);
    }
    return clean;
  }
  // Production fallback: ensure requests route to Render backend if env var is omitted
  if (import.meta.env.PROD) {
    return 'https://kisanvue-ai.onrender.com';
  }
  // Local development fallback: relative path leverages Vite dev server proxy to localhost:8000
  return '';
};

const BASE_URL = getBaseUrl();

export async function checkSystemHealth() {
  try {
    const res = await fetch(`${BASE_URL}/api/health`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('System health check fallback:', err);
    return { status: 'offline', gemini_ready: false, fallback_mode: true };
  }
}

export async function fetchLiveWeather(lat, lon) {
  try {
    const query = lat && lon ? `?lat=${lat}&lon=${lon}` : '';
    const res = await fetch(`${BASE_URL}/api/weather${query}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Live weather lookup failed, using fallback:', err);
    return {
      temperature: '31°C',
      humidity: '76%',
      rain_chance: '35%',
      wind_speed: '13 km/h',
      weather_description: 'Partly Cloudy',
      location: 'Guntur, Andhra Pradesh, India',
      agro_impact: 'Elevated relative humidity coupled with warm ambient temperature accelerates whitefly vector reproduction and fungal spore incubation.'
    };
  }
}

export async function fetchSatelliteIntelligence(lat, lon) {
  try {
    const query = lat && lon ? `?latitude=${lat}&longitude=${lon}` : '';
    const res = await fetch(`${BASE_URL}/api/satellite${query}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Satellite intelligence lookup failed, using simulated fallback:', err);
    return {
      available: true,
      mode: 'demo',
      source: 'Sentinel-2 (Simulated)',
      latitude: lat || 16.3067,
      longitude: lon || 80.4365,
      observation_date: '2026-09-28',
      ndvi: 0.72,
      ndwi: 0.31,
      vegetation_status: 'HEALTHY',
      vegetation_trend: 'STABLE',
      crop_health_summary: 'Simulated satellite context: Vegetation signal appears relatively strong across the monitored field sector. Water-related vegetation context shows adequate canopy hydration reflectance.',
      confidence: 'MEDIUM',
      is_demo: true,
      message: 'Demo Satellite Intelligence',
      interpretation_notes: {
        ndvi_context: 'Higher vegetation signal indicates stronger relative canopy activity.',
        ndwi_context: 'Water-related vegetation context indicator.'
      }
    };
  }
}

export async function analyzeCropImage(fileOrBlob, language = 'en', cropHint = '', lat = null, lon = null) {
  const formData = new FormData();
  formData.append('file', fileOrBlob);
  formData.append('language', language);
  formData.append('crop_hint', cropHint);
  if (lat) formData.append('lat', lat);
  if (lon) formData.append('lon', lon);

  const res = await fetch(`${BASE_URL}/api/analyze-crop`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Analysis failed with HTTP ${res.status}`);
  }

  return await res.json();
}

export async function verifyCropRecovery(fileOrBlob, previousCondition, previousRisk, daysElapsed = 5, language = 'en', baselineFileOrPath = '') {
  const formData = new FormData();
  formData.append('file', fileOrBlob);
  formData.append('previous_condition', previousCondition || 'Chilli Leaf Curl Virus');
  formData.append('previous_risk', previousRisk || 'HIGH');
  formData.append('days_elapsed', daysElapsed);
  formData.append('language', language);

  if (baselineFileOrPath && typeof baselineFileOrPath === 'object') {
    formData.append('baseline_file', baselineFileOrPath);
  } else if (baselineFileOrPath && typeof baselineFileOrPath === 'string') {
    try {
      const bRes = await fetch(baselineFileOrPath);
      if (bRes.ok) {
        const bBlob = await bRes.blob();
        formData.append('baseline_file', bBlob, 'baseline.jpg');
      } else {
        formData.append('baseline_sample_path', baselineFileOrPath);
      }
    } catch {
      formData.append('baseline_sample_path', baselineFileOrPath);
    }
  }

  const res = await fetch(`${BASE_URL}/api/verify-crop`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Verification failed with HTTP ${res.status}`);
  }

  return await res.json();
}

export async function askAgronomist(question, language = 'en', cropContext = '', conditionContext = '') {
  const res = await fetch(`${BASE_URL}/api/chat-advisory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question,
      language,
      crop_context: cropContext,
      condition_context: conditionContext
    }),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Agronomist query failed with HTTP ${res.status}`);
  }

  return await res.json();
}

export async function fetchDashboardTelemetry() {
  try {
    const res = await fetch(`${BASE_URL}/api/dashboard/stats`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Dashboard fetch fallback:', err);
    return {
      total_scans: 1284,
      high_risk_alerts: 37,
      active_advisories: 214,
      recovered_verifications: 89,
      is_demo_data: true,
      top_risk_crops: [
        { crop: 'Chilli (మిరప / मिर्च)', icon: '🌶️', risk_level: 'HIGH', affected_percentage: '34%', common_pathology: 'Chilli Leaf Curl Virus' },
        { crop: 'Tomato (టమోటా / टमाटर)', icon: '🍅', risk_level: 'MEDIUM', affected_percentage: '22%', common_pathology: 'Early Blight' },
        { crop: 'Paddy / Rice (వరి / धान)', icon: '🌾', risk_level: 'LOW', affected_percentage: '14%', common_pathology: 'Blast Alert' }
      ],
      regional_hotspots: [
        { district: 'Guntur', state: 'Andhra Pradesh', crop: 'Chilli', risk_level: 'HIGH', active_cases: 312, advisory_status: 'Vector Containment' },
        { district: 'Warangal', state: 'Telangana', crop: 'Cotton', risk_level: 'HIGH', active_cases: 245, advisory_status: 'Pheromone Trapping' },
        { district: 'Nashik', state: 'Maharashtra', crop: 'Tomato', risk_level: 'MEDIUM', active_cases: 189, advisory_status: 'Fungal Precaution' }
      ]
    };
  }
}

export async function fetchSampleCrops() {
  try {
    const res = await fetch(`${BASE_URL}/api/sample-images`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch {
    return [
      {
        id: 'chilli_curl',
        name: 'Chilli Leaf Curl (మిరప / मिर्च)',
        file: 'chilli_leaf_curl.jpg',
        path: '/samples/chilli_leaf_curl.jpg',
        crop: 'Chilli',
        expected_risk: 'HIGH',
        description: 'Upward curling and vein thickening caused by whitefly vector.'
      },
      {
        id: 'chilli_recovery',
        name: 'Chilli 5-Day Post Advisory (Verify Again)',
        file: 'chilli_recovered.jpg',
        path: '/samples/chilli_recovered.jpg',
        crop: 'Chilli',
        expected_risk: 'MEDIUM',
        description: 'Healthy new terminal flush emerging after neem bio-spray treatment.'
      },
      {
        id: 'tomato_blight',
        name: 'Tomato Early Blight (టమోటా / टमाटर)',
        file: 'tomato_early_blight.jpg',
        path: '/samples/tomato_early_blight.jpg',
        crop: 'Tomato',
        expected_risk: 'MEDIUM',
        description: 'Concentric target-board rings on lower foliage.'
      },
      {
        id: 'healthy_crop',
        name: 'Healthy Paddy / Field Crop (ఆరోగ్యకరమైన / स्वस्थ)',
        file: 'leaf_healthy.jpg',
        path: '/samples/leaf_healthy.jpg',
        crop: 'Paddy / Foliage',
        expected_risk: 'HEALTHY',
        description: 'Vibrant emerald green leaf without fungal or viral lesions.'
      }
    ];
  }
}
