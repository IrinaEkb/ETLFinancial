
import json
from pathlib import Path

from config.generated_mapping import FINANCIAL_MAPPING


RAW_PATH = Path("data/raw")



def test_financial_mapping_exists():

    assert FINANCIAL_MAPPING



def test_mapping_has_statements():

    expected = {
        "balance_sheet",
        "income_statement",
        "cash_flow"
    }


    actual = set(
        FINANCIAL_MAPPING.keys()
    )


    missing = expected - actual


    assert not missing, (
        f"Missing statements: {missing}"
    )



def test_mapping_metrics_are_not_empty():

    for statement, metrics in FINANCIAL_MAPPING.items():

        assert metrics, (
            f"{statement} has no metrics"
        )



def test_mapping_metrics_have_tags():

    for statement, metrics in FINANCIAL_MAPPING.items():

        for metric_name, tags in metrics.items():

            assert tags, (
                f"{statement}.{metric_name} has no tags"
            )


            for item in tags:

                assert "tag" in item

                assert "matched_rule" in item

                assert "metric" in item

                assert "statement" in item



def test_mapping_tags_exist_in_sec_data():

    input_file = (
        RAW_PATH /
        "humana.json"
    )


    with open(input_file) as f:

        data = json.load(f)


    gaap = data["facts"]["us-gaap"]


    missing_tags = []


    for statement, metrics in FINANCIAL_MAPPING.items():

        for metric_name, tags in metrics.items():

            for item in tags:

                tag = item["tag"]


                if tag not in gaap:

                    missing_tags.append(tag)



    assert not missing_tags, (
        f"Tags missing in SEC data: {missing_tags[:20]}"
    )



def test_mapping_has_no_duplicate_tags():

    for statement, metrics in FINANCIAL_MAPPING.items():

        for metric_name, tags in metrics.items():

            tag_names = [
                item["tag"]
                for item in tags
            ]


            duplicates = (
                len(tag_names)
                -
                len(set(tag_names))
            )


            assert duplicates == 0, (
                f"Duplicate tags in {metric_name}"
            )