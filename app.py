import streamlit as st
from modules import database
from datetime import datetime, timedelta

st.set_page_config(
    page_title="AI Powered Journal",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ Your AI-Powered Journal")
st.write("Welcome back! Here are your most recent entries. Use the sidebar to navigate.")

st.header("Recent Activity")
try:
    entries = database.get_entries_in_range(datetime.now().date() - timedelta(days=7), datetime.now().date())

    if entries:
        for entry in entries:
            st.subheader(f"{entry['entry_date'].strftime('%A, %B %d, %Y')}")
            st.write(entry['content'])
            st.markdown("---")
    else:
        st.info("You have no entries in the last 7 days. Go to the 'New Entry' page to add one!")
except Exception as e:
    st.error(f"Failed to connect to the database. Please check your .env configuration. Error: {e}")


