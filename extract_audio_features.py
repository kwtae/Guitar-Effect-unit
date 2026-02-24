import librosa
import numpy as np
import json
import os

def extract_features(audio_path):
    print(f"\n🎧 Loading {audio_path}...")
    original_size = os.path.getsize(audio_path)
    
    # librosa.load reads the file to memory.
    # sr=22050 standardizes the sample rate for all files, mono=True merges L+R
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    
    # 1. Extract MFCC (Mel-Frequency Cepstral Coefficients)
    # Extracts 20 features that describe the overall "shape" or timbre of the sound
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    # We take the mean across the time axis (reducing 2D matrix to 1D vector)
    mfcc_mean = np.mean(mfcc.T, axis=0).tolist()
    
    # 2. Extract Spectral Centroid
    # Represents the "brightness" of the sound, like where the center of mass of the spectrum is.
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    centroid_mean = float(np.mean(centroid))
    
    # 3. Create a lightweight payload (This is what gets sent over the network)
    payload = {
        "status": "success",
        "file_analyzed": audio_path,
        "features": {
            "mfcc_vector_20_dims": [round(x, 4) for x in mfcc_mean],
            "spectral_centroid": round(centroid_mean, 2),
            "duration_sec": round(float(librosa.get_duration(y=y, sr=sr)), 2)
        }
    }
    
    json_str = json.dumps(payload, indent=4)
    extracted_size = len(json_str.encode('utf-8'))
    
    print("\n📦 [Extracted 'Sound Fingerprint' Payload]")
    print(json_str)
    
    print("\n📏 [Data Size Comparison]")
    print(f"Original Audio Size : {original_size} Bytes ({original_size/1024:.2f} KB)")
    print(f"Extracted JSON Size : {extracted_size} Bytes")
    print(f"🔥 Compression Ratio: {original_size/extracted_size:.1f}x times lighter!")

if __name__ == '__main__':
    # Make sure to run generate_test_audio.py before this!
    if os.path.exists('test_tone.wav'):
        extract_features('test_tone.wav')
    else:
        print("Please run `python generate_test_audio.py` first to create the audio file.")
