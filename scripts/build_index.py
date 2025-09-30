import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import database, query_logic
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def build_all_indexes():
    print("Fetching all users...")
    users = database.get_all_users()
    if not users:
        print("No users found.")
        return

    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"Found {len(users)} users. Building indexes...")

    for user in users:
        user_id = user['id']
        print(f"  - Building index for user_id: {user_id} ({user['username']})")
        chunks = database.get_all_chunks(user_id)
        
        if not chunks:
            print(f"    - No chunks found for user {user_id}. Skipping.")
            continue
            
        chunk_texts = [chunk['chunk_text'] for chunk in chunks]
        embeddings = model.encode(chunk_texts)
        
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings, dtype=np.float32))
        
        index_file = query_logic.get_faiss_index_path(user_id)
        faiss.write_index(index, index_file)
        print(f"    - Successfully built and saved index to {index_file}")

if __name__ == "__main__":
    build_all_indexes()