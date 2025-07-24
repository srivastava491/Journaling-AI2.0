# 🧠 AI-Powered Journal

An intelligent, multi-page journaling application built with Streamlit, MySQL, and the Groq LLM API. This tool enables users to write, save, and reflect on their daily entries. It leverages natural language processing to query past records, automatically generates weekly and monthly summaries, and provides a comprehensive interface for exploring your personal history.

---

## ✨ Features

-   **Daily Journaling**: A clean, straightforward interface for writing and saving daily entries.
-   **AI-Powered Querying**: Ask complex questions about your past entries in natural language and get intelligent, context-aware answers.
-   **Automated Summaries**: Scripts to automatically generate insightful weekly and monthly summaries of your entries.
-   **Complete Entry History**: Browse, search, and filter all your past entries by date.
-   **Chat History**: Review your past conversations with the journal's AI.
-   **Modular Backend**: A well-organized backend that separates database interactions, AI logic, and application pages.
-   **Secure Credential Management**: Uses a `.env` file to keep your database and API keys secure.

---

## 📁 Project Structure

```
.
├── app.py                     # Main Streamlit app entry point
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables (MySQL & Groq keys)
│
├── modules/
│   ├── __init__.py            # Makes 'modules' a Python package
│   ├── database.py            # Handles all database interactions
│   ├── llm_handler.py         # Manages API calls to the Groq LLM
│   └── query_logic.py         # Contains core query classification logic
│
├── pages/
│   ├── 1_New_Entry.py         # Page for adding new entries
│   ├── 2_Query_Entries.py     # Page for querying the journal AI
│   ├── 3_Chat_History.py      # Page to view past AI conversations
│   └── 4_All_Entries.py       # Page to browse all past entries
│
├── scripts/
│   ├── weekly_summarizer.py   # Script to generate weekly summaries
│   └── monthly_summarizer.py  # Script to generate monthly summaries
│
└── sql/
    └── schema.sql             # SQL script to create the database schema
```

---

## ⚙️ Requirements

-   Python 3.8+
-   Streamlit
-   MySQL Server
-   Groq API Key
-   Python packages listed in `requirements.txt`

Install all required Python dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Clone the Repository

```bash
git clone https://github.com/srivastava491/Journaling-AI2.0.git
cd ai-journal
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory and populate it with your credentials.

```
MYSQL_HOST=127.0.0.1
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=ai_journal
GROQ_API_KEY=your_groq_api_key
```

### 3. Set Up MySQL Database

Ensure your MySQL server is running. Connect to your MySQL server and run the commands in the `sql/schema.sql` file. This will create the `ai_journal` database and all the necessary tables (`daily_entries`, `weekly_summaries`, `monthly_summaries`, `chat_history`).

You can do this via a command line client or by pasting the contents into a GUI tool like MySQL Workbench.

```bash
mysql -u your_user -p < sql/schema.sql
```

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

The application should now be running and accessible in your web browser.

### 5. Run the Summarization Scripts (Optional)

To generate weekly or monthly summaries, you can run the scripts manually from your terminal. These are designed to be automated (e.g., with cron jobs).

```bash
# To generate a summary for the previous week
python scripts/weekly_summarizer.py

# To generate a summary for the previous month
python scripts/monthly_summarizer.py
```

---

## ✍️ How to Use the App

-   **New Entry**: Navigate to this page from the sidebar to write and save your journal entry for a specific date.
-   **Query Entries**: Ask the AI questions about your journal. Select a date range to narrow the context for the AI.
-   **Chat History**: View your past questions and the AI's answers. You can also filter this history by date.
-   **All Entries**: Browse your entire journal history. Use the date pickers to search for a specific period.

---

## 🛠 Future Improvements

-   **User Authentication**: Implement a login system for private, multi-user journaling.
-   **Sentiment Analysis**: Add visualizations to track mood and sentiment over time.
-   **Cloud Deployment**: Deploy the application to a cloud service like Streamlit Community Cloud or AWS.
-   **Enhanced Summaries**: Improve the summary query logic to fetch and use the pre-generated weekly/monthly summaries for faster, more efficient responses.

---

## 📚 References

-   Groq: [groq.com](https://groq.com)
-   Streamlit: [streamlit.io](https://streamlit.io)
-   MySQL: [mysql.com](https://mysql.com)
