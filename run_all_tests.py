import requests
import json
import uuid

API_BASE = "http://127.0.0.1:8000"

def run_tests():
    print("🚀 Starting Virtual Execution & Bug Fix Tests...")
    
    # 1. Test Preset Creation (Ensuring standardized schema)
    print("\n[1/4] Testing Backend API: Create Preset")
    mock_prompt = "I want a fat RAT overdrive"
    mock_features = {"mfcc_vector_20_dims": [1.0] * 20, "spectral_centroid": 500.0}
    
    # Standardized Schema matching C++ DSP Engine
    mock_parameters = {
        "routing_chain": ["eq_module", "drive_module"],
        "dsp_parameters": {
            "eq_module": {
                "bass": 0.6,
                "mid": 0.8,
                "treble": 0.5
            },
            "drive_module": {
                "gain": 0.85,
                "tone": 0.40,
                "level": 0.60,
                "clipping_type": "asymmetrical_fet"
            }
        }
    }
    
    payload = {
        "user_id": str(uuid.uuid4()),
        "preset_name": "Greasy FAT RAT",
        "ai_target_prompt": mock_prompt,
        "parameters": mock_parameters,
        "input_features": mock_features,
        "is_public": True
    }
    
    try:
        res = requests.post(f"{API_BASE}/presets/", json=payload)
        res.raise_for_status()
        created_preset = res.json()
        preset_id = created_preset["id"]
        print(f"✅ Preset created successfully with ID: {preset_id}")
    except Exception as e:
        print(f"❌ Failed to create preset: {e}")
        return

    # 2. Test RLHF Feedback Creation
    print(f"\n[2/4] Testing RLHF User Override Feedback for Preset {preset_id}")
    
    # User bumps gain from 0.85 to 1.00
    override_payload = {
        "user_id": str(uuid.uuid4()),
        "preset_id": preset_id,
        "rating": 2,
        "adjusted_parameters": {
             "routing_chain": ["eq_module", "drive_module"],
             "dsp_parameters": {
                 "drive_module": {"gain": 1.0, "tone": 0.40, "level": 0.60}
             }
        }
    }
    
    try:
        res = requests.post(f"{API_BASE}/rlhf-feedback/", json=override_payload)
        res.raise_for_status()
        print(f"✅ User Override Logged Successfully!")
    except Exception as e:
        print(f"❌ Failed to log RLHF feedback: {e}")
        return
        
    print("\n[3/4] Testing Audio Extraction Script")
    import subprocess
    try:
        subprocess.run(["python", "extract_audio_features.py"], check=True)
        print("✅ Extractor works without bugs!")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        
    print("\n[4/4] Testing RLHF Training Job Parser (Checking Schema Consistency)")
    try:
        subprocess.run(["python", "-c", "import sys; sys.path.append('.'); from backend.rlhf_training_job import run_rlhf_optimization_job; run_rlhf_optimization_job()"], check=True)
        print("✅ RLHF Nightly Job parses DB without errors!")
    except Exception as e:
        print(f"❌ Job Failed: {e}")

if __name__ == "__main__":
    run_tests()
