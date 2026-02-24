import streamlit as st
from google.cloud import bigquery
import pandas as pd
import yaml
import plotly.express as px
import time

# ---------------- Config ----------------
with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

PROJECT_ID = config["project_id"]
DATASET_ID = config["dataset_id"]

client = bigquery.Client(project=PROJECT_ID)

st.set_page_config(page_title="Logistics Intelligence", layout="wide")
st.title("🚚 Logistics Intelligence Dashboard")

# ---------------- Load Gold Data ----------------
@st.cache_data
def load_data():
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET_ID}.gold_logistics_master`
    """
    return client.query(query).to_dataframe()

df = load_data()

# ---------------- Filters ----------------
st.sidebar.header("📅 Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["order_date"].min(), df["order_date"].max()]
)

df_filtered = df[
    (df["order_date"] >= pd.to_datetime(date_range[0])) &
    (df["order_date"] <= pd.to_datetime(date_range[1]))
]

# ---------------- KPIs ----------------
st.header("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", f"{df_filtered['total_orders'].sum():,}")
col2.metric("Average Delay", f"{df_filtered['avg_delay'].mean():.2f} days")
col3.metric("Max Delay", f"{df_filtered['avg_delay'].max():.2f} days")

# ---------------- Charts ----------------
st.header("📈 Order Trend")

fig_orders = px.line(
    df_filtered,
    x="order_date",
    y="total_orders",
    title="Orders Over Time"
)
st.plotly_chart(fig_orders, use_container_width=True)

st.header("📉 Delay Trend")

fig_delay = px.line(
    df_filtered,
    x="order_date",
    y="avg_delay",
    title="Average Delay Over Time"
)
st.plotly_chart(fig_delay, use_container_width=True)

# ---------------- Distribution ----------------
st.header("📊 Delay Distribution")

fig_hist = px.histogram(
    df_filtered,
    x="avg_delay",
    nbins=30,
    title="Distribution of Average Delay"
)
st.plotly_chart(fig_hist, use_container_width=True)

# ==========================================================
# 🧠 ADVANCED INTERACTIVE QUERY SECTION (NEW)
# ==========================================================

st.sidebar.markdown("---")
st.sidebar.header("🧠 Advanced SQL Explorer")



# Proper mapping
layer_mapping = {
    "Gold Layer": "gold_logistics_master",
    "Silver Layer": "silver_orders",
    "Bronze Layer": "bronze_orders"
}

# Select label
layer_label = st.sidebar.selectbox(
    "Select Data Layer",
    list(layer_mapping.keys())
)

# Get actual table name
selected_table = layer_mapping[layer_label]
full_table_name = f"`{PROJECT_ID}.{DATASET_ID}.{selected_table}`"

st.sidebar.markdown("You can write SQL without worrying about project or dataset name.")

default_query = f"SELECT * FROM {full_table_name} LIMIT 100"

user_query = st.sidebar.text_area(
    "Write SQL Query",
    value=default_query,
    height=200
)




# Initialize session state
if "df_result" not in st.session_state:
    st.session_state.df_result = None

if st.sidebar.button("Run Custom Query"):

    try:
        forbidden_keywords = ["DELETE", "DROP", "TRUNCATE", "UPDATE", "INSERT"]
        if any(word in user_query.upper() for word in forbidden_keywords):
            st.error("Destructive queries are not allowed.")
        else:
            start_time = time.time()

            job_config = bigquery.QueryJobConfig(
                maximum_bytes_billed=10**9
            )

            query_job = client.query(user_query, job_config=job_config)
            df_result = query_job.to_dataframe()

            end_time = time.time()
            execution_time = round(end_time - start_time, 2)

            # Store in session state
            st.session_state.df_result = df_result
            st.session_state.execution_time = execution_time

    except Exception as e:
        st.error(f"Query Failed: {e}")

# ---------------- DISPLAY RESULT ----------------

if st.session_state.df_result is not None:

    st.subheader("📋 Query Result")
    st.success(f"Query executed in {st.session_state.execution_time} seconds")
    st.write(f"Rows returned: {len(st.session_state.df_result)}")

    st.dataframe(st.session_state.df_result)

    numeric_cols = st.session_state.df_result.select_dtypes(include=['number']).columns.tolist()

    if len(st.session_state.df_result.columns) >= 2 and numeric_cols:

        st.subheader("📈 Quick Chart")

        col1, col2 = st.columns(2)

        with col1:
            x_axis = st.selectbox("Select X-axis", st.session_state.df_result.columns)

        with col2:
            y_axis = st.selectbox("Select Y-axis (Numeric Only)", numeric_cols)

        fig = px.line(st.session_state.df_result, x=x_axis, y=y_axis)
        st.plotly_chart(fig, use_container_width=True)



# ---------------- Footer ----------------

st.markdown("---")
st.markdown("Data Engineering ETL Validation Portal • Built with BigQuery & Streamlit")