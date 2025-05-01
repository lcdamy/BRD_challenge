import os
import pandas as pd
import psycopg2
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_FILE = os.path.join(OUTPUT_DIR, "Cleaned_Customer_Info.csv")

DB_PARAMS = {
    "dbname": "brd_challenge",
    "user": "postgres",
    "password": "Zudanga12345",
    "host": "localhost",
    "port": "5432"
}
TABLE_NAME = "customers"

# Load CSV
df = pd.read_csv(CSV_FILE)

# Clean & format date_of_birth to YYYY-MM-DD
df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.strftime('%Y-%m-%d')

# Connect to PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# Insert data
for _, row in df.iterrows():
    cur.execute(f"""
        INSERT INTO {TABLE_NAME} 
        (customer_id, email, phone, region, date_of_birth)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row['customer_id'],
        row['email'],
        row['phone'],
        row['region'],
        row['date_of_birth']
    ))

# Commit and close
conn.commit()
cur.close()
conn.close()

print(f"✅ Inserted {len(df)} customers into '{TABLE_NAME}'.")
