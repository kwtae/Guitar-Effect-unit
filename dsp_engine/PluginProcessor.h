#pragma once

#include <JuceHeader.h>
#include <string>
#include <vector>

// ==============================================================================
// 1. Abstract Base Class for all dynamic Effect Nodes (Drive, EQ, Delay, etc.)
// ==============================================================================
class EffectNode {
public:
  virtual ~EffectNode() = default;

  // Process audio buffer in real-time (0 latency)
  virtual void process(juce::AudioBuffer<float> &buffer) = 0;

  // Update internal DSP variables based on incoming JSON-like parameter map
  virtual void updateParameters(const juce::var &nodeParams) = 0;

  virtual juce::String getName() const = 0;
};

// ==============================================================================
// 2. Concrete Implementation: Drive (Distortion) Module
// ==============================================================================
class DriveModule : public EffectNode {
public:
  DriveModule() {
    gain = 1.0f;
    tone = 1.0f;
    level = 1.0f;
    isAsymmetrical = false;
    bias = 0.0f;
  }

  void process(juce::AudioBuffer<float> &buffer) override;
  void updateParameters(const juce::var &nodeParams) override;
  juce::String getName() const override { return "drive_module"; }

private:
  float gain, tone, level, bias;
  bool isAsymmetrical;
  // Internal state variables for IIR filters, etc. would go here
};

// ==============================================================================
// 3. Concrete Implementation: EQ Module
// ==============================================================================
class EQModule : public EffectNode {
public:
  EQModule() {
    bass = 1.0f;
    mid = 1.0f;
    treble = 1.0f;
  }

  void process(juce::AudioBuffer<float> &buffer) override;
  void updateParameters(const juce::var &nodeParams) override;
  juce::String getName() const override { return "eq_module"; }

private:
  float bass, mid, treble;
  // Biquad filter coefficients would go here
};

// ==============================================================================
// 4. Main Processor (Handles OSC and Dynamic Routing)
// ==============================================================================
class AIPedalAudioProcessor : public juce::AudioProcessor,
                              private juce::OSCReceiver,
                              private juce::OSCReceiver::Listener<
                                  juce::OSCReceiver::MessageLoopCallback> {
public:
  AIPedalAudioProcessor();
  ~AIPedalAudioProcessor() override;

  void prepareToPlay(double sampleRate, int samplesPerBlock) override;
  void releaseResources() override;
  void processBlock(juce::AudioBuffer<float> &, juce::MidiBuffer &) override;

  // ... Standard JUCE overrides omitted for brevity ...
  // (createEditor, hasEditor, getStateInformation, etc.)
  void setCurrentProgram(int index) override {}
  const juce::String getProgramName(int index) override { return {}; }
  void changeProgramName(int index, const juce::String &newName) override {}

  // ==========================================================================
  // Core AI Integration: Parses the JSON string received from the Mobile App
  // and dynamically reconfigures the DSP routing chain and parameters in
  // real-time.
  // ==========================================================================
  void applyAIPreset(const juce::String &jsonString);

private:
  void oscMessageReceived(const juce::OSCMessage &message) override;

  // A vector holding pointers to the base class, allowing mixed modules
  std::vector<std::unique_ptr<EffectNode>> routingChain;

  // OSC network listener
  juce::OSCReceiver oscReceiver;

  // Lock to prevent swapping the chain while processing audio
  juce::CriticalSection processLock;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(AIPedalAudioProcessor)
};
