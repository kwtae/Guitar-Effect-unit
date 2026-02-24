import time
import json
import requests
import threading
from gpiozero import Button, RotaryEncoder, PWMLED
from pythonosc.udp_client import SimpleUDPClient

# Configuration & Network Routing
FASTAPI_URL = "http://127.0.0.1:8000"
OSC_CLIENT_IP = "127.0.0.1"
OSC_CLIENT_PORT = 9000  # JUCE DSP Engine listening port

# Setup OSC Client to talk directly to C++
osc_client = SimpleUDPClient(OSC_CLIENT_IP, OSC_CLIENT_PORT)

# --- Hardware GPIO Mapping ---
# 1. Rotary Encoders (Level, Tone, Gain)
enc_level = RotaryEncoder(17, 27, max_steps=100)
enc_tone = RotaryEncoder(22, 23, max_steps=100)
enc_gain = RotaryEncoder(24, 25, max_steps=100)

# 2. 3PDT Footswitch (Bypass / Generate)
footswitch = Button(5, pull_up=True, bounce_time=0.1)

# 3. Status LEDs
led_red = PWMLED(6)   # Active / Engaged
led_blue = PWMLED(13) # AI Processing / Syncing

# Global Active Preset State (Cached locally)
current_params = {
    "level": 0.5,
    "tone": 0.5,
    "gain": 0.5
}
is_bypassed = False

# ==========================================================
# OSC & REST Event Handlers
# ==========================================================

def update_dsp_parameter(param_name, new_val):
    """Fires instantaneous UDP OSC message to the C++ Engine (Zero Latency)"""
    new_val = max(0.0, min(1.0, new_val)) # Clamp to 0~1
    
    # 1. Send to C++ via OSC immediately
    osc_addr = f"/pedal/drive/{param_name}"
    osc_client.send_message(osc_addr, new_val)
    
    # Update local cache
    current_params[param_name] = new_val
    print(f"🎛️ Knob Turned: {param_name} -> {new_val:.2f} (OSC fired)")

    
def sync_rlhf_to_cloud():
    """Debounced function to send manual override data to FastAPI for Nightly RLHF"""
    payload = {
        "preset_id": "current-active-id", # In real implementation, grab from state
        "rating": 3, # Implicitly assume 3 stars if user had to manually adjust
        "adjusted_parameters": {
            "drive_module": current_params
        }
    }
    try:
        requests.post(f"{FASTAPI_URL}/rlhf-feedback/", json=payload, timeout=2)
        print("☁️ Synced manual override delta to Local AI Brain (RLHF).")
    except Exception as e:
        print("Error syncing to API:", e)

# Timer for debouncing REST calls so we don't spam the DB while user is turning the knob fast
rlhf_sync_timer = None

def handle_encoder_turn(param_name, delta):
    global rlhf_sync_timer
    
    new_value = current_params[param_name] + (delta * 0.05)
    update_dsp_parameter(param_name, new_value)
    
    # Reset debounce timer for Cloud Sync
    if rlhf_sync_timer:
        rlhf_sync_timer.cancel()
    rlhf_sync_timer = threading.Timer(1.5, sync_rlhf_to_cloud)
    rlhf_sync_timer.start()

def on_footswitch_pressed():
    global is_bypassed
    is_bypassed = not is_bypassed
    
    if is_bypassed:
        print("🛑 PEDAL BYPASSED")
        osc_client.send_message("/pedal/bypass", 1)
        led_red.value = 0.0
    else:
        print("🔥 PEDAL ENGAGED")
        osc_client.send_message("/pedal/bypass", 0)
        led_red.value = 1.0


# ==========================================================
# Main Execution Loop
# ==========================================================

print("🎸 AI Guitar Pedal Hardware Daemon Booting...")
led_blue.pulse(fade_in_time=0.5, fade_out_time=0.5)

# Bind Hardware Events
enc_level.when_rotated_clockwise = lambda: handle_encoder_turn("level", 1)
enc_level.when_rotated_counter_clockwise = lambda: handle_encoder_turn("level", -1)

enc_tone.when_rotated_clockwise = lambda: handle_encoder_turn("tone", 1)
enc_tone.when_rotated_counter_clockwise = lambda: handle_encoder_turn("tone", -1)

enc_gain.when_rotated_clockwise = lambda: handle_encoder_turn("gain", 1)
enc_gain.when_rotated_counter_clockwise = lambda: handle_encoder_turn("gain", -1)

footswitch.when_pressed = on_footswitch_pressed

time.sleep(2) # Fake boot time
led_blue.value = 0
led_red.value = 1.0 # Default to engaged

print("✅ Daemon Ready & Listening to GPIO Pins.")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nShutting down hardware daemon.")
    led_red.off()
    led_blue.off()
