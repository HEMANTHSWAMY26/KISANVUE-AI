import React, { useState, useRef } from 'react';
import { 
  GitCompare, 
  Upload, 
  Camera, 
  CheckCircle2, 
  TrendingUp, 
  ArrowRight, 
  ShieldCheck, 
  RotateCcw,
  Sparkles,
  Calendar,
  AlertCircle
} from 'lucide-react';
import AudioPlayer from './AudioPlayer';

export default function VerifyAgain({ 
  initialAnalysis, 
  currentLang, 
  onRunVerification, 
  isVerifying,
  verificationResult, 
  sampleCrops = [],
  t 
}) {
  const [followupImage, setFollowupImage] = useState(null);
  const [followupPreview, setFollowupPreview] = useState('/samples/chilli_recovered.jpg');
  const [daysElapsed, setDaysElapsed] = useState(5);
  const fileInputRef = useRef(null);

  const baselineCrop = initialAnalysis?.crop || 'Chilli (మిరప / मिर्च)';
  const baselineCondition = initialAnalysis?.condition || 'Chilli Leaf Curl Virus (Begomovirus)';
  const baselineRisk = initialAnalysis?.risk_level || 'HIGH';
  const baselineImage = initialAnalysis?.imagePreview || '/samples/chilli_leaf_curl.jpg';

  const handleFile = (file) => {
    if (!file) return;
    setFollowupImage(file);
    const url = URL.createObjectURL(file);
    setFollowupPreview(url);
  };

  const handleSelectSampleFollowup = async (sample) => {
    try {
      const res = await fetch(sample.path);
      const blob = await res.blob();
      const file = new File([blob], sample.file, { type: 'image/jpeg' });
      setFollowupImage(file);
      setFollowupPreview(sample.path);
    } catch (e) {
      console.error('Failed to load sample followup:', e);
    }
  };

  const handleExecuteVerification = async () => {
    let fileToSend = followupImage;
    if (!fileToSend) {
      // Fetch default sample
      try {
        const res = await fetch(followupPreview);
        const blob = await res.blob();
        fileToSend = new File([blob], 'chilli_recovered.jpg', { type: 'image/jpeg' });
      } catch (err) {
        console.warn('Could not fetch default preview:', err);
      }
    }
    onRunVerification(fileToSend, baselineCondition, baselineRisk, daysElapsed);
  };

  const ml = verificationResult?.multilingual || {};
  const displaySummary = ml.summary || verificationResult?.comparison_summary || '';
  const displayChanges = ml.observed_changes || verificationResult?.observed_changes || [];
  const displayRecs = ml.ongoing_recommendations || verificationResult?.ongoing_recommendations || [];
  const speechText = ml.speech_summary || displaySummary;

  return (
    <div className="verify-again-view animate-fade-in">
      {/* Header */}
      <div className="verify-header text-center">
        <div className="badge badge-medium mb-2">
          <GitCompare size={14} />
          <span>VERIFY-AGAIN ENGINE</span>
        </div>
        <h1 className="hero-title">{t.verifyTitle}</h1>
        <p className="hero-subtitle">{t.verifySubtitle}</p>
      </div>

      {/* Comparison Viewport */}
      <div className="comparison-grid grid-2">
        {/* Baseline Card */}
        <div className="comparison-card glass-card">
          <div className="comparison-card-top">
            <span className="badge badge-high">BASELINE: INITIAL SCAN</span>
            <span className="comparison-timestamp">Day 0 (Initial Advisory)</span>
          </div>
          <div className="comparison-img-box">
            <img src={baselineImage} alt="Initial Scan" className="comparison-img" />
            <div className="comparison-img-overlay">
              <span className="overlay-condition">{baselineCondition}</span>
              <span className="badge badge-high">{baselineRisk} RISK</span>
            </div>
          </div>
          <div className="comparison-details">
            <h4>{baselineCrop}</h4>
            <p className="text-dim text-sm">
              Baseline diagnosis indicated upward curl and whitefly infestation. Advisory instructed neem oil application and yellow sticky traps.
            </p>
          </div>
        </div>

        {/* Follow-up Scan Card */}
        <div className="comparison-card glass-card border-verify">
          <div className="comparison-card-top">
            <span className="badge badge-medium">FOLLOW-UP: VERIFY SCAN</span>
            <div className="days-picker">
              <Calendar size={14} />
              <span>{daysElapsed} Days Post Advisory</span>
            </div>
          </div>
          <div className="comparison-img-box">
            <img src={followupPreview} alt="Follow-up Scan" className="comparison-img" />
            <div className="comparison-img-actions">
              <input 
                type="file" 
                ref={fileInputRef} 
                accept="image/*" 
                className="hidden-input"
                onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              />
              <button 
                type="button" 
                className="btn btn-secondary btn-sm"
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload size={14} />
                <span>Upload New Scan</span>
              </button>
            </div>
          </div>

          <div className="comparison-details">
            <div className="sample-quick-pick">
              <span className="text-xs text-dim">Quick Test Sample:</span>
              <button 
                type="button"
                className="btn-pill-sample"
                onClick={() => handleSelectSampleFollowup({ path: '/samples/chilli_recovered.jpg', file: 'chilli_recovered.jpg' })}
              >
                🌶️ Recovered Chilli (5-Day Post Advisory)
              </button>
            </div>

            <div className="days-slider-row">
              <label className="text-sm font-medium">Days Elapsed Post Advisory: <strong>{daysElapsed} days</strong></label>
              <input 
                type="range" 
                min="2" 
                max="14" 
                value={daysElapsed} 
                onChange={(e) => setDaysElapsed(Number(e.target.value))}
                className="range-slider"
              />
            </div>

            <button 
              type="button" 
              className="btn btn-verify w-full mt-3"
              disabled={isVerifying}
              onClick={handleExecuteVerification}
            >
              <Sparkles size={18} />
              <span>{isVerifying ? 'Evaluating Recovery...' : t.btnRunVerification}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Verification Result Section */}
      {verificationResult && (
        <div className="verification-results-panel glass-card mt-4 animate-fade-in">
          {/* Recovery Trajectory Header */}
          <div className="verify-result-header">
            <div className="verify-status-col">
              <div className="verify-badge-row">
                <span className="badge badge-healthy text-sm">
                  <ShieldCheck size={16} />
                  <span>{ml.recovery_status_label || t.statusImproving}</span>
                </span>
                <span className="recovery-score-pill">
                  Score: <strong>{verificationResult.recovery_score}/100</strong>
                </span>
              </div>
              <h2 className="verify-progress-title">Crop Health Progress: Improving</h2>
              <p className="verify-summary-lead">{displaySummary}</p>
            </div>

            {/* Audio Voice Player */}
            <div className="verify-audio-col">
              <AudioPlayer 
                text={speechText} 
                language={currentLang}
                label={t.btnListenAdvisory}
                t={t}
              />
            </div>
          </div>

          {/* Risk Migration Indicator */}
          <div className="risk-migration-bar glass-card">
            <div className="risk-box prev">
              <span className="risk-title">{t.previousRisk}</span>
              <span className="badge badge-high text-md">{verificationResult.previous_risk_level}</span>
            </div>
            <div className="risk-arrow">
              <ArrowRight size={24} className="text-emerald" />
              <span className="text-xs text-emerald">Risk Reduced</span>
            </div>
            <div className="risk-box curr">
              <span className="risk-title">{t.currentRisk}</span>
              <span className="badge badge-medium text-md">{verificationResult.current_risk_level}</span>
            </div>
          </div>

          {/* Observed Milestones & Ongoing Maintenance */}
          <div className="grid-2 mt-4">
            <div className="glass-card result-section-card">
              <div className="section-card-header">
                <TrendingUp size={20} className="text-emerald" />
                <h3>{t.observedImprovements}</h3>
              </div>
              <ul className="action-checklist">
                {displayChanges.map((ch, idx) => (
                  <li key={idx} className="action-item">
                    <CheckCircle2 size={18} className="text-emerald flex-shrink-0" />
                    <span className="action-text">{ch}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="glass-card result-section-card">
              <div className="section-card-header">
                <ShieldCheck size={20} className="text-amber" />
                <h3>{t.ongoingCare}</h3>
              </div>
              <ul className="preventive-list">
                {displayRecs.map((rec, idx) => (
                  <li key={idx} className="preventive-item">
                    <span className="action-num">{idx + 1}</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
