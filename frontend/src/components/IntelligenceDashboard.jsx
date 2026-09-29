import React from 'react';
import { 
  BarChart3, 
  AlertTriangle, 
  CheckCircle2, 
  MapPin, 
  ShieldAlert, 
  Layers, 
  TrendingUp,
  Info
} from 'lucide-react';

export default function IntelligenceDashboard({ telemetry, t }) {
  if (!telemetry) return null;

  const topCrops = telemetry.top_risk_crops || [];
  const hotspots = telemetry.regional_hotspots || [];

  return (
    <div className="intelligence-dashboard-view animate-fade-in">
      {/* Header */}
      <div className="dash-header text-center">
        <div className="badge badge-demo mb-2">
          <Info size={14} />
          <span>{telemetry.notice || t.demoDataWarning}</span>
        </div>
        <h1 className="hero-title">{t.dashboardTitle}</h1>
        <p className="hero-subtitle">{t.dashboardSubtitle}</p>
      </div>

      {/* Top 4 KPI Metric Cards */}
      <div className="grid-4 kpi-metrics-grid">
        <div className="glass-card kpi-card">
          <span className="kpi-label">{t.totalScans}</span>
          <h2 className="kpi-value text-emerald">{telemetry.total_scans?.toLocaleString() || '1,284'}</h2>
          <span className="kpi-sub">Across 5 monitored states</span>
        </div>

        <div className="glass-card kpi-card border-crimson">
          <span className="kpi-label">{t.highRiskAlerts}</span>
          <h2 className="kpi-value text-crimson">{telemetry.high_risk_alerts || '37'}</h2>
          <span className="kpi-sub">Whitefly & fungal alerts</span>
        </div>

        <div className="glass-card kpi-card border-amber">
          <span className="kpi-label">{t.activeAdvisories}</span>
          <h2 className="kpi-value text-amber">{telemetry.active_advisories || '214'}</h2>
          <span className="kpi-sub">IPM bio-spray active</span>
        </div>

        <div className="glass-card kpi-card border-emerald">
          <span className="kpi-label">{t.recoveredVerifications}</span>
          <h2 className="kpi-value text-mint">{telemetry.recovered_verifications || '89'}</h2>
          <span className="kpi-sub">Verified via Re-Scan</span>
        </div>
      </div>

      {/* Top Risk Crops & Regional Hotspots */}
      <div className="grid-2 dash-main-grid mt-4">
        {/* Top Risk Crops */}
        <div className="glass-card dash-section-card">
          <div className="section-card-header">
            <BarChart3 size={20} className="text-amber" />
            <h3>{t.topRiskCrops}</h3>
          </div>
          <div className="crop-risk-table">
            {topCrops.map((c, idx) => (
              <div key={idx} className="crop-risk-row">
                <div className="crop-risk-meta">
                  <span className="crop-icon-large">{c.icon}</span>
                  <div>
                    <strong className="crop-name-label">{c.crop}</strong>
                    <span className="crop-pathology-label">{c.common_pathology}</span>
                  </div>
                </div>
                <div className="crop-risk-stat">
                  <span className={`badge badge-sm badge-${c.risk_level?.toLowerCase()}`}>
                    {c.risk_level}
                  </span>
                  <span className="crop-perc">{c.affected_percentage}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Regional Hotspot Monitoring */}
        <div className="glass-card dash-section-card">
          <div className="section-card-header">
            <MapPin size={20} className="text-cyan" />
            <h3>{t.regionalHotspots}</h3>
          </div>
          <div className="hotspots-list">
            {hotspots.map((h, idx) => (
              <div key={idx} className="hotspot-item">
                <div className="hotspot-location">
                  <span className="hotspot-district">{h.district}</span>
                  <span className="hotspot-state">, {h.state}</span>
                  <span className="hotspot-crop-tag">({h.crop})</span>
                </div>
                <div className="hotspot-info-row">
                  <span className={`badge badge-xs badge-${h.risk_level?.toLowerCase()}`}>
                    {h.risk_level}
                  </span>
                  <span className="hotspot-cases">{h.active_cases} Active Reports</span>
                </div>
                <p className="hotspot-advisory-text">{h.advisory_status}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Demo Data Compliance Notice Banner */}
      <div className="demo-notice-banner glass-card mt-4">
        <Info size={18} className="text-dim" />
        <p className="text-xs text-dim">
          <strong>Hackathon Transparency Note:</strong> All dashboard telemetry presented above represents simulated data for prototype testing. 
          KisanVue AI does not claim this is verified government census data. In production, this layer connects to state agricultural university databases and farmer advisory networks.
        </p>
      </div>
    </div>
  );
}
