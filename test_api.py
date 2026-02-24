import urllib.request
import json
import uuid

# Define the url
url = "http://127.0.0.1:8000/presets/"

# Simulated app features extracted payload
mock_app_data = {
    "user_id": str(uuid.uuid4()),
    "preset_name": "Greasy Rat Overdrive",
    "ai_target_prompt": "I want a RAT pedal that sounds more amp-like and greasy",
    "parameters": {
        "routing": "EQ_THEN_DRIVE",
        "drive_gain": 0.85,
        "eq_high": 0.3,
        "clipping_asymmetry": 0.6,
        "diode_material": "FET"
    },
    "input_features": {
        "mfcc_vector_20_dims": [-431.01, 24.64, 0.06, -4.86, -6.99],
        "spectral_centroid": 995.81
    },
    "is_public": True
}

# Encode data
data = json.dumps(mock_app_data).encode("utf-8")
headers = {"Content-Type": "application/json"}

# Send Request
req = urllib.request.Request(url, data=data, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        print("✅ Backend API Test Successful!")
        print("Received Preset from DB:")
        print(json.dumps(res, indent=4))
except urllib.error.HTTPError as e:
    print(f"❌ Failed to reach API: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"❌ Error: {e}")
