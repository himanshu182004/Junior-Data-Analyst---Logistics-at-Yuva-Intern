import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Logistics Analytics Dashboard", layout="wide")

# 1. Generate Mock Logistics Data
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
    data = pd.DataFrame({
        'Date': np.random.choice(dates, 1000),
        'Carrier': np.random.choice(['FedEx', 'UPS', 'DHL', 'USPS', 'XPO Logistics'], 1000),
        'Origin': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'], 1000),
        'Destination': np.random.choice(['Dallas', 'Seattle', 'Atlanta', 'Denver', 'Boston'], 1000),
        'Shipping_Cost': np.random.normal(loc=150, scale=40, size=1000).round(2),
        'Delivery_Time_Days': np.random.normal(loc=4, scale=1.5, size=1000).round(1),
        'Status': np.random.choice(['On Time', 'Delayed', 'Damaged'], 1000, p=[0.85, 0.12, 0.03])
    })
    return data

df = load_data()

# 2. Dashboard Header & KPIs
st.title("📦 Logistics Performance Dashboard")
st.markdown("Monitor key supply chain metrics, carrier performance, and delivery trends.")

# Calculate KPIs
total_shipments = len(df)
otd_rate = (len(df[df['Status'] == 'On Time']) / total_shipments) * 100
avg_cost = df['Shipping_Cost'].mean()
avg_delivery_time = df['Delivery_Time_Days'].mean()

# Render KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Shipments", f"{total_shipments:,}")
col2.metric("On-Time Delivery Rate", f"{otd_rate:.1f}%")
col3.metric("Avg Cost per Shipment", f"${avg_cost:.2f}")
col4.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} Days")

st.markdown("---")

# 3. Visualizations
col_charts1, col_charts2 = st.columns(2)

with col_charts1:
    # Trend Analysis: Costs over time
    st.subheader("Monthly Shipping Cost Trends")
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly_costs = df.groupby('Month')['Shipping_Cost'].sum().reset_index()
    fig_line = px.line(monthly_costs, x='Month', y='Shipping_Cost', markers=True, title="Total Freight Spend by Month")
    st.plotly_chart(fig_line, use_container_width=True)

with col_charts2:
    # Carrier Performance: Stacked Bar Chart
    st.subheader("Carrier Performance (Delivery Status)")
    carrier_status = df.groupby(['Carrier', 'Status']).size().reset_index(name='Count')
    fig_bar = px.bar(carrier_status, x='Carrier', y='Count', color='Status', 
                     title="Volume and Delay Breakdown by Carrier",
                     color_discrete_map={'On Time':'#2ECC71', 'Delayed':'#F1C40F', 'Damaged':'#E74C3C'})
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# 4. Detailed Data View
st.subheader("High-Risk/Delayed Shipments Feed")
delayed_shipments = df[df['Status'] != 'On Time'].sort_values(by='Date', ascending=False)
st.dataframe(delayed_shipments[['Date', 'Carrier', 'Origin', 'Destination', 'Shipping_Cost', 'Status']].head(10), use_container_width=True)