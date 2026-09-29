import React, { useState, useEffect } from 'react';
import { translations } from './i18n/translations';
import { 
  checkSystemHealth, 
  fetchLiveWeather, 
  analyzeCropImage, 
  verifyCropRecovery, 
  askAgronomist, 
  fetchDashboardTelemetry, 
  fetchSampleCrops 
} from './services/api';

import Header from './components/Header';
import Footer from './components/Footer';
import WeatherBanner from './components/WeatherBanner';
import CropScanner from './components/CropScanner';
import AnalysisResult from './components/AnalysisResult';
import VerifyAgain from './components/VerifyAgain';
import VoiceAgronomist from './components/VoiceAgronomist';
import IntelligenceDashboard from './components/IntelligenceDashboard';
import ArchitectureModal from './components/ArchitectureModal';

export default function App() {
  const [currentLang, setCurrentLang] = useState('en');
  const [activeTab, setActiveTab] = useState('scan');
  
  // Data States
  const [systemStatus, setSystemStatus] = useState({ gemini_ready: false });
  const [weather, setWeather] = useState(null);
  const [sampleCrops, setSampleCrops] = useState([]);
  const [telemetry, setTelemetry] = useState(null);

  // Crop Scan & Analysis State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [scanStep, setScanStep] = useState(0);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisError, setAnalysisError] = useState(null);

  // Verify Again State
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);

  // Chat / Agronomist Context
  const [cropContext, setCropContext] = useState('');
  const [conditionContext, setConditionContext] = useState('');

  // Modals
  const [isArchModalOpen, setIsArchModalOpen] = useState(false);

  // Active translation dictionary
  const t = translations[currentLang] || translations.en;

  // Initial Load: Health, Weather, Samples, Dashboard
  useEffect(() => {
    async function initApp() {
      try {
        const [healthRes, weatherRes, samplesRes, dashRes] = await Promise.all([
          checkSystemHealth(),
          fetchLiveWeather(),
          fetchSampleCrops(),
          fetchDashboardTelemetry()
        ]);
        setSystemStatus(healthRes);
        setWeather(weatherRes);
        setSampleCrops(samplesRes);
        setTelemetry(dashRes);
      } catch (err) {
        console.warn('Initialization notice:', err);
      }
    }
    initApp();
  }, []);

  // Handler: Analyze Crop Image
  const handleAnalyzeCrop = async (fileOrBlob, hint = '') => {
    setIsAnalyzing(true);
    setScanStep(1);
    setAnalysisError(null);
    setAnalysisResult(null);

    // Progressive step simulation tied to real analysis
    const stepInterval = setInterval(() => {
      setScanStep((prev) => (prev < 4 ? prev + 1 : prev));
    }, 450);

    try {
      const result = await analyzeCropImage(fileOrBlob, currentLang, hint);
      clearInterval(stepInterval);
      setScanStep(5);
      
      // Attach preview image object URL if not already present
      const previewUrl = typeof fileOrBlob === 'string' ? fileOrBlob : URL.createObjectURL(fileOrBlob);
      result.imagePreview = previewUrl;

      setTimeout(() => {
        setAnalysisResult(result);
        setIsAnalyzing(false);
        setCropContext(result.crop);
        setConditionContext(result.condition);
      }, 500);

    } catch (err) {
      clearInterval(stepInterval);
      setIsAnalyzing(false);
      setAnalysisError(err.message || 'Analysis encountered an error. Please try again.');
    }
  };

  // Handler: Navigate to Verify Again
  const handleGoToVerifyAgain = (baseline) => {
    setAnalysisResult(baseline);
    setActiveTab('verify');
    // Pre-calculate initial verification
    handleRunVerification(
      null, 
      baseline?.condition || 'Chilli Leaf Curl Virus', 
      baseline?.risk_level || 'HIGH', 
      5
    );
  };

  // Handler: Execute Verify Again Comparison
  const handleRunVerification = async (followupFile, prevCondition, prevRisk, daysElapsed) => {
    setIsVerifying(true);
    try {
      // If followupFile is null, fetch the default recovered sample
      let fileToSend = followupFile;
      if (!fileToSend) {
        const res = await fetch('/samples/chilli_recovered.jpg');
        const blob = await res.blob();
        fileToSend = new File([blob], 'chilli_recovered.jpg', { type: 'image/jpeg' });
      }

      const res = await verifyCropRecovery(fileToSend, prevCondition, prevRisk, daysElapsed, currentLang);
      setVerificationResult(res);
    } catch (err) {
      console.error('Verification error:', err);
    } finally {
      setIsVerifying(false);
    }
  };

  // Handler: Go to Agronomist Chat
  const handleGoToAgronomist = (crop, condition) => {
    setCropContext(crop);
    setConditionContext(condition);
    setActiveTab('voice');
  };

  // Handler: Reset to Scanner View
  const handleScanAnother = () => {
    setAnalysisResult(null);
    setActiveTab('scan');
  };

  return (
    <div className="kisanvue-app">
      {/* Header Bar */}
      <Header 
        currentLang={currentLang}
        onLangChange={setCurrentLang}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        systemStatus={systemStatus}
        onOpenArchitecture={() => setIsArchModalOpen(true)}
        t={t}
      />

      <main className="main-content">
        <div className="app-container">
          {/* Micro-Climate Weather Context Bar */}
          <WeatherBanner weather={weather} />

          {/* Tab 1: Crop Scanner & Diagnosis */}
          {activeTab === 'scan' && (
            <>
              {!analysisResult ? (
                <CropScanner 
                  onAnalyze={handleAnalyzeCrop}
                  isAnalyzing={isAnalyzing}
                  scanStep={scanStep}
                  error={analysisError}
                  sampleCrops={sampleCrops}
                  currentLang={currentLang}
                  t={t}
                />
              ) : (
                <AnalysisResult 
                  result={analysisResult}
                  currentLang={currentLang}
                  onVerifyAgain={handleGoToVerifyAgain}
                  onAskAgronomist={handleGoToAgronomist}
                  onScanAnother={handleScanAnother}
                  t={t}
                />
              )}
            </>
          )}

          {/* Tab 2: Verify Again Workflow */}
          {activeTab === 'verify' && (
            <VerifyAgain 
              initialAnalysis={analysisResult}
              currentLang={currentLang}
              onRunVerification={handleRunVerification}
              isVerifying={isVerifying}
              verificationResult={verificationResult}
              sampleCrops={sampleCrops}
              t={t}
            />
          )}

          {/* Tab 3: Conversational Voice Agronomist */}
          {activeTab === 'voice' && (
            <VoiceAgronomist 
              currentLang={currentLang}
              onAskAgronomist={askAgronomist}
              cropContext={cropContext}
              conditionContext={conditionContext}
              t={t}
            />
          )}

          {/* Tab 4: Regional Agricultural Intelligence Dashboard */}
          {activeTab === 'dashboard' && (
            <IntelligenceDashboard 
              telemetry={telemetry}
              t={t}
            />
          )}
        </div>
      </main>

      {/* Safety & Attribution Footer */}
      <Footer t={t} />

      {/* India-Scale Architecture Modal */}
      <ArchitectureModal 
        isOpen={isArchModalOpen} 
        onClose={() => setIsArchModalOpen(false)} 
      />
    </div>
  );
}
