# ETL Step 1: Extract
# Downloads company financial data from SEC XBRL API.
# Input:
#           SEC API
#           Process:
#               - Sends request to SEC company facts endpoint
#               - Receives JSON response
#               - Saves raw XBRL data
# Output:
#   
#         data/raw/humana.json
#         data/processed/humana_all_facts.csv
#         The all_facts dataset contains all available XBRL facts without business classification.

import json
import time
from pathlib import Path

import pandas as pd
import requests

from config.settings import (
    COMPANY_CIK,
    RAW_PATH,
    PROCESSED_PATH,
)


def build_headers():
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.sec.gov/",
    }


def create_all_facts_csv(data):

    gaap = data["facts"]["us-gaap"]

    all_facts = []

    for tag, info in gaap.items():

        units = info.get("units", {})

        for unit_name, values in units.items():

            for item in values:

                all_facts.append(
                    {
                        "tag": tag,
                        "unit": unit_name,
                        "value": item.get("val"),
                        "start_date": item.get("start"),
                        "end_date": item.get("end"),
                        "filed_date": item.get("filed"),
                        "form": item.get("form"),
                    }
                )

    df = pd.DataFrame(all_facts)

    processed = Path(PROCESSED_PATH)
    processed.mkdir(parents=True, exist_ok=True)

    output = processed / "humana_all_facts.csv"

    df.to_csv(output, index=False)

    print(f"Saved {len(df)} rows to {output}")


def fetch_company_facts(url, timeout=30, max_attempts=3, output_path=None):

    headers = build_headers()

    for attempt in range(1, max_attempts + 1):

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout,
            )

        except requests.RequestException as exc:

            if attempt < max_attempts:
                time.sleep(2)
                continue

            raise RuntimeError(
                f"Network error: {exc}"
            ) from exc

        print(
            f"Attempt {attempt}: "
            f"{response.status_code}"
        )

        if (
            response.status_code
            in {403, 429, 500, 502, 503, 504}
            and attempt < max_attempts
        ):

            time.sleep(2)
            continue

        if response.status_code != 200:

            raise RuntimeError(
                f"SEC request failed: "
                f"{response.status_code}"
            )

        try:
            data = response.json()

        except ValueError as e:
            raise RuntimeError(
                "Expected JSON response from SEC API"
        ) from e

        

        if output_path is None:

            output_path = (
                Path(RAW_PATH)
                / "humana.json"
            )

        else:

            output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            json.dumps(data, indent=4)
        )

        print(f"Saved JSON to {output_path}")

        create_all_facts_csv(data)

        return data

    raise RuntimeError(
        "Unable to retrieve SEC data."
    )


def run_extract():

    url = (
        "https://data.sec.gov/api/xbrl/"
        f"companyfacts/CIK{COMPANY_CIK}.json"
    )

    fetch_company_facts(url)


if __name__ == "__main__":
    run_extract()