import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import database, vector_store

def rebuild_all_user_indexes():
    """Rebuild FAISS indexes for all users."""
    print("Starting the index rebuilding process for all users...")
    
    # Get all users
    users = database.get_all_users()
    if not users:
        print("No users found in the database. Exiting.")
        return
    
    print(f"Found {len(users)} users. Building indexes...")
    
    for user in users:
        user_id = user['id']
        username = user['username']
        print(f"\nProcessing user: {username} (ID: {user_id})")
        
        # Delete existing index if it exists
        vector_store.delete_user_index(user_id)
        
        # Get user's entries
        entries = database.get_all_entries(user_id)
        if not entries:
            print(f"  No entries found for user {username}")
            continue
        
        print(f"  Found {len(entries)} entries for user {username}")
        
        # Process each entry and create chunks
        for entry in entries:
            entry_id = entry['id']
            content = entry['content']
            
            # Create chunks for this entry
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, 
                chunk_overlap=50,
                separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
            )
            chunks = text_splitter.split_text(content)
            
            # Save chunks to database
            database.save_entry_chunks(user_id, entry_id, chunks)
        
        # Build the FAISS index for this user
        success = vector_store.create_index(user_id)
        if success:
            print(f"  Successfully built index for user {username}")
        else:
            print(f"  Failed to build index for user {username}")
    
    print("\nIndex rebuilding process complete!")

if __name__ == "__main__":
    rebuild_all_user_indexes() 