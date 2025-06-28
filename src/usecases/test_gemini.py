import unittest
from unittest.mock import patch

from .gemini import get_api_key

class TestUsecaseGemini(unittest.TestCase):
    #get_api_key
    @patch('src.usecases.gemini.load_dotenv')
    @patch('os.getenv')
    def test_get_api_key_success(self, mock_getenv, mock_load_dotenv):
        """
        Tests if the function returns the API key when it exists.
        """
        expected_key = "fake_api_key_12345"
        mock_getenv.return_value = expected_key

        api_key = get_api_key()

        self.assertEqual(api_key, expected_key)
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_with('API_KEY')

    @patch('src.usecases.gemini.load_dotenv')
    @patch('os.getenv')
    def test_get_api_key_missing(self, mock_getenv, mock_load_dotenv):
        """
        Tests if the function raises an Exception when the API key is missing.
        """
        mock_getenv.return_value = None

        with self.assertRaises(Exception) as context:
            get_api_key()

        self.assertEqual("❌ missing API_KEY in .env", str(context.exception))
        mock_load_dotenv.assert_called_once()