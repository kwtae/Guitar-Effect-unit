import sqlite3
import json
import time

# Phase 13: Offline Resilience (SPOF Mitigation)
# This script ensures that even if the Python Backend crashes, the Vercel Cloud goes down,
# or the phone battery dies, the Raspberry Pi can instantly (< 5ms) swap presets 
# from a lightweight, ultra-fast SQLite cache stored directly on the SD Card.

CACHE_DB_PATH = "./offline_preset_cache.db"

def init_offline_database():
    """Initializes the ultra-lightweight SQLite cache used purely for live gigs."""
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gig_presets (
            preset_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            json_parameters TEXT NOT NULL,
            embedding_vector TEXT,
            last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def sync_cloud_to_local_cache(preset_id, name, parameters_dict, embedding_list):
    """
    Called asynchronously when the phone/cloud has finished the heavy LLM/AudioMAE processing.
    Writes the resulting raw analog values into the fast local SQLite cache.
    """
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    # Compress the complex float array into a text blob for quick reading
    json_params = json.dumps(parameters_dict)
    emb_vector = json.dumps(embedding_list)
    
    cursor.execute('''
        INSERT OR REPLACE INTO gig_presets (preset_id, name, json_parameters, embedding_vector, last_synced)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (preset_id, name, json_params, emb_vector))
    
    conn.commit()
    conn.close()
    print(f"🔄 [Cache Sync] Preset '{name}' pinned to local SQLite for offline Gig Mode.")

def gig_mode_instant_swap(preset_id):
    """
    The function triggered by the physical footswitch or the offline Mobile App (BLE).
    Must execute in less than 5ms to ensure no audible delay between songs on stage.
    """
    start_time = time.perf_counter()
    
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT json_parameters FROM gig_presets WHERE preset_id = ?', (preset_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        params = json.loads(result[0])
        # Execute immediate OSC send to C++ DSP Thread here...
        # osc_client.send_message("/pedal/load_all", params)
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        print(f"⚡ [Gig Mode] Switched to '{preset_id}' in {elapsed_ms:.2f}ms. (Target: < 5ms)")
        return params
    else:
        print(f"❌ [Error] Preset '{preset_id}' not found in offline cache.")
        return None

if __name__ == "__main__":
    print("--- 🛡️ Phase 13: Offline SPOF Mitigation Test ---")
    
    init_offline_database()
    
    # 1. Simulate finding a great tone at home while connected to the Cloud "Hive Mind"
    sync_cloud_to_local_cache(
        preset_id="preset_001_clean",
        name="Gilmour Shine On",
        parameters_dict={"drive": 2.1, "level": 7.0, "comp": 4.5, "delay_ms": 450},
        embedding_list=[0.11, -0.44, 0.88] # Dummy AudioMAE vector
    )
    
    sync_cloud_to_local_cache(
        preset_id="preset_002_lead",
        name="Satriani Screaming",
        parameters_dict={"drive": 9.8, "level": 8.5, "comp": 6.0, "delay_ms": 320},
        embedding_list=[0.99, 0.84, -0.12]
    )
    
    print("\n[Simulating connection loss... Entering Stage Gig Mode...]")
    time.sleep(1)
    
    # 2. Simulate stomping the physical footswitch on stage to change sounds instantly
    gig_mode_instant_swap("preset_001_clean")
    gig_mode_instant_swap("preset_002_lead")
