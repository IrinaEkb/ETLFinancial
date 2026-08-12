
# Reads financial_metrics from PostgreSQL and creates
# dated CSV files for Income Statement, Balance Sheet,
# and Cash Flow Statement without aggregating values.

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


ANALYTICS_PATH = Path("data/analytics")


def get_database_engine():
    """Create a PostgreSQL connection using existing environment settings."""

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

    return create_engine(connection_string)


def load_financial_metrics():
    """Load the existing financial_metrics table from PostgreSQL."""

    engine = get_database_engine()

    query = """
        SELECT
            statement,
            metric,
            source_tag,
            value,
            unit,
            start_date,
            end_date,
            filed_date,
            form
        FROM financial_metrics
    """

    return pd.read_sql(query, engine)


def prepare_statement_data(df, statement):


    statement_df = df[
        df["statement"] == statement
    ].copy()

    if statement_df.empty:
        return statement_df

    date_columns = [
        "start_date",
        "end_date",
        "filed_date",
    ]

    for column in date_columns:
        statement_df[column] = pd.to_datetime(
            statement_df[column],
            errors="coerce"
        )

    # Keep instant facts and duration facts separate.
    statement_df["period_type"] = "duration"

    instant_mask = (
        statement_df["start_date"].isna()
        & statement_df["end_date"].notna()
    )

    statement_df.loc[
        instant_mask,
        "period_type"
    ] = "instant"

    # Do not aggregate or combine financial facts.
    # Each SEC fact remains a separate record.
    statement_df = statement_df.sort_values(
        by=[
            "metric",
            "end_date",
            "start_date",
            "filed_date",
            "form",
            "source_tag",
        ],
        na_position="last"
    )

    return statement_df


def save_statement(df, filename):
    """Save one statement to a dated analytics CSV file."""

    ANALYTICS_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    today = datetime.today().strftime("%Y_%m_%d")

    output_file = (
        ANALYTICS_PATH
        / f"{filename}_{today}.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Saved {len(df)} rows to {output_file}"
    )

    return output_file


def generate_financial_statements():
    """
    Generate three dated financial statement CSV files
    from the PostgreSQL financial_metrics table.
    """

    df = load_financial_metrics()

    required_columns = [
        "statement",
        "metric",
        "source_tag",
        "value",
        "unit",
        "start_date",
        "end_date",
        "filed_date",
        "form",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    income_statement = prepare_statement_data(
        df,
        "income_statement"
    )

    balance_sheet = prepare_statement_data(
        df,
        "balance_sheet"
    )

    cash_flow = prepare_statement_data(
        df,
        "cash_flow"
    )

    income_file = save_statement(
        income_statement,
        "income_statement"
    )

    balance_file = save_statement(
        balance_sheet,
        "balance_sheet"
    )

    cash_flow_file = save_statement(
        cash_flow,
        "cash_flow"
    )

    print("\n========== FINANCIAL STATEMENT REPORT ==========")

    print(
        f"Income Statement: {len(income_statement)} rows"
    )

    print(
        f"Balance Sheet: {len(balance_sheet)} rows"
    )

    print(
        f"Cash Flow: {len(cash_flow)} rows"
    )

    return (
        income_file,
        balance_file,
        cash_flow_file
    )


if __name__ == "__main__":
    generate_financial_statements()