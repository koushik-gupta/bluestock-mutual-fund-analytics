import pandas as pd
import glob

# Load all CSVs and print basic info
csv_files = glob.glob('data/raw/*.csv')

for file in csv_files:
    df = pd.read_csv(file)
    print(f"\n--- {file} ---")
    print(df.shape)
    print(df.dtypes)
    print(df.head())

# Explore fund master and validate codes
try:
    fund_master = pd.read_csv('data/raw/01_fund_master.csv')
    print("\nUnique values in fund master:")
    print(fund_master['fund_house'].unique())
    print(fund_master['category'].unique())
    print(fund_master['sub_category'].unique())
    print(fund_master['risk_category'].unique())

    nav_history = pd.read_csv('data/raw/02_nav_history.csv')
    missing = set(fund_master['amfi_code']) - set(nav_history['amfi_code'])
    print(f"\nMissing codes in nav_history: {len(missing)}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
