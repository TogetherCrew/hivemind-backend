import unittest

from tc_hivemind_backend.db.credentials import Credentials
from tc_hivemind_backend.db.mongo import get_mongo_uri


class TestCredentialLoadings(unittest.TestCase):
    def setUp(self) -> None:
        self.credentials = Credentials()

    def test_postgres_envs_type(self):
        postgres_creds = self.credentials.load_postgres()

        self.assertIsInstance(postgres_creds, dict)

    def test_postgres_envs_values(self):
        postgres_creds = self.credentials.load_postgres()

        self.assertNotEqual(postgres_creds["host"], None)
        self.assertNotEqual(postgres_creds["password"], None)
        self.assertNotEqual(postgres_creds["user"], None)
        self.assertNotEqual(postgres_creds["port"], None)

        self.assertIsInstance(postgres_creds["host"], str)
        self.assertIsInstance(postgres_creds["password"], str)
        self.assertIsInstance(postgres_creds["user"], str)
        self.assertIsInstance(postgres_creds["port"], str)

    def test_load_qdrant_creds(self):
        qdrant_creds = self.credentials.load_qdrant()

        self.assertIsNotNone(qdrant_creds["host"])
        self.assertIsNotNone(qdrant_creds["port"])
        self.assertIsNotNone(qdrant_creds["api_key"])

    def test_mongo_envs_check_type(self):
        mongo_creds = self.credentials.load_mongo()

        self.assertIsInstance(mongo_creds, dict)

    def test_mongo_envs_values(self):
        mongo_creds = self.credentials.load_mongo()

        self.assertNotEqual(mongo_creds["user"], "")
        self.assertNotEqual(mongo_creds["password"], "")
        self.assertNotEqual(mongo_creds["host"], "")
        self.assertNotEqual(mongo_creds["port"], "")

        self.assertIsInstance(mongo_creds["user"], str)
        self.assertIsInstance(mongo_creds["password"], str)
        self.assertIsInstance(mongo_creds["host"], str)
        self.assertIsInstance(mongo_creds["port"], str)

    def test_redis_envs_check_type(self):
        redis_creds = self.credentials.load_redis()

        self.assertIsInstance(redis_creds, dict)

    def test_redis_envs_values(self):
        redis_creds = self.credentials.load_redis()

        self.assertIsNotNone(redis_creds["password"])
        self.assertIsNotNone(redis_creds["host"])
        self.assertIsNotNone(redis_creds["port"])

        self.assertIsInstance(redis_creds["password"], str)
        self.assertIsInstance(redis_creds["host"], str)
        self.assertIsInstance(redis_creds["port"], str)

    def test_config_mongo_creds(self):
        mongo_uri = get_mongo_uri()

        self.assertIsInstance(mongo_uri, str)
        self.assertIn("mongodb://", mongo_uri)
        self.assertNotIn("None", mongo_uri)
