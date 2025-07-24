import streamlit as st
from modules import database

st.title("📜 Chat History")
st.write("Here are your past conversations with your journal.")

try:
    history = database.get_chat_history()

    if history:
        for item in history:
            with st.container():
                st.markdown(f"**You asked:** {item['query']}")
                st.info(f"{item['response']}")
                st.caption(f"Answered on: {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown("---")
    else:
        st.info("You don't have any chat history yet. Go to the 'Query Entries' page to ask a question!")
except Exception as e:
    st.error(f"Could not retrieve chat history. Error: {e}") 