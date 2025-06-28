import unittest
from unittest.mock import patch, MagicMock

from .scheduler import format_events, find_events, create_event

class TestFormatEvents(unittest.TestCase):
  def test_format_events_with_events(self):
    """
    should format a list of events with start and end times.
    """
    events = [
        {
            'summary': 'Reunião de Alinhamento',
            'start': {'dateTime': '2025-06-29T10:00:00-03:00'},
            'end': {'dateTime': '2025-06-29T11:00:00-03:00'}
        }
    ]
    expected = ["Event Name: Reunião de Alinhamento - starts at 2025-06-29T10:00:00-03:00 ends at 2025-06-29T11:00:00-03:00"]
    
    result = format_events(events)
    
    self.assertEqual(result, expected)

  def test_format_events_with_events_during_all_day(self):
    """
    should format a list of all-day events with start and end dates.
    """
    events = [
        {'summary': 'Feriado Nacional', 'start': {'date': '2025-07-01'}, 'end': {'date': '2025-07-02'}}
    ]
    expected = ["Event Name: Feriado Nacional - starts at 2025-07-01 ends at 2025-07-02"]
    
    result = format_events(events)
    
    self.assertEqual(result, expected)

  def test_format_events_empty(self):
    """
    should return an empty list when no events are provided.
    """
    self.assertEqual(format_events([]), [])

class TestFindEvents(unittest.TestCase):
  def test_find_events_with_events(self):
    """
    should return a list of events from the API.
    """
    mock_service = MagicMock()
    fake_event_list = [{'id': '123', 'summary': 'Evento Teste'}]
    mock_service.events.return_value.list.return_value.execute.return_value = {
        'items': fake_event_list
    }

    result = find_events(mock_service, "timeMin", "timeMax", "primary")

    self.assertEqual(result, fake_event_list)
    mock_service.events.return_value.list.assert_called_once_with(
        calendarId='primary',
        timeMin='timeMin',
        timeMax='timeMax',
        maxResults=10,
        singleEvents=True,
        orderBy="startTime",
    )

  def test_find_events_without_events(self):
    """
    should return an empty list when no events are found.
    """
    mock_service = MagicMock()
    mock_service.events.return_value.list.return_value.execute.return_value = {}

    result = find_events(mock_service, "timeMin", "timeMax", "primary")
    
    self.assertEqual(result, [])

class TestCreateEvents(unittest.TestCase):
  @patch('src.usecases.scheduler.get_local_timezone_name')
  def test_create_event_com_convidados(self, mock_get_tz_name):
    """
    should create an event with attendees and verify the event body structure.
    """
    mock_service = MagicMock()
    mock_get_tz_name.return_value = "America/Sao_Paulo"
    fake_created_event = {'id': 'xyz', 'summary': 'Novo Evento'}
    mock_service.events.return_value.insert.return_value.execute.return_value = fake_created_event

    result = create_event(
        service=mock_service,
        next_available_slot="2025-06-29T15:00:00-03:00",
        event_duration_minutes=45,
        event_name="New test event",
        invites="test@gmail.com",
        calendar_id="primary"
    )

    self.assertEqual(result, fake_created_event)
    mock_service.events.return_value.insert.assert_called_once()
    call_kwargs = mock_service.events.return_value.insert.call_args.kwargs
    event_body = call_kwargs['body']
    expected_end_time = "2025-06-29T15:45:00-03:00"
    self.assertEqual(event_body['summary'], "New test event")
    self.assertEqual(event_body['attendees'][0]['email'], "test@gmail.com")
    self.assertEqual(event_body['start']['dateTime'], "2025-06-29T15:00:00-03:00")
    self.assertEqual(event_body['end']['dateTime'], expected_end_time)
    self.assertEqual(event_body['start']['timeZone'], "America/Sao_Paulo")