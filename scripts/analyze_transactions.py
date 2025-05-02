import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === CONFIGURATION ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
TRANSACTION_FILE = os.path.join(SCRIPT_DIR, "../output/Cleaned_Transactions_data.csv")
CUSTOMER_FILE = os.path.join(SCRIPT_DIR, "../output/Cleaned_Customer_Info.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../output")
OUTPUT_DIR_IMAGES = os.path.join(OUTPUT_DIR, "../images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === STEP 1: Load and Prepare Data ===
transactions = pd.read_csv(TRANSACTION_FILE)
customers = pd.read_csv(CUSTOMER_FILE)

transactions.columns = transactions.columns.str.strip().str.lower()
customers.columns = customers.columns.str.strip().str.lower()

transactions['amount'] = pd.to_numeric(transactions['amount'], errors='coerce')
transactions['transaction_type'] = transactions['transaction_type'].fillna('UNKNOWN').str.upper()
transactions['period'] = transactions['period'].astype(str).str.upper()

# === STEP 2: Merge Customer Region ===
merged_df = transactions.merge(customers[['customer_id', 'region']],
                                left_on='id', right_on='customer_id', how='left')

# === STEP 3: Disbursement Summary ===
disbursement_summary = (
    merged_df.groupby(['id', 'period', 'transaction_type', 'currency'])
    .agg(total_disbursement=('amount', 'sum'))
    .reset_index()
)
disbursement_summary.to_csv(os.path.join(OUTPUT_DIR, "disbursement_summary.csv"), index=False)

# === STEP 4: Average Transaction by Period ===
avg_txn_by_period = (
    merged_df.groupby('period')
    .agg(average_transaction_amount=('amount', 'mean'))
    .reset_index()
    .sort_values('period')
)
avg_txn_by_period.to_csv(os.path.join(OUTPUT_DIR, "average_transaction_by_period.csv"), index=False)

# === STEP 5: Visualization: Regional Disbursement ===
region_summary = (
    merged_df.groupby('region')
    .agg(total_disbursement=('amount', 'sum'))
    .reset_index()
    .sort_values('total_disbursement', ascending=False)
)

plt.figure(figsize=(10, 6))
sns.barplot(data=region_summary, x='region', y='total_disbursement', palette='viridis')
plt.title("Total Disbursement by Region")
plt.xlabel("Region")
plt.ylabel("Disbursement Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "disbursement_by_region.png"))
plt.savefig(os.path.join(OUTPUT_DIR_IMAGES, "disbursement_by_region.png"))
print("✅ All outputs saved to 'output/' folder")