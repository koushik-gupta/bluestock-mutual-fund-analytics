-- 1. Top 5 funds by AUM
SELECT scheme_name, aum_crore, category 
FROM fact_performance 
ORDER BY aum_crore DESC 
LIMIT 5;

-- 2. Average NAV per month for SBI Bluechip Fund
SELECT strftime('%Y-%m', date) as month, AVG(nav) as avg_nav 
FROM fact_nav 
WHERE amfi_code = 119551
GROUP BY month 
ORDER BY month;

-- 3. Total SIP amount grouped by State
SELECT state, SUM(amount_inr) as total_sip_amount 
FROM fact_transactions 
WHERE transaction_type = 'SIP' 
GROUP BY state 
ORDER BY total_sip_amount DESC;

-- 4. Funds with expense ratio less than 1%
SELECT amfi_code, scheme_name, expense_ratio_pct 
FROM dim_fund 
WHERE expense_ratio_pct < 1.0 
ORDER BY expense_ratio_pct ASC;

-- 5. Best performing funds in Large Cap (1yr return)
SELECT scheme_name, return_1yr_pct 
FROM fact_performance 
WHERE category = 'Large Cap' 
ORDER BY return_1yr_pct DESC 
LIMIT 5;

-- 6. Count of investors by Age Group
SELECT age_group, COUNT(DISTINCT investor_id) as investor_count 
FROM fact_transactions 
GROUP BY age_group 
ORDER BY investor_count DESC;

-- 7. Monthly SIP Inflows Trend over the years
SELECT month, SUM(amount_inr) as total_inflows 
FROM fact_transactions 
WHERE transaction_type = 'SIP'
GROUP BY month 
ORDER BY month;

-- 8. Transaction types distribution
SELECT transaction_type, COUNT(*) as tx_count, SUM(amount_inr) as total_amount 
FROM fact_transactions 
GROUP BY transaction_type;

-- 9. KYC Status overview
SELECT kyc_status, COUNT(DISTINCT investor_id) as unique_investors 
FROM fact_transactions 
GROUP BY kyc_status;

-- 10. Average Sharpe Ratio by Category
SELECT category, AVG(sharpe_ratio) as avg_sharpe 
FROM fact_performance 
GROUP BY category 
ORDER BY avg_sharpe DESC;
