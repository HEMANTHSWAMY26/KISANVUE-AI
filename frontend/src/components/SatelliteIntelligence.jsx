import React from 'react';
import { 
  Activity, 
  Droplets, 
  Leaf, 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  HelpCircle, 
  Calendar, 
  Info,
  Layers,
  Sparkles
} from 'lucide-react';

export default function SatelliteIntelligence({ satelliteData, t = {} }) {
  if (!satelliteData || !satelliteData.available) {
    return null;
  }

  const isDemo = satelliteData.is_demo !== false && satelliteData.mode !== 'real';
  const obsDate = satelliteData.observation_date || 'Recent Cycle';
  const ndvi = satelliteData.ndvi !== undefined && satelliteData.ndvi !== null ? Number(satelliteData.ndvi).toFixed(2) : '--';
  const ndwi = satelliteData.ndwi !== undefined && satelliteData.ndwi !== null ? Number(satelliteData.ndwi).toFixed(2) : '--';
  const status = (satelliteData.vegetation_status || 'MODERATE').toUpperCase();
  const trend = (satelliteData.vegetation_trend || 'INCONCLUSIVE').toUpperCase();

  // Status badge styling
  const getStatusBadgeClass = (st) => {
    switch (st) {
      case 'HEALTHY': return 'badge-healthy';
      case 'MODERATE': return 'badge-medium';
      case 'STRESSED': return 'badge-high';
      case 'CRITICAL': return 'badge-critical';
      default: return 'badge-medium';
    }
  };

  // Trend icon & styling
  const renderTrendIcon = (tr) => {
    switch (tr) {
      case 'IMPROVING':
        return <span className="trend-indicator text-emerald"><TrendingUp size={16} /> IMPROVING</span>;
      case 'DECLINING':
        return <span className="trend-indicator text-crimson"><TrendingDown size={16} /> DECLINING</span>;
      case 'STABLE':
        return <span className="trend-indicator text-cyan"><Minus size={16} /> STABLE</span>;
      case 'INCONCLUSIVE':
      default:
        return <span className="trend-indicator text-dim"><HelpCircle size={16} /> INCONCLUSIVE</span>;
    }
  };

  // NDVI interpretive text
  const getNdviDescriptor = (val) => {
    const num = parseFloat(val);
    if (isNaN(num)) return 'Vegetation signal';
    if (num >= 0.65) return 'Strong vegetation signal';
    if (num >= 0.45) return 'Moderate vegetation signal';
    if (num >= 0.25) return 'Weaker/stressed vegetation signal';
    return 'Low vegetative reflectance';
  };

  // NDWI interpretive text
  const getNdwiDescriptor = (val) => {
    const num = parseFloat(val);
    if (isNaN(num)) return 'Moisture-context indicator';
    if (num >= 0.25) return 'Adequate canopy hydration context';
    if (num >= 0.10) return 'Moderate canopy moisture context';
    return 'Lower moisture-related canopy signal';
  };

  return (
    <div className="satellite-intelligence-card glass-card">
      {/* Header */}
      <div className="satellite-card-header">
        <div className="satellite-title-row">
          <div className="satellite-icon-pill">
            <span className="sat-emoji">🛰️</span>
            <span className="sat-title">{t.satelliteTitle || 'SATELLITE INTELLIGENCE'}</span>
          </div>
          <div className="satellite-source-tag">
            <span className="sat-source-name">{isDemo ? 'Sentinel-2 (Simulated)' : 'Sentinel-2'}</span>
          </div>
        </div>

        <div className="satellite-meta-row">
          <div className="satellite-obs-date">
            <Calendar size={14} className="text-dim" />
            <span>{t.observationDate || 'Observation'}: <strong>{obsDate}</strong></span>
          </div>
          <div className="satellite-badge-wrap">
            {isDemo ? (
              <span className="badge badge-demo animate-pulse-glow" title="Simulated context calibrated for evaluation">
                🧪 {t.demoSatelliteBadge || 'Demo Satellite Intelligence'}
              </span>
            ) : (
              <span className="badge badge-emerald" title="Live multi-spectral Sentinel-2 observation">
                ✨ {t.realSatelliteBadge || 'Sentinel-2 Live'}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Primary Metrics Grid: NDVI, NDWI, Status, Trend */}
      <div className="satellite-metrics-grid">
        {/* NDVI */}
        <div className="sat-metric-tile">
          <div className="sat-tile-header">
            <Activity size={15} className="text-emerald" />
            <span className="sat-tile-label">NDVI</span>
          </div>
          <div className="sat-tile-val text-emerald">{ndvi}</div>
          <div className="sat-tile-desc">{getNdviDescriptor(ndvi)}</div>
        </div>

        {/* NDWI */}
        <div className="sat-metric-tile">
          <div className="sat-tile-header">
            <Droplets size={15} className="text-cyan" />
            <span className="sat-tile-label">NDWI</span>
          </div>
          <div className="sat-tile-val text-cyan">{ndwi}</div>
          <div className="sat-tile-desc">{getNdwiDescriptor(ndwi)}</div>
        </div>

        {/* Vegetation Status */}
        <div className="sat-metric-tile">
          <div className="sat-tile-header">
            <Leaf size={15} className="text-mint" />
            <span className="sat-tile-label">{t.vegetationStatusLabel || 'Vegetation'}</span>
          </div>
          <div className="sat-tile-badge-val">
            <span className={`badge ${getStatusBadgeClass(status)}`}>
              {status}
            </span>
          </div>
          <div className="sat-tile-desc">Canopy vigour indicator</div>
        </div>

        {/* Vegetation Trend */}
        <div className="sat-metric-tile">
          <div className="sat-tile-header">
            <TrendingUp size={15} className="text-amber" />
            <span className="sat-tile-label">{t.vegetationTrendLabel || 'Trend'}</span>
          </div>
          <div className="sat-tile-trend-val">
            {renderTrendIcon(trend)}
          </div>
          <div className="sat-tile-desc">Multi-temporal comparison</div>
        </div>
      </div>

      {/* Field-level Summary */}
      {satelliteData.crop_health_summary && (
        <div className="satellite-summary-box">
          <p className="satellite-summary-text">
            {satelliteData.crop_health_summary}
          </p>
        </div>
      )}

      {/* Footnote / Disclaimer */}
      <div className="satellite-footnote">
        <Info size={13} className="text-dim flex-shrink-0" />
        <span className="footnote-text">
          {isDemo ? (
            <em>Simulated satellite context for demonstration. NDVI & NDWI represent canopy reflectance metrics, not a disease diagnosis.</em>
          ) : (
            <em>Sentinel-2 multi-spectral surface reflectance. Contextual environmental indicator alongside ground scouting.</em>
          )}
        </span>
      </div>
    </div>
  );
}
