import unittest
import jwt
import time
import os
import sys

from auth_plugin.jwt_auth import JWTAuth


class TestJWTAuth(unittest.TestCase):

    def setUp(self):
        self.jwt_auth = JWTAuth(secret_key="testsecret")

    def test_generate_token(self):
        token = self.jwt_auth.generate_token(user_id=1)
        self.assertIsNotNone(token)

    def test_validate_token(self):
        token = self.jwt_auth.generate_token(user_id=1)
        user_id = self.jwt_auth.validate_token(token)
        self.assertEqual(user_id, 1)

    def test_expired_token(self):
        token = self.jwt_auth.generate_token(user_id=1, expires_in=1)
        time.sleep(2)
        user_id = self.jwt_auth.validate_token(token)
        self.assertIsNone(user_id)

    def test_invalid_token(self):
        token = "invalid.token.here"
        user_id = self.jwt_auth.validate_token(token)
        self.assertIsNone(user_id)


if __name__ == "__main__":
    unittest.main()
