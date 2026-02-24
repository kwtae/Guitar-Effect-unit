import time
import requests
import json
from pythonosc import udp_client

# Laptop Keyboard Emulator for Raspberry Pi GPIO Hardware Daemon
# To use this on Windows/Mac, you might need: pip install keyboard
try:
    import keyboard
except ImportError:
    print("⚠️ Please run: pip install keyboard (Needs Administrator/Sudo privileges)")
    exit(1)

# --- Configuration (Same as actual daemon) ---
FASTAPI_URL = "http://localhost:8000"
OSC_IP = "127.0.0.1" 
OSC_PORT = 9000

print("🚀 Starting Laptop Hardware Emulator (GPIO Simulation)")
print("🔌 Connecting to OSC DSP Engine at {}:{}".format(OSC_IP, OSC_PORT))
osc_client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

# --- State Variables ---
is_bypassed = False
preset_active = True
active_preset_id = 1 

# Simulated Knobs
current_values = {
    "level": 0.5,
    "tone": 0.5,
    "gain": 0.5
}

# --- Event Handlers (Mirroring the physical ones) ---
def handle_encoder_turn(parameter_name, delta_direction):
    """Simulates a physical rotary knob click"""
    global current_values, preset_active
    
    # Update local state +/- 5%
    delta = 0.05 * delta_direction 
    current_values[parameter_name] = max(0.0, min(1.0, current_values[parameter_name] + delta))
    new_val = current_values[parameter_name]
    
    # 1. Fire OSC to local JUCE Engine (Real-time Audio Change)
    osc_address = f"/pedal/drive/{parameter_name}"
    osc_client.send_message(osc_address, new_val)
    
    print(f"🎛️ [Simulated Knob] {parameter_name.upper()} turned! New Value: {new_val:.2f} (OSC Fired)")

    # 2. RLHF: Log manual intervention to FastAPI
    if preset_active:
        print("📝 Logging manual correction (RLHF Feedback) to FastAPI...")
        try:
            requests.post(f"{FASTAPI_URL}/rlhf-feedback/", json={
                "preset_id": active_preset_id,
                "parameter_name": parameter_name,
                "user_adjusted_value": new_val,
                "original_ai_value": new_val - delta 
            })
        except Exception as e:
            print("⚠️ FastAPI backend offline. Run `docker-compose up` or `uvicorn main:app`")

def on_footswitch_pressed():
    """Simulates stomping on the heavy metal 3PDT Switch"""
    global is_bypassed
    is_bypassed = not is_bypassed
    
    if is_bypassed:
        print("\n🦶 [Simulated Stomp] Pedal BYPASSED (Clean Signal)")
        # OSC command to bypass DSP
        osc_client.send_message("/pedal/bypass", 1.0)
    else:
        print("\n🦶 [Simulated Stomp] Pedal ENGAGED (AI Tone Active)")
        osc_client.send_message("/pedal/bypass", 0.0)

# --- Keyboard Bindings (The Emulation Magic) ---
print("\n--- ⌨️ Keyboard Controls ---")
print("[Spacebar] : Stomp Footswitch (Bypass/Engage)")
print("[ Up  Arrow ] : Gain Knob CLOCKWISE (+)")
print("[Down Arrow ] : Gain Knob COUNTER-CLOCKWISE (-)")
print("[Right Arrow] : Tone Knob CLOCKWISE (+)")
print("[Left  Arrow] : Tone Knob COUNTER-CLOCKWISE (-)")
print("[   W   ]     : Level Knob CLOCKWISE (+)")
print("[   S   ]     : Level Knob COUNTER-CLOCKWISE (-)")
print("[   Q   ]     : Quit Emulator")
print("----------------------------\n")

keyboard.on_release_key('space', lambda e: on_footswitch_pressed())

keyboard.on_release_key('up', lambda e: handle_encoder_turn('gain', 1))
keyboard.on_release_key('down', lambda e: handle_encoder_turn('gain', -1))

keyboard.on_release_key('right', lambda e: handle_encoder_turn('tone', 1))
keyboard.on_release_key('left', lambda e: handle_encoder_turn('tone', -1))

keyboard.on_release_key('w', lambda e: handle_encoder_turn('level', 1))
keyboard.on_release_key('s', lambda e: handle_encoder_turn('level', -1))

# Keep daemon running until Q is pressed
keyboard.wait('q')
print("👋 Emulator Shutdown.")
