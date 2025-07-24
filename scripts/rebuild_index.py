import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import database, vector_store
import faiss

def rebuild_full_index():
    print("Starting the index rebuilding process...")
    print("Clearing old index and database chunks...")
    if os.path.exists(vector_store.INDEX_PATH):
        os.remove(vector_store.INDEX_PATH)
    database.clear_chunks_table()
    vector_store.index = faiss.IndexIDMap(faiss.IndexFlatL2(vector_store.embedding_dim))
    all_entries = database.get_all_daily_entries()
    if not all_entries:
        print("No entries found in the database. Exiting.")
        return
    print(f"Found {len(all_entries)} entries to index.")
    for entry in all_entries:
        entry_id = entry['id']
        entry_content = entry['content']
        print(f"Processing entry ID: {entry_id}")
        vector_store.add_entry_to_index(entry_id, entry_content)
    print("Saving the final, complete index to disk...")
    faiss.write_index(vector_store.index, vector_store.INDEX_PATH)
    print("\nRebuilding process complete!")
    print(f"The index now contains {vector_store.index.ntotal} vectors.")

if __name__ == "__main__":
    rebuild_full_index() 