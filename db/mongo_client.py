from typing import Any, Dict, List
from pymongo import MongoClient


class MONGO_DB:
    def __init__(self, cfg: Dict[str, Any]) -> None:
        """
        Initializes the MongoDB client, database, and collection using configuration settings.
        :param cfg: A dictionary containing connection string, database name, and collection name.
        """
        self.client: Any = MongoClient(cfg['mongo_client'])
        self.db: Any = self.client[cfg['mongo_db']]
        self.collection: Any = self.db[cfg['mongo_collection']]


    def insert_log_into_mongo_db(self, doc: Dict[str, Any]) -> Any:
        """
        Inserts a single log document into the MongoDB collection.
        :param doc: A dictionary representing the search telemetry log payload.
        :return: InsertOneResult object containing the inserted document ID.
        """
        return self.collection.insert_one(doc)


    def get_top_5_frequent(self) -> List[Dict[str, Any]]:
        """
        Executes an aggregation pipeline to find the top 5 most frequent search keywords.
        :return: A list of dictionaries containing grouped keywords and their query count.
        """
        pipeline: List[Dict[str, Any]] = [
            {"$match": {"search_type": "keyword", "params.keyword": {"$exists": True, "$ne": ""}}},
            {"$group": {"_id": "$params.keyword", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        return list(self.collection.aggregate(pipeline))


    def get_top_5_recent(self) -> List[Dict[str, Any]]:
        """
        Fetches the top 5 most recently executed movie search logs.
        :return: A list of the 5 latest log dictionaries sorted by timestamp.
        """
        return list(self.collection.find({}).sort("timestamp", -1).limit(5))


    def __enter__(self) -> "MONGO_DB":
        """
        Enters the runtime context related to this object for use in a with-statement.
        :return: The instance of the MONGO_DB class itself.
        """
        return self


    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exits the runtime context and ensures the MongoDB connection is closed safely.
        :param exc_type: The type of the exception raised within the with-block, if any.
        :param exc_val: The instance of the exception raised within the with-block, if any.
        :param exc_tb: The traceback object associated with the exception, if any.
        :return: None
        """
        if not self.client:
            print('Not connected!')
        else:
            self.client.close()