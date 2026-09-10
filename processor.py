import sqlite3
import pandas as pd

from database import DB_NAME


def categorize_transaction(description):
    desc = str(description).upper()

    rules = {
        "PAYROLL": "Income",
        "SALARY": "Income",
        "UPI/CR": "Income",
        "AMZN": "Shopping",
        "AMAZON": "Shopping",
        "FLIPKART": "Shopping",
        "MYNTRA": "Shopping",
        "WALMART": "Groceries",
        "TARGET": "Groceries",
        "DMART": "Groceries",
        "RELIANCE FRESH": "Groceries",
        "STARBUCKS": "Food & Drink",
        "ZOMATO": "Food & Drink",
        "SWIGGY": "Food & Drink",
        "UBER EATS": "Food & Drink",
        "MCDONALD": "Food & Drink",
        "NETFLIX": "Subscriptions",
        "SPOTIFY": "Subscriptions",
        "PRIME VIDEO": "Subscriptions",
        "HOTSTAR": "Subscriptions",
        "UBER": "Transportation",
        "OLA": "Transportation",
        "RAPIDO": "Transportation",
        "SHELL": "Gas/Automotive",
        "BPCL": "Gas/Automotive",
        "HPCL": "Gas/Automotive",
        "PETROL": "Gas/Automotive",
        "ELECTRICITY": "Bills & Utilities",
        "WATER BILL": "Bills & Utilities",
        "AIRTEL": "Bills & Utilities",
        "JIO": "Bills & Utilities",
        "RENT": "Housing",
        "PHARMACY": "Health",
        "HOSPITAL": "Health",
        "MEDICAL": "Health",
        "GYM": "Health & Fitness",
    }

    for keyword, category in rules.items():
        if keyword in desc:
            return category
    return "Uncategorized"


def process_uploaded_file(file):
    filename = file.name
    df = pd.read_csv(file)

    required_columns = {"Date", "Description", "Amount"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"CSV is missing required columns: {', '.join(sorted(missing))}. "
            "Expected: Date, Description, Amount."
        )

    df = df[["Date", "Description", "Amount"]].copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Description"] = df["Description"].fillna("Unknown transaction").astype(str).str.strip()
    df = df.dropna(subset=["Date", "Amount"])
    df["Category"] = df["Description"].apply(categorize_transaction)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    new_records = 0
    duplicate_records = 0

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT OR IGNORE INTO transactions
            (date, description, amount, category, source_file)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                row["Date"],
                row["Description"],
                float(row["Amount"]),
                row["Category"],
                filename,
            ),
        )
        if cursor.rowcount == 1:
            new_records += 1
        else:
            duplicate_records += 1

    conn.commit()
    conn.close()
    return new_records, duplicate_records
