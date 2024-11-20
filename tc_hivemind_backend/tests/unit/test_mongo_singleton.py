import logging
import unittest
from unittest.mock import MagicMock, patch

# Import the modules to test
from tc_hivemind_backend.db.mongo import MongoSingleton, get_mongo_uri


class TestMongoSingleton(unittest.TestCase):
    def setUp(self):
        """Reset the singleton instance before each test"""
        MongoSingleton._MongoSingleton__instance = None
        # Set up logging capture
        self.log_records = []
        self.logger = logging.getLogger()
        self.old_level = self.logger.level
        self.logger.setLevel(logging.INFO)
        self.handler = logging.Handler()
        self.handler.emit = lambda record: self.log_records.append(record)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        """Clean up after each test"""
        self.logger.removeHandler(self.handler)
        self.logger.setLevel(self.old_level)
        self.log_records = []

    def test_get_mongo_uri(self):
        """Test the get_mongo_uri function"""
        mock_credentials = {
            "user": "test_user",
            "password": "test_pass",
            "host": "test_host",
            "port": "27017",
        }

        with patch("tc_hivemind_backend.db.mongo.Credentials") as mock_creds:
            mock_creds.return_value.load_mongo.return_value = mock_credentials
            uri = get_mongo_uri()
            expected_uri = "mongodb://test_user:test_pass@test_host:27017"
            self.assertEqual(uri, expected_uri)

    def test_singleton_creation(self):
        """Test that only one instance of MongoSingleton can be created"""
        with patch("tc_hivemind_backend.db.mongo.MongoClient"):
            # First instance should be created successfully
            instance1 = MongoSingleton.get_instance()
            self.assertIsInstance(instance1, MongoSingleton)

            # Second instance should return the same object
            instance2 = MongoSingleton.get_instance()
            self.assertIs(instance1, instance2)

    def test_direct_instantiation_fails(self):
        """Test that direct instantiation fails after first instance"""
        with patch("tc_hivemind_backend.db.mongo.MongoClient"):
            # First instantiation should work
            _ = MongoSingleton()

            # Second instantiation should raise an exception
            with self.assertRaises(Exception) as context:
                MongoSingleton()
            self.assertEqual(str(context.exception), "This class is a singleton!")

    def test_successful_connection(self):
        """Test successful MongoDB connection logging"""
        with patch("tc_hivemind_backend.db.mongo.MongoClient") as mock_client:
            # Mock successful connection
            mock_client_instance = mock_client.return_value
            mock_client_instance.server_info.return_value = {"version": "4.4.0"}

            MongoSingleton.get_instance()

            # Verify logging
            log_messages = [record.getMessage() for record in self.log_records]
            self.assertTrue(
                any("MongoDB Connected Successfully!" in msg for msg in log_messages)
            )
            self.assertTrue(any("version" in msg for msg in log_messages))

    def test_failed_connection(self):
        """Test failed MongoDB connection logging"""
        with patch("tc_hivemind_backend.db.mongo.MongoClient") as mock_client:
            # Mock failed connection
            mock_client_instance = mock_client.return_value
            mock_client_instance.server_info.side_effect = Exception(
                "Connection failed"
            )

            MongoSingleton.get_instance()

            # Verify logging
            log_messages = [record.getMessage() for record in self.log_records]
            self.assertTrue(
                any("MongoDB not connected!" in msg for msg in log_messages)
            )
            self.assertTrue(any("Connection failed" in msg for msg in log_messages))

    def test_get_client(self):
        """Test get_client method returns MongoDB client"""
        with patch("tc_hivemind_backend.db.mongo.MongoClient") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance

            singleton = MongoSingleton.get_instance()
            client = singleton.get_client()

            self.assertIs(client, mock_instance)
