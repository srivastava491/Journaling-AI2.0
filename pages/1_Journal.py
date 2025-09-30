import streamlit as st
from modules import database, query_logic, llm_handler
from datetime import datetime, timedelta, date
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Your Journal", layout="wide")

if not st.session_state.get("authentication_status"):
    st.warning("Please login to access the journal.")
    st.stop()

st.sidebar.title(f"Welcome, {st.session_state.name}!")
user_id = st.session_state.user_id

# Main App Logic
st.title("Journal Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["🖋️ New Entry", "❓ Query Journal", "📜 All Entries", "📅 Summaries"])

with tab1:
    st.header("Add a New Entry")
    entry_date = st.date_input("Entry Date", datetime.now())
    content = st.text_area("How was your day?", height=300)
    if st.button("Save Entry"):
        if content.strip():
            with st.spinner("Saving and indexing..."):
                entry_id = database.save_daily_entry(user_id, entry_date, content)
                if entry_id:
                    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                    chunks = splitter.split_text(content)
                    database.save_entry_chunks(user_id, entry_id, entry_date, chunks)
                    
                    # Update FAISS index for the user
                    all_chunks = database.get_all_chunks(user_id)
                    if all_chunks:
                        model = SentenceTransformer('all-MiniLM-L6-v2')
                        embeddings = model.encode([c['chunk_text'] for c in all_chunks])
                        index = faiss.IndexFlatL2(embeddings.shape[1])
                        index.add(np.array(embeddings, dtype=np.float32))
                        faiss.write_index(index, query_logic.get_faiss_index_path(user_id))
                    st.success("Entry saved and indexed!")
                else:
                    st.error("Failed to save entry.")
        else:
            st.warning("Please write something.")

with tab2:
    st.header("Query Your Journal")
    query = st.text_input("Ask something...", placeholder="How was my week? or What did I do on my birthday?")
    start_date = st.date_input("Start Date (for summaries)", date.today() - timedelta(days=7))
    end_date = st.date_input("End Date (for summaries)", date.today())
    if st.button("Get Answer"):
        if query:
            with st.spinner("Thinking..."):
                response = query_logic.handle_query(user_id, query, start_date, end_date)
                st.markdown(response)
                database.save_chat_history(user_id, query, response)
        else:
            st.warning("Please enter a query.")

with tab3:
    st.header("All Your Entries")
    all_entries = database.get_all_entries(user_id)
    if not all_entries:
        st.info("You have no entries yet.")
    else:
        for entry in all_entries:
            with st.expander(f"{entry['entry_date'].strftime('%A, %B %d, %Y')}"):
                st.write(entry['content'])

with tab4:
    st.header("AI-Generated Summaries")
    st.subheader("Weekly Summaries")
    weekly_summaries = database.get_weekly_summaries(user_id)
    if not weekly_summaries:
        st.info("No weekly summaries yet.")
    else:
        for summary in weekly_summaries:
            with st.expander(f"Week of {summary['start_date']}"):
                st.write(summary['summary'])

    st.subheader("Monthly Summaries")
    monthly_summaries = database.get_monthly_summaries(user_id)
    if not monthly_summaries:
        st.info("No monthly summaries yet.")
    else:
        for summary in monthly_summaries:
            with st.expander(f"Month of {summary['start_date'].strftime('%B %Y')}"):
                st.write(summary['summary'])
