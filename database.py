import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27000")
MONGO_DB = os.getenv("MONGO_DB", "student_db")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[MONGO_DB]


def test_connection():
    try:
        client.admin.command("ping")
        return True
    except ServerSelectionTimeoutError:
        return False


def close_connection():
    client.close()
