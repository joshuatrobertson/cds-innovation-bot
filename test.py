import os
from pymongo import MongoClient
import datetime

from app import config

# Replace these variables with your actual details or manage them through environment variables
MONGO_URI = config.MONGO_URI
DATABASE_NAME = 'test'
COLLECTION_NAME = 'test_collection'  # You can change this if you have a specific collection in mind


def test_mongodb_connection(uri, db_name):
    print(f"Attempting to connect to MongoDB using URI: {uri}")  # Debugging output
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[COLLECTION_NAME]

    # Insert a test document
    post = {
        "author": "Josh",
        "text": "Hello MongoDB!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.now(datetime.UTC)
    }

    post_id = collection.insert_one(post).inserted_id
    print(f"Inserted post with ID: {post_id}")

    # Fetch the inserted document
    retrieved_post = collection.find_one({"_id": post_id})
    print("Retrieved Post:")
    print(retrieved_post)


if __name__ == '__main__':
    test_mongodb_connection(MONGO_URI, DATABASE_NAME)