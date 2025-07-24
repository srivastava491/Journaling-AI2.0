from datetime import date, timedelta
from modules import llm_handler, database

def classify_query(query):
    prompt = f"""Classify the following user query about their journal as either 'summary' or 'rag'.\n- 'summary' queries ask for broad patterns, trends, or overviews (e.g., 'How was my mood last month?', 'What was I focused on in May?').\n- 'rag' queries ask for specific facts or events from particular days (e.g., 'What did I do on my birthday?', 'Find the entry where I mentioned the new project').\n\nQuery: '{query}'\nClassification:"""
    response = llm_handler.get_llm_response(prompt).strip().lower()
    if "summary" in response:
        return "summary"
    return "rag"

def get_minimum_overlapping_summaries(start_date, end_date):
    s = start_date
    result_contexts = []
    while s <= end_date:
        if s + timedelta(days=29) <= end_date:
            result_contexts.append(f"Retrieve monthly summary from {s} to {s + timedelta(days=29)}")
            s += timedelta(days=30)
        elif s + timedelta(days=6) <= end_date:
            result_contexts.append(f"Retrieve weekly summary from {s} to {s + timedelta(days=6)}")
            s += timedelta(days=7)
        else:
            result_contexts.append(f"Retrieve daily entry for {s}")
            s += timedelta(days=1)
    return "\n".join(result_contexts)

def handle_query(query, start_date, end_date):
    query_type = classify_query(query)
    if query_type == "summary":
        summary_plan = get_minimum_overlapping_summaries(start_date, end_date)
        prompt = f"""You are an AI assistant analyzing a personal journal. Based on the following data retrieval plan, answer the user's query. The plan specifies which summaries (monthly, weekly, or daily) to use.\n\nData Retrieval Plan:\n{summary_plan}\n\nUser's Query: {query}\n\nAnswer:"""
        return llm_handler.get_llm_response(prompt)
    else:
        entries = database.get_entries_in_range(start_date, end_date)
        if not entries:
            return "I couldn't find any entries in that date range to answer your question."
        context = "\n\n".join([f"Date: {entry['entry_date']}\nContent: {entry['content']}" for entry in entries])
        prompt = f"""You are an AI assistant answering questions based on specific journal entries. Use only the information from the entries provided below to answer the user's query.\n\nJournal Entries:\n---\n{context}\n---\n\nUser's Query: {query}\n\nAnswer:"""
        return llm_handler.get_llm_response(prompt) 