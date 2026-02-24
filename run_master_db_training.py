import os
import json
import time

# Phase 12: Master DB Training Orchestrator
# This script bridges all the Extractors (Layer 1, 2) and the Bouncer (Layer 3) 
# to officially populate our local ChromaDB (Vector DB) with actual training data.

from vector_db_manager import VectorDBManager
from bulk_audio_extractor import process_single_file
from layer3_cross_validation_filter import cross_validate_scraped_data

def generate_mock_wav_files(directory):
    """Creates some dummy .wav files to simulate downloaded youtube/NAM data."""
    import numpy as np
    import soundfile as sf
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    sample_rate = 22050
    t = np.linspace(0, 1, sample_rate)
    
    files = {
        "dataset_baseline/Academic_Clean_Tone.wav": np.sin(2 * np.pi * 440 * t), # Clean sine
        "dataset_baseline/Academic_Fuzz_Tone.wav": np.sign(np.sin(2 * np.pi * 440 * t)), # Square wave (Fuzz)
        "youtube_stems/Scraped_YouTube_Heavy_Metal.wav": np.sign(np.sin(2 * np.pi * 220 * t)) * 0.8,
        "youtube_stems/Scraped_YouTube_Troll_Acoustic.wav": np.sin(2 * np.pi * 880 * t) * 0.2, # Name says metal, but sounds like weak clean
    }
    
    for filepath, data in files.items():
        dir_name = os.path.dirname(filepath)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        sf.write(filepath, data, sample_rate)
        print(f"   [Mock Data] Generated: {filepath}")

def run_master_training():
    print("=========================================================")
    print("🎸 [PHASE 12] INITIATING MASTER DB TRAINING SEQUENCE 🎸")
    print("=========================================================")
    
    # 1. Initialize DBs
    print("\n[STEP 1] Initializing ChromaDB (Vector Neural Brain)...")
    db = VectorDBManager()
    
    # 2. Get Data
    print("\n[STEP 2] Harvesting Data Source Files (.wav)...")
    generate_mock_wav_files("dataset_baseline")
    
    # 3. Layer 1 Baseline Ingestion (The Absolute Truth)
    print("\n[STEP 3] Extracting Layer 1 (Academic Baseline) MFCCs...")
    baseline_db = []
    
    clean_mfcc = process_single_file("dataset_baseline/Academic_Clean_Tone.wav")["features"]["mfcc_vector"]
    fuzz_mfcc = process_single_file("dataset_baseline/Academic_Fuzz_Tone.wav")["features"]["mfcc_vector"]
    
    baseline_db.append({"trusted_label": "Clean_Tone", "mfcc_vector": clean_mfcc})
    baseline_db.append({"trusted_label": "Fuzz_Tone", "mfcc_vector": fuzz_mfcc})
    
    # Save baseline to disk for Layer 3 to use
    with open("master_baseline.json", "w") as f:
        json.dump(baseline_db, f)
        
    print("   ✅ Layer 1 Baseline DB Created. Trust Anchor Established.")
    
    # Inject baseline into ChromaDB directly
    db.collection.upsert(
        ids=["base_clean_001", "base_fuzz_001"],
        embeddings=[clean_mfcc, fuzz_mfcc],
        metadatas=[{"source": "HuggingFace", "preset": "Clean_Tone"}, {"source": "HuggingFace", "preset": "Fuzz_Tone"}],
        documents=["Layer 1 Clean Anchor", "Layer 1 Fuzz Anchor"]
    )
    print("   ✅ Layer 1 Ingested into ChromaDB.")

    # 4. Layer 2 & 3 Process (Scraped Data Cross-Validation)
    print("\n[STEP 4] Processing Scraped YouTube Data through Layer 3 Bouncer...")
    
    yt_metal_mfcc = process_single_file("youtube_stems/Scraped_YouTube_Heavy_Metal.wav")["features"]["mfcc_vector"]
    yt_troll_mfcc = process_single_file("youtube_stems/Scraped_YouTube_Troll_Acoustic.wav")["features"]["mfcc_vector"]
    
    yt_metal_candidate = {"label": "YouTube Heavy Metal", "mfcc_vector": yt_metal_mfcc}
    yt_troll_candidate = {"label": "YouTube Heavy Metal (Actually Acoustic)", "mfcc_vector": yt_troll_mfcc}
    
    print("   -> Filtering Candidate: 'YouTube Heavy Metal'...")
    is_valid_metal = cross_validate_scraped_data("master_baseline.json", yt_metal_candidate)
    if is_valid_metal:
        db.collection.upsert(
            ids=["yt_metal_001"], embeddings=[yt_metal_mfcc], 
            metadatas=[{"source": "YouTube", "preset": "Heavy_Metal_Riff"}], documents=["Scraped metal tone"]
        )
        print("   🟢 [INGESTED] YouTube Heavy Metal added to ChromaDB.")
        
    print("\n   -> Filtering Candidate: 'YouTube Heavy Metal (Actually Acoustic)'...")
    is_valid_troll = cross_validate_scraped_data("master_baseline.json", yt_troll_candidate)
    if is_valid_troll:
        db.collection.upsert(
            ids=["yt_troll_001"], embeddings=[yt_troll_mfcc], 
            metadatas=[{"source": "YouTube", "preset": "Troll_Acoustic"}], documents=["Scraped acoustic tone"]
        )
    else:
        print("   🔴 [REJECTED] Troll data dropped. DB safe.")
    
    print("\n[STEP 5] Training Complete. Vector DB Status:")
    print(f"   🧠 DB currently holds {db.collection.count()} validated tone vectors.")
    print("=========================================================")
    print("✅ AI IS NOW READY TO PREDICT TONES!")

if __name__ == "__main__":
    run_master_training()
