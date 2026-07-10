"""
Bonus Challenge B4 – Markowitz Efficient Frontier
=================================================
Calculates and plots the Efficient Frontier for 5 selected mutual funds.
Simulates 10,000 random portfolios to find the optimal weight allocation
that maximizes the Sharpe Ratio.

Run from project root:
    python scripts/efficient_frontier.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).parent.parent
NAV_PATH  = ROOT / "data" / "processed" / "02_nav_history.csv"
PERF_PATH = ROOT / "data" / "processed" / "07_scheme_performance.csv"
OUT_PATH  = ROOT / "reports" / "efficient_frontier.png"

# ── Parameters ─────────────────────────────────────────────────────────────
NUM_PORTFOLIOS = 10_000
RISK_FREE_RATE = 0.06 # Assuming 6% annual risk-free rate
TRADING_DAYS   = 252

# ── Load Data ──────────────────────────────────────────────────────────────
nav_df  = pd.read_csv(NAV_PATH, parse_dates=["date"])
perf_df = pd.read_csv(PERF_PATH)

# Select top 5 funds by AUM
top5_funds = perf_df.nlargest(5, "aum_crore")[["amfi_code", "scheme_name"]].reset_index(drop=True)
selected_codes = top5_funds["amfi_code"].tolist()
selected_names = top5_funds["scheme_name"].tolist()

# Filter NAV data for these 5 funds
nav_filtered = nav_df[nav_df["amfi_code"].isin(selected_codes)].copy()

# Pivot data so each column is a fund's NAV
nav_pivot = nav_filtered.pivot(index="date", columns="amfi_code", values="nav")
nav_pivot.columns = selected_names

# Calculate daily returns and drop missing values
returns = nav_pivot.pct_change().dropna()

# Calculate mean daily returns and covariance matrix
mean_returns = returns.mean()
cov_matrix = returns.cov()

# ── Run Simulation ─────────────────────────────────────────────────────────
results = np.zeros((3 + len(selected_names), NUM_PORTFOLIOS))
np.random.seed(42)

for i in range(NUM_PORTFOLIOS):
    # Generate random weights
    weights = np.random.random(len(selected_names))
    weights /= np.sum(weights)
    
    # Calculate portfolio return and volatility
    # Annualized portfolio return
    portfolio_return = np.sum(mean_returns * weights) * TRADING_DAYS
    # Annualized portfolio volatility
    portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(TRADING_DAYS)
    
    # Calculate Sharpe Ratio
    sharpe_ratio = (portfolio_return - RISK_FREE_RATE) / portfolio_std_dev
    
    # Store results
    results[0, i] = portfolio_return
    results[1, i] = portfolio_std_dev
    results[2, i] = sharpe_ratio
    # Store weights
    for j in range(len(weights)):
        results[3+j, i] = weights[j]

# Create a DataFrame for the results
columns = ['Return', 'Volatility', 'Sharpe'] + selected_names
results_df = pd.DataFrame(results.T, columns=columns)

# Find the portfolio with the maximum Sharpe Ratio
max_sharpe_idx = results_df['Sharpe'].idxmax()
max_sharpe_port = results_df.iloc[max_sharpe_idx]

# Find the portfolio with minimum volatility
min_vol_idx = results_df['Volatility'].idxmin()
min_vol_port = results_df.iloc[min_vol_idx]

# ── Plotting ───────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 8))
plt.scatter(results_df['Volatility'], results_df['Return'], c=results_df['Sharpe'], cmap='viridis', marker='o', s=10, alpha=0.3)
plt.colorbar(label='Sharpe Ratio')

# Plot Max Sharpe Portfolio
plt.scatter(max_sharpe_port['Volatility'], max_sharpe_port['Return'], marker='*', color='r', s=500, label='Maximum Sharpe Ratio')
# Plot Min Volatility Portfolio
plt.scatter(min_vol_port['Volatility'], min_vol_port['Return'], marker='*', color='b', s=500, label='Minimum Volatility')

plt.title('Markowitz Efficient Frontier (5 Funds, 10,000 Portfolios)', fontsize=14, fontweight='bold', color="#0d2d52")
plt.xlabel('Expected Volatility (Annualised Risk)', fontsize=12)
plt.ylabel('Expected Return (Annualised)', fontsize=12)
plt.legend(labelspacing=0.8)
plt.grid(True, alpha=0.3)

# Formatting axes as percentages
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=180, bbox_inches='tight')
print(f"[OK] Chart saved -> {OUT_PATH}")
plt.close()

# ── Print Output ───────────────────────────────────────────────────────────
print("\n-- Markowitz Efficient Frontier Summary --")
print("\nOptimal Portfolio (Maximum Sharpe Ratio):")
print(f"Expected Annual Return:  {max_sharpe_port['Return']:.2%}")
print(f"Expected Volatility:     {max_sharpe_port['Volatility']:.2%}")
print(f"Sharpe Ratio:            {max_sharpe_port['Sharpe']:.2f}")
print("\nOptimal Weights:")
for name in selected_names:
    print(f"  {name}: {max_sharpe_port[name]:.2%}")
