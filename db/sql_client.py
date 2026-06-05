from typing import Any, Dict, List, Optional, Union
import pymysql


class SQL_DB:
    def __init__(self, sql_conn: Dict[str, Any]) -> None:
        """
        Initializes the database handler with connection configuration.
        :param sql_conn: A dictionary containing connection parameters for pymysql.connect.
        """
        self.config: Dict[str, Any] = sql_conn
        self.conn: Optional[Any] = None

    def __enter__(self) -> "SQL_DB":
        """
        Enters the runtime context and establishes the database connection.
        :return: The instance of the SQL_DB class itself.
        """
        try:
            self.conn = pymysql.connect(**self.config)
        except pymysql.MySQLError as e:
            print("╔" + "═" * 60 + "╗")
            print(f"║{"[Ошибка соединения] Не удалось подключиться к базе данных.".center(60) + '║'}")
            print("╚" + "═" * 60 + "╝")
            print(f"Проверьте интернет-соединение или параметры подключения.Детали: {e}")
            self.conn = None
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """
        Exits the runtime context, handles transactions, and safely closes the connection.
        :param exc_type: The type of the exception raised within the with-block, if any.
        :param exc_val: The instance of the exception raised within the with-block, if any.
        :param exc_tb: The traceback object associated with the exception, if any.
        :return: False to allow any raised exceptions to propagate normally.
        """
        if exc_type and issubclass(exc_type, pymysql.MySQLError):
            print("╔" + "═" * 100 + "╗")
            print(f"║{"[Ошибка сети] Соединение с базой данных было разорвано во время выполнения запроса.".center(100) + '║'}")
            print("╚" + "═" * 100 + "╝")
            print(f"Детали ошибки: {exc_val}\n")
            if self.conn:
                try:
                    self.conn.close()
                except pymysql.MySQLError:
                    pass
                finally:
                    self.conn = None
            return True

        if self.conn:
            try:
                pass
            finally:
                self.conn.close()
                self.conn = None
        return False

    def select(self, query: str, params: Optional[Union[tuple, list, dict]] = None) -> List[Dict[str, Any]] | None:
        """
        Executes a SELECT SQL query and returns all fetched rows.
        :param query: The SQL query string to be executed.
        :param params: Optional query parameters to safely interpolate into the SQL statement.
        :return: A list of dictionaries representing the fetched rows from the database.
        """
        if not self.conn:
            return None

        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
