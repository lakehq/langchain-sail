"""Integration tests for langchain-sail. Requires pysail to be installed.

Mirrors the Spark SQL integration test patterns, using an embedded Sail server.
"""

import pytest
from pysail.spark import SparkConnectServer
from pyspark.sql import SparkSession

from langchain_sail.tools import (
    InfoSailSQLTool,
    ListSailSQLTool,
    QuerySailSQLTool,
)
from langchain_sail.utilities import SailSQL


@pytest.fixture(scope="module")
def sail_server():
    """Start an embedded Sail server for the test session."""
    server = SparkConnectServer()
    server.start()
    _, port = server.listening_address
    yield port
    server.stop()


@pytest.fixture(scope="module")
def spark(sail_server):
    """Create a SparkSession connected to the Sail server."""
    session = SparkSession.builder.remote(f"sc://localhost:{sail_server}").getOrCreate()
    yield session
    session.stop()


@pytest.fixture(scope="module")
def sail_db(spark):
    """Create a SailSQL instance with test data."""
    spark.sql(
        "CREATE TABLE test_employees (name STRING, department STRING, salary INT)"
    )
    spark.sql(
        "INSERT INTO test_employees VALUES "
        "('Alice', 'Engineering', 120000), "
        "('Bob', 'Marketing', 95000), "
        "('Charlie', 'Engineering', 135000)"
    )
    db = SailSQL(spark_session=spark)
    yield db
    spark.sql("DROP TABLE test_employees")


def test_get_usable_table_names(sail_db: SailSQL) -> None:
    tables = list(sail_db.get_usable_table_names())
    assert "test_employees" in tables


def test_get_table_info(sail_db: SailSQL) -> None:
    info = sail_db.get_table_info(["test_employees"])
    assert "CREATE TABLE test_employees" in info
    assert "name" in info
    assert "salary" in info


def test_get_table_info_no_throw(sail_db: SailSQL) -> None:
    info = sail_db.get_table_info_no_throw(["test_employees"])
    assert "CREATE TABLE test_employees" in info


def test_get_table_info_no_throw_invalid(sail_db: SailSQL) -> None:
    result = sail_db.get_table_info_no_throw(["nonexistent_table"])
    assert "Error" in result


def test_run_query(sail_db: SailSQL) -> None:
    result = sail_db.run("SELECT * FROM test_employees WHERE salary > 100000")
    assert "Alice" in result
    assert "Charlie" in result


def test_run_query_fetch_one(sail_db: SailSQL) -> None:
    result = sail_db.run("SELECT * FROM test_employees ORDER BY salary", fetch="one")
    assert "Bob" in result


def test_run_no_throw(sail_db: SailSQL) -> None:
    result = sail_db.run_no_throw("SELECT COUNT(*) FROM test_employees")
    assert "3" in result


def test_run_no_throw_invalid(sail_db: SailSQL) -> None:
    result = sail_db.run_no_throw("SELECT * FROM nonexistent_table")
    assert "Error" in result


def test_query_tool(sail_db: SailSQL) -> None:
    tool = QuerySailSQLTool(db=sail_db)
    result = tool.invoke("SELECT name FROM test_employees WHERE salary = 120000")
    assert "Alice" in result


def test_list_tool(sail_db: SailSQL) -> None:
    tool = ListSailSQLTool(db=sail_db)
    result = tool.invoke("")
    assert "test_employees" in result


def test_info_tool(sail_db: SailSQL) -> None:
    tool = InfoSailSQLTool(db=sail_db)
    result = tool.invoke("test_employees")
    assert "CREATE TABLE test_employees" in result
    assert "name" in result
