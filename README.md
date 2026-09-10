# FinSight AI

AI-Powered Personal Expense Tracker

FinSight AI is a personal expense tracking application that helps users upload bank transaction data, automatically categorize expenses, analyze spending patterns, and ask financial questions using natural language.

Live Demo: https://finsight-ai-bk9pjiwt4bwmcbhl2ddzez.streamlit.app/

## Features

### Transaction Management

* Upload transactions using a CSV file
* Automatically categorize transactions
* Identify income and expenses
* Handle duplicate transactions
* Store transaction data using SQLite
* Search and filter transactions

### Dashboard

The dashboard provides an overview of financial activity, including:

* Total income
* Total expenses
* Number of transactions
* Spending by category
* Daily spending trends

### Analytics

The Analytics section provides interactive visualizations to understand spending patterns.

Users can analyze:

* Category-wise spending
* Daily spending trends
* Income versus expenses
* Transaction distribution

### AI Analyst

FinSight AI integrates Google Gemini to allow users to ask questions about their financial data using natural language.

Example questions:

* How much did I spend on food?
* What is my total spending?
* Which category has the highest spending?
* How much did I spend on shopping?

The AI converts the user's question into a SQL query, executes it against the SQLite database, and returns the result in a simple format.

Only read-only SQL queries are allowed for AI-generated analysis.

### Data Manager

The Data Manager allows users to manage uploaded transaction data and track the files used to process transactions.

## Technology Stack

* Python
* Streamlit
* Pandas
* SQLite
* Plotly
* Google Gemini API
* Git and GitHub

## How It Works

CSV Upload
↓
Data Processing with Pandas
↓
Transaction Categorization
↓
SQLite Database
↓
Dashboard and Analytics
↓
Gemini AI Analysis

For AI-based questions:

Natural Language Question
↓
Gemini AI
↓
SQL Query
↓
Read-Only SQLite Query
↓
Financial Result

## Project Structure

```text
FinSight-AI/
│
├── app.py
├── ai_engine.py
├── database.py
├── processor.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/simranagarwal1008/FinSight-AI.git
cd FinSight-AI
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Deployment

FinSight AI is deployed using Streamlit Community Cloud.

The Gemini API key is stored securely using Streamlit Secrets and is not included in the GitHub repository.

## Future Improvements

* Monthly budget tracking
* Recurring expense detection
* Improved transaction categorization
* Personalized spending recommendations
* Exportable financial reports
* Advanced financial summaries

## Author

Simran Agarwal

MCA Student | Python | C++ | SQL | Data and AI Applications

GitHub: https://github.com/simranagarwal1008
LinkedIn: https://www.linkedin.com/in/simranagarwal1008/
