# sharehousepy

#### A python library to create and execute sharehouse queries

## Installation

```bash
pip install sharehousepy
```

## Usage

```python
from sharehousepy import Query, SnowflakeConnection

# Initialize a connection
sf_conn = SnowflakeConnection()

# Create a query
query = Query(query="SELECT * FROM zod_maid_default2 LIMIT 10")

# Run the query
sf_conn.run(query)

# Print the results
print(f"Results: {query.results[:10]}")
```
