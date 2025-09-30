import sys
import os
from datetime import date
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import database, llm_handler

def main():
    print("Starting monthly summarization for all users...")
    users = database.get_all_users()
    if not users:
        print("No users found.")
        return
        
    for user in users:
        user_id = user['id']
        print(f"  - Generating summary for user {user_id}...")
        today = date.today()
        end_date = today.replace(day=1) - relativedelta(days=1)
        start_date = end_date.replace(day=1)

        entries = database.get_entries_in_range(user_id, start_date, end_date)

        if not entries:
            print(f"    - No entries found for user {user_id} last month. Skipping.")
            continue

        full_text = "\n\n".join([f"Date: {entry['entry_date']}\n{entry['content']}" for entry in entries])
        prompt = f"Perform a comprehensive review of the journal entries from {start_date.strftime('%B %Y')}. Generate a detailed summary covering significant events, recurring themes, and personal growth.\n\nEntries:\n{full_text}\n\nComprehensive Monthly Summary:"
        
        summary = llm_handler.get_llm_response(prompt)
        database.save_monthly_summary(user_id, start_date, end_date, summary)
        print(f"    - Successfully generated summary for user {user_id}.")

if __name__ == "__main__":
    main()