import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from modules import database

# Global configuration
MODEL_NAME = 'all-MiniLM-L6-v2'
FAISS_INDEX_PATH = "faiss_index_{}.bin"

class VectorStore:
    """Manages FAISS vector stores for individual users."""
    
    def __init__(self, model_name=MODEL_NAME):
        """Initialize the vector store with a sentence transformer model."""
        self.model_name = model_name
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            print(f"Error loading SentenceTransformer model: {e}")
            self.model = None
            self.embedding_dim = None
    
    def get_index_path(self, user_id):
        """Get the file path for a user's FAISS index."""
        return FAISS_INDEX_PATH.format(user_id)
    
    def load_index(self, user_id):
        """Load a user's FAISS index from disk."""
        index_path = self.get_index_path(user_id)
        if os.path.exists(index_path):
            try:
                return faiss.read_index(index_path)
            except Exception as e:
                print(f"Error loading FAISS index for user {user_id}: {e}")
                return None
        return None
    
    def save_index(self, index, user_id):
        """Save a user's FAISS index to disk."""
        index_path = self.get_index_path(user_id)
        try:
            faiss.write_index(index, index_path)
            return True
        except Exception as e:
            print(f"Error saving FAISS index for user {user_id}: {e}")
            return False
    
    def create_index(self, user_id):
        """Create a new FAISS index for a user from their chunks."""
        if not self.model:
            print("Error: SentenceTransformer model not loaded")
            return False
        
        chunks = database.get_all_chunks(user_id)
        if not chunks:
            print(f"No chunks found for user {user_id}")
            return False
        
        chunk_texts = [chunk['chunk_text'] for chunk in chunks]
        
        try:
            # Generate embeddings
            embeddings = self.model.encode(chunk_texts, show_progress_bar=True)
            
            # Create FAISS index
            index = faiss.IndexFlatL2(self.embedding_dim)
            index.add(embeddings)
            
            # Save index
            if self.save_index(index, user_id):
                print(f"Created FAISS index for user {user_id} with {index.ntotal} vectors")
                return True
            return False
            
        except Exception as e:
            print(f"Error creating FAISS index for user {user_id}: {e}")
            return False
    
    def update_index(self, user_id):
        """Update a user's FAISS index with all their current chunks."""
        return self.create_index(user_id)  # For simplicity, rebuild the entire index
    
    def search(self, user_id, query, top_k=5):
        """Search a user's index for similar chunks."""
        if not self.model:
            return []
        
        index = self.load_index(user_id)
        if index is None:
            return []
        
        chunks = database.get_all_chunks(user_id)
        if not chunks:
            return []
        
        try:
            # Encode query
            query_embedding = self.model.encode([query])
            
            # Search index
            k = min(top_k, len(chunks))
            distances, indices = index.search(query_embedding, k)
            
            # Format results
            results = []
            for i, distance in zip(indices[0], distances[0]):
                if i != -1:
                    results.append({
                        'chunk_text': chunks[i]['chunk_text'],
                        'chunk_id': chunks[i]['id'],
                        'distance': float(distance),
                        'similarity': float(1 / (1 + distance))
                    })
            
            return results
            
        except Exception as e:
            print(f"Error searching index for user {user_id}: {e}")
            return []
    
    def add_chunks(self, user_id, new_chunks):
        """Add new chunks to a user's index."""
        if not self.model:
            return False
        
        # Get all existing chunks
        all_chunks = database.get_all_chunks(user_id)
        if not all_chunks:
            return self.create_index(user_id)
        
        # Rebuild index with all chunks
        return self.update_index(user_id)
    
    def delete_user_index(self, user_id):
        """Delete a user's FAISS index file."""
        index_path = self.get_index_path(user_id)
        if os.path.exists(index_path):
            try:
                os.remove(index_path)
                print(f"Deleted FAISS index for user {user_id}")
                return True
            except Exception as e:
                print(f"Error deleting FAISS index for user {user_id}: {e}")
                return False
        return True
    
    def get_index_stats(self, user_id):
        """Get statistics about a user's index."""
        index = self.load_index(user_id)
        if index is None:
            return None
        
        return {
            'num_vectors': index.ntotal,
            'dimension': index.d,
            'index_type': type(index).__name__
        }

# Global vector store instance
vector_store = VectorStore()

def get_vector_store():
    """Get the global vector store instance."""
    return vector_store

def build_index_for_user(user_id):
    """Build FAISS index for a specific user."""
    return vector_store.create_index(user_id)

def search_user_entries(user_id, query, top_k=5):
    """Search a user's entries using vector similarity."""
    return vector_store.search(user_id, query, top_k)

def update_user_index(user_id):
    """Update a user's FAISS index."""
    return vector_store.update_index(user_id)

def delete_user_index(user_id):
    """Delete a user's FAISS index."""
    return vector_store.delete_user_index(user_id)