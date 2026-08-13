# Validates financial statement generation, period classification, and CSV output.

from pathlib import Path

import pandas as pd
import pytest

from utils.generate_financial_statements import (
    load_financial_metrics,
    prepare_statement_data,
    generate_financial_statements,
)


EXPECTED_STATEMENTS = [
    "income_statement",
    "balance_sheet",
    "cash_flow",
]


@pytest.fixture(scope="module")
def financial_metrics():
    """Load financial metrics from PostgreSQL."""

    return load_financial_metrics()


@pytest.mark.parametrize(
    "statement",
    EXPECTED_STATEMENTS,
)
def test_statement_contains_only_its_own_data(
    financial_metrics,
    statement,
):
    """Verify that each statement contains only its own records."""

    statement_df = prepare_statement_data(
        financial_metrics,
        statement,
    )

    assert not statement_df.empty

    assert (
        statement_df["statement"]
        .eq(statement)
        .all()
    )


@pytest.mark.parametrize(
    "statement",
    EXPECTED_STATEMENTS,
)
def test_statement_row_count_matches_source(
    financial_metrics,
    statement,
):
    """Verify that filtering a statement does not lose rows."""

    source_count = (
        financial_metrics["statement"]
        .eq(statement)
        .sum()
    )

    statement_df = prepare_statement_data(
        financial_metrics,
        statement,
    )

    assert len(statement_df) == source_count


@pytest.mark.parametrize(
    "statement",
    EXPECTED_STATEMENTS,
)
def test_period_type_is_created(
    financial_metrics,
    statement,
):
    """Verify that period_type is added to statement data."""

    statement_df = prepare_statement_data(
        financial_metrics,
        statement,
    )

    assert "period_type" in statement_df.columns


@pytest.mark.parametrize(
    "statement",
    EXPECTED_STATEMENTS,
)
def test_instant_periods_are_classified_correctly(
    financial_metrics,
    statement,
):
    """Verify that facts without start_date are classified as instant."""

    statement_df = prepare_statement_data(
        financial_metrics,
        statement,
    )

    instant_mask = (
        statement_df["start_date"].isna()
        & statement_df["end_date"].notna()
    )

    assert (
        statement_df.loc[
            instant_mask,
            "period_type"
        ]
        .eq("instant")
        .all()
    )


@pytest.mark.parametrize(
    "statement",
    EXPECTED_STATEMENTS,
)
def test_duration_periods_are_classified_correctly(
    financial_metrics,
    statement,
):
    """Verify that facts with both dates are classified as duration."""

    statement_df = prepare_statement_data(
        financial_metrics,
        statement,
    )

    duration_mask = (
        statement_df["start_date"].notna()
        & statement_df["end_date"].notna()
    )

    assert (
        statement_df.loc[
            duration_mask,
            "period_type"
        ]
        .eq("duration")
        .all()
    )


@pytest.mark.parametrize(
    "statement",
    EXPECTED_STATEMENTS,
)
def test_dates_are_converted_to_datetime(
    financial_metrics,
    statement,
):
    """Verify that financial statement dates are converted to datetime."""

    statement_df = prepare_statement_data(
        financial_metrics,
        statement,
    )

    assert pd.api.types.is_datetime64_any_dtype(
        statement_df["start_date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        statement_df["end_date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        statement_df["filed_date"]
    )


@pytest.mark.parametrize(
    "statement",
    EXPECTED_STATEMENTS,
)
def test_statement_is_sorted(
    financial_metrics,
    statement,
):
    """Verify that statement data follows the expected sorting order."""

    statement_df = prepare_statement_data(
        financial_metrics,
        statement,
    )

    expected_df = statement_df.sort_values(
        by=[
            "metric",
            "end_date",
            "start_date",
            "filed_date",
            "form",
            "source_tag",
        ],
        na_position="last",
    )

    assert statement_df.reset_index(drop=True).equals(
        expected_df.reset_index(drop=True)
    )


def test_all_statement_rows_are_preserved(
    financial_metrics,
):
    """Verify that all source rows appear in one of the three statements."""

    source_count = len(financial_metrics)

    generated_count = 0

    for statement in EXPECTED_STATEMENTS:

        statement_df = prepare_statement_data(
            financial_metrics,
            statement,
        )

        generated_count += len(statement_df)

    assert generated_count == source_count


def test_no_statement_rows_are_aggregated(
    financial_metrics,
):
    """
    Verify that statement generation preserves the source row count.

    Financial values are not summed or grouped at this stage.
    """

    source_count = len(financial_metrics)

    generated_count = sum(
        len(
            prepare_statement_data(
                financial_metrics,
                statement,
            )
        )
        for statement in EXPECTED_STATEMENTS
    )

    assert generated_count == source_count


def test_financial_statement_csv_files_are_created():
    """Verify that all three analytics CSV files are generated."""

    income_file, balance_file, cash_flow_file = (
        generate_financial_statements()
    )

    assert Path(income_file).exists()
    assert Path(balance_file).exists()
    assert Path(cash_flow_file).exists()


def test_financial_statement_csv_filenames():
    """Verify that generated CSV filenames use the expected names."""

    income_file, balance_file, cash_flow_file = (
        generate_financial_statements()
    )

    assert Path(income_file).name.startswith(
        "income_statement_"
    )

    assert Path(balance_file).name.startswith(
        "balance_sheet_"
    )

    assert Path(cash_flow_file).name.startswith(
        "cash_flow_"
    )

    assert Path(income_file).suffix == ".csv"
    assert Path(balance_file).suffix == ".csv"
    assert Path(cash_flow_file).suffix == ".csv"


def test_generated_csv_row_counts_match_postgres():
    """
    Verify that the three generated CSV files preserve
    the total number of PostgreSQL financial facts.
    """

    source_df = load_financial_metrics()

    income_file, balance_file, cash_flow_file = (
        generate_financial_statements()
    )

    income_df = pd.read_csv(income_file)
    balance_df = pd.read_csv(balance_file)
    cash_flow_df = pd.read_csv(cash_flow_file)

    generated_count = (
        len(income_df)
        + len(balance_df)
        + len(cash_flow_df)
    )

    assert generated_count == len(source_df)


@pytest.mark.parametrize(
    "filename,statement",
    [
        ("income_statement_", "income_statement"),
        ("balance_sheet_", "balance_sheet"),
        ("cash_flow_", "cash_flow"),
    ],
)
def test_generated_csv_contains_correct_statement(
    filename,
    statement,
):
    """Verify that each generated CSV contains only its own statement."""

    analytics_path = Path("data/analytics")

    files = sorted(
        analytics_path.glob(
            f"{filename}*.csv"
        )
    )

    assert files

    latest_file = files[-1]

    df = pd.read_csv(latest_file)

    assert not df.empty

    assert (
        df["statement"]
        .eq(statement)
        .all()
    )