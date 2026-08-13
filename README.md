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