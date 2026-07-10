# Bluestock Mutual Fund Analytics Capstone

This repository contains the full end-to-end data pipeline, analytical notebooks, Power BI dashboard, and interactive Web Application developed for the **Bluestock Mutual Fund Analytics Capstone Project**.

## 📂 Project Structure
- `data/` - Raw datasets, processed CSVs, and the SQLite database (`bluestock_mf.db`).
- `notebooks/` - Jupyter notebooks detailing EDA, Performance Analytics, and Advanced Risk Metrics.
- `scripts/` - Python scripts for ETL pipelines, live NAV fetching, quantitative metric computation, and the Streamlit app.
- `sql/` - Database schemas and data validation queries.
- `Power_BI/` - The final interactive Power BI dashboard (`.pbix`).
- `reports/` - Output charts, the final PDF report, automated HTML emails, and the presentation deck.

## 🚀 Key Deliverables Completed
- **Data Engineering:** Fully automated ETL pipeline using Python, Pandas, and SQLite, managed by a cron scheduler.
- **Data Analysis:** Exploratory Data Analysis identifying key retail investment and demographic trends.
- **Risk Analytics:** Quantitative metric calculations including CAGR, Sharpe Ratio, Beta, VaR, and CVaR.
- **Business Intelligence:** A 4-page interactive Power BI dashboard featuring dynamic slicers, drill-throughs, and heatmaps.
- **Bonus Challenges Achieved:** 
  - Deployed a fully interactive self-service **Streamlit Web Application**.
  - Built an AI-driven **Fund Recommender System** matching investors to funds based on risk appetite.
  - Implemented advanced **Markowitz Efficient Frontier** portfolio optimization.
  - Conducted **Monte Carlo Simulations** for 5-year NAV forecasting.
  - Developed a script to generate and send **Automated Weekly HTML Email Reports**.

## ⚙️ How to Run Locally

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Run the Interactive Web App (Streamlit)**
```bash
streamlit run scripts/streamlit_app.py
```

**3. Run the Automated ETL Pipeline**
```bash
python scripts/run_scheduler.py
```
