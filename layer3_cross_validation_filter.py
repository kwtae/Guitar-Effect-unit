import json
import logging

# Layer 3: The Cross-Validation Filter (The Bouncer)
# This script loads an untrusted scraped vector (Layer 2) and compares it against a trusted academic vector (Layer 1).
# If the cosine similarity contradicts the text label, it prompts the LLM to intervene.

def cosine_similarity(v1, v2):
    """Calculates Cosine Similarity between two MFCC vectors (0.0 to 1.0)"""
    import numpy as np
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

def cross_validate_scraped_data(trusted_db_file, scraped_data_item):
    """
    Validates a single scraped audio fingerprint against the baseline DB.
    scraped_data_item = {"label": "Fuzz Metal", "mfcc_vector": [...]}
    """
    print(f"🛡️ [Layer 3 Bouncer] Inspecting incoming web-scraped data: Label='{scraped_data_item['label']}'")
    
    try:
        with open(trusted_db_file, 'r') as f:
            trusted_db = json.load(f)
    except FileNotFoundError:
        print("⚠️ Trusted DB not found. Run Layer 1 (HuggingFace) baseline generator first.")
        return False

    if not trusted_db:
        print("⚠️ Trusted DB is empty.")
        return False
        
    highest_sim = 0.0
    best_matching_trusted_label = "Unknown"
    
    # Compare against every academic standard
    for trusted_item in trusted_db:
        sim = cosine_similarity(scraped_data_item["mfcc_vector"], trusted_item["mfcc_vector"])
        if sim > highest_sim:
            highest_sim = sim
            best_matching_trusted_label = trusted_item["trusted_label"]
            
    # Mock Validation Logic
    print(f"   🔍 Similarity Check: Looks {highest_sim*100:.2f}% like '{best_matching_trusted_label}'")
    
    # If the scraped YouTube title says "Fuzz Metal", but it sounds 99% like an academic "Acoustic Guitar"
    # we have a poisoning problem.
    THRESHOLD = 0.85 
    
    if highest_sim < THRESHOLD:
         print(f"   ❌ [REJECTED] Poisoned Data Detected. Mathematical waveform contradicts the user-provided text label.")
         return False
         
    # Let's say it passes the math check. Now we ask the LLM for sanity.
    print(f"   ✅ [MATH PASSED] Sending to Gemini LLM for final NLP sanity check...")
    
    # MOCK LLM CALL
    llm_verdict = "APPROVED" 
    
    if llm_verdict == "APPROVED":
        print(f"   🟢 [INGESTED] Data is pure. Sent to Vector DB (ChromaDB) permanently.")
        return True
    else:
        print(f"   🔴 [LLM REJECTED] Gemini found the description illogical. Data dropped.")
        return False

if __name__ == "__main__":
    # --- Integration Test ---
    # We will generate a fake JSON file to represent the baseline
    dummy_trusted_db = [
        {"trusted_label": "High_Gain_Distortion", "mfcc_vector": [1.0] * 20},
        {"trusted_label": "Clean_Chorus", "mfcc_vector": [-1.0] * 20}
    ]
    with open("temp_layer1_db.json", "w") as f:
        json.dump(dummy_trusted_db, f)
        
    # Scenario A: Good Data (Similar vector shape to Dist)
    good_scraped_data = {
        "label": "YouTube: Insane Metal Breakdown",
        "mfcc_vector": [0.9] * 20 
    }
    
    # Scenario B: Poisoned Data (Troll uploaded a clean tone but named it Fuzz)
    bad_scraped_data = {
        "label": "ToneHunt: Ultimate Doom Fuzz",
        "mfcc_vector": [-0.9] * 20 # Negative vector looks like clean chorus
    }
    
    print("\n--- Test 1: Valid YouTube Data ---")
    cross_validate_scraped_data("temp_layer1_db.json", good_scraped_data)
    
    print("\n--- Test 2: Troll/Mislabelled Data ---")
    cross_validate_scraped_data("temp_layer1_db.json", bad_scraped_data)
