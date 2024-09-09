from dotenv import load_dotenv
from pymongo import MongoClient

import os


load_dotenv()


def get_db_handler(database_name: str):
    client = MongoClient(
        host=os.getenv("MONGODB_HOST"),
        port=int(os.getenv("MONGODB_PORT")),
        username=os.getenv("MONGODB_USERNAME"),
        password=os.getenv("MONGODB_PASSWORD"),
    )
    return client[database_name]


if __name__ == "__main__":
    db = get_db_handler("md410_2024_conv")
    print(db.list_collection_names())
