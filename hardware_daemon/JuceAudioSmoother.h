// Phase 15, Risk 2: DSP Zipper Noise & Snapshot Popping Elimination
// File: JuceAudioSmoother.h
// This middleware prevents digital "popping" and "zipper" noises when
// loading a new AI preset (switching floats from 0.0 to 10.0 in 0.8ms).

#pragma once
#include <JuceHeader.h>

class JuceAudioSmoother {
public:
  JuceAudioSmoother() {
    // Default smoothing time of 20 milliseconds to avoid audible zipper noise
    // while remaining imperceptible to the performing guitarist.
    setSmoothingTimeMs(20.0);
  }

  void prepareToPlay(double sampleRate) {
    currentSampleRate = sampleRate;
    smoothedGain.reset(currentSampleRate, smoothingTimeMs / 1000.0);
    smoothedDelayTime.reset(currentSampleRate, smoothingTimeMs / 1000.0);
  }

  void setSmoothingTimeMs(double newTimeMs) {
    smoothingTimeMs = newTimeMs;
    if (currentSampleRate > 0) {
      smoothedGain.reset(currentSampleRate, smoothingTimeMs / 1000.0);
      smoothedDelayTime.reset(currentSampleRate, smoothingTimeMs / 1000.0);
    }
  }

  // Called instantly when an OSC message (Preset Change) is received
  void setTargetGain(float newGainDb) {
    smoothedGain.setTargetValue(newGainDb);
  }

  void setTargetDelayTime(float newDelayMs) {
    smoothedDelayTime.setTargetValue(newDelayMs);
  }

  // Called precisely per-sample inside the AudioProcessor::processBlock
  float getNextSmoothedGain() { return smoothedGain.getNextValue(); }

  float getNextSmoothedDelay() { return smoothedDelayTime.getNextValue(); }

private:
  double currentSampleRate = 44100.0;
  double smoothingTimeMs = 20.0;

  // JUCE provides built-in linear & exponential value smoothers
  juce::SmoothedValue<float, juce::ValueSmoothingTypes::Linear> smoothedGain;

  // Delay time is often smoothed exponentially to recreate the analog "tape
  // pitch warp" feel when switching presets, rather than a jarring digital
  // jump.
  juce::SmoothedValue<float, juce::ValueSmoothingTypes::Multiplicative>
      smoothedDelayTime;
};

/*
// --- USAGE EXAMPLE IN JUCE PROCESSBLOCK ---
void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&
midiMessages) override
{
    // Iterate through every single audio sample (e.g. 512 times per block)
    for (int channel = 0; channel < totalNumInputChannels; ++channel)
    {
        auto* channelData = buffer.getWritePointer (channel);

        for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
        {
            // Instead of jumping instantly to the new preset parameter, we
glide: float currentSmoothGain = smoother.getNextSmoothedGain();

            // Apply smoothed DSP
            channelData[sample] = channelData[sample] *
juce::Decibels::decibelsToGain(currentSmoothGain);
        }
    }
}
*/
