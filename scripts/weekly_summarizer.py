import sys
import os
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import database, llm_handler

def summarize_last_week():
    print("Starting weekly summarization process...")
    today = date.today()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)

    print(f"Fetching entries from {last_monday} to {last_sunday}.")
    entries = database.get_entries_in_range(last_monday, last_sunday)

    if not entries:
        print("No entries found for the last week. Exiting.")
        return

    full_text = "\n\n".join([f"Date: {entry['entry_date']}\n{entry['content']}" for entry in entries])
    
    prompt = f"""
You are a reflective journaling assistant. Please read the following journal entries from the past week ({last_monday} to {last_sunday}) and create a cohesive summary. The summary should be around 1500 characters and highlight key events, recurring thoughts, and overall emotional trends.

Weekly Entries:
{full_text}

Weekly Summary:
"""

    print("Generating summary with the LLM...")
    try:
        summary = llm_handler.get_llm_response(prompt)
        database.save_weekly_summary(last_monday, last_sunday, summary)
        print(f"Successfully generated and saved the weekly summary for {last_monday} to {last_sunday}.")
    except Exception as e:
        print(f"An error occurred during weekly summarization: {e}")

if __name__ == "__main__":
    summarize_last_week() 