🧾 Overview

This project demonstrates an end-to-end ETL pipeline, analytical reporting, and visualization based on offline banking transaction data. The aim is to improve customer insights, data quality, and support strategic decision-making in line with banking compliance and operational efficiency.

🧰 Tools & Technologies

- Python 3.9+ for ETL scripting and analysis
- pandas for data cleaning and transformation
- psycopg2 for PostgreSQL integration
- matplotlib & seaborn for visualizations
- PostgreSQL as the target data warehouse

📁 Folder Structure

```
Senior_Data_Analyst_ETL_Case_Submission/
├── README.md
├── ETL_Process_Design.pdf
├── data/
├── scripts/
├── sql/
├── output/
└── report.pdf
```

🔄 ETL Workflow Summary

**Extract:**

- Load raw offline data from CSV files (transactions and customer info)

**Transform:**

- Clean column names and formats
- Convert amounts to float and standardize dates
- Extract identifiers and periods from comment fields
- Infer transaction types (credit/debit) where missing

**Load:**

- Load cleaned data into a PostgreSQL data warehouse using psycopg2

📊 Analytical Tasks Performed

- Disbursement per customer, period, transaction type, and currency
- Average transaction amount by period
- Regional disbursement summary with visual insights

📈 Visuals Generated:

- Bar chart of disbursement by region

📝 SQL Query Highlights

Located in the sql/ folder:

- Total transactions & amounts per customer
- Average credit transaction amount per region
- Allocation summary per customer, period, region, and currency
- sql query to create customers and transactions tables

🚀 How to Run

1. Install required libraries:

```bash
pip install pandas matplotlib seaborn psycopg2
```

2. Run data scripts in order:

```bash
python scripts/clean_transactions.py
python scripts/clean_customers.py
python scripts/load_to_postgres.py
python scripts/infer_transaction_type.py
python scripts/analyze_disbursements.py
```

👤 Author

[Pierre Damien Murindangabo Cyuzuzo]Senior Data Analyst Candidate

# BRD_challenge
