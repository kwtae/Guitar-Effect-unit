from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import Preset, RLHFFeedback
from backend.database import SessionLocal
import json

def run_rlhf_optimization_job():
    """
    Simulates a nightly background job that analyzes all user overrides
    to calculate the "AI Error Delta" and adjust global weights for the LLM prompt.
    """
    db = SessionLocal()
    print("🚀 Starting Daily RLHF Optimization Analysis...")

    # 1. Fetch all feedbacks with rating <= 3 (Where user felt the need to override AI heavily)
    critical_feedbacks = db.query(RLHFFeedback).filter(RLHFFeedback.rating <= 3).all()

    if not critical_feedbacks:
        print("✅ AI is performing perfectly. No critical overrides detected.")
        db.close()
        return

    # A simplistic aggregator for 'drive_gain' errors
    gain_deltas = []

    for fb in critical_feedbacks:
        # Get what the AI originally suggested
        original_preset = db.query(Preset).filter(Preset.id == fb.preset_id).first()
        if not original_preset:
            continue

        try:
            ai_gain = float(original_preset.parameters.get("drive_gain", 0))
            user_gain = float(fb.adjusted_parameters.get("drive_module", {}).get("gain", 0))

            if user_gain > 0 and ai_gain > 0:
                # Calculate Delta
                delta = user_gain - ai_gain 
                gain_deltas.append(delta)
                
                print(f"🔍 Discrepancy Found in '{original_preset.preset_name}' -> AI Gain: {ai_gain:.2f}, User Adjusted to: {user_gain:.2f} (Delta: {delta:+.2f})")

        except Exception as e:
            print(f"Warning: Payload mapping error - {e}")

    # 2. Derive new knowledge (Global weight adjustment with Outlier Removal)
    if not gain_deltas:
        print("✅ No valid gain comparisons found.")
        db.close()
        return

    import numpy as np
    
    # Calculate IQR to remove extreme user outliers (e.g., trolls or noise)
    Q1 = np.percentile(gain_deltas, 25)
    Q3 = np.percentile(gain_deltas, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_deltas = [d for d in gain_deltas if lower_bound <= d <= upper_bound]
    outliers_removed = len(gain_deltas) - len(filtered_deltas)
    
    if filtered_deltas:
        avg_error = sum(filtered_deltas) / len(filtered_deltas)
        print(f"\n📊 --- RLHF SUMMARY ---")
        print(f"Analyzed {len(gain_deltas)} manual overrides (Removed {outliers_removed} outliers).")
        print(f"Robust Average Gain Error Delta: {avg_error:+.3f}")
        
        # In a real model, this 'avg_error' would be injected back into the LLM's system prompt 
        # as a bias weight via EMA (Exponential Moving Average) to prevent sudden jumps
        EMA_ALPHA = 0.2
        print(f"💡 Suggest EMA smooth update strategy: NewBias = OldBias*(1-{EMA_ALPHA}) + {avg_error:.3f}*{EMA_ALPHA}")

        if avg_error > 0.1:
            print("🧠 KNOWLEDGE GAINED: The AI is systematically generating drives that are too clean.")
            print("   -> Action: Increasing global 'Drive Gain Bias' in the LLM System Prompt +15%.")
        elif avg_error < -0.1:
            print("🧠 KNOWLEDGE GAINED: The AI is systematically generating drives that are too distorted.")
            print("   -> Action: Decreasing global 'Drive Gain Bias' in the LLM System Prompt -15%.")
        else:
            print("✅ Error margin within acceptable threshold (+- 10%). No hyperparameter updates needed.")

    db.close()

if __name__ == "__main__":
    run_rlhf_optimization_job()
