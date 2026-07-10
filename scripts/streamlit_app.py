import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bluestock MF Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent.parent / "data" / "processed"

# ─────────────────────────────────────────────
# LOAD DATA (cached)
# Verified column names from actual CSVs:
#   06_industry_folio_count: month, total_folios_crore, equity_folios_crore, ...
#   04_monthly_sip_inflows:  month, sip_inflow_crore, sip_aum_lakh_crore, ...
#   05_category_inflows:     month, category, net_inflow_crore
#   03_aum_by_fund_house:    date, fund_house, aum_lakh_crore, aum_crore, num_schemes
#   07_scheme_performance:   amfi_code, scheme_name, fund_house, category, plan,
#                            return_1yr_pct, return_3yr_pct, sharpe_ratio,
#                            std_dev_ann_pct, aum_crore, risk_grade, ...
#   08_investor_transactions: investor_id, transaction_date, amfi_code,
#                             transaction_type, amount_inr, state, city,
#                             city_tier, age_group, gender, ...
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    fund_master  = pd.read_csv(DATA_DIR / "01_fund_master.csv")
    nav_history  = pd.read_csv(DATA_DIR / "02_nav_history.csv", parse_dates=["date"])
    aum_fh       = pd.read_csv(DATA_DIR / "03_aum_by_fund_house.csv")
    sip_inflows  = pd.read_csv(DATA_DIR / "04_monthly_sip_inflows.csv")
    cat_inflows  = pd.read_csv(DATA_DIR / "05_category_inflows.csv")
    folio        = pd.read_csv(DATA_DIR / "06_industry_folio_count.csv")
    performance  = pd.read_csv(DATA_DIR / "07_scheme_performance.csv")
    transactions = pd.read_csv(DATA_DIR / "08_investor_transactions.csv", parse_dates=["transaction_date"])
    holdings     = pd.read_csv(DATA_DIR / "09_portfolio_holdings.csv")
    return fund_master, nav_history, aum_fh, sip_inflows, cat_inflows, folio, performance, transactions, holdings

fund_master, nav_history, aum_fh, sip_inflows, cat_inflows, folio, performance, transactions, holdings = load_data()

