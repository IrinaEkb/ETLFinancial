# Builds financial tag mapping for Humana SEC XBRL data.
# Reads extracted XBRL JSON → applies FINANCIAL_RULES →
# creates FINANCIAL_MAPPING used by transform_financials.py
#
# Output: generated_mapping.py with XBRL tags classified
# into Income Statement, Balance Sheet, and Cash Flow metrics.

import json
import re
from pathlib import Path
from pprint import pprint

from config.financial_rules import FINANCIAL_RULES
from config.settings import RAW_PATH


OUTPUT_FILE = Path(
    "config/generated_mapping.py"
)


IGNORE_RULES = [

    "FairValueDisclosure",
    "FairValueMeasurement",
    "FairValueHierarchy",
    "WeightedAverage",
    "NumberOfSharesOutstanding",
    "WeightedAverageNumberOfShares",
    "SharesAuthorized",
    "Maturities",
    "MaturityDate",
    "InterestRateEffective",
    "InterestRateRange",
    "Reconciliation",
    "RollForward",
    "FutureMinimum",
    "FutureAmortization",
    "ExpectedLife",
    "ExpectedVolatility",
    "AccumulatedOtherComprehensive",
    "Disclosure",
    "LossContingency",
    "RestructuringAndRelatedCost",
    "StatutoryAccountingPractices",
    "EarningsPerShare",
    "CommitmentsAndContingencies",
    "CommonStockShares",
    "CumulativeEffect",
    "FairValueLevel",
    "InsuranceRegulatory",
    "SegmentDisclosure",
    "StockIssuedDuringPeriod",
    "StockRepurchaseProgram",
    "TreasuryStockShares",
    "NumberOfReportableSegments",
    "UnconditionalPurchaseObligation"

]


FINANCIAL_WORDS = [

    "Asset",
    "Liability",
    "Revenue",
    "Expense",
    "Income",
    "Cash",
    "Debt",
    "Investment",
    "Premium",
    "Claim",
    "Benefit",
    "Tax",
    "Equity",
    "Receivable",
    "Payable",
    "Lease",
    "Dividend",
    "Cost",
    "Loss",
    "Gain"

]


def normalize(text):

    text = re.sub(
        r"(?<!^)(?=[A-Z])",
        " ",
        text
    )

    return text.lower().split()



def has_values(tag, gaap):

    units = gaap[tag].get(
        "units",
        {}
    )

    for values in units.values():

        for item in values:

            if item.get("val") is not None:
                return True

    return False



def is_ignored(tag):

    for word in IGNORE_RULES:

        if word.lower() in tag.lower():
            return True

    return False



def exact_match(tag, rule):

    return tag.lower() == rule.lower()



def safe_match(tag, rule):

    if is_ignored(tag):
        return False


    tag_words = set(
        normalize(tag)
    )

    rule_words = set(
        normalize(rule)
    )


    return rule_words.issubset(
        tag_words
    )



def check_mapping_duplicates(tag_classification):

    tag_metrics = {}


    for item in tag_classification:

        tag = item["tag"]

        metric = (
            f"{item['statement']}.{item['metric']}"
        )


        if tag not in tag_metrics:

            tag_metrics[tag] = []


        tag_metrics[tag].append(metric)



    duplicates = {

        tag: metrics

        for tag, metrics in tag_metrics.items()

        if len(metrics) > 1

    }


    print(
        "\n========== MAPPING DUPLICATES =========="
    )


    print(
        f"Tags mapped to multiple metrics: {len(duplicates)}"
    )


    for tag, metrics in duplicates.items():

        print("\n", tag)

        for metric in metrics:

            print(
                "  ->",
                metric
            )


    return duplicates



