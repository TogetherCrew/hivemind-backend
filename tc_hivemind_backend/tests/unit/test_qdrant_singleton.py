import unittest
from unittest.mock import MagicMock, patch

from tc_hivemind_backend.db.qdrant import QdrantSingleton


class TestQdrantSingleton(unittest.TestCase):
    def setUp(self):
        QdrantSingleton._QdrantSingleton__instance = None

    def test_singleton_pattern(self):
        instance1 = QdrantSingleton.get_instance()
        instance2 = QdrantSingleton.get_instance()

        self.assertIs(instance1, instance2)

        with self.assertRaises(Exception) as context:
            QdrantSingleton()
        self.assertEqual(str(context.exception), "This class is a singleton!")

    @patch("tc_hivemind_backend.db.qdrant.load_qdrant_credentials")
    @patch("tc_hivemind_backend.db.qdrant.QdrantClient")
    def test_initialization_without_api_key(
        self, mock_qdrant_client, mock_load_credentials
    ):
        mock_load_credentials.return_value = {
            "host": "test_host",
            "port": 6333,
            "api_key": "",
        }

        instance = QdrantSingleton.get_instance()

        mock_qdrant_client.assert_called_once_with(host="test_host", port=6333)

        self.assertEqual(instance.get_client(), mock_qdrant_client.return_value)

    @patch("tc_hivemind_backend.db.qdrant.load_qdrant_credentials")
    @patch("tc_hivemind_backend.db.qdrant.QdrantClient")
    def test_initialization_with_api_key(
        self, mock_qdrant_client, mock_load_credentials
    ):
        mock_load_credentials.return_value = {
            "host": "test_host",
            "port": 6333,
            "api_key": "test_api_key",
        }

        instance = QdrantSingleton.get_instance()

        mock_qdrant_client.assert_called_once_with(
            host="test_host", port=6333, api_key="test_api_key", https=False
        )

        self.assertEqual(instance.get_client(), mock_qdrant_client.return_value)

    @patch("tc_hivemind_backend.db.qdrant.load_qdrant_credentials")
    @patch("tc_hivemind_backend.db.qdrant.QdrantClient")
    @patch("logging.info")
    @patch("logging.error")
    def test_successful_connection(
        self, mock_error_log, mock_info_log, mock_qdrant_client, mock_load_credentials
    ):
        mock_load_credentials.return_value = {
            "host": "test_host",
            "port": 6333,
            "api_key": "test_api_key",
        }

        mock_client = MagicMock()
        mock_client.get_collections.return_value = []
        mock_qdrant_client.return_value = mock_client

        QdrantSingleton.get_instance()

        mock_info_log.assert_called_once_with("QDrant Connected Successfully!")
        mock_error_log.assert_not_called()

    @patch("tc_hivemind_backend.db.qdrant.load_qdrant_credentials")
    @patch("tc_hivemind_backend.db.qdrant.QdrantClient")
    @patch("logging.info")
    @patch("logging.error")
    def test_failed_connection(
        self, mock_error_log, mock_info_log, mock_qdrant_client, mock_load_credentials
    ):
        mock_load_credentials.return_value = {
            "host": "test_host",
            "port": 6333,
            "api_key": "test_api_key",
        }

        mock_client = MagicMock()
        mock_client.get_collections.side_effect = Exception("Connection failed")
        mock_qdrant_client.return_value = mock_client

        QdrantSingleton.get_instance()

        mock_error_log.assert_called_once_with(
            "QDrant not connected! exp: Connection failed"
        )
        mock_info_log.assert_not_called()

    @patch("tc_hivemind_backend.db.qdrant.load_qdrant_credentials")
    def test_credentials_loading_error(self, mock_load_credentials):
        mock_load_credentials.side_effect = Exception("Failed to load credentials")

        with self.assertRaises(Exception) as context:
            QdrantSingleton.get_instance()
        self.assertEqual(str(context.exception), "Failed to load credentials")
