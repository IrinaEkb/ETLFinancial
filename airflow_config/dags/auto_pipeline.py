import sys
from pathlib import Path

from src.load.load_postgres import run_load

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from airflow.sdk import dag, task

from datetime import datetime


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

        result = run_extract()

        print(f"Extract completed: {result}")

        return str(result)


    @task
    def transform():

        from src.transform.transform_financials import transform_financials

        result = transform_financials()

        print("Transform completed")

        return result

    @task
    def load(file):

        from src.load.load_postgres import run_load

        run_load(file)

        print("Load completed")


    extract_task = extract()
    transform_task = transform()
    load_task = load(transform_task)


    extract_task >> transform_task >> load_task 



xbrl_financial_pipeline()