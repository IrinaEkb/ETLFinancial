import json
from pathlib import Path
import re
from pprint import pprint

from config.financial_rules import FINANCIAL_RULES


RAW_FILE = Path("data/raw/humana.json")

OUTPUT_FILE = Path("config/generated_mapping.py")


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
    "Segment disclosure",
    "StockIssuedDuringPeriod",
    "StatutoryAccountingPracticesStatutoryCapitalAndSurplusBalance",
    "StatutoryAccountingPracticesStatutoryCapitalAndSurplusRequired",
    "StockRepurchaseProgram",
    "TreasuryStockShares",
    "NumberOfReportableSegments",
    "UnconditionalPurchaseObligation"



]


with open(RAW_FILE, "r") as f:

    data = json.load(f)


gaap = data["facts"]["us-gaap"]



def normalize(text):

    text = re.sub(
        r"(?<!^)(?=[A-Z])",
        " ",
        text
    )

    return text.lower().split()



def has_values(tag):

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


    return rule_words.issubset(tag_words)



metric_mapping = {}


for tag in sorted(gaap):

    if not has_values(tag):

        continue


    metric_mapping[tag] = "_".join(
        normalize(tag)
    )



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



for statement, metrics in FINANCIAL_RULES.items():

    financial_mapping[statement] = {}


    for metric, rules in metrics.items():

        financial_mapping[statement][metric] = []


        for tag in gaap:


            if not has_values(tag):

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



        metric_name = f"{statement}.{metric}"


        count = len(
            financial_mapping[statement][metric]
        )


        quality["matched"][metric_name] = count



        if count == 0:

            quality["missing_rules"][metric_name] = rules

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


for tag in sorted(gaap):


    if not has_values(tag):

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


    if not has_values(tag):

        continue


    if (

        tag not in used_tags

        and tag not in quality["ignored_tags"]

        and tag not in quality["unmapped_financial_candidates"]

    ):

        quality["not_classified_tags"].append(tag)



total_tags = len(gaap)

matched_count = len(used_tags)

ignored_count = len(
    quality["ignored_tags"]
)

unmapped_count = len(
    quality["unmapped_financial_candidates"]
)

not_classified_count = len(
    quality["not_classified_tags"]
)



OUTPUT_FILE.parent.mkdir(
    exist_ok=True
)


with open(OUTPUT_FILE, "w") as f:


    f.write("# AUTO GENERATED FILE\n\n")


    f.write(
        "METRIC_MAPPING = "
    )

    pprint(
        metric_mapping,
        stream=f,
        width=100
    )


    f.write("\n\n")


    f.write(
        "FINANCIAL_MAPPING = "
    )

    pprint(
        financial_mapping,
        stream=f,
        width=100
    )


    f.write("\n\n")


    f.write(
        "TAG_CLASSIFICATION = "
    )

    pprint(
        tag_classification,
        stream=f,
        width=100
    )


    f.write("\n\n")


    f.write(
        "IGNORED_TAGS = "
    )

    pprint(
        quality["ignored_tags"],
        stream=f,
        width=100
    )


    f.write("\n\n")


    f.write(
        "QUALITY_REPORT = "
    )

    pprint(
        quality,
        stream=f,
        width=100
    )



print(
    "\n========== QUALITY REPORT ==========\n"
)


print(
    f"Total XBRL tags: {total_tags}"
)


print(
    f"Mapped financial tags: {matched_count}"
)


print(
    f"Ignored disclosures: {ignored_count}"
)


print(
    f"Unmapped financial candidates: {unmapped_count}"
)


print(
    f"Not classified: {not_classified_count}"
)



print(
    "\n========== NOT CLASSIFIED TAGS ==========\n"
)


if quality["not_classified_tags"]:


    for tag in quality["not_classified_tags"]:

        print(tag)


else:

    print("None")



print(
    "\n========== UNMAPPED FINANCIAL CANDIDATES ==========\n"
)


if quality["unmapped_financial_candidates"]:


    for tag in quality["unmapped_financial_candidates"]:

        print(tag)


else:

    print("None")



print(
    "\n========== IGNORED DISCLOSURES ==========\n"
)


for tag in quality["ignored_tags"]:

    print(tag)



print(
    "\n========== MATCHED METRICS ==========\n"
)


for metric, count in quality["matched"].items():

    print(
        f"{metric}: {count}"
    )



print(
    "\n========== MISSING RULES ==========\n"
)


if not quality["missing_rules"]:

    print("None")


else:


    for metric, rules in quality["missing_rules"].items():

        print(metric)

        print(
            "Expected:",
            rules
        )