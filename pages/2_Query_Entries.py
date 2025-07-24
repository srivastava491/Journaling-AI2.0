import streamlit as st
from modules import query_logic, database
from datetime import datetime, timedelta

st.title("❓ Query Your Journal")
st.write("Ask questions about your past entries. Select a date range to focus your query.")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=30))
with col2:
    end_date = st.date_input("End Date", datetime.now().date())

query = st.text_input("Ask something...", placeholder="e.g., How was my mood last week?")

if st.button("Get Answer"):
    if query and start_date and end_date:
        if start_date > end_date:
            st.error("Error: Start date cannot be after end date.")
        else:
            with st.spinner("Analyzing your journal..."):
                try:
                    response = query_logic.handle_query(query, start_date, end_date)
                    st.success("Here's what I found:")
                    st.markdown(response)
                    database.save_chat_history(query, response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query and select a valid date range.") 