import unittest
from auth_plugin.utils import extract_token_from_header


class TestUtils(unittest.TestCase):

    def test_extract_token_from_valid_header(self):
        auth_header = "Bearer sometokenvalue"
        token = extract_token_from_header(auth_header)
        self.assertEqual(token, "sometokenvalue")

    def test_extract_token_from_invalid_header(self):
        auth_header = "Invalid header"
        token = extract_token_from_header(auth_header)
        self.assertIsNone(token)


if __name__ == "__main__":
    unittest.main()
