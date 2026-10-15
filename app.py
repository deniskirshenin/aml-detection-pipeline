import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="AML monitoring dashboard", page_icon="🛡️", layout="wide")

@st.cache_resource
def load_data():
    # Connect to DuckDB and load the data
    con = duckdb.connect('data/raw_data.duckdb', read_only=True)
    return con

con = load_data()

st.title("🛡️ AML Transaction & Wallet Monitoring Dashboard")
st.markdown("Modern Data Stack demo: DuckDB + dbt + Streamlit for Blockchain Analytics.")

# Sidebar filters
st.sidebar.header("Filters")
risk_filter = st.sidebar.selectbox("Filter by Risk Level", ["ALL", "HIGH", "MEDIUM", "LOW"])

# Query the data based on the selected filter
query = "SELECT * FROM main.dim_addresses_enriched"
if risk_filter != "ALL":
    query += f" WHERE risk_level = '{risk_filter}'"

df_addresses = con.execute(query).fetchdf()

# Display metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Monitored Addresses", len(df_addresses))
high_risk_count = len(df_addresses[df_addresses['risk_level'] == 'HIGH']) if 'risk_level' in df_addresses.columns else 0
col2.metric("High Risk Wallets", high_risk_count, delta_color="inverse")
col3.metric("High Velocity Bursts", int(df_addresses['is_high_velocity_burst'].sum()) if 'is_high_velocity_burst' in df_addresses.columns else 0)
col4.metric("Potential Structuring", int(df_addresses['is_potential_structuring'].sum()) if 'is_potential_structuring' in df_addresses.columns else 0)

st.divider()

# Display the data table
st.subheader("📋 Wallet Risk Profiles & AML Scores")
if not df_addresses.empty:
    st.dataframe(df_addresses, use_container_width=True)
else:
    st.info("No addresses match the selected filter.")

# Display the risk score distribution chart
st.subheader("📊 Risk Score Distribution")
if 'aml_risk_score' in df_addresses.columns and not df_addresses.empty:
    st.bar_chart(df_addresses['aml_risk_score'])
    