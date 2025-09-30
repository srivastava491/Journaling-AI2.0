import sys
import os
from datetime import date, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import database, llm_handler

def main():
    print("Starting weekly summarization for all users...")
    users = database.get_all_users()
    if not users:
        print("No users found.")
        return

    for user in users:
        user_id = user['id']
        print(f"  - Generating summary for user {user_id}...")
        today = date.today()
        end_date = today - timedelta(days=today.weekday() + 1)
        start_date = end_date - timedelta(days=6)

        entries = database.get_entries_in_range(user_id, start_date, end_date)

        if not entries:
            print(f"    - No entries found for user {user_id} last week. Skipping.")
            continue

        full_text = "\n\n".join([f"Date: {entry['entry_date']}\n{entry['content']}" for entry in entries])
        prompt = f"Review the following journal entries from the past week and provide a concise summary. Highlight key events, moods, and recurring themes.\n\nEntries:\n{full_text}\n\nWeekly Summary:"
        
        summary = llm_handler.get_llm_response(prompt)
        database.save_weekly_summary(user_id, start_date, end_date, summary)
        print(f"    - Successfully generated summary for user {user_id}.")

if __name__ == "__main__":
    main()