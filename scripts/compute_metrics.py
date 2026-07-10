import pandas as pd
import sqlite3
import os
import glob

# Ensure processed directory exists
os.makedirs('data/processed', exist_ok=True)

# 1. Clean nav_history.csv
nav_history = pd.read_csv('data/raw/02_nav_history.csv')
nav_history['date'] = pd.to_datetime(nav_history['date'])
nav_history = nav_history.sort_values(['amfi_code', 'date'])
nav_history['nav'] = nav_history.groupby('amfi_code')['nav'].ffill()
nav_history = nav_history.drop_duplicates()
nav_history = nav_history[nav_history['nav'] > 0]
nav_history.to_csv('data/processed/02_nav_history.csv', index=False)

# 2. Clean investor_transactions.csv
investor_tx = pd.read_csv('data/raw/08_investor_transactions.csv')
investor_tx['transaction_type'] = investor_tx['transaction_type'].str.strip().str.title()
investor_tx = investor_tx[investor_tx['amount_inr'] > 0]
investor_tx['transaction_date'] = pd.to_datetime(investor_tx['transaction_date'])
valid_kyc = ['Verified', 'Pending', 'Rejected']
investor_tx['kyc_status'] = investor_tx['kyc_status'].apply(lambda x: x if x in valid_kyc else 'Unknown')
investor_tx.to_csv('data/processed/08_investor_transactions.csv', index=False)

# 3. Clean scheme_performance.csv
scheme_perf = pd.read_csv('data/raw/07_scheme_performance.csv')
return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
for col in return_cols:
    scheme_perf[col] = pd.to_numeric(scheme_perf[col], errors='coerce')
# Check expense_ratio range (0.1% - 2.5%)
scheme_perf['expense_ratio_pct'] = scheme_perf['expense_ratio_pct'].clip(lower=0.1, upper=2.5)
scheme_perf.to_csv('data/processed/07_scheme_performance.csv', index=False)

# 4. Copy the remaining 7 datasets to processed directly for now
other_files = [
    '01_fund_master.csv', '03_aum_by_fund_house.csv', 
    '04_monthly_sip_inflows.csv', '05_category_inflows.csv', 
    '06_industry_folio_count.csv', '09_portfolio_holdings.csv', 
    '10_benchmark_indices.csv'
]
for f in other_files:
    df = pd.read_csv(f'data/raw/{f}')
    df.to_csv(f'data/processed/{f}', index=False)

# 5. Load to SQLite
conn = sqlite3.connect('bluestock_mf.db')

for file in glob.glob('data/processed/*.csv'):
    table_name = os.path.basename(file).split('.')[0][3:] # remove '01_' prefix and '.csv'
    df = pd.read_csv(file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

conn.close()
print("Data cleaning and SQLite load complete.")
