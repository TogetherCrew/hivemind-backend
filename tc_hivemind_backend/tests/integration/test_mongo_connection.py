import os

from dotenv import load_dotenv
from pymongo import MongoClient
from tc_hivemind_backend.db.mongo import MongoSingleton


def test_mongo_env_variables():
    """
    test if the environment variables are loaded correctly
    """
    load_dotenv()

    host = os.getenv("MONGODB_HOST")
    port = os.getenv("MONGODB_PORT")
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASS")

    assert host is not None
    assert port is not None
    assert user is not None
    assert password is not None


def test_mongo_connection():
    """
    test connecting to mongodb
    """
    load_dotenv()

    mongo = MongoSingleton.get_instance()
    assert type(mongo.client) is MongoClient
