import unittest
from unittest.mock import patch, MagicMock
from .gemini import get_api_key, find_next_available_slot


class TestGetApiKey(unittest.TestCase):
  @patch("src.usecases.gemini.load_dotenv")
  @patch("os.getenv")
  def test_get_api_key_success(self, mock_getenv, mock_load_dotenv):
    """
    Tests if the function returns the API key when it exists.
    """
    expected_key = "fake_api_key_12345"
    mock_getenv.return_value = expected_key

    api_key = get_api_key()

    self.assertEqual(api_key, expected_key)
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_with("API_KEY")

  @patch("src.usecases.gemini.load_dotenv")
  @patch("os.getenv")
  def test_get_api_key_missing(self, mock_getenv, mock_load_dotenv):
    """
    Tests if the function raises an Exception when the API key is missing.
    """
    mock_getenv.return_value = None

    with self.assertRaises(Exception) as context:
      get_api_key()

    self.assertEqual("❌ missing API_KEY in .env", str(context.exception))
    mock_load_dotenv.assert_called_once()


class TestFindNextAvailableSlot(unittest.TestCase):
  @patch("src.usecases.gemini.genai.Client")
  @patch("src.usecases.gemini.get_local_timezone_offset")
  @patch("src.usecases.gemini.get_api_key")
  def test_find_next_available_slot_success(
    self, mock_get_api_key, mock_get_tz, mock_genai_client_class
  ):
    """
    should find next available slot in the calendar
    """
    mock_get_api_key.return_value = "fake-api-key"
    mock_get_tz.return_value = "-03:00"
    expected_response_str = "2025-06-28T20:30:00.000-03:00"

    mock_api_response = MagicMock()
    mock_api_response.text = expected_response_str

    mock_genai_instance = mock_genai_client_class.return_value
    mock_genai_instance.models.generate_content.return_value = mock_api_response

    result = find_next_available_slot(
      events="[]",
      attendance_time_start="09:00",
      attendance_time_end="21:00",
      attendance_minutes_duration=60,
      plus_waiting_time="2025-06-28T19:02:16",
    )

    self.assertEqual(result, expected_response_str)
    mock_get_api_key.assert_called_once()
    mock_get_tz.assert_called_once()
    mock_genai_instance.models.generate_content.assert_called_once()
    call_kwargs = mock_genai_instance.models.generate_content.call_args.kwargs
    prompt_sent_to_api = call_kwargs["contents"][0]
    self.assertIn("The event must last 60 minutes", prompt_sent_to_api)
    self.assertIn("timezone is -03:00", prompt_sent_to_api)
    self.assertIn("now it is 2025-06-28T19:02:16", prompt_sent_to_api)

  @patch("src.usecases.gemini.genai.Client")
  @patch("src.usecases.gemini.get_local_timezone_offset")
  @patch("src.usecases.gemini.get_api_key")
  def test_find_next_available_slot_no_slots(
    self, mock_get_api_key, mock_get_tz, mock_genai_client_class
  ):
    """
    should handle no available slots response from the API
    """
    mock_get_api_key.return_value = "fake-api-key"
    mock_get_tz.return_value = "-03:00"
    mock_api_response = MagicMock()
    mock_api_response.text = "no available slots"
    mock_genai_instance = mock_genai_client_class.return_value
    mock_genai_instance.models.generate_content.return_value = mock_api_response

    result = find_next_available_slot([], "09:00", "10:00", 60, "2025-06-28T09:30:00")

    self.assertEqual(result, "no available slots")
