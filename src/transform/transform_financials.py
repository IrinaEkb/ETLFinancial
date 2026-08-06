# Reads:
# - data/raw/humana_YYYY_MM_DD.json
# - config/generated_mapping.py
#
# Creates:
# - data/processed/humana_financial_metrics_YYYY_MM_DD.csv


from datetime import datetime
import json
from pathlib import Path

import pandas as pd

from config.settings import PROCESSED_PATH
from utils.generate_mapping import get_latest_raw_file



def run_transform(input_file=None):

    from config.generated_mapping import FINANCIAL_MAPPING


    if input_file is None:
        input_file = get_latest_raw_file()


    input_file = Path(input_file)


    if not input_file.exists():
        raise FileNotFoundError(
            f"File not found: {input_file}"
        )


    print(
        f"Using raw file: {input_file}"
    )


    with open(input_file, "r") as f:
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
                    {}
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


    processed_path = Path(
        PROCESSED_PATH
    )


    processed_path.mkdir(
        parents=True,
        exist_ok=True
    )


    today = datetime.today().strftime(
        "%Y_%m_%d"
    )


    output_file = (
        processed_path
        /
        f"humana_financial_metrics_{today}.csv"
    )


    financial_metrics_df.to_csv(
        output_file,
        index=False
    )



    print(
        f"\nSaved {len(financial_metrics_df)} rows to {output_file}"
    )


    print(
        "\n========== DATA QUALITY CHECKS =========="
    )


    print(
        f"Total rows: {len(financial_metrics_df)}"
    )


    print(
        f"Unique metrics: {financial_metrics_df['metric'].nunique()}"
    )


    duplicates = (
        financial_metrics_df
        .duplicated()
        .sum()
    )

    duplicate_tags = (
    financial_metrics_df
    .groupby("source_tag")["metric"]
    .nunique()
)

    print(duplicate_tags[duplicate_tags > 1])


    print(
        f"Duplicate rows: {duplicates}"
    )


    print(
        "\nMissing values by column:"
    )


    print(
        financial_metrics_df
        .isna()
        .sum()
    )



    return output_file





if __name__ == "__main__":

    run_transform()