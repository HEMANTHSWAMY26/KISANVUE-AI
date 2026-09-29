import React from 'react';
import { Sprout, Globe, Activity, Layers } from 'lucide-react';

export default function Header({ 
  currentLang, 
  onLangChange, 
  activeTab, 
  onTabChange, 
  systemStatus,
  onOpenArchitecture,
  t 
}) {
  const languages = [
    { code: 'en', label: 'English', native: 'English' },
    { code: 'te', label: 'Telugu', native: 'తెలుగు' },
    { code: 'hi', label: 'Hindi', native: 'हिंदी' },
  ];

  return (
    <header className="header-bar">
      <div className="app-container header-inner">
        {/* Brand */}
        <div className="brand" onClick={() => onTabChange('scan')} style={{ cursor: 'pointer' }}>
          <div className="brand-logo">
            <Sprout size={28} className="brand-icon" />
          </div>
          <div className="brand-text">
            <div className="brand-title-row">
              <span className="brand-name">KisanVue</span>
              <span className="brand-ai">AI</span>
              <span className="brand-badge-prototype">HACKATHON MVP</span>
            </div>
            <span className="brand-tagline">{t.tagline}</span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="header-nav">
          <button 
            className={`nav-link ${activeTab === 'scan' ? 'active' : ''}`}
            onClick={() => onTabChange('scan')}
          >
            {t.navScan}
          </button>
          <button 
            className={`nav-link ${activeTab === 'verify' ? 'active' : ''}`}
            onClick={() => onTabChange('verify')}
          >
            {t.navVerify}
          </button>
          <button 
            className={`nav-link ${activeTab === 'voice' ? 'active' : ''}`}
            onClick={() => onTabChange('voice')}
          >
            {t.navVoice}
          </button>
          <button 
            className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => onTabChange('dashboard')}
          >
            {t.navDashboard}
          </button>
        </nav>

        {/* Right Tools: Architecture, Language & Health */}
        <div className="header-tools">
          {/* Architecture Modal Trigger */}
          <button 
            className="btn btn-secondary btn-sm arch-btn"
            onClick={onOpenArchitecture}
            title="India-Scale Architecture"
          >
            <Layers size={16} />
            <span className="hide-on-mobile">Architecture</span>
          </button>

          {/* Language Selector */}
          <div className="lang-switcher">
            <Globe size={16} className="lang-icon" />
            <select 
              value={currentLang} 
              onChange={(e) => onLangChange(e.target.value)}
              className="lang-select"
              aria-label="Select Language"
            >
              {languages.map((l) => (
                <option key={l.code} value={l.code}>
                  {l.native} ({l.label})
                </option>
              ))}
            </select>
          </div>

          {/* Backend Status */}
          <div className="status-pill" title="Gemini Agricultural Reasoning Engine Readiness">
            <span className={`status-dot ${systemStatus.gemini_ready ? 'online' : 'simulated'}`}></span>
            <span className="status-label hide-on-mobile">
              {systemStatus.gemini_ready ? 'Gemini Live' : 'AI Engine Ready'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
