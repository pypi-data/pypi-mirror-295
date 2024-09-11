class Query:
    """
    A class representing a query object for database operations.

    This class handles the composition and management of complex SQL queries,
    including nested queries and set operations (UNION, INTERSECT).

    :param query: An optional initial query string.
    :type query: str or None
    :param blocks: A list of query components to be composed.
    :type blocks: list or None

    :ivar query: The composed query string.
    :ivar blocks: The list of query components.
    :ivar status: The current status of the query (e.g., 'created', 'executed').
    :ivar id: An identifier for the query.
    :ivar results: A list to store query results.
    :ivar total_rows: The total number of rows returned by the query.
    :ivar total_partitions: The total number of partitions in the queried data.
    :ivar search_partitions: The number of partitions searched during query execution.
    :ivar search_bytes: The number of bytes searched during query execution.
    :ivar scanned_partitions: The number of partitions scanned during query execution.
    :ivar scanned_bytes: The number of bytes scanned during query execution.
    :ivar time: The total time taken for query execution.
    :ivar compilation_time: The time taken for query compilation.
    :ivar execution_time: The time taken for query execution.
    """

    def __init__(self, query=None, blocks=None):
        """
        Initialize a new Query instance.

        :param query: An optional initial query string.
        :type query: str or None
        :param blocks: A list of query components to be composed.
        :type blocks: list or None
        """
        self.query = query
        self.blocks = blocks
        self.status = 'created'
        self.id = None
        self.results = []
        self.total_rows = 0
        self.total_partitions = 0
        self.search_partitions = 0
        self.search_bytes = 0
        self.scanned_partitions = 0
        self.scanned_bytes = 0
        self.time = 0
        self.compilation_time = 0
        self.execution_time = 0

    def compose(self):
        """
        Compose the query from the provided blocks.

        This method processes the blocks to create a complete SQL query string.
        It handles nested queries and set operations (UNION, INTERSECT).

        :return: True if the composition was successful, False otherwise.
        :rtype: bool

        :raises ValueError: If there are invalid items in the blocks or if validation fails.

        .. note::
           This method sets the `query` attribute of the instance to the composed query string.
        """
        try:
            def process_blocks(blocks):
                """
                Recursively process blocks to compose the query.

                :param blocks: A list of query components.
                :type blocks: list
                :return: A composed query string.
                :rtype: str
                :raises ValueError: If there are invalid items in the blocks.
                """
                statements = []
                separator = None

                for item in blocks:
                    if isinstance(item, (tuple, list)):
                        nested_statement = process_blocks(item)
                        if nested_statement is None:
                            raise ValueError("Invalid nested block")
                        statements.append(f"({nested_statement})")
                    elif isinstance(item, str) and item.lower() in ('and', 'or'):
                        if separator is None:
                            separator = item.lower()
                        elif separator != item.lower():
                            raise ValueError("Mixed separators within parentheses")
                    elif hasattr(item, 'validate') and hasattr(item, 'compose'):
                        if item.validate():
                            item.compose()
                            if hasattr(item, 'statement') and item.statement:
                                statements.append(item.statement)
                        else:
                            raise ValueError("Validation failed for an item")
                    else:
                        raise ValueError("Invalid item in blocks")

                if not statements:
                    return ""

                if separator is None:
                    return " ".join(statements)
                elif separator == 'and':
                    return "\nintersect\n".join(statements)
                else:  # separator == 'or'
                    return "\nunion all\n".join(statements)

            self.query = process_blocks(self.blocks)
            return True
        except Exception as e:
            print(f"Error during query composition: {str(e)}")
            self.query = None
            return False
