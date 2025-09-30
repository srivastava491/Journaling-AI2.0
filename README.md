# 🧠 AI-Powered Journal (Multi-User Hybrid RAG Edition)

An intelligent, multi-user journaling application built with **Python** and **Streamlit**.  
This platform provides a private and secure space for users to record daily entries and gain deep insights into their reflections through a sophisticated, **hybrid AI query engine** powered by the **Groq LLM**.

---

## ✨ Key Features

- **🔐 Secure Multi-User Authentication**  
  Private accounts with secure login and registration, using **bcrypt** for industry-standard password hashing.  
  All user data is strictly partitioned by `user_id` at the database level to ensure complete privacy.

- **⚡ Advanced Hybrid RAG System**  
  The core of the application is a Retrieval-Augmented Generation pipeline that intelligently classifies user intent to perform one of two retrieval strategies:
  - **High-Speed Vector Search**: For specific, fact-based questions (e.g., *"What did I do on my birthday?"*), the system uses a user-specific **FAISS vector index** for semantic search.
  - **Optimized Hierarchical Retrieval**: For broad, time-based summaries (e.g., *"Summarize my last month"*), the system leverages pre-computed summaries and fetches raw entries only when needed.

- **⚙️ Real-Time Indexing**  
  Each new entry automatically updates the user’s FAISS index, making reflections instantly available for querying.

- **📊 Automated Summaries**  
  Backend scripts proactively generate **weekly** and **monthly** summaries for curated, zero-wait insights.

- **🖥️ Full-Featured UI**  
  Multi-page Streamlit interface including:
  - Main dashboard
  - Rich-text entry form
  - Query interface with date-range selection
  - Searchable chat history page

---

## 📁 Project Structure

```
.
├── app.py                     # Main Streamlit app for login/registration
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables (DB & Groq API keys)
│
├── modules/
│   ├── __init__.py            # Makes 'modules' a Python package
│   ├── database.py            # Handles all user-specific DB interactions
│   ├── llm_handler.py         # Manages API calls to the Groq LLM
│   └── query_logic.py         # Multi-user hybrid RAG pipeline
│
├── pages/
│   ├── 1_Journal.py           # Main dashboard (New Entry, Query, All Entries)
│   └── 2_Chat_History.py      # View & filter past AI conversations
│
├── scripts/
│   ├── build_index.py         # Build FAISS indexes for all users
│   ├── weekly_summarizer.py   # Generate weekly summaries
│   └── monthly_summarizer.py  # Generate monthly summaries
│
└── sql/
    └── schema.sql             # SQL schema for multi-user database
```

---

## 🛠️ Tech Stack

- **Backend**: Python  
- **Database**: MySQL  
- **Frontend**: Streamlit  
- **AI & Machine Learning**:  
  - LLM: **Groq API** (`llama-3.1-8b-instant`)  
  - Vector Embeddings: **sentence-transformers**  
  - Vector Search: **faiss-cpu**  
  - Text Processing: **langchain-text-splitters**  
- **Authentication**: streamlit-authenticator, bcrypt  

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+  
- A running MySQL server  

### 2. Installation & Setup

**Clone the Repository**
```bash
git clone <your-repository-url>
cd <repository-name>
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Set Up MySQL Database**
```bash
mysql -u your_user -p < sql/schema.sql
```

**Set Up Environment Variables**  
Create a `.env` file in the root directory:
```ini
MYSQL_HOST=127.0.0.1
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=ai_journal
GROQ_API_KEY=your_groq_api_key
```

### 3. Running the Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ✍️ How to Use the App

1. **Register & Login** – Create a private account. Data is tied to your user ID.  
2. **Journal Page** – Write and save entries. New entries instantly update the FAISS index.  
3. **Query Journal** – Ask questions about your journal. Use date ranges for summaries.  
4. **All Entries** – Browse your history in an expandable list.  
5. **Summaries** – View AI-generated weekly & monthly insights.  
6. **Chat History** – Search and filter your past AI conversations.  

---

## 🔮 Future Improvements

- [ ] **Sentiment Analysis**: Track mood trends with visualizations.  
- [ ] **Cloud Deployment**: Deployment guides for Streamlit Cloud / Azure.  
- [ ] **Enhanced Search**: Add keyword search alongside semantic search.  
- [ ] **Data Export**: Export entries & summaries (JSON/CSV).  
- [ ] **Notifications**: Email or in-app alerts for new summaries.  

---

## 📚 References

- [Groq](https://groq.com)  
- [Streamlit](https://streamlit.io)  
- [FAISS](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/)  
- [SentenceTransformers](https://sbert.net)  

---
