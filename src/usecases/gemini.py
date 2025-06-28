import os

from dotenv import load_dotenv
from google import genai

from src.utils.date import get_local_timezone_offset

MODEL = "gemini-2.5-flash-preview-05-20"


def get_api_key():
  load_dotenv()
  api_key = os.getenv("API_KEY")
  if not api_key:
    raise Exception("❌ missing API_KEY in .env")
  return api_key


def find_next_available_slot(
  events,
  attendance_time_start,
  attendance_time_end,
  attendance_minutes_duration,
  plus_waiting_time,
):
  client = genai.Client(api_key=get_api_key())
  tz = get_local_timezone_offset()
  prompt = (
    f"You are an event scheduling agent. Your task is to find the next available time slot to schedule an event.\n"
    f"The event must last {attendance_minutes_duration} minutes.\n"
    f"You cannot return a time when there are already registered events.\n"
    f"Pay attention in timezone, the timezone is {tz}.\n"
    f"Pay attention to the start and end time of each event and timezone, the calendar with the events already occupied are these:\n{events}\n\n"
    f"ATTENTION HEAR! YOU CAN ONLY SEARCH FOR TIMES TODAY (cannot create the event at a time that has already passed, now it is {plus_waiting_time}) and if they are between {attendance_time_start} and {attendance_time_end} which is the defined business hours.\n"
    f"No worry if there are no available slots, respond with 'no available slots'. \n"
    f"Respond ONLY with the date and time of the next available slot in the ISO 8601 format 'YYYY-MM-DDTHH:MM:SS.sss{tz} (I will use your response directly in new Date(), so it must be ONLY that, nothing else)'.\n"
    f"If you find more than one event, send just the first one.\n"
  )
  return client.models.generate_content(model=MODEL, contents=[prompt]).text.strip()
