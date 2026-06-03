from typing import Any, Dict, List, Optional, Union
import pymysql


class SQL_DB:
    def __init__(self, sql_conn: Dict[str, Any]) -> None:
        """
        Initializes the MySQL database connection using the provided configuration dictionary.
        :param sql_conn: A dictionary containing connection parameters for pymysql.connect.
        """
        self.conn: Any = pymysql.connect(**sql_conn)


    def select(self, query: str, params: Optional[Union[tuple, list, dict]] = None) -> List[Dict[str, Any]]:
        """
        Executes a SELECT SQL query and returns all fetched rows.
        :param query: The SQL query string to be executed.
        :param params: Optional query parameters (tuple, list, or dict) to safely interpolate into the SQL statement.
        :return: A list of dictionaries representing the fetched rows from the database.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


    def __enter__(self) -> "SQL_DB":
        """
        Enters the runtime context related to this object for use in a with-statement.
        :return: The instance of the SQL_DB class itself.
        """
        return self


    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exits the runtime context and ensures the database connection is closed safely.
        :param exc_type: The type of the exception raised within the with-block, if any.
        :param exc_val: The instance of the exception raised within the with-block, if any.
        :param exc_tb: The traceback object associated with the exception, if any.
        :return: None
        """
        self.conn.close()