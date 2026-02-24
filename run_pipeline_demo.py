import os
import numpy as np
import scipy.io.wavfile as wav
import shutil
import json
import multiprocessing

def main():
    # 1. Create Mock Dataset Directory
    DATASET_DIR = "mock_dataset"
    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)
    os.makedirs(DATASET_DIR)

    # 2. Generate 5 distinct mock audio files (1 second each)
    sample_rate = 22050
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    bass_wave = 0.5 * np.sin(2 * np.pi * 100 * t) 
    wav.write(os.path.join(DATASET_DIR, "isolated_bass.wav"), sample_rate, bass_wave.astype(np.float32))

    mid_wave = 0.5 * np.sin(2 * np.pi * 800 * t) + 0.2 * np.sin(2 * np.pi * 1600 * t)
    wav.write(os.path.join(DATASET_DIR, "overdrive_riff.wav"), sample_rate, mid_wave.astype(np.float32))

    high_wave = 0.5 * np.sin(2 * np.pi * 3000 * t)
    wav.write(os.path.join(DATASET_DIR, "clean_solo.wav"), sample_rate, high_wave.astype(np.float32))

    fuzz_wave = np.clip(1.5 * np.sin(2 * np.pi * 400 * t), -0.5, 0.5)
    wav.write(os.path.join(DATASET_DIR, "heavy_metal_chug.wav"), sample_rate, fuzz_wave.astype(np.float32))

    target_wave = 0.5 * np.sin(2 * np.pi * 850 * t) + 0.1 * np.sin(2 * np.pi * 1700 * t)
    wav.write(os.path.join(DATASET_DIR, "oasis_isolated_guitar.wav"), sample_rate, target_wave.astype(np.float32))

    print(f"✅ Generated 5 diverse mock `.wav` files inside `{DATASET_DIR}/`")

    # 3. Import and run the actual Bulk Extractor we wrote
    print("\n--- 🚀 Running Phase 3: Bulk MFCC Extractor ---")
    from bulk_audio_extractor import bulk_extract_audio_features
    bulk_extract_audio_features(DATASET_DIR, "mock_mfcc_db.json")

    # 4. Import and run Vector DB Ingestion
    print("\n--- 🚀 Running Phase 3: Vector DB Initialization & Ingestion ---")
    from vector_db_manager import VectorDBManager
    db = VectorDBManager(db_path="./test_chroma_db")

    try:
        db.client.delete_collection("guitar_tone_fingerprints")
        db = VectorDBManager(db_path="./test_chroma_db")
    except Exception:
        pass

    db.ingest_from_bulk_json("mock_mfcc_db.json")

    # 5. Simulate Phase 4: Demucs separated stem search
    print("\n--- 🎧 Running Phase 4: Target Search (Reverse-Engineering) ---")
    with open("mock_mfcc_db.json", "r") as f:
        mfcc_data = json.load(f)
        target_vector = next(item for item in mfcc_data if item["source_file"] == "oasis_isolated_guitar.wav")["features"]["mfcc_vector"]

    print(f"🎯 Target Acquired: oasis_isolated_guitar.wav (Vector Shape: {len(target_vector)} dims)")

    db.search_closest_tone(target_vector, n_results=3)

    print("\n🎉 Full Pipeline Test Completed Successfully!")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
