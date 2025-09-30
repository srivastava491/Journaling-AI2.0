import streamlit as st
from modules import database
from datetime import datetime, date, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Chat History", layout="wide")

if not st.session_state.get("authentication_status"):
    st.warning("Please login to access the journal.")
    st.stop()

st.sidebar.title(f"Welcome, {st.session_state.name}!")
user_id = st.session_state.user_id

st.title("📜 Chat History")
st.write("Here are your past conversations with your AI journal assistant.")

try:
    full_history = database.get_chat_history(user_id)
except Exception as e:
    st.error(f"Could not retrieve chat history. Error: {e}")
    st.stop()

if not full_history:
    st.info("You have no chat history yet. Go to the 'Journal' page to ask a question.")
    st.stop()

# --- Filtering and Search UI ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("🔍 Filter by Date")
    start_date = st.date_input("Show history from", date.today() - timedelta(days=30))
    end_date = st.date_input("Show history to", date.today())

with col2:
    st.subheader("🔍 Search within history")
    search_term = st.text_input("Enter a keyword to search for in queries or responses:")

# --- Apply Filters ---
filtered_history = full_history

if start_date and end_date:
    if start_date > end_date:
        st.error("Start date cannot be after end date.")
    else:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        filtered_history = [
            item for item in full_history 
            if start_datetime <= item['timestamp'] <= end_datetime
        ]

if search_term:
    search_term_lower = search_term.lower()
    filtered_history = [
        item for item in filtered_history
        if search_term_lower in item['query'].lower() or search_term_lower in item['response'].lower()
    ]

# --- Display Filtered History ---
st.markdown("---")
st.header("Filtered Results")

if not filtered_history:
    st.warning("No chat history matches your filters.")
else:
    for item in filtered_history:
        with st.container():
            st.markdown(f"**You asked:** {item['query']}")
            st.info(f"**AI answered:** {item['response']}")
            st.caption(f"On: {item['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown("---")
