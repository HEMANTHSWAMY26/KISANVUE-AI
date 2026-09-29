import React from 'react';
import { X, Cpu, Cloud, MapPin, CheckCircle, Database, Smartphone, ShieldCheck } from 'lucide-react';

export default function ArchitectureModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content glass-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-row">
            <Cpu size={24} className="text-emerald" />
            <div>
              <h3>India-Scale Agricultural Intelligence Architecture</h3>
              <p className="text-xs text-dim">How KisanVue AI scales from village farm to national telemetry</p>
            </div>
          </div>
          <button type="button" className="btn-close-modal" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          {/* Architecture Pipeline Flow */}
          <div className="architecture-diagram">
            <div className="arch-node">
              <div className="arch-node-icon"><Smartphone size={20} className="text-emerald" /></div>
              <strong>1. Farmer Edge</strong>
              <span>Mobile Photo / Voice / GPS</span>
            </div>
            <div className="arch-connector">➔</div>

            <div className="arch-node">
              <div className="arch-node-icon"><Cpu size={20} className="text-cyan" /></div>
              <strong>2. Gemini Multimodal</strong>
              <span>Pathology & Reasoning</span>
            </div>
            <div className="arch-connector">➔</div>

            <div className="arch-node">
              <div className="arch-node-icon"><Cloud size={20} className="text-amber" /></div>
              <strong>3. Climate Context</strong>
              <span>Open-Meteo & Soil Risk</span>
            </div>
            <div className="arch-connector">➔</div>

            <div className="arch-node">
              <div className="arch-node-icon"><ShieldCheck size={20} className="text-mint" /></div>
              <strong>4. Verify-Again Loop</strong>
              <span>Efficacy Tracking (48h)</span>
            </div>
            <div className="arch-connector">➔</div>

            <div className="arch-node">
              <div className="arch-node-icon"><Database size={20} className="text-crimson" /></div>
              <strong>5. National Grid</strong>
              <span>Aggregated Telemetry</span>
            </div>
          </div>

          <div className="arch-details-grid grid-2 mt-4">
            <div className="arch-box">
              <h4>🤖 Google Gemini Integration</h4>
              <p className="text-sm text-dim">
                Gemini processes high-resolution field imagery alongside real-time humidity and thermal telemetry. 
                Rather than generic chatbots, it executes specialized crop pathology prompts to classify foliar lesions, 
                detect insect vector presence (such as <em>Bemisia tabaci</em>), and output strictly validated IPM field advisories.
              </p>
            </div>

            <div className="arch-box">
              <h4>🔄 The "Verify Again" Differentiator</h4>
              <p className="text-sm text-dim">
                Most AI agritech ends at diagnosis. KisanVue AI introduces a closed-loop verification pipeline where farmers 
                upload follow-up photos after applying treatment. The system computes a quantitative recovery score and tracks symptom remission over time.
              </p>
            </div>

            <div className="arch-box">
              <h4>🇮🇳 Multilingual Accessibility</h4>
              <p className="text-sm text-dim">
                Full end-to-end support for English, Telugu (తెలుగు), and Hindi (हिंदी). Built-in speech recognition and 
                oral speech synthesis allow illiterate and marginal farmers to interact conversationally with their crops.
              </p>
            </div>

            <div className="arch-box">
              <h4>🛡️ Responsible Agricultural AI</h4>
              <p className="text-sm text-dim">
                Adheres to safe agronomy: strictly avoids hallucinating extreme chemical dosages, prioritizes Integrated Pest Management (IPM) 
                and bio-control (Neem oil, sticky traps), and escalates severe cases to Krishi Vigyan Kendras (KVK).
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
