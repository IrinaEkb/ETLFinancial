import pandas as pd

df = pd.read_csv(
"data/processed/humana_financial_metrics.csv"
)

print(
df["metric"].unique()
)