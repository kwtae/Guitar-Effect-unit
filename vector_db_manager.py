import json
import chromadb
from chromadb.config import Settings

class VectorDBManager:
    def __init__(self, db_path="./chroma_db"):
        print("💾 Initializing ChromaDB (Vector Database)...")
        # Persistent storage locally so we don't have to re-inject data every time
        self.client = chromadb.PersistentClient(path=db_path)
        
        # We create a collection specifically for Guitar Tones. 
        # L2 (Euclidean distance) or Cosine Similarity can be used for MFCC matching.
        self.collection = self.client.get_or_create_collection(
            name="guitar_tone_fingerprints",
            metadata={"hnsw:space": "cosine"} # Cosine similarity usually works best for MFCCs
        )

    def ingest_from_bulk_json(self, json_file_path):
        """Reads the output from bulk_audio_extractor.py and injects it into Vector DB"""
        print(f"📥 Loading bulk dataset from {json_file_path}...")
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
        except FileNotFoundError:
            print("⚠️ Dataset not found. Please run bulk extraction first.")
            return

        documents = []
        embeddings = []
        metadatas = []
        ids = []

        for row in dataset:
            # The 'ID' in ChromaDB
            ids.append(row["source_file"])
            
            # The Vector itself (20-dimensional MFCC)
            embeddings.append(row["features"]["mfcc_vector"])
            
            # Metadata (We can store the centroid and any hypothetical extracted tags)
            metadatas.append({
                "spectral_centroid": row["features"]["spectral_centroid"],
                "duration": row["features"]["duration_sec"]
            })
            
            # Document (Text description). We mock this based on filename for now.
            documents.append(f"Guitar tone reference extracted from {row['source_file']}")

        # Batch insert into Vector DB
        print(f"🚀 Injecting {len(embeddings)} multi-dimensional vectors into ChromaDB...")
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        print("✅ Vector Vector Injection Complete! Ready for Cosine Similarity Searches.")

    def search_closest_tone(self, target_mfcc_vector, n_results=3):
        """
        [Phase 4 RAG Core]
        Given a new audio fingerprint (e.g., from an isolated Demucs stem), 
        find the N closest known tones from the pre-trained database.
        """
        print(f"🔍 Searching Vector DB for closest acoustic matches...")
        results = self.collection.query(
            query_embeddings=[target_mfcc_vector],
            n_results=n_results
        )
        
        # Display Results
        print("\n🏆 Top Matches:")
        distances = results['distances'][0]
        match_ids = results['ids'][0]
        
        for i in range(len(match_ids)):
            # Convert cosine distance to an intuitive "Similarity Score" percentage
            similarity = round((1.0 - distances[i]) * 100, 2)
            print(f" - {match_ids[i]} (Acoustic Similarity: {similarity}%)")
            
        return results

if __name__ == '__main__':
    # Usage Example:
    # 1. db = VectorDBManager()
    # 2. db.ingest_from_bulk_json("mfcc_database.json")
    # 3. db.search_closest_tone( [ -20.4, 15.3, ... ] ) 
    pass
