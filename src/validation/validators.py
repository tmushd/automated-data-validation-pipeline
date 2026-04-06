from __future__ import annotations

import re
import sqlite3
from typing import Iterable

import pandas as pd


def _result(
    check_name: str,
    table: str,
    column: str | None,
    passed: bool,
    failed_rows: int,
    message: str,
) -> dict[str, object]:
    return {
        "check_name": check_name,
        "table": table,
        "column": column,
        "passed": passed,
        "failed_rows": int(failed_rows),
        "message": message,
    }


def validate_table_exists(conn: sqlite3.Connection, table_name: str) -> dict[str, object]:
    query = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = ?"
    exists = conn.execute(query, (table_name,)).fetchone()[0] == 1
    return _result(
        "table_exists",
        table_name,
        None,
        exists,
        0 if exists else 1,
        f"{table_name} exists in SQLite" if exists else f"{table_name} is missing in SQLite",
    )


def validate_columns_exist(df: pd.DataFrame, expected_columns: list[str], table: str) -> dict[str, object]:
    missing_columns = [column for column in expected_columns if column not in df.columns]
    passed = not missing_columns
    message = (
        f"{table} contains all expected columns"
        if passed
        else f"{table} is missing columns: {missing_columns}"
    )
    return _result("columns_exist", table, None, passed, len(missing_columns), message)


def validate_column_order(df: pd.DataFrame, expected_columns: list[str], table: str) -> dict[str, object]:
    passed = list(df.columns) == list(expected_columns)
    return _result(
        "column_order",
        table,
        None,
        passed,
        0 if passed else len(expected_columns),
        f"{table} column order matches expected schema"
        if passed
        else f"{table} column order does not match expected schema",
    )


def validate_not_null(df: pd.DataFrame, column: str, table: str) -> dict[str, object]:
    failed_rows = int(df[column].isna().sum())
    passed = failed_rows == 0
    return _result(
        "not_null",
        table,
        column,
        passed,
        failed_rows,
        f"{table}.{column} passed not-null validation"
        if passed
        else f"{table}.{column} has {failed_rows} null values",
    )


def validate_unique(df: pd.DataFrame, columns: list[str], table: str) -> dict[str, object]:
    failed_rows = int(df.duplicated(subset=columns).sum())
    passed = failed_rows == 0
    column_label = ", ".join(columns)
    return _result(
        "unique",
        table,
        column_label,
        passed,
        failed_rows,
        f"{table}.{column_label} is unique"
        if passed
        else f"{table}.{column_label} has {failed_rows} duplicate rows",
    )


def validate_composite_uniqueness(
    df: pd.DataFrame, columns: list[str], table: str
) -> dict[str, object]:
    result = validate_unique(df, columns, table)
    result["check_name"] = "composite_uniqueness"
    return result


def validate_no_negative_values(df: pd.DataFrame, column: str, table: str) -> dict[str, object]:
    numeric_values = pd.to_numeric(df[column], errors="coerce")
    failed_rows = int((numeric_values.dropna() < 0).sum())
    passed = failed_rows == 0
    return _result(
        "no_negative_values",
        table,
        column,
        passed,
        failed_rows,
        f"{table}.{column} has no negative values"
        if passed
        else f"{table}.{column} has {failed_rows} negative values",
    )


def validate_allowed_values(
    df: pd.DataFrame, column: str, allowed_values: Iterable[str], table: str
) -> dict[str, object]:
    allowed_values_set = set(allowed_values)
    invalid_mask = df[column].notna() & ~df[column].isin(allowed_values_set)
    failed_rows = int(invalid_mask.sum())
    passed = failed_rows == 0
    invalid_values = sorted(df.loc[invalid_mask, column].astype(str).unique().tolist())
    return _result(
        "allowed_values",
        table,
        column,
        passed,
        failed_rows,
        f"{table}.{column} contains only allowed values"
        if passed
        else f"{table}.{column} has invalid values: {invalid_values}",
    )


def validate_dtype_family(
    df: pd.DataFrame, column: str, expected_type: str, table: str
) -> dict[str, object]:
    series = df[column]

    if expected_type == "numeric":
        coerced = pd.to_numeric(series, errors="coerce")
        failed_rows = int(series.notna().sum() - coerced.notna().sum())
        passed = failed_rows == 0
    elif expected_type == "integer":
        coerced = pd.to_numeric(series, errors="coerce")
        valid_mask = coerced.dropna().mod(1).eq(0)
        failed_rows = int(series.notna().sum() - valid_mask.sum())
        passed = failed_rows == 0
    elif expected_type == "string":
        failed_rows = int(series.isna().sum())
        passed = series.dropna().map(lambda value: isinstance(value, str)).all()
        failed_rows = 0 if passed else failed_rows or 1
    elif expected_type == "string_datetime":
        coerced = pd.to_datetime(series, errors="coerce")
        failed_rows = int(series.notna().sum() - coerced.notna().sum())
        passed = failed_rows == 0
    else:
        passed = False
        failed_rows = len(series)

    return _result(
        "dtype_family",
        table,
        column,
        passed,
        failed_rows,
        f"{table}.{column} matches expected dtype family {expected_type}"
        if passed
        else f"{table}.{column} does not match expected dtype family {expected_type}",
    )


