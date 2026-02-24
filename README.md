# 🚚 Logistics Intelligence Engine

An end-to-end cloud-native Data Engineering project implementing Medallion Architecture (Bronze → Silver → Gold) using Google BigQuery and an interactive Streamlit dashboard for analytics and insights.

This project demonstrates real-world ETL design, data modeling, warehouse optimization, feature engineering, and analytics delivery.

---

## 📌 Project Overview

The Logistics Intelligence Engine processes e-commerce logistics data and transforms it into analytics-ready datasets using structured SQL-based ELT pipelines.

The system includes:

- Raw data ingestion (Bronze)
- Data cleaning & feature engineering (Silver)
- Aggregated business metrics (Gold)
- BigQuery ML model training
- Interactive KPI dashboard (Streamlit)

This simulates a production-style data warehouse pipeline.

---

## 🏗 Architecture

### High-Level Flow

┌─────────────────────────────┐


```mermain
flowchart TD

    A["BigQuery Public Dataset<br/>(Orders + Weather Data)"]
    B[Bronze Layer<br/>Raw copy of source tables]
    C["Silver Layer<br/>Cleaned + Feature Engineered<br/>(delay_days, order_date)"]
    D[Gold Layer<br/>Aggregated Analytics Table<br/>Partitioned by order_date]
    E[BigQuery ML Model<br/>Delay Prediction Model]
    F[Streamlit Dashboard<br/>KPI + Interactive SQL UI]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F

```
## 🥉 Bronze Layer

- Raw ingestion from public BigQuery datasets
- No transformations applied
- Serves as reproducible raw data layer

Purpose:
Maintain source-of-truth copy for traceability and auditability.

---

## 🥈 Silver Layer

- Filters completed orders
- Adds engineered features:
  - order_date
  - delay_days
- Cleans and prepares structured data

Purpose:
Transform raw data into analytics-ready structured format.

---

## 🥇 Gold Layer

- Aggregates daily metrics
- Partitioned by order_date
- Optimized for BI queries

Generated KPIs:
- Total Orders
- Average Delay
- Maximum Delay

Purpose:
Enable efficient analytics consumption and dashboard reporting.

---

## 🤖 Machine Learning (BigQuery ML)

A linear regression model is trained to predict shipping delays using aggregated metrics.

Model:

Purpose:
Demonstrate integration between data engineering and ML workflows.

---

## 📊 Streamlit Dashboard Features

- KPI summary metrics
- Order trend visualization
- Delay trend visualization
- Delay distribution histogram
- Date range filtering
- Interactive SQL query builder
- Dynamic aggregation queries

The dashboard reads directly from the Gold layer.

---

## 🛠 Tech Stack

- Google BigQuery (Data Warehouse)
- SQL (Transformations)
- Python
- Streamlit (Dashboard)
- BigQuery ML
- GCP Authentication via gcloud

---

## 📂 Project Structure

---

## 🚀 Setup Instructions

### 1. Clone Repository

### 2. Install Dependencies

### 3. Authenticate with GCP

### 4. Run ETL Pipeline

This creates:
- Bronze tables
- Silver tables
- Gold table
- ML model

### 5. Launch Dashboard
