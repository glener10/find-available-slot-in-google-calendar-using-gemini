import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.utils.date import get_local_timezone_name

SCOPES = [
  "https://www.googleapis.com/auth/calendar.readonly",
  "https://www.googleapis.com/auth/calendar.events",
]


def get_credentials():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds


def find_events(service, timeMin, timeMax, calendar_id):
  events_result = (
    service.events()
    .list(
      calendarId=calendar_id,
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
    formatted_event = f"Event Name: {event.get('summary')} - starts at {event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))} ends at {event.get('end', {}).get('dateTime', event.get('end', {}).get('date'))}"
    formatted_events.append(formatted_event)
  return formatted_events


def create_event(
  service, next_available_slot, event_duration_minutes, event_name, invites, calendar_id
):
  TIME_ZONE = str(get_local_timezone_name())
  attendees = []
  if invites:
    emails = [email.strip() for email in invites.split(",") if email.strip()]
    attendees = [{"email": email} for email in emails]

  event = {
    "summary": event_name,
    "attendees": attendees,
    "start": {"dateTime": next_available_slot, "timeZone": TIME_ZONE},
    "end": {
      "dateTime": (
        datetime.datetime.fromisoformat(next_available_slot)
        + datetime.timedelta(minutes=int(event_duration_minutes))
      ).isoformat(),
      "timeZone": TIME_ZONE,
    },
  }
  return service.events().insert(calendarId=calendar_id, body=event).execute()
