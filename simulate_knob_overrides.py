import urllib.request
import json
import uuid

def simulate_app_overrides():
    url = "http://127.0.0.1:8000/rlhf-feedback/"

    # We use the preset_id that we just generated from test_api.py
    # We must ensure this preset exists in the database for the join to work
    target_preset_id = "e54fb2de-0ac9-4148-a8e1-e2ca35ac864a"
    
    # AI originally suggested gain: 0.85
    fake_override_1 = {
        "user_id": str(uuid.uuid4()),
        "preset_id": target_preset_id, 
        "rating": 2,
        "adjusted_parameters": {
            "drive_module": {"gain": 0.95, "tone": 0.3}
        }
    }

    fake_override_2 = {
        "user_id": str(uuid.uuid4()),
        "preset_id": target_preset_id,
        "rating": 3,
        "adjusted_parameters": {
            "drive_module": {"gain": 1.0, "tone": 0.4}
        }
    }

    headers = {"Content-Type": "application/json"}
    
    for payload in [fake_override_1, fake_override_2]:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                print("✅ RLHF Feedback Ingested to Database")
        except urllib.error.HTTPError as e:
            print(f"❌ Failed to reach API: {e.code}")

if __name__ == "__main__":
    simulate_app_overrides()
