import React from 'react';
import { MapPin, CloudSun, Radio, Layers, Sprout, RefreshCw, CheckCircle, Info } from 'lucide-react';

export default function FarmSnapshot({ farmData, t = {} }) {
  if (!farmData) return null;

  const loc = farmData.location_name || 'Guntur, Andhra Pradesh';
  const weather = farmData.weather || {};
  const sat = farmData.satellite || {};
  const soil = farmData.soil || {};
  const recs = farmData.recommendations || {};
  const topCrop = (recs.recommended_crops && recs.recommended_crops[0]) || null;
  const topRegen = (recs.regenerative_options && recs.regenerative_options[0]) || null;
  const flags = farmData.transparency_flags || {};

  return (
    <div className="farm-snapshot-card glass-card">
      <div className="farm-snapshot-header">
        <div className="snapshot-title-group">
          <span className="snapshot-emoji">🌾</span>
          <h3>{t.farmSnapshotTitle || 'UNIFIED FARM INTELLIGENCE'}</h3>
        </div>
        <div className="snapshot-location-pill">
          <MapPin size={14} className="text-emerald" />
          <span>{loc}</span>
        </div>
      </div>

      <div className="snapshot-layers-grid">
        {/* Weather Layer */}
        <div className="snapshot-layer-cell">
          <div className="layer-cell-top">
            <CloudSun size={15} className="text-amber" />
            <span className="layer-name">Weather</span>
            <span className="source-pill">{flags.weather_live ? 'Open-Meteo' : 'Simulated'}</span>
          </div>
          <div className="layer-main-val text-amber">
            {weather.temperature || '30°C'} / {weather.humidity || '75% RH'}
          </div>
          <p className="layer-sub-desc">{weather.weather_description || 'Partly Cloudy'}</p>
        </div>

        {/* Satellite Layer */}
        <div className="snapshot-layer-cell">
          <div className="layer-cell-top">
            <Radio size={15} className="text-cyan" />
            <span className="layer-name">Satellite</span>
            <span className={`source-pill ${sat.mode === 'real' ? 'live' : 'demo'}`}>
              {sat.mode === 'real' ? 'Sentinel-2' : 'Demo Sentinel'}
            </span>
          </div>
          <div className="layer-main-val text-cyan">
            NDVI {sat.ndvi !== undefined ? sat.ndvi : '0.72'}
          </div>
          <p className="layer-sub-desc">Vegetation: <strong>{sat.vegetation_status || 'HEALTHY'}</strong> ({sat.vegetation_trend || 'STABLE'})</p>
        </div>

        {/* Soil Layer */}
        <div className="snapshot-layer-cell">
          <div className="layer-cell-top">
            <Layers size={15} className="text-mint" />
            <span className="layer-name">Soil</span>
            <span className={`source-pill ${soil.mode === 'real' ? 'live' : 'demo'}`}>
              {soil.mode === 'real' ? 'SoilGrids' : 'Demo Soil'}
            </span>
          </div>
          <div className="layer-main-val text-mint">
            SOC: {soil.organic_carbon || '8.4'} g/kg
          </div>
          <p className="layer-sub-desc">Clay: {soil.clay_percent || '44'}% | Sand: {soil.sand_percent || '28'}%</p>
        </div>

        {/* Recommendation Layer */}
        <div className="snapshot-layer-cell highlight-cell">
          <div className="layer-cell-top">
            <Sprout size={15} className="text-emerald" />
            <span className="layer-name">Crop Rotation</span>
            <span className="source-pill ai">Gemini</span>
          </div>
          <div className="layer-main-val text-emerald">
            {topCrop ? topCrop.crop.split('(')[0] : 'Bengal Gram'}
          </div>
          <p className="layer-sub-desc line-clamp-2">
            {topCrop ? topCrop.reason : 'Restores nitrogen in clay soils.'}
          </p>
        </div>
      </div>

      {/* Regenerative Agriculture Highlight */}
      {topRegen && (
        <div className="snapshot-regen-bar">
          <div className="regen-bar-title">
            <RefreshCw size={14} className="text-amber" />
            <span>Regenerative Practice:</span>
            <strong>{topRegen.practice}</strong>
          </div>
          <p className="regen-bar-benefit">
            {topRegen.benefit}
          </p>
        </div>
      )}
    </div>
  );
}
