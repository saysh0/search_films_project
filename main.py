from code import Client
from config import config_mongo, config_sql
from db.mongo_client import MONGO_DB
from db.sql_client import SQL_DB
from ui import UI


def start_app() -> None:
    """
    Initializes database engines and starts the main UI application loop
    using a safe context manager session for MongoDB logging.
    """
    sql: SQL_DB = SQL_DB(config_sql)
    code: Client = Client(sql)

    with MONGO_DB(config_mongo) as mongo:
        menu: UI = UI(code, mongo)

        menu.clear_screen()
        menu.start()

if __name__ == '__main__':
    start_app()
