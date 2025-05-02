import pandas as pd
import re
import os

# CONFIGURATION
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_identifier(comment):
    if pd.isna(comment):
        return None
    pattern = (
        r'(?:IDENT NO NO IDENT|IDENT NO NO|NO IDENTIFIER  HUW5669|IDENT NO ZTE|NO ID|IDNO|IDENTNO|SN|SN,|REG NO|KM|IW|ZTE|MPCST|MPELC|CT|RHA|HUW5669|'
        r'ID NO|NO IDENTIFIER|IDENT NO NO IDENT ,|IDENT NO|NO  ID|IDNTI|'
        r'NO IDENT)[\s_:,-]*(\w+(?:\s+\w+)*)'
    )
    match = re.search(pattern, comment.upper())
    return f"ID: {match.group(1).lstrip()}" if match else None

def extract_period(comment):
    if pd.isna(comment):
        return None
    match = re.search(r'\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[A-Z]*[\s\-]*(\d{2,4})', comment.upper())
    return f"{match.group(1)}-{match.group(2)}" if match else None

def clean_and_combine(file1, file2):
    df1 = pd.read_csv(file1, sep='\t', dtype=str)
    df2 = pd.read_csv(file2, sep='\t', dtype=str)

    # Standardize column names
    df1.columns = df1.columns.str.strip().str.upper()
    df2.columns = df2.columns.str.strip().str.upper()

    # Rename for consistency
    df2 = df2.rename(columns={
        'LAST NAME': 'LASTNAME',
        'UNNAMED: 7': 'TRANSACTION_TYPE'
    })

    # Guess transaction type if not provided
    def guess_transaction_type(comment):
        if pd.isna(comment):
            return "UNKNOWN"
        comment_upper = comment.upper()
        if any(keyword in comment_upper for keyword in ['DISB LOAN', 'DISBURSEMENT', 'ARREARS']):
            return "D"
        elif any(keyword in comment_upper for keyword in ['PAYMENT', 'REG PAYMENT', 'REPAYMENT', 'INSTALLMENT']):
            return "C"
        elif any(keyword in comment_upper for keyword in ['REFUND', 'REVERSAL']):
            return "C"
        else:
            return "UNKNOWN"

    df2['TRANSACTION_TYPE'] = df2['TRANSACTION_TYPE'].fillna(df2['COMMENT'].apply(guess_transaction_type))
    df1 = df1.rename(columns={
        'LAST_NAME': 'LASTNAME'
    })

    # Standardize fields
    for df in [df1, df2]:
        df['AMOUNT'] = df['AMOUNT'].str.replace(',', '').astype(float)
        df['TRANSACTION_COMMENTS'] = df['COMMENT']
        df['PERIOD'] = df['COMMENT'].apply(extract_period)
        df['IDENTIFIER'] = df['COMMENT'].apply(extract_identifier)
        df['ID'] = df['CUSTOMER_ID']
        df['ACCOUNT_NUMBER'] = df['ACCOUNT']
        df['NAME'] = df['NAME'].str.replace(r"[^\w\s]", "", regex=True).str.strip()
        df['NAME'] = df['NAME'].str.replace(r"([A-Z]+)(\d+)", r"\1_\2", regex=True)
        df['LASTNAME'] = df['LASTNAME'].str.replace(r"[^\w\s]", "", regex=True).str.strip()
        df['LASTNAME'] = df['LASTNAME'].str.replace(r"([A-Z]+)(\d+)", r"\1_\2", regex=True)
        df['CURRENCY'] = df['CURRENCY'].str.strip()

    # Final column structure
    final_cols = ['ID', 'ACCOUNT_NUMBER', 'NAME', 'LASTNAME', 'TRANSACTION_COMMENTS',
                  'PERIOD', 'IDENTIFIER', 'AMOUNT', 'CURRENCY', 'TRANSACTION_TYPE']

    df1 = df1[final_cols]
    df2 = df2[final_cols]

    # Combine
    combined = pd.concat([df1, df2], ignore_index=True)
    return combined

if __name__ == "__main__":
    file1 = os.path.join(SCRIPT_DIR, "../data/Dummy Data I TXN part 1.csv")
    file2 = os.path.join(SCRIPT_DIR, "../data/Dummy Data I TXN part 2.csv")
    output_file = "cleaned_Transactions_data.csv"

    combined_df = clean_and_combine(file1, file2)
    output_path = os.path.join(OUTPUT_DIR, output_file)
    combined_df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to: {output_path}")
