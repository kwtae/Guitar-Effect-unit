# 🎸 Tier 1: Hardware & Physical UI Interface Design

## 1. Core Hardware Architecture
- **MCU / DSP Board**: Electro-Smith **Daisy Seed** (ARM Cortex-M7 running at 480MHz, 64MB SDRAM, 24-bit 96kHz audio codec). This board natively supports C++ and handles ultra-low real-time latency (< 3ms) effortlessly.
- **Wireless Module**: **ESP32-C3** (Bluetooth Low Energy / Wi-Fi). Acts purely as a message broker between the Mobile App and the Daisy Seed over UART/SPI to inject the JSON parameter payloads.

## 2. Physical User Interface (The Board Layout)
The major pain point of current complex modellers is "menu diving". Even though AI builds the tone, users must have instant, tactile control over the *current* sound on stage.

### The Front Panel Layout
- **1x OLED Display (128x64 I2C):** Located top-center. It simply displays the **Current Preset Name** (e.g., "Greasy RAT Overdrive") and the active routing blocks (`EQ -> DRV -> DLY`).
- **3x Endless Rotary Encoders w/ Push-button:**
  These are context-aware knobs mapping to the most critical parameters of the *current* AI preset.
  - *Example:* If the AI selected a Drive, Knock 1 = Gain, Knob 2 = Tone, Knob 3 = Output Level.
  - If the user presses Knob 1, it toggles from adjusting 'Gain' to navigating an array of presets.
- **LED Ring Indicators (around the Knobs):**
  Since the AI generated the starting value (e.g., Gain at 60%), an analog potentiometer wouldn't match. Endless encoders with LED rings instantly jump to display 60% load. When the user grabs it and turns it to 80%, the LED ring expands, overriding the AI.
- **2x Heavy-Duty Footswitches:**
  - `Left`: Bypass (True Bypass Relay for safety).
  - `Right`: Bank Up / Preset Next.

## 3. The Override System (RLHF Workflow)
When the user overwrites an AI preset on stage by turning physical knob 1 from 60% -> 80%:
1. The ESP32 immediately detects the GPIO encoder increment.
2. The Daisy Seed instantly updates audio processing (0 latency shift).
3. The new Delta (Gain +20%) is buffered to the mobile app over BLE.
4. The mobile app syncs this manual correction to the **PostgreSQL `RLHFFeedback` Table** the next time it has internet, teaching the cloud that "This user prefers 20% more gain for RAT tones."
