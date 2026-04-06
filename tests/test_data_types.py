from __future__ import annotations

import pytest

from src.validation.schema_rules import DTYPE_FAMILY_RULES
from src.validation.validators import validate_dtype_family


@pytest.mark.parametrize(
    "table_name,fixture_name,column,expected_type",
    [
        (table_name, f"{table_name}_df", column, expected_type)
        for table_name, rules in DTYPE_FAMILY_RULES.items()
        for column, expected_type in rules.items()
    ],
)
def test_dtype_families_match_expected_contract(table_name, fixture_name, column, expected_type, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_dtype_family(dataframe, column, expected_type, table_name)
    assert result["passed"], result["message"]
