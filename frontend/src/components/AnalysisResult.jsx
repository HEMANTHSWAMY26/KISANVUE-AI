import React from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  ShieldAlert, 
  ArrowRight, 
  MessageSquare, 
  RotateCcw, 
  Clock, 
  Sparkles,
  CloudSun,
  Eye,
  CheckSquare
} from 'lucide-react';
import AudioPlayer from './AudioPlayer';
import SatelliteIntelligence from './SatelliteIntelligence';

export default function AnalysisResult({ 
  result, 
  currentLang, 
  onVerifyAgain, 
  onAskAgronomist, 
  onScanAnother,
  t 
}) {
  if (!result) return null;

  // Localized data override if available
  const ml = result.multilingual || {};
  const displayCrop = ml.crop_name || result.crop;
  const displayCondition = ml.condition_name || result.condition;
  const displaySummary = ml.summary || '';
  const displayImmediate = ml.immediate_actions || result.immediate_actions || [];
  const displayPreventive = ml.preventive_actions || result.preventive_actions || [];
  const speechText = ml.speech_advisory || displaySummary || `${displayCrop} diagnosed with ${displayCondition}.`;

  const getRiskBadgeClass = (risk) => {
    switch (risk?.toUpperCase()) {
      case 'HIGH': return 'badge-high';
      case 'MEDIUM': return 'badge-medium';
      case 'LOW': return 'badge-low';
      case 'HEALTHY': return 'badge-healthy';
      default: return 'badge-medium';
    }
  };

  return (
    <div className="analysis-result-view animate-fade-in">
      {/* Top Banner Card */}
      <div className="result-header-card glass-card">
        <div className="result-header-main">
          <div className="result-title-col">
            <div className="result-crop-row">
              <span className="result-crop-name">{displayCrop}</span>
              <span className={`badge ${getRiskBadgeClass(result.risk_level)} animate-pulse-glow`}>
                {ml.risk_level_label || `${result.risk_level} RISK`}
              </span>
              <span className="confidence-pill" title="AI Model Confidence">
                {Math.round((result.confidence || 0.9) * 100)}% Match
              </span>
              {result.ai_provider === 'gemini' ? (
                <span className="badge badge-gemini" title="Real-time multimodal Google Gemini inference">
                  ✨ Powered by Google Gemini
                </span>
              ) : (
                <span className="badge badge-demo" title="Domain-grounded simulation fallback">
                  🧪 Demo Simulation
                </span>
              )}
            </div>
            <h2 className="result-condition-title">{displayCondition}</h2>
            {displaySummary && (
              <p className="result-summary-lead">{displaySummary}</p>
            )}
            {result.limitations && (
              <p className="text-xs text-dim mt-2 italic">
                * {result.limitations}
              </p>
            )}
          </div>

          {/* Audio TTS Advisory Player */}
          <div className="result-audio-col">
            <AudioPlayer 
              text={speechText} 
              language={currentLang}
              label={t.btnListenAdvisory}
              t={t}
            />
          </div>
        </div>

        {/* Monitoring & Escalation Bar */}
        <div className="result-meta-bar">
          <div className="meta-item">
            <Clock size={16} className="text-dim" />
            <span><strong>{t.monitoringPeriod}:</strong> {result.monitoring_period || '48 hours'}</span>
          </div>
          {result.escalation_required && (
            <div className="meta-item text-amber">
              <ShieldAlert size={16} />
              <span>{t.escalateNotice}</span>
            </div>
          )}
        </div>
      </div>

      {/* Main Grid: Actions, Symptoms, Weather Context */}
      <div className="grid-2 result-grid-sections">
        {/* Left Column: Immediate Recommended Actions */}
        <div className="glass-card result-section-card border-emerald">
          <div className="section-card-header">
            <CheckSquare size={20} className="text-emerald" />
            <h3>{t.immediateActions}</h3>
          </div>
          <p className="section-card-desc">Practical, field-tested recovery interventions for smallholder growers:</p>
          <ul className="action-checklist">
            {displayImmediate.map((act, idx) => (
              <li key={idx} className="action-item">
                <span className="action-num">{idx + 1}</span>
                <span className="action-text">{act}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Right Column: Symptoms & Causes */}
        <div className="glass-card result-section-card">
          <div className="section-card-header">
            <Eye size={20} className="text-cyan" />
            <h3>{t.symptomsObserved}</h3>
          </div>
          <ul className="symptoms-list">
            {(result.visual_symptoms || []).map((sym, idx) => (
              <li key={idx} className="symptom-item">
                <span className="bullet-dot"></span>
                <span>{sym}</span>
              </li>
            ))}
          </ul>

          <div className="section-sub-block">
            <h4 className="sub-block-title">{t.possibleCauses}</h4>
            <ul className="causes-list">
              {(result.possible_causes || []).map((cau, idx) => (
                <li key={idx} className="cause-item">{cau}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Secondary Row: Preventive Measures & Weather Correlation */}
      <div className="grid-2 result-grid-secondary">
        {/* Preventive Actions */}
        <div className="glass-card result-section-card">
          <div className="section-card-header">
            <ShieldAlert size={20} className="text-mint" />
            <h3>{t.preventiveActions}</h3>
          </div>
          <ul className="preventive-list">
            {displayPreventive.map((prev, idx) => (
              <li key={idx} className="preventive-item">
                <CheckCircle size={16} className="text-emerald flex-shrink-0" />
                <span>{prev}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Weather Impact Context */}
        {result.weather_context && (
          <div className="glass-card result-section-card">
            <div className="section-card-header">
              <CloudSun size={20} className="text-amber" />
              <h3>{t.weatherImpact}</h3>
            </div>
            <div className="weather-snapshot">
              <span className="weather-chip">Temp: {result.weather_context.temperature}</span>
              <span className="weather-chip">Humidity: {result.weather_context.humidity}</span>
              <span className="weather-chip">Rain Chance: {result.weather_context.rain_chance}</span>
            </div>
            <p className="weather-correlation-text">
              {result.weather_context.agro_impact}
            </p>
          </div>
        )}
      </div>

      {/* Satellite Environmental Context (Sentinel-2 / Demo Mode) */}
      {result.satellite_context && (
        <SatelliteIntelligence satelliteData={result.satellite_context} t={t} />
      )}

      {/* Signature Action Bar: Verify Again & Ask Agronomist */}
      <div className="result-action-footer glass-card">
        <div className="footer-action-info">
          <h4>Next Step: Apply advisory and track recovery</h4>
          <p>Scan again in 48-72 hours to verify symptom remission and validate plant health recovery.</p>
        </div>
        <div className="footer-buttons">
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={onScanAnother}
          >
            <RotateCcw size={16} />
            <span>Scan Another</span>
          </button>
          <button 
            type="button" 
            className="btn btn-voice"
            onClick={() => onAskAgronomist(result.crop, result.condition)}
          >
            <MessageSquare size={16} />
            <span>{t.btnAskAgronomist}</span>
          </button>
          <button 
            type="button" 
            className="btn btn-verify btn-lg"
            onClick={() => onVerifyAgain(result)}
          >
            <span>{t.btnVerifyAgain}</span>
            <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
