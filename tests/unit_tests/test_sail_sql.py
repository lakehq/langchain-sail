"""Unit tests for langchain-sail. Mirrors the Spark SQL test patterns."""

from langchain_sail import __all__

EXPECTED_ALL = [
    "BaseSailSQLTool",
    "InfoSailSQLTool",
    "ListSailSQLTool",
    "QuerySailSQLTool",
    "SailQueryCheckerTool",
    "SailSQL",
    "SailSQLToolkit",
    "create_sail_sql_agent",
]


def test_all_imports() -> None:
    assert set(__all__) == set(EXPECTED_ALL)


def test_sail_sql_is_spark_sql_subclass() -> None:
    from langchain_community.utilities.spark_sql import SparkSQL

    from langchain_sail.utilities import SailSQL

    assert issubclass(SailSQL, SparkSQL)


def test_default_sail_uri() -> None:
    from langchain_sail.utilities import _DEFAULT_SAIL_URI

    assert _DEFAULT_SAIL_URI == "sc://localhost:50051"
