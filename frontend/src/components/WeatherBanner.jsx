import React from 'react';
import { CloudRain, Droplets, Thermometer, Wind, MapPin, AlertCircle } from 'lucide-react';

export default function WeatherBanner({ weather }) {
  if (!weather) return null;

  return (
    <div className="weather-banner glass-card">
      <div className="weather-top-row">
        <div className="weather-location">
          <MapPin size={16} className="weather-icon-pin" />
          <span className="location-name">{weather.location || 'Guntur, Andhra Pradesh'}</span>
          <span className="weather-tag">Agro-Meteorology</span>
        </div>
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
