import React from 'react';
import { Sprout, ShieldAlert, Heart } from 'lucide-react';

export default function Footer({ t }) {
  return (
    <footer className="footer-bar">
      <div className="app-container footer-inner">
        {/* Safety Disclaimer Banner */}
        <div className="safety-disclaimer-card glass-card">
          <ShieldAlert size={20} className="text-amber flex-shrink-0" />
          <p className="disclaimer-text">
            <strong>Safety & Trust Notice:</strong> {t.disclaimer}
          </p>
        </div>

        {/* Brand & Attribution */}
        <div className="footer-bottom-row">
          <div className="footer-brand">
            <Sprout size={20} className="text-emerald" />
            <span className="footer-brand-name">KisanVue AI</span>
            <span className="footer-tagline">— {t.tagline}</span>
          </div>

          <div className="footer-hackathon">
            <span>Built for <strong>Google Cloud "Build with AI: Code for Communities"</strong> Hackathon</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
