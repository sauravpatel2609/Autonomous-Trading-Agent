# src/config.py
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from dotenv import load_dotenv

# This line loads the variables from your .env file into the environment
load_dotenv()

# Read keys from the environment; provide a default for local testing if you want
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- NEW: Database Client ---
try:
    db_client = MongoClient(DATABASE_URL)
    # The ismaster command is cheap and does not require auth.
    db_client.admin.command('ismaster')
    logging.info("MongoDB connection successful.")
except ConnectionFailure as e:
    logging.error(f"Could not connect to MongoDB: {e}")
    db_client = None
except Exception as e:
    logging.error(f"An error occurred during database connection: {e}")
    db_client = None