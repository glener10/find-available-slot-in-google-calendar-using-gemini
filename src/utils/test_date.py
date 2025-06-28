import unittest
from unittest.mock import patch

from .date import format_datetime, get_local_timezone_name


class TestFormatDatetime(unittest.TestCase):
  def test_format_datetime_success_case(self):
    """
    Test string formatting a datetime string in ISO 8601 format
    """
    input_str = "2024-07-26T10:30:55"
    expected = "2024-07-26 10:30"

    result = format_datetime(input_str)

    self.assertEqual(result, expected)

  def test_format_datetime_invalid_input(self):
    """
    Tests if the function raises a ValueError when receiving a string in a date/time format other than ISO 8601.
    """
    invalid_input = "28/06/2025 18:30:00"

    with self.assertRaises(ValueError):
      format_datetime(invalid_input)


class TestGetLocalTimezoneName(unittest.TestCase):
  @patch("src.utils.date.tzlocal")
  def test_get_local_timezone_name_success(self, mock_tzlocal):
    """
    Tests that the function correctly returns the local timezone name by mocking the external library.
    """
    expected_timezone = "America/Sao_Paulo"
    mock_tzlocal.get_localzone.return_value = expected_timezone

    result = get_local_timezone_name()

    self.assertEqual(result, expected_timezone)
    mock_tzlocal.get_localzone.assert_called_once()


if __name__ == "__main__":
  unittest.main()
