import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def get_credentials():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds

def find_events(service, timeMin, timeMax):
  events_result = (
      service.events()
      .list(
          calendarId="primary",
          timeMin=timeMin,
          timeMax=timeMax,
          maxResults=10,
          singleEvents=True,
          orderBy="startTime",
      )
      .execute()
  )
  return events_result.get("items", [])

def format_events(events):
  formatted_events = []
  for event in events:
    formatted_event = f"{event.get('summary')} - {event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))} to {event.get('end', {}).get('dateTime', event.get('end', {}).get('date'))}"
    formatted_events.append(formatted_event)
  return formatted_events

def find_next_available_slot(formatted_events, gap_minutes):
  parsed_events = []
  for event_str in formatted_events:
    parts = event_str.split(' | ')
    if len(parts) >= 3:
      start_str = parts[1]
      end_str = parts[2]

      try:
        start_dt = datetime.datetime.fromisoformat(start_str)
        end_dt = datetime.datetime.fromisoformat(end_str)
        parsed_events.append((start_dt, end_dt))
      except ValueError:
        try:
          start_dt = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
          end_dt = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
          parsed_events.append((start_dt, end_dt))
        except ValueError:
          print(f"could not parse event date/time: {event_str}")
          raise ValueError(f"could not parse event date/time: {event_str}")

  parsed_events.sort(key=lambda x: x[0])
  now = datetime.datetime.now()
  current_time = now

  for i in range(len(parsed_events)):
    event_start = parsed_events[i][0]
    event_end = parsed_events[i][1]

    if event_start > current_time:
      time_until_next_event = event_start - current_time
      if time_until_next_event >= datetime.timedelta(minutes=gap_minutes):
        return current_time.isoformat()

    if event_end > current_time:
      current_time = event_end

  return current_time.isoformat()

def create_event(service, next_available_slot, EVENT_GAP_INTERVAL_MINUTES):
  TIME_ZONE = "America/Sao_Paulo"
  event = {
    "summary": "Scheduler API Test Event",
    "start": {"dateTime": next_available_slot, "timeZone": TIME_ZONE},
    "end": {
      "dateTime": (
      datetime.datetime.fromisoformat(next_available_slot) +
      datetime.timedelta(minutes=EVENT_GAP_INTERVAL_MINUTES)
      ).isoformat(),
      "timeZone": TIME_ZONE
    },
  }
  return service.events().insert(calendarId="primary", body=event).execute()