# Validates the structure and data quality of the PostgreSQL financial_metrics table.

import os
import re

import pandas as pd
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text


load_dotenv()


EXPECTED_COLUMNS = {
    "statement",
    "metric",
    "source_tag",
    "value",
    "unit",
    "start_date",
    "end_date",
    "filed_date",
    "form",
}

EXPECTED_STATEMENTS = {
    "income_statement",
    "balance_sheet",
    "cash_flow",
}


def get_database_engine():
    """Create a PostgreSQL connection using environment settings."""

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


@pytest.fixture(scope="module")
def engine():
    """Provide one PostgreSQL engine for this test module."""

    return get_database_engine()


@pytest.fixture(scope="module")
def financial_metrics(engine):
    """Load the financial_metrics table into a DataFrame."""

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

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)


def test_financial_metrics_table_exists(engine):
    """Verify that the financial_metrics table exists."""

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    assert "financial_metrics" in tables


def test_required_columns_exist(financial_metrics):
    """Verify that all required financial metric columns exist."""

    actual_columns = set(financial_metrics.columns)

    missing_columns = EXPECTED_COLUMNS - actual_columns

    assert not missing_columns, (
        f"Missing required columns: {missing_columns}"
    )


def test_exactly_three_statements(financial_metrics):
    """Verify that exactly three financial statements are present."""

    statements = set(
        financial_metrics["statement"].dropna().unique()
    )

    assert len(statements) == 3


def test_expected_statements_exist(financial_metrics):
    """Verify that Income, Balance Sheet, and Cash Flow exist."""

    statements = set(
        financial_metrics["statement"].dropna().unique()
    )

    assert statements == EXPECTED_STATEMENTS


def test_no_unknown_statements(financial_metrics):
    """Verify that no unexpected statement categories exist."""

    statements = set(
        financial_metrics["statement"].dropna().unique()
    )

    unknown_statements = statements - EXPECTED_STATEMENTS

    assert not unknown_statements, (
        f"Unknown statements found: {unknown_statements}"
    )


def test_statement_counts_are_positive(financial_metrics):
    """Verify that every statement contains financial facts."""

    counts = financial_metrics["statement"].value_counts()

    for statement in EXPECTED_STATEMENTS:
        assert counts.get(statement, 0) > 0, (
            f"No rows found for statement: {statement}"
        )


def test_start_date_is_not_after_end_date(financial_metrics):
    """Verify that start_date never occurs after end_date."""

    df = financial_metrics.copy()

    df["start_date"] = pd.to_datetime(
        df["start_date"],
        errors="coerce",
    )

    df["end_date"] = pd.to_datetime(
        df["end_date"],
        errors="coerce",
    )

    invalid_periods = (
        df["start_date"].notna()
        & df["end_date"].notna()
        & (df["start_date"] > df["end_date"])
    )

    assert invalid_periods.sum() == 0, (
        f"Found {invalid_periods.sum()} rows where "
        "start_date is after end_date."
    )


def test_period_types_are_valid(financial_metrics):
    """
    Verify that every fact has either an instant or duration period.

    Instant:
        start_date is NULL
        end_date is NOT NULL

    Duration:
        start_date is NOT NULL
        end_date is NOT NULL
    """

    df = financial_metrics.copy()

    df["start_date"] = pd.to_datetime(
        df["start_date"],
        errors="coerce",
    )

    df["end_date"] = pd.to_datetime(
        df["end_date"],
        errors="coerce",
    )

    instant_mask = (
        df["start_date"].isna()
        & df["end_date"].notna()
    )

    duration_mask = (
        df["start_date"].notna()
        & df["end_date"].notna()
    )

    valid_mask = instant_mask | duration_mask

    invalid_rows = df[~valid_mask]

    assert invalid_rows.empty, (
        f"Found {len(invalid_rows)} rows with invalid "
        "period structure."
    )


def test_no_empty_metrics(financial_metrics):
    """Verify that metric is populated for every row."""

    assert financial_metrics["metric"].notna().all()

    assert (
        financial_metrics["metric"]
        .astype(str)
        .str.strip()
        .ne("")
        .all()
    )


def test_no_empty_source_tags(financial_metrics):
    """Verify that source_tag is populated for every row."""

    assert financial_metrics["source_tag"].notna().all()

    assert (
        financial_metrics["source_tag"]
        .astype(str)
        .str.strip()
        .ne("")
        .all()
    )


def test_no_empty_values(financial_metrics):
    """Verify that every financial fact has a value."""

    assert financial_metrics["value"].notna().all()


def test_no_empty_units(financial_metrics):
    """Verify that every financial fact has a unit."""

    assert financial_metrics["unit"].notna().all()

    assert (
        financial_metrics["unit"]
        .astype(str)
        .str.strip()
        .ne("")
        .all()
    )


def test_no_empty_filed_dates(financial_metrics):
    """Verify that every SEC fact has a filed date."""

    assert financial_metrics["filed_date"].notna().all()


def test_forms_are_populated(financial_metrics):
    """Verify that every financial fact has a filing form."""

    assert financial_metrics["form"].notna().all()

    assert (
        financial_metrics["form"]
        .astype(str)
        .str.strip()
        .ne("")
        .all()
    )


def test_forms_are_valid_sec_filing_types(financial_metrics):
    """
    Verify that form values follow the SEC filing form pattern.

    Examples:
        10-K
        10-Q
        8-K
        10-K/A
        10-Q/A
    """

    forms = (
        financial_metrics["form"]
        .astype(str)
        .str.strip()
    )

    invalid_forms = forms[
        ~forms.str.match(
            r"^\d{1,2}-[A-Z]{1,3}(?:/[A-Z])?$"
        )
    ]

    assert invalid_forms.empty, (
        f"Invalid SEC filing forms found: "
        f"{invalid_forms.unique().tolist()}"
    )


def test_form_distribution(financial_metrics):
    """
    Verify that filing forms can be grouped and counted.

    This is intentionally not restricted to a fixed list because
    SEC filings may contain additional valid form types.
    """

    form_counts = (
        financial_metrics["form"]
        .value_counts()
    )

    print("\n========== SEC FORM DISTRIBUTION ==========")

    print(form_counts.to_string())

    assert not form_counts.empty
    assert form_counts.sum() == len(financial_metrics)


def test_no_exact_duplicate_rows(financial_metrics):
    """Verify that the financial_metrics table has no exact duplicates."""

    duplicate_count = (
        financial_metrics
        .duplicated()
        .sum()
    )

    assert duplicate_count == 0, (
        f"Found {duplicate_count} exact duplicate rows."
    )


def test_total_rows_match_statement_counts(financial_metrics):
    """Verify that statement row counts equal the total table row count."""

    statement_counts = (
        financial_metrics["statement"]
        .value_counts()
    )

    total_statement_rows = (
        statement_counts
        .reindex(EXPECTED_STATEMENTS)
        .sum()
    )

    assert total_statement_rows == len(financial_metrics)