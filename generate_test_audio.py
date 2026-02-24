import numpy as np
import soundfile as sf
import os

def generate_test_tone(filename="test_tone.wav", duration=3.0, sr=22050):
    print("Generating simulated guitar tone...")
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    
    # Fundamental frequency (e.g. A4 = 440Hz)
    signal = 0.5 * np.sin(2 * np.pi * 440 * t) * np.exp(-3 * t)
    
    # Adding harmonics to simulate string richness
    signal += 0.25 * np.sin(2 * np.pi * 880 * t) * np.exp(-4 * t)
    signal += 0.125 * np.sin(2 * np.pi * 1320 * t) * np.exp(-5 * t)
    signal += 0.05 * np.sin(2 * np.pi * 1760 * t) * np.exp(-6 * t)
    
    # Adding slight non-linear distortion (soft clipping) to simulate a bit of drive
    signal = np.tanh(signal * 2.0)
    
    # Normalizing
    signal = signal / np.max(np.abs(signal))
    
    # Save as 16-bit PCM wav
    sf.write(filename, signal, sr, subtype='PCM_16')
    print(f"Generated {filename} ({os.path.getsize(filename)} Bytes or {os.path.getsize(filename)/1024:.2f} KB)")
    
if __name__ == "__main__":
    generate_test_tone()
