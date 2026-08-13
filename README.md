# ETL Financial Data Pipeline — Humana

## Project Overview

This project is an automated ETL pipeline that collects financial data for **Humana, Inc.** from the U.S. Securities and Exchange Commission (SEC) XBRL API, transforms and classifies the data using predefined financial business rules, stores the results in PostgreSQL, and generates separate datasets for the three main financial statements:

- Income Statement
- Balance Sheet
- Cash Flow Statement

The main purpose of the project is to automate the collection and organization of financial data so that relevant financial information can be retrieved and analyzed more efficiently.

Instead of manually searching through SEC filings and XBRL facts, the pipeline automatically retrieves the available XBRL data and organizes relevant facts into financial statement categories.

---

## Project Goals

The main goals of the project are:

1. Automatically retrieve Humana's financial data from the SEC.
2. Preserve the original SEC XBRL data.
3. Transform raw XBRL facts into a structured financial dataset.
4. Classify XBRL tags into financial statement metrics using predefined business rules.
5. Store the transformed financial data in PostgreSQL.
6. Separate the data into:
   - Income Statement
   - Balance Sheet
   - Cash Flow Statement
7. Generate dated analytical CSV files for easier downstream analysis.
8. Automate the ETL process using Apache Airflow.
9. Test the ETL components to verify that the pipeline works as expected.

---

# Data Source

## U.S. SEC XBRL Company Facts API

The primary data source is the **U.S. Securities and Exchange Commission (SEC) Company Facts API**.

The pipeline retrieves Humana's XBRL facts from the SEC endpoint:

```
https://data.sec.gov/api/xbrl/companyfacts/CIK{COMPANY_CIK}.json
```

---

# Tools & Technologies

- Python
- Pandas
- Requests
- PostgreSQL
- SQLAlchemy
- Apache Airflow
- Pytest
- Git

---

# Architecture

```
SEC API
   ↓
extract_sec.py
   ↓
data/raw/humana_YYYY_MM_DD.json
   ↓
financial_rules.py
   ↓
generate_mapping.py
   ↓
config/generated_mapping.py
   ↓
transform_financials.py
   ↓
data/processed/humana_financial_metrics_YYYY_MM_DD.csv
   ↓
load_postgres.py
   ↓
PostgreSQL: financial_metrics
      ↑
      │
   storage layer
   │
   └── persistent intermediate data / SQL validation
   ↓
generate_financial_statements.py
   ↓
split by statement
   ↓
period / date / form validation
   ↓
data/analytics/
   ├── income_statement_YYYY_MM_DD.csv
   ├── balance_sheet_YYYY_MM_DD.csv
   └── cash_flow_YYYY_MM_DD.csv
   ```