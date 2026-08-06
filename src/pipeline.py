from src.extract.extract_sec import run_extract
from src.transform.transform_financials import run_transform
from src.load.load_postgres import run_load
from utils.generate_mapping import generate_mapping


def main():
    raw_file = run_extract()

    generate_mapping(raw_file)

    processed_file = run_transform(raw_file)

    run_load(processed_file)


if __name__ == "__main__":
    main()