# INPUT:
# humana_financial_metrics.csv
# Contains standardized financial metrics mapped from XBRL tags
# OUTPUT:
# PostgreSQL financial database

import pandas as pd
from sqlalchemy import create_engine 

from config.settings import PROCESSED_PATH

def run_load():
    file = (PROCESSED_PATH/"humana_financial_metrics.csv" )

    df = pd.read_csv(file)
    engine = create_engine('postgresql://username:password@localhost:5432/financial_db') 

    df.to_sql(
        'financial_metrics', 
        engine, 
        if_exists='replace', 
        index=False 
    )

    print("Data loaded into PostgreSQL database successfully." )

    if __name__ == "__main__": 
        run_load() 