// Phase 13: DSP Audio Engine Integrity & Ear Protection
// File: OscSafetyValidator.h
// This middleware sits between the Python Backend (via UDP/OSC) and the
// realtime JUCE AudioProcessor thread. It strictly catches LLM hallucinations
// or corrupted float data before it causes a math explosion in the filters or
// gain stages.

#pragma once
#include <JuceHeader.h>
#include <algorithm> // for std::clamp

class OscSafetyValidator {
public:
  // Safe Hard Limits based on physical analog component modeling thresholds
  static constexpr float MAX_GAIN_DB = 24.0f;
  static constexpr float MIN_GAIN_DB = -90.0f;
  static constexpr float MAX_FILTER_Q =
      20.0f; // Above this causes dangerous self-oscillation
  static constexpr float MIN_FILTER_Q = 0.1f;
  static constexpr float MAX_DELAY_TIME_MS = 2000.0f;
  static constexpr float MIN_DELAY_TIME_MS = 0.0f;

  // Struct to hold sanitized output safely
  struct ValidatedParams {
    float gainDb;
    float filterQ;
    float delayMs;
    bool wasCorrupted; // Flag to trigger UI warning if AI hallucinated
  };

  /**
   * @brief Parses and strictly sanitizes incoming floating point data.
   * @return A guaranteed safe `ValidatedParams` object ready for the audio
   * thread.
   */
  static ValidatedParams sanitizeIncomingOsc(float rawGain, float rawQ,
                                             float rawDelay) {
    ValidatedParams safeParams;
    safeParams.wasCorrupted = false;

    // 1. Check for NaNs or Infinities (Critical for DSP math safety)
    if (std::isnan(rawGain) || std::isinf(rawGain)) {
      rawGain = 0.0f; // Reset to safe unity string
      safeParams.wasCorrupted = true;
    }
    if (std::isnan(rawQ) || std::isinf(rawQ)) {
      rawQ = 0.707f; // Reset to standard Butterworth Q
      safeParams.wasCorrupted = true;
    }

    // 2. Strict Mathematical Clamping (Sanitization)
    // If Gemini LLM predicted Gain = 999.0, it will be hard-clamped to
    // MAX_GAIN_DB.
    safeParams.gainDb = std::clamp(rawGain, MIN_GAIN_DB, MAX_GAIN_DB);
    safeParams.filterQ = std::clamp(rawQ, MIN_FILTER_Q, MAX_FILTER_Q);
    safeParams.delayMs =
        std::clamp(rawDelay, MIN_DELAY_TIME_MS, MAX_DELAY_TIME_MS);

    // Flag if any clamping had to occur
    if (safeParams.gainDb != rawGain || safeParams.filterQ != rawQ) {
      safeParams.wasCorrupted = true;
    }

    return safeParams;
  }
};

/*
// --- USAGE EXAMPLE IN JUCE OSC LISTENER ---
void oscMessageReceived(const juce::OSCMessage& message) override
{
    if (message.getAddressPattern().toString() == "/pedal/ai_params")
    {
        float rawGain = message[0].getFloat32();
        float rawQ = message[1].getFloat32();

        // 🔒 The Wall: Sanitizer intercepts BEFORE audio thread touching
        auto safeOutput = OscSafetyValidator::sanitizeIncomingOsc(rawGain, rawQ,
500.0f);

        if (safeOutput.wasCorrupted) {
            // Signal a warning LED on the pedal PCB or send alert to React
Native app hardwareLedManager.setWarning(true);
        }

        // Safely apply to AudioProcessorValueTreeState
        apvts.getParameter("gain")->setValueNotifyingHost(safeOutput.gainDb);
    }
}
*/
