import unittest

from pymongo.mongo_client import MongoClient
from tc_hivemind_backend.db.mongo import MongoSingleton


class TestMongoSingletonIntegration(unittest.TestCase):
    """Separate test class for integration tests"""

    def setUp(self):
        """Reset the singleton instance before each test"""
        MongoSingleton._MongoSingleton__instance = None

    def test_real_connection(self):
        """Integration test for real MongoDB connection"""
        instance = MongoSingleton.get_instance()
        client = instance.get_client()
        self.assertIsInstance(client, MongoClient)

        # Test actual connection
        try:
            info = client.server_info()
            self.assertIsInstance(info, dict)
            self.assertIn("version", info)
        except Exception as e:
            self.fail(f"Failed to connect to MongoDB: {e}")
