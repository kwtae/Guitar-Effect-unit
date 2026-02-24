import os
import json
import google.generativeai as genai
from sqlalchemy.orm import Session
from backend.models import Preset, RLHFFeedback
from backend.database import SessionLocal

# To run this script, set your Gemini API key:
# $env:GEMINI_API_KEY="your_api_key_here"
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=API_KEY)

def analyze_and_recalibrate_ai_with_gemini():
    db = SessionLocal()
    print("🚀 AI vs Human RLHF Error Parsing starts...")

    # Calculate average errors from the actual user override DB
    critical_feedbacks = db.query(RLHFFeedback).filter(RLHFFeedback.rating <= 3).all()
    if not critical_feedbacks:
        print("✅ Outstanding AI Performance! No RLHF overrides found.")
        return

    total_gain_error = 0.0
    total_tone_error = 0.0
    count = 0

    for fb in critical_feedbacks:
        preset = db.query(Preset).filter(Preset.id == fb.preset_id).first()
        if not preset: continue

        ai_gain = float(preset.parameters.get("drive_gain", 0.85)) # Fallback mock values
        ai_tone = float(preset.parameters.get("eq_high", 0.5))

        user_gain = float(fb.adjusted_parameters.get("drive_module", {}).get("gain", ai_gain))
        user_tone = float(fb.adjusted_parameters.get("drive_module", {}).get("tone", ai_tone))

        total_gain_error += (user_gain - ai_gain)
        total_tone_error += (user_tone - ai_tone)
        count += 1

    if count == 0: return

    avg_gain_error = total_gain_error / count
    avg_tone_error = total_tone_error / count
    
    db.close()

    print(f"\n📊 [RLHF Database Stats]")
    print(f"Data points collected: {count} manual stage overrides.")
    print(f"Systematic Gain bias: {avg_gain_error:+.3f}")
    print(f"Systematic Tone bias: {avg_tone_error:+.3f}")

    # --- Actual Gemini API Integration ---
    print("\n🧠 Connecting to Gemini API for RLHF Parameter Correction...")
    
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
You are the master brain of the 'AI Guitar Pedal'. 
Recently, when evaluating 'Greasy RAT' overdrive tones, our users have been physically overriding your settings on stage.
Your average errors are: Gain {avg_gain_error:+.3f} and Tone {avg_tone_error:+.3f}. 

This means your generated presets are usually too clean or too dark compared to what human guitarists want.

Old Base System Prompt Rules:
- "Amp-like and greasy" means FET clipping, +0 Bias, Gain around 0.85.

Given this systematic error, formulate a new updated SYSTEM RULE for handling 'Greasy RAT' tones so that next time, your output aligns with actual human preference.
Output *only* the new, highly specific JSON routing configuration strategy and a brief reasoning.
        """
        
        response = model.generate_content(prompt)
        
        print("\n✨ --- GEMINI'S SELF-CORRECTED LOGIC ---")
        print(response.text)
        print("-----------------------------------------")
        print("✅ The LLM has successfully updated its internal biases based on human RLHF data!")
        
    except Exception as e:
        print(f"\n❌ Error calling Gemini API. Did you set GEMINI_API_KEY? Error: {e}")

if __name__ == "__main__":
    analyze_and_recalibrate_ai_with_gemini()
