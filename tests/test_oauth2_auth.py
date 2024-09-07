import unittest
from unittest.mock import patch, MagicMock
import requests
import logging
from auth_plugin.oauth2_auth import OAuth2Auth


class TestOAuth2Auth(unittest.TestCase):

    def setUp(self):
        self.auth = OAuth2Auth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            auth_url="http://auth.example.com",
            token_url="http://token.example.com",
        )

    def test_get_authorization_url(self):
        expected_url = "http://auth.example.com?client_id=test_client_id&redirect_uri=http://localhost/callback&response_type=code"
        auth_url = self.auth.get_authorization_url()
        self.assertEqual(auth_url, expected_url)

    @patch("requests.post")
    def test_get_access_token_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"access_token": "test_access_token"}
        mock_post.return_value = mock_response

        token = self.auth.get_access_token("test_code")
        self.assertEqual(token, "test_access_token")
        mock_post.assert_called_once_with(
            "http://token.example.com",
            data={
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "code": "test_code",
                "redirect_uri": "http://localhost/callback",
                "grant_type": "authorization_code",
            },
        )

    @patch("requests.post")
    @patch("logging.error")
    def test_get_access_token_failure(self, mock_logging_error, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Request failed")

        with self.assertRaises(RuntimeError):
            self.auth.get_access_token("test_code")

        mock_logging_error.assert_called_with(
            "Error getting access token: Request failed"
        )

    @patch("requests.post")
    @patch("logging.error")
    def test_get_access_token_unexpected_error(self, mock_logging_error, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.side_effect = KeyError("Key not found")
        mock_post.return_value = mock_response

        with self.assertRaises(RuntimeError):
            self.auth.get_access_token("test_code")

        # Check the actual logged message
        mock_logging_error.assert_called_with("Unexpected error: 'Key not found'")

    def test_authenticate_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.auth.authenticate("test_token")


if __name__ == "__main__":
    unittest.main()
