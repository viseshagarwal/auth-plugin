import unittest
from auth_plugin.jwt_auth import JWTAuth


class TestJWTAuth(unittest.TestCase):

    def setUp(self):
        self.secret_key = "test_secret_key"
        self.jwt_auth = JWTAuth(self.secret_key, token_expiration=1)

    def test_generate_and_decode_token(self):
        payload = {"user_id": 123}
        token = self.jwt_auth.generate_token(payload)
        self.assertIsNotNone(token, "Token should not be None")

        decoded_payload = self.jwt_auth.decode_token(token)
        self.assertEqual(
            decoded_payload["user_id"], 123, "Decoded user_id should match the payload"
        )

    def test_expired_token(self):
        payload = {"user_id": 123}
        token = self.jwt_auth.generate_token(payload)

        import time

        time.sleep(2)  # Wait for the token to expire

        with self.assertRaises(RuntimeError) as context:
            self.jwt_auth.decode_token(token)
        self.assertTrue(
            "Token has expired" in str(context.exception),
            "Expired token should raise a proper error",
        )

    def test_invalid_token(self):
        with self.assertRaises(RuntimeError) as context:
            self.jwt_auth.decode_token("invalid.token.value")
        self.assertTrue(
            "Invalid token" in str(context.exception),
            "Invalid token should raise a proper error",
        )


if __name__ == "__main__":
    unittest.main()
