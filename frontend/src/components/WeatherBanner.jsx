import React, { useState } from 'react';
import { CloudRain, Droplets, Thermometer, Wind, MapPin, AlertCircle, Compass, ChevronDown, Sprout, Check } from 'lucide-react';

const PRESET_LOCATIONS = [
  { name: 'Guntur, Andhra Pradesh (Chilli Hub)', lat: 16.3067, lon: 80.4365, state: 'Andhra Pradesh', district: 'Guntur' },
  { name: 'Nashik, Maharashtra (Onion & Tomato)', lat: 19.9975, lon: 73.7898, state: 'Maharashtra', district: 'Nashik' },
  { name: 'Warangal, Telangana (Cotton & Chilli)', lat: 17.9689, lon: 79.5941, state: 'Telangana', district: 'Warangal' },
  { name: 'Ludhiana, Punjab (Wheat & Paddy)', lat: 30.9010, lon: 75.8573, state: 'Punjab', district: 'Ludhiana' },
  { name: 'Belagavi, Karnataka (Sugarcane & Maize)', lat: 15.8497, lon: 74.4977, state: 'Karnataka', district: 'Belagavi' },
  { name: 'Indore, Madhya Pradesh (Soybean & Wheat)', lat: 22.7196, lon: 75.8577, state: 'Madhya Pradesh', district: 'Indore' }
];

const PRESET_CROPS = [
  { id: 'Chilli', name: 'Chilli (మిరప / मिर्च)' },
  { id: 'Tomato', name: 'Tomato (టమోటా / टमाटर)' },
  { id: 'Cotton', name: 'Cotton (ప్రత్తి / कपास)' },
  { id: 'Rice', name: 'Paddy / Rice (వరి / धान)' },
  { id: 'Maize', name: 'Maize / Corn (మొక్కజొన్న / मक्का)' }
];

