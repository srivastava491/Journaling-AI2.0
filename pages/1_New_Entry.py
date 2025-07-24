import streamlit as st
from modules import database
from datetime import datetime

st.title("🖋️ Add a New Entry")

entry_date = st.date_input("Entry Date", datetime.now())
content = st.text_area("How was your day?", height=300, placeholder="Write about your day, your thoughts, or anything on your mind...")

if st.button("Save Entry"):
    if content and content.strip():
        try:
            database.save_daily_entry(entry_date, content)
            st.success("Your entry has been saved successfully!")
        except Exception as e:
            st.error(f"An error occurred while saving: {e}")
    else:
        st.warning("Please write something before saving.") 