import json
from pydantic import BaseModel, Field, ValidationError

# Phase 14, Risk 3: LLM JSON Hallucinations in the DSP
# To prevent the Gemini API from generating rogue float values (e.g., gain=999.0) 
# that could crash the JUCE C++ engine or blow out P.A. speakers, we enforce 
# Strict Schema Validation using Pydantic. The Python Backend will drop any 
# LLM response that violates the physical bounds of the analog circuit model.

class DspParameters(BaseModel):
    """
    Strict blueprint representing the physical limitations of the pedal's DSP engine.
    The LLM MUST conform to these boundaries.
    """
    preset_name: str = Field(..., max_length=50, description="Short name of the tone")
    drive: float = Field(..., ge=0.0, le=10.0, description="Overdrive gain amount (0 to 10)")
    level: float = Field(..., ge=0.0, le=10.0, description="Master output volume (0 to 10)")
    tone: float = Field(..., ge=0.0, le=10.0, description="Tone knob filtering (0 to 10)")
    delay_ms: float = Field(0.0, ge=0.0, le=2000.0, description="Delay time in milliseconds")
    
def validate_llm_response(raw_llm_json_string):
    """
    Takes the messy, potentially hallucinatory text from Gemini and sanitizes it.
    """
    print(f"📥 [LLM Response Received]: {raw_llm_json_string}")
    
    try:
        # Step 1: Prove it's even valid JSON
        parsed_dict = json.loads(raw_llm_json_string)
        
        # Step 2: Push it through the Pydantic physical bounds checker
        safe_params = DspParameters(**parsed_dict)
        
        print("✅ [Validation Passed] AI parameters are strictly within hardware safety limits.")
        print(f"🚀 [Ready for OSC Transmission]: {safe_params.json()}")
        return safe_params.dict()
        
    except json.JSONDecodeError:
        print("❌ [CRITICAL ERROR] LLM failed to return valid JSON format (Hallucination). Dropping payload.")
        return get_failsafe_payload()
        
    except ValidationError as e:
        print("❌ [SAFETY TRIGGERED] LLM hallucinated out-of-bounds float values that violate analog constraints!")
        print(f"   Details: {e}")
        return get_failsafe_payload()

def get_failsafe_payload():
    """If the LLM goes rogue, we default to a safe, quiet analog bypass setting."""
    print("🛡️ [Failsafe Active] Injecting default safe parameters to DSP.")
    return {
        "preset_name": "Failsafe Bypass",
        "drive": 0.0,
        "level": 5.0,
        "tone": 5.0,
        "delay_ms": 0.0
    }

if __name__ == "__main__":
    print("--- 🛡️ Phase 14: LLM Pydantic Anti-Hallucination Test ---")
    
    # Scenario A: Good LLM Array
    good_llm = '{"preset_name": "Vintage Fuzz", "drive": 7.5, "level": 6.0, "tone": 4.2, "delay_ms": 350.0}'
    validate_llm_response(good_llm)
    
    print("\n---")
    
    # Scenario B: Rogue LLM Hallucinated Gain = 999.0 (Speaker Killer)
    rogue_llm = '{"preset_name": "DEATH METAL", "drive": 999.0, "level": 11.5, "tone": 10.0, "delay_ms": -50.0}'
    validate_llm_response(rogue_llm)
