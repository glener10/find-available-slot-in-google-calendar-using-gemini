import argparse

def get_args():
  parser = argparse.ArgumentParser(description="using gemini to find available time slots in a google calendar api and create events")
  parser.add_argument('-s', '--start', required=False, default='09:00', help='attendance time start (default: 09:00)')
  parser.add_argument('-e', '--end', required=False, default='18:00', help='attendance time end (default: 18:00)')
  parser.add_argument('-d', '--duration', required=False, default='60', help='event duration in minutes (default: 60)')
  parser.add_argument('-n', '--name', required=False, default='Event created by Gemini', help='event name (default: "Event created by Gemini")')
  parser.add_argument('-id', '--id', required=False, default='primary', help='calendar id (default: "primary")')
  parser.add_argument('-i', '--invites', required=False, help='email to invite to the event, pass N emails separates by , (optional)')
  args = parser.parse_args()
  return args