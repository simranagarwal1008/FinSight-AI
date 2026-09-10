import sqlite3
import pandas as pd

DB_NAME = "finsight.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            source_file TEXT NOT NULL,
            UNIQUE(date, description, amount)
        )
        """
    )
    conn.commit()
    conn.close()


def load_data():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT id, date, description, amount, category, source_file FROM transactions ORDER BY date DESC, id DESC",
        conn,
    )
    conn.close()
    return df


def update_database(edited_df):
    required = ["id", "date", "description", "amount", "category", "source_file"]
    if not all(col in edited_df.columns for col in required):
        raise ValueError("Invalid ledger format.")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        for _, row in edited_df.iterrows():
            if pd.isna(row["id"]):
                continue
            cursor.execute(
                """
                UPDATE transactions
                SET date = ?, description = ?, amount = ?, category = ?, source_file = ?
                WHERE id = ?
                """,
                (
                    str(row["date"]),
                    str(row["description"]),
                    float(row["amount"]),
                    str(row["category"]),
                    str(row["source_file"]),
                    int(row["id"]),
                ),
            )
        conn.commit()
    finally:
        conn.close()


def get_uploaded_files():
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT source_file FROM transactions ORDER BY source_file"
    ).fetchall()
    conn.close()
    return [row[0] for row in rows]


def delete_file_data(filename):
    conn = get_connection()
    conn.execute("DELETE FROM transactions WHERE source_file = ?", (filename,))
    conn.commit()
    conn.close()


def clear_all_data():
    conn = get_connection()
    conn.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()
