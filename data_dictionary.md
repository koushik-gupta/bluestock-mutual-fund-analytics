# Data Dictionary

## 1. dim_fund (01_fund_master.csv)
- **amfi_code** (Integer): Unique identifier for the mutual fund scheme as per AMFI.
- **fund_house** (Text): Name of the AMC (Asset Management Company).
- **scheme_name** (Text): Full name of the mutual fund scheme.
- **category** (Text): Primary asset class (e.g., Equity, Debt).
- **sub_category** (Text): Specific category as per SEBI (e.g., Large Cap, Small Cap).
- **plan** (Text): Regular or Direct plan.
- **launch_date** (Date): Inception date of the scheme.
- **benchmark** (Text): The index against which the fund's performance is measured.
- **expense_ratio_pct** (Float): Annual fee charged by the fund house as a percentage of AUM.
- **exit_load_pct** (Float): Fee charged if redeemed before a specified period.
- **min_sip_amount** (Integer): Minimum amount required to start a SIP.
- **min_lumpsum_amount** (Integer): Minimum amount required for a lump sum investment.
- **fund_manager** (Text): Name of the primary fund manager.
- **risk_category** (Text): Risk level (e.g., Low, Moderate, Very High).
- **sebi_category_code** (Text): Regulatory classification code.

## 2. fact_nav (02_nav_history.csv)
- **amfi_code** (Integer): Foreign key referencing dim_fund.
- **date** (Date): The date of the NAV.
- **nav** (Float): Net Asset Value per unit on the given date.

## 3. fact_transactions (08_investor_transactions.csv)
- **investor_id** (Text): Unique identifier for the investor.
- **transaction_date** (Date): Date the transaction was executed.
- **amfi_code** (Integer): Foreign key referencing dim_fund.
- **transaction_type** (Text): Type of transaction (SIP, Lumpsum, Redemption).
- **amount_inr** (Float): Transaction amount in Indian Rupees.
- **state** (Text): State of residence of the investor.
- **city** (Text): City of residence of the investor.
- **city_tier** (Text): Classification of the city (T30 = Top 30, B30 = Beyond 30).
- **age_group** (Text): Age bracket of the investor.
- **gender** (Text): Gender of the investor.
- **annual_income_lakh** (Float): Annual income of the investor in Lakhs INR.
- **payment_mode** (Text): Method of payment (e.g., UPI, Net Banking).
- **kyc_status** (Text): KYC verification status (Verified, Pending, Rejected).

## 4. fact_performance (07_scheme_performance.csv)
- **amfi_code** (Integer): Primary key for the scheme.
- **return_1yr_pct**, **return_3yr_pct**, **return_5yr_pct** (Float): Historical annualized returns.
- **alpha** (Float): Excess return relative to the benchmark.
- **beta** (Float): Measure of volatility against the market.
- **sharpe_ratio** (Float): Risk-adjusted return metric.
- **aum_crore** (Float): Assets Under Management in Crores.
