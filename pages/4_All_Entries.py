import streamlit as st
from modules import database
from datetime import datetime, timedelta, date

st.title("📖 All Journal Entries")
st.write("Browse all your past entries or search for entries within a specific date range.")

col1, col2 = st.columns(2)
with col1:
    start_date_filter = st.date_input("Start Date", datetime.now().date() - timedelta(days=90))
with col2:
    end_date_filter = st.date_input("End Date", datetime.now().date())

if isinstance(start_date_filter, tuple):
    start_date_filter = start_date_filter[0] if start_date_filter else None
if isinstance(end_date_filter, tuple):
    end_date_filter = end_date_filter[0] if end_date_filter else None

if start_date_filter is None or end_date_filter is None:
    st.warning("Please select valid start and end dates.")
elif start_date_filter > end_date_filter:
    st.error("Error: Start date cannot be after end date.")
else:
    try:
        entries = database.get_entries_in_range(start_date_filter, end_date_filter)
        st.write(f"Found **{len(entries)}** entries from **{start_date_filter.strftime('%B %d, %Y')}** to **{end_date_filter.strftime('%B %d, %Y')}**.")
        if entries:
            for entry in entries:
                if isinstance(entry, dict) and 'entry_date' in entry and 'content' in entry:
                    entry_date = entry['entry_date']
                    if isinstance(entry_date, str):
                        try:
                            entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
                        except Exception:
                            continue
                    if not isinstance(entry_date, date):
                        continue
                    st.subheader(f"{entry_date.strftime('%A, %B %d, %Y')}")
                    st.write(entry['content'])
                    st.markdown("---")
        else:
            st.info("No entries found for the selected date range.")
    except Exception as e:
        st.error(f"Could not retrieve entries. Error: {e}") 