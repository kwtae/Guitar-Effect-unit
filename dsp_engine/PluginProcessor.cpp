#include "PluginProcessor.h"
#include <iostream>
#include <juce_osc/juce_osc.h>

// ==============================================================================
// 1. Process Logic: Drive Module (Distortion)
// This applies non-linear amplification (Drive) mimicking analog clipping
// ==============================================================================
void DriveModule::process(juce::AudioBuffer<float>& buffer)
{
    // A simplified example of overdrive clipping (digital soft-clip vs asymmetric).
    float gainFactor = juce::Decibels::decibelsToGain(gain * 40.0f); // 0 to 40dB Drive
    
    for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
    {
        float* channelData = buffer.getWritePointer(channel);
        
        for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
        {
            float inputVar = channelData[sample] * gainFactor;
            
            // Artificial Bias (Tube Warmth Simulation)
            inputVar += bias;

            // Simple clipping logic
            if (isAsymmetrical) {
                // e.g. RAT or BOSS SD-1 clipping topology
                if (inputVar > 1.0f)       inputVar = 1.0f;
                else if (inputVar < -0.5f) inputVar = -0.5f; 
            } else {
                // Soft clipping (Tube Screamer style)
                inputVar = std::tanh(inputVar); 
            }
            
            // Output level mapping
            channelData[sample] = inputVar * level; 
        }
    }
}

void DriveModule::updateParameters(const juce::var& nodeParams)
{
    // Parse JSON directly into floats
    if (nodeParams.hasProperty("gain"))    gain = static_cast<float>(nodeParams["gain"]);
    if (nodeParams.hasProperty("tone"))    tone = static_cast<float>(nodeParams["tone"]);
    if (nodeParams.hasProperty("level"))   level = static_cast<float>(nodeParams["level"]);
    
    if (nodeParams.hasProperty("clipping_type")) {
        juce::String clipType = nodeParams["clipping_type"].toString();
        isAsymmetrical = (clipType.containsIgnoreCase("asymmetrical") || clipType.containsIgnoreCase("fet"));
    }
    
    if (nodeParams.hasProperty("bias_mv")) {
        float biasMv = static_cast<float>(nodeParams["bias_mv"]);
        bias = biasMv / 1000.0f; // mV to Volt normalization (0-1 range)
    }
}

// ==============================================================================
// 2. Process Logic: EQ Module
// ==============================================================================
void EQModule::process(juce::AudioBuffer<float>& buffer)
{
    // In production, this runs optimized JUCE Biquad filters (LowShelf, Peak, HighShelf).
    // Omitted real biquad implementation for concept clarity.
    float masterGainScale = (bass + mid + treble) / 3.0f;
    buffer.applyGain(masterGainScale); 
}

void EQModule::updateParameters(const juce::var& nodeParams)
{
    if (nodeParams.hasProperty("bass"))   bass = static_cast<float>(nodeParams["bass"]);
    if (nodeParams.hasProperty("mid"))    mid = static_cast<float>(nodeParams["mid"]);
    if (nodeParams.hasProperty("treble")) treble = static_cast<float>(nodeParams["treble"]);
}


// ==============================================================================
// 3. Central Router & OSC Receiver (AIPedalAudioProcessor)
// ==============================================================================
AIPedalAudioProcessor::AIPedalAudioProcessor() : 
    AudioProcessor (BusesProperties().withInput("Input",  juce::AudioChannelSet::mono(), true)
                                     .withOutput("Output", juce::AudioChannelSet::mono(), true))
{
    // Initialize OSC Receiver on Port 9000 to listen to FastAPI and Hardware Daemon
    if (!oscReceiver.connect(9000)) {
        std::cerr << "❌ OSC Error: Could not connect to UDP port 9000." << std::endl;
    } else {
        oscReceiver.addListener(this, "/pedal/ai_rebuild_chain");
        oscReceiver.addListener(this, "/pedal/drive/gain");
        oscReceiver.addListener(this, "/pedal/drive/tone");
        oscReceiver.addListener(this, "/pedal/drive/level");
        std::cout << "📡 OSC Receiver listening on port 9000." << std::endl;
    }
}

AIPedalAudioProcessor::~AIPedalAudioProcessor() {}

void AIPedalAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer&)
{
    juce::ScopedNoDenormals noDenormals;

    // Enter lock to prevent the app from rewriting the chain while audio is processing
    const juce::ScopedLock sl (processLock);

    // Dynamic Processing Loop: Apply each effect block in the EXACT order defined by the AI
    for (auto& effect : routingChain)
    {
        effect->process(buffer);
    }
}


// ==============================================================================
// 4. App -> Bluetooth -> JUCE JSON Interpreter
// This function parses the incoming payload from the Mobile App and dynamically
// rebuilds the vector array of effect processors.
// ==============================================================================
void AIPedalAudioProcessor::applyAIPreset(const juce::String& jsonString)
{
    auto parsedResult = juce::JSON::parse(jsonString);
    if (parsedResult.isVoid()) return; // Invalid Payload

    // Safely lock the audio thread so we don't pop/glitch while repopulating the vector
    const juce::ScopedLock sl (processLock);

    routingChain.clear();
    
    auto routingArray = parsedResult["routing_chain"]; // e.g. ["eq_module", "drive_module"]
    auto parametersList = parsedResult["dsp_parameters"];

    // 1. Build the modules in the exact index order specified by the AI routing strategy
    for (int i = 0; i < routingArray.size(); ++i)
    {
        juce::String nodeName = routingArray[i].toString();
        std::unique_ptr<EffectNode> newNode = nullptr;

        if (nodeName == "eq_module")         newNode = std::make_unique<EQModule>();
        else if (nodeName == "drive_module") newNode = std::make_unique<DriveModule>();

        if (newNode != nullptr)
        {
            // 2. Hydrate the module with its specific tuned values
            newNode->updateParameters(parametersList[nodeName]);
            
            // 3. Mount it onto the central audio loop array
            routingChain.push_back(std::move(newNode));
        }
    }
    
    // Once the lock exits, the audio thread instantly starts using the new architecture.
    std::cout << "✅ Swapped to new dynamic DSP routing mapping. " << routingChain.size() << " nodes loaded." << std::endl;
}

// ==============================================================================
// 5. OSC Message Handler (Real-time Knob Turns & AI Injection)
// ==============================================================================
void AIPedalAudioProcessor::oscMessageReceived(const juce::OSCMessage& message)
{
    if (message.getAddressPattern() == "/pedal/ai_rebuild_chain")
    {
        if (message.size() == 1 && message[0].isString()) {
            juce::String jsonPayload = message[0].getString();
            applyAIPreset(jsonPayload);
        }
    }
    // Handle real-time physical knob turns from Raspberry Pi GPIO
    else if (message.getAddressPattern().toString().startsWith("/pedal/drive/"))
    {
        if (message.size() == 1 && message[0].isFloat32()) {
            float newValue = message[0].getFloat32();
            
            // In a real implementation, we'd search the routingChain for the DriveModule instance. 
            // For this phase 2 prototype, we just print the successful network reception.
            std::cout << "🎛️ OSC Real-time Parameter Update Received: " 
                      << message.getAddressPattern().toString() << " -> " << newValue << std::endl;
        }
    }
}
