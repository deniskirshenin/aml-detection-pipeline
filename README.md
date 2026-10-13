# AML Detection Pipeline

A modular, lightweight data pipeline designed for Anti-Money Laundering (AML) analysis and blockchain transaction monitoring. Built following modern architectural standards using Python, SQL, dbt, and DuckDB.

---

## 🏗️ Architecture & Data Flow

The project implements a classic **Kimball dimensional modeling** approach split into three clean transformation layers:

[Alchemy API (Raw Data)]
│
▼
[Staging Layer (stg_)] --> Cleaning, casting, type safety
│
▼
[Intermediate Layer (int_)] --> Unstacked graph transfers (IN/OUT), aggregations
│
▼
[Marts Layer (fct_ / dim_)] --> Fact tables & Wallet Risk Profiles (dim_addresses)

---

## 🛠️ Tech Stack

- **Ingestion:** Python (Alchemy SDK, custom extraction scripts)
- **Transformation:** **dbt (Data Build Tool)** for modular SQL-based modeling
- **Storage & Processing:** **DuckDB** (Blazing-fast analytical processing embedded locally)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```text
aml_dbt/
├── data/
│   └── raw_data.duckdb             # Local embedded analytical database
├── models/
│   ├── staging/               # Cleaned raw data sources
│   │   ├── stg_transfers.sql
│   │   └── schema.yml
│   ├── intermediate/          # Business logic & graph preparation
│   │   ├── int_address_transfers_unstacked.sql
│   │   ├── int_address_summary.sql
│   │   └── schema.yml
│   └── marts/                 # Analytical facts & dimensions
│       ├── fct_transfers.sql
│       ├── dim_addresses.sql
│       └── schema.yml
├── profiles.yml               # dbt connection profiles for DuckDB
└── dbt_project.yml            # dbt project configuration

Key Features & Highlights
Graph-Ready Transformations: The intermediate layer features an unstacked transaction model (int_address_transfers_unstacked) that treats every transaction symmetrically (IN / OUT), enabling high-performance network and cluster analysis.

Wallet Profiling (dim_addresses): Aggregates volumes, unique counterparties, transaction frequencies, and net flows per address to build behavioural profiles.

Risk Heuristics: Automated rule engines embedded directly into the data models to flag high-risk anomalies (e.g., high-frequency volume concentrations).

Roadmap / Next Steps
[ ] Advanced Features: Implement velocity checks (time windows between txs) and smurfing pattern detection.

[ ] Risk Scoring Model: Composite risk score assignment for dim_addresses.

[ ] Orchestration: Wrap ingestion and dbt run into a unified DAG using Makefile / Prefect.
```
