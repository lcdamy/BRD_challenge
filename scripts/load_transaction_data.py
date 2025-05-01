import os
import psycopg2
import pandas as pd

# CONFIGURATION
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_FILE = os.path.join(OUTPUT_DIR, "Cleaned_Transactions_data.csv")

DB_PARAMS = {
    "dbname": "brd_challenge",
    "user": "postgres",
    "password": "Zudanga12345",
    "host": "localhost",
    "port": "5432"
}
TABLE_NAME = "transactions"

# STEP 1: Load CSV into pandas
df = pd.read_csv(CSV_FILE)

# STEP 2: Connect to PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# STEP 3: Insert row-by-row
for _, row in df.iterrows():
    # Remove "ID:" before the identifier if the identifier is not null or empty
    if row['IDENTIFIER'] and isinstance(row['IDENTIFIER'], str):
        row['IDENTIFIER'] = row['IDENTIFIER'].replace("ID:", "").strip()
    # Insert the row into the database
    cur.execute(f"""
        INSERT INTO {TABLE_NAME} 
        (id, account_number, name, lastname, transaction_comments, period, identifier, amount, currency, transaction_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# STEP 4: Commit and close
conn.commit()
cur.close()
conn.close()

print(f"✅ {len(df)} records inserted into '{TABLE_NAME}'.")
