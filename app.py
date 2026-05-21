import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Silver Bank - Security Intelligence",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; color: #00D4FF; font-weight: bold; }
    .metric-card { background: #1E1E1E; padding: 20px; border-radius: 10px; border: 1px solid #333; }
    .metric-value { font-size: 2rem; color: white; font-weight: bold; }
    .metric-label { color: #888; font-size: 0.9rem; }
    .ghost-badge { background: #00D4FF; color: black; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ===================== DATA GENERATION =====================
@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    
    # Generate 500 ghost mode triggers across SA
    n = 500
    cities = {
        "Johannesburg": (-26.2041, 28.0473),
        "Soweto": (-26.2485, 27.8580),
        "Pretoria": (-25.7479, 28.2293),
        "Cape Town": (-33.9249, 18.4241),
        "Khayelitsha": (-34.0397, 18.6770),
        "Durban": (-29.8587, 31.0218),
        "Port Elizabeth": (-33.9608, 25.6022),
        "Bloemfontein": (-29.1183, 26.2290),
        "Polokwane": (-23.8962, 29.4484),
        "Rustenburg": (-25.6673, 27.2402),
        "Nelspruit": (-25.4747, 30.9682),
        "Kimberley": (-28.7282, 24.7492)
    }
    
    data = []
    for _ in range(n):
        city = random.choice(list(cities.keys()))
        lat, lon = cities[city]
        # Add random offset to spread points
        lat += np.random.normal(0, 0.05)
        lon += np.random.normal(0, 0.05)
        
        amount = np.random.choice([5000, 10000, 15000, 20000, 50000, 100000], p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03])
        bank = np.random.choice(["Standard Bank", "Capitec", "FNB", "Absa", "Nedbank"], p=[0.4, 0.2, 0.2, 0.1, 0.1])
        hour = np.random.randint(0, 24)
        day = np.random.randint(0, 30)
        resolved = np.random.choice([True, False], p=[0.85, 0.15])
        risk_score = np.random.randint(30, 95)
        
        data.append({
            "lat": lat,
            "lon": lon,
            "city": city,
            "amount": amount,
            "bank": bank,
            "hour": hour,
            "day": day,
            "resolved": resolved,
            "risk_score": risk_score,
            "date": datetime.now() - timedelta(days=random.randint(0, 30))
        })
    
    df = pd.DataFrame(data)
    
    # Revenue data
    months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6", 
              "Month 7", "Month 8", "Month 9", "Month 10", "Month 11", "Month 12"]
    users = [10000, 25000, 50000, 100000, 200000, 400000, 700000, 1000000, 1300000, 1600000, 1800000, 2000000]
    subscriptions = [u * 0.6 for u in users]
    hardware_sales = [u * 0.25 for u in users]
    data_sales = [u * 0.15 for u in users]
    
    revenue_df = pd.DataFrame({
        "Month": months,
        "Subscribers": users,
        "Subscription_Revenue": [u * 29 for u in subscriptions],
        "Hardware_Revenue": [u * 199 * 0.25 for u in users],
        "Data_Revenue": [u * 15 for u in users]
    })
    revenue_df["Total_Revenue"] = revenue_df["Subscription_Revenue"] + revenue_df["Hardware_Revenue"] + revenue_df["Data_Revenue"]
    
    # Switching data
    banks = ["Standard Bank", "FNB", "Capitec", "Absa", "Nedbank"]
    safety_scores = [9.8, 6.2, 5.4, 5.0, 5.8]
    switching_intent = [67, 23, 18, 12, 15]
    nps = [45, 5, 3, -2, 4]
    
    switching_df = pd.DataFrame({
        "Bank": banks,
        "Safety_Score": safety_scores,
        "Switching_Intent": switching_intent,
        "NPS": nps
    })
    
    return df, revenue_df, switching_df

df, revenue_df, switching_df = generate_mock_data()

# ===================== SIDEBAR =====================
st.sidebar.image("https://img.icons8.com/fluency/96/ghost.png", width=80)
st.sidebar.title("👻 Silver Bank")
st.sidebar.markdown("**Security Intelligence Platform**")
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

# Date filter
date_range = st.sidebar.date_input("Date Range", [datetime.now() - timedelta(days=30), datetime.now()])

# City filter
cities = ["All"] + list(df['city'].unique())
city_filter = st.sidebar.selectbox("City", cities)

# Bank filter
banks = ["All"] + list(df['bank'].unique())
bank_filter = st.sidebar.selectbox("Bank", banks)

# Filter data
filtered_df = df.copy()
if city_filter != "All":
    filtered_df = filtered_df[filtered_df['city'] == city_filter]
if bank_filter != "All":
    filtered_df = filtered_df[filtered_df['bank'] == bank_filter]

# ===================== MAIN TABS =====================
tab1, tab2, tab3 = st.tabs(["🌍 Ghost Heatmap", "💰 Revenue & Adoption", "🏆 Customer Diversion"])

# ===================== TAB 1: HEATMAP =====================
with tab1:
    st.markdown('<div class="main-title">🌍 Ghost Mode Incident Heatmap</div>', unsafe_allow_html=True)
    st.markdown("*Real-time hijacking & robbery risk data for insurers, SAPS, and urban planners.*")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", len(filtered_df), delta="+12% this month")
    with col2:
        total_saved = filtered_df['amount'].sum()
        st.metric("Money Saved (Ghost Mode)", f"R{total_saved:,.0f}", delta="R1.2M this week")
    with col3:
        resolved_rate = (filtered_df['resolved'].sum() / len(filtered_df)) * 100
        st.metric("Resolution Rate", f"{resolved_rate:.1f}%", delta="+3%")
    with col4:
        avg_risk = filtered_df['risk_score'].mean()
        st.metric("Avg Risk Score", f"{avg_risk:.0f}/100", delta="+5%")
    
    st.markdown("---")
    
    # Heatmap Map
    st.subheader("📍 Incident Locations")
    
    # Color by bank or risk
    map_color = st.radio("Color by:", ["Bank", "Risk Score"], horizontal=True)
    
    if map_color == "Bank":
        fig = px.scatter_mapbox(
            filtered_df,
            lat="lat",
            lon="lon",
            size="amount",
            color="bank",
            hover_name="city",
            hover_data={"amount": ":R{:.0f}", "risk_score": True},
            zoom=6,
            height=500,
            title="Ghost Mode Triggers by Bank"
        )
    else:
        fig = px.scatter_mapbox(
            filtered_df,
            lat="lat",
            lon="lon",
            size="amount",
            color="risk_score",
            color_continuous_scale="Reds",
            hover_name="city",
            hover_data={"amount": ":R{:.0f}", "bank": True},
            zoom=6,
            height=500,
            title="Ghost Mode Triggers by Risk Score"
        )
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox_zoom=6,
        mapbox_center={"lat": -28.5, "lon": 25.5},
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Risk Analysis
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏙️ Risk by City")
        city_risk = filtered_df.groupby('city')['risk_score'].mean().sort_values(ascending=False)
        fig2 = px.bar(
            city_risk,
            x=city_risk.values,
            y=city_risk.index,
            orientation='h',
            color=city_risk.values,
            color_continuous_scale="Reds",
            title="Average Risk Score by City"
        )
        fig2.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("🕐 Risk by Hour")
        hour_risk = filtered_df.groupby('hour')['risk_score'].mean()
        fig3 = px.line(
            hour_risk,
            x=hour_risk.index,
            y=hour_risk.values,
            title="Average Risk Score by Hour of Day",
            markers=True
        )
        fig3.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    st.info("💡 *This data is anonymized and sold to insurance partners (Santam, Old Mutual, Discovery) and SAPS for R18M/year.*")

# ===================== TAB 2: REVENUE & ADOPTION =====================
with tab2:
    st.markdown('<div class="main-title">💰 Revenue & Adoption Dashboard</div>', unsafe_allow_html=True)
    st.markdown("*Projected ROI for Standard Bank executives.*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_revenue_12m = revenue_df['Total_Revenue'].sum()
        st.metric("Projected Year 1 Revenue", f"R{total_revenue_12m:,.0f}", delta="+15% month-over-month")
    with col2:
        total_users_12m = revenue_df['Subscribers'].iloc[-1]
        st.metric("Projected Users (Month 12)", f"{total_users_12m:,.0f}", delta="2M target")
    with col3:
        savings = 280_000_000  # R280M saved from hijackings
        st.metric("Annual Cost Savings", f"R{savings:,.0f}", delta="From reduced hijackings")
    
    st.markdown("---")
    
    # Revenue breakdown
    st.subheader("📊 Revenue Mix (Year 1)")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart
        total_sub = revenue_df['Subscription_Revenue'].sum()
        total_hw = revenue_df['Hardware_Revenue'].sum()
        total_data = revenue_df['Data_Revenue'].sum()
        
        fig4 = px.pie(
            names=["Subscriptions (Vimba Shield/Armor)", "Hardware Sales (Bracelets/Watches)", "Data Sales (Insurers)"],
            values=[total_sub, total_hw, total_data],
            hole=0.4,
            title="Revenue Breakdown"
        )
        fig4.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # Growth chart
        fig5 = px.area(
            revenue_df,
            x="Month",
            y="Total_Revenue",
            title="Monthly Revenue Growth (R)",
            color_discrete_sequence=["#00D4FF"]
        )
        fig5.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
        st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("---")
    
    # User growth
    st.subheader("📈 User Adoption Forecast")
    fig6 = px.line(
        revenue_df,
        x="Month",
        y="Subscribers",
        title="Projected Silver Bank Users",
        markers=True,
        color_discrete_sequence=["#00FF88"]
    )
    fig6.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
    st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("---")
    st.success("✅ *R600M annual subscription revenue + R280M cost savings = R880M total value to Standard Bank.*")

# ===================== TAB 3: CUSTOMER DIVERSION =====================
with tab3:
    st.markdown('<div class="main-title">🏆 Customer Diversion Dashboard</div>', unsafe_allow_html=True)
    st.markdown("*Why Standard Bank becomes the safest bank in the world.*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Safety Index Score (Standard Bank + Silver Bank)", "9.8 / 10", delta="Rank #1")
        st.metric("Competitor Average Safety Score", "5.6 / 10", delta="-4.2 vs Standard Bank")
    with col2:
        st.metric("Switching Intent (Non-Standard Customers)", "67%", delta="Would switch to Standard Bank")
        st.metric("Projected New Customers (Year 1)", "1,500,000", delta="From competitors")
    
    st.markdown("---")
    
    # Safety score comparison
    st.subheader("🔒 Safety Score by Bank")
    fig7 = px.bar(
        switching_df,
        x="Bank",
        y="Safety_Score",
        color="Safety_Score",
        color_continuous_scale="Blues",
        text="Safety_Score",
        title="Bank Safety Index (With Silver Bank vs Without)"
    )
    fig7.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
    st.plotly_chart(fig7, use_container_width=True)
    
    # Switching intent
    st.subheader("🔄 Customer Switching Intent")
    fig8 = px.bar(
        switching_df,
        x="Bank",
        y="Switching_Intent",
        color="Switching_Intent",
        color_continuous_scale="Greens",
        text="Switching_Intent",
        title="% of Customers Who Would Switch to Standard Bank for Ghost Mode"
    )
    fig8.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
    st.plotly_chart(fig8, use_container_width=True)
    
    # NPS
    st.subheader("📊 Net Promoter Score (NPS) Comparison")
    fig9 = px.bar(
        switching_df,
        x="Bank",
        y="NPS",
        color="NPS",
        color_continuous_scale="RdYlGn",
        text="NPS",
        title="NPS: Standard Bank vs Competitors"
    )
    fig9.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="white")
    st.plotly_chart(fig9, use_container_width=True)
    
    st.markdown("---")
    st.success("🔥 *1.5M new customers × R10,000 avg deposit = R15B in new deposits. Standard Bank becomes the safest bank in Africa.*")

# ===================== FOOTER =====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8rem;">
    👻 Silver Bank Security Intelligence Platform | Built for Standard Bank & BBD Hackathon<br>
    Data simulated for demo purposes. 
</div>
""", unsafe_allow_html=True)
