import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from . import database
import os

INDEX_PATH = "journal_index.faiss"
MODEL_NAME = 'all-MiniLM-L6-v2'

model = SentenceTransformer(MODEL_NAME)
embedding_dim = model.get_sentence_embedding_dimension()

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))

def chunk_text(text, chunk_size=512, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def add_entry_to_index(entry_id, entry_content):
    chunks = chunk_text(entry_content)
    chunk_embeddings = model.encode(chunks)
    chunk_ids = [database.save_entry_chunk(entry_id, chunk) for chunk in chunks]
    index.add_with_ids(np.array(chunk_embeddings), np.array(chunk_ids))
    faiss.write_index(index, INDEX_PATH)
    print(f"Added {len(chunks)} chunks for entry ID {entry_id} to the index.")

def search_index(query_text, k=5):
    if index.ntotal == 0:
        return "The journal index is empty. Please add some entries or run the rebuild script."
    query_embedding = model.encode([query_text])
    distances, chunk_ids = index.search(np.array(query_embedding), k)
    retrieved_chunks = database.get_chunk_text_by_ids(chunk_ids[0])
    context = "\n\n---\n\n".join([chunk['chunk_text'] for chunk in retrieved_chunks])
    return context 