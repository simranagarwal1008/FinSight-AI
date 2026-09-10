import os
import re
import sqlite3

import pandas as pd
from dotenv import load_dotenv
from google import genai

try:
    import streamlit as st
except Exception:
    st = None

from database import DB_NAME

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key and st is not None:
            try:
                api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
            except Exception:
                pass
        if not api_key:
            raise ValueError("Gemini API key not found. Add GEMINI_API_KEY to your local .env or Streamlit Cloud Secrets.")
        _client = genai.Client(api_key=api_key)
    return _client


def ask_ai_about_finances(user_question, df_schema_context):
    prompt = f"""
You are the SQL analyst inside a personal expense-tracking application.
The SQLite table is named transactions.
Schema:
{df_schema_context}

User question:
{user_question}

Rules:
- Return ONLY one valid SQLite SELECT statement.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, PRAGMA, ATTACH, DETACH, or VACUUM.
- Use only the transactions table.
- For spending, expenses are negative amounts, so use ABS(amount) when calculating expense totals.
- Keep the query simple and directly answer the user's question.
"""

    response = get_client().models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    sql = response.text.strip()
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)
    return sql.strip()


def execute_read_only_sql(query):
    query = query.strip().rstrip(";").strip()
    normalized = re.sub(r"\s+", " ", query).upper()

    if not normalized.startswith("SELECT ") and normalized != "SELECT":
        return "Security Error: Only SELECT queries are allowed."

    forbidden = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|PRAGMA|ATTACH|DETACH|VACUUM|REPLACE)\b"
    if re.search(forbidden, normalized):
        return "Security Error: Query contains a blocked SQL operation."

    if ";" in query:
        return "Security Error: Multiple SQL statements are not allowed."

    if "TRANSACTIONS" not in normalized:
        return "Security Error: Query must use the transactions table."

    try:
        conn = sqlite3.connect(DB_NAME)
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as exc:
        return f"Error executing query: {exc}"
