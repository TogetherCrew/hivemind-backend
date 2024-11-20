import unittest
from unittest.mock import MagicMock, patch

from tc_hivemind_backend.db.redis import RedisSingleton


class TestRedisSingleton(unittest.TestCase):
    def setUp(self):
        RedisSingleton._RedisSingleton__instance = None

    def test_singleton_pattern(self):
        instance1 = RedisSingleton.get_instance()
        instance2 = RedisSingleton.get_instance()

        self.assertIs(instance1, instance2)

        with self.assertRaises(Exception) as context:
            RedisSingleton()
        self.assertEqual(str(context.exception), "This class is a singleton!")

    @patch("tc_hivemind_backend.db.redis.Credentials")
    @patch("redis.Redis")
    def test_initialization(self, mock_redis, mock_credentials):
        mock_credentials_instance = MagicMock()
        mock_credentials_instance.load_redis.return_value = {
            "host": "test_host",
            "port": "6379",
            "password": "test_password",
        }
        mock_credentials.return_value = mock_credentials_instance

        instance = RedisSingleton.get_instance()

        mock_redis.assert_called_once_with(
            host="test_host", port=6379, password="test_password", decode_responses=True
        )

        self.assertEqual(instance.get_client(), mock_redis.return_value)

    @patch("tc_hivemind_backend.db.redis.Credentials")
    @patch("redis.Redis")
    @patch("logging.info")
    @patch("logging.error")
    def test_successful_connection(
        self, mock_error_log, mock_info_log, mock_redis, mock_credentials
    ):
        mock_credentials_instance = MagicMock()
        mock_credentials_instance.load_redis.return_value = {
            "host": "test_host",
            "port": "6379",
            "password": "test_password",
        }
        mock_credentials.return_value = mock_credentials_instance

        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_redis.return_value = mock_client

        RedisSingleton.get_instance()

        mock_info_log.assert_called_once_with(
            "Redis Connected Successfully! Ping returned: True"
        )
        mock_error_log.assert_not_called()

    @patch("tc_hivemind_backend.db.redis.Credentials")
    @patch("redis.Redis")
    @patch("logging.info")
    @patch("logging.error")
    def test_failed_connection(
        self, mock_error_log, mock_info_log, mock_redis, mock_credentials
    ):
        mock_credentials_instance = MagicMock()
        mock_credentials_instance.load_redis.return_value = {
            "host": "test_host",
            "port": "6379",
            "password": "test_password",
        }
        mock_credentials.return_value = mock_credentials_instance

        mock_client = MagicMock()
        mock_client.ping.side_effect = Exception("Connection failed")
        mock_redis.return_value = mock_client

        RedisSingleton.get_instance()

        mock_error_log.assert_called_once_with(
            "Redis not connected! exp: Connection failed"
        )
        mock_info_log.assert_not_called()

    @patch("tc_hivemind_backend.db.redis.Credentials")
    def test_credentials_loading_error(self, mock_credentials):
        mock_credentials_instance = MagicMock()
        mock_credentials_instance.load_redis.side_effect = Exception(
            "Failed to load credentials"
        )
        mock_credentials.return_value = mock_credentials_instance

        with self.assertRaises(Exception) as context:
            RedisSingleton.get_instance()
        self.assertEqual(str(context.exception), "Failed to load credentials")


if __name__ == "__main__":
    unittest.main()
