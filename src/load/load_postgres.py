# INPUT:
# data/processed/humana_financial_metrics.csv
#
# OUTPUT:
# PostgreSQL table financial_metrics


import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

from config.settings import PROCESSED_PATH


load_dotenv()


def get_latest_processed_file():

    files = list(
        Path(PROCESSED_PATH).glob(
            "humana_financial_metrics_*.csv"
        )
    )


    if not files:

        raise FileNotFoundError(
            "No processed CSV files found"
        )


    def extract_date(file):

        date_part = (
            file.stem
            .replace(
                "humana_financial_metrics_",
             ""
             )
         )

        return datetime.strptime(
            date_part,
            "%Y_%m_%d"
        )

    


    latest_file = max(
        files,
        key=extract_date
    )


    return latest_file



def run_load(file=None):

    if file is None:

        file = get_latest_processed_file()


    file = Path(file)


    print(
        f"Loading file: {file}"
    )


    if not file.exists():

        raise FileNotFoundError(
            f"File not found: {file}"
        )


    df = pd.read_csv(file)


    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")


    connection_string = (

        f"postgresql+psycopg://"

        f"{user}:{password}@"

        f"{host}:{port}/{database}"

    )


    engine = create_engine(
        connection_string
    )


    df.to_sql(

        name="financial_metrics",

        con=engine,

        if_exists="replace",

        index=False,

    )


    print(
        f"Loaded {len(df)} rows into PostgreSQL"
    )



if __name__ == "__main__":

    run_load()