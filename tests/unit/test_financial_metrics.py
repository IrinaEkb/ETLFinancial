import pandas as pd
from pathlib import Path

from config.generated_mapping import FINANCIAL_MAPPING



PROCESSED_PATH = Path(
    "data/processed"
)


METRICS_FILE = (
    PROCESSED_PATH /
    "humana_financial_metrics.csv"
)



def test_financial_metrics_file_exists():

    assert METRICS_FILE.exists()



def test_financial_metrics_not_empty():

    df = pd.read_csv(
        METRICS_FILE
    )


    assert len(df) > 0



def test_financial_metrics_columns_exist():

    df = pd.read_csv(
        METRICS_FILE
    )


    expected_columns = [

        "metric",
        "source_tag",
        "value",
        "unit",
        "start_date",
        "end_date",
        "filed_date",
        "form"

    ]


    for column in expected_columns:

        assert column in df.columns



def test_metrics_exist_in_financial_mapping():

    df = pd.read_csv(
        METRICS_FILE
    )


    allowed_metrics = set()


    for statement, metrics in FINANCIAL_MAPPING.items():

        for metric_name in metrics.keys():

            allowed_metrics.add(
                metric_name
            )


    created_metrics = set(
        df["metric"]
    )


    unknown_metrics = (
        created_metrics -
        allowed_metrics
    )


    assert not unknown_metrics, (
        f"Unknown metrics: {unknown_metrics}"
    )



def test_source_tags_exist_in_financial_mapping():

    df = pd.read_csv(
        METRICS_FILE
    )


    allowed_tags = set()


    for statement, metrics in FINANCIAL_MAPPING.items():

        for metric_name, tags in metrics.items():

            for item in tags:

                allowed_tags.add(
                    item["tag"]
                )


    created_tags = set(
        df["source_tag"]
    )


    unknown_tags = (
        created_tags -
        allowed_tags
    )


    assert not unknown_tags, (
        f"Unknown tags: {unknown_tags}"
    )



def test_financial_metrics_have_values():

    df = pd.read_csv(
        METRICS_FILE
    )


    required_columns = [

        "metric",
        "source_tag",
        "value"

    ]


    for column in required_columns:

        assert df[column].notna().all()



def test_financial_values_are_numeric():

    df = pd.read_csv(
        METRICS_FILE
    )


    numeric = pd.to_numeric(
        df["value"],
        errors="coerce"
    )


    assert numeric.notna().all()