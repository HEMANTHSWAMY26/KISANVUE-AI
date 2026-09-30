import React from 'react';
import { Layers, Info, CheckCircle2, ShieldCheck } from 'lucide-react';

export default function SoilCard({ soilData, t = {} }) {
  if (!soilData || !soilData.available) {
    return null;
  }

  const isDemo = soilData.is_demo !== false && soilData.mode !== 'real';
  const oc = soilData.organic_carbon !== undefined && soilData.organic_carbon !== null ? `${soilData.organic_carbon} g/kg` : '--';
  const clay = soilData.clay_percent !== undefined && soilData.clay_percent !== null ? `${soilData.clay_percent}%` : '--';
  const sand = soilData.sand_percent !== undefined && soilData.sand_percent !== null ? `${soilData.sand_percent}%` : '--';
  const silt = soilData.silt_percent !== undefined && soilData.silt_percent !== null ? `${soilData.silt_percent}%` : '--';
  const texture = soilData.soil_texture_class || 'Clay Loam';

  return (
    <div className="soil-intelligence-card glass-card">
      {/* Header */}
      <div className="soil-card-header">
        <div className="soil-title-row">
          <div className="soil-icon-pill">
            <span className="soil-emoji">🧪</span>
            <span className="soil-title">{t.soilTitle || 'SOIL INTELLIGENCE'}</span>
          </div>
          <div className="soil-source-tag">
            <span className="soil-source-name">{isDemo ? 'SoilGrids (Simulated)' : 'SoilGrids'}</span>
          </div>
        </div>

        <div className="soil-meta-row">
          <div className="soil-texture-label">
            <Layers size={14} className="text-amber" />
            <span>Profile: <strong>{texture}</strong></span>
          </div>
          <div className="soil-badge-wrap">
            {isDemo ? (
              <span className="badge badge-demo" title="Domain-calibrated regional soil profile">
                🧪 {t.demoSoilBadge || 'Demo Soil Intelligence'}
              </span>
            ) : (
              <span className="badge badge-emerald" title="Live ISRIC SoilGrids 250m global query">
                ✨ {t.realSoilBadge || 'SoilGrids Live'}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Primary Metrics Grid: Organic Carbon, Clay, Sand, Silt */}
      <div className="soil-metrics-grid">
        {/* Organic Carbon */}
        <div className="soil-metric-tile">
          <span className="soil-tile-label">{t.organicCarbon || 'Organic Carbon'}</span>
          <div className="soil-tile-val text-mint">{oc}</div>
          <div className="soil-tile-desc">Organic-carbon indicator</div>
        </div>

        {/* Clay % */}
        <div className="soil-metric-tile">
          <span className="soil-tile-label">{t.clayPercent || 'Clay'}</span>
          <div className="soil-tile-val text-amber">{clay}</div>
          <div className="soil-tile-desc">Moisture holding fraction</div>
        </div>

        {/* Sand % */}
        <div className="soil-metric-tile">
          <span className="soil-tile-label">{t.sandPercent || 'Sand'}</span>
          <div className="soil-tile-val text-cyan">{sand}</div>
          <div className="soil-tile-desc">Drainage & aeration context</div>
        </div>

        {/* Silt % */}
        <div className="soil-metric-tile">
          <span className="soil-tile-label">{t.siltPercent || 'Silt'}</span>
          <div className="soil-tile-val text-emerald">{silt}</div>
          <div className="soil-tile-desc">Fine mineral fraction</div>
        </div>
      </div>

      {/* Contextual Narrative */}
      {soilData.soil_context && (
        <div className="soil-context-box">
          <p className="soil-context-text">{soilData.soil_context}</p>
        </div>
      )}

      {/* Footnote / Scientific Transparency */}
      <div className="soil-footnote">
        <Info size={13} className="text-dim flex-shrink-0" />
        <span className="footnote-text">
          <em>{t.soilDisclaimer || 'Regional soil texture context. Does not replace physical laboratory soil testing.'}</em>
        </span>
      </div>
    </div>
  );
}
