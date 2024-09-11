# sharehousepy

#### A python library to create and execute sharehouse queries

## File Tree

```
a6py/
├── a6py/
│ └── **init**.py
│ └── blocks.py
│ └── query.py
│ └── snowflake.py
├──── data/
│ └── country_geos.csv
├── docs/
│ └── ...
├── tests/
│ └── test.py
├── .env.example
├── .gitignore
├── licenses.json
├── README.md
├── requirements.txt
├── setup.py
└── LICENSE
```

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

# Access the results
print(f"Number of rows returned: {len(query.results)}")
for row in query.results[:5]:
    print(row)
```
