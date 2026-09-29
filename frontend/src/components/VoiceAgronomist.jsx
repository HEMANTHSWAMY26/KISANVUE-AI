import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Send, MessageSquare, Sparkles, Volume2, User, Bot, AlertCircle } from 'lucide-react';
import AudioPlayer from './AudioPlayer';

export default function VoiceAgronomist({ 
  currentLang, 
  onAskAgronomist, 
  cropContext, 
  conditionContext,
  t 
}) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: currentLang === 'te' 
        ? 'నమస్కారం రైతు సోదరులారా! నేను మీ కిసాన్‌వ్యూ AI వ్యవసాయ సలహాదారుని. మీ పంట సంరక్షణ, ఎరువులు, పురుగుమందుల గురించి ఏదైనా అడగండి.'
        : currentLang === 'hi'
        ? 'नमस्ते किसान भाई! मैं आपका किसानव्यू AI कृषि सलाहकार हूँ। आप अपनी फसल, खाद, कीटनाशक या रोग के बारे में कुछ भी पूछ सकते हैं।'
        : 'Welcome! I am your KisanVue AI Digital Agronomist. Ask me any farming questions regarding crop care, pest management, bio-sprays, or irrigation.',
      speechText: currentLang === 'te'
        ? 'నమస్కారం రైతు సోదరులారా! నేను మీ కిసాన్‌వ్యూ AI వ్యవసాయ సలహాదారుని. మీ పంట గురించి ఏదైనా అడగండి.'
        : currentLang === 'hi'
        ? 'नमस्ते किसान भाई! मैं आपका किसानव्यू AI कृषि सलाहकार हूँ। पूछिए आपकी फसल में क्या समस्या है।'
        : 'Welcome! I am your KisanVue AI Digital Agronomist. How can I assist your farm today?'
    }
  ]);
  const [inputQuestion, setInputQuestion] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(true);
  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Suggested questions based on language
  const suggestedQueries = {
    te: [
      'మిరప ఆకు ముడుతకు ఏ వేప నూనె వాడాలి?',
      'ఎకరాకు ఎన్ని పసుపు జిగురు అట్టలు పెట్టాలి?',
      'టమోటా మచ్చ తెగులుకు కాపర్ మందు ఎప్పుడు కొట్టాలి?'
    ],
    hi: [
      'मिर्च में लीफ कर्ल वायरस के लिए कौन सा नीम तेल डालें?',
      'प्रति एकड़ कितने पीले स्टिकी कार्ड लगाने चाहिए?',
      'टमाटर में अगेती झुलसा के लिए कॉपर का छिड़काव कब करें?'
    ],
    en: [
      'What bio-spray controls whiteflies in chilli?',
      'How many yellow sticky traps per acre are recommended?',
      'When should copper fungicide be applied for tomato blight?'
    ]
  };

  const queries = suggestedQueries[currentLang] || suggestedQueries.en;

  // Initialize Speech Recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      recognition.onerror = (e) => {
        console.warn('Speech recognition notice:', e.error);
        setIsListening(false);
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          setInputQuestion(transcript);
          handleSendQuery(transcript);
        }
      };

      recognitionRef.current = recognition;
    } else {
      setSpeechSupported(false);
    }
  }, [currentLang]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const toggleListen = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser. Please type your query below.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
    } else {
      // Map language code for Speech Recognition
      const langMap = { te: 'te-IN', hi: 'hi-IN', en: 'en-US' };
      recognitionRef.current.lang = langMap[currentLang] || 'en-US';
      try {
        recognitionRef.current.start();
      } catch (err) {
        console.warn('Recognition start retry:', err);
      }
    }
  };

  const handleSendQuery = async (queryText) => {
    const textToSend = (queryText || inputQuestion).trim();
    if (!textToSend || isLoading) return;

    // Append user message
    const userMsg = { id: Date.now(), sender: 'user', text: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    setInputQuestion('');
    setIsLoading(true);

    try {
      const res = await onAskAgronomist(textToSend, currentLang, cropContext, conditionContext);
      const botMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        text: res.response,
        speechText: res.speech_text || res.response
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errorMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        text: 'Could not connect to agronomist service. Please check network connection.',
        speechText: ''
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="voice-agronomist-view glass-card animate-fade-in">
      {/* Header */}
      <div className="voice-header text-center">
        <div className="badge badge-low mb-2">
          <Sparkles size={14} />
          <span>CONVERSATIONAL GEMINI AGRO-EXTENSION</span>
        </div>
        <h2 className="voice-title">{t.voiceTitle}</h2>
        <p className="voice-subtitle">{t.voiceSubtitle}</p>
      </div>

      {/* Suggested Quick Question Chips */}
      <div className="suggested-queries-bar">
        <span className="suggested-title">{t.suggestedQuestionsTitle}</span>
        <div className="suggested-chips">
          {queries.map((q, idx) => (
            <button 
              key={idx} 
              type="button" 
              className="btn-query-chip"
              onClick={() => handleSendQuery(q)}
            >
              "{q}"
            </button>
          ))}
        </div>
      </div>

      {/* Messages Thread */}
      <div className="chat-thread-container">
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message-row ${msg.sender === 'user' ? 'from-user' : 'from-bot'}`}>
            <div className="message-avatar">
              {msg.sender === 'user' ? <User size={18} /> : <Bot size={18} className="text-emerald" />}
            </div>
            <div className="message-bubble glass-card">
              <p className="message-text">{msg.text}</p>
              {msg.speechText && (
                <div className="message-audio-row">
                  <AudioPlayer 
                    text={msg.speechText} 
                    language={currentLang} 
                    label="Speak"
                    t={t} 
                  />
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="chat-message-row from-bot">
            <div className="message-avatar">
              <Bot size={18} className="text-emerald" />
            </div>
            <div className="message-bubble glass-card typing-bubble">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Voice & Input Controls */}
      <div className="chat-input-bar">
        <button
          type="button"
          className={`btn btn-voice btn-mic ${isListening ? 'listening animate-pulse-glow' : ''}`}
          onClick={toggleListen}
          title={isListening ? 'Listening...' : t.tapToSpeak}
        >
          {isListening ? <MicOff size={22} /> : <Mic size={22} />}
          <span className="hide-on-mobile">{isListening ? t.listening : t.btnSpeak}</span>
        </button>

        <input 
          type="text" 
          value={inputQuestion}
          onChange={(e) => setInputQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSendQuery()}
          placeholder={t.typePlaceholder}
          className="chat-text-input"
        />

        <button 
          type="button" 
          className="btn btn-primary btn-icon-only"
          onClick={() => handleSendQuery()}
          disabled={!inputQuestion.trim() || isLoading}
          title="Send query"
        >
          <Send size={18} />
        </button>
      </div>

      {!speechSupported && (
        <div className="speech-support-notice">
          <AlertCircle size={14} />
          <span>{t.speechNotSupported}</span>
        </div>
      )}
    </div>
  );
}
