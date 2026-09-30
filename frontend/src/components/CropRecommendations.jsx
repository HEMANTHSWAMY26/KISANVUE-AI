import React from 'react';
import { Sprout, RefreshCw, ShieldCheck, Droplets, Sun, Sparkles, CheckCircle2 } from 'lucide-react';

export default function CropRecommendations({ recommendations, t = {} }) {
  if (!recommendations) return null;

  const crops = recommendations.recommended_crops || [];
  const regenOptions = recommendations.regenerative_options || [];
  const summary = recommendations.agronomic_summary || '';
  const provider = recommendations.ai_provider || 'gemini';

  const getRiskBadge = (risk) => {
    switch (risk?.toUpperCase()) {
      case 'LOW':
        return <span className="badge badge-low">LOW RISK</span>;
      case 'MEDIUM':
        return <span className="badge badge-medium">MODERATE RISK</span>;
      case 'HIGH':
        return <span className="badge badge-high">HIGH RISK</span>;
      default:
        return <span className="badge badge-low">LOW RISK</span>;
    }
  };

  return (
    <div className="crop-recommendations-wrapper">
      {/* Section Header */}
      <div className="recommendations-header glass-card">
        <div className="rec-header-row">
          <div className="rec-title-pill">
            <Sprout size={20} className="text-emerald" />
            <h3>{t.recommendationTitle || 'Crop & Regenerative Strategy'}</h3>
          </div>
          <div className="rec-provider-badge">
            {provider === 'gemini' ? (
              <span className="badge badge-gemini">✨ Powered by Google Gemini</span>
            ) : (
              <span className="badge badge-demo">🧪 Domain Agro-Reasoning</span>
            )}
          </div>
        </div>
        {summary && (
          <p className="rec-lead-summary">{summary}</p>
        )}
      </div>

      <div className="grid-2 rec-main-grid mt-3">
        {/* Left Column: Recommended Crops */}
        <div className="glass-card rec-card border-emerald">
          <div className="rec-card-header">
            <Sprout size={18} className="text-emerald" />
            <h4>{t.recommendedCrops || 'Recommended Alternative / Rotation Crops'}</h4>
          </div>
          <div className="crops-list">
            {crops.map((c, idx) => (
              <div key={idx} className="crop-rec-item">
                <div className="crop-rec-top">
                  <strong className="crop-name text-mint">{c.crop}</strong>
                  {getRiskBadge(c.risk)}
                </div>
                <p className="crop-reason">{c.reason}</p>
                <div className="crop-fit-chips">
                  <span className="fit-chip" title="Soil Match">
                    🧱 {c.soil_fit}
                  </span>
                  <span className="fit-chip" title="Climate Match">
                    ☀️ {c.weather_fit}
                  </span>
                  <span className="fit-chip" title="Water Requirement">
                    💧 Water: {c.water_need}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Regenerative Agriculture Practices */}
        <div className="glass-card rec-card border-amber">
          <div className="rec-card-header">
            <RefreshCw size={18} className="text-amber" />
            <h4>{t.regenerativeTitle || 'Regenerative Agriculture Practices'}</h4>
          </div>
          <div className="regen-list">
            {regenOptions.map((rg, idx) => (
              <div key={idx} className="regen-item">
                <div className="regen-top">
                  <CheckCircle2 size={16} className="text-amber flex-shrink-0" />
                  <strong className="regen-practice-name">{rg.practice}</strong>
                </div>
                <div className="regen-benefit-box">
                  <span className="regen-label">Potential Ecological Benefit:</span>
                  <p className="regen-benefit-text">{rg.benefit}</p>
                </div>
                <p className="regen-reason-text">{rg.reason}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
