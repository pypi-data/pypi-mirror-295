import snowflake.connector
from a6py.query import Query
from dotenv import load_dotenv
from tqdm import tqdm
import time
import os
from yaspin import yaspin


load_dotenv(override=True)

class SnowflakeConnection:
    """
    A class to manage connections and operations with Snowflake.

    This class handles the connection to Snowflake, execution of queries,
    and retrieval of results. It uses environment variables for configuration.

    :ivar username: Snowflake username from environment variable.
    :type username: str
    :ivar password: Snowflake password from environment variable.
    :type password: str
    :ivar account: Snowflake account from environment variable.
    :type account: str
    :ivar database: Snowflake database from environment variable.
    :type database: str
    :ivar connected: Flag indicating if a connection has been established.
    :type connected: bool
    :ivar connection: The Snowflake connection object.
    :type connection: snowflake.connector.SnowflakeConnection or None

    Example:
        >>> from a6py.snowflake import SnowflakeConnection
        >>> from a6py.query import Query
        >>> 
        >>> # Initialize the connection
        >>> sf_conn = SnowflakeConnection()
        >>> 
        >>> # Create a query
        >>> query = Query(query="SELECT * FROM zod_maid_default2 LIMIT 10")
        >>> 
        >>> # Run the query
        >>> sf_conn.run(query)
        >>> 
        >>> # Access the results
        >>> print(f"Number of rows returned: {len(query.total_rows)}")
        >>> for row in query.results[:5]:
        ...     print(row)
    """

    def __init__(self):
        """
        Initialize the SnowflakeConnection instance.

        Sets up the connection parameters from environment variables.
        """
        self.username = os.getenv('SNOWFLAKE_USERNAME')
        self.password = os.getenv('SNOWFLAKE_PASSWORD')
        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.database = os.getenv('SNOWFLAKE_DATABASE')
        self.connected = False
        self.connection = None

    def connect(self):
        """
        Establish a connection to Snowflake.

        Uses the credentials provided in the environment variables to connect to Snowflake.
        Sets the 'connected' flag to True if successful.

        Raises:
            Exception: Any exception that occurs during the connection process.
        """
        try:
            self.connection = snowflake.connector.connect(
                user=self.username,
                password=self.password,
                account=self.account,
                database=self.database
            )
            self.connected = True
        except Exception as e:
            print(f'Unable to connect to Snowflake\nError: {e}')

    def execute_query(self, query: Query):
        """
        Execute a SQL query on the connected Snowflake database.

        Args:
            query (Query): A Query object containing the SQL query to execute.

        Raises:
            Exception: Any exception that occurs during query execution.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"use warehouse {os.getenv('SNOWFLAKE_2XL_WAREHOUSE')};")
            query.id = cursor.execute(query.query, _no_results=True)['queryId']
            query.status = 'running'
        except Exception as e:
            print(f'Unable to execute query in Snowflake\nError: {e}')

    def explain_query(self, query: Query) -> bool:
        """
        Execute an EXPLAIN statement for the given query to validate it and update query attributes.

        Args:
            query (Query): The Query object containing the SQL query to explain.

        Returns:
            bool: True if the query is valid, False otherwise.

        Raises:
            Exception: Any exception that occurs during the EXPLAIN process.
        """
        try:
            with yaspin(text="Validating query...", color="green") as spinner:
                cursor = self.connection.cursor()
                cursor.execute(f"use warehouse {os.getenv('SNOWFLAKE_2XL_WAREHOUSE')};")
                cursor.execute(f"EXPLAIN {query.query}")
                rows = cursor.fetchall()
                if len(rows) > 1:
                    info_row = rows[0]
                    query.total_partitions = info_row[7]
                    query.search_partitions = info_row[8]
                    query.search_bytes = info_row[9] 
                spinner.text = ""
                spinner.ok("✅ Query Validated")
            return True
        except Exception as e:
            print(f'Query Error: {e}')
            return False

    def check_query_status(self, query: Query):
        """
        Check the status of a submitted query using the Snowflake query history table.

        Updates the Query object with the latest status and statistics.

        Args:
            query (Query): The Query object associated with the query being checked.

        Raises:
            Exception: Any exception that occurs during the status check.
        """
        try:
            cursor = self.connection.cursor()
            status_sql = f"""
            SELECT 
                execution_status, bytes_scanned, rows_produced, total_elapsed_time, compilation_time, execution_time
            FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
            WHERE QUERY_ID = '{query.id}'
            """
            cursor.execute(f"use warehouse {os.getenv('SNOWFLAKE_XS_WAREHOUSE')};")
            cursor.execute(status_sql)
            result = cursor.fetchone()
            if result:
                status, bytes_scanned, total_rows, total_ms, comp_time, exec_time = result
                query.status = status.lower()
                query.scanned_bytes = bytes_scanned
                query.total_rows = total_rows
                query.time = total_ms
                query.compilation_time = comp_time
                query.execution_time = exec_time    
            else:
                print(f"No information found for query ID: {query.id}")
        except Exception as e:
            print(f'Unable to check query status in Snowflake\nError: {e}')

    def get_query_results(self, query: Query, batch_size: int = 1_000_000, device_history: bool = False):
        """
        Retrieve the results of a completed query from Snowflake.

        Args:
            query (Query): The Query object containing the query information and results.
            batch_size (int, optional): The number of rows to fetch in each batch. Defaults to 1,000,000.
            device_history (bool, optional): Flag indicating whether to retrieve device history. Defaults to False.

        Raises:
            Exception: Any exception that occurs during result retrieval.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"use warehouse {os.getenv('SNOWFLAKE_2XL_WAREHOUSE')};")
            cursor.get_results_from_sfqid(query.id)
            if query.total_rows == 0:
                print("There are 0 results for your query")
            else:
                query.results = []
                with tqdm(total=query.total_rows, desc="Fetching results", unit="row", colour="GREEN", position=0, leave=True) as pbar:
                    while True:
                        rows = cursor.fetchmany(batch_size)
                        if not rows:
                            break
                        if len(rows[0]) == 1:
                            query.results.extend([row[0] for row in rows])
                        else:
                            query.results.extend(rows)
                        pbar.update(len(rows))
        except Exception as e:
            print(f'Unable to retrieve query results in Snowflake\nError: {e}')

    def run(self, query: Query):
        """
        Run a complete query workflow, from connection to result retrieval.

        This method handles the entire process of executing a query, including:
        - Connecting to Snowflake
        - Composing the query (if blocks are provided)
        - Explaining and validating the query
        - Executing the query
        - Monitoring query progress
        - Retrieving query results

        :param query: The Query object to run.
        :type query: Query
        """
        self.connect()

        if query.blocks is not None:
            if not query.compose():
                print("Error creating query (see error message above)")
                return
            if query.query is None:
                print("Error: Query is None after composition")
                return
        elif query.query is None and query.blocks is None:
            print("No query or blocks specified")
            return
        
        if self.explain_query(query):
            print(f"Scanning {query.search_partitions / query.total_partitions * 100:,.2f}% ({format_bytes(query.search_bytes)}) of total data")
            self.execute_query(query)
            
            with yaspin(text="Optimizing query...", color="green") as spinner:
                while query.execution_time == 0:
                    self.check_query_status(query)
                    if query.status == "success":
                        break
                    time.sleep(5)
                spinner.text = ""
                spinner.ok("✅ Query Optimized")
            
            with tqdm(total=100, desc="Query Progress", unit="%", colour="GREEN", position=0, leave=True) as pbar:
                last_progress = 0
                while True:
                    progress = min(95, round((query.scanned_bytes / query.search_bytes) * 100, 1))
                    pbar.update(progress - last_progress)
                    last_progress = progress
                    self.check_query_status(query)
                    if query.status == 'success':
                        pbar.update(100 - last_progress)
                        break
                    elif query.status not in ['running', 'resuming_warehouse']:
                        print(f"Unexpected query status: {query.status}")
                        break
                    time.sleep(5)
            print(f"Query completed in {(query.time / 1000):.0f} seconds")

            self.get_query_results(query)

def format_bytes(bytes_value):
    sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while bytes_value >= 1024 and i < len(sizes) - 1:
        bytes_value /= 1024.0
        i += 1
    return f"{bytes_value:.2f} {sizes[i]}"
    