export default function WeatherBanner({ 
  weather, 
  currentLocation, 
  onLocationChange,
  selectedCrop,
  onCropChange,
  isLoadingContext = false,
  t = {} 
}) {
  const [showLocDropdown, setShowLocDropdown] = useState(false);
  const [showCropDropdown, setShowCropDropdown] = useState(false);
  const [isLocating, setIsLocating] = useState(false);

  if (!weather) return null;

  const handleUseMyLocation = () => {
    if (!navigator.geolocation) {
      alert('Browser geolocation is not supported on this device.');
      return;
    }
    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setIsLocating(false);
        const { latitude, longitude } = pos.coords;
        onLocationChange({
          name: `My GPS Location (${latitude.toFixed(2)}°N, ${longitude.toFixed(2)}°E)`,
          lat: latitude,
          lon: longitude,
          state: 'Local Field',
          district: 'GPS Coordinates'
        });
        setShowLocDropdown(false);
      },
      (err) => {
        setIsLocating(false);
        console.warn('Geolocation error:', err);
        alert('Could not retrieve GPS location. Falling back to regional agricultural hub.');
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  const activeLocName = currentLocation?.name || weather.location || 'Guntur, Andhra Pradesh';
  const activeCropName = PRESET_CROPS.find(c => c.id === selectedCrop)?.name || selectedCrop || 'Chilli';

  return (
    <div className="weather-banner glass-card">
      <div className="weather-top-row">
        {/* Dynamic Location & Crop Controls */}
        <div className="weather-location-controls">
          {/* Location Picker */}
          <div className="location-picker-wrapper">
            <button 
              type="button"
              className="location-picker-btn"
              onClick={() => { setShowLocDropdown(!showLocDropdown); setShowCropDropdown(false); }}
              title="Change agricultural district or coordinates"
            >
              <MapPin size={15} className="weather-icon-pin text-emerald" />
              <span className="location-name">{activeLocName}</span>
              <ChevronDown size={14} className="text-dim" />
            </button>

            {showLocDropdown && (
              <div className="location-dropdown-panel glass-card animate-fade-in">
                <div className="dropdown-section-title">Select Agricultural District:</div>
                <div className="location-presets-list">
                  {PRESET_LOCATIONS.map((loc, idx) => (
                    <button
                      key={idx}
                      type="button"
                      className={`preset-loc-item ${currentLocation?.lat === loc.lat ? 'active' : ''}`}
                      onClick={() => {
                        onLocationChange(loc);
                        setShowLocDropdown(false);
                      }}
                    >
                      <div className="preset-loc-meta">
                        <strong>{loc.name}</strong>
                        <span className="text-xs text-dim">Lat: {loc.lat.toFixed(2)}°, Lon: {loc.lon.toFixed(2)}°</span>
                      </div>
                      {currentLocation?.lat === loc.lat && <Check size={14} className="text-emerald" />}
                    </button>
                  ))}
                </div>

                <div className="dropdown-divider"></div>

                <button 
                  type="button" 
                  className="btn btn-secondary btn-sm w-full location-gps-btn"
                  onClick={handleUseMyLocation}
                  disabled={isLocating}
                >
                  <Compass size={14} className={isLocating ? 'spin-icon' : 'text-cyan'} />
                  <span>{isLocating ? 'Acquiring GPS...' : 'Use My GPS Location'}</span>
                </button>
              </div>
            )}
          </div>

          {/* Active Crop Selector */}
          <div className="crop-picker-wrapper">
            <button
              type="button"
              className="crop-picker-btn"
              onClick={() => { setShowCropDropdown(!showCropDropdown); setShowLocDropdown(false); }}
              title="Change target crop context"
            >
              <Sprout size={15} className="text-mint" />
              <span className="crop-picker-name">{activeCropName.split('(')[0].trim()}</span>
              <ChevronDown size={13} className="text-dim" />
            </button>

            {showCropDropdown && (
              <div className="crop-dropdown-panel glass-card animate-fade-in">
                <div className="dropdown-section-title">Focus Crop Context:</div>
                <div className="crop-presets-list">
                  {PRESET_CROPS.map((cp) => (
                    <button
                      key={cp.id}
                      type="button"
                      className={`preset-crop-item ${selectedCrop === cp.id ? 'active' : ''}`}
                      onClick={() => {
                        onCropChange(cp.id);
                        setShowCropDropdown(false);
                      }}
                    >
                      <span>{cp.name}</span>
                      {selectedCrop === cp.id && <Check size={14} className="text-emerald" />}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <span className="weather-tag">Agro-Meteorology</span>
          {isLoadingContext && <span className="sync-badge">Syncing Context...</span>}
        </div>

        {/* Real-time Weather Metrics from Open-Meteo */}
        <div className="weather-metrics">
          <div className="metric-item" title="Field Temperature">
            <Thermometer size={16} className="metric-icon temp" />
            <span className="metric-val">{weather.temperature}</span>
          </div>
          <div className="metric-item" title="Relative Humidity">
            <Droplets size={16} className="metric-icon hum" />
            <span className="metric-val">{weather.humidity}</span>
          </div>
          <div className="metric-item" title="Precipitation Probability">
            <CloudRain size={16} className="metric-icon rain" />
            <span className="metric-val">{weather.rain_chance} Rain</span>
          </div>
          <div className="metric-item hide-on-mobile" title="Wind Velocity">
            <Wind size={16} className="metric-icon wind" />
            <span className="metric-val">{weather.wind_speed}</span>
          </div>
        </div>
      </div>

      {/* Agro-Meteorological Fungal & Spray Window Advisory */}
      {weather.agro_impact && (
        <div className="weather-impact-alert">
          <AlertCircle size={15} className="alert-icon" />
          <p className="impact-text">
            <strong>Micro-Climate Advisory:</strong> {weather.agro_impact}
          </p>
        </div>
      )}
    </div>
  );
}