def validate_foreign_key(
    child_df: pd.DataFrame,
    child_col: str,
    parent_df: pd.DataFrame,
    parent_col: str,
    child_table: str,
    parent_table: str,
) -> dict[str, object]:
    parent_values = set(parent_df[parent_col].dropna().astype(str))
    child_values = child_df[child_col].dropna().astype(str)
    failed_rows = int((~child_values.isin(parent_values)).sum())
    passed = failed_rows == 0
    return _result(
        "foreign_key",
        child_table,
        child_col,
        passed,
        failed_rows,
        f"{child_table}.{child_col} values exist in {parent_table}.{parent_col}"
        if passed
        else f"{child_table}.{child_col} has {failed_rows} orphan values against {parent_table}.{parent_col}",
    )


def validate_date_order(
    df: pd.DataFrame, earlier_col: str, later_col: str, table: str
) -> dict[str, object]:
    earlier = pd.to_datetime(df[earlier_col], errors="coerce")
    later = pd.to_datetime(df[later_col], errors="coerce")
    invalid_mask = earlier.notna() & later.notna() & (later < earlier)
    failed_rows = int(invalid_mask.sum())
    passed = failed_rows == 0
    return _result(
        "date_order",
        table,
        later_col,
        passed,
        failed_rows,
        f"{table}.{later_col} respects the ordering against {earlier_col}"
        if passed
        else f"{table}.{later_col} has {failed_rows} rows earlier than {earlier_col}",
    )


def validate_non_empty_dataframe(df: pd.DataFrame, table: str) -> dict[str, object]:
    passed = not df.empty
    return _result(
        "non_empty_dataframe",
        table,
        None,
        passed,
        0 if passed else 1,
        f"{table} is not empty" if passed else f"{table} is empty",
    )


def validate_min_row_count(df: pd.DataFrame, threshold: int, table: str) -> dict[str, object]:
    passed = len(df) >= threshold
    failed_rows = max(0, threshold - len(df))
    return _result(
        "min_row_count",
        table,
        None,
        passed,
        failed_rows,
        f"{table} meets the minimum row count threshold of {threshold}"
        if passed
        else f"{table} has {len(df)} rows, below threshold {threshold}",
    )


def validate_regex_pattern(
    df: pd.DataFrame, column: str, pattern: str, table: str
) -> dict[str, object]:
    compiled = re.compile(pattern)
    mask = df[column].dropna().astype(str).map(lambda value: bool(compiled.fullmatch(value)))
    failed_rows = int((~mask).sum())
    passed = failed_rows == 0
    return _result(
        "regex_pattern",
        table,
        column,
        passed,
        failed_rows,
        f"{table}.{column} matches regex {pattern}"
        if passed
        else f"{table}.{column} has {failed_rows} values that do not match regex {pattern}",
    )


def validate_max_null_percent(
    df: pd.DataFrame, column: str, max_percent: float, table: str
) -> dict[str, object]:
    null_percent = float(df[column].isna().mean() * 100)
    passed = null_percent <= max_percent
    failed_rows = int(df[column].isna().sum())
    return _result(
        "max_null_percent",
        table,
        column,
        passed,
        failed_rows,
        f"{table}.{column} null percentage {null_percent:.2f}% is within limit {max_percent:.2f}%"
        if passed
        else f"{table}.{column} null percentage {null_percent:.2f}% exceeds limit {max_percent:.2f}%",
    )


def validate_no_blank_strings(df: pd.DataFrame, column: str, table: str) -> dict[str, object]:
    blank_mask = df[column].fillna("").astype(str).str.strip().eq("")
    failed_rows = int(blank_mask.sum())
    passed = failed_rows == 0
    return _result(
        "no_blank_strings",
        table,
        column,
        passed,
        failed_rows,
        f"{table}.{column} contains no blank strings"
        if passed
        else f"{table}.{column} has {failed_rows} blank values",
    )


def validate_no_full_row_duplicates(df: pd.DataFrame, table: str) -> dict[str, object]:
    failed_rows = int(df.duplicated().sum())
    passed = failed_rows == 0
    return _result(
        "no_full_row_duplicates",
        table,
        None,
        passed,
        failed_rows,
        f"{table} has no fully duplicated rows"
        if passed
        else f"{table} has {failed_rows} fully duplicated rows",
    )
