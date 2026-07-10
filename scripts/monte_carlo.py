"""
Bonus Challenge B3 – Monte Carlo NAV Growth Simulation
=======================================================
Simulates 5-year NAV growth for 5 key funds using 1,000 random paths
based on each fund's historical daily return distribution.
Plots 95% / 50% / 5th-percentile confidence bands.

Run from project root:
    python scripts/monte_carlo.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).parent.parent
NAV_PATH  = ROOT / "data" / "processed" / "02_nav_history.csv"
PERF_PATH = ROOT / "data" / "processed" / "07_scheme_performance.csv"
OUT_PATH  = ROOT / "reports" / "monte_carlo_simulation.png"

# ── Simulation Parameters ──────────────────────────────────────────────────
N_SIMULATIONS  = 1_000     # number of random paths per fund
TRADING_DAYS   = 252 * 5   # 5 years of trading days
RANDOM_SEED    = 42

np.random.seed(RANDOM_SEED)

# ── Load data ──────────────────────────────────────────────────────────────
nav_df  = pd.read_csv(NAV_PATH, parse_dates=["date"])
perf_df = pd.read_csv(PERF_PATH)

# Pick the top 5 funds by AUM for simulation
top5 = perf_df.nlargest(5, "aum_crore")[["amfi_code", "scheme_name"]].reset_index(drop=True)

# ── Plot Setup ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle(
    "Monte Carlo NAV Growth Simulation – 5 Years (1,000 Paths per Fund)",
    fontsize=16, fontweight="bold", color="#0d2d52", y=1.02
)
axes = axes.flatten()

BAND_COLORS = {
    "p95": "#d32f2f",
    "p75": "#f57c00",
    "p50": "#1976d2",
    "p25": "#388e3c",
    "p05": "#7b1fa2",
}

all_summary = []

for idx, row in top5.iterrows():
    amfi_code   = row["amfi_code"]
    scheme_name = row["scheme_name"]
    ax          = axes[idx]

    # ── Compute daily returns ─────────────────────────────────────────────
    fund_nav = (
        nav_df[nav_df["amfi_code"] == amfi_code]
        .sort_values("date")
        .copy()
    )
    fund_nav["daily_return"] = fund_nav["nav"].pct_change()
    returns = fund_nav["daily_return"].dropna()

    mu    = returns.mean()       # mean daily return
    sigma = returns.std()        # daily volatility
    S0    = fund_nav["nav"].iloc[-1]   # latest NAV as starting price

    # ── Run Monte Carlo ────────────────────────────────────────────────────
    # Shape: (TRADING_DAYS, N_SIMULATIONS)
    random_shocks = np.random.normal(mu, sigma, (TRADING_DAYS, N_SIMULATIONS))
    # Cumulative product to get price paths
    price_paths = S0 * np.cumprod(1 + random_shocks, axis=0)

    # ── Compute percentile bands ───────────────────────────────────────────
    p05 = np.percentile(price_paths, 5,  axis=1)
    p25 = np.percentile(price_paths, 25, axis=1)
    p50 = np.percentile(price_paths, 50, axis=1)
    p75 = np.percentile(price_paths, 75, axis=1)
    p95 = np.percentile(price_paths, 95, axis=1)

    t = np.arange(TRADING_DAYS)

    # Plot a few sample paths (semi-transparent)
    for i in range(min(80, N_SIMULATIONS)):
        ax.plot(t, price_paths[:, i], color="#b0bec5", alpha=0.12, linewidth=0.5)

    # Fill bands
    ax.fill_between(t, p05, p95, color="#bbdefb", alpha=0.5, label="5th–95th %ile")
    ax.fill_between(t, p25, p75, color="#1976d2", alpha=0.25, label="25th–75th %ile")

    # Median & extremes
    ax.plot(t, p50, color="#1976d2", linewidth=2,   label=f"Median  ₹{p50[-1]:,.0f}")
    ax.plot(t, p95, color="#d32f2f", linewidth=1.5, linestyle="--", label=f"95th    ₹{p95[-1]:,.0f}")
    ax.plot(t, p05, color="#7b1fa2", linewidth=1.5, linestyle="--", label=f"5th     ₹{p05[-1]:,.0f}")
    ax.axhline(S0, color="black", linewidth=1, linestyle=":", alpha=0.6)

    ax.set_title(scheme_name, fontsize=9, fontweight="bold", color="#0d2d52", pad=6)
    ax.set_xlabel("Trading Days", fontsize=8)
    ax.set_ylabel("NAV (₹)", fontsize=8)
    ax.legend(fontsize=7, loc="upper left")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.grid(True, alpha=0.3)

    all_summary.append({
        "scheme_name":    scheme_name,
        "start_nav":      round(S0, 2),
        "median_nav_5yr": round(p50[-1], 2),
        "bull_case_p95":  round(p95[-1], 2),
        "bear_case_p05":  round(p05[-1], 2),
        "annualised_mu":  round(mu * 252 * 100, 2),
        "annualised_vol": round(sigma * np.sqrt(252) * 100, 2),
    })

# ── Remove unused 6th subplot ──────────────────────────────────────────────
axes[5].axis("off")

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=180, bbox_inches="tight")
print(f"[OK] Chart saved -> {OUT_PATH}")
plt.close()

# ── Print summary table ────────────────────────────────────────────────────
summary_df = pd.DataFrame(all_summary)
print("\n-- Monte Carlo 5-Year Simulation Summary --")
print(summary_df.to_string(index=False))