# ─────────────────────────────────────────────
# CUSTOM CSS – Bluestock branding
# ─────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] {background: linear-gradient(160deg,#0d1b2a 0%,#1a3a5c 100%);}
    [data-testid="stSidebar"] * {color: #e8f4fd !important;}
    .metric-card {
        background: linear-gradient(135deg,#1a3a5c,#0d2d52);
        border-radius: 12px; padding: 18px 22px; margin-bottom: 12px;
        border-left: 4px solid #00a8e8; color: #fff;
    }
    .metric-value {font-size: 2rem; font-weight: 700; color: #00a8e8;}
    .metric-label {font-size: 0.78rem; color: #93b8d4; text-transform: uppercase; letter-spacing: 1px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.title("📊 Bluestock MF Analytics")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Market Overview", "📈 Fund Performance", "👥 Investor Analytics", "📉 Market Trends"],
    label_visibility="collapsed"
)

# ═══════════════════════════════════════════════════════════
# PAGE 1 – MARKET OVERVIEW
# ═══════════════════════════════════════════════════════════
if page == "🏠 Market Overview":
    st.title("🏠 Market Overview")
    st.caption("Industry-level mutual fund market metrics")

    total_aum      = performance["aum_crore"].sum()
    total_schemes  = len(fund_master)
    total_folios   = folio["total_folios_crore"].sum()      # ✅ correct column
    total_sip      = sip_inflows["sip_inflow_crore"].sum()  # ✅ correct column

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total Industry AUM</div>
            <div class="metric-value">₹{total_aum/100:.1f}T</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total Schemes</div>
            <div class="metric-value">{total_schemes}</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total Folios (Cr)</div>
            <div class="metric-value">{total_folios:.1f} Cr</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total SIP Inflows (Cr)</div>
            <div class="metric-value">₹{total_sip:,.0f}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("AUM by Fund House (Top 10)")
        top_aum = aum_fh.groupby("fund_house")["aum_crore"].sum().nlargest(10).reset_index()
        fig = px.bar(top_aum, x="aum_crore", y="fund_house", orientation="h",
                     color="aum_crore", color_continuous_scale="Blues",
                     labels={"aum_crore": "AUM (₹ Cr)", "fund_house": ""},
                     template="plotly_white")
        fig.update_layout(showlegend=False, coloraxis_showscale=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Schemes by Category")
        cat_count = fund_master["category"].value_counts().reset_index()
        cat_count.columns = ["category", "count"]
        fig = px.pie(cat_count, values="count", names="category",
                     color_discrete_sequence=px.colors.sequential.Blues_r,
                     hole=0.45, template="plotly_white")
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Category-wise Net Inflows")
        # aggregate across all months
        cat_agg = cat_inflows.groupby("category")["net_inflow_crore"].sum().reset_index()
        cat_agg = cat_agg.sort_values("net_inflow_crore", ascending=True)
        fig = px.bar(cat_agg, x="net_inflow_crore", y="category", orientation="h",
                     color="net_inflow_crore", color_continuous_scale="RdYlGn",
                     labels={"net_inflow_crore": "Net Inflow (₹ Cr)", "category": ""},
                     template="plotly_white")
        fig.update_layout(height=380, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Industry Folio Growth")
        folio_sorted = folio.sort_values("month")
        fig = px.area(folio_sorted, x="month", y="total_folios_crore",   # ✅ correct column
                      color_discrete_sequence=["#00a8e8"],
                      labels={"total_folios_crore": "Total Folios (Cr)", "month": ""},
                      template="plotly_white")
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE 2 – FUND PERFORMANCE
# ═══════════════════════════════════════════════════════════
elif page == "📈 Fund Performance":
    st.title("📈 Fund Performance Analytics")

    st.sidebar.markdown("### Filters")
    categories = ["All"] + sorted(performance["category"].dropna().unique().tolist())
    sel_cat = st.sidebar.selectbox("Category", categories)

    risk_grades = ["All"] + sorted(performance["risk_grade"].dropna().unique().tolist())
    sel_risk = st.sidebar.selectbox("Risk Grade", risk_grades)

    perf = performance.copy()
    if sel_cat != "All":
        perf = perf[perf["category"] == sel_cat]
    if sel_risk != "All":
        perf = perf[perf["risk_grade"] == sel_risk]

    st.subheader(f"Risk vs Return Scatter ({len(perf)} funds)")
    fig = px.scatter(
        perf, x="std_dev_ann_pct", y="return_3yr_pct",
        size="aum_crore", color="category",
        hover_name="scheme_name",
        hover_data={"sharpe_ratio": True, "aum_crore": True},
        labels={"std_dev_ann_pct": "Risk (Annualised Std Dev %)", "return_3yr_pct": "3-Year Return %"},
        template="plotly_white", height=440,
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Fund Scorecard")
        scorecard = perf[["scheme_name", "category", "risk_grade", "return_3yr_pct",
                           "sharpe_ratio", "std_dev_ann_pct", "aum_crore"]].copy()
        scorecard.columns = ["Scheme", "Category", "Risk", "Return 3Y%", "Sharpe", "Std Dev%", "AUM (Cr)"]
        st.dataframe(scorecard.sort_values("Sharpe", ascending=False).reset_index(drop=True),
                     use_container_width=True, height=320)

    with col2:
        st.subheader("NAV History")
        nav_schemes = performance["scheme_name"].tolist()
        sel_scheme  = st.selectbox("Select Fund", nav_schemes)
        sel_code    = performance[performance["scheme_name"] == sel_scheme]["amfi_code"].iloc[0]
        nav_data    = nav_history[nav_history["amfi_code"] == sel_code].sort_values("date")
        fig2 = px.line(nav_data, x="date", y="nav",
                       color_discrete_sequence=["#00a8e8"],
                       labels={"nav": "NAV (₹)", "date": ""},
                       template="plotly_white", height=320)
        st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE 3 – INVESTOR ANALYTICS
# ═══════════════════════════════════════════════════════════
elif page == "👥 Investor Analytics":
    st.title("👥 Investor Analytics")

    st.sidebar.markdown("### Filters")
    states     = ["All"] + sorted(transactions["state"].dropna().unique().tolist())
    sel_state  = st.sidebar.selectbox("State", states)
    age_groups = ["All"] + sorted(transactions["age_group"].dropna().unique().tolist())
    sel_age    = st.sidebar.selectbox("Age Group", age_groups)

    tx = transactions.copy()
    if sel_state != "All":
        tx = tx[tx["state"] == sel_state]
    if sel_age != "All":
        tx = tx[tx["age_group"] == sel_age]

    c1, c2, c3, c4 = st.columns(4)
    avg_sip = tx[tx["transaction_type"] == "Sip"]["amount_inr"].mean()
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total Investors</div>
            <div class="metric-value">{tx['investor_id'].nunique():,}</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total Transactions</div>
            <div class="metric-value">{len(tx):,}</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total Amount (Cr)</div>
            <div class="metric-value">₹{tx['amount_inr'].sum()/1e7:,.1f}</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Avg SIP Amount</div>
            <div class="metric-value">₹{avg_sip:,.0f}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transaction Type Split")
        tx_type = tx.groupby("transaction_type")["amount_inr"].sum().reset_index()
        fig = px.pie(tx_type, values="amount_inr", names="transaction_type",
                     hole=0.45, color_discrete_sequence=px.colors.sequential.Blues_r,
                     template="plotly_white", height=340)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Investment by State (Top 15)")
        state_grp = tx.groupby("state")["amount_inr"].sum().nlargest(15).reset_index()
        fig = px.bar(state_grp, y="state", x="amount_inr", orientation="h",
                     color="amount_inr", color_continuous_scale="Blues",
                     labels={"amount_inr": "Amount (₹)", "state": ""},
                     template="plotly_white", height=340)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Avg SIP Amount by Age Group")
        age_sip = tx[tx["transaction_type"] == "Sip"].groupby("age_group")["amount_inr"].mean().reset_index()
        fig = px.bar(age_sip, x="age_group", y="amount_inr",
                     color="amount_inr", color_continuous_scale="Blues",
                     labels={"amount_inr": "Avg SIP (₹)", "age_group": ""},
                     template="plotly_white", height=340)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Monthly Transaction Volume")
        tx["month"] = tx["transaction_date"].dt.to_period("M").astype(str)
        monthly = tx.groupby("month").size().reset_index(name="count")
        fig = px.line(monthly, x="month", y="count",
                      color_discrete_sequence=["#00a8e8"],
                      labels={"count": "Transactions", "month": ""},
                      template="plotly_white", height=340)
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE 4 – MARKET TRENDS
# ═══════════════════════════════════════════════════════════
elif page == "📉 Market Trends":
    st.title("📉 Market Trends")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly SIP Inflows vs AUM")
        sip_sorted = sip_inflows.sort_values("month")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sip_sorted["month"], y=sip_sorted["sip_inflow_crore"],  # ✅ correct column
            name="SIP Inflow (₹ Cr)", marker_color="#00a8e8"))
        fig.add_trace(go.Scatter(
            x=sip_sorted["month"], y=sip_sorted["sip_aum_lakh_crore"],  # ✅ correct column
            name="SIP AUM (Lakh Cr)", yaxis="y2", line=dict(color="#ff7043", width=2)))
        fig.update_layout(
            yaxis=dict(title="SIP Inflow (₹ Cr)"),
            yaxis2=dict(overlaying="y", side="right", title="SIP AUM (Lakh Cr)"),
            template="plotly_white", height=380,
            legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top Categories by Net Inflow")
        cat_agg = cat_inflows.groupby("category")["net_inflow_crore"].sum().nlargest(10).reset_index()
        fig = px.bar(cat_agg, y="category", x="net_inflow_crore", orientation="h",
                     color="net_inflow_crore", color_continuous_scale="RdYlGn",
                     labels={"net_inflow_crore": "Net Inflow (₹ Cr)", "category": ""},
                     template="plotly_white", height=380)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Fund Category vs Risk Grade Heatmap (Avg 3Y Return %)")
    heat_data = performance.groupby(["category", "risk_grade"])["return_3yr_pct"].mean().unstack(fill_value=0)
    fig = px.imshow(heat_data, color_continuous_scale="Blues", aspect="auto",
                    labels=dict(color="Avg 3Y Return %"),
                    template="plotly_white", height=420)
    fig.update_layout(xaxis_title="Risk Grade", yaxis_title="Category")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Rolling 90-Day Sharpe Ratio – Top 5 Funds by AUM")
    top5 = performance.nlargest(5, "aum_crore")[["amfi_code", "scheme_name"]]
    nav_top5 = nav_history[nav_history["amfi_code"].isin(top5["amfi_code"])].copy()
    nav_top5 = nav_top5.sort_values(["amfi_code", "date"])
    nav_top5["daily_return"] = nav_top5.groupby("amfi_code")["nav"].pct_change()

    fig = go.Figure()
    for _, row in top5.iterrows():
        fund_data = nav_top5[nav_top5["amfi_code"] == row["amfi_code"]].set_index("date")
        rolling_sharpe = (
            fund_data["daily_return"].rolling(90).mean() /
            fund_data["daily_return"].rolling(90).std()
        ) * np.sqrt(252)
        fig.add_trace(go.Scatter(x=fund_data.index, y=rolling_sharpe,
                                 name=row["scheme_name"], mode="lines"))
    fig.update_layout(template="plotly_white", height=420,
                      yaxis_title="Annualised Sharpe Ratio",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig, use_container_width=True)
