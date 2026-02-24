import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [activePreset, setActivePreset] = useState(null);
  const [isEngaged, setIsEngaged] = useState(false); // Pedal bypass state

  // Dummy parameters before generating
  const defaultParams = { gain: 0.5, tone: 0.5, level: 0.5 };
  const currentParams = activePreset?.parameters?.drive_module || defaultParams;

  // Convert 0.0-1.0 to -135deg to +135deg rotation
  const valToRotation = (val) => {
    const minDeg = -135;
    const maxDeg = 135;
    const mapped = minDeg + (val * (maxDeg - minDeg));
    return mapped;
  };

  const generateTone = async () => {
    if (!prompt) {
      // If no prompt, just toggle bypass like a normal pedal
      setIsEngaged(!isEngaged);
      return;
    }

    setIsEngaged(true); // Turn on when generating
    setIsGenerating(true);

    const payload = {
      user_id: "5addfcbf-0f7d-4ed7-ab4a-375f4f9e04a5",
      preset_name: "AI Override",
      ai_target_prompt: prompt,
      parameters: {
        routing: ["drive_module"],
        drive_module: {
          gain: (Math.random() * 0.8 + 0.1).toFixed(2),
          tone: (Math.random() * 0.7 + 0.2).toFixed(2),
          level: 0.60
        }
      },
      input_features: { "mfcc": [] },
      is_public: true
    };

    try {
      const resp = await axios.post(`${API_BASE}/presets/`, payload);
      setActivePreset(resp.data);
      setPrompt(""); // Clear prompt after generation
    } catch (e) {
      console.error(e);
      // Fallback pseudo-generation for visual effect if backend is offline
      setTimeout(() => {
        setActivePreset({
          parameters: {
            drive_module: {
              gain: (Math.random() * 0.8 + 0.1).toFixed(2),
              tone: (Math.random() * 0.7 + 0.2).toFixed(2),
              level: 0.60
            }
          }
        });
        setPrompt("");
      }, 1500);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleStomp = () => {
    if (prompt) {
      generateTone();
    } else {
      setIsEngaged(!isEngaged);
    }
  };

  // Determine LED state class
  let ledClass = "pedal-led";
  if (isGenerating) ledClass += " thinking";
  else if (isEngaged) ledClass += " active";

  return (
    <div className="pedal-box">

      {/* 1. LED Indicator */}
      <div className={ledClass}></div>

      {/* 2. Branding */}
      <div className="pedal-brand">AI TONE</div>
      <div className="pedal-subtitle">NEURAL OVERDRIVE STM-1</div>

      {/* 3. Physical Knobs */}
      <div className="knobs-container">
        <div className="knob-wrapper">
          <div
            className="knob-potentiometer"
            style={{ transform: `rotate(${valToRotation(currentParams.level)}deg)` }}
          ></div>
          <div className="knob-label">LEVEL</div>
        </div>

        <div className="knob-wrapper" style={{ marginTop: '-15px' }}>
          <div
            className="knob-potentiometer"
            style={{ transform: `rotate(${valToRotation(currentParams.tone)}deg)` }}
          ></div>
          <div className="knob-label">TONE</div>
        </div>

        <div className="knob-wrapper">
          <div
            className="knob-potentiometer"
            style={{ transform: `rotate(${valToRotation(currentParams.gain)}deg)` }}
          ></div>
          <div className="knob-label">DIST</div>
        </div>
      </div>

      {/* 4. AI Prompt Input Area */}
      <div className="ai-prompt-container">
        <textarea
          className="ai-prompt-input"
          placeholder="e.g. Give me a greasy vintage rat tone for a solo..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled={isGenerating}
        />
      </div>

      {/* 5. Metallic Footswitch */}
      <div className="stomp-switch-container">
        <div className="stomp-washer" onClick={handleStomp}>
          <div className="stomp-bolt">
            <button className="stomp-button" disabled={isGenerating}></button>
          </div>
        </div>
        <div className="stomp-label">
          {isGenerating ? "ANALYZING..." : "BYPASS / GENERATE"}
        </div>
      </div>

    </div>
  );
}

export default App;
