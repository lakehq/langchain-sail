# langchain-sail

LangChain integration for [Sail](https://github.com/lakehq/sail), a drop-in replacement for Apache Spark.

## Installation

```bash
pip install langchain-sail
```

To run a local Sail server for development/testing:

```bash
pip install pysail
```

## Usage

```python
from pysail.spark import SparkConnectServer
from pyspark.sql import SparkSession
from langchain_sail import SailSQL, SailSQLToolkit, create_sail_sql_agent

# Start a local Sail server
server = SparkConnectServer()
server.start()
_, port = server.listening_address

# Connect via SailSQL
spark = SparkSession.builder.remote(f"sc://localhost:{port}").getOrCreate()
sail = SailSQL(spark_session=spark)

# Use with an LLM agent
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6")
toolkit = SailSQLToolkit(db=sail, llm=llm)
agent = create_sail_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

result = agent.invoke({"input": "What tables are available?"})
print(result["output"])
```

## What is Sail?

[Sail](https://docs.lakesail.com/) is a drop-in replacement for Apache Spark, written in Rust. It uses the Spark Connect protocol, so existing PySpark code works out of the box — just point your `SparkSession` at a Sail server instead of a Spark cluster.
