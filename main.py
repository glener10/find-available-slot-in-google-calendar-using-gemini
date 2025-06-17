#TODO: use AI to ask when you want the event and handle errors
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from usecases.scheduler import find_next_available_slot, get_credentials, find_events, format_events, create_event

EVENTS_SEARCH_NUM_WEEKS=2
EVENT_GAP_INTERVAL_MINUTES = 30

def main():
  creds = get_credentials()

  try:
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    future_date = now + datetime.timedelta(weeks=EVENTS_SEARCH_NUM_WEEKS)
    timeMin = now.isoformat()
    timeMax = future_date.isoformat()

    print(f"getting all events between {timeMin} and {timeMax}")
    events = find_events(service, timeMin, timeMax)

    if not events:
      #TODO: no events is not an error
      print(f"no events in this interval")
      return

    print(f"found {len(events)} events")
    formatted_events = format_events(events)

    next_available_slot = find_next_available_slot(
        formatted_events, EVENT_GAP_INTERVAL_MINUTES
    )

    print(f"next available slot: {next_available_slot}")

    user_input = input(f"do you want to create an event at the suggested time ({next_available_slot})? (y/n): ")
    if user_input.strip().lower() == "y":
      created_event = create_event(service, next_available_slot, EVENT_GAP_INTERVAL_MINUTES)
      print(f"event created: {created_event.get('htmlLink')}")
    else:
      print("okay, not creating an event")

  except HttpError as error:
    print(f"an error occurred: {error}")


if __name__ == "__main__":
  start_time = datetime.datetime.now()
  print(f"🚀 starting process at {start_time}")

  main()

  end_time = datetime.datetime.now()
  total_time = end_time - start_time
  print(f"⏱️ execution finished. Total time: {total_time}")
