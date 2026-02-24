import json
from notion_logger import log_to_notion

def generate_llm_prompt_test():
    # 1. System Prompt (Expert Guitar Tech & DSP Engineer Persona)
    system_prompt = """
You are an expert Guitar Tone Designer and DSP Audio Engineer.
Your task is to analyze user requests for guitar tones (written in natural language) 
and (if available) lightweight audio feature data (MFCC, Spectral Centroid) to output 
a precise JSON configuration for a dynamic hardware DSP multi-effects pedal matrix.

AVAILABLE EFFECT MODULES & PARAMETERS:
- drive_module: [gain (0.0-1.0), tone (0.0-1.0), level (0.0-1.0), clipping_type (symmetrical, asymmetrical, led, silicon, germanium, fet), bias_mv (-1000 to +1000), slew_rate_v_us (1.0-20.0)]
- eq_module: [bass, mid, treble, mid_freq_hz]
- delay_module: [time_ms (20-2000), feedback (0.0-1.0), mix (0.0-1.0)]
- reverb_module: [decay_s, mix, type (spring, plate, hall)]

RULES:
1. "Amp-like and greasy" usually means FET or asymmetrical clipping, higher bias, slower slew rate (sag), and enhanced low-mids.
2. "Tight metal" means silicon symmetrical clipping, fast slew rate, mid scoop, bass cut before drive.
3. Determine the optimal 'routing_chain' (e.g., ["eq_module", "drive_module", "reverb_module"] vs ["drive_module", "eq_module"]).
4. Output ONLY valid JSON matching the system requirements. No conversational text.
"""

    # 2. User Input
    user_request = "I have a RAT distortion pedal tone right now, but I want it to sound more amp-like and greasy."
    audio_features_payload = {
        "mfcc_vector_20_dims": [-431.01, 24.64, 0.06, -4.86, -6.99],
        "spectral_centroid": 995.81
    }

    # 3. Simulated LLM Output Engine (This represents the JSON returned by Gemini API)
    # Based on the rules, we craft the exact JSON we expect the LLM to generate.
    simulated_llm_response = {
        "analysis_reasoning": "User requested 'amp-like and greasy' from a RAT baseline. Switching to asymmetrical FET clipping creates tube-like harmonics. Increasing bias adds warmth. Routing EQ before the drive allows us to push low-mids into the clipping stage to make it 'greasy', while slowing the slew rate simulates tube sag.",
        "routing_chain": ["eq_module", "drive_module"],
        "dsp_parameters": {
            "eq_module": {
                "bass": 0.65,
                "mid": 0.70,
                "mid_freq_hz": 400.0,
                "treble": 0.50
            },
            "drive_module": {
                "gain": 0.55,
                "tone": 0.45,
                "level": 0.60,
                "clipping_type": "asymmetrical_fet",
                "bias_mv": 120,
                "slew_rate_v_us": 2.5
            }
        }
    }

    # 4. Format everything beautifully for the Notion Log
    log_title = "🧠 LLM Prompt Engineering & Parameter Mapping Test"
    
    log_body = f"""### 1. System Prompt (The AI's Brain)
{system_prompt.strip()}

### 2. User Input (Context)
- **Natural Language:** "{user_request}"
- **Audio Features (MFCC):** Centroid = {audio_features_payload['spectral_centroid']}

### 3. Generated DSP Matrix JSON (Simulated LLM Output)
{json.dumps(simulated_llm_response, indent=4)}
"""

    print("Sending Prompt Test Log to Notion...")
    print(log_body)
    
    # Save to Notion!
    log_to_notion(log_title, log_body, "markdown")

if __name__ == "__main__":
    generate_llm_prompt_test()
