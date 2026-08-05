import json
from pathlib import Path

# Read JSON
from config.settings import RAW_PATH


input_file = Path(RAW_PATH) / "humana.json"

# Read JSON
with open(input_file, "r") as file:
    data = json.load(file)

company = data["entityName"]

print(company)


# Read GAAP tags
gaap = data["facts"]["us-gaap"]


keywords = [
    "Revenue",
    "Sales",
    "Income",
    "Profit",
    "Assets",
    "Liabilities",
    "Cash",
    "Debt",
    "Equity",
    "Expense",
    "Cost",
    "Tax",
    "Inventory",
    "Receivable",
    "Payable",
    "Goodwill",
    "Property"
]


found_tags = []


# Search financial tags
for tag in gaap.keys():

    for search_word in keywords:

        if search_word.lower() in tag.lower():
            found_tags.append(tag)
            break
        
# Print tags
for tag in found_tags:
    print(tag)


# Save metadata
metadata_path = Path("data/metadata")
metadata_path.mkdir(
    parents=True,
    exist_ok=True
)


output_file = metadata_path / "humana_tags.txt"


with open(output_file, "w") as file:
    for tag in found_tags:
        file.write(tag + "\n")


print(f"Saved {len(found_tags)} tags")