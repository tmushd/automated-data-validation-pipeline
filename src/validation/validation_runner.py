from __future__ import annotations

from src.validation.db_utils import get_connection, read_table
from src.validation.schema_rules import EXPECTED_SCHEMAS
from src.validation.validators import (
    validate_column_order,
    validate_columns_exist,
    validate_non_empty_dataframe,
    validate_table_exists,
)


def run_basic_validations() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    with get_connection() as connection:
        for table_name, expected_columns in EXPECTED_SCHEMAS.items():
            results.append(validate_table_exists(connection, table_name))
            dataframe = read_table(table_name)
            results.append(validate_non_empty_dataframe(dataframe, table_name))
            results.append(validate_columns_exist(dataframe, expected_columns, table_name))
            results.append(validate_column_order(dataframe, expected_columns, table_name))

    return results


if __name__ == "__main__":
    for result in run_basic_validations():
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f"[{status}] {result['check_name']} | table={result['table']} | "
            f"column={result['column']} | failed_rows={result['failed_rows']} | "
            f"message={result['message']}"
        )
