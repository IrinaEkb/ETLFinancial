# Reads:
# - data/raw/humana.json
# - config/generated_mapping.py

# Creates:
# data/processed/humana_financial_metrics.csv

# The dataset contains only classified financial metrics:
# Balance Sheet,
# Income Statement,
# Cash Flow items.

import json
from pathlib import Path

import pandas as pd

from config.generated_mapping import FINANCIAL_MAPPING
from config.settings import RAW_PATH, PROCESSED_PATH


input_file = Path(RAW_PATH) / "humana.json"

with open(input_file) as f:
    data = json.load(f)


gaap = data["facts"]["us-gaap"]


financial_metrics = []


for statement, metrics in FINANCIAL_MAPPING.items():

    for metric_name, tags in metrics.items():

        for tag_info in tags:

            tag = tag_info["tag"]

            if tag not in gaap:
                continue

            units = gaap[tag].get(
                "units",
                {},
            )

            for unit_name, values in units.items():

                for item in values:

                    financial_metrics.append(
                        {
                            "metric": metric_name,
                            "source_tag": tag,
                            "value": item.get("val"),
                            "unit": unit_name,
                            "start_date": item.get("start"),
                            "end_date": item.get("end"),
                            "filed_date": item.get("filed"),
                            "form": item.get("form"),
                        }
                    )


financial_metrics_df = pd.DataFrame(
    financial_metrics
)

processed_path = Path(PROCESSED_PATH)

processed_path.mkdir(
    parents=True,
    exist_ok=True,
)

financial_metrics_df.to_csv(
    processed_path /
    "humana_financial_metrics.csv",
    index=False,
)

print(
    f"Saved "
    f"{len(financial_metrics_df)} "
    f"rows to "
    f"humana_financial_metrics.csv"
)