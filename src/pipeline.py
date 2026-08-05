from src.extract.extract_sec import run_extract
from src.transform.transform_financials import run_transform
from src.load.load_postgres import run_load


def main():

    run_extract()

    run_transform()

    run_load()


if __name__ == "__main__":
    main()