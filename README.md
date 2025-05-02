🧾 Overview

This project demonstrates an end-to-end ETL pipeline, analytical reporting, and visualization based on offline banking transaction data. The aim is to improve customer insights, data quality, and support strategic decision-making in line with banking compliance and operational efficiency.


📁 Folder Structure Explained

```
Senior_Data_Analyst_ETL_Case_Submission/
├── README.md                # Project overview and instructions.
├── ETL_Process_Design.pdf   # Detailed ETL process design documentation.
├── data/                    # Raw and processed data files.
├── images/                  # Visual assets for reports and documentation.
├── scripts/                 # Python scripts for data cleaning, loading, and analysis.
├── sql/                     # SQL scripts for data summarization and transformation.
├── output/                  # Generated outputs such as reports or processed data.
└── raport_summary.pdf       # Summary report of the analysis and findings.
```

🚀 How to Run

1. Install required libraries:

```bash
pip install pandas matplotlib seaborn psycopg2
```

2. Run data scripts in order:

```bash
python scripts/clean_transaction_data.py
python scripts/clean_customer_info.py
python scripts/load_customer_info.py
python scripts/load_transaction_data.py
python scripts/analyze_transactions.py
```

👤 Author

[Pierre Damien Murindangabo Cyuzuzo - Senior Data Analyst Candidate](https://www.linkedin.com/in/pierre-damien-murindangabo-cyuzuzo-709b53151/)

