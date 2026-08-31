from src.extract.extract_sec import run_extract
from src.transform.transform_financials import run_transform
from src.load.load_postgres import run_load
from utils.generate_mapping import generate_mapping
from utils.generate_financial_statements import generate_financial_statements
from utils.cleanup_old_files import cleanup_old_files


def main():

    raw_file = run_extract()

    generate_mapping(raw_file)

    processed_file = run_transform(raw_file)

    run_load(processed_file)

    generate_financial_statements()

    cleanup_old_files(max_files=5)


if __name__ == "__main__":
    main()