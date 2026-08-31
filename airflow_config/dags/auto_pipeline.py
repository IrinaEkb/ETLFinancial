import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from airflow.sdk import dag, task


@dag(
    dag_id="xbrl_financial_pipeline",
    description="Automated XBRL financial ETL pipeline",
    schedule="0 8 * * 4",
    start_date=datetime(2026, 8, 6),
    catchup=False,
    tags=[
        "finance",
        "etl",
        "xbrl"
    ],
)
def xbrl_financial_pipeline():

    @task
    def extract():
        from src.extract.extract_sec import run_extract

        output_file = run_extract()
        print(f"Extract completed: {output_file}")
        return str(output_file)

    @task
    def generate_mapping(raw_file):
        from utils.generate_mapping import generate_mapping as run_generate_mapping

        mapping_file = run_generate_mapping(raw_file)
        print(f"Mapping completed: {mapping_file}")
        return str(mapping_file)

    @task
    def transform(input_file):
        from src.transform.transform_financials import run_transform

        output_file = run_transform(input_file)
        print(f"Transform completed: {output_file}")
        return str(output_file)

    @task
    def load(file):
        from src.load.load_postgres import run_load

        run_load(file)
        print("Load completed")

    @task
    def generate_financial_statements():
        from utils.generate_financial_statements import (
            generate_financial_statements as run_generate_financial_statements
        )

        files = run_generate_financial_statements()
        print(f"Financial statements generated: {files}")
        return [str(file) for file in files]

    @task
    def cleanup():
        from utils.cleanup_old_files import cleanup_old_files

        cleanup_old_files(max_files=5)
        print("Cleanup completed")

    extract_task = extract()

    mapping_task = generate_mapping(extract_task)

    transform_task = transform(extract_task)

    load_task = load(transform_task)

    statements_task = generate_financial_statements()

    cleanup_task = cleanup()

    extract_task >> mapping_task
    mapping_task >> transform_task
    transform_task >> load_task
    load_task >> statements_task
    statements_task >> cleanup_task


xbrl_financial_pipeline()