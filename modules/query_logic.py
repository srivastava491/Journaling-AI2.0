from modules import llm_handler, database
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from datetime import timedelta

MODEL_NAME = 'all-MiniLM-L6-v2'

try:
    model = SentenceTransformer(MODEL_NAME)
except Exception as e:
    model = None

def get_faiss_index_path(user_id):
    return f"faiss_index_user_{user_id}.bin"

def get_faiss_index(user_id):
    index_path = get_faiss_index_path(user_id)
    if os.path.exists(index_path):
        try:
            return faiss.read_index(index_path)
        except Exception as e:
            print(f"Error reading FAISS index for user {user_id}: {e}")
    return None

def classify_intent(query):
    prompt = f"Classify the user's query as 'qa' or 'summary'.\nQuery: '{query}'\nClassification:"
    response = llm_handler.get_llm_response(prompt).strip().lower()
    if "summary" in response:
        return "summary"
    return "qa"

def get_optimized_summary_context(user_id, start_date, end_date):
    context_pieces = []
    covered_dates = set()

    monthly_summaries = database.get_monthly_summaries_in_range(user_id, start_date, end_date)
    for summary in monthly_summaries:
        context_pieces.append(f"--- Monthly Summary ({summary['start_date']} to {summary['end_date']}) ---\n{summary['summary']}")
        d = summary['start_date']
        while d <= summary['end_date']:
            covered_dates.add(d)
            d += timedelta(days=1)

    weekly_summaries = database.get_weekly_summaries_in_range(user_id, start_date, end_date)
    for summary in weekly_summaries:
        date_range_to_add = [summary['start_date'] + timedelta(days=x) for x in range((summary['end_date'] - summary['start_date']).days + 1)]
        if not all(d in covered_dates for d in date_range_to_add):
            context_pieces.append(f"--- Weekly Summary ({summary['start_date']} to {summary['end_date']}) ---\n{summary['summary']}")
            for day in date_range_to_add:
                covered_dates.add(day)

    uncovered_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)) not in covered_dates]
    if uncovered_dates:
        daily_chunks_data = database.get_chunks_for_dates(user_id, uncovered_dates)
        if daily_chunks_data:
            chunks_by_date = {}
            for chunk in daily_chunks_data:
                chunks_by_date.setdefault(chunk['entry_date'], []).append(chunk['chunk_text'])
            for entry_date, chunks in sorted(chunks_by_date.items()):
                context_pieces.append(f"--- Raw Entry for {entry_date.strftime('%Y-%m-%d')} ---\n" + "\n".join(chunks))
    
    return "\n\n".join(context_pieces) if context_pieces else None

def handle_query(user_id, query, start_date=None, end_date=None):
    if model is None: return "Error: Embedding model not available."

    intent = classify_intent(query)

    if intent == "qa":
        index = get_faiss_index(user_id)
        if index is None: return "Your journal search index has not been built."
        all_chunks = database.get_all_chunks(user_id)
        if not all_chunks: return "You have no journal entries to search."
        
        index_to_chunk_id_map = [chunk['id'] for chunk in all_chunks]
        query_vector = model.encode([query])
        k = min(5, len(all_chunks))
        distances, indices = index.search(np.array(query_vector, dtype=np.float32), k)
        
        retrieved_chunk_ids = [index_to_chunk_id_map[i] for i in indices[0] if i != -1]
        relevant_texts = database.get_chunks_by_ids(user_id, retrieved_chunk_ids)
        
        if not relevant_texts: return "I couldn't find any relevant information."
        
        context = "\n\n---\n\n".join(relevant_texts)
        prompt = f"Use the following journal entries to answer the question.\n\nEntries:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        return llm_handler.get_llm_response(prompt)

    elif intent == "summary":
        if not start_date or not end_date: return "Please select a date range for the summary."
        
        context = get_optimized_summary_context(user_id, start_date, end_date)
        if not context: return f"I couldn't find any entries or summaries between {start_date} and {end_date}."
        if len(context) > 15000: return "The selected date range is too large to summarize."

        prompt = f"Based on the following context, provide a detailed summary for the user's query.\n\nContext:\n{context}\n\nQuery: {query}\n\nSummary:"
        return llm_handler.get_llm_response(prompt)