import React, { useState, useRef } from 'react';
import { Camera, Upload, CheckCircle2, Loader2, Sparkles, RefreshCw, AlertCircle } from 'lucide-react';

export default function CropScanner({ 
  onAnalyze, 
  isAnalyzing, 
  scanStep, 
  error, 
  sampleCrops = [], 
  currentLang,
  t 
}) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [activeHint, setActiveHint] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);

  const handleFile = (file, hint = '') => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file (JPEG, PNG, WebP).');
      return;
    }
    setSelectedImage(file);
    setActiveHint(hint || file.name);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleSelectSample = async (sample) => {
    try {
      // Fetch sample as blob
      const res = await fetch(sample.path);
      const blob = await res.blob();
      const file = new File([blob], sample.file, { type: 'image/jpeg' });
      handleFile(file, sample.file);
    } catch (err) {
      console.error('Failed to load sample image:', err);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = () => {
    if (!selectedImage) return;
    onAnalyze(selectedImage, activeHint);
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setActiveHint('');
    if (fileInputRef.current) fileInputRef.current.value = '';
    if (cameraInputRef.current) cameraInputRef.current.value = '';
  };

  const steps = [
    { id: 1, label: t.step1 },
    { id: 2, label: t.step2 },
    { id: 3, label: t.step3 },
    { id: 4, label: t.step4 },
    { id: 5, label: t.step5 },
  ];

  return (
    <div className="crop-scanner-section">
      {/* Hero Intro */}
      <div className="scanner-hero text-center">
        <h1 className="hero-title">{t.heroTitle}</h1>
        <p className="hero-subtitle">{t.heroSubtitle}</p>
      </div>

      {/* Quick 1-Click Test Samples */}
      <div className="quick-samples-bar glass-card">
        <div className="quick-samples-header">
          <Sparkles size={16} className="text-amber" />
          <span className="quick-samples-title">{t.quickSamplesTitle}</span>
        </div>
        <div className="sample-chips-row">
          {sampleCrops.map((sample) => (
            <button
              key={sample.id}
              type="button"
              className={`sample-chip ${activeHint === sample.file ? 'active' : ''}`}
              onClick={() => handleSelectSample(sample)}
            >
              <img src={sample.path} alt={sample.name} className="sample-chip-thumb" />
              <div className="sample-chip-info">
                <span className="sample-chip-name">{sample.name}</span>
                <span className={`badge badge-xs badge-${sample.expected_risk.toLowerCase()}`}>
                  {sample.expected_risk}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Upload & Viewport Area */}
      <div className="scanner-main-card glass-card">
        {!previewUrl ? (
          <div 
            className={`dropzone ${isDragging ? 'dragging' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              accept="image/*" 
              className="hidden-input"
              onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
            />
            <input 
              type="file" 
              ref={cameraInputRef} 
              accept="image/*" 
              capture="environment" 
              className="hidden-input"
              onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
            />

            <div className="dropzone-content">
              <div className="dropzone-icon-circle">
                <Camera size={36} className="dropzone-icon" />
              </div>
              <h3 className="dropzone-title">Take or Upload a Crop Photo</h3>
              <p className="dropzone-hint">
                Photograph affected leaves, stems, or pests under natural daylight. Supports JPG, PNG, WebP.
              </p>

              <div className="dropzone-actions">
                <button 
                  type="button" 
                  className="btn btn-primary"
                  onClick={() => cameraInputRef.current?.click()}
                >
                  <Camera size={18} />
                  <span>{t.btnTakeLivePhoto}</span>
                </button>
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <Upload size={18} />
                  <span>{t.btnUploadImage}</span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="preview-container">
            <div className="preview-image-wrapper">
              <img src={previewUrl} alt="Crop Scan Target" className="preview-image" />
              {isAnalyzing && (
                <div className="laser-scanline"></div>
              )}
              <div className="preview-overlay-info">
                <span className="preview-filename">{activeHint || selectedImage?.name}</span>
                {!isAnalyzing && (
                  <button type="button" className="btn-icon-clear" onClick={handleReset} title="Change photo">
                    <RefreshCw size={16} />
                  </button>
                )}
              </div>
            </div>

            {/* Analysis Progress or Action Button */}
            {isAnalyzing ? (
              <div className="analysis-progress-panel">
                <div className="progress-header">
                  <Loader2 size={24} className="spin-icon text-emerald" />
                  <h4>{t.analyzingTitle}</h4>
                </div>
                <div className="steps-checklist">
                  {steps.map((st) => {
                    const isDone = scanStep >= st.id;
                    const isCurrent = scanStep === st.id;
                    return (
                      <div key={st.id} className={`step-item ${isDone ? 'completed' : ''} ${isCurrent ? 'current' : ''}`}>
                        <div className="step-marker">
                          {isDone ? (
                            <CheckCircle2 size={18} className="text-emerald" />
                          ) : (
                            <span className="step-circle">{st.id}</span>
                          )}
                        </div>
                        <span className="step-label">{st.label}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="preview-action-row">
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={handleReset}
                >
                  <RefreshCw size={16} />
                  <span>Choose Another Image</span>
                </button>
                <button 
                  type="button" 
                  className="btn btn-primary btn-lg"
                  onClick={handleSubmit}
                >
                  <Sparkles size={20} />
                  <span>{t.btnStartAnalysis}</span>
                </button>
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="scanner-error-box">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}
      </div>
    </div>
  );
}
