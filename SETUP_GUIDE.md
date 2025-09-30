# 🚀 AI-Powered Journal Setup Guide

This guide will help you set up the AI-Powered Journal application on your system.

## Prerequisites

- Python 3.8 or higher
- MySQL database
- Groq API key (free tier available)

## Quick Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd JournalingAI2.0
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Start the application**
   ```bash
   streamlit run app.py
   ```

## Manual Setup

If the automated setup doesn't work, follow these manual steps:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

1. Copy the environment template:
   ```bash
   cp env_template.txt .env
   ```

2. Edit `.env` with your actual credentials:
   ```env
   MYSQL_HOST=your_mysql_host
   MYSQL_USER=your_mysql_username
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=your_database_name
   GROQ_API_KEY=your_groq_api_key
   ```

### 3. Set Up MySQL Database

1. Create a MySQL database
2. Run the schema:
   ```bash
   mysql -u your_username -p your_database < sql/schema.sql
   ```

### 4. Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

### 5. Build Search Index

```bash
python scripts/build_index.py
```

### 6. Run the Application

```bash
streamlit run app.py
```

## Features Overview

### 🔐 User Authentication
- Secure user registration and login
- Password hashing with Streamlit-Authenticator
- Session management with automatic logout

### 📝 Journal Entries
- Write and save daily entries
- Automatic text chunking for vector search
- Entry statistics and analytics

### 🤖 AI-Powered Search
- Natural language queries about your entries
- RAG (Retrieval-Augmented Generation) pipeline
- FAISS vector search for fast similarity matching

### 📊 Analytics
- Word frequency analysis
- Writing patterns and statistics
- Entry export functionality

### 🔄 Automated Summaries
- Weekly summaries (generated every Monday)
- Monthly summaries (generated on the 1st of each month)
- User-specific and private summaries

## Project Structure

```
JournalingAI2.0/
├── .github/workflows/     # GitHub Actions for automation
├── modules/               # Core backend modules
│   ├── database.py       # Database operations
│   ├── llm_handler.py    # Groq API integration
│   ├── query_logic.py    # RAG pipeline
│   └── vector_store.py   # FAISS operations
├── pages/                # Streamlit pages
│   ├── 1_New_Entry.py    # Main journal page
│   ├── 2_Query_Entries.py # AI query interface
│   ├── 3_Chat_History.py  # Chat history viewer
│   └── 4_All_Entries.py   # Browse all entries
├── scripts/              # Automation scripts
│   ├── build_index.py    # Build FAISS indexes
│   ├── weekly_summarizer.py
│   └── monthly_summarizer.py
├── sql/                  # Database schema
│   └── schema.sql
├── app.py               # Main application entry point
├── requirements.txt     # Python dependencies
└── setup.py            # Setup script
```

## Usage

### First Time Setup

1. **Register an account**: Create your first user account
2. **Write your first entry**: Go to "New Entry" and write something
3. **Test the search**: Go to "Query Entries" and ask a question
4. **Explore your data**: Use "All Entries" to browse your journal

### Daily Usage

1. **Write entries**: Use the "New Entry" page to write daily
2. **Search your journal**: Ask questions about your past entries
3. **Review patterns**: Check "All Entries" for insights
4. **View summaries**: Automated summaries appear in your data

### Advanced Features

- **Export data**: Download your entries as text files
- **Similar entries**: Find related entries using AI
- **Word analysis**: See your most common words and patterns
- **Date filtering**: Search within specific time periods

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check your MySQL credentials in `.env`
   - Ensure MySQL server is running
   - Verify database exists

2. **Groq API error**
   - Check your API key in `.env`
   - Ensure you have API credits
   - Verify internet connection

3. **Search not working**
   - Run `python scripts/build_index.py`
   - Check if you have journal entries
   - Verify FAISS index files exist

4. **Import errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+)
   - Verify all dependencies installed

### Getting Help

1. Check the logs in the terminal
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Check database and API connections

## Security Notes

- Never commit your `.env` file
- Use strong passwords for user accounts
- Keep your Groq API key secure
- Regularly backup your database

## Performance Tips

- The first search may be slow (model loading)
- FAISS indexes are built automatically
- Large journals may take longer to search
- Consider running summaries during off-peak hours

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.






