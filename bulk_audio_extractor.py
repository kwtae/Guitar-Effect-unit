import os
import glob
import json
import librosa
import numpy as np
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def process_single_file(file_path):
    """Extracts MFCC and Spectral features from a single audio file of any format."""
    try:
        # librosa handles wav, mp3, flac, ogg automatically (if soundfile/ffmpeg is installed)
        y, sr = librosa.load(file_path, sr=22050, mono=True)
        
        # 1. Feature Extraction
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        mfcc_mean = np.mean(mfcc.T, axis=0).tolist()
        
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        centroid_mean = float(np.mean(centroid))
        
        # 2. Extract hypothetical metadata from filename (e.g. "fender_clean_01.wav")
        base_name = os.path.basename(file_path)
        
        return {
            "source_file": base_name,
            "status": "success",
            "features": {
                "mfcc_vector": [round(x, 4) for x in mfcc_mean],
                "spectral_centroid": round(centroid_mean, 2),
                "duration_sec": round(float(librosa.get_duration(y=y, sr=sr)), 2)
            }
        }
    except Exception as e:
        return {
            "source_file": os.path.basename(file_path),
            "status": "error",
            "error_msg": str(e)
        }

def bulk_extract_audio_features(target_directory, output_json="mfcc_database.json"):
    """Crawls a directory for large quantities of audio files and extracts features in parallel."""
    print(f"🔍 Scanning {target_directory} for audio files...")
    
    # Collect all audio extensions
    audio_files = []
    for ext in ("*.wav", "*.mp3", "*.flac", "*.ogg", "*.m4a"):
        audio_files.extend(glob.glob(os.path.join(target_directory, "**", ext), recursive=True))
        
    total_files = len(audio_files)
    if total_files == 0:
        print("⚠️ No audio files found in directory.")
        return
        
    print(f"📦 Found {total_files} audio files. Starting multi-core extraction on {cpu_count()} CPU cores...")
    
    results = []
    # Utilize multiprocessing for fast bulk extraction
    with Pool(processes=cpu_count()) as pool:
        # Use tqdm for a nice loading bar on the terminal
        for result in tqdm(pool.imap_unordered(process_single_file, audio_files), total=total_files):
            if result["status"] == "success":
                results.append(result)
            else:
                print(f"❌ Failed to process {result['source_file']}: {result['error_msg']}")
                
    # Save the giant database of extracted fingerprints
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    print(f"✅ Bulk Extraction Complete! Saved {len(results)} valid fingerprints to {output_json}.")
    print(f"💾 This compressed DB is ready to be injected into Vector DB (ChromaDB) for RAG.")

if __name__ == '__main__':
    # Usage Example: Point this to a downloaded open-source dataset directory
    # bulk_extract_audio_features("./dataset/IDMT-SMT-Guitar/")
    pass
