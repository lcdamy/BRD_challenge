# clean_customer_info.py

import pandas as pd
from datetime import datetime
import os

# CONFIGURATION
OUTPUT_DIR = "../output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def standardize_date(date_str):
    try:
        return pd.to_datetime(date_str, dayfirst=True, errors='coerce').date()
    except Exception:
        return None

def clean_customer_info(input_path, output_path):
    # Load and split the file
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"❌ Error: The file '{input_path}' does not exist.")
        return
    df = df.iloc[:, 0].str.split(",", expand=True)
    df.columns = ['customer_id', 'email', 'phone', 'region', 'date_of_birth']
    df['customer_id'] = df['customer_id'].astype(int)

    # Clean date format
    df['date_of_birth'] = df['date_of_birth'].apply(standardize_date)

    # Normalize region
    df['region'] = df['region'].str.strip().str.title()

    # Deduplicate by customer_id (keep latest by date_of_birth)
    df = df.sort_values(by='date_of_birth', ascending=False)
    df = df.drop_duplicates(subset='customer_id', keep='first')

    # sort by customer_id
    df = df.sort_values(by='customer_id')

    # Export cleaned data
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned file saved to: {output_path}")

# Entry point
if __name__ == "__main__":
    input_csv = "../data/Dummy Data cust Info.csv"
    output_csv = "../output/Cleaned_Customer_Info.csv"
    clean_customer_info(input_csv, output_csv)
