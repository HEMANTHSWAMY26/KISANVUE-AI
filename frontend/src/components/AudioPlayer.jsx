import React, { useState, useEffect } from 'react';
import { Volume2, Square } from 'lucide-react';

export default function AudioPlayer({ text, language = 'en', label = 'Listen to Advisory', t }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      setIsSupported(true);
    }
  }, []);

  const handleToggleSpeak = () => {
    if (!isSupported || !text) return;

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    window.speechSynthesis.cancel(); // Stop any pending speech

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Select appropriate language voice
    if (language === 'te') {
      utterance.lang = 'te-IN';
    } else if (language === 'hi') {
      utterance.lang = 'hi-IN';
    } else {
      utterance.lang = 'en-US';
    }

    utterance.rate = 0.95; // Slightly slower for clear farmer comprehension
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsPlaying(true);
    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);

    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  if (!text) return null;

  return (
    <div className="audio-player-widget">
      <button 
        type="button"
        className={`btn ${isPlaying ? 'btn-secondary is-playing' : 'btn-primary'}`}
        onClick={handleToggleSpeak}
        title={isPlaying ? (t?.btnStopAudio || 'Stop') : (label || t?.btnListenAdvisory || 'Listen')}
      >
        {isPlaying ? (
          <>
            <Square size={16} fill="currentColor" />
            <span>{t?.btnStopAudio || 'Stop Voice'}</span>
            <div className="waveform-bars">
              <span className="waveform-bar"></span>
              <span className="waveform-bar"></span>
              <span className="waveform-bar"></span>
              <span className="waveform-bar"></span>
              <span className="waveform-bar"></span>
            </div>
          </>
        ) : (
          <>
            <Volume2 size={18} />
            <span>{label || t?.btnListenAdvisory || 'Listen to Advisory'}</span>
          </>
        )}
      </button>
    </div>
  );
}
