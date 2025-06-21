import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.usecases.scheduler import get_credentials, find_events, format_events, create_event
from src.usecases.gemini import find_next_available_slot
from src.utils.date import format_datetime
from src.utils.args import get_args

def main():
  args = get_args()
  creds = get_credentials()

  try:
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    timeMin = (now + datetime.timedelta(minutes=int(args.waiting))).isoformat()
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeMax = end_of_day.isoformat()

    print(f"🔎 getting all events between {format_datetime(timeMin)} and {format_datetime(timeMax)}")
    events = find_events(service, timeMin, timeMax, args.id)

    print(f"☑ found {len(events)} events")
    formatted_events = format_events(events)

    ai_finding_next_availabe_slot = find_next_available_slot(formatted_events, args.start, args.end, args.duration)

    if ai_finding_next_availabe_slot.lower() == "no available slots":
      print("❌ no available slots found")
      return

    user_input = input(f"❔ do you want to create the event '{args.name}' at {ai_finding_next_availabe_slot} during {args.duration} minutes? (y/n): ")
    if user_input.strip().lower() == "y":
      created_event = create_event(service, ai_finding_next_availabe_slot, args.duration, args.name, args.invites, args.id)
      print(f"✅ event created: {created_event.get('htmlLink')}")
    else:
      print("okay, bye! 👋")

  except HttpError as error:
    print(f"🙁 an error occurred: {error}")


if __name__ == "__main__":
  start_time = datetime.datetime.now()
  print(f"🚀 starting process at {start_time}")

  main()

  end_time = datetime.datetime.now()
  total_time = end_time - start_time
  print(f"⏱️ execution finished. Total time: {total_time}")
