# src/db.py
from pymongo import MongoClient
from src.config import DATABASE_URL

# Create a client to connect to your running MongoDB instance
client = MongoClient(DATABASE_URL)

# Get the database (it will be created if it doesn't exist)
db = client.trading_agent

# Get the collection (like a table in SQL)
trades_collection = db.trades