import unittest

from tc_hivemind_backend.db.credentials import (
    load_postgres_credentials,
    load_qdrant_credentials,
)


class TestCredentialLoadings(unittest.TestCase):
    def test_postgres_envs_type(self):
        postgres_creds = load_postgres_credentials()

        self.assertIsInstance(postgres_creds, dict)

    def test_postgres_envs_values(self):
        postgres_creds = load_postgres_credentials()

        self.assertNotEqual(postgres_creds["host"], None)
        self.assertNotEqual(postgres_creds["password"], None)
        self.assertNotEqual(postgres_creds["user"], None)
        self.assertNotEqual(postgres_creds["port"], None)

        self.assertIsInstance(postgres_creds["host"], str)
        self.assertIsInstance(postgres_creds["password"], str)
        self.assertIsInstance(postgres_creds["user"], str)
        self.assertIsInstance(postgres_creds["port"], str)

    def test_load_qdrant_creds(self):
        qdrant_creds = load_qdrant_credentials()

        self.assertIsNotNone(qdrant_creds["host"])
        self.assertIsNotNone(qdrant_creds["port"])
        self.assertIsNotNone(qdrant_creds["api_key"])
