import unittest
from auth_plugin.oauth2_auth import OAuth2Auth


class TestOAuth2Auth(unittest.TestCase):

    def setUp(self):
        self.oauth2_auth = OAuth2Auth(
            client_id="testclientid",
            client_secret="testclientsecret",
            redirect_uri="http://localhost/callback",
            auth_url="http://localhost/auth",
            token_url="http://localhost/token",
        )

    def test_get_authorization_url(self):
        url = self.oauth2_auth.get_authorization_url()
        expected_url = "http://localhost/auth?client_id=testclientid&redirect_uri=http://localhost/callback&response_type=code"
        self.assertEqual(url, expected_url)


if __name__ == "__main__":
    unittest.main()