def generate_mapping(raw_file=None):


    if raw_file is None:

        raw_file = get_latest_raw_file()


    print(
        f"Generating mapping from: {raw_file}"
    )


    with open(raw_file, "r") as f:

        data = json.load(f)


    gaap = data["facts"]["us-gaap"]


    metric_mapping = {}

    financial_mapping = {}

    used_tags = set()

    tag_classification = []



    quality = {

        "matched": {},

        "missing_rules": {},

        "unmapped_financial_candidates": [],

        "ignored_tags": [],

        "not_classified_tags": []

    }



    for tag in sorted(gaap):

        if not has_values(tag, gaap):

            continue


        metric_mapping[tag] = "_".join(
            normalize(tag)
        )



    for statement, metrics in FINANCIAL_RULES.items():


        financial_mapping[statement] = {}



        for metric, rules in metrics.items():


            financial_mapping[statement][metric] = []



            for tag in gaap:


                if not has_values(tag, gaap):

                    continue



                matched_rule = None



                for rule in rules:

                    if exact_match(tag, rule):

                        matched_rule = rule

                        break



                if matched_rule is None:

                    for rule in rules:

                        if safe_match(tag, rule):

                            matched_rule = rule

                            break



                if matched_rule:


                    financial_mapping[statement][metric].append(

                        {
                            "tag": tag,
                            "matched_rule": matched_rule,
                            "statement": statement,
                            "metric": metric
                        }

                    )


                    tag_classification.append(

                        {
                            "tag": tag,
                            "statement": statement,
                            "metric": metric
                        }

                    )


                    used_tags.add(tag)



            metric_name = (
                f"{statement}.{metric}"
            )


            count = len(
                financial_mapping[statement][metric]
            )


            quality["matched"][metric_name] = count



            if count == 0:

                quality["missing_rules"][metric_name] = rules



    for tag in sorted(gaap):

        if not has_values(tag, gaap):

            continue


        if tag in used_tags:

            continue



        if is_ignored(tag):

            quality["ignored_tags"].append(tag)

            continue



        if any(
            word.lower() in tag.lower()
            for word in FINANCIAL_WORDS
        ):

            quality["unmapped_financial_candidates"].append(tag)



    for tag in sorted(gaap):

        if not has_values(tag, gaap):

            continue


        if (

            tag not in used_tags

            and tag not in quality["ignored_tags"]

            and tag not in quality["unmapped_financial_candidates"]

        ):

            quality["not_classified_tags"].append(tag)



    duplicates = check_mapping_duplicates(
        tag_classification
    )



    quality["duplicate_tags"] = duplicates



    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )



    with open(
        OUTPUT_FILE,
        "w"
    ) as f:


        f.write(
            "# AUTO GENERATED FILE\n\n"
        )


        f.write(
            "METRIC_MAPPING = "
        )

        pprint(
            metric_mapping,
            stream=f,
            width=100
        )


        f.write("\n\nFINANCIAL_MAPPING = ")

        pprint(
            financial_mapping,
            stream=f,
            width=100
        )


        f.write("\n\nTAG_CLASSIFICATION = ")

        pprint(
            tag_classification,
            stream=f,
            width=100
        )


        f.write("\n\nIGNORED_TAGS = ")

        pprint(
            quality["ignored_tags"],
            stream=f,
            width=100
        )


        f.write("\n\nQUALITY_REPORT = ")

        pprint(
            quality,
            stream=f,
            width=100
        )



    print(
        "\n========== QUALITY REPORT =========="
    )


    print(
        f"Total XBRL tags: {len(gaap)}"
    )


    print(
        f"Mapped tags: {len(used_tags)}"
    )


    print(
        f"Ignored: {len(quality['ignored_tags'])}"
    )


    print(
        f"Unmapped candidates: {len(quality['unmapped_financial_candidates'])}"
    )


    print(
        f"Not classified: {len(quality['not_classified_tags'])}"
    )


    print(
        f"\nSaved mapping to {OUTPUT_FILE}"
    )


    return OUTPUT_FILE



def get_latest_raw_file():

    files = list(
        Path(RAW_PATH).glob(
            "humana_*.json"
        )
    )


    if not files:

        raise FileNotFoundError(
            "No raw JSON files found"
        )


    return max(
        files,
        key=lambda file: file.stat().st_mtime
    )



if __name__ == "__main__":

    generate_mapping()