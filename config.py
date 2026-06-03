import os
from dotenv import load_dotenv
import pymysql

load_dotenv('.env')

config_sql = {
    'host': os.getenv('SQL_HOST'),
    'user': os.getenv('SQL_USER'),
    'password': os.getenv('SQL_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'cursorclass': pymysql.cursors.DictCursor,
}

config_mongo = {
    'mongo_client': os.getenv('MONGO_URI'),
    'mongo_db': os.getenv('MONGO_DB'),
    'mongo_collection': os.getenv('MONGO_COLLECTION'),
}
