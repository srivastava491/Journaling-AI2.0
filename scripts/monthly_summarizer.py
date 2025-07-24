import sys
import os
from datetime import date
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import database, llm_handler

def summarize_last_month():
    print("Starting monthly summarization process...")
    today = date.today()
    first_day_of_current_month = today.replace(day=1)
    end_date = first_day_of_current_month - relativedelta(days=1)
    start_date = end_date.replace(day=1)
    
    print(f"Fetching entries for the month of {start_date.strftime('%B %Y')}, from {start_date} to {end_date}.")
    entries = database.get_entries_in_range(start_date, end_date)

    if not entries:
        print(f"No entries found for {start_date.strftime('%B %Y')}. Exiting.")
        return

    full_text = "\n\n".join([f"Date: {entry['entry_date']}\n{entry['content']}" for entry in entries])

    prompt = f"""
You are a highly insightful journaling analyst. Please perform a comprehensive review of the following journal entries from the past month ({start_date.strftime('%B %Y')}). Generate a detailed summary of about 4000 characters. The summary should cover:
1.  A high-level overview of the month.
2.  Significant events, challenges, and achievements.
3.  Recurring themes, habits, and emotional patterns.
4.  Any notable changes or personal growth observed.

Monthly Entries:
{full_text}

Comprehensive Monthly Summary:
"""

    print("Generating detailed monthly summary with the LLM...")
    try:
        summary = llm_handler.get_llm_response(prompt)
        database.save_monthly_summary(start_date, end_date, summary)
        print(f"Successfully generated and saved the monthly summary for {start_date.strftime('%B %Y')}.")
    except Exception as e:
        print(f"An error occurred during monthly summarization: {e}")

if __name__ == "__main__":
    summarize_last_month() 