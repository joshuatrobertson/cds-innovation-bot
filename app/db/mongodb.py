import time
from datetime import datetime, timedelta

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

from app import config


# Function to get MongoDB client
def get_mongo_client(uri=config.MONGO_URI):
    try:
        client = MongoClient(uri)
        client.admin.command('ismaster')
        return client
    except ConnectionFailure:
        logging.error("Server not available")
        return None


# Function to add idea to the database
def add_idea(db_name, idea_data):
    client = get_mongo_client()
    if client is not None:
        db = client[db_name]
        db.ideas.insert_one(idea_data)
        client.close()
    else:
        logging.error("Failed to connect to MongoDB")


# Function to get the leaderboard for the last month
def get_ideas_leaderboard_for_month(db_name):
    client = get_mongo_client()
    if client is not None:
        db = client[db_name]
        one_month_ago = time.time() - timedelta(days=30).total_seconds()  # Get seconds since epoch 30 days ago
        pipeline = [
            {"$match": {"timestamp": {"$gte": one_month_ago}}},  # Compare as float
            {"$group": {
                "_id": "$user_name",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        results = list(db.ideas.aggregate(pipeline))
        client.close()
        return results
    else:
        logging.error("Failed to connect to MongoDB")
        return []


